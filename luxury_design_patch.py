import os

# ۱. دیزاین لوکس و شیشه‌ای صفحه آرتیست
fp_artist = "app/src/main/kotlin/com/github/soundpod/ui/screens/artist/ArtistScreen.kt"
code_artist = """package com.github.musick.ui.screens.artist

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
    return extracted.replace(Regex("=w\\\\d+-h\\\\d+"), "=w1080-h1080").replace(Regex("=s\\\\d+"), "=s1080")
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
                    contentDescription = null, tint = Color.White, modifier = Modifier.size(26.dp)
                )
            }
            IconButton(onClick = onSearchClick) {
                Icon(imageVector = Icons.Default.Search, contentDescription = null, tint = Color.White, modifier = Modifier.size(28.dp))
            }
        },
        dropDownMenuContent = { dismissMenu ->
            DropdownMenuItem(text = { Text(stringResource(id = R.string.settings), color = colorPalette.text) }, onClick = { onSettingsClick(); dismissMenu() })
        },
        headerContent = {
            Box(modifier = Modifier.fillMaxWidth().height(360.dp)) {
                // بک گراند به شدت تار و اتمسفریک
                AsyncImage(model = highResCover, contentDescription = null, modifier = Modifier.fillMaxSize().blur(60.dp), contentScale = ContentScale.Crop)
                Box(modifier = Modifier.fillMaxSize().background(Brush.verticalGradient(listOf(Color.Black.copy(alpha = 0.2f), Color.Black))))
                
                Column(
                    modifier = Modifier.fillMaxSize().padding(bottom = 24.dp),
                    horizontalAlignment = Alignment.CenterHorizontally,
                    verticalArrangement = Arrangement.Bottom
                ) {
                    // آواتار آرتیست: گرد، با حاشیه شیشه ای و سایه
                    AsyncImage(
                        model = highResCover, 
                        contentDescription = null, 
                        modifier = Modifier.size(170.dp).shadow(24.dp, CircleShape).clip(CircleShape).border(3.dp, Color.White.copy(alpha = 0.3f), CircleShape),
                        contentScale = ContentScale.Crop
                    )
                    Spacer(modifier = Modifier.height(16.dp))
                    Text(text = artist?.name.orEmpty(), style = typography.headlineLarge.copy(fontWeight = FontWeight.Black, fontSize = 34.sp), color = Color.White, maxLines = 1, overflow = TextOverflow.Ellipsis)
                    
                    // بازگرداندن اطلاعات اضافه با استایل ظریف
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
                        Box(
                            modifier = Modifier
                                .clip(RoundedCornerShape(50))
                                .background(if (selected) Color.White else Color.White.copy(alpha = 0.1f))
                                .clickable { coroutineScope.launch { pagerState.animateScrollToPage(index) } }
                                .padding(horizontal = 20.dp, vertical = 10.dp)
                        ) {
                            Text(text = stringResource(titleRes), style = typography.titleSmall.copy(fontWeight = FontWeight.Bold), color = if (selected) Color.Black else Color.White)
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
with open(fp_artist, "w") as f: f.write(code_artist)

# ۲. دیزاین عظیم، سینمایی و کامل صفحه آلبوم و سینگل
fp_album = "app/src/main/kotlin/com/github/soundpod/ui/screens/album/AlbumScreen.kt"
code_album = """package com.github.musick.ui.screens.album

