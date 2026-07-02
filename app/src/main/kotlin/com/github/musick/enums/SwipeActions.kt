package com.github.musick.enums

import androidx.annotation.StringRes
import com.github.musick.R

enum class SwipeActions(
    @get:StringRes val resourceId: Int
) {
    Remove(
        resourceId = R.string.remove_from_playlist,
    ),
    AddToFavorites(
        resourceId = R.string.add_to_favorites,
    ),
    Blocklist(
        resourceId = R.string.add_to_blocklist,
    ),
    Off(
    resourceId = R.string.off,
    )
}