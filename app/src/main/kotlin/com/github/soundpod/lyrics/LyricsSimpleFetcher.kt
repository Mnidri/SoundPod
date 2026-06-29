package com.github.soundpod.lyrics

import java.net.HttpURLConnection
import java.net.URL
import java.net.URLEncoder
import org.json.JSONArray
import java.util.regex.Pattern

object LyricsSimpleFetcher {
    fun fetch(title: String, artist: String): String {
        val cleanArtist = if (artist.trim().equals(title.trim(), ignoreCase = true)) "" else artist
        
        try {
            val queryParam = if (cleanArtist.isNotEmpty()) {
                "track_name=${URLEncoder.encode(title, "UTF-8")}&artist_name=${URLEncoder.encode(cleanArtist, "UTF-8")}"
            } else {
                "query=${URLEncoder.encode(title, "UTF-8")}"
            }
            val url = URL("https://lrclib.net/api/search?$queryParam")
            val conn = url.openConnection() as HttpURLConnection
            conn.connectTimeout = 4000
            conn.readTimeout = 4000
            
            val response = conn.inputStream.bufferedReader().use { it.readText() }
            val jsonArray = JSONArray(response)
            if (jsonArray.length() > 0) {
                val bestMatch = jsonArray.getJSONObject(0)
                val synced = bestMatch.optString("syncedLyrics", "")
                if (synced.isNotEmpty()) return synced
                val plain = bestMatch.optString("plainLyrics", "")
                if (plain.isNotEmpty()) return plain
            }
        } catch (e: Exception) {}

        try {
            val searchQuery = if (cleanArtist.isNotEmpty()) "$cleanArtist $title متن آهنگ" else "$title متن آهنگ"
            val url = URL("https://html.duckduckgo.com/html/?q=${URLEncoder.encode(searchQuery, "UTF-8")}")
            val conn = url.openConnection() as HttpURLConnection
            conn.setRequestProperty("User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64)")
            conn.connectTimeout = 5000
            conn.readTimeout = 5000
            
            val html = conn.inputStream.bufferedReader().use { it.readText() }
            val matcher = Pattern.compile("class=\"result__snippet\"[^>]*>(.*?)</a>").matcher(html)
            val cleanLines = mutableListOf<String>()
            
            while (matcher.find()) {
                val snippet = matcher.group(1)
                    ?.replace("<[^>]*>".toRegex(), "")
                    ?.replace("&quot;", "\"")
                    ?.replace("&amp;", "&")
                    ?.trim() ?: ""
                
                snippet.split("...", " - ", "|", "\n").forEach { chunk ->
                    val line = chunk.trim()
                    
                    val isInvalid = line.contains("آلبوم") || line.contains("Released") || 
                                    line.contains("Lyrics by") || line.contains("دانلود آهنگ") ||
                                    line.contains("متن آهنگ") || line.contains("A deep dive") ||
                                    line.contains("#") || line.contains("Reaction") || line.contains("ری اکشن") ||
                                    line.contains("Listen to") || line.contains("tour dates") ||
                                    line.matches("^[a-zA-Z0-9\\s\\.,!\\?-\\|\\(\\)]+$".toRegex())
                    
                    if (line.length > 6 && !isInvalid && !cleanLines.contains(line)) {
                        cleanLines.add(line)
                    }
                }
            }
            
            if (cleanLines.isNotEmpty()) {
                return "$title - $artist\n\n" + cleanLines.joinToString("\n\n")
            }
        } catch (e: Exception) {}

        return "Lyrics unavailable."
    }
}
