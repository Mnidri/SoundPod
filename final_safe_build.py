import os

def write_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        f.write(content)

# ۱. کدهای کامل و سالم HomeScreen (فقط اصلاح رنگ دیالوگ لایت‌مود)
home_code = """@file:OptIn(androidx.compose.foundation.ExperimentalFoundationApi::class, androidx.compose.animation.ExperimentalAnimationApi::class, androidx.compose.material3.ExperimentalMaterial3Api::class)
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
    val isDark = androidx.compose.foundation.isSystemInDarkTheme()

    var showProfileOverlay by remember { mutableStateOf(false) }
    var showAuthScreen by remember { mutableStateOf(false) }
    var expandedSection by remember { mutableStateOf<String?>(null) }
    var aiTranslationEnabled by remember { mutableStateOf(false) }
    var apiToken by remember { mutableStateOf("") }

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
                        // FIX: رنگ‌بندی دیالوگ لایت مود کاملاً سفید و شیشه‌ای شد
                        val outerGlassColor = if (isDark) Color.Black.copy(alpha = 0.75f) else Color.White.copy(alpha = 0.98f)
                        val outerBorderColor = if (isDark) Color.White.copy(alpha = 0.08f) else Color.Black.copy(alpha = 0.1f)
                        val innerGlassColor = if (isDark) Color.Black.copy(alpha = 0.90f) else Color.White
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
                                            Text("Sign in to Musick", style = TextStyle(fontWeight = FontWeight.Bold, fontSize = 16.sp), color = innerTextColor)
                                            Text("Set up local sync profile", style = TextStyle(fontWeight = FontWeight.Medium, fontSize = 11.sp), color = innerTextColor.copy(alpha = 0.6f))
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
                                            Text("Unlock ad-free streaming, maximum audio bitrate, and elite adaptive designs.", style = TextStyle(fontSize = 13.sp, lineHeight = 18.sp), color = innerTextColor.copy(alpha = 0.8f), modifier = Modifier.padding(top = 10.dp, start = 6.dp, end = 6.dp))
                                        }
                                    }
                                }
                                Spacer(modifier = Modifier.height(14.dp))
                                Card(modifier = Modifier.fillMaxWidth(), shape = RoundedCornerShape(18.dp), colors = CardDefaults.cardColors(containerColor = innerGlassColor), border = BorderStroke(1.dp, innerBorderColor), elevation = CardDefaults.cardElevation(defaultElevation = if (isDark) 0.dp else 2.dp)) {
                                    Column(modifier = Modifier.fillMaxWidth().clickable { expandedSection = if (expandedSection == "ai") null else "ai" }.padding(12.dp)) {
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
}
"""

