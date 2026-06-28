package com.github.musick.enums

import androidx.annotation.StringRes
import com.github.musick.R


enum class AutoBackUp(@StringRes val resourceId: Int) {
    OFF(R.string.off),
    DAILY(R.string.daily),
    WEEKLY(R.string.weekly),
    MONTHLY(R.string.monthly);

    companion object {
        fun fromOrdinal(ordinal: Int): AutoBackUp {
            return entries.getOrNull(ordinal) ?: OFF
        }
    }
}

