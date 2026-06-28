package com.github.musick.ui.screens.favorites

import androidx.compose.animation.ExperimentalAnimationApi
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.itemsIndexed
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.res.stringResource
import androidx.compose.ui.unit.dp
import androidx.lifecycle.viewmodel.compose.viewModel
import com.github.musick.LocalPlayerPadding
import com.github.musick.LocalPlayerServiceBinder
import com.github.musick.R
import com.github.musick.models.LocalMenuState
import com.github.musick.models.Song
import com.github.musick.ui.components.InHistoryMediaItemMenu
import com.github.musick.ui.components.SettingsCard
import com.github.musick.ui.components.SettingsScreenLayout
import com.github.musick.ui.items.LocalSongItem
import com.github.musick.utils.asMediaItem
import com.github.musick.utils.forcePlayAtIndex
import com.github.musick.viewmodels.favorites.FavoritesViewModel

@OptIn(ExperimentalAnimationApi::class)
@Composable
fun FavoriteTracksScreen(
    onBackClick: () -> Unit,
    onGoToAlbum: (String) -> Unit,
    onGoToArtist: (String) -> Unit,
    viewModel: FavoritesViewModel = viewModel()
) {
    val binder = LocalPlayerServiceBinder.current
    val menuState = LocalMenuState.current
    val playerPadding = LocalPlayerPadding.current
    val songs = viewModel.favoriteSongs

    SettingsScreenLayout(
        title = stringResource(R.string.favorite_tracks),
        onBackClick = onBackClick,
        scrollable = false,
        horizontalPadding = 0.dp
    ) {
        SettingsCard {
            LazyColumn(
                contentPadding = PaddingValues(bottom = playerPadding + 16.dp),
                modifier = Modifier.fillMaxSize()
            ) {
                itemsIndexed(
                    items = songs,
                    key = { _, song -> song.id }
                ) { index, song ->
                    LocalSongItem(
                        song = song,
                        onClick = {
                            binder?.stopRadio()
                            binder?.player?.forcePlayAtIndex(
                                songs.map(Song::asMediaItem),
                                index
                            )
                        },
                        onLongClick = {
                            menuState.display {
                                InHistoryMediaItemMenu(
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
    }
}
