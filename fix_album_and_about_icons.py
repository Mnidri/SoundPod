import os

# ۱. ساخت آیکون‌های اورجینال تلگرام و اینستاگرام با کدهای Vector XML
res_dir = "app/src/main/res/drawable"
os.makedirs(res_dir, exist_ok=True)

with open(f"{res_dir}/ic_telegram_custom.xml", "w") as f:
    f.write("""<vector xmlns:android="http://schemas.android.com/apk/res/android"
    android:width="24dp" android:height="24dp" android:viewportWidth="24" android:viewportHeight="24">
    <path android:fillColor="#FFFFFFFF" android:pathData="M11.94,10.66l-2.45,7.9l2.76,-4.24l4.24,3.15l2.67,-14.28L3.25,9.66l3.96,1.27l10.02,-6.33L11.94,10.66z"/>
</vector>""")

with open(f"{res_dir}/ic_instagram_custom.xml", "w") as f:
    f.write("""<vector xmlns:android="http://schemas.android.com/apk/res/android"
    android:width="24dp" android:height="24dp" android:viewportWidth="24" android:viewportHeight="24">
    <path android:fillColor="#00000000" android:strokeColor="#FFFFFFFF" android:strokeWidth="2" android:pathData="M7,2h10c2.76,0 5,2.24 5,5v10c0,2.76 -2.24,5 -5,5h-10c-2.76,0 -5,-2.24 -5,-5v-10c0,-2.76 2.24,-5 5,-5z" />
    <path android:fillColor="#00000000" android:strokeColor="#FFFFFFFF" android:strokeWidth="2" android:pathData="M12,7c-2.76,0 -5,2.24 -5,5s2.24,5 5,5 5,-2.24 5,-5 -2.24,-5 -5,-5z" />
    <path android:fillColor="#FFFFFFFF" android:pathData="M17.5,6.5m-1,0a1,1 0,1 1,2 0a1,1 0,1 1,-2 0" />
</vector>""")


# ۲. بازنویسی صفحه About با آیکون‌های صحیح، بزرگ و دوبرابر شده
fp_about = "app/src/main/kotlin/com/github/soundpod/ui/screens/settings/About.kt"
if not os.path.exists(fp_about): fp_about = "app/src/main/kotlin/com/github/musick/ui/screens/settings/About.kt"

code_about = """package com.github.musick.ui.screens.settings

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
        
        Spacer(modifier = Modifier.height(48.dp))
        
        Text(text = "Contact Us", style = MaterialTheme.typography.titleMedium.copy(fontWeight = FontWeight.Bold, fontSize = 18.sp, letterSpacing = 1.sp), color = colorPalette.text.copy(alpha = 0.8f), modifier = Modifier.fillMaxWidth(), textAlign = TextAlign.Start)
        Spacer(modifier = Modifier.height(12.dp))
        
        Card(
            modifier = Modifier.fillMaxWidth(),
            shape = RoundedCornerShape(24.dp),
            colors = CardDefaults.cardColors(containerColor = colorPalette.text.copy(alpha = 0.04f))
        ) {
            Row(
                modifier = Modifier.fillMaxWidth().padding(vertical = 32.dp, horizontal = 12.dp),
                horizontalArrangement = Arrangement.SpaceEvenly,
                verticalAlignment = Alignment.CenterVertically
            ) {
                // Website
                Column(horizontalAlignment = Alignment.CenterHorizontally, modifier = Modifier.clip(RoundedCornerShape(16.dp)).clickable { Toast.makeText(context, "Website: Coming soon", Toast.LENGTH_SHORT).show() }.padding(8.dp)) {
                    Box(modifier = Modifier.size(72.dp).clip(CircleShape).background(colorPalette.text.copy(alpha = 0.08f)), contentAlignment = Alignment.Center) {
                        Icon(imageVector = Icons.Default.Language, contentDescription = null, modifier = Modifier.size(40.dp), tint = colorPalette.text)
                    }
                    Spacer(modifier = Modifier.height(10.dp))
                    Text(text = "Website", style = MaterialTheme.typography.labelMedium.copy(fontWeight = FontWeight.Bold), color = colorPalette.text.copy(alpha = 0.7f))
                }
                
                // Instagram
                Column(horizontalAlignment = Alignment.CenterHorizontally, modifier = Modifier.clip(RoundedCornerShape(16.dp)).clickable { Toast.makeText(context, "Instagram: Coming soon", Toast.LENGTH_SHORT).show() }.padding(8.dp)) {
                    Box(modifier = Modifier.size(72.dp).clip(CircleShape).background(colorPalette.text.copy(alpha = 0.08f)), contentAlignment = Alignment.Center) {
                        Icon(imageVector = ImageVector.vectorResource(R.drawable.ic_instagram_custom), contentDescription = null, modifier = Modifier.size(40.dp), tint = colorPalette.text)
                    }
                    Spacer(modifier = Modifier.height(10.dp))
                    Text(text = "Instagram", style = MaterialTheme.typography.labelMedium.copy(fontWeight = FontWeight.Bold), color = colorPalette.text.copy(alpha = 0.7f))
                }
                
                // Email
                Column(horizontalAlignment = Alignment.CenterHorizontally, modifier = Modifier.clip(RoundedCornerShape(16.dp)).clickable { Toast.makeText(context, "Email: Coming soon", Toast.LENGTH_SHORT).show() }.padding(8.dp)) {
                    Box(modifier = Modifier.size(72.dp).clip(CircleShape).background(colorPalette.text.copy(alpha = 0.08f)), contentAlignment = Alignment.Center) {
                        Icon(imageVector = Icons.Default.Email, contentDescription = null, modifier = Modifier.size(40.dp), tint = colorPalette.text)
                    }
                    Spacer(modifier = Modifier.height(10.dp))
                    Text(text = "Email", style = MaterialTheme.typography.labelMedium.copy(fontWeight = FontWeight.Bold), color = colorPalette.text.copy(alpha = 0.7f))
                }
                
                // Telegram
                Column(horizontalAlignment = Alignment.CenterHorizontally, modifier = Modifier.clip(RoundedCornerShape(16.dp)).clickable { Toast.makeText(context, "Telegram: Coming soon", Toast.LENGTH_SHORT).show() }.padding(8.dp)) {
                    Box(modifier = Modifier.size(72.dp).clip(CircleShape).background(colorPalette.text.copy(alpha = 0.08f)), contentAlignment = Alignment.Center) {
                        Icon(imageVector = ImageVector.vectorResource(R.drawable.ic_telegram_custom), contentDescription = null, modifier = Modifier.size(40.dp), tint = colorPalette.text)
                    }
                    Spacer(modifier = Modifier.height(10.dp))
                    Text(text = "Telegram", style = MaterialTheme.typography.labelMedium.copy(fontWeight = FontWeight.Bold), color = colorPalette.text.copy(alpha = 0.7f))
                }
            }
        }
    }
}
"""
with open(fp_about, "w") as f: f.write(code_about)


