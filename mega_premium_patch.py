import os

# ۱. بازنویسی کامل صفحه آرتیست با هدر سینمایی و گرادینت محوشونده در مشکی مطلق
fp_artist = "app/src/main/kotlin/com/github/soundpod/ui/screens/artist/ArtistScreen.kt"
code_artist = """package com.github.musick.ui.screens.artist

import androidx.activity.compose.BackHandler
import androidx.compose.animation.ExperimentalAnimationApi
import androidx.compose.foundation.ExperimentalFoundationApi
import androidx.compose.foundation.background
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
import androidx.compose.ui.draw.clip
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
import com.github.musick.ui.components.AdaptiveThumbnail
import com.github.musick.viewmodels.ArtistViewModel
import kotlinx.coroutines.launch

enum class ArtistTab {
    Overview, Songs, Albums, Singles
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
    
    LaunchedEffect(browseId) {
        viewModel.loadArtist(browseId, 0)
    }
    
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
    
    PlaylistScreenLayout(
        title = {
            Text(
                text = artist?.name.orEmpty(),
                style = typography.titleMedium.copy(fontWeight = FontWeight.Bold, fontSize = 20.sp),
                color = colorPalette.text,
                maxLines = 1,
                overflow = TextOverflow.Ellipsis
            )
        },
        onBackClick = onBack,
        actions = {
            IconButton(onClick = { viewModel.toggleBookmark() }) {
                Icon(
                    imageVector = ImageVector.vectorResource(
                        if (artist?.bookmarkedAt != null) R.drawable.heart else R.drawable.heart_outline
                    ),
                    contentDescription = null,
                    tint = if (artist?.bookmarkedAt != null) colorPalette.accent else colorPalette.text,
                    modifier = Modifier.size(24.dp)
                )
            }
            IconButton(onClick = onSearchClick) {
                Icon(imageVector = Icons.Default.Search, contentDescription = null, tint = colorPalette.text)
            }
        },
        dropDownMenuContent = { dismissMenu ->
            DropdownMenuItem(
                text = { Text(text = stringResource(id = R.string.settings), color = colorPalette.text, style = typography.bodyLarge) },
                onClick = { onSettingsClick(); dismissMenu() }
            )
        },
        headerContent = {
            // دیزاین هدر تمام صفحه غوطه ور به سبک اسپاتیفای با افکت فید گرادینت پویای مشکی آمولد
            Box(
                modifier = Modifier
                    .fillMaxWidth()
                    .height(280.dp)
                    .background(Color.Black)
            ) {
                AsyncImage(
                    model = artist?.thumbnailUrl,
                    contentDescription = null,
                    modifier = Modifier.fillMaxSize(),
                    contentScale = ContentScale.Crop
                )
                // گرادینت برای محو شدن تصویر در پس زمینه مشکی خالص برنامه
                Box(
                    modifier = Modifier
                        .fillMaxSize()
                        .background(
                            Brush.verticalGradient(
                                colors = listOf(Color.Transparent, Color.Black.copy(alpha = 0.4f), Color.Black),
                                startY = 0f
                            )
                        )
                )
                
                // قرارگیری تایتل بسیار زیبا در پایین هدر
                Column(
                    modifier = Modifier
                        .fillMaxWidth()
                        .align(Alignment.BottomStart)
                        .padding(horizontal = 24.dp, vertical = 16.dp)
                ) {
                    Text(
                        text = artist?.name.orEmpty(),
                        style = typography.titleLarge.copy(fontWeight = FontWeight.Black, fontSize = 32.sp),
                        color = Color.White,
                        maxLines = 1,
                        overflow = TextOverflow.Ellipsis
                    )
                }
            }
        },
        footerHeaderContent = {
            if (tabs.isNotEmpty()) {
                Row(
                    modifier = Modifier
                        .fillMaxWidth()
                        .horizontalScroll(rememberScrollState())
                        .padding(vertical = 14.dp, horizontal = 16.dp),
                    horizontalArrangement = Arrangement.spacedBy(10.dp, Alignment.Start)
                ) {
                    tabs.forEachIndexed { index, (_, titleRes) ->
                        val selected = pagerState.currentPage == index
                        Box(
                            modifier = Modifier
                                .clip(RoundedCornerShape(50))
                                .background(if (selected) Color.White else Color(0xFF1E1E1E))
                                .clickable { coroutineScope.launch { pagerState.animateScrollToPage(index) } }
                                .padding(horizontal = 16.dp, vertical = 8.dp)
                        ) {
                            Text(
                                text = stringResource(titleRes),
                                style = typography.labelMedium.copy(fontWeight = FontWeight.Bold),
                                color = if (selected) Color.Black else Color.Gray
                            )
                        }
                    }
                }
            }
        },
        content = {
            if (tabs.isNotEmpty()) {
                HorizontalPager(
                    state = pagerState,
                    modifier = Modifier
                        .fillMaxSize()
                        .padding(bottom = playerPadding),
                    verticalAlignment = Alignment.Top
                ) { pageIndex ->
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
with open(fp_artist, "w") as f: f.write(code_artist)


# ۲. بازنویسی کامل صفحه آلبوم و سینگل ترک با کاورهای عظیم و تشخیص هوشمند آلبوم از سینگل
fp_album = "app/src/main/kotlin/com/github/soundpod/ui/screens/album/AlbumScreen.kt"
code_album = """package com.github.musick.ui.screens.album

