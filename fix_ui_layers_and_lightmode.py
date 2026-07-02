import os
import re

home_file = "app/src/main/kotlin/com/github/soundpod/ui/screens/home/HomeScreen.kt"

# ۱. جایگذاری کدهای HomeScreen کاملاً تمیز، بدون فاصله‌های اضافی و با دیالوگ هوشمند دو-تمه
code_home = """@file:OptIn(androidx.compose.foundation.ExperimentalFoundationApi::class, androidx.compose.animation.ExperimentalAnimationApi::class, androidx.compose.material3.ExperimentalMaterial3Api::class)
package com.github.soundpod.ui.screens.home

import android.widget.Toast
import androidx.compose.animation.*
import androidx.compose.animation.core.tween
import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.isSystemInDarkTheme
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.pager.HorizontalPager
import androidx.compose.foundation.pager.rememberPagerState
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Search
import androidx.compose.material.icons.rounded.AccountCircle
import androidx.compose.material.icons.rounded.ChevronRight
import androidx.compose.material.icons.rounded.Person
import androidx.compose.material.icons.rounded.Settings
import androidx.compose.material.icons.rounded.Star
import androidx.compose.material.icons.rounded.Translate
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.TransformOrigin
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.TextStyle
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.navigation.NavController
import androidx.lifecycle.viewmodel.compose.viewModel
import com.github.soundpod.ui.components.HorizontalTabs
import com.github.soundpod.enums.BuiltInPlaylist
import com.github.soundpod.ui.navigation.Routes
import com.github.soundpod.ui.screens.favorites.FavoritesScreen
import com.github.soundpod.viewmodels.home.HomeViewModel

@Composable
fun HomeScreen(navController: NavController, onSettingsClick: () -> Unit) {
    val homeViewModel: HomeViewModel = viewModel()
    val pagerState = rememberPagerState(initialPage = 0) { homeViewModel.tabs.size }
    val navigateToAlbum = { browseId: String -> navController.navigate(route = Routes.Album(id = browseId)) }
    val navigateToArtist = { browseId: String -> navController.navigate(route = Routes.Artist(id = browseId)) }
    
    val bgColor = MaterialTheme.colorScheme.background
    val textColor = MaterialTheme.colorScheme.onBackground
    val context = LocalContext.current
    val isDark = isSystemInDarkTheme()
    
    var showProfileOverlay by remember { mutableStateOf(false) }
    var expandedSection by remember { mutableStateOf<String?>(null) }
    var aiTranslationEnabled by remember { mutableStateOf(false) }
    var apiToken by remember { mutableStateOf("") }

    Box(modifier = Modifier.fillMaxSize()) {
        Scaffold(
            containerColor = bgColor,
            topBar = {
                TopAppBar(
                    title = {
                        Text(
                            text = "Musick",
                            fontSize = 44.sp,
                            fontWeight = FontWeight.ExtraBold,
                            fontFamily = FontFamily.Serif,
                            letterSpacing = (-1.5).sp,
                            color = textColor
                        )
                    },
                    actions = {
                        IconButton(onClick = { navController.navigate(route = Routes.Search) }) {
                            Icon(imageVector = Icons.Default.Search, contentDescription = "Search", tint = textColor)
                        }
                        Spacer(modifier = Modifier.width(4.dp))
                        OutlinedIconButton(onClick = { showProfileOverlay = true }, border = BorderStroke(1.dp, textColor.copy(alpha = 0.15f))) {
                            Icon(imageVector = Icons.Rounded.Person, contentDescription = "Profile", tint = textColor)
                        }
                    },
                    colors = TopAppBarDefaults.topAppBarColors(containerColor = bgColor)
                )
            }
        ) { paddingValues ->
            // در اینجا هیچ پدینگ و فاصله اضافی بین لیست‌ها اعمال نشده و ساختار دقیقاً اورجینال است
            Box(modifier = Modifier.fillMaxSize().padding(paddingValues)) {
                Column(modifier = Modifier.fillMaxSize()) {
                    HorizontalTabs(pagerState = pagerState, tabs = homeViewModel.tabs)
                    HorizontalPager(state = pagerState, beyondViewportPageCount = 4, modifier = Modifier.weight(1f).background(Color.Transparent)) { page ->
                        when (page) {
                            0 -> QuickPicks(onAlbumClick = navigateToAlbum, onArtistClick = navigateToArtist, onPlaylistClick = { browseId -> navController.navigate(route = Routes.Playlist(id = browseId)) }, onOfflinePlaylistClick = { navController.navigate(route = Routes.BuiltInPlaylist(index = 1)) })
                            1 -> FavoritesScreen(onFavoriteTracksClick = { navController.navigate(route = Routes.FavoriteTracks) }, onGoToAlbum = navigateToAlbum, onGoToArtist = navigateToArtist, isEmbedded = true)
                            2 -> HomeSongs(onGoToAlbum = navigateToAlbum, onGoToArtist = navigateToArtist)
                            3 -> HomeArtistList(onArtistClick = { artist -> navigateToArtist(artist.id) })
                            4 -> HomeAlbums(onAlbumClick = { album -> navigateToAlbum(album.id) })
                            5 -> HomePlaylists(onBuiltInPlaylist = { playlistIndex -> if (playlistIndex == BuiltInPlaylist.Favorites.ordinal) navController.navigate(route = Routes.Favorites) else navController.navigate(route = Routes.BuiltInPlaylist(index = playlistIndex)) }, onPlaylistClick = { playlist -> navController.navigate(route = Routes.LocalPlaylist(id = playlist.id)) })
                        }
                    }
                }
            }
        }
        
        // دیالوگ شیشه‌ای
        AnimatedVisibility(
            visible = showProfileOverlay,
            enter = fadeIn(tween(300)) + scaleIn(tween(300), transformOrigin = TransformOrigin(0.9f, 0.05f)),
            exit = fadeOut(tween(200)) + scaleOut(tween(200), transformOrigin = TransformOrigin(0.9f, 0.05f)),
            modifier = Modifier.fillMaxSize()
        ) {
            Box(
                modifier = Modifier
                    .fillMaxSize()
                    .background(Color.Transparent) // لایه سوم (تاریکی کل صفحه) کاملاً حذف شده
                    .clickable { showProfileOverlay = false },
                contentAlignment = Alignment.Center
            ) {
                // رنگ‌بندی داینامیک برای لایه بنفش و زرد
                val outerGlassColor = if (isDark) Color.Black.copy(alpha = 0.35f) else Color.White.copy(alpha = 0.65f)
                val innerGlassColor = if (isDark) Color.Black.copy(alpha = 0.85f) else Color(0xFFF3F3F3).copy(alpha = 0.98f)
                val innerTextColor = if (isDark) Color.White else Color.Black
                val itemBorderColor = if (isDark) Color.White.copy(alpha = 0.15f) else Color.Black.copy(alpha = 0.1f)

                // لایه بنفش (کادر اصلی): شفاف‌تر و ملایم‌تر
                Card(
                    shape = RoundedCornerShape(28.dp),
                    colors = CardDefaults.cardColors(containerColor = outerGlassColor),
                    border = BorderStroke(1.dp, textColor.copy(alpha = 0.15f)),
                    modifier = Modifier.fillMaxWidth(0.92f).clickable(enabled = false) {} 
                ) {
                    Column(
                        modifier = Modifier
                            .fillMaxWidth()
                            .padding(horizontal = 24.dp, vertical = 28.dp),
                        horizontalAlignment = Alignment.CenterHorizontally
                    ) {
                        // لایه‌های زرد (گزینه‌های داخلی): غلیظ‌تر و تیره/مات
                        
                        Card(
                            modifier = Modifier.fillMaxWidth().clickable { showProfileOverlay = false; /* TODO: Navigation */ },
                            shape = RoundedCornerShape(18.dp),
                            colors = CardDefaults.cardColors(containerColor = innerGlassColor),
                            border = BorderStroke(1.5.dp, MaterialTheme.colorScheme.primary.copy(alpha = 0.8f))
                        ) {
                            Row(modifier = Modifier.fillMaxWidth().padding(14.dp), verticalAlignment = Alignment.CenterVertically) {
                                Box(modifier = Modifier.size(46.dp).clip(CircleShape).background(MaterialTheme.colorScheme.primary.copy(alpha = 0.15f)), contentAlignment = Alignment.Center) {
                                    Icon(Icons.Rounded.AccountCircle, contentDescription = null, modifier = Modifier.size(28.dp), tint = MaterialTheme.colorScheme.primary)
                                }
                                Spacer(modifier = Modifier.width(14.dp))
                                Column(modifier = Modifier.weight(1f)) {
                                    Text("Sign in to Musick", style = TextStyle(fontWeight = FontWeight.Bold, fontSize = 16.sp), color = innerTextColor)
                                    Text("Set up local sync profile", style = TextStyle(fontWeight = FontWeight.Medium, fontSize = 11.sp), color = innerTextColor.copy(alpha = 0.6f))
                                }
                                Icon(Icons.Rounded.ChevronRight, contentDescription = null, tint = innerTextColor.copy(alpha = 0.5f))
                            }
                        }

                        Spacer(modifier = Modifier.height(14.dp))

                        Card(modifier = Modifier.fillMaxWidth(), shape = RoundedCornerShape(18.dp), colors = CardDefaults.cardColors(containerColor = innerGlassColor), border = BorderStroke(1.5.dp, Color(0xFFFFD700).copy(alpha = 0.8f))) {
                            Column(modifier = Modifier.fillMaxWidth().clickable { expandedSection = if (expandedSection == "premium") null else "premium" }.padding(12.dp)) {
                                Row(verticalAlignment = Alignment.CenterVertically) {
                                    Box(modifier = Modifier.size(42.dp).clip(CircleShape).background(Color(0xFFFFD700).copy(alpha = 0.15f)), contentAlignment = Alignment.Center) {
                                        Icon(Icons.Rounded.Star, contentDescription = null, tint = Color(0xFFFFD700), modifier = Modifier.size(22.dp))
                                    }
                                    Spacer(modifier = Modifier.width(14.dp))
                                    Column {
                                        Text("Musick Premium", style = TextStyle(fontWeight = FontWeight.Bold, fontSize = 15.sp), color = innerTextColor)
                                        Text("Exclusive layouts & quality", style = TextStyle(fontWeight = FontWeight.Medium, fontSize = 11.sp), color = innerTextColor.copy(alpha = 0.6f))
                                    }
                                }
                                AnimatedVisibility(visible = expandedSection == "premium") {
                                    Text("Unlock ad-free streaming, maximum audio bitrate, and elite adaptive designs.", style = TextStyle(fontSize = 13.sp, lineHeight = 18.sp), color = innerTextColor.copy(alpha = 0.8f), modifier = Modifier.padding(top = 10.dp, start = 6.dp, end = 6.dp))
                                }
                            }
                        }

                        Spacer(modifier = Modifier.height(14.dp))

                        Card(modifier = Modifier.fillMaxWidth(), shape = RoundedCornerShape(18.dp), colors = CardDefaults.cardColors(containerColor = innerGlassColor), border = BorderStroke(1.2.dp, itemBorderColor)) {
                            Column(modifier = Modifier.fillMaxWidth().clickable { expandedSection = if (expandedSection == "ai") null else "ai" }.padding(12.dp)) {
                                Row(verticalAlignment = Alignment.CenterVertically) {
                                    Box(modifier = Modifier.size(42.dp).clip(CircleShape).background(innerTextColor.copy(alpha = 0.08f)), contentAlignment = Alignment.Center) {
                                        Icon(Icons.Rounded.Translate, contentDescription = null, tint = innerTextColor, modifier = Modifier.size(22.dp))
                                    }
                                    Spacer(modifier = Modifier.width(14.dp))
                                    Column {
                                        Text("AI Translation", style = TextStyle(fontWeight = FontWeight.Bold, fontSize = 15.sp), color = innerTextColor)
                                        Text("Translate lyrics instantly", style = TextStyle(fontWeight = FontWeight.Medium, fontSize = 11.sp), color = innerTextColor.copy(alpha = 0.6f))
                                    }
                                }
                                AnimatedVisibility(visible = expandedSection == "ai") {
                                    Column(modifier = Modifier.fillMaxWidth().padding(top = 10.dp, start = 6.dp, end = 6.dp)) {
                                        Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween, verticalAlignment = Alignment.CenterVertically) {
                                            Text("Enable Smart Lyrics", style = TextStyle(fontWeight = FontWeight.Medium, fontSize = 13.sp), color = innerTextColor.copy(alpha = 0.9f))
                                            Switch(checked = aiTranslationEnabled, onCheckedChange = { if (apiToken.isBlank()) Toast.makeText(context, "Please enter your API token first", Toast.LENGTH_SHORT).show() else aiTranslationEnabled = it })
                                        }
                                        Spacer(modifier = Modifier.height(8.dp))
                                        OutlinedTextField(
                                            value = apiToken, onValueChange = { apiToken = it },
                                            label = { Text("API Token", fontSize = 12.sp, color = innerTextColor.copy(alpha = 0.6f)) },
                                            placeholder = { Text("Enter token key") },
                                            modifier = Modifier.fillMaxWidth(), singleLine = true, shape = RoundedCornerShape(10.dp),
                                            colors = OutlinedTextFieldDefaults.colors(focusedTextColor = innerTextColor, unfocusedTextColor = innerTextColor)
                                        )
                                    }
                                }
                            }
                        }

                        Spacer(modifier = Modifier.height(14.dp))

                        Card(modifier = Modifier.fillMaxWidth(), shape = RoundedCornerShape(18.dp), colors = CardDefaults.cardColors(containerColor = innerGlassColor), border = BorderStroke(1.2.dp, itemBorderColor)) {
                            Row(modifier = Modifier.fillMaxWidth().clickable { showProfileOverlay = false; onSettingsClick() }.padding(14.dp), verticalAlignment = Alignment.CenterVertically) {
                                Box(modifier = Modifier.size(42.dp).clip(CircleShape).background(innerTextColor.copy(alpha = 0.08f)), contentAlignment = Alignment.Center) {
                                    Icon(Icons.Rounded.Settings, contentDescription = null, tint = innerTextColor, modifier = Modifier.size(22.dp))
                                }
                                Spacer(modifier = Modifier.width(14.dp))
                                Text("Settings", style = TextStyle(fontWeight = FontWeight.Bold, fontSize = 15.sp), color = innerTextColor)
                            }
                        }
                    }
                }
            }
        }
    }
}
"""

with open(home_file, "w") as f: f.write(code_home)

# ۲. جستجو و اصلاح رنگ تب‌ها در فایل‌های کامپوننت و آرتیست (حل مشکل لایت‌مود)
files_to_fix_tabs = [
    "app/src/main/kotlin/com/github/soundpod/ui/components/HorizontalTabs.kt",
    "app/src/main/kotlin/com/github/soundpod/ui/screens/artist/ArtistScreen.kt"
]

for fp in files_to_fix_tabs:
    if os.path.exists(fp):
        with open(fp, "r") as f:
            content = f.read()
        
        # جایگزینی رنگ سفید ثابت با رنگ متنی که متناسب با تم تغییر می‌کند
        content = re.sub(r'Color\.White(?!\.copy)', 'MaterialTheme.colorScheme.onBackground', content)
        
        with open(fp, "w") as f:
            f.write(content)

print("SUCCESS: UI Layers updated for Light/Dark mode and Spacing reverted safely!")
