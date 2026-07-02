package com.github.musick.ui.screens.artist
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
import androidx.compose.ui.graphics.luminance
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
                    contentDescription = null, tint = if (androidx.compose.material3.MaterialTheme.colorScheme.background.luminance() < 0.5f) Color.White else Color.Black, modifier = Modifier.size(26.dp)
                )
            }
            IconButton(onClick = onSearchClick) {
                Icon(imageVector = Icons.Default.Search, contentDescription = null, tint = if (androidx.compose.material3.MaterialTheme.colorScheme.background.luminance() < 0.5f) Color.White else Color.Black, modifier = Modifier.size(28.dp))
            }
        },
        dropDownMenuContent = { dismissMenu ->
            DropdownMenuItem(text = { Text(stringResource(id = R.string.settings), color = colorPalette.text) }, onClick = { onSettingsClick(); dismissMenu() })
        },
        headerContent = {
            Box(modifier = Modifier.fillMaxWidth().height(360.dp)) {
                AsyncImage(model = highResCover, contentDescription = null, modifier = Modifier.fillMaxSize().blur(60.dp), contentScale = ContentScale.Crop)
                Box(modifier = Modifier.fillMaxSize().background(Brush.verticalGradient(listOf(Color.Black.copy(alpha = 0.2f), if (androidx.compose.material3.MaterialTheme.colorScheme.background.luminance() < 0.5f) Color.Black else Color.Black.copy(alpha = 0.06f)))))
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
                    Text(text = artist?.name.orEmpty(), style = typography.headlineLarge.copy(fontWeight = FontWeight.Black, fontSize = 34.sp), color = if (androidx.compose.material3.MaterialTheme.colorScheme.background.luminance() < 0.5f) Color.White else Color.Black, maxLines = 1, overflow = TextOverflow.Ellipsis)
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
                        val isDark = androidx.compose.material3.MaterialTheme.colorScheme.background.luminance() < 0.5f
                        
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