import androidx.activity.compose.BackHandler
import androidx.compose.animation.ExperimentalAnimationApi
import androidx.compose.foundation.ExperimentalFoundationApi
import androidx.compose.foundation.background
import androidx.compose.foundation.basicMarquee
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
                Icon(imageVector = Icons.Default.Search, contentDescription = null, tint = Color.White)
            }
        },
        dropDownMenuContent = { dismissMenu ->
            DropdownMenuItem(text = { Text(stringResource(id = R.string.settings), color = colorPalette.text) }, onClick = { onSettingsClick(); dismissMenu() })
        },
        headerContent = {
            Box(modifier = Modifier.fillMaxWidth().wrapContentHeight()) {
                // پس زمینه تار داینامیک
                AsyncImage(model = highResCover, contentDescription = null, modifier = Modifier.fillMaxWidth().height(450.dp).blur(80.dp), contentScale = ContentScale.Crop)
                Box(modifier = Modifier.fillMaxWidth().height(450.dp).background(Brush.verticalGradient(listOf(Color.Black.copy(alpha = 0.3f), Color.Black))))
                
                Column(
                    modifier = Modifier.fillMaxWidth().padding(top = 40.dp, bottom = 24.dp),
                    horizontalAlignment = Alignment.CenterHorizontally
                ) {
                    // کاور عظیم، با لبه های نرم و سایه سنگین
                    AsyncImage(
                        model = highResCover, 
                        contentDescription = null, 
                        modifier = Modifier.fillMaxWidth(0.75f).aspectRatio(1f).shadow(32.dp, RoundedCornerShape(24.dp)).clip(RoundedCornerShape(24.dp)),
                        contentScale = ContentScale.Crop
                    )
                    
                    Spacer(modifier = Modifier.height(28.dp))
                    
                    // نام آلبوم/سینگل - بسیار درشت و چشم نواز
                    Text(
                        text = album?.title.orEmpty(),
                        style = typography.headlineMedium.copy(fontWeight = FontWeight.Black, fontSize = 28.sp),
                        color = Color.White,
                        textAlign = TextAlign.Center,
                        maxLines = 2,
                        overflow = TextOverflow.Ellipsis,
                        modifier = Modifier.fillMaxWidth(0.85f).basicMarquee()
                    )
                    
                    Spacer(modifier = Modifier.height(8.dp))
                    
                    // بازگرداندن آرتیست و سال انتشار به شکلی بسیار ظریف و مجله ای
                    Text(
                        text = (album?.authorsText.orEmpty()) + (if (album?.year != null) " • " + album.year else ""),
                        style = typography.titleMedium.copy(fontWeight = FontWeight.Bold, fontSize = 16.sp),
                        color = Color.White.copy(alpha = 0.7f),
                        textAlign = TextAlign.Center,
                        maxLines = 1,
                        modifier = Modifier.fillMaxWidth(0.8f).basicMarquee().clickable(enabled = album?.artistId != null) { album?.artistId?.let { onGoToArtist(it) } }
                    )
                    
                    Spacer(modifier = Modifier.height(24.dp))
                    
                    // نوار دکمه های شیشه ای (پلی و لایک)
                    Row(
                        modifier = Modifier.fillMaxWidth(),
                        horizontalArrangement = Arrangement.Center,
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        Button(
                            onClick = { /* عمل پخش */ },
                            colors = ButtonDefaults.buttonColors(containerColor = Color.White, contentColor = Color.Black),
                            shape = RoundedCornerShape(50),
                            modifier = Modifier.height(56.dp).width(160.dp).shadow(8.dp, RoundedCornerShape(50))
                        ) {
                            Icon(Icons.Default.PlayArrow, contentDescription = null, modifier = Modifier.size(28.dp))
                            Spacer(modifier = Modifier.width(8.dp))
                            Text("Play", fontWeight = FontWeight.Black, fontSize = 18.sp)
                        }
                        
                        Spacer(modifier = Modifier.width(16.dp))
                        
                        IconButton(
                            onClick = { viewModel.toggleLove() },
                            modifier = Modifier.size(56.dp).clip(CircleShape).background(Color.White.copy(alpha = 0.15f))
                        ) {
                            Icon(
                                imageVector = ImageVector.vectorResource(if (uiState.isLoved) R.drawable.heart else R.drawable.heart_outline),
                                contentDescription = null, 
                                tint = if (uiState.isLoved) Color(0xFFFF4B4B) else Color.White, 
                                modifier = Modifier.size(28.dp)
                            )
                        }
                    }
                }
            }
        },
        content = { AlbumSongs(browseId = browseId, onGoToArtist = onGoToArtist) }
    )
}
"""
with open(fp_album, "w") as f: f.write(code_album)

print("SURPRISE! Premium Glassmorphic UI Injected Successfully! 🎨✨")