# ۲. کدهای کامل AuthScreen (حل مشکل فریز و افزودن فاصله از مینی‌پلیر)
auth_code = """package com.github.musick.ui.screens.auth
import android.widget.Toast
import androidx.compose.animation.AnimatedVisibility
import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.rounded.ArrowBack
import androidx.compose.material.icons.rounded.Email
import androidx.compose.material.icons.rounded.ImageSearch
import androidx.compose.material.icons.rounded.Lock
import androidx.compose.material.icons.rounded.Person
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
import androidx.compose.ui.text.input.PasswordVisualTransformation
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun AuthScreen(onBack: () -> Unit) {
    val bgColor = MaterialTheme.colorScheme.background
    val textColor = MaterialTheme.colorScheme.onBackground
    val primaryColor = MaterialTheme.colorScheme.primary
    val context = LocalContext.current
    var isLoginMode by remember { mutableStateOf(true) }
    var username by remember { mutableStateOf("") }
    var email by remember { mutableStateOf("") }
    var password by remember { mutableStateOf("") }

    Scaffold(
        containerColor = bgColor,
        topBar = {
            TopAppBar(
                title = { },
                navigationIcon = {
                    IconButton(onClick = onBack) {
                        Icon(Icons.Rounded.ArrowBack, contentDescription = "Back", tint = textColor)
                    }
                },
                colors = TopAppBarDefaults.topAppBarColors(containerColor = Color.Transparent)
            )
        }
    ) { paddingValues ->
        // FIX: اضافه کردن اسکرول استاندارد بدون ایجاد فریز
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(paddingValues)
                .verticalScroll(rememberScrollState())
                .padding(horizontal = 24.dp),
            horizontalAlignment = Alignment.CenterHorizontally
        ) {
            Spacer(modifier = Modifier.height(20.dp))
            Text(
                text = "Musick",
                fontSize = 48.sp,
                fontWeight = FontWeight.ExtraBold,
                fontFamily = FontFamily.Serif,
                letterSpacing = (-1.5).sp,
                color = textColor,
                style = TextStyle(shadow = androidx.compose.ui.graphics.Shadow(color = textColor.copy(alpha = 0.5f), blurRadius = 24f))
            )
            Spacer(modifier = Modifier.height(32.dp))
            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .height(52.dp)
                    .clip(RoundedCornerShape(50))
                    .background(textColor.copy(alpha = 0.05f))
                    .padding(4.dp),
                verticalAlignment = Alignment.CenterVertically
            ) {
                Box(
                    modifier = Modifier
                        .weight(1f)
                        .fillMaxHeight()
                        .clip(RoundedCornerShape(50))
                        .background(if (isLoginMode) textColor.copy(alpha = 0.1f) else Color.Transparent)
                        .clickable { isLoginMode = true },
                    contentAlignment = Alignment.Center
                ) {
                    Text("Log In", fontWeight = FontWeight.Bold, color = if (isLoginMode) textColor else textColor.copy(alpha = 0.5f))
                }
                Box(
                    modifier = Modifier
                        .weight(1f)
                        .fillMaxHeight()
                        .clip(RoundedCornerShape(50))
                        .background(if (!isLoginMode) textColor.copy(alpha = 0.1f) else Color.Transparent)
                        .clickable { isLoginMode = false },
                    contentAlignment = Alignment.Center
                ) {
                    Text("Sign Up", fontWeight = FontWeight.Bold, color = if (!isLoginMode) textColor else textColor.copy(alpha = 0.5f))
                }
            }
            Spacer(modifier = Modifier.height(32.dp))
            Column(modifier = Modifier.fillMaxWidth(), horizontalAlignment = Alignment.CenterHorizontally) {
                AnimatedVisibility(visible = !isLoginMode) {
                    Column(horizontalAlignment = Alignment.CenterHorizontally) {
                        Box(
                            modifier = Modifier
                                .size(90.dp)
                                .clip(CircleShape)
                                .background(textColor.copy(alpha = 0.05f))
                                .border(1.dp, textColor.copy(alpha = 0.2f), CircleShape)
                                .clickable { Toast.makeText(context, "Gallery opened", Toast.LENGTH_SHORT).show() },
                            contentAlignment = Alignment.Center
                        ) {
                            Icon(Icons.Rounded.ImageSearch, contentDescription = null, tint = textColor.copy(alpha = 0.6f), modifier = Modifier.size(28.dp))
                        }
                        Spacer(modifier = Modifier.height(24.dp))
                    }
                }
                AnimatedVisibility(visible = !isLoginMode) {
                    Column {
                        OutlinedTextField(
                            value = username,
                            onValueChange = { username = it },
                            placeholder = { Text("Username") },
                            leadingIcon = { Icon(Icons.Rounded.Person, contentDescription = null, tint = textColor.copy(alpha = 0.5f)) },
                            modifier = Modifier.fillMaxWidth(),
                            singleLine = true,
                            shape = RoundedCornerShape(16.dp),
                            colors = OutlinedTextFieldDefaults.colors(unfocusedBorderColor = textColor.copy(alpha = 0.1f))
                        )
                        Spacer(modifier = Modifier.height(16.dp))
                    }
                }
                OutlinedTextField(
                    value = email,
                    onValueChange = { email = it },
                    placeholder = { Text("Email Address") },
                    leadingIcon = { Icon(Icons.Rounded.Email, contentDescription = null, tint = textColor.copy(alpha = 0.5f)) },
                    modifier = Modifier.fillMaxWidth(),
                    singleLine = true,
                    shape = RoundedCornerShape(16.dp),
                    colors = OutlinedTextFieldDefaults.colors(unfocusedBorderColor = textColor.copy(alpha = 0.1f))
                )
                Spacer(modifier = Modifier.height(16.dp))
                OutlinedTextField(
                    value = password,
                    onValueChange = { password = it },
                    placeholder = { Text("Password") },
                    leadingIcon = { Icon(Icons.Rounded.Lock, contentDescription = null, tint = textColor.copy(alpha = 0.5f)) },
                    modifier = Modifier.fillMaxWidth(),
                    singleLine = true,
                    visualTransformation = PasswordVisualTransformation(),
                    shape = RoundedCornerShape(16.dp),
                    colors = OutlinedTextFieldDefaults.colors(unfocusedBorderColor = textColor.copy(alpha = 0.1f))
                )
                Spacer(modifier = Modifier.height(32.dp))
                Button(
                    onClick = {
                        Toast.makeText(context, if (isLoginMode) "Logging in..." else "Creating account...", Toast.LENGTH_SHORT).show()
                        onBack()
                    },
                    modifier = Modifier.fillMaxWidth().height(54.dp),
                    shape = RoundedCornerShape(50),
                    colors = ButtonDefaults.buttonColors(containerColor = primaryColor)
                ) {
                    Text(if (isLoginMode) "Log In" else "Create Account", fontWeight = FontWeight.Bold, fontSize = 16.sp)
                }
                Spacer(modifier = Modifier.height(32.dp))
                Row(verticalAlignment = Alignment.CenterVertically, modifier = Modifier.fillMaxWidth()) {
                    HorizontalDivider(modifier = Modifier.weight(1f), color = textColor.copy(alpha = 0.1f))
                    Text(" OR ", color = textColor.copy(alpha = 0.4f), fontSize = 12.sp, modifier = Modifier.padding(horizontal = 16.dp))
                    HorizontalDivider(modifier = Modifier.weight(1f), color = textColor.copy(alpha = 0.1f))
                }
                Spacer(modifier = Modifier.height(32.dp))
                Card(
                    modifier = Modifier.fillMaxWidth().height(54.dp).clickable { Toast.makeText(context, "Google Auth Started", Toast.LENGTH_SHORT).show() },
                    shape = RoundedCornerShape(50),
                    colors = CardDefaults.cardColors(containerColor = Color.Transparent),
                    border = BorderStroke(1.dp, textColor.copy(alpha = 0.2f))
                ) {
                    Row(modifier = Modifier.fillMaxSize(), verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.Center) {
                        Text("G", fontWeight = FontWeight.ExtraBold, fontSize = 20.sp, color = textColor)
                        Spacer(modifier = Modifier.width(12.dp))
                        Text("Continue with Google", fontWeight = FontWeight.Bold, fontSize = 15.sp, color = textColor)
                    }
                }
                // FIX: فضای خالی امن برای جلوگیری از افتادن زیر مینی‌پلیر
                Spacer(modifier = Modifier.height(130.dp))
            }
        }
    }
}
"""

