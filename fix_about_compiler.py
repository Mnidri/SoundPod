import os

fp_about = "app/src/main/kotlin/com/github/soundpod/ui/screens/settings/About.kt"
if not os.path.exists(fp_about): fp_about = "app/src/main/kotlin/com/github/musick/ui/screens/settings/About.kt"

code_about = """package com.github.musick.ui.screens.settings

import android.widget.Toast
import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.res.painterResource
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.lifecycle.viewmodel.compose.viewModel
import com.github.core.ui.LocalAppearance
import com.github.musick.R
import com.github.musick.viewmodels.AboutViewModel

@Composable
fun AboutSettingsContent(
    viewModel: AboutViewModel = viewModel()
) {
    val context = LocalContext.current
    val (colorPalette) = LocalAppearance.current
    
    Column(
        modifier = Modifier
            .fillMaxWidth()
            .padding(horizontal = 24.dp, vertical = 16.dp),
        horizontalAlignment = Alignment.CenterHorizontally
    ) {
        Spacer(modifier = Modifier.height(24.dp))
        
        Icon(
            painter = painterResource(id = R.drawable.app_icon),
            contentDescription = null,
            modifier = Modifier
                .size(130.dp)
                .clip(RoundedCornerShape(32.dp)),
            tint = colorPalette.text
        )
        
        Spacer(modifier = Modifier.height(16.dp))
        
        Text(
            text = "Musick",
            style = MaterialTheme.typography.headlineMedium.copy(fontWeight = FontWeight.Black, fontSize = 30.sp),
            color = colorPalette.text,
            textAlign = TextAlign.Center
        )
        
        Text(
            text = "Version 1.0.0",
            style = MaterialTheme.typography.bodyLarge.copy(fontWeight = FontWeight.Medium),
            color = colorPalette.text.copy(alpha = 0.5f),
            modifier = Modifier.padding(top = 4.dp),
            textAlign = TextAlign.Center
        )
        
        Spacer(modifier = Modifier.height(48.dp))
        
        Text(
            text = "Contact Us",
            style = MaterialTheme.typography.titleMedium.copy(fontWeight = FontWeight.Bold, fontSize = 18.sp, letterSpacing = 1.sp),
            color = colorPalette.text.copy(alpha = 0.8f),
            modifier = Modifier.fillMaxWidth(),
            textAlign = TextAlign.Start
        )
        
        Spacer(modifier = Modifier.height(12.dp))
        
        Card(
            modifier = Modifier.fillMaxWidth(),
            shape = RoundedCornerShape(24.dp),
            colors = CardDefaults.cardColors(containerColor = colorPalette.text.copy(alpha = 0.04f))
        ) {
            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(vertical = 24.dp, horizontal = 16.dp),
                horizontalArrangement = Arrangement.SpaceEvenly,
                verticalAlignment = Alignment.CenterVertically
            ) {
                // دکمه اول: وبسایت
                Column(
                    horizontalAlignment = Alignment.CenterHorizontally,
                    modifier = Modifier.clip(RoundedCornerShape(16.dp)).clickable { Toast.makeText(context, "Website: Coming soon", Toast.LENGTH_SHORT).show() }.padding(8.dp)
                ) {
                    Box(modifier = Modifier.size(56.dp).clip(CircleShape).background(colorPalette.text.copy(alpha = 0.08f)), contentAlignment = Alignment.Center) {
                        Icon(painter = painterResource(id = R.drawable.idea), contentDescription = null, modifier = Modifier.size(28.dp), tint = colorPalette.text)
                    }
                    Spacer(modifier = Modifier.height(8.dp))
                    Text(text = "Website", style = MaterialTheme.typography.labelMedium.copy(fontWeight = FontWeight.SemiBold), color = colorPalette.text.copy(alpha = 0.6f))
                }

                // دکمه دوم: اینستاگرام
                Column(
                    horizontalAlignment = Alignment.CenterHorizontally,
                    modifier = Modifier.clip(RoundedCornerShape(16.dp)).clickable { Toast.makeText(context, "Instagram: Coming soon", Toast.LENGTH_SHORT).show() }.padding(8.dp)
                ) {
                    Box(modifier = Modifier.size(56.dp).clip(CircleShape).background(colorPalette.text.copy(alpha = 0.08f)), contentAlignment = Alignment.Center) {
                        Icon(painter = painterResource(id = R.drawable.github), contentDescription = null, modifier = Modifier.size(28.dp), tint = colorPalette.text)
                    }
                    Spacer(modifier = Modifier.height(8.dp))
                    Text(text = "Instagram", style = MaterialTheme.typography.labelMedium.copy(fontWeight = FontWeight.SemiBold), color = colorPalette.text.copy(alpha = 0.6f))
                }

                // دکمه سوم: ایمیل
                Column(
                    horizontalAlignment = Alignment.CenterHorizontally,
                    modifier = Modifier.clip(RoundedCornerShape(16.dp)).clickable { Toast.makeText(context, "Email: Coming soon", Toast.LENGTH_SHORT).show() }.padding(8.dp)
                ) {
                    Box(modifier = Modifier.size(56.dp).clip(CircleShape).background(colorPalette.text.copy(alpha = 0.08f)), contentAlignment = Alignment.Center) {
                        Icon(painter = painterResource(id = R.drawable.bug), contentDescription = null, modifier = Modifier.size(28.dp), tint = colorPalette.text)
                    }
                    Spacer(modifier = Modifier.height(8.dp))
                    Text(text = "Email", style = MaterialTheme.typography.labelMedium.copy(fontWeight = FontWeight.SemiBold), color = colorPalette.text.copy(alpha = 0.6f))
                }

                // دکمه چهارم: تلگرام
                Column(
                    horizontalAlignment = Alignment.CenterHorizontally,
                    modifier = Modifier.clip(RoundedCornerShape(16.dp)).clickable { Toast.makeText(context, "Telegram: Coming soon", Toast.LENGTH_SHORT).show() }.padding(8.dp)
                ) {
                    Box(modifier = Modifier.size(56.dp).clip(CircleShape).background(colorPalette.text.copy(alpha = 0.08f)), contentAlignment = Alignment.Center) {
                        Icon(painter = painterResource(id = R.drawable.app_icon), contentDescription = null, modifier = Modifier.size(28.dp), tint = colorPalette.text)
                    }
                    Spacer(modifier = Modifier.height(8.dp))
                    Text(text = "Telegram", style = MaterialTheme.typography.labelMedium.copy(fontWeight = FontWeight.SemiBold), color = colorPalette.text.copy(alpha = 0.6f))
                }
            }
        }
    }
}
"""

with open(fp_about, "w") as f: f.write(code_about)
print("About content compilation syntax fully simplified!")
