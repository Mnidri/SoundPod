package com.github.musick.viewmodels.home

import android.util.Log
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.setValue
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.github.innertube.Innertube
import com.github.innertube.requests.charts
import com.github.innertube.requests.recommendations
import com.github.innertube.requests.relatedPage
import com.github.innertube.requests.searchPage
import com.github.innertube.utils.from
import com.github.musick.appContext
import com.github.musick.db
import com.github.musick.enums.QuickPicksSource
import com.github.musick.models.Song
import com.github.musick.utils.ScreenCache
import com.github.musick.utils.asMediaItem
import com.github.musick.utils.isScreenCacheEnabledKey
import com.github.musick.utils.preferences
import com.github.musick.utils.quickPicksCustomGenreKey
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.Job
import kotlinx.coroutines.async
import kotlinx.coroutines.coroutineScope
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.first
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext

class QuickPicksViewModel : ViewModel() {
    val recentHistoryFlow = com.github.musick.db.lastPlayed(24)
    var relatedPageResult: Result<Innertube.RelatedPage?>? by mutableStateOf(null)
    var newReleasesResult: Result<List<Innertube.SongItem>>? by mutableStateOf(null)
    var dailyDiscoverResult: Result<Innertube.SongItem>? by mutableStateOf(null)
    private var job: Job? = null

    companion object {
        private const val CACHE_EXPIRATION = 30 * 60 * 1000L
        private const val PERSISTENT_CACHE_PREFIX = "quick_picks_cache_v2_"
    }

    private fun getSeedSongsFlow(source: QuickPicksSource, limit: Int): Flow<List<Song>> = when (source) {
        QuickPicksSource.Trending -> db.trending(limit)
        QuickPicksSource.LastPlayed -> db.lastPlayed(limit)
        QuickPicksSource.Recommended -> db.lastPlayed(limit)
        QuickPicksSource.Custom -> db.randomSongs(limit)
    }

    private fun getCached(source: QuickPicksSource): Innertube.RelatedPage? = ScreenCache.load(PERSISTENT_CACHE_PREFIX + source.name)
    private fun saveToCache(source: QuickPicksSource, page: Innertube.RelatedPage) = ScreenCache.save(PERSISTENT_CACHE_PREFIX + source.name, page)

    private fun <T : Innertube.Item> interleave(lists: List<List<T>>): List<T> {
        val result = mutableListOf<T>()
        val iterators = lists.map { it.iterator() }
        val seenKeys = mutableSetOf<String>()
        var hasMore = true
        while (hasMore) {
            hasMore = false
            for (iterator in iterators) {
                if (iterator.hasNext()) {
                    val item = iterator.next()
                    if (seenKeys.add(item.key)) { result.add(item) }
                    hasMore = true
                }
            }
        }
        return result
    }

