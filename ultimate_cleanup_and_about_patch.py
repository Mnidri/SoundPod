import os
import re

# ۱. اصلاح کامل دیزاین آلبوم، بازگرداندن متن کلیکی آرتیست بدون تداخل لمس کاور
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
import androidx.compose.ui.draw.clip
import androidx.compose.ui.draw.shadow
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
                Icon(imageVector = Icons.Default.Search, contentDescription = null, tint = colorPalette.text)
            }
        },
        dropDownMenuContent = { dismissMenu ->
            DropdownMenuItem(text = { Text(stringResource(id = R.string.settings), color = colorPalette.text) }, onClick = { onSettingsClick(); dismissMenu() })
        },
        headerContent = {
            Column(
                modifier = Modifier.fillMaxWidth().padding(top = 32.dp, bottom = 24.dp),
                horizontalAlignment = Alignment.CenterHorizontally
            ) {
                // کاور شیک و مستقل در مرکز بدون هیچ تداخل لمسی
                AsyncImage(
                    model = highResCover, 
                    contentDescription = null, 
                    modifier = Modifier.fillMaxWidth(0.6f).aspectRatio(1f).shadow(20.dp, RoundedCornerShape(16.dp)).clip(RoundedCornerShape(16.dp)),
                    contentScale = ContentScale.Crop
                )
                
                Spacer(modifier = Modifier.height(24.dp))
                
                Text(
                    text = album?.title.orEmpty(),
                    style = typography.titleLarge.copy(fontWeight = FontWeight.ExtraBold, fontSize = 24.sp),
                    color = colorPalette.text,
                    textAlign = TextAlign.Center,
                    maxLines = 2,
                    overflow = TextOverflow.Ellipsis,
                    modifier = Modifier.fillMaxWidth(0.85f)
                )
                
                Spacer(modifier = Modifier.height(8.dp))
                
                // متن کلیکی خواننده کاملاً تفکیک‌شده و بدون اورلپ
                Box(
                    modifier = Modifier
                        .clip(RoundedCornerShape(8.dp))
                        .background(colorPalette.text.copy(alpha = 0.05f))
                        .clickable(enabled = album?.artistId != null) { album?.artistId?.let { onGoToArtist(it) } }
                        .padding(horizontal = 14.dp, vertical = 6.dp)
                ) {
                    Text(
                        text = album?.authorsText.orEmpty(),
                        style = typography.titleMedium.copy(fontWeight = FontWeight.Bold, color = colorPalette.accent),
                        textAlign = TextAlign.Center,
                        maxLines = 1,
                        overflow = TextOverflow.Ellipsis
                    )
                }
                
                album?.year?.let {
                    Spacer(modifier = Modifier.height(8.dp))
                    Text(
                        text = "Released: " + it,
                        style = typography.bodyMedium,
                        color = colorPalette.text.copy(alpha = 0.5f),
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
                        colors = ButtonDefaults.buttonColors(containerColor = colorPalette.text, contentColor = colorPalette.background0),
                        shape = RoundedCornerShape(50),
                        modifier = Modifier.height(52.dp).width(150.dp)
                    ) {
                        Icon(Icons.Default.PlayArrow, contentDescription = null, modifier = Modifier.size(26.dp))
                        Spacer(modifier = Modifier.width(8.dp))
                        Text("Play", fontWeight = FontWeight.Bold, fontSize = 17.sp)
                    }
                    Spacer(modifier = Modifier.width(16.dp))
                    IconButton(
                        onClick = { viewModel.toggleLove() },
                        modifier = Modifier.size(52.dp).clip(CircleShape).background(colorPalette.text.copy(alpha = 0.08f))
                    ) {
                        Icon(
                            imageVector = ImageVector.vectorResource(if (uiState.isLoved) R.drawable.heart else R.drawable.heart_outline),
                            contentDescription = null, 
                            tint = if (uiState.isLoved) Color(0xFFFF4B4B) else colorPalette.text, 
                            modifier = Modifier.size(26.dp)
                        )
                    }
                }
            }
        },
        content = { AlbumSongs(browseId = browseId, onGoToArtist = onGoToArtist) }
    )
}
"""
with open(fp_album, "w") as f: f.write(code_album)


# ۲. تغییر تغییر ورژن کل نرم‌افزار به 1.0.0 در build.gradle.kts
fp_gradle = "app/build.gradle.kts"
if os.path.exists(fp_gradle):
    with open(fp_gradle, "r") as f: gradle_code = f.read()
    gradle_code = re.sub(r'versionName\s*=\s*"[^"]+"', 'versionName = "1.0.0"', gradle_code)
    gradle_code = re.sub(r'versionCode\s*=\s*\d+', 'versionCode = 1', gradle_code)
    with open(fp_gradle, "w") as f: f.write(gradle_code)


# ۳. بازنویسی کامل صفحه About با دیزاین لوکس ارتباط با ما و پاپ آپ Coming Soon
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
        
        // آیکون بزرگ و مینیمال اپلیکیشن
        Icon(
            painter = painterResource(id = R.drawable.app_icon),
            contentDescription = null,
            modifier = Modifier
                .size(130.dp)
                .clip(RoundedCornerShape(32.dp)),
            tint = colorPalette.text
        )
        
        Spacer(modifier = Modifier.height(16.dp))
        
        // نام برند جدید شما
        Text(
            text = "Musick",
            style = MaterialTheme.typography.headlineMedium.copy(fontWeight = FontWeight.Black, fontSize = 30.sp),
            color = colorPalette.text,
            textAlign = TextAlign.Center
        )
        
        // ورژن پایه و جدید ۱.۰.۰
        Text(
            text = "Version 1.0.0",
            style = MaterialTheme.typography.bodyLarge.copy(fontWeight = FontWeight.Medium),
            color = colorPalette.text.copy(alpha = 0.5f),
            modifier = Modifier.padding(top = 4.dp),
            textAlign = TextAlign.Center
        )
        
        Spacer(modifier = Modifier.height(48.dp))
        
        // هدر کارت ارتباط با ما
        Text(
            text = "Contact Us",
            style = MaterialTheme.typography.titleMedium.copy(fontWeight = FontWeight.Bold, fontSize = 18.sp, letterSpacing = 1.sp),
            color = colorPalette.text.copy(alpha = 0.8f),
            modifier = Modifier.fillMaxWidth(),
            textAlign = TextAlign.Start
        )
        
        Spacer(modifier = Modifier.height(12.dp))
        
        // کارت لوکس شیشه‌ای/مات برای بخش دکمه‌های شبکه اجتماعی
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
                // لیست دکمه ها با لوگوهای بزرگ و افکت Coming Soon توست ردیف شد
                val socialButtons = listOf(
                    Triple(R.drawable.idea, "Website"),
                    Triple(R.drawable.github, "Instagram"),
                    Triple(R.drawable.bug, "Email"),
                    Triple(R.drawable.app_icon, "Telegram")
                )
                
                socialButtons.forEach { (iconId, name) ->
                    Column(
                        horizontalAlignment = Alignment.CenterHorizontally,
                        modifier = Modifier
                            .clip(RoundedCornerShape(16.dp))
                            .clickable { 
                                Toast.makeText(context, "$name: Coming soon", Toast.LENGTH_SHORT).show()
                            }
                            .padding(8.dp)
                    ) {
                        Box(
                            modifier = Modifier
                                .size(56.dp)
                                .clip(CircleShape)
                                .background(colorPalette.text.copy(alpha = 0.08f)),
                            contentAlignment = Alignment.Center
                        ) {
                            Icon(
                                painter = painterResource(id = iconId),
                                contentDescription = name,
                                modifier = Modifier.size(28.dp),
                                tint = colorPalette.text
                            )
                        }
                        Spacer(modifier = Modifier.height(8.dp))
                        Text(
                            text = name,
                            style = MaterialTheme.typography.labelMedium.copy(fontWeight = FontWeight.SemiBold),
                            color = colorPalette.text.copy(alpha = 0.6f)
                        )
                    }
                }
            }
        }
    }
}
"""
with open(fp_about, "w") as f: f.write(code_about)

print("All modifications completed! Ready to compile Version 1.0.0 with Premium About Screen.")
