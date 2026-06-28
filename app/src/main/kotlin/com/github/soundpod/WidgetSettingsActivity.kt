package com.github.musick

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import com.github.musick.ui.common.WidgetCustomizationScreen
import com.github.musick.ui.styling.AppTheme // Adjust import if needed

class WidgetSettingsActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        
        setContent {
            AppTheme(darkTheme = true) {
                WidgetCustomizationScreen(
                    onNavigateBack = { finish() }
                )
            }
        }
    }
}