    fun loadQuickPicks(quickPicksSource: QuickPicksSource, forceRefresh: Boolean = false) {
        val isScreenCacheEnabled = appContext.preferences.getBoolean(isScreenCacheEnabledKey, true)
        val cached = if (isScreenCacheEnabled) getCached(quickPicksSource) else null
        
        if (cached != null) relatedPageResult = Result.success(cached)
        
        job?.cancel()
        job = viewModelScope.launch(Dispatchers.IO) {
            val seedSongs = runCatching {
                when (quickPicksSource) {
                    QuickPicksSource.Custom -> {
                        val customGenre = appContext.preferences.getString(quickPicksCustomGenreKey, "Psaltic music") ?: "Psaltic music"
                        val searchResult = Innertube.searchPage(query = customGenre, params = Innertube.SearchFilter.Song.value, fromMusicShelfRendererContent = Innertube.SongItem.Companion::from)?.getOrNull()
                        searchResult?.items?.take(3)?.map { item ->
                            val mediaItem = item.asMediaItem
                            Song(id = mediaItem.mediaId, title = mediaItem.mediaMetadata.title.toString(), artistsText = mediaItem.mediaMetadata.artist.toString(), durationText = null, thumbnailUrl = mediaItem.mediaMetadata.artworkUri.toString())
                        } ?: emptyList()
                    }
                    QuickPicksSource.Trending, QuickPicksSource.Recommended -> {
                        val sourceCall = if (quickPicksSource == QuickPicksSource.Trending) Innertube.charts() else Innertube.recommendations()
                        sourceCall?.getOrNull()?.take(3)?.map { item ->
                            val mediaItem = item.asMediaItem
                            Song(id = mediaItem.mediaId, title = mediaItem.mediaMetadata.title.toString(), artistsText = mediaItem.mediaMetadata.artist.toString(), durationText = null, thumbnailUrl = mediaItem.mediaMetadata.artworkUri.toString())
                        } ?: getSeedSongsFlow(quickPicksSource, 3).first()
                    }
                    else -> {
                        val onboardedStr = appContext.getSharedPreferences("preferences", android.content.Context.MODE_PRIVATE).getString("onboardingSelectedArtists", "") ?: ""
                        val userHistory = getSeedSongsFlow(com.github.musick.enums.QuickPicksSource.LastPlayed, 5).first()
                        if (userHistory.isNotEmpty()) {
                            userHistory
                        } else if (onboardedStr.isNotEmpty()) {
                            val artistNames = onboardedStr.split(",").filter { it.isNotBlank() }.take(3)
                            val songs = mutableListOf<Song>()
                            for (artistName in artistNames) {
                                runCatching {
                                    val searchResult = Innertube.searchPage(query = artistName, params = Innertube.SearchFilter.Song.value, fromMusicShelfRendererContent = Innertube.SongItem.Companion::from)?.getOrNull()
                                    searchResult?.items?.filterIsInstance<Innertube.SongItem>()?.firstOrNull()?.let { item ->
                                        val mediaItem = item.asMediaItem
                                        songs.add(Song(id = mediaItem.mediaId, title = mediaItem.mediaMetadata.title.toString(), artistsText = mediaItem.mediaMetadata.artist.toString(), durationText = null, thumbnailUrl = mediaItem.mediaMetadata.artworkUri.toString()))
                                    }
                                }
                            }
                            if (songs.isNotEmpty()) songs else getSeedSongsFlow(quickPicksSource, 3).first()
                        } else {
                            getSeedSongsFlow(quickPicksSource, 3).first()
                        }
                    }
                }
            }.getOrElse { emptyList() }

            coroutineScope {
                val chartsDeferred = async { runCatching { Innertube.charts()?.getOrNull() }.getOrNull() }
                
                val newReleasesDeferred = async<List<Innertube.SongItem>?> {
                    try {
                        val historySongs = runCatching { db.lastPlayed(100).first() }.getOrNull() ?: emptyList()
                        val favSongs = runCatching { db.favorites().first() }.getOrNull() ?: emptyList()
                        val searchQueries = runCatching { db.queries("").first() }.getOrNull() ?: emptyList()

                        val historyArtists = historySongs.mapNotNull { it.artistsText }.flatMap { it.split(Regex(" & |, | x | • ")) }
                        val favArtists = favSongs.mapNotNull { it.artistsText }.flatMap { it.split(Regex(" & |, | x | • ")) }
                        val searchTexts = searchQueries.map { it.toString() }.flatMap { it.split(" ") }

                        val onboardedPref = appContext.getSharedPreferences("preferences", android.content.Context.MODE_PRIVATE).getString("onboardingSelectedArtists", "") ?: ""
                        val onboardedArtists = onboardedPref.split(",")

                        val myLovedArtists = (historyArtists + favArtists + onboardedArtists + searchTexts)
                            .map { it.trim().lowercase() }
                            .filter { it.length > 2 }
                            .toSet()

                        // جستجوی واقعی و تضمینی برای آهنگ‌های جدید
                        var globalNewReleases = runCatching { Innertube.searchPage(query = "latest single releases", params = Innertube.SearchFilter.Song.value, fromMusicShelfRendererContent = Innertube.SongItem.Companion::from)?.getOrNull()?.items?.filterIsInstance<Innertube.SongItem>() }.getOrNull() ?: emptyList()
                        
                        // سپر دفاعی: اگر سرچ خالی بود، از چارت جهانی بردار تا صفحه خالی نماند
                        if (globalNewReleases.isEmpty()) {
                            globalNewReleases = runCatching { Innertube.charts()?.getOrNull()?.filterIsInstance<Innertube.SongItem>() }.getOrNull() ?: emptyList()
                        }

                        if (myLovedArtists.isNotEmpty() && globalNewReleases.isNotEmpty()) {
                            val filteredSongs = globalNewReleases.filter { song ->
                                val songArtist = song.asMediaItem.mediaMetadata.artist?.toString()?.lowercase() ?: ""
                                val songTitle = song.asMediaItem.mediaMetadata.title?.toString()?.lowercase() ?: ""
                                myLovedArtists.any { beloved -> songArtist.contains(beloved) || songTitle.contains(beloved) }
                            }
                            if (filteredSongs.isNotEmpty()) filteredSongs.distinctBy { it.key } else { 
                                if (globalNewReleases.isNotEmpty()) globalNewReleases.take(8) else {
                                    // تلاش مجدد برای گرفتن چارت جهانی در صورت بن‌بست کامل
                                    runCatching { Innertube.charts()?.getOrNull()?.filterIsInstance<Innertube.SongItem>()?.take(8) }.getOrNull() ?: emptyList()
                                }
                            }
                        } else {
                            globalNewReleases.take(8)
                        }
                    } catch (e: Exception) {
                        e.printStackTrace()
                        // تله خطا: ارسال پیغام واقعی به یوزر برای عیب‌یابی راحت‌تر
                        withContext(Dispatchers.Main) {
                            android.widget.Toast.makeText(com.github.musick.appContext, "QuickPicks Error: ${e.localizedMessage}", android.widget.Toast.LENGTH_LONG).show()
                        }
                        null
                    }
                }

                // بازگردانی کدهای پاک شده برای لود کردن میکس‌ها
                val relatedDeferreds = seedSongs.map { song ->
                    async { Innertube.relatedPage(videoId = song.id)?.getOrNull() }
                }
                val relatedResults = relatedDeferreds.mapNotNull { it.await() }

                var mergedPage = if (relatedResults.isNotEmpty()) {
                    Innertube.RelatedPage(
                        songs = interleave(relatedResults.map { it.songs ?: emptyList() }).take(40),
                        playlists = interleave(relatedResults.map { it.playlists ?: emptyList() }).take(15),
                        albums = interleave(relatedResults.map { it.albums ?: emptyList() }).take(15),
                        artists = interleave(relatedResults.map { it.artists ?: emptyList() }).take(15)
                    )
                } else null

                if (mergedPage == null || mergedPage.songs.isNullOrEmpty()) {
                    chartsDeferred.await()?.shuffled()?.take(2)?.forEach { fallbackSong ->
                        val fallbackResult = Innertube.relatedPage(videoId = fallbackSong.key)?.getOrNull()
                        if (fallbackResult != null && !fallbackResult.songs.isNullOrEmpty()) {
                            mergedPage = fallbackResult
                            return@forEach
                        }
                    }
                }

                val finalResult = mergedPage?.let { Result.success(it) } ?: Result.failure(Exception("Failed to load Quick Picks"))
                finalResult.getOrNull()?.let { if (isScreenCacheEnabled) saveToCache(quickPicksSource, it) }

                withContext(Dispatchers.Main) {
                    relatedPageResult = finalResult
                    newReleasesResult = newReleasesDeferred.await()?.let { Result.success(it) }
                }
            }
        }
    }
}
