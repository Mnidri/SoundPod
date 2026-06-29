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
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.Text
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
import kotlinx.coroutines.withContext
import org.json.JSONArray
import org.json.JSONObject
import java.net.HttpURLConnection
import java.net.URL
import java.net.URLEncoder

data class LyricLine(val timeMs: Long, val text: String, val isSynced: Boolean)

// تمیز کردن اسم آهنگ
fun sanitizeTitle(input: String): String {
    var text = input.replace(Regex("\\(.*?\\)|\\[.*?\\]"), "")
    text = text.replace(Regex("(?i)\\b(ft\\.?|feat\\.?|featuring|prod\\.?|x|&)\\b.*"), "")
    return text.trim().replace(Regex("\\s+"), " ")
}

// تمیز کردن اسم خواننده (حل مشکل آهنگ‌های ایرانی با چند خواننده)
fun sanitizeArtist(input: String): String {
    var text = input.replace(Regex("\\(.*?\\)|\\[.*?\\]"), "")
    // جدا کردن خواننده‌ها بر اساس جداکننده‌های رایج و انتخاب خواننده اصلی (اولی)
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

    LaunchedEffect(mediaMetadata?.title, mediaMetadata?.artist) {
        isLoading = true
        val rawTitle = mediaMetadata?.title?.toString() ?: ""
        val rawArtist = mediaMetadata?.artist?.toString() ?: ""
        
        val title = sanitizeTitle(rawTitle)
        val artist = sanitizeArtist(rawArtist)

        val fetchedLyrics = withContext(Dispatchers.IO) {
            var finalLyrics = ""
            try {
                val useExactGet = title.isNotBlank() && artist.isNotBlank() && !title.equals(artist, ignoreCase = true)

                // منبع ۱: جستجوی دقیق LRCLIB
                if (useExactGet) {
                    val encodedTitle = URLEncoder.encode(title, "UTF-8")
                    val encodedArtist = URLEncoder.encode(artist, "UTF-8")
                    val getUrl = URL("https://lrclib.net/api/get?track_name=$encodedTitle&artist_name=$encodedArtist")
                    val conn1 = getUrl.openConnection() as HttpURLConnection
                    conn1.connectTimeout = 5000
                    
                    if (conn1.responseCode == 200) {
                        val responseText = conn1.inputStream.bufferedReader().readText()
                        val json = JSONObject(responseText)
                        if (!json.isNull("syncedLyrics")) {
                            finalLyrics = json.getString("syncedLyrics")
                        } else if (!json.isNull("plainLyrics")) {
                            finalLyrics = json.getString("plainLyrics")
                        }
                    }
                }

                // منبع ۲: جستجوی هوشمند LRCLIB (اگر منبع اول جواب نداد)
                if (finalLyrics.isBlank() && rawTitle.isNotBlank()) {
                    val searchQuery = if (useExactGet) "$title $artist" else rawTitle.replace(Regex("[\\[\\]\\(\\)]"), "")
                    val encodedQuery = URLEncoder.encode(searchQuery.trim(), "UTF-8")
                    val searchUrl = URL("https://lrclib.net/api/search?q=$encodedQuery")
                    val conn2 = searchUrl.openConnection() as HttpURLConnection
                    conn2.connectTimeout = 5000
                    
                    if (conn2.responseCode == 200) {
                        val responseText = conn2.inputStream.bufferedReader().readText()
                        val jsonArray = JSONArray(responseText)
                        var bestSynced = ""
                        var bestPlain = ""
                        val titleLower = title.lowercase()

                        for (i in 0 until jsonArray.length()) {
                            val item = jsonArray.getJSONObject(i)
                            val apiTrackLower = item.optString("trackName", "").lowercase()
                            
                            if (apiTrackLower.contains(titleLower) || titleLower.contains(apiTrackLower) || titleLower.isEmpty()) {
                                if (!item.isNull("syncedLyrics") && item.getString("syncedLyrics").isNotBlank()) {
                                    bestSynced = item.getString("syncedLyrics")
                                    break
                                } else if (bestPlain.isBlank() && !item.isNull("plainLyrics")) {
                                    bestPlain = item.getString("plainLyrics")
                                }
                            }
                        }
                        finalLyrics = bestSynced.ifBlank { bestPlain }
                    }
                }

                // منبع ۳: Lyrics.ovh به عنوان آخرین خط دفاعی
                if (finalLyrics.isBlank() && title.isNotBlank() && artist.isNotBlank()) {
                    val encodedTitle = URLEncoder.encode(title, "UTF-8")
                    val encodedArtist = URLEncoder.encode(artist, "UTF-8")
                    val ovhUrl = URL("https://api.lyrics.ovh/v1/$encodedArtist/$encodedTitle")
                    val conn3 = ovhUrl.openConnection() as HttpURLConnection
                    conn3.connectTimeout = 5000
                    
                    if (conn3.responseCode == 200) {
                        val responseText = conn3.inputStream.bufferedReader().readText()
                        val json = JSONObject(responseText)
                        if (!json.isNull("lyrics")) {
                            finalLyrics = json.getString("lyrics")
                        }
                    }
                }

            } catch (e: Exception) { e.printStackTrace() }
            finalLyrics
        }

        val parsedLines = mutableListOf<LyricLine>()
        if (fetchedLyrics.isNotBlank()) {
            // حذف متون اضافی که بعضی API ها به اول لیریک اضافه می‌کنند
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
            listState.animateScrollToItem(maxOf(0, activeIndex - 2))
        }
    }

    // لایه‌بندی کل صفحه برای قرار دادن دکمه کپی در بالا
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
                contentPadding = PaddingValues(top = 180.dp, bottom = 180.dp),
                horizontalAlignment = Alignment.CenterHorizontally
            ) {
                itemsIndexed(lyricLines) { index, line ->
                    val isCurrent = index == activeIndex && line.isSynced
                    val alpha by animateFloatAsState(targetValue = if (isCurrent) 1f else 0.4f, animationSpec = tween(500))

                    Text(
                        text = line.text, 
                        color = Color.White.copy(alpha = alpha), 
                        fontSize = 26.sp,                   
                        fontWeight = FontWeight.ExtraBold,
                        textAlign = TextAlign.Center,
                        lineHeight = 38.sp,
                        modifier = Modifier
                            .fillMaxWidth()
                            .padding(vertical = 14.dp, horizontal = 24.dp)
                            .clickable { if (line.isSynced) onSeekToPosition(line.timeMs) }
                    )
                }
            }
            
            // دکمه کپی در گوشه بالا سمت راست
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
}
