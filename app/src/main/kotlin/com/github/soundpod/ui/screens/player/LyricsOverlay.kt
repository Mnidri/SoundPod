package com.github.musick.ui.screens.player

import android.widget.Toast
import androidx.compose.animation.core.animateFloatAsState
import androidx.compose.animation.core.tween
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.itemsIndexed
import androidx.compose.foundation.lazy.rememberLazyListState
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.ContentCopy
import androidx.compose.material.icons.filled.Language
import androidx.compose.material3.AlertDialog
import androidx.compose.material3.CircularProgressIndicator
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.Text
import androidx.compose.material3.TextButton
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.platform.LocalClipboardManager
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.AnnotatedString
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.media3.common.MediaMetadata
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.delay
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext
import org.json.JSONArray
import org.json.JSONObject
import java.io.File
import java.net.HttpURLConnection
import java.net.URL
import java.net.URLEncoder

data class LyricLine(val timeMs: Long, val text: String, val isSynced: Boolean, val translation: String? = null)

fun sanitizeTitle(input: String): String {
    var text = input.replace(Regex("\\(.*?\\)|\\[.*?\\]"), "")
    text = text.replace(Regex("(?i)\\b(ft\\.?|feat\\.?|featuring|prod\\.?|x|&)\\b.*"), "")
    return text.trim().replace(Regex("\\s+"), " ")
}

fun sanitizeArtist(input: String): String {
    var text = input.replace(Regex("\\(.*?\\)|\\[.*?\\]"), "")
    val parts = text.split(Regex("(?i)\\s*(ft\\.?|feat\\.?|featuring|prod\\.?|x|&|,|،|و)\\s*"))
    return parts.firstOrNull()?.trim()?.replace(Regex("\\s+"), " ") ?: ""
}

