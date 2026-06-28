package com.github.musick.viewmodels.home

import androidx.lifecycle.ViewModel
import com.github.musick.R

class HomeViewModel : ViewModel() {
    val tabs = listOf(
        R.string.home,
        R.string.favorites,
        R.string.songs,
        R.string.artists,
        R.string.albums,
        R.string.playlists
    )
}
