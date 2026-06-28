package com.github.musick.viewmodels.home

import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.setValue
import androidx.lifecycle.ViewModel
import com.github.musick.db
import com.github.musick.enums.AlbumSortBy
import com.github.musick.enums.SortOrder
import com.github.musick.models.Album

class HomeAlbumsViewModel : ViewModel() {
    var items: List<Album> by mutableStateOf(emptyList())

    suspend fun loadAlbums(
        sortBy: AlbumSortBy,
        sortOrder: SortOrder
    ) {
        db
            .albums(sortBy, sortOrder)
            .collect { items = it }
    }
}