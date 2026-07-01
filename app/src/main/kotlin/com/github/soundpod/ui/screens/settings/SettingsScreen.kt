@file:OptIn(ExperimentalMaterial3Api::class)
package com.github.musick.ui.screens.settings

import androidx.compose.foundation.layout.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.res.painterResource
import androidx.compose.ui.res.stringResource
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import androidx.lifecycle.viewmodel.compose.viewModel
import com.github.musick.R
import com.github.musick.ui.common.IconSource
import com.github.musick.ui.components.SettingsCard
import com.github.musick.ui.components.SettingsScreenLayout
import com.github.musick.ui.navigation.SettingsDestinations
import com.github.musick.ui.screens.player.TrackDetails
import com.github.musick.viewmodels.SettingsViewModel

@Composable
fun SettingsScreen(
    screenId: String,
    onBackClick: () -> Unit,
    onOptionClick: (String) -> Unit
) {
    val title = when (screenId) {
        SettingsDestinations.MAIN -> stringResource(R.string.settings)
        SettingsDestinations.APPEARANCE -> stringResource(R.string.appearance)
        SettingsDestinations.BACKGROUND -> stringResource(R.string.player_background)
        SettingsDestinations.PLAYER -> stringResource(R.string.player)
        SettingsDestinations.PRIVACY -> stringResource(R.string.privacy)
        SettingsDestinations.BACKUP -> stringResource(R.string.backup_restore)
        SettingsDestinations.DATABASE -> stringResource(R.string.database)
        SettingsDestinations.MORE -> stringResource(R.string.more_settings)
        SettingsDestinations.EXPERIMENT -> stringResource(R.string.experimental)
        SettingsDestinations.ABOUT -> stringResource(R.string.about)
        SettingsDestinations.SLEEP_TIMER -> stringResource(R.string.sleep_timer)
        SettingsDestinations.QUICK_PICKS -> stringResource(R.string.quick_picks)
        SettingsDestinations.TRACK_DETAILS -> stringResource(R.string.track_details)
        SettingsDestinations.ACCOUNT -> stringResource(R.string.youtube)
        SettingsDestinations.LOGIN -> stringResource(R.string.sign_in)
        else -> stringResource(R.string.settings)
    }

    SettingsScreenLayout(
        title = title,
        shape = MaterialTheme.shapes.extraLarge,
        onBackClick = onBackClick,
        content = {
            when (screenId) {
                SettingsDestinations.MAIN -> SettingsMainContent(onOptionClick)
                SettingsDestinations.APPEARANCE -> AppearanceSettingsContent(onBackgroundClick = { onOptionClick(SettingsDestinations.BACKGROUND) })
                SettingsDestinations.BACKGROUND -> BackgroundSettingsContent()
                SettingsDestinations.PLAYER -> PlayerSettingsContent(onSleepTimerClick = { onOptionClick(SettingsDestinations.SLEEP_TIMER) })
                SettingsDestinations.SLEEP_TIMER -> SleepTimerSettingsContent()
                SettingsDestinations.PRIVACY -> PrivacySettingsContent()
                SettingsDestinations.BACKUP -> BackupSettingsContent()
                SettingsDestinations.DATABASE -> CacheSettingsContent(onOptionClick)
                SettingsDestinations.MORE -> MoreSettingsContent()
                SettingsDestinations.EXPERIMENT -> ExperimentSettingsContent()
                SettingsDestinations.ABOUT -> AboutSettingsContent()
                SettingsDestinations.QUICK_PICKS -> QuickPicksSettingsContent()
                SettingsDestinations.TRACK_DETAILS -> TrackDetails()
                SettingsDestinations.ACCOUNT -> YouTubeSettingsContent(onOptionClick)
                SettingsDestinations.LOGIN -> LoginSettingsContent(onBackClick)
            }
        }
    )
}

@Composable
fun SettingsMainContent(
    onOptionClick: (String) -> Unit,
    viewModel: SettingsViewModel = viewModel()
) {
    val sections by viewModel.sections.collectAsStateWithLifecycle()
    
    // متغیرهای مدیریت دیالوگ‌های اختصاصی بدون تداخل در ناوبری
    var showPremiumDialog by remember { mutableStateOf(false) }
    var showAiDialog by remember { mutableStateOf(false) }
    var apiKey by remember { mutableStateOf("") }

    if (showPremiumDialog) {
        AlertDialog(
            onDismissRequest = { showPremiumDialog = false },
            title = { Text("Musick Premium", fontWeight = FontWeight.Bold, color = androidx.compose.ui.graphics.Color(0xFFFFD700)) },
            text = { Text("Coming soon...", fontSize = 22.sp, fontWeight = FontWeight.Bold) },
            confirmButton = { TextButton(onClick = { showPremiumDialog = false }) { Text("OK") } }
        )
    }

    if (showAiDialog) {
        AlertDialog(
            onDismissRequest = { showAiDialog = false },
            title = { Text("AI Translation Settings", fontWeight = FontWeight.Bold) },
            text = {
                Column {
                    Text("Enter your AI API Key for smart lyrics translation:")
                    Spacer(modifier = Modifier.height(12.dp))
                    OutlinedTextField(
                        value = apiKey,
                        onValueChange = { apiKey = it },
                        label = { Text("API Key") },
                        singleLine = true
                    )
                }
            },
            confirmButton = { TextButton(onClick = { showAiDialog = false }) { Text("Save") } },
            dismissButton = { TextButton(onClick = { showAiDialog = false }) { Text("Cancel") } }
        )
    }

    Spacer(modifier = Modifier.height(8.dp))
    
    // رندر کارت اختصاصی شما با آیکون‌های حرفه‌ای جدید
    SettingsCard {
        SettingRow(
            title = "Musick Premium",
            icon = IconSource.Icon(painterResource(id = R.drawable.ic_premium_custom)),
            onClick = { showPremiumDialog = true }
        )
        SettingRow(
            title = "AI Translation",
            icon = IconSource.Icon(painterResource(id = R.drawable.ic_translate_custom)),
            onClick = { showAiDialog = true }
        )
    }
    Spacer(modifier = Modifier.height(8.dp))

    // رندر بقیه تنظیمات
    sections.forEach { section ->
        SettingsCard {
            section.options.forEach { option ->
                if (option.icon != null) {
                    SettingRow(
                        title = stringResource(id = option.title),
                        icon = IconSource.Vector(option.icon),
                        onClick = { onOptionClick(option.screenId) }
                    )
                } else {
                    option.iconRes?.let { iconResId ->
                        SettingRow(
                            title = stringResource(id = option.title),
                            icon = IconSource.Icon(painterResource(iconResId)),
                            onClick = { onOptionClick(option.screenId) }
                        )
                    }
                }
            }
        }
        Spacer(modifier = Modifier.height(8.dp))
    }
}
