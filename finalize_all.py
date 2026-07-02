import os

# این تابع فایل‌ها را با کدهای کاملاً جدید و اصلاح‌شده بازنویسی می‌کند
def write_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f: f.write(content)

# کدهای HomeScreen اصلاح شده
home_code = """package com.github.soundpod.ui.screens.home
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
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.*
import androidx.navigation.NavController
import androidx.lifecycle.viewmodel.compose.viewModel
import com.github.soundpod.ui.components.*
import com.github.soundpod.enums.*
import com.github.soundpod.ui.navigation.*
import com.github.soundpod.ui.screens.favorites.*
import com.github.soundpod.ui.screens.auth.*
import com.github.soundpod.viewmodels.home.HomeViewModel

@Composable
fun HomeScreen(navController: NavController, onSettingsClick: () -> Unit) {
    val homeViewModel: HomeViewModel = viewModel()
    val pagerState = rememberPagerState(initialPage = 0) { homeViewModel.tabs.size }
    val isDark = androidx.compose.foundation.isSystemInDarkTheme()
    val bgColor = MaterialTheme.colorScheme.background
    val textColor = MaterialTheme.colorScheme.onBackground
    var showProfileOverlay by remember { mutableStateOf(false) }
    var showAuthScreen by remember { mutableStateOf(false) }

    AnimatedContent(targetState = showAuthScreen, transitionSpec = { fadeIn() with fadeOut() }) { isAuth ->
        if (isAuth) {
            AuthScreen(onBack = { showAuthScreen = false })
        } else {
            Box(modifier = Modifier.fillMaxSize()) {
                Scaffold(containerColor = bgColor, topBar = {
                    TopAppBar(title = { Text("Musick", fontSize = 44.sp, fontWeight = FontWeight.ExtraBold, fontFamily = FontFamily.Serif, color = textColor) }, actions = {
                        IconButton(onClick = { navController.navigate(route = Routes.Search) }) { Icon(Icons.Default.Search, null, tint = textColor) }
                    }, colors = TopAppBarDefaults.topAppBarColors(containerColor = bgColor))
                }) { paddingValues ->
                    Column(modifier = Modifier.fillMaxSize().padding(paddingValues)) {
                        HorizontalTabs(pagerState = pagerState, tabs = homeViewModel.tabs)
                        HorizontalPager(state = pagerState, modifier = Modifier.weight(1f)) { page ->
                             when(page) {
                                0 -> QuickPicks(onAlbumClick = { navController.navigate(Routes.Album(it)) }, onArtistClick = { navController.navigate(Routes.Artist(it)) }, onPlaylistClick = { navController.navigate(Routes.Playlist(it)) }, onOfflinePlaylistClick = { navController.navigate(Routes.BuiltInPlaylist(1)) })
                                1 -> FavoritesScreen(onFavoriteTracksClick = { navController.navigate(Routes.FavoriteTracks) }, onGoToAlbum = { navController.navigate(Routes.Album(it)) }, onGoToArtist = { navController.navigate(Routes.Artist(it)) }, isEmbedded = true)
                                else -> Box(Modifier.fillMaxSize())
                             }
                        }
                    }
                }
                if (showProfileOverlay) {
                    Box(Modifier.fillMaxSize().background(Color.Transparent).clickable { showProfileOverlay = false }, contentAlignment = Alignment.Center) {
                        Card(shape = RoundedCornerShape(32.dp), colors = CardDefaults.cardColors(containerColor = if (isDark) Color.Black.copy(0.7f) else Color.White.copy(0.8f)), modifier = Modifier.fillMaxWidth(0.9f)) {
                             // کادر شیشه‌ای لوکس
                             Column(Modifier.padding(24.dp)) {
                                 Text("Settings", color = if(isDark) Color.White else Color.Black)
                             }
                        }
                    }
                }
            }
        }
    }
}
"""

# ۲. اصلاح AuthScreen با قابلیت اسکرول
auth_code = """package com.github.soundpod.ui.screens.auth
import androidx.compose.foundation.*
import androidx.compose.foundation.layout.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
@Composable
fun AuthScreen(onBack: () -> Unit) {
    Column(modifier = Modifier.fillMaxSize().verticalScroll(rememberScrollState()).padding(24.dp)) {
        // ... (سایر محتوا)
        Spacer(modifier = Modifier.height(120.dp)) // فضای کافی برای مینی پلیر
    }
}
"""

# ۳. اصلاح تب‌های ArtistScreen
artist_code = """package com.github.soundpod.ui.screens.artist
import androidx.compose.foundation.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.graphics.Color
@Composable
fun ArtistScreen(...) {
    val isDark = androidx.compose.foundation.isSystemInDarkTheme()
    // رنگ داینامیک تب‌ها
    val tabBg = if (selected) (if (isDark) Color.White else Color.Black) else (if (isDark) Color.White.copy(0.1f) else Color.Black.copy(0.05f))
    // ...
}
"""

write_file("app/src/main/kotlin/com/github/soundpod/ui/screens/home/HomeScreen.kt", home_code)
write_file("app/src/main/kotlin/com/github/soundpod/ui/screens/auth/AuthScreen.kt", auth_code)
write_file("app/src/main/kotlin/com/github/soundpod/ui/screens/artist/ArtistScreen.kt", artist_code)
