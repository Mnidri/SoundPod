import os

# ۱. اصلاح کامل و کلاسیک صفحه آلبوم (حذف بلر مزاحم و استفاده از رنگ‌های ۱۰۰٪ داینامیک سیستم)
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
                modifier = Modifier.fillMaxWidth().padding(top = 16.dp, bottom = 32.dp),
                horizontalAlignment = Alignment.CenterHorizontally
            ) {
                AsyncImage(
                    model = highResCover, 
                    contentDescription = null, 
                    modifier = Modifier.fillMaxWidth(0.6f).aspectRatio(1f).shadow(24.dp, RoundedCornerShape(20.dp)).clip(RoundedCornerShape(20.dp)),
                    contentScale = ContentScale.Crop
                )
                
                Spacer(modifier = Modifier.height(28.dp))
                
                Text(
                    text = album?.title.orEmpty(),
                    style = typography.titleLarge.copy(fontWeight = FontWeight.ExtraBold, fontSize = 24.sp),
                    color = colorPalette.text,
                    textAlign = TextAlign.Center,
                    maxLines = 2,
                    overflow = TextOverflow.Ellipsis,
                    modifier = Modifier.fillMaxWidth(0.85f)
                )
                
                Spacer(modifier = Modifier.height(12.dp))
                
                Box(
                    modifier = Modifier
                        .clip(RoundedCornerShape(12.dp))
                        .background(colorPalette.text.copy(alpha = 0.05f))
                        .clickable(enabled = album?.artistId != null) { album?.artistId?.let { onGoToArtist(it) } }
                        .padding(horizontal = 16.dp, vertical = 8.dp)
                ) {
                    Text(
                        text = album?.authorsText.orEmpty(),
                        style = typography.titleMedium.copy(fontWeight = FontWeight.Bold),
                        color = colorPalette.accent,
                        textAlign = TextAlign.Center,
                        maxLines = 1,
                        overflow = TextOverflow.Ellipsis
                    )
                }
                
                album?.year?.let {
                    Spacer(modifier = Modifier.height(8.dp))
                    Text(
                        text = "Released • " + it,
                        style = typography.bodyMedium.copy(fontWeight = FontWeight.Medium),
                        color = colorPalette.text.copy(alpha = 0.6f),
                        textAlign = TextAlign.Center
                    )
                }
                
                Spacer(modifier = Modifier.height(28.dp))
                
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


# ۲. جایگزینی دیالوگ شیشه‌ای و هوشمند پروفایل در صفحه اصلی
fp_home = "app/src/main/kotlin/com/github/soundpod/ui/screens/home/HomeScreen.kt"
if not os.path.exists(fp_home): fp_home = "app/src/main/kotlin/com/github/musick/ui/screens/home/HomeScreen.kt"

code_home = """@file:OptIn(androidx.compose.foundation.ExperimentalFoundationApi::class, androidx.compose.animation.ExperimentalAnimationApi::class, androidx.compose.material3.ExperimentalMaterial3Api::class)
package com.github.musick.ui.screens.home

import android.widget.Toast
import androidx.compose.animation.AnimatedVisibility
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
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.TextStyle
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.compose.ui.window.Dialog
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
    val context = LocalContext.current
    
    var showProfileDialog by remember { mutableStateOf(false) }
    var expandedSection by remember { mutableStateOf<String?>(null) }
    var aiTranslationEnabled by remember { mutableStateOf(true) }

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
                    OutlinedIconButton(onClick = { showProfileDialog = true }, border = BorderStroke(1.dp, textColor.copy(alpha = 0.15f))) {
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
        
        if (showProfileDialog) {
            Dialog(onDismissRequest = { showProfileDialog = false }) {
                Card(
                    shape = RoundedCornerShape(24.dp),
                    colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surface.copy(alpha = 0.95f)),
                    elevation = CardDefaults.cardElevation(defaultElevation = 8.dp),
                    modifier = Modifier.fillMaxWidth().padding(vertical = 16.dp)
                ) {
                    Column(
                        modifier = Modifier.fillMaxWidth().padding(20.dp),
                        horizontalAlignment = Alignment.CenterHorizontally
                    ) {
                        // هدر لاگین
                        Row(
                            modifier = Modifier
                                .fillMaxWidth()
                                .clip(RoundedCornerShape(16.dp))
                                .background(MaterialTheme.colorScheme.primary.copy(alpha = 0.12f))
                                .clickable { 
                                    showProfileDialog = false
                                    Toast.makeText(context, "Navigating to Login...", Toast.LENGTH_SHORT).show()
                                }
                                .padding(16.dp),
                            verticalAlignment = Alignment.CenterVertically
                        ) {
                            Box(
                                modifier = Modifier.size(52.dp).clip(CircleShape).background(MaterialTheme.colorScheme.primary.copy(alpha = 0.2f)),
                                contentAlignment = Alignment.Center
                            ) {
                                Icon(Icons.Rounded.AccountCircle, contentDescription = null, modifier = Modifier.size(32.dp), tint = MaterialTheme.colorScheme.primary)
                            }
                            Spacer(modifier = Modifier.width(16.dp))
                            Column(modifier = Modifier.weight(1f)) {
                                Text("Sign in to Musick", style = TextStyle(fontWeight = FontWeight.Bold, fontSize = 17.sp), color = textColor)
                                Text("Sync all your data", style = TextStyle(fontWeight = FontWeight.Medium, fontSize = 12.sp), color = textColor.copy(alpha = 0.6f))
                            }
                            Icon(Icons.Rounded.ChevronRight, contentDescription = null, tint = textColor.copy(alpha = 0.5f))
                        }

                        Spacer(modifier = Modifier.height(24.dp))

                        // گزینه Premium با محتوای بازشونده
                        Column(modifier = Modifier.fillMaxWidth().clip(RoundedCornerShape(16.dp)).clickable { expandedSection = if (expandedSection == "premium") null else "premium" }.padding(12.dp)) {
                            Row(verticalAlignment = Alignment.CenterVertically) {
                                Box(modifier = Modifier.size(44.dp).clip(CircleShape).background(textColor.copy(alpha = 0.06f)), contentAlignment = Alignment.Center) {
                                    Icon(Icons.Rounded.Star, contentDescription = null, tint = Color(0xFFFFD700))
                                }
                                Spacer(modifier = Modifier.width(16.dp))
                                Column {
                                    Text("Musick Premium", style = TextStyle(fontWeight = FontWeight.Bold, fontSize = 16.sp), color = textColor)
                                    Text("Exclusive features", style = TextStyle(fontWeight = FontWeight.Medium, fontSize = 12.sp), color = textColor.copy(alpha = 0.5f))
                                }
                            }
                            AnimatedVisibility(visible = expandedSection == "premium") {
                                Text("Experience ad-free listening, ultra-high audio quality, and early access to new features. Upgrade coming soon!", 
                                     style = TextStyle(fontSize = 13.sp, lineHeight = 20.sp), color = textColor.copy(alpha = 0.7f), 
                                     modifier = Modifier.padding(top = 12.dp, start = 8.dp, end = 8.dp))
                            }
                        }

                        // گزینه AI Translation با سوییچ داخلی
                        Column(modifier = Modifier.fillMaxWidth().clip(RoundedCornerShape(16.dp)).clickable { expandedSection = if (expandedSection == "ai") null else "ai" }.padding(12.dp)) {
                            Row(verticalAlignment = Alignment.CenterVertically) {
                                Box(modifier = Modifier.size(44.dp).clip(CircleShape).background(textColor.copy(alpha = 0.06f)), contentAlignment = Alignment.Center) {
                                    Icon(Icons.Rounded.Translate, contentDescription = null, tint = textColor)
                                }
                                Spacer(modifier = Modifier.width(16.dp))
                                Column {
                                    Text("AI Translation", style = TextStyle(fontWeight = FontWeight.Bold, fontSize = 16.sp), color = textColor)
                                    Text("Translate lyrics instantly", style = TextStyle(fontWeight = FontWeight.Medium, fontSize = 12.sp), color = textColor.copy(alpha = 0.5f))
                                }
                            }
                            AnimatedVisibility(visible = expandedSection == "ai") {
                                Row(modifier = Modifier.fillMaxWidth().padding(top = 12.dp, start = 8.dp, end = 8.dp), horizontalArrangement = Arrangement.SpaceBetween, verticalAlignment = Alignment.CenterVertically) {
                                    Text("Enable Smart Lyrics", style = TextStyle(fontWeight = FontWeight.Medium, fontSize = 14.sp), color = textColor.copy(alpha = 0.8f))
                                    Switch(checked = aiTranslationEnabled, onCheckedChange = { aiTranslationEnabled = it })
                                }
                            }
                        }

                        Divider(modifier = Modifier.fillMaxWidth().padding(vertical = 8.dp), color = textColor.copy(alpha = 0.05f))

                        // دکمه تنظیمات (انتقال به صفحه اصلی تنظیمات)
                        Row(
                            modifier = Modifier.fillMaxWidth().clip(RoundedCornerShape(16.dp)).clickable { showProfileDialog = false; onSettingsClick() }.padding(12.dp),
                            verticalAlignment = Alignment.CenterVertically
                        ) {
                            Box(modifier = Modifier.size(44.dp).clip(CircleShape).background(textColor.copy(alpha = 0.06f)), contentAlignment = Alignment.Center) {
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
"""
with open(fp_home, "w") as f: f.write(code_home)

print("Glass Dialog UI and dynamic Album text patches successfully applied!")
