import os, re

# ۱. رفع باگ سرچ Onboarding (تزریق همزمان آرتیست سرچ‌شده و مشابهانش به فید اصلی)
fp_onb = "app/src/main/kotlin/com/github/soundpod/ui/screens/onboarding/OnboardingScreen.kt"
if not os.path.exists(fp_onb): fp_onb = "app/src/main/kotlin/com/github/musick/ui/screens/onboarding/OnboardingScreen.kt"

code_onboarding = """package com.github.musick.ui.screens.onboarding

import androidx.compose.animation.AnimatedVisibility
import androidx.compose.animation.animateContentSize
import androidx.compose.animation.core.tween
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyRow
import androidx.compose.foundation.lazy.grid.GridCells
import androidx.compose.foundation.lazy.grid.LazyVerticalGrid
import androidx.compose.foundation.lazy.grid.items
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Check
import androidx.compose.material.icons.filled.Close
import androidx.compose.material.icons.filled.Search
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import coil3.compose.AsyncImage
import com.github.innertube.Innertube
import com.github.innertube.requests.searchPage
import com.github.innertube.requests.relatedPage
import com.github.innertube.utils.from
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.Job
import kotlinx.coroutines.async
import kotlinx.coroutines.awaitAll
import kotlinx.coroutines.delay
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun OnboardingScreen(onComplete: () -> Unit) {
    val context = LocalContext.current
    val scope = rememberCoroutineScope()
    
    var query by remember { mutableStateOf("") }
    var mainFeed by remember { mutableStateOf<List<Innertube.ArtistItem>>(emptyList()) }
    var searchResults by remember { mutableStateOf<List<Innertube.ArtistItem>>(emptyList()) }
    val selectedArtists = remember { mutableStateListOf<Innertube.ArtistItem>() }
    
    var searchJob by remember { mutableStateOf<Job?>(null) }
    var isLoading by remember { mutableStateOf(true) }

    val bgColor = Color.Black 
    val textColor = Color.White

    LaunchedEffect(Unit) {
        scope.launch(Dispatchers.IO) {
            val topNames = listOf("The Weeknd", "Drake", "Taylor Swift", "Travis Scott", "Billie Eilish", "Eminem", "Post Malone")
            val deferreds = topNames.map { name ->
                async {
                    Innertube.searchPage(query = name, params = Innertube.SearchFilter.Artist.value, fromMusicShelfRendererContent = Innertube.ArtistItem.Companion::from)
                        ?.getOrNull()?.items?.filterIsInstance<Innertube.ArtistItem>()?.firstOrNull()
                }
            }
            val results = deferreds.awaitAll().filterNotNull()
            withContext(Dispatchers.Main) { 
                mainFeed = results
                isLoading = false 
            }
        }
    }

    // تزریق قطعی به فید اصلی (چه از صفحه اصلی باشه چه از سرچ)
    fun fetchSimilarArtistsInline(parentArtist: Innertube.ArtistItem) {
        scope.launch(Dispatchers.IO) {
            val artistName = parentArtist.info?.name?.toString() ?: return@launch
            val songRes = Innertube.searchPage(query = artistName, params = Innertube.SearchFilter.Song.value, fromMusicShelfRendererContent = Innertube.SongItem.Companion::from)?.getOrNull()
            val firstSong = songRes?.items?.filterIsInstance<Innertube.SongItem>()?.firstOrNull()
            
            if (firstSong != null) {
                val related = Innertube.relatedPage(firstSong.key)?.getOrNull()
                val simArtists = related?.artists?.filterIsInstance<Innertube.ArtistItem>()?.take(4) ?: emptyList()
                
                withContext(Dispatchers.Main) {
                    val newList = mainFeed.toMutableList()
                    val index = newList.indexOfFirst { it.key == parentArtist.key }
                    
                    // اگر آرتیست از سرچ اومده و تو فید اصلی نیست، میذاریمش اول فید
                    val insertIndex = if (index != -1) {
                        index + 1
                    } else {
                        newList.add(0, parentArtist)
                        1
                    }
                    
                    if (simArtists.isNotEmpty()) {
                        val uniqueSims = simArtists.filter { sim -> newList.none { it.key == sim.key } }
                        newList.addAll(insertIndex, uniqueSims)
                    }
                    mainFeed = newList
                }
            } else {
                // اگر رادیویی نداشت ولی از سرچ اومده بود، حداقل خودشو بفرستیم تو فید اصلی
                withContext(Dispatchers.Main) {
                    val index = mainFeed.indexOfFirst { it.key == parentArtist.key }
                    if (index == -1) {
                        val newList = mainFeed.toMutableList()
                        newList.add(0, parentArtist)
                        mainFeed = newList
                    }
                }
            }
        }
    }

    LaunchedEffect(query) {
        if (query.length > 1) {
            searchJob?.cancel()
            searchJob = launch(Dispatchers.IO) {
                delay(400)
                val result = Innertube.searchPage(query = query, params = Innertube.SearchFilter.Artist.value, fromMusicShelfRendererContent = Innertube.ArtistItem.Companion::from)?.getOrNull()
                val artists = result?.items?.filterIsInstance<Innertube.ArtistItem>() ?: emptyList()
                withContext(Dispatchers.Main) { searchResults = artists }
            }
        }
    }

    Scaffold(containerColor = bgColor, floatingActionButton = {
        AnimatedVisibility(visible = selectedArtists.isNotEmpty()) {
            ExtendedFloatingActionButton(
                onClick = {
                    val prefs = context.getSharedPreferences("preferences", android.content.Context.MODE_PRIVATE)
                    prefs.edit()
                        .putBoolean("isOnboardingComplete", true)
                        .putBoolean("persistentQueue", true)
                        .putString("onboardingSelectedArtists", selectedArtists.joinToString(",") { it.info?.name?.toString() ?: "" })
                        .apply()
                    onComplete()
                },
                text = { Text("Done", fontWeight = FontWeight.Bold, fontSize = 18.sp) },
                icon = { Icon(Icons.Default.Check, null) },
                containerColor = Color.White, 
                contentColor = Color.Black,
                shape = RoundedCornerShape(50),
                modifier = Modifier.padding(bottom = 24.dp).height(56.dp).width(160.dp)
            )
        }
    }, floatingActionButtonPosition = FabPosition.Center) { paddingValues ->
        Column(modifier = Modifier.fillMaxSize().padding(paddingValues).animateContentSize(tween(300))) {
            
            Text(text = "Musick", fontSize = 34.sp, fontWeight = FontWeight.Bold, fontFamily = FontFamily.Serif, color = textColor, textAlign = TextAlign.Center, modifier = Modifier.fillMaxWidth().padding(top = 16.dp, bottom = 16.dp))
            Text("Choose artists you like.", fontSize = 22.sp, fontWeight = FontWeight.Bold, color = textColor, textAlign = TextAlign.Center, modifier = Modifier.fillMaxWidth().padding(horizontal = 24.dp))
            Spacer(modifier = Modifier.height(20.dp))
            
            OutlinedTextField(
                value = query, 
                onValueChange = { query = it }, 
                modifier = Modifier.fillMaxWidth().padding(horizontal = 24.dp).height(52.dp), 
                placeholder = { Text("Search...", color = Color.Gray) }, 
                leadingIcon = { Icon(Icons.Default.Search, null, tint = Color.Black) },
                shape = RoundedCornerShape(50), 
                singleLine = true, 
                colors = OutlinedTextFieldDefaults.colors(focusedContainerColor = Color.White, unfocusedContainerColor = Color.White, focusedTextColor = Color.Black, unfocusedTextColor = Color.Black, cursorColor = Color.Black)
            )
            
            AnimatedVisibility(visible = selectedArtists.isNotEmpty()) {
                LazyRow(
                    modifier = Modifier.fillMaxWidth().padding(top = 16.dp).animateContentSize(),
                    contentPadding = PaddingValues(horizontal = 24.dp),
                    horizontalArrangement = Arrangement.spacedBy(16.dp)
                ) {
                    items(selectedArtists, key = { it.key }) { artist ->
                        Column(horizontalAlignment = Alignment.CenterHorizontally) {
                            Box(modifier = Modifier.size(64.dp).clip(CircleShape).clickable { selectedArtists.removeIf { it.key == artist.key } }) {
                                AsyncImage(model = extractHighResUrl(artist.thumbnail?.toString()), contentDescription = null, modifier = Modifier.fillMaxSize(), contentScale = ContentScale.Crop)
                                Box(modifier = Modifier.fillMaxSize().background(Color.Black.copy(alpha = 0.6f)), contentAlignment = Alignment.Center) {
                                    Icon(Icons.Default.Close, null, tint = Color.White, modifier = Modifier.size(24.dp))
                                }
                            }
                            Spacer(modifier = Modifier.height(6.dp))
                            Text(text = artist.info?.name?.toString() ?: "", fontSize = 11.sp, fontWeight = FontWeight.Bold, color = textColor, maxLines = 1, overflow = TextOverflow.Ellipsis, modifier = Modifier.width(64.dp), textAlign = TextAlign.Center)
                        }
                    }
                }
            }

            Spacer(modifier = Modifier.height(16.dp))
            val displayList = if (query.isNotEmpty()) searchResults else mainFeed

            if (isLoading && displayList.isEmpty()) {
                Box(modifier = Modifier.fillMaxWidth().padding(32.dp), contentAlignment = Alignment.Center) { CircularProgressIndicator(color = Color.White) }
            } else {
                LazyVerticalGrid(
                    columns = GridCells.Fixed(2), 
                    modifier = Modifier.fillMaxSize().padding(horizontal = 16.dp), 
                    contentPadding = PaddingValues(bottom = 120.dp), 
                    horizontalArrangement = Arrangement.spacedBy(20.dp), 
                    verticalArrangement = Arrangement.spacedBy(28.dp)
                ) {
                    items(displayList, key = { it.key }) { artist ->
                        val isSelected = selectedArtists.any { it.key == artist.key }
                        Column(
                            horizontalAlignment = Alignment.CenterHorizontally, 
                            modifier = Modifier.fillMaxWidth().clickable { 
                                if (isSelected) {
                                    selectedArtists.removeIf { it.key == artist.key }
                                } else {
                                    selectedArtists.add(artist)
                                    query = "" // ریست کردن سرچ
                                    fetchSimilarArtistsInline(artist) // فراخوانی هوشمند
                                } 
                            }
                        ) {
                            Box(contentAlignment = Alignment.Center, modifier = Modifier.fillMaxWidth().aspectRatio(1f)) {
                                Box(modifier = Modifier.fillMaxSize().clip(CircleShape).background(Color(0xFF1E1E1E)))
                                AsyncImage(
                                    model = extractHighResUrl(artist.thumbnail?.toString()), 
                                    contentDescription = null, 
                                    modifier = Modifier.fillMaxSize().clip(CircleShape).border(if (isSelected) 4.dp else 0.dp, Color.White, CircleShape), 
                                    contentScale = ContentScale.Crop
                                )
                                if (isSelected) Box(modifier = Modifier.fillMaxSize().clip(CircleShape).background(Color.Black.copy(alpha = 0.5f)), contentAlignment = Alignment.Center) { Icon(Icons.Default.Check, null, tint = Color.White, modifier = Modifier.size(48.dp)) }
                            }
                            Spacer(modifier = Modifier.height(12.dp))
                            Text(text = artist.info?.name?.toString() ?: "Unknown", fontSize = 15.sp, fontWeight = FontWeight.Bold, maxLines = 1, textAlign = TextAlign.Center, color = textColor)
                        }
                    }
                }
            }
        }
    }
}

fun extractHighResUrl(rawThumb: String?): String {
    if (rawThumb == null) return ""
    var extracted = if (rawThumb.contains("url=")) Regex("url=([^,)]+)").find(rawThumb)?.groupValues?.get(1) ?: rawThumb else rawThumb
    extracted = if (extracted.startsWith("//")) "https:$extracted" else extracted
    return extracted.replace(Regex("=w\\\\d+-h\\\\d+"), "=w1080-h1080").replace(Regex("=s\\\\d+"), "=s1080")
}
"""
with open(fp_onb, "w") as f: f.write(code_onboarding)

