package com.github.musick.ui.screens.playlist

import androidx.compose.animation.ExperimentalAnimationApi
import androidx.compose.foundation.ExperimentalFoundationApi
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.itemsIndexed
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.outlined.PlaylistPlay
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import androidx.media3.common.util.UnstableApi
import com.github.innertube.Innertube
import com.github.musick.LocalPlayerPadding
import com.github.musick.LocalPlayerServiceBinder
import com.github.musick.R
import com.github.musick.models.ActionInfo
import com.github.musick.models.LocalMenuState
import com.github.musick.ui.components.NonQueuedMediaItemMenu
import com.github.musick.ui.components.ShimmerHost
import com.github.musick.ui.components.SwipeToActionBox
import com.github.musick.ui.items.ListItemPlaceholder
import com.github.musick.ui.items.SongItem
import com.github.musick.utils.asMediaItem
import com.github.musick.utils.enqueue
import com.github.musick.utils.forcePlayAtIndex

@ExperimentalFoundationApi
@ExperimentalAnimationApi
@UnstableApi
@Composable
fun PlaylistSongs(
    playlistPage: Innertube.PlaylistOrAlbumPage?,
    onGoToAlbum: (String) -> Unit,
    onGoToArtist: (String) -> Unit,
) {
    val binder = LocalPlayerServiceBinder.current
    val menuState = LocalMenuState.current
    val playerPadding = LocalPlayerPadding.current

    androidx.compose.runtime.LaunchedEffect(playlistPage) {
        playlistPage?.songsPage?.items?.take(5)?.map { it.key }?.let { videoIds ->
            binder?.preCacheManager?.preCache(videoIds)
        }
    }

    LazyColumn(
        contentPadding = PaddingValues(top = 0.dp, bottom = 16.dp + playerPadding),
        modifier = Modifier.fillMaxSize(),
        horizontalAlignment = Alignment.CenterHorizontally
    ) {
        itemsIndexed(
            items = playlistPage?.songsPage?.items ?: emptyList(),
            key = { _, song -> song.key }
        ) { index, song ->
            SwipeToActionBox(
                primaryAction = ActionInfo(
                    onClick = { binder?.player?.enqueue(song.asMediaItem) },
                    icon = Icons.AutoMirrored.Outlined.PlaylistPlay,
                    description = R.string.enqueue
                )
            ) {
                SongItem(
                    song = song,
                    onClick = {
                        playlistPage?.songsPage?.items?.map(Innertube.SongItem::asMediaItem)
                            ?.let { mediaItems ->
                                binder?.stopRadio()
                                binder?.player?.forcePlayAtIndex(mediaItems, index)
                            }
                    },
                    onLongClick = {
                        menuState.display {
                            NonQueuedMediaItemMenu(
                                onDismiss = menuState::hide,
                                mediaItem = song.asMediaItem,
                                onGoToAlbum = onGoToAlbum,
                                onGoToArtist = onGoToArtist
                            )
                        }
                    }
                )
            }
        }

        if (playlistPage == null) {
            item(key = "loading") {
                ShimmerHost {
                    repeat(8) {
                        ListItemPlaceholder()
                    }
                }
            }
        }
    }
}
