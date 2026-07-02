import os

fp_home = "app/src/main/kotlin/com/github/soundpod/ui/screens/home/HomeScreen.kt"
if not os.path.exists(fp_home): fp_home = "app/src/main/kotlin/com/github/musick/ui/screens/home/HomeScreen.kt"

code_home = """@file:OptIn(androidx.compose.foundation.ExperimentalFoundationApi::class, androidx.compose.animation.ExperimentalAnimationApi::class, androidx.compose.material3.ExperimentalMaterial3Api::class)
package com.github.musick.ui.screens.home

import android.widget.Toast
import androidx.compose.animation.*
import androidx.compose.animation.core.tween
import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
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
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.TransformOrigin
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.res.vectorResource
import androidx.compose.ui.text.TextStyle
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.navigation.NavController
import androidx.lifecycle.viewmodel.compose.viewModel
import com.github.musick.R
import com.github.musick.ui.components.HorizontalTabs
import com.github.musick.enums.BuiltInPlaylist
import com.github.musick.ui.navigation.Routes
import com.github.musick.ui.screens.favorites.FavoritesScreen
import com.github.musick.viewmodels.home.HomeViewModel

@Composable
fun HomeScreen(navController: NavController, onSettingsClick: () -> Unit) {
    val homeViewModel: HomeViewModel = viewModel()
    val pagerState = rememberPagerState(initialPage = 0) { homeViewModel.tabs.size }
    val navigateToAlbum = { browseId: String -> navController.navigate(route = Routes.Album(id = browseId)) }
    val navigateToArtist = { browseId: String -> navController.navigate(route = Routes.Artist(id = browseId)) }
    
    val bgColor = MaterialTheme.colorScheme.background
    val textColor = MaterialTheme.colorScheme.onBackground
    val context = LocalContext.current
    
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
                            fontSize = 46.sp, // بزرگنمایی چشمگیر فونت طبق دستورات قبلی
                            fontWeight = FontWeight.ExtraBold,
                            fontFamily = FontFamily.Serif,
                            letterSpacing = (-1.5).sp,
                            color = textColor,
                            style = TextStyle(shadow = androidx.compose.ui.graphics.Shadow(color = textColor.copy(alpha = 0.5f), blurRadius = 24f))
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
        
        // لایه انیمیشنی پنجره شیشه‌ای (اجرا از نقطه بالا-راست)
        AnimatedVisibility(
            visible = showProfileOverlay,
            enter = fadeIn(tween(300)) + scaleIn(tween(300), transformOrigin = TransformOrigin(0.9f, 0.05f)),
            exit = fadeOut(tween(200)) + scaleOut(tween(200), transformOrigin = TransformOrigin(0.9f, 0.05f)),
            modifier = Modifier.fillMaxSize()
        ) {
            Box(
                modifier = Modifier
                    .fillMaxSize()
                    .background(Color.Black.copy(alpha = 0.6f))
                    .clickable { showProfileOverlay = false },
                contentAlignment = Alignment.TopCenter
            ) {
                Card(
                    shape = RoundedCornerShape(28.dp),
                    colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surface.copy(alpha = 0.85f)),
                    border = BorderStroke(1.dp, textColor.copy(alpha = 0.1f)),
                    modifier = Modifier
                        .fillMaxWidth(0.92f)
                        .padding(top = 90.dp)
                        .clickable(enabled = false) {} 
                ) {
                    Column(
                        modifier = Modifier.fillMaxWidth().padding(16.dp),
                        horizontalAlignment = Alignment.CenterHorizontally
                    ) {
                        // کادر ورود با رنگ برند
                        Card(
                            modifier = Modifier.fillMaxWidth(),
                            shape = RoundedCornerShape(20.dp),
                            colors = CardDefaults.cardColors(containerColor = Color.Transparent),
                            border = BorderStroke(1.5.dp, MaterialTheme.colorScheme.primary)
                        ) {
                            Row(
                                modifier = Modifier
                                    .fillMaxWidth()
                                    .clickable { 
                                        showProfileOverlay = false
                                        Toast.makeText(context, "Navigating to Login Setup...", Toast.LENGTH_SHORT).show()
                                    }
                                    .padding(16.dp),
                                verticalAlignment = Alignment.CenterVertically
                            ) {
                                Box(
                                    modifier = Modifier.size(48.dp).clip(CircleShape).background(MaterialTheme.colorScheme.primary.copy(alpha = 0.15f)),
                                    contentAlignment = Alignment.Center
                                ) {
                                    Icon(Icons.Rounded.AccountCircle, contentDescription = null, modifier = Modifier.size(32.dp), tint = MaterialTheme.colorScheme.primary)
                                }
                                Spacer(modifier = Modifier.width(16.dp))
                                Column(modifier = Modifier.weight(1f)) {
                                    Text("Sign in to Musick", style = TextStyle(fontWeight = FontWeight.Bold, fontSize = 17.sp), color = textColor)
                                    Text("Set up your local profile", style = TextStyle(fontWeight = FontWeight.Medium, fontSize = 12.sp), color = textColor.copy(alpha = 0.6f))
                                }
                                Icon(Icons.Rounded.ChevronRight, contentDescription = null, tint = textColor.copy(alpha = 0.5f))
                            }
                        }

                        Spacer(modifier = Modifier.height(16.dp))

                        // کادر طلایی پریمیوم
                        Card(
                            modifier = Modifier.fillMaxWidth(),
                            shape = RoundedCornerShape(20.dp),
                            colors = CardDefaults.cardColors(containerColor = Color.Transparent),
                            border = BorderStroke(1.5.dp, Color(0xFFFFD700).copy(alpha = 0.6f))
                        ) {
                            Column(modifier = Modifier.fillMaxWidth().clickable { expandedSection = if (expandedSection == "premium") null else "premium" }.padding(12.dp)) {
                                Row(verticalAlignment = Alignment.CenterVertically) {
                                    Box(modifier = Modifier.size(44.dp).clip(CircleShape).background(Color(0xFFFFD700).copy(alpha = 0.1f)), contentAlignment = Alignment.Center) {
                                        Icon(Icons.Rounded.Star, contentDescription = null, tint = Color(0xFFFFD700))
                                    }
                                    Spacer(modifier = Modifier.width(16.dp))
                                    Column {
                                        Text("Musick Premium", style = TextStyle(fontWeight = FontWeight.Bold, fontSize = 16.sp), color = textColor)
                                        Text("Exclusive features", style = TextStyle(fontWeight = FontWeight.Medium, fontSize = 12.sp), color = textColor.copy(alpha = 0.5f))
                                    }
                                }
                                AnimatedVisibility(visible = expandedSection == "premium") {
                                    Text("Upgrade your experience with ultra-high audio quality and premium layouts.", 
                                         style = TextStyle(fontSize = 13.sp, lineHeight = 20.sp), color = textColor.copy(alpha = 0.7f), 
                                         modifier = Modifier.padding(top = 12.dp, start = 8.dp, end = 8.dp))
                                }
                            }
                        }

                        Spacer(modifier = Modifier.height(8.dp))

                        // کادر خنثی ترجمه (دارای لوگوی اختصاصی طراحی شده)
                        Card(
                            modifier = Modifier.fillMaxWidth(),
                            shape = RoundedCornerShape(20.dp),
                            colors = CardDefaults.cardColors(containerColor = Color.Transparent),
                            border = BorderStroke(1.dp, textColor.copy(alpha = 0.2f))
                        ) {
                            Column(modifier = Modifier.fillMaxWidth().clickable { expandedSection = if (expandedSection == "ai") null else "ai" }.padding(12.dp)) {
                                Row(verticalAlignment = Alignment.CenterVertically) {
                                    Box(modifier = Modifier.size(44.dp).clip(CircleShape).background(textColor.copy(alpha = 0.05f)), contentAlignment = Alignment.Center) {
                                        Icon(imageVector = ImageVector.vectorResource(R.drawable.ic_translate_custom), contentDescription = null, tint = textColor, modifier = Modifier.size(24.dp))
                                    }
                                    Spacer(modifier = Modifier.width(16.dp))
                                    Column {
                                        Text("AI Translation", style = TextStyle(fontWeight = FontWeight.Bold, fontSize = 16.sp), color = textColor)
                                        Text("Translate lyrics instantly", style = TextStyle(fontWeight = FontWeight.Medium, fontSize = 12.sp), color = textColor.copy(alpha = 0.5f))
                                    }
                                }
                                AnimatedVisibility(visible = expandedSection == "ai") {
                                    Column(modifier = Modifier.fillMaxWidth().padding(top = 12.dp, start = 8.dp, end = 8.dp)) {
                                        Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween, verticalAlignment = Alignment.CenterVertically) {
                                            Text("Enable Smart Lyrics", style = TextStyle(fontWeight = FontWeight.Medium, fontSize = 14.sp), color = textColor.copy(alpha = 0.8f))
                                            Switch(
                                                checked = aiTranslationEnabled, 
                                                onCheckedChange = { 
                                                    if (apiToken.isBlank()) {
                                                        Toast.makeText(context, "Please enter your API token first", Toast.LENGTH_SHORT).show()
                                                    } else {
                                                        aiTranslationEnabled = it 
                                                    }
                                                }
                                            )
                                        }
                                        Spacer(modifier = Modifier.height(12.dp))
                                        OutlinedTextField(
                                            value = apiToken,
                                            onValueChange = { apiToken = it },
                                            label = { Text("API Token") },
                                            placeholder = { Text("Enter token here") },
                                            modifier = Modifier.fillMaxWidth(),
                                            singleLine = true,
                                            shape = RoundedCornerShape(12.dp)
                                        )
                                    }
                                }
                            }
                        }

                        Spacer(modifier = Modifier.height(8.dp))

                        // کادر خنثی تنظیمات
                        Card(
                            modifier = Modifier.fillMaxWidth(),
                            shape = RoundedCornerShape(20.dp),
                            colors = CardDefaults.cardColors(containerColor = Color.Transparent),
                            border = BorderStroke(1.dp, textColor.copy(alpha = 0.2f))
                        ) {
                            Row(
                                modifier = Modifier.fillMaxWidth().clickable { showProfileOverlay = false; onSettingsClick() }.padding(12.dp),
                                verticalAlignment = Alignment.CenterVertically
                            ) {
                                Box(modifier = Modifier.size(44.dp).clip(CircleShape).background(textColor.copy(alpha = 0.05f)), contentAlignment = Alignment.Center) {
                                    Icon(Icons.Rounded.Settings, contentDescription = null, tint = textColor)
                                }
                                Spacer(modifier = Modifier.width(16.dp))
                                Text("Settings", style = TextStyle(fontWeight = FontWeight.Bold, fontSize = 16.sp), color = textColor)
                            }
                        }
                    }
                }
            }
        }
    }
}
"""
with open(fp_home, "w") as f: f.write(code_home)

print("Scale-animated Glass Dialog with custom borders applied perfectly!")
