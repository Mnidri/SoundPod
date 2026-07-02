import os

# ۱. جراحی صفحه اصلی: اضافه کردن پاپ‌آپ شیشه‌ای پروفایل و دکمه‌های انتقال یافته
fp_home = "app/src/main/kotlin/com/github/soundpod/ui/screens/home/HomeScreen.kt"
if not os.path.exists(fp_home): fp_home = "app/src/main/kotlin/com/github/musick/ui/screens/home/HomeScreen.kt"

code_home = """@file:OptIn(androidx.compose.foundation.ExperimentalFoundationApi::class, androidx.compose.animation.ExperimentalAnimationApi::class, androidx.compose.material3.ExperimentalMaterial3Api::class)
package com.github.musick.ui.screens.home

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
import androidx.compose.material.icons.rounded.Translate
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.TextStyle
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.navigation.NavController
import androidx.lifecycle.viewmodel.compose.viewModel
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
    
    // وضعیت باز و بسته بودن پاپ‌آپ پروفایل
    var showProfileSheet by remember { mutableStateOf(false) }
    val sheetState = rememberModalBottomSheetState(skipPartiallyExpanded = true)

    Scaffold(
        containerColor = bgColor,
        topBar = {
            TopAppBar(
                title = {
                    Text(
                        text = "Musick",
                        fontSize = 36.sp,
                        fontWeight = FontWeight.Bold,
                        fontFamily = FontFamily.Serif,
                        letterSpacing = (-1).sp,
                        color = textColor,
                        style = TextStyle(shadow = androidx.compose.ui.graphics.Shadow(color = textColor.copy(alpha = 0.5f), blurRadius = 24f))
                    )
                },
                actions = {
                    IconButton(onClick = { navController.navigate(route = Routes.Search) }) {
                        Icon(imageVector = Icons.Default.Search, contentDescription = "Search", tint = textColor)
                    }
                    Spacer(modifier = Modifier.width(4.dp))
                    // جایگزینی دکمه تنظیمات با دکمه آدمک (پروفایل)
                    OutlinedIconButton(onClick = { showProfileSheet = true }, border = BorderStroke(1.dp, textColor.copy(alpha = 0.15f))) {
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
        
        // پیاده‌سازی پاپ‌آپ مدرن و شیشه‌ای پروفایل
        if (showProfileSheet) {
            ModalBottomSheet(
                onDismissRequest = { showProfileSheet = false },
                sheetState = sheetState,
                containerColor = MaterialTheme.colorScheme.surface,
                scrimColor = Color.Black.copy(alpha = 0.6f),
                shape = RoundedCornerShape(topStart = 32.dp, topEnd = 32.dp)
            ) {
                Column(
                    modifier = Modifier.fillMaxWidth().padding(horizontal = 24.dp, vertical = 16.dp),
                    horizontalAlignment = Alignment.CenterHorizontally
                ) {
                    // بنر لوکس ورود و ساخت حساب
                    Row(
                        modifier = Modifier
                            .fillMaxWidth()
                            .clip(RoundedCornerShape(20.dp))
                            .background(MaterialTheme.colorScheme.primary.copy(alpha = 0.1f))
                            .clickable { /* در آینده به صفحه لاگین متصل می‌شود */ }
                            .padding(20.dp),
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        Box(
                            modifier = Modifier.size(56.dp).clip(CircleShape).background(MaterialTheme.colorScheme.primary.copy(alpha = 0.2f)),
                            contentAlignment = Alignment.Center
                        ) {
                            Icon(Icons.Rounded.AccountCircle, contentDescription = null, modifier = Modifier.size(32.dp), tint = MaterialTheme.colorScheme.primary)
                        }
                        Spacer(modifier = Modifier.width(16.dp))
                        Column(modifier = Modifier.weight(1f)) {
                            Text("Sign in to Musick", style = TextStyle(fontWeight = FontWeight.Bold, fontSize = 18.sp), color = textColor)
                            Text("Sync playlists & favorites", style = TextStyle(fontWeight = FontWeight.Medium, fontSize = 13.sp), color = textColor.copy(alpha = 0.6f))
                        }
                        Icon(Icons.Rounded.ChevronRight, contentDescription = null, tint = textColor.copy(alpha = 0.5f))
                    }

                    Spacer(modifier = Modifier.height(28.dp))

                    // لیست امکانات ویژه و تنظیمات
                    val menuItems = listOf(
                        Triple(Icons.Rounded.Star, "Musick Premium", "Exclusive features"),
                        Triple(Icons.Rounded.Translate, "AI Translation", "Translate lyrics instantly"),
                        Triple(Icons.Rounded.Settings, "Settings", "App preferences")
                    )

                    menuItems.forEach { (icon, title, subtitle) ->
                        Row(
                            modifier = Modifier
                                .fillMaxWidth()
                                .clip(RoundedCornerShape(16.dp))
                                .clickable {
                                    showProfileSheet = false
                                    // فعلاً هر سه به تنظیمات می‌روند تا بعداً صفحاتشان جدا شود
                                    if (title == "Settings") onSettingsClick() else onSettingsClick() 
                                }
                                .padding(horizontal = 16.dp, vertical = 16.dp),
                            verticalAlignment = Alignment.CenterVertically
                        ) {
                            Box(
                                modifier = Modifier.size(48.dp).clip(CircleShape).background(textColor.copy(alpha = 0.05f)),
                                contentAlignment = Alignment.Center
                            ) {
                                Icon(icon, contentDescription = null, modifier = Modifier.size(24.dp), tint = if (title == "Musick Premium") Color(0xFFFFD700) else textColor)
                            }
                            Spacer(modifier = Modifier.width(16.dp))
                            Column(modifier = Modifier.weight(1f)) {
                                Text(title, style = TextStyle(fontWeight = FontWeight.Bold, fontSize = 16.sp), color = textColor)
                                Text(subtitle, style = TextStyle(fontWeight = FontWeight.Medium, fontSize = 12.sp), color = textColor.copy(alpha = 0.5f))
                            }
                        }
                    }
                    Spacer(modifier = Modifier.height(32.dp))
                }
            }
        }
    }
}
"""
with open(fp_home, "w") as f: f.write(code_home)


# ۲. حل معمای غیب شدن متن‌ها در صفحه آلبوم (قفل کردن رنگ‌ها روی سفید مطلق)
fp_album = "app/src/main/kotlin/com/github/soundpod/ui/screens/album/AlbumScreen.kt"
if not os.path.exists(fp_album): fp_album = "app/src/main/kotlin/com/github/musick/ui/screens/album/AlbumScreen.kt"

if os.path.exists(fp_album):
    with open(fp_album, "r") as f: code_album = f.read()
    
    # جایگزینی colorPalette.text و colorPalette.accent با Color.White در بخش Header
    start_idx = code_album.find("headerContent = {")
    end_idx = code_album.find("content = {", start_idx)
    
    if start_idx != -1 and end_idx != -1:
        header_block = code_album[start_idx:end_idx]
        
        # قفل کردن رنگ‌ها برای جلوگیری از استتار متن روی پس‌زمینه تیره
        header_block = header_block.replace("colorPalette.text", "Color.White")
        header_block = header_block.replace("colorPalette.accent", "Color.White")
        
        new_album_code = code_album[:start_idx] + header_block + code_album[end_idx:]
        with open(fp_album, "w") as f: f.write(new_album_code)

print("Glassmorphic Profile Sheet added and Album text visibility locked to White!")
