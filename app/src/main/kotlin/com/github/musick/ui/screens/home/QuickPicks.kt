@file:OptIn(androidx.compose.foundation.ExperimentalFoundationApi::class, androidx.compose.animation.ExperimentalAnimationApi::class)
package com.github.musick.ui.screens.home

import android.annotation.SuppressLint
import androidx.compose.animation.Crossfade
import androidx.compose.animation.ExperimentalAnimationApi
import androidx.compose.animation.core.*
import androidx.compose.foundation.ExperimentalFoundationApi
import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.isSystemInDarkTheme
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.LazyRow
import androidx.compose.foundation.lazy.grid.GridCells
import androidx.compose.foundation.lazy.grid.LazyHorizontalGrid
import androidx.compose.foundation.lazy.grid.items
import androidx.compose.foundation.lazy.grid.rememberLazyGridState
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.pager.HorizontalPager
import androidx.compose.foundation.pager.rememberPagerState
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.PlayArrow
import androidx.compose.material.icons.outlined.DownloadForOffline
import androidx.compose.material.icons.outlined.Refresh
import androidx.compose.material.icons.rounded.OpenInNew
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.draw.scale
import androidx.compose.ui.draw.shadow
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.graphicsLayer
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.platform.LocalConfiguration
import androidx.compose.ui.res.stringResource
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.compose.ui.util.lerp
import androidx.compose.ui.window.Dialog
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
import com.github.musick.ui.components.SpeedDialGrid
import com.github.musick.ui.components.FeedItemMock
import java.io.IOException
import java.util.Calendar

private fun extractHighResUrlLocal(rawThumb: String?): String {
    if (rawThumb == null) return ""
    var extracted = if (rawThumb.contains("url=")) Regex("url=([^,)]+)").find(rawThumb)?.groupValues?.get(1) ?: rawThumb else rawThumb
    extracted = if (extracted.startsWith("//")) "https:$extracted" else extracted
    return extracted.replace(Regex("=w\\d+-h\\d+"), "=w1080-h1080").replace(Regex("=s\\d+"), "=s1080")
}