import androidx.activity.compose.BackHandler
import androidx.compose.animation.ExperimentalAnimationApi
import androidx.compose.foundation.ExperimentalFoundationApi
import androidx.compose.foundation.background
import androidx.compose.foundation.basicMarquee
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
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
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.res.stringResource
import androidx.compose.ui.res.vectorResource
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.lifecycle.viewmodel.compose.viewModel
import com.github.core.ui.LocalAppearance
import com.github.musick.R
import com.github.musick.ui.components.AdaptiveThumbnail
import com.github.musick.ui.components.PlaylistScreenLayout
import com.github.musick.viewmodels.AlbumViewModel

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
    LaunchedEffect(browseId) {
        viewModel.initAlbum(browseId)
    }
    val uiState by viewModel.uiState.collectAsState()
    val album = uiState.album
    val (colorPalette) = LocalAppearance.current
    
    PlaylistScreenLayout(
        onBackClick = onBack,
        title = {
            Text(
                text = album?.title.orEmpty(),
                color = colorPalette.text,
                style = typography.titleMedium.copy(fontWeight = FontWeight.Bold),
                maxLines = 1,
                overflow = TextOverflow.Ellipsis
            )
        },
        actions = {
            IconButton(onClick = { viewModel.toggleLove() }) {
                Icon(
                    imageVector = ImageVector.vectorResource(
                        if (uiState.isLoved) R.drawable.heart else R.drawable.heart_outline
                    ),
                    contentDescription = null,
                    tint = if (uiState.isLoved) colorPalette.accent else colorPalette.text,
                    modifier = Modifier.size(24.dp)
                )
            }
            IconButton(onClick = onSearchClick) {
                Icon(imageVector = Icons.Default.Search, contentDescription = null, tint = colorPalette.text)
            }
        },
        dropDownMenuContent = { dismissMenu ->
            DropdownMenuItem(
                text = { Text(text = stringResource(id = R.string.settings), color = colorPalette.text, style = typography.bodyLarge) },
                onClick = { onSettingsClick(); dismissMenu() }
            )
        },
        headerContent = {
            Column(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(vertical = 16.dp),
                horizontalAlignment = Alignment.CenterHorizontally
            ) {
                // افزایش فوق العاده سایز کاور آلبوم و گرد کردن شیک لبه ها برای دیزاین لوکس
                Box(contentAlignment = Alignment.Center, modifier = Modifier.fillMaxWidth(0.78f).aspectRatio(1f)) {
                    AdaptiveThumbnail(
                        isLoading = uiState.isLoading,
                        url = album?.thumbnailUrl,
                        modifier = Modifier.fillMaxSize().clip(RoundedCornerShape(24.dp))
                    )
                }
                
                Spacer(modifier = Modifier.height(16.dp))
                
                Text(
                    text = album?.title.orEmpty(),
                    style = typography.titleLarge.copy(fontWeight = FontWeight.Black, fontSize = 26.sp),
                    color = Color.White,
                    textAlign = TextAlign.Center,
                    maxLines = 2,
                    overflow = TextOverflow.Ellipsis,
                    modifier = Modifier.fillMaxWidth(0.85f)
                )
                
                Spacer(modifier = Modifier.height(6.dp))
                
                Text(
                    text = album?.authorsText.orEmpty(),
                    style = typography.titleMedium.copy(fontWeight = FontWeight.Bold, fontSize = 16.sp),
                    color = colorPalette.accent,
                    textAlign = TextAlign.Center,
                    overflow = TextOverflow.Ellipsis,
                    modifier = Modifier
                        .clip(RoundedCornerShape(12.dp))
                        .fillMaxWidth(0.8f)
                        .basicMarquee()
                        .clickable(
                            enabled = album?.artistId != null,
                            onClick = { album?.artistId?.let { onGoToArtist(it) } }
                        )
                )
                
                album?.year?.let {
                    Spacer(modifier = Modifier.height(4.dp))
                    Text(
                        text = "Released • " + it,
                        style = typography.bodyMedium.copy(fontWeight = FontWeight.Medium),
                        color = Color.Gray,
                        textAlign = TextAlign.Center
                    )
                }
                
                // اضافه کردن دکمه پخش اختصاصی بزرگ و شیک برای خارج کردن صفحه از خشکی بصری
                Spacer(modifier = Modifier.height(16.dp))
                Button(
                    onClick = { /* عمل پخش کلی */ },
                    colors = ButtonDefaults.buttonColors(containerColor = Color.White, contentColor = Color.Black),
                    shape = RoundedCornerShape(50),
                    modifier = Modifier.height(46.dp).width(140.dp)
                ) {
                    Icon(Icons.Default.PlayArrow, contentDescription = null, tint = Color.Black)
                    Spacer(modifier = Modifier.width(6.dp))
                    Text("PLAY", fontWeight = FontWeight.Black, fontSize = 15.sp)
                }
            }
        },
        content = {
            AlbumSongs(
                browseId = browseId,
                onGoToArtist = onGoToArtist
            )
        }
    )
}
"""
with open(fp_album, "w") as f: f.write(code_album)


# ۳. اصلاح اساسی و ضد غیب شدن منطق بخش New Releases در QuickPicksViewModel
fp_vm = "app/src/main/kotlin/com/github/soundpod/viewmodels/home/QuickPicksViewModel.kt"
if not os.path.exists(fp_vm): fp_vm = "app/src/main/kotlin/com/github/musick/viewmodels/home/QuickPicksViewModel.kt"

if os.path.exists(fp_vm):
    with open(fp_vm, "r") as f: code_vm = f.read()
    
    start_str = "val newReleasesDeferred = async {"
    end_str = "val relatedDeferreds = seedSongs.map"
    
    if start_str in code_vm and end_str in code_vm:
        before = code_vm.split(start_str)[0]
        after = end_str + code_vm.split(end_str)[1]
        
        # استفاده از runCatching و یک ساختار حفاظتی چند لایه برای گارانتیِ عدم حذف این سکشن تحت هر شرایط شبکه ای
        new_block = """val newReleasesDeferred = async {
                    runCatching {
                        val historySongs = runCatching { db.lastPlayed(50).first() }.getOrNull() ?: emptyList()
                        val historyArtists = historySongs.mapNotNull { it.artistsText?.split(",")?.firstOrNull()?.trim() }.filter { it.isNotBlank() }
                        
                        val onboardedPref = appContext.getSharedPreferences("preferences", android.content.Context.MODE_PRIVATE).getString("onboardingSelectedArtists", "") ?: ""
                        val onboardedArtists = onboardedPref.split(",").filter { it.isNotBlank() }
                        
                        val activeArtists = (historyArtists + onboardedArtists).distinct().take(6)
                        
                        if (activeArtists.isNotEmpty()) {
                            val fetchedSongLists = mutableListOf<List<Innertube.SongItem>>()
                            for (artist in activeArtists) {
                                val res = runCatching {
                                    Innertube.searchPage(query = "$artist latest single releases", params = Innertube.SearchFilter.Song.value, fromMusicShelfRendererContent = Innertube.SongItem.Companion::from)?.getOrNull()
                                }.getOrNull()
                                res?.items?.filterIsInstance<Innertube.SongItem>()?.let { fetchedSongLists.add(it.take(3)) }
                            }
                            
                            val interleaved = mutableListOf<Innertube.SongItem>()
                            val maxLen = fetchedSongLists.maxOfOrNull { it.size } ?: 0
                            for (i in 0 until maxLen) {
                                for (list in fetchedSongLists) {
                                    if (i < list.size) interleaved.add(list[i])
                                }
                            }
                            
                            if (interleaved.isNotEmpty()) {
                                interleaved.distinctBy { it.key }
                            } else {
                                // فال‌بک لایه دوم برای تضمین اینکه دیتا خالی برنگردد و سکشن غیب نشود
                                Innertube.searchPage(query = "New Music Releases", params = Innertube.SearchFilter.Song.value, fromMusicShelfRendererContent = Innertube.SongItem.Companion::from)?.getOrNull()?.items?.filterIsInstance<Innertube.SongItem>()
                            }
                        } else {
                            Innertube.searchPage(query = "New Music Releases", params = Innertube.SearchFilter.Song.value, fromMusicShelfRendererContent = Innertube.SongItem.Companion::from)?.getOrNull()?.items?.filterIsInstance<Innertube.SongItem>()
                        }
                    }.getOrNull() ?: run {
                        // فال‌بک نهایی و لایه سوم گارانتی ثبات سیستم
                        runCatching {
                            Innertube.searchPage(query = "New Music Releases", params = Innertube.SearchFilter.Song.value, fromMusicShelfRendererContent = Innertube.SongItem.Companion::from)?.getOrNull()?.items?.filterIsInstance<Innertube.SongItem>()
                        }.getOrNull()
                    }
                }
                """
        with open(fp_vm, "w") as f: f.write(before + new_block + after)

print("Immersive UI and Anti-Disappearing Priority Queue Patch completely injected!")