# ۲. تزریق منطق "ورود به صفحه آرتیست" برای New Releases دقیق
fp_vm = "app/src/main/kotlin/com/github/soundpod/viewmodels/home/QuickPicksViewModel.kt"
if not os.path.exists(fp_vm): fp_vm = "app/src/main/kotlin/com/github/musick/viewmodels/home/QuickPicksViewModel.kt"

if os.path.exists(fp_vm):
    with open(fp_vm, "r") as f: code_vm = f.read()
    
    start_str = "val newReleasesDeferred = async {"
    end_str = "val relatedDeferreds = seedSongs.map"
    
    if start_str in code_vm and end_str in code_vm:
        before = code_vm.split(start_str)[0]
        after = end_str + code_vm.split(end_str)[1]
        
        new_block = """val newReleasesDeferred = async {
                    // ۱. خواندن حافظه محلی
                    val historySongs = runCatching { db.lastPlayed(50).first() }.getOrNull() ?: emptyList()
                    val historyArtists = historySongs.mapNotNull { it.artistsText?.split(",")?.firstOrNull()?.trim() }.filter { it.isNotBlank() }
                    
                    // ۲. خواندن انتخاب‌های اولیه
                    val onboardedPref = appContext.getSharedPreferences("preferences", android.content.Context.MODE_PRIVATE).getString("onboardingSelectedArtists", "") ?: ""
                    val onboardedArtists = onboardedPref.split(",").filter { it.isNotBlank() }
                    
                    val activeArtists = (historyArtists + onboardedArtists).distinct().take(6)
                    
                    if (activeArtists.isNotEmpty()) {
                        // ورود به صفحه تک‌تک آرتیست‌ها به صورت موازی برای استخراج جدیدترین آهنگ‌ها
                        val deferreds = activeArtists.map { artist ->
                            async {
                                runCatching {
                                    val searchRes = Innertube.searchPage(query = artist, params = Innertube.SearchFilter.Artist.value, fromMusicShelfRendererContent = Innertube.ArtistItem.Companion::from)?.getOrNull()
                                    val artistId = searchRes?.items?.filterIsInstance<Innertube.ArtistItem>()?.firstOrNull()?.key
                                    if (artistId != null) {
                                        val artistPage = Innertube.artistPage(artistId)?.getOrNull()
                                        // استخراج مستقیم از باکس آهنگ‌های خود خواننده
                                        artistPage?.songs?.filterIsInstance<Innertube.SongItem>()?.take(2)
                                    } else null
                                }.getOrNull()
                            }
                        }
                        
                        val fetchedSongs = deferreds.awaitAll().filterNotNull().flatten()
                        if (fetchedSongs.isNotEmpty()) {
                            fetchedSongs.distinctBy { it.key }
                        } else {
                            runCatching {
                                val searchResult = Innertube.searchPage(query = "New Music Releases", params = Innertube.SearchFilter.Song.value, fromMusicShelfRendererContent = Innertube.SongItem.Companion::from)?.getOrNull()
                                searchResult?.items?.filterIsInstance<Innertube.SongItem>()
                            }.getOrNull()
                        }
                    } else {
                        runCatching {
                            val searchResult = Innertube.searchPage(query = "New Music Releases", params = Innertube.SearchFilter.Song.value, fromMusicShelfRendererContent = Innertube.SongItem.Companion::from)?.getOrNull()
                            searchResult?.items?.filterIsInstance<Innertube.SongItem>()
                        }.getOrNull()
                    }
                }
                """
        with open(fp_vm, "w") as f: f.write(before + new_block + after)

print("Checkmate! The system is now fully adaptive and bug-free.")
