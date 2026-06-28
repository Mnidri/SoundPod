package com.github.musick.viewmodels

import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.setValue
import androidx.compose.runtime.snapshotFlow
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.github.innertube.Innertube
import com.github.innertube.requests.artistPage
import com.github.musick.db
import com.github.musick.models.Artist
import com.github.musick.utils.ScreenCache
import com.github.musick.utils.isScreenCacheEnabledKey
import com.github.musick.utils.preferences
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.flow.combine
import kotlinx.coroutines.flow.distinctUntilChanged
import kotlinx.coroutines.flow.map
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext

class ArtistViewModel : ViewModel() {
    var artist: Artist? by mutableStateOf(null)
    var artistPage: Innertube.ArtistPage? by mutableStateOf(null)

    companion object {
        private const val CACHE_EXPIRATION = 60 * 60 * 1000L // 1 hour
    }

    fun toggleBookmark() {
        val currentArtist = artist ?: return
        val bookmarkedAt = if (currentArtist.bookmarkedAt == null) System.currentTimeMillis() else null
        val updatedArtist = currentArtist.copy(bookmarkedAt = bookmarkedAt)
        viewModelScope.launch(Dispatchers.IO) {
            db.update(updatedArtist)
        }
    }

    suspend fun loadArtist(browseId: String, tabIndex: Int) {
        val context = com.github.musick.appContext
        val isScreenCacheEnabled = context.preferences.getBoolean(isScreenCacheEnabledKey, true)
        val cacheKey = "artist_$browseId"

        if (artistPage == null && isScreenCacheEnabled) {
            artistPage = ScreenCache.load(cacheKey)
        }

        db
            .artist(browseId)
            .combine(snapshotFlow { tabIndex }.map { it != 4 }) { artist, mustFetch -> artist to mustFetch }
            .distinctUntilChanged()
            .collect { (currentArtist, mustFetch) ->
                artist = currentArtist

                val isExpired = ScreenCache.isExpired(cacheKey, CACHE_EXPIRATION)

                if (artistPage == null || (isExpired && mustFetch && isScreenCacheEnabled)) {
                    withContext(Dispatchers.IO) {
                        Innertube.artistPage(browseId = browseId)
                            ?.onSuccess { currentArtistPage ->
                                artistPage = currentArtistPage
                                if (isScreenCacheEnabled) {
                                    ScreenCache.save(cacheKey, currentArtistPage)
                                }

                                db.upsert(
                                    Artist(
                                        id = browseId,
                                        name = currentArtistPage.name,
                                        thumbnailUrl = currentArtistPage.thumbnail?.url,
                                        timestamp = System.currentTimeMillis(),
                                        bookmarkedAt = currentArtist?.bookmarkedAt
                                    )
                                )
                            }
                    }
                }
            }
    }
}
