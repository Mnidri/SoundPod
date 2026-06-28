package com.github.musick.ui.screens.localplaylist

import androidx.compose.animation.ExperimentalAnimationApi
import androidx.compose.foundation.ExperimentalFoundationApi
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.itemsIndexed
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Modifier
import com.github.musick.LocalPlayerPadding
import com.github.musick.LocalPlayerServiceBinder
import com.github.musick.db
import com.github.musick.enums.SongSortBy
import com.github.musick.enums.SortOrder
import com.github.musick.models.LocalMenuState
import com.github.musick.models.Song
import com.github.musick.ui.components.InPlaylistMediaItemMenu
import com.github.musick.ui.components.SortingHeader
import com.github.musick.ui.items.LocalSongItem
import com.github.musick.utils.asMediaItem
import com.github.musick.utils.forcePlayAtIndex

@ExperimentalAnimationApi
@ExperimentalFoundationApi
@Composable
fun LocalPlaylistSongs(
    playlistId: Long,
    onGoToAlbum: (String) -> Unit,
    onGoToArtist: (String) -> Unit
) {
    val binder = LocalPlayerServiceBinder.current
    val menuState = LocalMenuState.current
    val playerPadding = LocalPlayerPadding.current

    var sortBy by remember { mutableStateOf(SongSortBy.Title) }
    var sortOrder by remember { mutableStateOf(SortOrder.Ascending) }

    var playlistSongs: List<Song> by remember { mutableStateOf(emptyList()) }

    // This handles both fetching the data AND applying the sorting logic.
    LaunchedEffect(playlistId, sortBy, sortOrder) {
        db.playlistSongs(playlistId).collect { fetchedSongs ->
            val sortedList = when (sortBy) {
                SongSortBy.Title -> fetchedSongs.sortedBy { it.title }
                SongSortBy.Artist -> fetchedSongs.sortedBy { it.artistsText }
                else -> fetchedSongs
            }
            playlistSongs = if (sortOrder.name == "Descending") sortedList.reversed() else sortedList
        }
    }

    LazyColumn(
        modifier = Modifier
            .fillMaxSize(),
        contentPadding = PaddingValues(bottom = playerPadding)
    ) {
        item {
            SortingHeader(
                sortBy = sortBy,
                changeSortBy = { sortBy = it },
                sortByEntries = SongSortBy.entries.toList(),
                sortOrder = sortOrder,
                toggleSortOrder = {
                    sortOrder =
                        if (sortOrder.name == "Ascending") SortOrder.Descending else SortOrder.Ascending
                },
                size = playlistSongs.size,
                onPlayClick = {
                    binder?.stopRadio()
                    binder?.player?.forcePlayAtIndex(playlistSongs.map(Song::asMediaItem), 0)
                },
                onShuffleClick = {
                    binder?.stopRadio()
                    val shuffledSongs = playlistSongs.shuffled()
                    binder?.player?.forcePlayAtIndex(shuffledSongs.map(Song::asMediaItem), 0)
                }
            )
        }

        itemsIndexed(playlistSongs) { index, song ->
            LocalSongItem(
                song = song,
                onClick = {
                    playlistSongs
                        .map(Song::asMediaItem)
                        .let { mediaItems ->
                            binder?.stopRadio()
                            binder?.player?.forcePlayAtIndex(
                                mediaItems,
                                index
                            )
                        }
                },
                showMoreVert = false,
                onLongClick = {
                    menuState.display {
                        InPlaylistMediaItemMenu(
                            playlistId = playlistId,
                            positionInPlaylist = index,
                            song = song,
                            onDismiss = menuState::hide,
                            onGoToAlbum = onGoToAlbum,
                            onGoToArtist = onGoToArtist
                        )
                    }
                }
            )
        }
    }
}