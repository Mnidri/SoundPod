import os

# ۱. جایگذاری کدهای HomeScreen (دیالوگ دو لایه، بک‌گراند بلر، کادرهای رنگی و انیمیشن از جایگاه آدمک)
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
                            color = textColor,
                            style = TextStyle(shadow = androidx.compose.ui.graphics.Shadow(color = textColor.copy(alpha = 0.4f), blurRadius = 20f))
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
        
        // سیستم دو لایه واقعی: لایه اول تاریکی ملایم پشت، لایه دوم باکس شیشه‌ای شناور در مرکز
        if (showProfileOverlay) {
            Dialog(onDismissRequest = { showProfileOverlay = false }) {
                AnimatedVisibility(
                    visible = showProfileOverlay,
                    enter = fadeIn(tween(300)) + scaleIn(tween(300), transformOrigin = TransformOrigin(0.85f, 0.1f)),
                    exit = fadeOut(tween(200)) + scaleOut(tween(200), transformOrigin = TransformOrigin(0.85f, 0.1f))
                ) {
                    Card(
                        shape = RoundedCornerShape(28.dp),
                        // پس‌زمینه کاملاً شیشه‌ای، نیمه‌شفاف و لایت متناسب با تم سیستم برای لایه دوم
                        colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surface.copy(alpha = 0.75f)),
                        border = BorderStroke(1.dp, textColor.copy(alpha = 0.15f)),
                        modifier = Modifier.fillMaxWidth().wrapContentHeight()
                    ) {
                        Column(
                            modifier = Modifier.fillMaxWidth().padding(20.dp),
                            horizontalAlignment = Alignment.CenterHorizontally
                        ) {
                            // گزینه اول: کادر حساب کاربری با رنگ برند
                            Card(
                                modifier = Modifier.fillMaxWidth(),
                                shape = RoundedCornerShape(18.dp),
                                colors = CardDefaults.cardColors(containerColor = textColor.copy(alpha = 0.03f)),
                                border = BorderStroke(1.5.dp, MaterialTheme.colorScheme.primary.copy(alpha = 0.7f))
                            ) {
                                Row(
                                    modifier = Modifier
                                        .fillMaxWidth()
                                        .clickable { 
                                            showProfileOverlay = false
                                            Toast.makeText(context, "Navigating to Login Setup...", Toast.LENGTH_SHORT).show()
                                        }
                                        .padding(14.dp),
                                    verticalAlignment = Alignment.CenterVertically
                                ) {
                                    Box(
                                        modifier = Modifier.size(46.dp).clip(CircleShape).background(MaterialTheme.colorScheme.primary.copy(alpha = 0.12f)),
                                        contentAlignment = Alignment.Center
                                    ) {
                                        Icon(Icons.Rounded.AccountCircle, contentDescription = null, modifier = Modifier.size(28.dp), tint = MaterialTheme.colorScheme.primary)
                                    }
                                    Spacer(modifier = Modifier.width(14.dp))
                                    Column(modifier = Modifier.weight(1f)) {
                                        Text("Sign in to Musick", style = TextStyle(fontWeight = FontWeight.Bold, fontSize = 16.sp), color = textColor)
                                        Text("Set up local sync profile", style = TextStyle(fontWeight = FontWeight.Medium, fontSize = 11.sp), color = textColor.copy(alpha = 0.5f))
                                    }
                                    Icon(Icons.Rounded.ChevronRight, contentDescription = null, tint = textColor.copy(alpha = 0.4f))
                                }
                            }

                            Spacer(modifier = Modifier.height(12.dp))

                            // گزینه دوم: کادر طلایی لایت پریمیوم روی لایه شیشه‌ای
                            Card(
                                modifier = Modifier.fillMaxWidth(),
                                shape = RoundedCornerShape(18.dp),
                                colors = CardDefaults.cardColors(containerColor = textColor.copy(alpha = 0.03f)),
                                border = BorderStroke(1.5.dp, Color(0xFFFFD700).copy(alpha = 0.7f))
                            ) {
                                Column(modifier = Modifier.fillMaxWidth().clickable { expandedSection = if (expandedSection == "premium") null else "premium" }.padding(12.dp)) {
                                    Row(verticalAlignment = Alignment.CenterVertically) {
                                        Box(modifier = Modifier.size(42.dp).clip(CircleShape).background(Color(0xFFFFD700).copy(alpha = 0.12f)), contentAlignment = Alignment.Center) {
                                            Icon(Icons.Rounded.Star, contentDescription = null, tint = Color(0xFFFFD700), modifier = Modifier.size(22.dp))
                                        }
                                        Spacer(modifier = Modifier.width(14.dp))
                                        Column {
                                            Text("Musick Premium", style = TextStyle(fontWeight = FontWeight.Bold, fontSize = 15.sp), color = textColor)
                                            Text("Exclusive layouts & quality", style = TextStyle(fontWeight = FontWeight.Medium, fontSize = 11.sp), color = textColor.copy(alpha = 0.5f))
                                        }
                                    }
                                    AnimatedVisibility(visible = expandedSection == "premium") {
                                        Text("Unlock ad-free streaming, maximum audio bitrate, and elite adaptive designs.", 
                                             style = TextStyle(fontSize = 13.sp, lineHeight = 18.sp), color = textColor.copy(alpha = 0.7f), 
                                             modifier = Modifier.padding(top = 10.dp, start = 6.dp, end = 6.dp))
                                    }
                                }
                            }

                            Spacer(modifier = Modifier.height(12.dp))

                            // گزینه سوم: کادر خنثی ترجمه هوشمند
                            Card(
                                modifier = Modifier.fillMaxWidth(),
                                shape = RoundedCornerShape(18.dp),
                                colors = CardDefaults.cardColors(containerColor = textColor.copy(alpha = 0.03f)),
                                border = BorderStroke(1.2.dp, textColor.copy(alpha = 0.2f))
                            ) {
                                Column(modifier = Modifier.fillMaxWidth().clickable { expandedSection = if (expandedSection == "ai") null else "ai" }.padding(12.dp)) {
                                    Row(verticalAlignment = Alignment.CenterVertically) {
                                        Box(modifier = Modifier.size(42.dp).clip(CircleShape).background(textColor.copy(alpha = 0.06f)), contentAlignment = Alignment.Center) {
                                            Icon(Icons.Rounded.Translate, contentDescription = null, tint = textColor, modifier = Modifier.size(22.dp))
                                        }
                                        Spacer(modifier = Modifier.width(14.dp))
                                        Column {
                                            Text("AI Translation", style = TextStyle(fontWeight = FontWeight.Bold, fontSize = 15.sp), color = textColor)
                                            Text("Translate lyrics instantly", style = TextStyle(fontWeight = FontWeight.Medium, fontSize = 11.sp), color = textColor.copy(alpha = 0.5f))
                                        }
                                    }
                                    AnimatedVisibility(visible = expandedSection == "ai") {
                                        Column(modifier = Modifier.fillMaxWidth().padding(top = 10.dp, start = 6.dp, end = 6.dp)) {
                                            Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween, verticalAlignment = Alignment.CenterVertically) {
                                                Text("Enable Smart Lyrics", style = TextStyle(fontWeight = FontWeight.Medium, fontSize = 13.sp), color = textColor.copy(alpha = 0.8f))
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
                                            Spacer(modifier = Modifier.height(8.dp))
                                            OutlinedTextField(
                                                value = apiToken,
                                                onValueChange = { apiToken = it },
                                                label = { Text("API Token", fontSize = 12.sp) },
                                                placeholder = { Text("Enter token key") },
                                                modifier = Modifier.fillMaxWidth(),
                                                singleLine = true,
                                                shape = RoundedCornerShape(10.dp)
                                            )
                                        }
                                    }
                                }
                            }

                            Spacer(modifier = Modifier.height(12.dp))

                            // گزینه چهارم: کادر خنثی تنظیمات عمومی
                            Card(
                                modifier = Modifier.fillMaxWidth(),
                                shape = RoundedCornerShape(18.dp),
                                colors = CardDefaults.cardColors(containerColor = textColor.copy(alpha = 0.03f)),
                                border = BorderStroke(1.2.dp, textColor.copy(alpha = 0.2f))
                            ) {
                                Row(
                                    modifier = Modifier.fillMaxWidth().clickable { showProfileOverlay = false; onSettingsClick() }.padding(14.dp),
                                    verticalAlignment = Alignment.CenterVertically
                                ) {
                                    Box(modifier = Modifier.size(42.dp).clip(CircleShape).background(textColor.copy(alpha = 0.06f)), contentAlignment = Alignment.Center) {
                                        Icon(Icons.Rounded.Settings, contentDescription = null, tint = textColor, modifier = Modifier.size(22.dp))
                                    }
                                    Spacer(modifier = Modifier.width(14.dp))
                                    Text("Settings", style = TextStyle(fontWeight = FontWeight.Bold, fontSize = 15.sp), color = textColor)
                                }
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


# ۲. جایگذاری کدهای AlbumScreen (حل مشکل شیفت شدن و خوانایی متن‌ها)
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
    return extracted.replace(Regex("=w\\d+-h\\d+"), "=w1080-h1080").replace(Regex("=s\\d+"), "=s1080")
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
                modifier = Modifier.fillMaxWidth().padding(top = 12.dp, bottom = 20.dp),
                horizontalAlignment = Alignment.CenterHorizontally
            ) {
                // سایز فیکس و کنترل‌شده تصویر کاور برای جلوگیری از بیرون افتادن متن از صفحه
                AsyncImage(
                    model = highResCover, 
                    contentDescription = null, 
                    modifier = Modifier.size(190.dp).shadow(14.dp, RoundedCornerShape(16.dp)).clip(RoundedCornerShape(16.dp)),
                    contentScale = ContentScale.Crop
                )
                
                Spacer(modifier = Modifier.height(18.dp))
                
                // استفاده قطعی از رنگ تم لایت/دارک سیستم برای خوانایی ۱۰۰ درصد
                Text(
                    text = album?.title.orEmpty(),
                    style = typography.titleLarge.copy(fontWeight = FontWeight.ExtraBold, fontSize = 23.sp),
                    color = colorPalette.text,
                    textAlign = TextAlign.Center,
                    maxLines = 2,
                    overflow = TextOverflow.Ellipsis,
                    modifier = Modifier.fillMaxWidth(0.85f)
                )
                
                Spacer(modifier = Modifier.height(10.dp))
                
                // کپسول خواننده کاملاً تفکیک‌شده و ۱۰۰٪ کلیکی
                Box(
                    modifier = Modifier
                        .clip(RoundedCornerShape(50))
                        .background(colorPalette.text.copy(alpha = 0.06f))
                        .clickable(enabled = album?.artistId != null) { album?.artistId?.let { onGoToArtist(it) } }
                        .padding(horizontal = 16.dp, vertical = 6.dp)
                ) {
                    Text(
                        text = album?.authorsText.orEmpty(),
                        style = typography.titleMedium.copy(fontWeight = FontWeight.Bold, fontSize = 15.sp),
                        color = colorPalette.accent,
                        textAlign = TextAlign.Center,
                        maxLines = 1,
                        overflow = TextOverflow.Ellipsis
                    )
                }
                
                album?.year?.let {
                    Spacer(modifier = Modifier.height(6.dp))
                    Text(
                        text = "Album • " + it,
                        style = typography.bodyMedium.copy(fontWeight = FontWeight.Medium),
                        color = colorPalette.text.copy(alpha = 0.5f),
                        textAlign = TextAlign.Center
                    )
                }
                
                Spacer(modifier = Modifier.height(18.dp))
                
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.Center,
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    Button(
                        onClick = { /* Handle Play */ },
                        colors = ButtonDefaults.buttonColors(containerColor = colorPalette.text, contentColor = colorPalette.background0),
                        shape = RoundedCornerShape(50),
                        modifier = Modifier.height(48.dp).width(135.dp)
                    ) {
                        Icon(Icons.Default.PlayArrow, contentDescription = null, modifier = Modifier.size(22.dp))
                        Spacer(modifier = Modifier.width(6.dp))
                        Text("Play", fontWeight = FontWeight.Bold, fontSize = 15.sp)
                    }
                    Spacer(modifier = Modifier.width(14.dp))
                    IconButton(
                        onClick = { viewModel.toggleLove() },
                        modifier = Modifier.size(48.dp).clip(CircleShape).background(colorPalette.text.copy(alpha = 0.06f))
                    ) {
                        Icon(
                            imageVector = ImageVector.vectorResource(if (uiState.isLoved) R.drawable.heart else R.drawable.heart_outline),
                            contentDescription = null, 
                            tint = if (uiState.isLoved) Color(0xFFFF4B4B) else colorPalette.text, 
                            modifier = Modifier.size(22.dp)
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

print("2-Layer Glass Dialog and Fixed Album text applied successfully via Python!")