# ۳. کدهای کامل ArtistScreen (اصلاح تب‌ها در لایت‌مود)
artist_code = """package com.github.musick.ui.screens.artist
import androidx.activity.compose.BackHandler
import androidx.compose.animation.ExperimentalAnimationApi
import androidx.compose.foundation.ExperimentalFoundationApi
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.horizontalScroll
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.pager.HorizontalPager
import androidx.compose.foundation.pager.rememberPagerState
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Search
import androidx.compose.material3.DropdownMenuItem
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.MaterialTheme.typography
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.remember
import androidx.compose.runtime.rememberCoroutineScope
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
import androidx.media3.common.util.UnstableApi
import coil3.compose.AsyncImage
import com.github.core.ui.LocalAppearance
import com.github.musick.LocalPlayerPadding
import com.github.musick.R
import com.github.musick.ui.components.PlaylistScreenLayout
import com.github.musick.viewmodels.ArtistViewModel
import kotlinx.coroutines.launch

enum class ArtistTab { Overview, Songs, Albums, Singles }

fun extractHighResUrl(rawThumb: String?): String {
    if (rawThumb == null) return ""
    var extracted = if (rawThumb.contains("url=")) Regex("url=([^,)]+)").find(rawThumb)?.groupValues?.get(1) ?: rawThumb else rawThumb
    extracted = if (extracted.startsWith("//")) "https:$extracted" else extracted
    return extracted.replace(Regex("=w\\d+-h\\d+"), "=w1080-h1080").replace(Regex("=s\\d+"), "=s1080")
}

@OptIn(ExperimentalAnimationApi::class, ExperimentalFoundationApi::class)
@UnstableApi
@Composable
fun ArtistScreen(
    browseId: String,
    onBack: () -> Unit,
    onSearchClick: () -> Unit,
    onSettingsClick: () -> Unit,
    onAlbumClick: (String) -> Unit,
    onArtistClick: (String) -> Unit,
    viewModel: ArtistViewModel = viewModel(),
) {
    val playerPadding = LocalPlayerPadding.current
    val (colorPalette) = LocalAppearance.current
    val artist = viewModel.artist
    val artistPage = viewModel.artistPage
    BackHandler { onBack() }
    LaunchedEffect(browseId) { viewModel.loadArtist(browseId, 0) }
    val tabs = remember(artistPage) {
        listOfNotNull(
            ArtistTab.Overview to R.string.overview,
            if (artistPage?.songs != null || artistPage?.songsEndpoint != null) ArtistTab.Songs to R.string.tracks else null,
            if (artistPage?.albums != null || artistPage?.albumsEndpoint != null) ArtistTab.Albums to R.string.albums else null,
            if (artistPage?.singles != null || artistPage?.singlesEndpoint != null) ArtistTab.Singles to R.string.singles else null
        )
    }
    val pagerState = rememberPagerState { tabs.size }
    val coroutineScope = rememberCoroutineScope()
    val highResCover = extractHighResUrl(artist?.thumbnailUrl)

    PlaylistScreenLayout(
        title = { },
        onBackClick = onBack,
        actions = {
            IconButton(onClick = { viewModel.toggleBookmark() }) {
                Icon(
                    imageVector = ImageVector.vectorResource(if (artist?.bookmarkedAt != null) R.drawable.heart else R.drawable.heart_outline),
                    contentDescription = null, tint = if (androidx.compose.foundation.isSystemInDarkTheme()) Color.White else Color.Black, modifier = Modifier.size(26.dp)
                )
            }
            IconButton(onClick = onSearchClick) {
                Icon(imageVector = Icons.Default.Search, contentDescription = null, tint = if (androidx.compose.foundation.isSystemInDarkTheme()) Color.White else Color.Black, modifier = Modifier.size(28.dp))
            }
        },
        dropDownMenuContent = { dismissMenu ->
            DropdownMenuItem(text = { Text(stringResource(id = R.string.settings), color = colorPalette.text) }, onClick = { onSettingsClick(); dismissMenu() })
        },
        headerContent = {
            Box(modifier = Modifier.fillMaxWidth().height(360.dp)) {
                AsyncImage(model = highResCover, contentDescription = null, modifier = Modifier.fillMaxSize().blur(60.dp), contentScale = ContentScale.Crop)
                Box(modifier = Modifier.fillMaxSize().background(Brush.verticalGradient(listOf(Color.Black.copy(alpha = 0.2f), if (androidx.compose.foundation.isSystemInDarkTheme()) Color.Black else Color.Black.copy(alpha = 0.06f)))))
                Column(
                    modifier = Modifier.fillMaxSize().padding(bottom = 24.dp),
                    horizontalAlignment = Alignment.CenterHorizontally,
                    verticalArrangement = Arrangement.Bottom
                ) {
                    AsyncImage(
                        model = highResCover,
                        contentDescription = null,
                        modifier = Modifier.size(170.dp).shadow(24.dp, CircleShape).clip(CircleShape).border(3.dp, Color.White.copy(alpha = 0.3f), CircleShape),
                        contentScale = ContentScale.Crop
                    )
                    Spacer(modifier = Modifier.height(16.dp))
                    Text(text = artist?.name.orEmpty(), style = typography.headlineLarge.copy(fontWeight = FontWeight.Black, fontSize = 34.sp), color = if (androidx.compose.foundation.isSystemInDarkTheme()) Color.White else Color.Black, maxLines = 1, overflow = TextOverflow.Ellipsis)
                    Text(text = "Verified Artist", style = typography.labelLarge.copy(fontWeight = FontWeight.Medium, letterSpacing = 2.sp), color = Color.White.copy(alpha = 0.6f), modifier = Modifier.padding(top = 4.dp))
                }
            }
        },
        footerHeaderContent = {
            if (tabs.isNotEmpty()) {
                Row(
                    modifier = Modifier.fillMaxWidth().horizontalScroll(rememberScrollState()).padding(vertical = 12.dp, horizontal = 16.dp),
                    horizontalArrangement = Arrangement.spacedBy(12.dp, Alignment.CenterHorizontally)
                ) {
                    tabs.forEachIndexed { index, (_, titleRes) ->
                        val selected = pagerState.currentPage == index
                        val isDark = androidx.compose.foundation.isSystemInDarkTheme()
                        
                        // FIX: رنگ‌بندی تب‌ها برای خوانایی عالی در لایت‌مود و دارک‌مود
                        val tabBg = if (selected) {
                            if (isDark) Color.White else Color.Black
                        } else {
                            if (isDark) Color.White.copy(alpha = 0.1f) else Color.Black.copy(alpha = 0.05f)
                        }
                        val tabTextColor = if (selected) {
                            if (isDark) Color.Black else Color.White
                        } else {
                            if (isDark) Color.White else Color.Black.copy(alpha = 0.7f)
                        }

                        Box(
                            modifier = Modifier
                                .clip(RoundedCornerShape(50))
                                .background(tabBg)
                                .clickable { coroutineScope.launch { pagerState.animateScrollToPage(index) } }
                                .padding(horizontal = 20.dp, vertical = 10.dp)
                        ) {
                            Text(text = stringResource(titleRes), style = typography.titleSmall.copy(fontWeight = FontWeight.Bold), color = tabTextColor)
                        }
                    }
                }
            }
        },
        content = {
            if (tabs.isNotEmpty()) {
                HorizontalPager(state = pagerState, modifier = Modifier.fillMaxSize().padding(bottom = playerPadding), verticalAlignment = Alignment.Top) { pageIndex ->
                    val tab = tabs[pageIndex].first
                    when (tab) {
                        ArtistTab.Overview -> ArtistOverviewContent(youtubeArtistPage = artistPage, onAlbumClick = onAlbumClick, playerPadding = playerPadding)
                        ArtistTab.Songs -> ArtistTracksPage(browseId = artistPage?.songsEndpoint?.browseId ?: browseId, params = artistPage?.songsEndpoint?.params, onAlbumClick = onAlbumClick, onArtistClick = onArtistClick, initialItems = if (artistPage?.songsEndpoint == null) artistPage?.songs else null)
                        ArtistTab.Albums -> ArtistAlbumsPage(browseId = artistPage?.albumsEndpoint?.browseId ?: browseId, params = artistPage?.albumsEndpoint?.params, onAlbumClick = onAlbumClick, initialItems = if (artistPage?.albumsEndpoint == null) artistPage?.albums else null)
                        ArtistTab.Singles -> ArtistAlbumsPage(browseId = artistPage?.singlesEndpoint?.browseId ?: browseId, params = artistPage?.singlesEndpoint?.params, onAlbumClick = onAlbumClick, initialItems = if (artistPage?.singlesEndpoint == null) artistPage?.singles else null)
                    }
                }
            }
        }
    )
}
"""

write_file("app/src/main/kotlin/com/github/soundpod/ui/screens/home/HomeScreen.kt", home_code)
write_file("app/src/main/kotlin/com/github/soundpod/ui/screens/auth/AuthScreen.kt", auth_code)
write_file("app/src/main/kotlin/com/github/soundpod/ui/screens/artist/ArtistScreen.kt", artist_code)

print("Files successfully generated with safe implementations.")
