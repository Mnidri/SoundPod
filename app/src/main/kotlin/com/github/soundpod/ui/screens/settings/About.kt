package com.github.musick.ui.screens.settings

import android.widget.Toast
import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Email
import androidx.compose.material.icons.filled.Language
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.res.painterResource
import androidx.compose.ui.res.vectorResource
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.lifecycle.viewmodel.compose.viewModel
import com.github.core.ui.LocalAppearance
import com.github.musick.R
import com.github.musick.viewmodels.AboutViewModel

@Composable
fun AboutSettingsContent(viewModel: AboutViewModel = viewModel()) {
    val context = LocalContext.current
    val (colorPalette) = LocalAppearance.current
    
    Column(
        modifier = Modifier.fillMaxWidth().padding(horizontal = 24.dp, vertical = 16.dp),
        horizontalAlignment = Alignment.CenterHorizontally
    ) {
        Spacer(modifier = Modifier.height(24.dp))
        
        Icon(
            painter = painterResource(id = R.drawable.app_icon),
            contentDescription = null,
            modifier = Modifier.size(130.dp).clip(RoundedCornerShape(32.dp)),
            tint = colorPalette.text
        )
        
        Spacer(modifier = Modifier.height(16.dp))
        
        Text(text = "Musick", style = MaterialTheme.typography.headlineMedium.copy(fontWeight = FontWeight.Black, fontSize = 30.sp), color = colorPalette.text, textAlign = TextAlign.Center)
        Text(text = "Version 1.0.0", style = MaterialTheme.typography.bodyLarge.copy(fontWeight = FontWeight.Medium), color = colorPalette.text.copy(alpha = 0.5f), modifier = Modifier.padding(top = 4.dp), textAlign = TextAlign.Center)
        
        Spacer(modifier = Modifier.height(40.dp))
        
        Text(text = "Contact Us", style = MaterialTheme.typography.titleMedium.copy(fontWeight = FontWeight.Bold, fontSize = 18.sp, letterSpacing = 1.sp), color = colorPalette.text.copy(alpha = 0.8f), modifier = Modifier.fillMaxWidth(), textAlign = TextAlign.Start)
        Spacer(modifier = Modifier.height(16.dp))
        
        Card(
            modifier = Modifier.fillMaxWidth(),
            shape = RoundedCornerShape(24.dp),
            colors = CardDefaults.cardColors(containerColor = colorPalette.text.copy(alpha = 0.04f))
        ) {
            // چیدمان دوتایی زیر هم (کلا ۲ ردیف و در هر ردیف ۲ لوگو برای جلوگیری از کوچک شدن)
            Column(
                modifier = Modifier.fillMaxWidth().padding(vertical = 24.dp, horizontal = 12.dp),
                verticalArrangement = Arrangement.spacedBy(24.dp)
            ) {
                // ردیف اول: وبسایت و اینستاگرام
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.SpaceEvenly,
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    // Website
                    Column(horizontalAlignment = Alignment.CenterHorizontally, modifier = Modifier.clip(RoundedCornerShape(16.dp)).clickable { Toast.makeText(context, "Website: Coming soon", Toast.LENGTH_SHORT).show() }.padding(8.dp)) {
                        Box(modifier = Modifier.size(80.dp).clip(CircleShape).background(colorPalette.text.copy(alpha = 0.08f)), contentAlignment = Alignment.Center) {
                            Icon(imageVector = Icons.Default.Language, contentDescription = null, modifier = Modifier.size(44.dp), tint = colorPalette.text)
                        }
                        Spacer(modifier = Modifier.height(10.dp))
                        Text(text = "Website", style = MaterialTheme.typography.labelMedium.copy(fontWeight = FontWeight.Bold, fontSize = 14.sp), color = colorPalette.text.copy(alpha = 0.7f))
                    }
                    
                    // Instagram
                    Column(horizontalAlignment = Alignment.CenterHorizontally, modifier = Modifier.clip(RoundedCornerShape(16.dp)).clickable { Toast.makeText(context, "Instagram: Coming soon", Toast.LENGTH_SHORT).show() }.padding(8.dp)) {
                        Box(modifier = Modifier.size(80.dp).clip(CircleShape).background(colorPalette.text.copy(alpha = 0.08f)), contentAlignment = Alignment.Center) {
                            Icon(imageVector = ImageVector.vectorResource(R.drawable.ic_instagram_custom), contentDescription = null, modifier = Modifier.size(44.dp), tint = colorPalette.text)
                        }
                        Spacer(modifier = Modifier.height(10.dp))
                        Text(text = "Instagram", style = MaterialTheme.typography.labelMedium.copy(fontWeight = FontWeight.Bold, fontSize = 14.sp), color = colorPalette.text.copy(alpha = 0.7f))
                    }
                }
                
                // ردیف دوم: ایمیل و تلگرام
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.SpaceEvenly,
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    // Email
                    Column(horizontalAlignment = Alignment.CenterHorizontally, modifier = Modifier.clip(RoundedCornerShape(16.dp)).clickable { Toast.makeText(context, "Email: Coming soon", Toast.LENGTH_SHORT).show() }.padding(8.dp)) {
                        Box(modifier = Modifier.size(80.dp).clip(CircleShape).background(colorPalette.text.copy(alpha = 0.08f)), contentAlignment = Alignment.Center) {
                            Icon(imageVector = Icons.Default.Email, contentDescription = null, modifier = Modifier.size(44.dp), tint = colorPalette.text)
                        }
                        Spacer(modifier = Modifier.height(10.dp))
                        Text(text = "Email", style = MaterialTheme.typography.labelMedium.copy(fontWeight = FontWeight.Bold, fontSize = 14.sp), color = colorPalette.text.copy(alpha = 0.7f))
                    }
                    
                    // Telegram
                    Column(horizontalAlignment = Alignment.CenterHorizontally, modifier = Modifier.clip(RoundedCornerShape(16.dp)).clickable { Toast.makeText(context, "Telegram: Coming soon", Toast.LENGTH_SHORT).show() }.padding(8.dp)) {
                        Box(modifier = Modifier.size(80.dp).clip(CircleShape).background(colorPalette.text.copy(alpha = 0.08f)), contentAlignment = Alignment.Center) {
                            Icon(imageVector = ImageVector.vectorResource(R.drawable.ic_telegram_custom), contentDescription = null, modifier = Modifier.size(44.dp), tint = colorPalette.text)
                        }
                        Spacer(modifier = Modifier.height(10.dp))
                        Text(text = "Telegram", style = MaterialTheme.typography.labelMedium.copy(fontWeight = FontWeight.Bold, fontSize = 14.sp), color = colorPalette.text.copy(alpha = 0.7f))
                    }
                }
            }
        }
    }
}
