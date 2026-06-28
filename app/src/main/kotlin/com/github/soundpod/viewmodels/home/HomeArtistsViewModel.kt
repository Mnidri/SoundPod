package com.github.musick.viewmodels.home

import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.setValue
import androidx.lifecycle.ViewModel
import com.github.musick.db
import com.github.musick.enums.ArtistSortBy
import com.github.musick.enums.SortOrder
import com.github.musick.models.Artist

class HomeArtistsViewModel : ViewModel() {
    var items: List<Artist> by mutableStateOf(emptyList())

    suspend fun loadArtists(
        sortBy: ArtistSortBy,
        sortOrder: SortOrder
    ) {
        db
            .artists(sortBy, sortOrder)
            .collect { items = it }
    }
}