# ۳. بازنویسی اساسی دیزاین صفحه آلبوم/سینگل
fp_album = "app/src/main/kotlin/com/github/soundpod/ui/screens/album/AlbumScreen.kt"
if not os.path.exists(fp_album): fp_album = "app/src/main/kotlin/com/github/musick/ui/screens/album/AlbumScreen.kt"

code_album = """package com.github.musick.ui.screens.album

import androidx.activity.compose.BackHandler
import androidx.compose.animation.ExperimentalAnimationApi
import androidx.compose.foundation.ExperimentalFoundationApi
import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.PlayArrow
import androidx.compose.material.icons.filled.Search
import androidx.compose.material3.Button
import androidx.compose.material3.ButtonDefaults
import androidx.compose.material3.DropdownMenuItem
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.MaterialTheme.typography
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.blur
import androidx.compose.ui.draw.clip
import androidx.compose.ui.draw.shadow
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.res.stringResource
import androidx.compose.ui.res.vectorResource
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.lifecycle.viewmodel.compose.viewModel
import coil3.compose.AsyncImage
import com.github.core.ui.LocalAppearance
import com.github.musick.R
import com.github.musick.ui.components.PlaylistScreenLayout
import com.github.musick.viewmodels.AlbumViewModel

fun extractHighResUrl(rawThumb: String?): String {
    if (rawThumb == null) return ""
    var extracted = if (rawThumb.contains("url=")) Regex("url=([^,)]+)").find(rawThumb)?.groupValues?.get(1) ?: rawThumb else rawThumb
    extracted = if (extracted.startsWith("//")) "https:$extracted" else extracted
    return extracted.replace(Regex("=w\\\\d+-h\\\\d+"), "=w1080-h1080").replace(Regex("=s\\\\d+"), "=s1080")
}

@OptIn(ExperimentalAnimationApi::class, ExperimentalFoundationApi::class)
@Composable
fun AlbumScreen(
    browseId: String,
    onGoToArtist: (String) -> Unit,
    onBack: () -> Unit,
    onSearchClick: () -> Unit,
    onSettingsClick: () -> Unit,
    viewModel: AlbumViewModel = viewModel(),
) {
    BackHandler { onBack() }
    LaunchedEffect(browseId) { viewModel.initAlbum(browseId) }
    val uiState by viewModel.uiState.collectAsState()
    val album = uiState.album
    val (colorPalette) = LocalAppearance.current
    val highResCover = extractHighResUrl(album?.thumbnailUrl)
    
    PlaylistScreenLayout(
        onBackClick = onBack,
        title = { },
        actions = {
            IconButton(onClick = onSearchClick) {
                Icon(imageVector = Icons.Default.Search, contentDescription = null, tint = Color.White)
            }
        },
        dropDownMenuContent = { dismissMenu ->
            DropdownMenuItem(text = { Text(stringResource(id = R.string.settings), color = colorPalette.text) }, onClick = { onSettingsClick(); dismissMenu() })
        },
        headerContent = {
            Box(modifier = Modifier.fillMaxWidth().wrapContentHeight()) {
                // افکت بلر پشت صفحه
                AsyncImage(model = highResCover, contentDescription = null, modifier = Modifier.fillMaxWidth().height(400.dp).blur(60.dp), contentScale = ContentScale.Crop)
                Box(modifier = Modifier.fillMaxWidth().height(400.dp).background(Brush.verticalGradient(listOf(Color.Black.copy(alpha = 0.3f), Color.Black))))
                
                Column(
                    modifier = Modifier.fillMaxWidth().padding(top = 40.dp, bottom = 24.dp),
                    horizontalAlignment = Alignment.CenterHorizontally
                ) {
                    // کاور اصلی با سایز ایده آل و لبه های نرم (کاملا دور از متن ها)
                    AsyncImage(
                        model = highResCover, 
                        contentDescription = null, 
                        modifier = Modifier.fillMaxWidth(0.65f).aspectRatio(1f).shadow(24.dp, RoundedCornerShape(20.dp)).clip(RoundedCornerShape(20.dp)),
                        contentScale = ContentScale.Crop
                    )
                    
                    Spacer(modifier = Modifier.height(28.dp))
                    
                    Text(
                        text = album?.title.orEmpty(),
                        style = typography.titleLarge.copy(fontWeight = FontWeight.Black, fontSize = 26.sp),
                        color = Color.White,
                        textAlign = TextAlign.Center,
                        maxLines = 2,
                        overflow = TextOverflow.Ellipsis,
                        modifier = Modifier.fillMaxWidth(0.85f)
                    )
                    
                    Spacer(modifier = Modifier.height(12.dp))
                    
                    // دکمه اختصاصی، واضح و کلیکی برای نام خواننده
                    Box(
                        modifier = Modifier
                            .clip(RoundedCornerShape(12.dp))
                            .background(Color.White.copy(alpha = 0.15f))
                            .clickable(enabled = album?.artistId != null) { album?.artistId?.let { onGoToArtist(it) } }
                            .padding(horizontal = 16.dp, vertical = 8.dp)
                    ) {
                        Text(
                            text = album?.authorsText.orEmpty(),
                            style = typography.titleMedium.copy(fontWeight = FontWeight.Bold),
                            color = Color.White,
                            textAlign = TextAlign.Center,
                            maxLines = 1,
                            overflow = TextOverflow.Ellipsis
                        )
                    }
                    
                    album?.year?.let {
                        Spacer(modifier = Modifier.height(12.dp))
                        Text(
                            text = "Released • " + it,
                            style = typography.bodyMedium.copy(fontWeight = FontWeight.Medium),
                            color = Color.Gray,
                            textAlign = TextAlign.Center
                        )
                    }
                    
                    Spacer(modifier = Modifier.height(24.dp))
                    
                    Row(
                        modifier = Modifier.fillMaxWidth(),
                        horizontalArrangement = Arrangement.Center,
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        Button(
                            onClick = { /* Handle Play */ },
                            colors = ButtonDefaults.buttonColors(containerColor = Color.White, contentColor = Color.Black),
                            shape = RoundedCornerShape(50),
                            modifier = Modifier.height(52.dp).width(150.dp)
                        ) {
                            Icon(Icons.Default.PlayArrow, contentDescription = null, modifier = Modifier.size(26.dp))
                            Spacer(modifier = Modifier.width(8.dp))
                            Text("Play", fontWeight = FontWeight.Black, fontSize = 17.sp)
                        }
                        Spacer(modifier = Modifier.width(16.dp))
                        IconButton(
                            onClick = { viewModel.toggleLove() },
                            modifier = Modifier.size(52.dp).clip(CircleShape).background(Color.White.copy(alpha = 0.1f))
                        ) {
                            Icon(
                                imageVector = ImageVector.vectorResource(if (uiState.isLoved) R.drawable.heart else R.drawable.heart_outline),
                                contentDescription = null, 
                                tint = if (uiState.isLoved) Color(0xFFFF4B4B) else Color.White, 
                                modifier = Modifier.size(26.dp)
                            )
                        }
                    }
                }
            }
        },
        content = { AlbumSongs(browseId = browseId, onGoToArtist = onGoToArtist) }
    )
}
"""
with open(fp_album, "w") as f: f.write(code_album)

print("Icons built natively. Album and About screens perfected!")
