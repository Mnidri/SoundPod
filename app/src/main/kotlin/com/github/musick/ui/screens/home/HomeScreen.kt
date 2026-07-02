@file:OptIn(androidx.compose.foundation.ExperimentalFoundationApi::class, androidx.compose.animation.ExperimentalAnimationApi::class, androidx.compose.material3.ExperimentalMaterial3Api::class)
package com.github.musick.ui.screens.home

import android.widget.Toast
import androidx.compose.animation.*
import androidx.compose.animation.core.tween
import androidx.compose.foundation.*
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.pager.*
import androidx.compose.foundation.shape.*
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.*
import androidx.compose.material.icons.rounded.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.*
import androidx.compose.ui.graphics.luminance
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.TextStyle
import androidx.compose.ui.text.font.*
import androidx.compose.ui.unit.*
import androidx.navigation.NavController
import androidx.lifecycle.viewmodel.compose.viewModel

import com.github.musick.ui.components.*
import com.github.musick.enums.*
import com.github.musick.ui.navigation.*
import com.github.musick.ui.screens.favorites.*
import com.github.musick.ui.screens.auth.*
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
    val aiPrefs = context.getSharedPreferences("ai_settings", android.content.Context.MODE_PRIVATE)
    val isDark = MaterialTheme.colorScheme.background.luminance() < 0.5f

    var showProfileOverlay by remember { mutableStateOf(false) }
    var showAuthScreen by remember { mutableStateOf(false) }
    var expandedSection by remember { mutableStateOf<String?>(null) }
    var showAiLoginPrompt by remember { mutableStateOf(false) }
    var aiTranslationEnabled by remember { mutableStateOf(false) }
    var apiToken by remember { mutableStateOf(aiPrefs.getString("api_key", "") ?: "") }

    AnimatedContent(targetState = showAuthScreen, transitionSpec = { fadeIn() with fadeOut() }) { isAuth ->
        if (isAuth) {
            AuthScreen(onBack = { showAuthScreen = false })
        } else {
            Box(modifier = Modifier.fillMaxSize()) {
                Scaffold(
                    containerColor = bgColor,
                    topBar = {
                        TopAppBar(
                            title = {
                                Text(
                                    text = "Musick",
                                    fontSize = 72.sp,
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
                    Column(modifier = Modifier.fillMaxSize().padding(paddingValues)) {
                        HorizontalTabs(pagerState = pagerState, tabs = homeViewModel.tabs)
                        HorizontalPager(state = pagerState, beyondViewportPageCount = 4, modifier = Modifier.weight(1f)) { page ->
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

                AnimatedVisibility(
                    visible = showProfileOverlay,
                    enter = fadeIn(tween(300)) + scaleIn(tween(300), transformOrigin = TransformOrigin(0.9f, 0.05f)),
                    exit = fadeOut(tween(200)) + scaleOut(tween(200), transformOrigin = TransformOrigin(0.9f, 0.05f)),
                    modifier = Modifier.fillMaxSize()
                ) {
                    Box(
                        modifier = Modifier
                            .fillMaxSize()
                            .background(Color.Transparent)
                            .clickable { showProfileOverlay = false },
                        contentAlignment = Alignment.Center
                    ) {
                        val outerGlassColor = if (isDark) Color.Black.copy(alpha = 0.75f) else Color.White.copy(alpha = 0.75f)
                        val outerBorderColor = if (isDark) Color.White.copy(alpha = 0.08f) else Color.Black.copy(alpha = 0.1f)
                        val innerGlassColor = if (isDark) Color.Black.copy(alpha = 0.90f) else Color.White.copy(alpha = 0.90f)
                        val innerTextColor = if (isDark) Color.White else Color.Black
                        val innerBorderColor = if (isDark) Color.White.copy(alpha = 0.12f) else Color.Black.copy(alpha = 0.08f)
                        val iconBgColor = if (isDark) Color.White.copy(alpha = 0.1f) else Color.Black.copy(alpha = 0.05f)
                        val shadowElev = if (isDark) 0.dp else 16.dp

                        Card(
                            shape = RoundedCornerShape(32.dp),
                            colors = CardDefaults.cardColors(containerColor = outerGlassColor),
                            border = BorderStroke(1.dp, outerBorderColor),
                            elevation = CardDefaults.cardElevation(defaultElevation = shadowElev),
                            modifier = Modifier.fillMaxWidth(0.92f).clickable(enabled = false) {}
                        ) {
                            Column(
                                modifier = Modifier
                                    .fillMaxWidth()
                                    .padding(horizontal = 24.dp, vertical = 28.dp),
                                horizontalAlignment = Alignment.CenterHorizontally
                            ) {
                                Card(
                                    modifier = Modifier.fillMaxWidth().clickable { showProfileOverlay = false; showAuthScreen = true },
                                    shape = RoundedCornerShape(18.dp),
                                    colors = CardDefaults.cardColors(containerColor = innerGlassColor),
                                    border = BorderStroke(1.5.dp, MaterialTheme.colorScheme.primary.copy(alpha = 0.7f)),
                                    elevation = CardDefaults.cardElevation(defaultElevation = if (isDark) 0.dp else 2.dp)
                                ) {
                                    Row(modifier = Modifier.fillMaxWidth().padding(14.dp), verticalAlignment = Alignment.CenterVertically) {
                                        Box(modifier = Modifier.size(46.dp).clip(CircleShape).background(MaterialTheme.colorScheme.primary.copy(alpha = 0.15f)), contentAlignment = Alignment.Center) {
                                            Icon(Icons.Rounded.AccountCircle, contentDescription = null, modifier = Modifier.size(28.dp), tint = MaterialTheme.colorScheme.primary)
                                        }
                                        Spacer(modifier = Modifier.width(14.dp))
                                        Column(modifier = Modifier.weight(1f)) {
                                            Text(if (com.google.firebase.auth.FirebaseAuth.getInstance().currentUser != null) "Manage Account" else "Log In / Sign Up", style = TextStyle(fontWeight = FontWeight.Bold, fontSize = 16.sp), color = innerTextColor)
                                            Text(if (com.google.firebase.auth.FirebaseAuth.getInstance().currentUser != null) com.google.firebase.auth.FirebaseAuth.getInstance().currentUser?.email ?: "Premium Account Active" else "Log in to unlock AI features", style = TextStyle(fontWeight = FontWeight.Medium, fontSize = 11.sp), color = innerTextColor.copy(alpha = 0.6f))
                                        }
                                        Icon(Icons.Rounded.ChevronRight, contentDescription = null, tint = innerTextColor.copy(alpha = 0.5f))
                                    }
                                }
                                Spacer(modifier = Modifier.height(14.dp))
                                Card(modifier = Modifier.fillMaxWidth(), shape = RoundedCornerShape(18.dp), colors = CardDefaults.cardColors(containerColor = innerGlassColor), border = BorderStroke(1.5.dp, Color(0xFFFFD700).copy(alpha = 0.7f)), elevation = CardDefaults.cardElevation(defaultElevation = if (isDark) 0.dp else 2.dp)) {
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
                                            Text(if (com.google.firebase.auth.FirebaseAuth.getInstance().currentUser != null) "Early-bird Premium is active for your account. Enjoy exclusive features!" else "Log in now to unlock premium features and AI translation for free!", style = TextStyle(fontSize = 13.sp, lineHeight = 18.sp), color = innerTextColor.copy(alpha = 0.8f), modifier = Modifier.padding(top = 10.dp, start = 6.dp, end = 6.dp))
                                        }
                                    }
                                }
                                Spacer(modifier = Modifier.height(14.dp))
                                Card(modifier = Modifier.fillMaxWidth(), shape = RoundedCornerShape(18.dp), colors = CardDefaults.cardColors(containerColor = innerGlassColor), border = BorderStroke(1.dp, innerBorderColor), elevation = CardDefaults.cardElevation(defaultElevation = if (isDark) 0.dp else 2.dp)) {
                                    Column(modifier = Modifier.fillMaxWidth().clickable { 
                                        if (com.google.firebase.auth.FirebaseAuth.getInstance().currentUser == null) {
                                            showAiLoginPrompt = true
                                        } else {
                                            expandedSection = if (expandedSection == "ai") null else "ai" 
                                        }
                                    }.padding(12.dp)) {
                                        Row(verticalAlignment = Alignment.CenterVertically) {
                                            Box(modifier = Modifier.size(42.dp).clip(CircleShape).background(iconBgColor), contentAlignment = Alignment.Center) {
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
                                                    value = apiToken, onValueChange = { apiToken = it; aiPrefs.edit().putString("api_key", it).apply() },
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
                                Card(modifier = Modifier.fillMaxWidth(), shape = RoundedCornerShape(18.dp), colors = CardDefaults.cardColors(containerColor = innerGlassColor), border = BorderStroke(1.dp, innerBorderColor), elevation = CardDefaults.cardElevation(defaultElevation = if (isDark) 0.dp else 2.dp)) {
                                    Row(modifier = Modifier.fillMaxWidth().clickable { showProfileOverlay = false; onSettingsClick() }.padding(14.dp), verticalAlignment = Alignment.CenterVertically) {
                                        Box(modifier = Modifier.size(42.dp).clip(CircleShape).background(iconBgColor), contentAlignment = Alignment.Center) {
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
    }

    if (showAiLoginPrompt) {
        AlertDialog(
            onDismissRequest = { showAiLoginPrompt = false },
            title = { Text("Account Required", fontWeight = FontWeight.Bold) },
            text = { Text("An account is required to use the free AI Lyrics Translation and activate Premium features. Would you like to log in or create an account now?") },
            confirmButton = {
                TextButton(onClick = {
                    showAiLoginPrompt = false
                    showProfileOverlay = false
                    showAuthScreen = true
                }) { Text("Log In / Sign Up", fontWeight = FontWeight.Bold) }
            },
            dismissButton = {
                TextButton(onClick = { showAiLoginPrompt = false }) { Text("Later") }
            }
        )
    }

}