@Composable
fun LyricsOverlay(
    modifier: Modifier = Modifier,
    mediaId: String?,
    mediaMetadata: MediaMetadata?,
    playbackPositionProvider: () -> Long,
    onSeekToPosition: (Long) -> Unit
) {
    var lyricLines by remember { mutableStateOf<List<LyricLine>>(emptyList()) }
    var currentPositionMs by remember { mutableStateOf(0L) }
    var isLoading by remember { mutableStateOf(true) }
    val listState = rememberLazyListState()

    val clipboardManager = LocalClipboardManager.current
    val context = LocalContext.current
    val coroutineScope = rememberCoroutineScope()

    val prefs = context.getSharedPreferences("preferences", android.content.Context.MODE_PRIVATE)
    var geminiApiKey by remember { mutableStateOf(prefs.getString("geminiApiKey", "") ?: "") }
    var showApiDialog by remember { mutableStateOf(false) }
    var tempApiKey by remember { mutableStateOf("") }
    var isTranslating by remember { mutableStateOf(false) }

    LaunchedEffect(showApiDialog) {
        if (showApiDialog) tempApiKey = geminiApiKey
    }

    LaunchedEffect(mediaMetadata?.title, mediaMetadata?.artist, mediaId) {
        isLoading = true
        val safeMediaId = mediaId?.replace(Regex("[^a-zA-Z0-9.-]"), "_") ?: "unknown"
        val cacheFile = File(context.cacheDir, "lyrics_cache_$safeMediaId.json")
        var loadedFromCache = false

        // ۱. تلاش برای خواندن از حافظه کش
        withContext(Dispatchers.IO) {
            try {
                if (cacheFile.exists() && cacheFile.length() > 0) {
                    val jsonArray = JSONArray(cacheFile.readText())
                    val cachedLines = mutableListOf<LyricLine>()
                    for (i in 0 until jsonArray.length()) {
                        val obj = jsonArray.getJSONObject(i)
                        cachedLines.add(
                            LyricLine(
                                timeMs = obj.getLong("timeMs"),
                                text = obj.getString("text"),
                                isSynced = obj.getBoolean("isSynced"),
                                translation = if (obj.has("translation")) obj.getString("translation") else null
                            )
                        )
                    }
                    if (cachedLines.isNotEmpty()) {
                        withContext(Dispatchers.Main) { lyricLines = cachedLines }
                        loadedFromCache = true
                    }
                }
            } catch (e: Exception) { e.printStackTrace() }
        }

        // ۲. اگر در کش نبود، دانلود از اینترنت
        if (!loadedFromCache) {
            val rawTitle = mediaMetadata?.title?.toString() ?: ""
            val rawArtist = mediaMetadata?.artist?.toString() ?: ""
            val title = sanitizeTitle(rawTitle)
            val artist = sanitizeArtist(rawArtist)

            val fetchedLyrics = withContext(Dispatchers.IO) {
                var finalLyrics = ""
                try {
                    val useExactGet = title.isNotBlank() && artist.isNotBlank() && !title.equals(artist, ignoreCase = true)

                    if (useExactGet) {
                        val encodedTitle = URLEncoder.encode(title, "UTF-8")
                        val encodedArtist = URLEncoder.encode(artist, "UTF-8")
                        val getUrl = URL("https://lrclib.net/api/get?track_name=$encodedTitle&artist_name=$encodedArtist")
                        val conn1 = getUrl.openConnection() as HttpURLConnection
                        conn1.connectTimeout = 5000
                        
                        if (conn1.responseCode == 200) {
                            val json = JSONObject(conn1.inputStream.bufferedReader().readText())
                            if (!json.isNull("syncedLyrics")) finalLyrics = json.getString("syncedLyrics")
                            else if (!json.isNull("plainLyrics")) finalLyrics = json.getString("plainLyrics")
                        }
                    }

                    if (finalLyrics.isBlank() && rawTitle.isNotBlank()) {
                        val searchQuery = if (useExactGet) "$title $artist" else rawTitle.replace(Regex("[\\[\\]\\(\\)]"), "")
                        val encodedQuery = URLEncoder.encode(searchQuery.trim(), "UTF-8")
                        val searchUrl = URL("https://lrclib.net/api/search?q=$encodedQuery")
                        val conn2 = searchUrl.openConnection() as HttpURLConnection
                        conn2.connectTimeout = 5000
                        
                        if (conn2.responseCode == 200) {
                            val jsonArray = JSONArray(conn2.inputStream.bufferedReader().readText())
                            var bestSynced = ""; var bestPlain = ""
                            val titleLower = title.lowercase()

                            for (i in 0 until jsonArray.length()) {
                                val item = jsonArray.getJSONObject(i)
                                val apiTrackLower = item.optString("trackName", "").lowercase()
                                if (apiTrackLower.contains(titleLower) || titleLower.contains(apiTrackLower) || titleLower.isEmpty()) {
                                    if (!item.isNull("syncedLyrics") && item.getString("syncedLyrics").isNotBlank()) {
                                        bestSynced = item.getString("syncedLyrics"); break
                                    } else if (bestPlain.isBlank() && !item.isNull("plainLyrics")) {
                                        bestPlain = item.getString("plainLyrics")
                                    }
                                }
                            }
                            finalLyrics = bestSynced.ifBlank { bestPlain }
                        }
                    }

                    if (finalLyrics.isBlank() && title.isNotBlank() && artist.isNotBlank()) {
                        val encodedTitle = URLEncoder.encode(title, "UTF-8")
                        val encodedArtist = URLEncoder.encode(artist, "UTF-8")
                        val ovhUrl = URL("https://api.lyrics.ovh/v1/$encodedArtist/$encodedTitle")
                        val conn3 = ovhUrl.openConnection() as HttpURLConnection
                        conn3.connectTimeout = 5000
                        if (conn3.responseCode == 200) {
                            val json = JSONObject(conn3.inputStream.bufferedReader().readText())
                            if (!json.isNull("lyrics")) finalLyrics = json.getString("lyrics")
                        }
                    }
                } catch (e: Exception) { e.printStackTrace() }
                finalLyrics
            }

            val parsedLines = mutableListOf<LyricLine>()
            if (fetchedLyrics.isNotBlank()) {
                val cleanedLyrics = fetchedLyrics.replace(Regex("Paroles de la chanson.*\\r?\\n"), "")
                val lines = cleanedLyrics.split("\n")
                val regex = Regex("\\[(\\d{2}):(\\d{2})[\\.:](\\d{2,3})\\]")
                for (line in lines) {
                    val match = regex.find(line)
                    if (match != null) {
                        val m = match.groupValues[1].toLong()
                        val s = match.groupValues[2].toLong()
                        val ms = match.groupValues[3].padEnd(3, '0').toLong()
                        val timeMs = (m * 60 * 1000) + (s * 1000) + ms
                        val text = line.substring(match.range.last + 1).trim()
                        if (text.isNotEmpty()) parsedLines.add(LyricLine(timeMs, text, isSynced = true))
                    } else if (line.trim().isNotEmpty()) {
                        parsedLines.add(LyricLine(0L, line.trim(), isSynced = false))
                    }
                }
            }
            lyricLines = parsedLines

            // ۳. ذخیره در حافظه کش بعد از دانلود
            withContext(Dispatchers.IO) {
                try {
                    if (parsedLines.isNotEmpty()) {
                        val jsonArray = JSONArray()
                        for (line in parsedLines) {
                            val obj = JSONObject()
                            obj.put("timeMs", line.timeMs)
                            obj.put("text", line.text)
                            obj.put("isSynced", line.isSynced)
                            jsonArray.put(obj)
                        }
                        cacheFile.writeText(jsonArray.toString())
                    }
                } catch (e: Exception) { e.printStackTrace() }
            }
        }
        isLoading = false
    }

    LaunchedEffect(Unit) {
        while (true) {
            currentPositionMs = playbackPositionProvider()
            delay(100)
        }
    }

    val activeIndex = if (lyricLines.isEmpty() || !lyricLines.any { it.isSynced }) -1 else {
        var idx = -1
        for (i in lyricLines.indices) {
            if (currentPositionMs >= lyricLines[i].timeMs) idx = i else break
        }
        idx
    }

    LaunchedEffect(activeIndex) {
        if (activeIndex >= 0 && lyricLines[activeIndex].isSynced) {
            // بالا آوردن خط فعال: اسکرول به یک آیتم قبل‌تر
            listState.animateScrollToItem(maxOf(0, activeIndex - 1))
        }
    }

    Box(modifier = modifier.fillMaxSize()) {
        if (isLoading) {
            Text(
                text = "Searching for lyrics...", 
                color = Color.White, 
                fontSize = 22.sp, 
                fontWeight = FontWeight.Bold,
                modifier = Modifier.align(Alignment.Center)
            )
        } else if (lyricLines.isEmpty()) {
            Text(
                text = "No lyrics found", 
                color = Color.White.copy(alpha = 0.4f), 
                fontSize = 22.sp, 
                fontWeight = FontWeight.Bold,
                modifier = Modifier.align(Alignment.Center)
            )
        } else {
            LazyColumn(
                modifier = Modifier.fillMaxSize(), 
                state = listState, 
                // تنظیم فاصله‌ها برای قرار گرفتن متن در نیمه بالایی صفحه
                contentPadding = PaddingValues(top = 100.dp, bottom = 250.dp),
                horizontalAlignment = Alignment.CenterHorizontally
            ) {
                itemsIndexed(lyricLines) { index, line ->
                    val isCurrent = index == activeIndex && line.isSynced
                    val alpha by animateFloatAsState(targetValue = if (isCurrent) 1f else 0.4f, animationSpec = tween(500))

                    Column(
                        modifier = Modifier
                            .fillMaxWidth()
                            .padding(vertical = 14.dp, horizontal = 24.dp)
                            .clickable { if (line.isSynced) onSeekToPosition(line.timeMs) },
                        horizontalAlignment = Alignment.CenterHorizontally
                    ) {
                        Text(
                            text = line.text, 
                            color = Color.White.copy(alpha = alpha), 
                            fontSize = 26.sp,                   
                            fontWeight = FontWeight.ExtraBold,
                            textAlign = TextAlign.Center,
                            lineHeight = 38.sp
                        )
                        if (!line.translation.isNullOrBlank()) {
                            Text(
                                text = line.translation,
                                color = Color.White.copy(alpha = alpha * 0.85f),
                                fontSize = 18.sp, // افزایش سایز فونت فارسی
                                fontWeight = FontWeight.SemiBold, // کمی بولدتر برای خوانایی
                                textAlign = TextAlign.Center,
                                lineHeight = 28.sp,
                                modifier = Modifier.padding(top = 6.dp)
                            )
                        }
                    }
                }
            }
            
            IconButton(
                onClick = {
                    if (geminiApiKey.isBlank()) {
                        showApiDialog = true
                    } else if (!isTranslating) {
                        isTranslating = true
                        coroutineScope.launch(Dispatchers.IO) {
                            try {
                                val url = URL("https://generativelanguage.googleapis.com/v1beta/models/gemini-flash-lite-latest:generateContent?key=${geminiApiKey.trim()}")
                                val conn = url.openConnection() as HttpURLConnection
                                conn.requestMethod = "POST"
                                conn.setRequestProperty("Content-Type", "application/json")
                                conn.doOutput = true

                                val linesToTranslate = lyricLines.map { it.text.ifBlank { " " } }
                                val prompt = "You are an expert translator. Translate the following lyrics to Persian line by line. You MUST return EXACTLY the same number of lines (${linesToTranslate.size}). Output ONLY the translated Persian text line by line. DO NOT include markdown, intro, or any extra text.\n\n" + linesToTranslate.joinToString("\n")

                                val jsonPayload = JSONObject().apply {
                                    put("contents", JSONArray().apply {
                                        put(JSONObject().apply {
                                            put("parts", JSONArray().apply {
                                                put(JSONObject().apply { put("text", prompt) })
                                            })
                                        })
                                    })
                                }

                                conn.outputStream.use { it.write(jsonPayload.toString().toByteArray(Charsets.UTF_8)) }

                                if (conn.responseCode == 200) {
                                    val response = conn.inputStream.bufferedReader().readText()
                                    val responseJson = JSONObject(response)
                                    val generatedText = responseJson
                                        .getJSONArray("candidates")
                                        .getJSONObject(0)
                                        .getJSONObject("content")
                                        .getJSONArray("parts")
                                        .getJSONObject(0)
                                        .getString("text")

                                    val translatedLines = generatedText.split("\n")
                                    
                                    withContext(Dispatchers.Main) {
                                        lyricLines = lyricLines.mapIndexed { index, line ->
                                            line.copy(translation = translatedLines.getOrNull(index)?.trim())
                                        }
                                    }

                                    // آپدیت کش: ذخیره ترجمه‌ها تا دوباره نیاز به دانلود نباشد
                                    val safeMediaId = mediaId?.replace(Regex("[^a-zA-Z0-9.-]"), "_") ?: "unknown"
                                    val cacheFile = File(context.cacheDir, "lyrics_cache_$safeMediaId.json")
                                    val jsonArray = JSONArray()
                                    for (line in lyricLines) {
                                        val obj = JSONObject()
                                        obj.put("timeMs", line.timeMs)
                                        obj.put("text", line.text)
                                        obj.put("isSynced", line.isSynced)
                                        if (line.translation != null) obj.put("translation", line.translation)
                                        jsonArray.put(obj)
                                    }
                                    cacheFile.writeText(jsonArray.toString())

                                } else {
                                    withContext(Dispatchers.Main) { Toast.makeText(context, "API Error: ${conn.responseCode}", Toast.LENGTH_SHORT).show() }
                                }
                            } catch (e: Exception) { e.printStackTrace() }
                            finally { withContext(Dispatchers.Main) { isTranslating = false } }
                        }
                    }
                },
                modifier = Modifier
                    .align(Alignment.TopEnd)
                    .padding(top = 16.dp, end = 64.dp)
            ) {
                if (isTranslating) {
                    CircularProgressIndicator(modifier = Modifier.size(20.dp), color = Color.White.copy(alpha = 0.6f), strokeWidth = 2.dp)
                } else {
                    Icon(
                        imageVector = Icons.Default.Language,
                        contentDescription = "Translate Lyrics",
                        tint = Color.White.copy(alpha = 0.6f)
                    )
                }
            }

            IconButton(
                onClick = {
                    val fullLyrics = lyricLines.joinToString("\n") { it.text }
                    clipboardManager.setText(AnnotatedString(fullLyrics))
                    Toast.makeText(context, "Lyrics copied to clipboard", Toast.LENGTH_SHORT).show()
                },
                modifier = Modifier
                    .align(Alignment.TopEnd)
                    .padding(top = 16.dp, end = 16.dp)
            ) {
                Icon(
                    imageVector = Icons.Default.ContentCopy,
                    contentDescription = "Copy Lyrics",
                    tint = Color.White.copy(alpha = 0.6f)
                )
            }
        }
    }

    if (showApiDialog) {
        AlertDialog(
            onDismissRequest = { showApiDialog = false },
            title = { Text("Gemini AI Translation", fontWeight = FontWeight.Bold) },
            text = {
                Column {
                    Text("Please enter your Google Gemini API Key to enable instant translations:", fontSize = 14.sp)
                    Spacer(modifier = Modifier.height(12.dp))
                    OutlinedTextField(
                        value = tempApiKey,
                        onValueChange = { tempApiKey = it },
                        singleLine = true,
                        placeholder = { Text("AIzaSy...") }
                    )
                }
            },
            confirmButton = {
                TextButton(onClick = {
                    prefs.edit().putString("geminiApiKey", tempApiKey.trim()).apply()
                    geminiApiKey = tempApiKey.trim()
                    showApiDialog = false
                }) { Text("Save Key") }
            },
            dismissButton = {
                TextButton(onClick = { showApiDialog = false }) { Text("Cancel") }
            }
        )
    }
}
