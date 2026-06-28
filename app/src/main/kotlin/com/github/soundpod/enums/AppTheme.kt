package com.github.musick.enums

import androidx.annotation.StringRes
import com.github.musick.R

enum class AppThemeColor(
    @get:StringRes val resourceId: Int
) {
    Dark(
        resourceId = R.string.dark_theme,
    ),
    Light(
        resourceId = R.string.light_theme,
    ),
    System(
        resourceId = R.string.System_default,
    )
}
