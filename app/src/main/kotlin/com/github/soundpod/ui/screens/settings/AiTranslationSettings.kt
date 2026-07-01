package com.github.musick.ui.screens.settings

import android.content.Context
import androidx.compose.foundation.layout.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.unit.dp

@Composable
fun AiTranslationSettingsContent() {
    val context = LocalContext.current
    val sharedPreferences = context.getSharedPreferences("ai_settings", Context.MODE_PRIVATE)
    var apiKey by remember { mutableStateOf(sharedPreferences.getString("api_key", "") ?: "") }
    var isSaved by remember { mutableStateOf(false) }

    Column(modifier = Modifier.padding(16.dp)) {
        Text("AI Translation Configuration", style = MaterialTheme.typography.titleMedium, color = MaterialTheme.colorScheme.onBackground)
        Spacer(modifier = Modifier.height(16.dp))
        OutlinedTextField(
            value = apiKey,
            onValueChange = { 
                apiKey = it
                isSaved = false
            },
            label = { Text("Enter API Key") },
            modifier = Modifier.fillMaxWidth()
        )
        Spacer(modifier = Modifier.height(16.dp))
        Button(
            onClick = {
                sharedPreferences.edit().putString("api_key", apiKey).apply()
                isSaved = true
            },
            modifier = Modifier.fillMaxWidth()
        ) {
            Text(if (isSaved) "Saved Successfully!" else "Save API Key")
        }
    }
}

@Composable
fun PremiumSettingsContent() {
    Column(modifier = Modifier.padding(16.dp)) {
        Text("Premium Settings", style = MaterialTheme.typography.titleLarge, color = MaterialTheme.colorScheme.onBackground)
        Spacer(modifier = Modifier.height(8.dp))
        Text("Exclusive features are coming soon...", style = MaterialTheme.typography.bodyMedium, color = MaterialTheme.colorScheme.onSurfaceVariant)
    }
}
