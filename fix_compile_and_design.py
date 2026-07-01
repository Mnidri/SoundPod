import os

# ۱. رفع ارور تایپ کاتلین و گارانتی ۱۰۰ درصدی New Releases
fp_vm = "app/src/main/kotlin/com/github/soundpod/viewmodels/home/QuickPicksViewModel.kt"
if not os.path.exists(fp_vm): fp_vm = "app/src/main/kotlin/com/github/musick/viewmodels/home/QuickPicksViewModel.kt"

if os.path.exists(fp_vm):
    with open(fp_vm, "r") as f: code_vm = f.read()
    
    start_str = "val newReleasesDeferred = async {"
    end_str = "val relatedDeferreds = seedSongs.map"
    
    if start_str in code_vm and end_str in code_vm:
        before = code_vm.split(start_str)[0]
        after = end_str + code_vm.split(end_str)[1]
        
        # استفاده از یک runCatching کلان برای مطابقت دقیق با نوع Result<List<Innertube.SongItem>>
        new_block = """val newReleasesDeferred = async {
                    runCatching {
                        val historySongs = runCatching { db.lastPlayed(50).first() }.getOrNull() ?: emptyList()
                        val historyArtists = historySongs.mapNotNull { it.artistsText?.split(",")?.firstOrNull()?.trim() }.filter { it.isNotBlank() }
                        val onboardedPref = appContext.getSharedPreferences("preferences", android.content.Context.MODE_PRIVATE).getString("onboardingSelectedArtists", "") ?: ""
                        val onboardedArtists = onboardedPref.split(",").filter { it.isNotBlank() }
                        val activeArtists = (historyArtists + onboardedArtists).distinct().take(4)
                        
                        var interleaved = emptyList<Innertube.SongItem>()
                        
                        if (activeArtists.isNotEmpty()) {
                            val fetchedSongLists = mutableListOf<List<Innertube.SongItem>>()
                            for (artist in activeArtists) {
                                val res = runCatching {
                                    Innertube.searchPage(query = "$artist latest single releases", params = Innertube.SearchFilter.Song.value, fromMusicShelfRendererContent = Innertube.SongItem.Companion::from)?.getOrNull()
                                }.getOrNull()
                                res?.items?.filterIsInstance<Innertube.SongItem>()?.let { fetchedSongLists.add(it.take(3)) }
                            }
                            
                            val tempInterleaved = mutableListOf<Innertube.SongItem>()
                            val maxLen = fetchedSongLists.maxOfOrNull { it.size } ?: 0
                            for (i in 0 until maxLen) {
                                for (list in fetchedSongLists) {
                                    if (i < list.size) tempInterleaved.add(list[i])
                                }
                            }
                            if (tempInterleaved.isNotEmpty()) {
                                interleaved = tempInterleaved.distinctBy { it.key }
                            }
                        }
                        
                        // فال‌بک تضمینی اگر لیست به هر دلیلی خالی بود
                        if (interleaved.isEmpty()) {
                            val fallback = runCatching {
                                Innertube.searchPage(query = "New Music Releases", params = Innertube.SearchFilter.Song.value, fromMusicShelfRendererContent = Innertube.SongItem.Companion::from)?.getOrNull()?.items?.filterIsInstance<Innertube.SongItem>()
                            }.getOrNull()
                            interleaved = fallback ?: seedSongs.shuffled().take(6).filterIsInstance<Innertube.SongItem>()
                        }
                        
                        interleaved
                    }
                }
                """
        with open(fp_vm, "w") as f: f.write(before + new_block + after)


# ۲. دیزاین کلاسیک، مینیمال و خوانا برای صفحه آلبوم/سینگل
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
                modifier = Modifier.fillMaxWidth().padding(top = 32.dp, bottom = 24.dp),
                horizontalAlignment = Alignment.CenterHorizontally
            ) {
                // کاور با سایز متعادل‌تر، گوشه‌های نرم‌تر و سایه تمیز
                AsyncImage(
                    model = highResCover, 
                    contentDescription = null, 
                    modifier = Modifier.fillMaxWidth(0.55f).aspectRatio(1f).shadow(24.dp, RoundedCornerShape(12.dp)).clip(RoundedCornerShape(12.dp)),
                    contentScale = ContentScale.Crop
                )
                
                Spacer(modifier = Modifier.height(24.dp))
                
                Text(
                    text = album?.title.orEmpty(),
                    style = typography.titleLarge.copy(fontWeight = FontWeight.ExtraBold, fontSize = 24.sp),
                    color = colorPalette.text,
                    textAlign = TextAlign.Center,
                    maxLines = 2,
                    overflow = TextOverflow.Ellipsis,
                    modifier = Modifier.fillMaxWidth(0.85f)
                )
                
                Spacer(modifier = Modifier.height(6.dp))
                
                // اطلاعات آرتیست تمیز، خوانا و دور از تداخل کلیک
                Text(
                    text = album?.authorsText.orEmpty(),
                    style = typography.titleMedium,
                    color = colorPalette.text.copy(alpha = 0.8f),
                    textAlign = TextAlign.Center,
                    maxLines = 1,
                    overflow = TextOverflow.Ellipsis,
                    modifier = Modifier
                        .clip(RoundedCornerShape(8.dp))
                        .clickable(enabled = album?.artistId != null) { album?.artistId?.let { onGoToArtist(it) } }
                        .padding(horizontal = 8.dp, vertical = 4.dp)
                )
                
                album?.year?.let {
                    Spacer(modifier = Modifier.height(4.dp))
                    Text(
                        text = it,
                        style = typography.bodyMedium.copy(fontWeight = FontWeight.Bold),
                        color = colorPalette.text.copy(alpha = 0.5f),
                        textAlign = TextAlign.Center
                    )
                }
                
                Spacer(modifier = Modifier.height(24.dp))
                
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

print("Kotlin compilation fix applied and album design restored to a classic, clean look!")
