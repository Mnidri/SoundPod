package com.github.musick.viewmodels.favorites

import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.setValue
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.github.musick.db
import com.github.musick.models.Album
import com.github.musick.models.Artist
import com.github.musick.models.PlaylistPreview
import com.github.musick.models.Song
import com.github.musick.R
import com.github.musick.enums.AlbumSortBy
import com.github.musick.enums.ArtistSortBy
import com.github.musick.enums.SortOrder
import kotlinx.coroutines.flow.collectLatest
import kotlinx.coroutines.launch

class FavoritesViewModel : ViewModel() {
    val tabs = listOf(
        R.string.songs,
        R.string.albums,
        R.string.artists,
        R.string.playlists
    )

    var favoriteSongs: List<Song> by mutableStateOf(emptyList())
        private set
    var favoriteAlbums: List<Album> by mutableStateOf(emptyList())
        private set
    var favoriteArtists: List<Artist> by mutableStateOf(emptyList())
        private set
    var favoritePlaylists: List<PlaylistPreview> by mutableStateOf(emptyList())
        private set

    init {
        viewModelScope.launch {
            db.favorites().collectLatest {
                favoriteSongs = it
            }
        }
        viewModelScope.launch {
            db.albums(AlbumSortBy.DateAdded, SortOrder.Descending).collectLatest {
                favoriteAlbums = it
            }
        }
        viewModelScope.launch {
            db.artists(ArtistSortBy.DateAdded, SortOrder.Descending).collectLatest {
                favoriteArtists = it
            }
        }
        // For now, let's just show all local playlists if we don't have a "favorite" flag yet
        viewModelScope.launch {
            db.playlistPreviewsByNameAsc().collectLatest { previews ->
                favoritePlaylists = previews
            }
        }
    }
}
