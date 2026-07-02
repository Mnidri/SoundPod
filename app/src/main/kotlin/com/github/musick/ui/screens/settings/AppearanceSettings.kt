package com.github.musick.ui.screens.settings

import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.BlurOn
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.setValue
import androidx.compose.ui.res.painterResource
import androidx.compose.ui.res.stringResource
import com.github.musick.R
import com.github.musick.enums.AppThemeColor
import com.github.musick.enums.PlayerLayout
import com.github.musick.enums.ProgressBar
import com.github.musick.ui.common.IconSource
import com.github.musick.utils.appTheme
import com.github.musick.utils.playerlayout
import com.github.musick.utils.progressBarStyle
import com.github.musick.utils.rememberPreference

@Composable
fun AppearanceSettingsContent(
    onBackgroundClick: () -> Unit
) {
    var appThemeColor by rememberPreference(appTheme, AppThemeColor.System)
    var progressBarStyle by rememberPreference(progressBarStyle, ProgressBar.Wave )
    var playerlayout by rememberPreference(playerlayout, PlayerLayout.Default )

    SettingsGroup(
        title = stringResource(id = R.string.theme),
    ) {
        EnumValueSelectorSettingsEntry(
            title = stringResource(id = R.string.app_theme),
            selectedValue = appThemeColor,
            onValueSelected = { appThemeColor = it },
            icon = IconSource.Icon( painterResource(id = R.drawable.dark_mode)),
            valueText = { stringResource(it.resourceId) }
        )
    }

    SettingsGroup(
        title = stringResource(id = R.string.player_style),
    ) {
        EnumValueSelectorSettingsEntry(
            title = stringResource(id = R.string.player_layout),
            selectedValue = playerlayout,
            onValueSelected = { playerlayout = it },
            icon = IconSource.Icon( painterResource(id = R.drawable.layout)),
            valueText = { stringResource(it.resourceId) }
        )
    }

    SettingsGroup{
        EnumValueSelectorSettingsEntry(
            title = stringResource(id = R.string.progress_bar_style),
            selectedValue = progressBarStyle,
            onValueSelected = { progressBarStyle = it },
            icon = IconSource.Icon( painterResource(id = R.drawable.wave)),
            valueText = { stringResource(it.resourceId) }
        )
        SettingsColumn(
            icon = IconSource.Vector(Icons.Default.BlurOn),
            title = stringResource(id = R.string.background_style),
            description = stringResource(id = R.string.background_style_discription),
            onClick = onBackgroundClick,
        )
    }
}
