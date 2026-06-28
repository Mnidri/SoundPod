package com.github.musick.viewmodels.home

import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.setValue
import androidx.lifecycle.ViewModel
import com.github.musick.db
import com.github.musick.enums.PlaylistSortBy
import com.github.musick.enums.SortOrder
import com.github.musick.models.PlaylistPreview

class HomePlaylistsViewModel : ViewModel() {
    var items: List<PlaylistPreview> by mutableStateOf(emptyList())

    suspend fun loadArtists(
        sortBy: PlaylistSortBy,
        sortOrder: SortOrder
    ) {
        db
            .playlistPreviews(sortBy, sortOrder)
            .collect { items = it }
    }
}