@SuppressLint("ConfigurationScreenWidthHeight")
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

    var currentPlayingMediaItem by remember { mutableStateOf<androidx.media3.common.MediaItem?>(null) }
    DisposableEffect(binder?.player) {
        val listener = object : androidx.media3.common.Player.Listener {
            override fun onMediaItemTransition(mediaItem: androidx.media3.common.MediaItem?, reason: Int) {
                currentPlayingMediaItem = mediaItem
            }
        }
        binder?.player?.addListener(listener)
        currentPlayingMediaItem = binder?.player?.currentMediaItem
        onDispose { binder?.player?.removeListener(listener) }
    }

    LaunchedEffect(quickPicksSource, quickPicksCustomGenre) {
        viewModel.loadQuickPicks(quickPicksSource = quickPicksSource, forceRefresh = quickPicksSource == QuickPicksSource.Custom)
    }

    val configuration = LocalConfiguration.current
    val screenWidth = configuration.screenWidthDp.dp
    val quickPicksLazyGridItemWidthFactor = if (isLandscape && screenWidth * 0.475f >= 320.dp) 0.475f else 0.9f
    val itemInHorizontalGridWidth = screenWidth * quickPicksLazyGridItemWidthFactor

    // تغییر ذخیره سازی میکس از حالت ماکت (Mock) به دیتای واقعی آهنگ (MediaItem)
    var mixToShow by remember { mutableStateOf<Pair<String, List<androidx.media3.common.MediaItem>>?>(null) }

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
            val recentHistory by viewModel.recentHistoryFlow.collectAsState(initial = emptyList())
            
            // معماری بی‌نقص برای شیفت خوردن اسپید دایل
            val speedDialItems = remember(recentHistory, related.songs) {
                val historyMocks = recentHistory.map { song -> FeedItemMock(id = song.id, title = song.title, subtitle = song.artistsText ?: "", thumbnailUrl = extractHighResUrlLocal(song.thumbnailUrl)) }
                val recommendedMocks = related.songs?.mapNotNull { song -> song.info?.endpoint?.videoId?.let { videoId -> FeedItemMock(id = videoId, title = song.info?.name.orEmpty(), subtitle = song.authors?.firstOrNull()?.name.orEmpty(), thumbnailUrl = extractHighResUrlLocal(song.thumbnail?.url)) } } ?: emptyList()
                (historyMocks + recommendedMocks).distinctBy { it.id }.take(24)
            }

            if (speedDialItems.isNotEmpty()) {
                SpeedDialGrid(
                    items = speedDialItems, 
                    onItemClick = { browseId -> 
                        try {
                            // پیدا کردن DNA واقعی آهنگ به جای استفاده از ماکتِ خراب
                            val songFromDb = recentHistory.firstOrNull { it.id == browseId }?.asMediaItem
                            val songFromApi = related.songs?.firstOrNull { it.info?.endpoint?.videoId == browseId }?.asMediaItem
                            val finalMediaItem = songFromDb ?: songFromApi ?: if (currentPlayingMediaItem?.mediaId == browseId) currentPlayingMediaItem else null
                            
                            if (finalMediaItem != null) {
                                binder?.stopRadio()
                                binder?.player?.forcePlay(finalMediaItem)
                                binder?.setupRadio(NavigationEndpoint.Endpoint.Watch(videoId = finalMediaItem.mediaId))
                            }
                        } catch (e: Exception) { e.printStackTrace() }
                    }
                )
                Spacer(modifier = Modifier.height(16.dp))
            }

            Text(text = stringResource(id = R.string.quick_picks), style = MaterialTheme.typography.titleLarge.copy(fontSize = 26.sp, fontWeight = FontWeight.Black, color = MaterialTheme.colorScheme.onBackground), modifier = sectionTextModifier)
            LazyHorizontalGrid(
                state = quickPicksLazyGridState, rows = GridCells.Fixed(count = 3),
                modifier = Modifier.fillMaxWidth().height(215.dp),
                horizontalArrangement = Arrangement.spacedBy(8.dp), verticalArrangement = Arrangement.spacedBy(4.dp)
            ) {
                items(items = (related.songs ?: emptyList()).filter { it.key.isNotEmpty() }.distinctBy { it.key + it.info?.endpoint?.playlistId.orEmpty() }, key = { it.key + it.info?.endpoint?.playlistId.orEmpty() }) { song ->
                    SongItem(modifier = Modifier.animateItem().width(itemInHorizontalGridWidth), song = song, onClick = { try { val mediaItem = song.asMediaItem; binder?.stopRadio(); binder?.player?.forcePlay(mediaItem); binder?.setupRadio(NavigationEndpoint.Endpoint.Watch(videoId = mediaItem.mediaId)) } catch(e:Exception){} }, onLongClick = { menuState.display { NonQueuedMediaItemMenu(onDismiss = menuState::hide, mediaItem = song.asMediaItem, onGoToAlbum = onAlbumClick, onGoToArtist = onArtistClick) } })
                }
            }

            val newReleasesRaw = viewModel.newReleasesResult?.getOrNull()
            val personalizedNewReleases = remember(newReleasesRaw, recentHistory) {
                if (newReleasesRaw.isNullOrEmpty()) emptyList()
                else {
                    val myArtists = recentHistory.mapNotNull { it.artistsText }.flatMap { it.split(Regex(" & |, | x | • ")) }.map { it.trim().lowercase() }.toSet()
                    val matched = newReleasesRaw.filter { song ->
                        val songArtist = song.asMediaItem.mediaMetadata.artist?.toString()?.lowercase() ?: ""
                        myArtists.any { songArtist.contains(it) }
                    }
                    if (matched.isNotEmpty()) matched else newReleasesRaw.take(8)
                }
            }
            if (personalizedNewReleases.isNotEmpty()) {
                Spacer(modifier = Modifier.height(36.dp))
                Row(modifier = sectionTextModifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween, verticalAlignment = Alignment.CenterVertically) {
                    Text(text = "New releases", style = MaterialTheme.typography.titleLarge.copy(fontSize = 24.sp, fontWeight = FontWeight.Black, color = MaterialTheme.colorScheme.onBackground))
                    Icon(Icons.Default.PlayArrow, contentDescription = null, tint = MaterialTheme.colorScheme.onBackground.copy(alpha = 0.5f))
                }
                LazyHorizontalGrid(
                    rows = GridCells.Fixed(2), modifier = Modifier.fillMaxWidth().height(160.dp),
                    contentPadding = PaddingValues(horizontal = 16.dp), horizontalArrangement = Arrangement.spacedBy(16.dp), verticalArrangement = Arrangement.spacedBy(16.dp)
                ) {
                    items(items = personalizedNewReleases.filter { it.key.isNotEmpty() }.distinctBy { it.key }, key = { it.key }) { song ->
                        Row(modifier = Modifier.width(300.dp).clickable { try { val mediaItem = song.asMediaItem; binder?.stopRadio(); binder?.player?.forcePlay(mediaItem); binder?.setupRadio(NavigationEndpoint.Endpoint.Watch(videoId = mediaItem.mediaId)) } catch(e:Exception){} }, verticalAlignment = Alignment.CenterVertically) {
                            AsyncImage(model = extractHighResUrlLocal(song.asMediaItem.mediaMetadata.artworkUri?.toString()), contentDescription = null, contentScale = ContentScale.Crop, modifier = Modifier.size(68.dp).clip(RoundedCornerShape(8.dp)))
                            Spacer(modifier = Modifier.width(12.dp))
                            Column(modifier = Modifier.weight(1f)) {
                                Text(text = song.asMediaItem.mediaMetadata.title.toString(), style = MaterialTheme.typography.titleMedium.copy(fontWeight = FontWeight.Bold, fontSize = 15.sp), maxLines = 1, overflow = TextOverflow.Ellipsis, color = MaterialTheme.colorScheme.onBackground)
                                Text(text = "Single • ${song.asMediaItem.mediaMetadata.artist}", style = MaterialTheme.typography.bodyMedium.copy(fontSize = 13.sp), maxLines = 1, overflow = TextOverflow.Ellipsis, color = MaterialTheme.colorScheme.onBackground.copy(alpha = 0.6f))
                            }
                        }
                    }
                }
            }

            val heroPagerState = rememberPagerState(pageCount = { 5 })
            val hourOfDay = Calendar.getInstance().get(Calendar.HOUR_OF_DAY)
            val timeMood = when (hourOfDay) { in 5..11 -> "Morning Energy"; in 12..17 -> "Afternoon Focus"; in 18..21 -> "Evening Chill"; else -> "Late Night Vibes" }
            
            val heroCardsData = remember(recentHistory, related.songs) {
                val fallbackImage = "https://picsum.photos/800/800?random="
                listOf(
                    Triple("Your Heavy Rotation", "The tracks you can't get enough of", recentHistory.firstOrNull()?.thumbnailUrl ?: fallbackImage+"1"),
                    Triple("Search Radar", "Mix based on your recent searches", related.songs?.randomOrNull()?.thumbnail?.url ?: fallbackImage+"2"),
                    Triple("Favorites Mix", "Your most loved tracks in one place", recentHistory.getOrNull(2)?.thumbnailUrl ?: fallbackImage+"3"),
                    Triple(timeMood, "Perfect sounds for right now", related.songs?.randomOrNull()?.thumbnail?.url ?: fallbackImage+"4"),
                    Triple("Discovery Mix", "Fresh finds based on your taste", recentHistory.getOrNull(4)?.thumbnailUrl ?: fallbackImage+"5")
                )
            }

            Spacer(modifier = Modifier.height(36.dp))
            Row(modifier = sectionTextModifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween, verticalAlignment = Alignment.CenterVertically) {
                Text(text = "Made For You", style = MaterialTheme.typography.titleLarge.copy(fontSize = 24.sp, fontWeight = FontWeight.Black, color = MaterialTheme.colorScheme.onBackground))
            }
            
            val infiniteTransition = rememberInfiniteTransition()
            // سرعت زوم سریع‌تر شد (۴ ثانیه)
            val breathScale by infiniteTransition.animateFloat(
                initialValue = 1f, targetValue = 1.08f,
                animationSpec = infiniteRepeatable(animation = tween(4000, easing = LinearEasing), repeatMode = RepeatMode.Reverse)
            )

            HorizontalPager(
                state = heroPagerState, contentPadding = PaddingValues(horizontal = 24.dp),
                pageSpacing = 16.dp, modifier = Modifier.fillMaxWidth().height(320.dp)
            ) { page ->
                val cardData = heroCardsData[page]
                val pageOffset = (heroPagerState.currentPage - page) + heroPagerState.currentPageOffsetFraction
                
                Box(
                    modifier = Modifier.fillMaxSize().graphicsLayer {
                        val scale = lerp(start = 0.85f, stop = 1f, fraction = 1f - Math.abs(pageOffset).coerceIn(0f, 1f))
                        scaleX = scale; scaleY = scale
                        alpha = lerp(start = 0.5f, stop = 1f, fraction = 1f - Math.abs(pageOffset).coerceIn(0f, 1f))
                    }.clip(RoundedCornerShape(32.dp)).clickable { 
                        try {
                            val songToPlay = recentHistory.getOrNull(page % Math.max(1, recentHistory.size))?.asMediaItem
                            if (songToPlay != null) { binder?.stopRadio(); binder?.player?.forcePlay(songToPlay); binder?.setupRadio(NavigationEndpoint.Endpoint.Watch(videoId = songToPlay.mediaId)) }
                        } catch(e:Exception){}
                    }
                ) {
                    AsyncImage(
                        model = extractHighResUrlLocal(cardData.third), contentDescription = null, contentScale = ContentScale.Crop,
                        modifier = Modifier.fillMaxSize().graphicsLayer {
                            translationX = pageOffset * 250f 
                            scaleX = breathScale; scaleY = breathScale 
                        }
                    )
                    
                    Box(modifier = Modifier.fillMaxSize().background(Brush.verticalGradient(listOf(Color.Transparent, Color.Black.copy(alpha = 0.9f)), startY = 350f)))
                    
                    Column(modifier = Modifier.align(Alignment.BottomStart).padding(24.dp).padding(end = 60.dp)) {
                        Text(text = cardData.first, style = MaterialTheme.typography.headlineMedium.copy(fontWeight = FontWeight.Black, color = Color.White))
                        Spacer(modifier = Modifier.height(6.dp))
                        Text(text = cardData.second, style = MaterialTheme.typography.bodyLarge.copy(fontWeight = FontWeight.Medium, color = Color.White.copy(alpha = 0.8f)), maxLines = 1, overflow = TextOverflow.Ellipsis)
                    }
                    
                    Row(modifier = Modifier.align(Alignment.BottomEnd).padding(20.dp), verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(10.dp)) {
                        Box(modifier = Modifier.size(38.dp).clip(CircleShape).background(Color.White.copy(alpha = 0.2f)).clickable { 
                            // دیتای واقعی میکس‌ها برای پاپ‌آپ
                            val mixItems = when(page) {
                                0 -> recentHistory.take(20).map { it.asMediaItem }
                                2 -> recentHistory.shuffled().take(20).map { it.asMediaItem }
                                else -> related.songs?.take(20)?.map { it.asMediaItem } ?: emptyList()
                            }
                            mixToShow = cardData.first to mixItems
                        }, contentAlignment = Alignment.Center) {
                            Icon(Icons.Rounded.OpenInNew, contentDescription = "View Mix", tint = Color.White, modifier = Modifier.size(18.dp))
                        }
                        Box(modifier = Modifier.size(52.dp).clip(CircleShape).background(Color.White).clickable { 
                            try {
                                val songToPlay = recentHistory.getOrNull(page % Math.max(1, recentHistory.size))?.asMediaItem
                                if (songToPlay != null) { binder?.stopRadio(); binder?.player?.forcePlay(songToPlay); binder?.setupRadio(NavigationEndpoint.Endpoint.Watch(videoId = songToPlay.mediaId)) }
                            } catch(e:Exception){}
                        }, contentAlignment = Alignment.Center) {
                            Icon(Icons.Default.PlayArrow, contentDescription = "Play", tint = Color.Black, modifier = Modifier.size(32.dp))
                        }
                    }
                }
            }

            related.albums?.let { albums ->
                Spacer(modifier = Modifier.height(24.dp))
                Text(text = stringResource(id = R.string.related_albums), style = MaterialTheme.typography.titleLarge.copy(fontSize = 24.sp, fontWeight = FontWeight.Bold, color = MaterialTheme.colorScheme.onBackground), modifier = sectionTextModifier)
                LazyRow(contentPadding = PaddingValues(horizontal = 8.dp)) { items(items = albums.filter { it.key.isNotEmpty() }.distinctBy { it.key }, key = Innertube.AlbumItem::key) { album -> AlbumItem(modifier = Modifier.width(185.dp), album = album, onClick = { onAlbumClick(album.key) }) } }
            }
            related.artists?.let { artists ->
                Spacer(modifier = Modifier.height(24.dp))
                Text(text = stringResource(id = R.string.similar_artists), style = MaterialTheme.typography.titleLarge.copy(fontSize = 24.sp, fontWeight = FontWeight.Bold, color = MaterialTheme.colorScheme.onBackground), modifier = sectionTextModifier)
                LazyRow(contentPadding = PaddingValues(horizontal = 8.dp)) { items(items = artists.filter { it.key.isNotEmpty() }.distinctBy { it.key }, key = Innertube.ArtistItem::key) { artist -> ArtistItem(modifier = Modifier.width(185.dp), artist = artist, onClick = { onArtistClick(artist.key) }) } }
            }
            related.playlists?.let { playlists ->
                Spacer(modifier = Modifier.height(24.dp))
                Text(text = stringResource(id = R.string.recommended_playlists), style = MaterialTheme.typography.titleLarge.copy(fontSize = 24.sp, fontWeight = FontWeight.Bold, color = MaterialTheme.colorScheme.onBackground), modifier = sectionTextModifier)
                LazyRow(contentPadding = PaddingValues(horizontal = 8.dp)) { items(items = playlists.filter { it.key.isNotEmpty() }.distinctBy { it.key }, key = Innertube.PlaylistItem::key) { playlist -> PlaylistItem(modifier = Modifier.width(185.dp), playlist = playlist, onClick = { onPlaylistClick(playlist.key) }) } }
            }
        } else {
            Crossfade(targetState = error, label = "RetryAnimation") { currentError ->
                if (currentError != null) {
                    Column(modifier = Modifier.fillMaxWidth().padding(top = 64.dp, bottom = 32.dp), horizontalAlignment = Alignment.CenterHorizontally, verticalArrangement = Arrangement.Center) {
                        AsyncImage(model = "file:///android_asset/img/A4.webp", contentDescription = null, modifier = Modifier.size(240.dp))
                        val errorMessage = if (currentError is IOException) stringResource(id = R.string.network_error) else stringResource(id = R.string.home_error)
                        Text(text = errorMessage, style = MaterialTheme.typography.titleMedium, textAlign = TextAlign.Center, modifier = Modifier.padding(horizontal = 32.dp))
                        Spacer(modifier = Modifier.height(24.dp))
                        Row(horizontalArrangement = Arrangement.spacedBy(12.dp), verticalAlignment = Alignment.CenterVertically) {
                            val needsConsent by YouTubeSessionManager.needsConsent.collectAsState()
                            if (needsConsent) { Button(onClick = { YouTubeSessionManager.setNeedsConsent(true) }, colors = ButtonDefaults.buttonColors(containerColor = MaterialTheme.colorScheme.primaryContainer, contentColor = MaterialTheme.colorScheme.onPrimaryContainer)) { Icon(imageVector = Icons.Outlined.DownloadForOffline, contentDescription = null); Spacer(Modifier.size(ButtonDefaults.IconSpacing)); Text(text = "Grant YouTube Consent") } }
                            else { Button(onClick = { viewModel.relatedPageResult = null; viewModel.loadQuickPicks(quickPicksSource) }) { Icon(imageVector = Icons.Outlined.Refresh, contentDescription = null); Spacer(Modifier.size(ButtonDefaults.IconSpacing)); Text(text = stringResource(id = R.string.retry)) } }
                            FilledTonalButton(onClick = onOfflinePlaylistClick) { Icon(imageVector = Icons.Outlined.DownloadForOffline, contentDescription = null); Spacer(Modifier.size(ButtonDefaults.IconSpacing)); Text(text = stringResource(id = R.string.offline)) }
                        }
                    }
                } else {
                    ShimmerHost { TextPlaceholder(modifier = sectionTextModifier); repeat(4) { ListItemPlaceholder() } }
                }
            }
        }
    }

    // پاپ‌آپِ زنده و قابل پخشِ میکس‌ها
    mixToShow?.let { (title, mixItems) ->
        Dialog(onDismissRequest = { mixToShow = null }) {
            Card(modifier = Modifier.fillMaxWidth().fillMaxHeight(0.7f).clip(RoundedCornerShape(24.dp)), colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.background)) {
                Column(modifier = Modifier.padding(16.dp)) {
                    Text(text = title, style = MaterialTheme.typography.titleLarge, fontWeight = FontWeight.Black, color = MaterialTheme.colorScheme.onBackground)
                    Spacer(modifier = Modifier.height(16.dp))
                    LazyColumn(modifier = Modifier.fillMaxSize()) {
                        items(mixItems.size) { index ->
                            val item = mixItems[index]
                            Row(modifier = Modifier.fillMaxWidth().clickable { 
                                mixToShow = null
                                try {
                                    binder?.stopRadio()
                                    binder?.player?.forcePlay(item)
                                    binder?.setupRadio(NavigationEndpoint.Endpoint.Watch(videoId = item.mediaId))
                                } catch(e:Exception){}
                            }.padding(vertical = 8.dp), verticalAlignment = Alignment.CenterVertically) {
                                AsyncImage(model = extractHighResUrlLocal(item.mediaMetadata.artworkUri?.toString()), contentDescription = null, modifier = Modifier.size(54.dp).clip(RoundedCornerShape(12.dp)), contentScale = ContentScale.Crop)
                                Spacer(modifier = Modifier.width(12.dp))
                                Column(modifier = Modifier.weight(1f)) {
                                    Text(text = item.mediaMetadata.title.toString(), style = MaterialTheme.typography.bodyLarge, color = MaterialTheme.colorScheme.onBackground, fontWeight = FontWeight.Bold, maxLines = 1, overflow = TextOverflow.Ellipsis)
                                    Text(text = item.mediaMetadata.artist.toString(), style = MaterialTheme.typography.bodyMedium, color = MaterialTheme.colorScheme.onBackground.copy(alpha=0.6f), maxLines = 1, overflow = TextOverflow.Ellipsis)
                                }
                            }
                        }
                    }
                }
            }
        }
    }
}
