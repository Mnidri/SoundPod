package com.github.musick.enums

import androidx.annotation.StringRes
import com.github.musick.R

enum class AccentColorSource(
    @get:StringRes val resourceId: Int
) {
    Default(
        resourceId = R.string.defualt,
    ),
    Dynamic(
        resourceId = R.string.dynamic,
    ),
    MaterialYou(
        resourceId = R.string.material_you,
    )
}