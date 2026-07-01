import os

fp_qp = "app/src/main/kotlin/com/github/soundpod/ui/screens/home/QuickPicks.kt"
if not os.path.exists(fp_qp): fp_qp = "app/src/main/kotlin/com/github/musick/ui/screens/home/QuickPicks.kt"

code_qp = """package com.github.musick.ui.screens.home

import androidx.compose.material3.MaterialTheme
import androidx.compose.ui.graphics.Color
import androidx.compose.foundation.isSystemInDarkTheme
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.text.style.TextOverflow
import android.annotation.SuppressLint
import androidx.compose.animation.Crossfade
import androidx.compose.animation.ExperimentalAnimationApi
import androidx.compose.foundation.ExperimentalFoundationApi
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.lazy.LazyRow
import androidx.compose.foundation.lazy.grid.GridCells
import androidx.compose.foundation.lazy.grid.LazyHorizontalGrid
import androidx.compose.foundation.lazy.grid.items
import androidx.compose.foundation.lazy.grid.rememberLazyGridState
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.PlayArrow
import androidx.compose.material.icons.outlined.DownloadForOffline
import androidx.compose.material.icons.outlined.Refresh
import androidx.compose.material3.Button
import androidx.compose.material3.ButtonDefaults
import androidx.compose.material3.FilledTonalButton
import androidx.compose.material3.Icon
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.foundation.clickable
import androidx.compose.ui.draw.clip
import androidx.compose.ui.draw.shadow
import androidx.compose.ui.platform.LocalConfiguration
import androidx.compose.ui.res.stringResource
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.lifecycle.viewmodel.compose.viewModel
import coil3.compose.AsyncImage
import com.github.innertube.Innertube
import com.github.innertube.models.NavigationEndpoint
import com.github.musick.LocalPlayerPadding
import com.github.musick.LocalPlayerServiceBinder
import com.github.musick.R
import com.github.musick.enums.QuickPicksSource
import com.github.musick.models.LocalMenuState
import com.github.musick.service.YouTubeSessionManager
import com.github.musick.ui.components.NonQueuedMediaItemMenu
import com.github.musick.ui.components.ShimmerHost
import com.github.musick.ui.components.TextPlaceholder
import com.github.musick.ui.items.AlbumItem
import com.github.musick.ui.items.ArtistItem
import com.github.musick.ui.items.ItemPlaceholder
import com.github.musick.ui.items.ListItemPlaceholder
import com.github.musick.ui.items.PlaylistItem
import com.github.musick.ui.items.SongItem
import com.github.musick.ui.styling.Dimensions
import com.github.musick.utils.asMediaItem
import com.github.musick.utils.forcePlay
import com.github.musick.utils.isLandscape
import com.github.musick.utils.quickPicksCustomGenreKey
import com.github.musick.utils.quickPicksSourceKey
import com.github.musick.utils.rememberPreference
import com.github.musick.viewmodels.home.QuickPicksViewModel
import java.io.IOException

// تابع اختصاصی و امن برای تزریق کیفیت 4K به عکس های صفحه اصلی
private fun extractHighResUrlLocal(rawThumb: String?): String {
    if (rawThumb == null) return ""
    var extracted = if (rawThumb.contains("url=")) Regex("url=([^,)]+)").find(rawThumb)?.groupValues?.get(1) ?: rawThumb else rawThumb
    extracted = if (extracted.startsWith("//")) "https:$extracted" else extracted
    return extracted.replace(Regex("=w\\\\d+-h\\\\d+"), "=w1080-h1080").replace(Regex("=s\\\\d+"), "=s1080")
}

@SuppressLint("ConfigurationScreenWidthHeight")
@ExperimentalFoundationApi
@ExperimentalAnimationApi
@androidx.annotation.OptIn(androidx.media3.common.util.UnstableApi::class)
@Composable
fun QuickPicks(
    onAlbumClick: (String) -> Unit,
    onArtistClick: (String) -> Unit,
    onPlaylistClick: (String) -> Unit,
    onOfflinePlaylistClick: () -> Unit
) {
    val binder = LocalPlayerServiceBinder.current
    val menuState = LocalMenuState.current
    val playerPadding = LocalPlayerPadding.current
    val viewModel: QuickPicksViewModel = viewModel()
    val quickPicksSource by rememberPreference(quickPicksSourceKey, QuickPicksSource.LastPlayed)
    val quickPicksCustomGenre by rememberPreference(quickPicksCustomGenreKey, "Psaltic music")
    val quickPicksLazyGridState = rememberLazyGridState()
    val sectionTextModifier = Modifier.padding(start = 16.dp, end = 16.dp, bottom = 12.dp)
    
    LaunchedEffect(quickPicksSource, quickPicksCustomGenre) {
        viewModel.loadQuickPicks(quickPicksSource = quickPicksSource, forceRefresh = quickPicksSource == QuickPicksSource.Custom)
    }
    
    LaunchedEffect(viewModel.relatedPageResult) {
        viewModel.relatedPageResult?.getOrNull()?.songs?.let { songs ->
            binder?.preCacheManager?.preCache(songs.mapNotNull { it.info?.endpoint?.videoId })
        }
    }
    
    val configuration = LocalConfiguration.current
    val screenWidth = configuration.screenWidthDp.dp
    val quickPicksLazyGridItemWidthFactor = if (isLandscape && screenWidth * 0.475f >= 320.dp) 0.475f else 0.9f
    val itemInHorizontalGridWidth = screenWidth * quickPicksLazyGridItemWidthFactor

    Column(
        modifier = Modifier
            .fillMaxSize()
            .background(Color.Transparent)
            .verticalScroll(rememberScrollState())
            .padding(start = 0.dp, end = 0.dp, top = 4.dp, bottom = 16.dp + playerPadding)
    ) {
        val result = viewModel.relatedPageResult
        val related = result?.getOrNull()
        val error = result?.exceptionOrNull() ?: if (result != null && related == null) Exception("Empty response") else null
        
        if (related != null) {
            Text(
                text = stringResource(id = R.string.quick_picks),
                style = MaterialTheme.typography.titleLarge.copy(fontSize = 26.sp, fontWeight = FontWeight.Black, color = MaterialTheme.colorScheme.onBackground),
                modifier = sectionTextModifier.padding(top = 12.dp)
            )
            // گرید Quick Picks بزرگ‌تر، با فاصله‌گذاری شیک‌تر و مجله‌ای
            LazyHorizontalGrid(
                state = quickPicksLazyGridState,
                rows = GridCells.Fixed(count = 3),
                modifier = Modifier
                    .fillMaxWidth()
                    .height(280.dp), // افزایش ارتفاع گرید برای بزرگتر شدن کاورها
                horizontalArrangement = Arrangement.spacedBy(8.dp),
                verticalArrangement = Arrangement.spacedBy(8.dp)
            ) {
                items(
                    items = (related.songs ?: emptyList()).filter { it.key.isNotEmpty() }.distinctBy { it.key + it.info?.endpoint?.playlistId.orEmpty() },
                    key = { it.key + it.info?.endpoint?.playlistId.orEmpty() }
                ) { song ->
                    SongItem(
                        modifier = Modifier
                            .animateItem()
                            .width(itemInHorizontalGridWidth),
                        song = song,
                        onClick = {
                            val mediaItem = song.asMediaItem
                            binder?.stopRadio()
                            binder?.player?.forcePlay(mediaItem)
                            binder?.setupRadio(NavigationEndpoint.Endpoint.Watch(videoId = mediaItem.mediaId))
                        },
                        onLongClick = {
                            menuState.display {
                                NonQueuedMediaItemMenu(onDismiss = menuState::hide, mediaItem = song.asMediaItem, onGoToAlbum = onAlbumClick, onGoToArtist = onArtistClick)
                            }
                        }
                    )
                }
            }
            
            // ردیف اختصاصی New Releases با دیزاین فوق پرچمدار، سایه دار و رزولوشن بالا
            val newReleases = viewModel.newReleasesResult?.getOrNull()
            if (!newReleases.isNullOrEmpty()) {
                Spacer(modifier = Modifier.height(32.dp))
                Text(text = "New Releases", style = MaterialTheme.typography.titleLarge.copy(fontSize = 26.sp, fontWeight = FontWeight.Black, color = MaterialTheme.colorScheme.onBackground), modifier = sectionTextModifier)
                
                LazyRow(contentPadding = PaddingValues(horizontal = 16.dp), horizontalArrangement = Arrangement.spacedBy(20.dp)) {
                    items(items = newReleases, key = { it.key }) { song ->
                        Column(
                            modifier = Modifier
                                .width(175.dp)
                                .clickable {
                                    val mediaItem = song.asMediaItem
                                    binder?.stopRadio()
                                    binder?.player?.forcePlay(mediaItem)
                                    binder?.setupRadio(NavigationEndpoint.Endpoint.Watch(videoId = mediaItem.mediaId))
                                },
                            horizontalAlignment = Alignment.Start
                        ) {
                            Box(
                                modifier = Modifier
                                    .size(175.dp)
                                    .shadow(16.dp, RoundedCornerShape(20.dp))
                                    .clip(RoundedCornerShape(20.dp))
                            ) {
                                // تزریق تابع رزولوشن بالا به عکس‌ها
                                AsyncImage(
                                    model = extractHighResUrlLocal(song.asMediaItem.mediaMetadata.artworkUri?.toString()),
                                    contentDescription = null,
                                    modifier = Modifier.fillMaxSize(),
                                    contentScale = ContentScale.Crop
                                )
                                // دکمه پلی شیشه ای (Glassmorphic Play Button)
                                Box(
                                    modifier = Modifier
                                        .align(Alignment.BottomEnd)
                                        .padding(12.dp)
                                        .size(40.dp)
                                        .clip(CircleShape)
                                        .background(Color.Black.copy(alpha = 0.5f)),
                                    contentAlignment = Alignment.Center
                                ) {
                                    Icon(Icons.Default.PlayArrow, contentDescription = null, tint = Color.White, modifier = Modifier.size(24.dp))
                                }
                            }
                            Spacer(modifier = Modifier.height(14.dp))
                            Text(
                                text = song.asMediaItem.mediaMetadata.title.toString(),
                                style = MaterialTheme.typography.titleMedium.copy(fontWeight = FontWeight.Bold, fontSize = 17.sp),
                                maxLines = 1,
                                overflow = TextOverflow.Ellipsis,
                                color = MaterialTheme.colorScheme.onBackground
                            )
                            Spacer(modifier = Modifier.height(2.dp))
                            Text(
                                text = song.asMediaItem.mediaMetadata.artist.toString(),
                                style = MaterialTheme.typography.bodyMedium.copy(fontWeight = FontWeight.Medium),
                                maxLines = 1,
                                overflow = TextOverflow.Ellipsis,
                                color = Color.Gray
                            )
                        }
                    }
                }
            }
            
            related.albums?.let { albums ->
                Spacer(modifier = Modifier.height(24.dp))
                Text(text = stringResource(id = R.string.related_albums), style = MaterialTheme.typography.titleLarge.copy(fontSize = 24.sp, fontWeight = FontWeight.Bold, color = MaterialTheme.colorScheme.onBackground), modifier = sectionTextModifier)
                LazyRow(contentPadding = PaddingValues(horizontal = 8.dp)) {
                    items(items = albums.filter { it.key.isNotEmpty() }.distinctBy { it.key }, key = Innertube.AlbumItem::key) { album ->
                        AlbumItem(modifier = Modifier.width(185.dp), album = album, onClick = { onAlbumClick(album.key) })
                    }
                }
            }
            related.artists?.let { artists ->
                Spacer(modifier = Modifier.height(24.dp))
                Text(text = stringResource(id = R.string.similar_artists), style = MaterialTheme.typography.titleLarge.copy(fontSize = 24.sp, fontWeight = FontWeight.Bold, color = MaterialTheme.colorScheme.onBackground), modifier = sectionTextModifier)
                LazyRow(contentPadding = PaddingValues(horizontal = 8.dp)) {
                    items(items = artists.filter { it.key.isNotEmpty() }.distinctBy { it.key }, key = Innertube.ArtistItem::key) { artist ->
                        ArtistItem(modifier = Modifier.width(185.dp), artist = artist, onClick = { onArtistClick(artist.key) })
                    }
                }
            }
            related.playlists?.let { playlists ->
                Spacer(modifier = Modifier.height(24.dp))
                Text(text = stringResource(id = R.string.recommended_playlists), style = MaterialTheme.typography.titleLarge.copy(fontSize = 24.sp, fontWeight = FontWeight.Bold, color = MaterialTheme.colorScheme.onBackground), modifier = sectionTextModifier)
                LazyRow(contentPadding = PaddingValues(horizontal = 8.dp)) {
                    items(items = playlists.filter { it.key.isNotEmpty() }.distinctBy { it.key }, key = Innertube.PlaylistItem::key) { playlist ->
                        PlaylistItem(modifier = Modifier.width(185.dp), playlist = playlist, onClick = { onPlaylistClick(playlist.key) })
                    }
                }
            }
        } else {
            Crossfade(targetState = error, label = "RetryAnimation") { currentError ->
                if (currentError != null) {
                    Column(
                        modifier = Modifier
                            .fillMaxWidth()
                            .padding(top = 64.dp, bottom = 32.dp),
                        horizontalAlignment = Alignment.CenterHorizontally,
                        verticalArrangement = Arrangement.Center
                    ) {
                        AsyncImage(model = "file:///android_asset/img/A4.webp", contentDescription = null, modifier = Modifier.size(240.dp))
                        val errorMessage = if (currentError is IOException) stringResource(id = R.string.network_error) else stringResource(id = R.string.home_error)
                        Text(text = errorMessage, style = MaterialTheme.typography.titleMedium, textAlign = TextAlign.Center, modifier = Modifier.padding(horizontal = 32.dp))
                        Spacer(modifier = Modifier.height(24.dp))
                        Row(horizontalArrangement = Arrangement.spacedBy(12.dp), verticalAlignment = Alignment.CenterVertically) {
                            val needsConsent by YouTubeSessionManager.needsConsent.collectAsState()
                            if (needsConsent) {
                                Button(onClick = { YouTubeSessionManager.setNeedsConsent(true) }, colors = ButtonDefaults.buttonColors(containerColor = MaterialTheme.colorScheme.primaryContainer, contentColor = MaterialTheme.colorScheme.onPrimaryContainer)) {
                                    Icon(imageVector = Icons.Outlined.DownloadForOffline, contentDescription = null)
                                    Spacer(Modifier.size(ButtonDefaults.IconSpacing))
                                    Text(text = "Grant YouTube Consent")
                                }
                            } else {
                                Button(onClick = { viewModel.relatedPageResult = null; viewModel.loadQuickPicks(quickPicksSource) }) {
                                    Icon(imageVector = Icons.Outlined.Refresh, contentDescription = null)
                                    Spacer(Modifier.size(ButtonDefaults.IconSpacing))
                                    Text(text = stringResource(id = R.string.retry))
                                }
                            }
                            FilledTonalButton(onClick = onOfflinePlaylistClick) {
                                Icon(imageVector = Icons.Outlined.DownloadForOffline, contentDescription = null)
                                Spacer(Modifier.size(ButtonDefaults.IconSpacing))
                                Text(text = stringResource(id = R.string.offline))
                            }
                        }
                    }
                } else {
                    ShimmerHost {
                        TextPlaceholder(modifier = sectionTextModifier)
                        repeat(4) { ListItemPlaceholder() }
                    }
                }
            }
        }
    }
}
"""
with open(fp_qp, "w") as f: f.write(code_qp)

print("QuickPicks UI upgraded to Luxury Glassmorphic 4K Version!")
