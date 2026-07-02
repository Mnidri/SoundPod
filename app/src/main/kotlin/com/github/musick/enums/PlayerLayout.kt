package com.github.musick.enums

import androidx.annotation.StringRes
import com.github.musick.R

enum class PlayerLayout(
    @get:StringRes val resourceId: Int
) {
    Default(
        resourceId = R.string.defualt,
    ),
    New(
        resourceId = R.string.new_layout,
    )
}