import os, re

# ۱. بازنویسی OnboardingScreen: کاورهای 1080p، لیست خارجی طولانی، پیشنهاد Inline و تایتل Musick
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

    // دریافت آرتیست‌های تاپ جهانی به صورت موازی (سریع‌تر)
    LaunchedEffect(Unit) {
        scope.launch(Dispatchers.IO) {
            val topNames = listOf("The Weeknd", "Drake", "Taylor Swift", "Travis Scott", "Billie Eilish", "Post Malone", "Bad Bunny", "Dua Lipa", "Justin Bieber", "Eminem")
            val list = mutableListOf<Innertube.ArtistItem>()
            
            val deferreds = topNames.map { name ->
                async {
                    Innertube.searchPage(query = name, params = Innertube.SearchFilter.Artist.value, fromMusicShelfRendererContent = Innertube.ArtistItem.Companion::from)
                        ?.getOrNull()?.items?.filterIsInstance<Innertube.ArtistItem>()?.firstOrNull()
                }
            }
            
            deferreds.forEach { d -> d.await()?.let { list.add(it) } }
            
            withContext(Dispatchers.Main) { 
                mainFeed = list
                isLoading = false 
            }
        }
    }

    // تزریق 3 آرتیست مشابه دقیقاً زیر آرتیست انتخاب شده
    fun fetchSimilarArtistsInline(parentArtist: Innertube.ArtistItem) {
        scope.launch(Dispatchers.IO) {
            val artistName = parentArtist.info?.name?.toString() ?: return@launch
            val songRes = Innertube.searchPage(query = artistName, params = Innertube.SearchFilter.Song.value, fromMusicShelfRendererContent = Innertube.SongItem.Companion::from)?.getOrNull()
            val firstSong = songRes?.items?.filterIsInstance<Innertube.SongItem>()?.firstOrNull()
            
            if (firstSong != null) {
                val related = Innertube.relatedPage(firstSong.key)?.getOrNull()
                // برداشتن ۳ تا آرتیست مشابه
                val simArtists = related?.artists?.filterIsInstance<Innertube.ArtistItem>()?.take(3) ?: emptyList()
                if (simArtists.isNotEmpty()) {
                    withContext(Dispatchers.Main) {
                        val index = mainFeed.indexOfFirst { it.key == parentArtist.key }
                        if (index != -1) {
                            val newList = mainFeed.toMutableList()
                            val uniqueSims = simArtists.filter { sim -> newList.none { it.key == sim.key } }
                            newList.addAll(index + 1, uniqueSims)
                            mainFeed = newList
                        }
                    }
                }
            }
        }
    }

    LaunchedEffect(query) {
        if (query.length > 1) {
            searchJob?.cancel()
            searchJob = launch(Dispatchers.IO) {
                delay(600)
                val result = Innertube.searchPage(query = query, params = Innertube.SearchFilter.Artist.value, fromMusicShelfRendererContent = Innertube.ArtistItem.Companion::from)?.getOrNull()
                val artists = result?.items?.filterIsInstance<Innertube.ArtistItem>() ?: emptyList()
                withContext(Dispatchers.Main) { searchResults = artists }
            }
        }
    }

    Scaffold(containerColor = bgColor, floatingActionButton = {
        AnimatedVisibility(visible = selectedArtists.size >= 3) {
            ExtendedFloatingActionButton(
                onClick = {
                    val prefs = context.getSharedPreferences("preferences", android.content.Context.MODE_PRIVATE)
                    prefs.edit().putBoolean("isOnboardingComplete", true).putString("onboardingSelectedArtists", selectedArtists.joinToString(",") { it.info?.name?.toString() ?: "" }).apply()
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
        Column(modifier = Modifier.fillMaxSize().padding(paddingValues).animateContentSize(tween(400))) {
            
            // تایتل اپلیکیشن در بالا
            Text(
                text = "Musick",
                fontSize = 32.sp,
                fontWeight = FontWeight.Bold,
                fontFamily = FontFamily.Serif,
                color = textColor,
                textAlign = TextAlign.Center,
                modifier = Modifier.fillMaxWidth().padding(top = 16.dp, bottom = 24.dp)
            )
            
            Text("Choose 3 or more artists you like.", fontSize = 24.sp, fontWeight = FontWeight.Bold, color = textColor, textAlign = TextAlign.Center, modifier = Modifier.fillMaxWidth().padding(horizontal = 24.dp))
            
            Spacer(modifier = Modifier.height(24.dp))
            
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
                Box(modifier = Modifier.fillMaxWidth().padding(32.dp), contentAlignment = Alignment.Center) {
                    CircularProgressIndicator(color = Color.White)
                }
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
                                    query = "" 
                                    fetchSimilarArtistsInline(artist)
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

// استخراج و فورس کردن رزولوشن بالا (1080p) برای کاورها
fun extractHighResUrl(rawThumb: String?): String {
    if (rawThumb == null) return ""
    var extracted = if (rawThumb.contains("url=")) {
        Regex("url=([^,)]+)").find(rawThumb)?.groupValues?.get(1) ?: rawThumb
    } else rawThumb
    extracted = if (extracted.startsWith("//")) "https:$extracted" else extracted
    // تبدیل اجباری پارامترهای سایز یوتیوب به بالاترین کیفیت
    return extracted.replace(Regex("=w\\\\d+-h\\\\d+"), "=w1080-h1080").replace(Regex("=s\\\\d+"), "=s1080")
}
"""
with open(fp_onb, "w") as f: f.write(code_onboarding)

# ۲. بازنویسی ViewModel برای New Releases (ترکیب آهنگ‌های جدید آرتیست‌های انتخاب شده)
fp_vm = "app/src/main/kotlin/com/github/soundpod/viewmodels/home/QuickPicksViewModel.kt"
if not os.path.exists(fp_vm): fp_vm = "app/src/main/kotlin/com/github/musick/viewmodels/home/QuickPicksViewModel.kt"

if os.path.exists(fp_vm):
    with open(fp_vm, "r") as f: code_vm = f.read()
    
    # پیدا کردن بلاک قبلی و جایگزینی با سیستم جدید که تمام آرتیست‌ها رو پردازش می‌کنه
    start_str = "val newReleasesDeferred = async {"
    end_str = "val relatedDeferreds = seedSongs.map"
    
    if start_str in code_vm and end_str in code_vm:
        before = code_vm.split(start_str)[0]
        after = end_str + code_vm.split(end_str)[1]
        
        new_block = """val newReleasesDeferred = async {
                    val onboardedPref = appContext.getSharedPreferences("preferences", android.content.Context.MODE_PRIVATE).getString("onboardingSelectedArtists", "") ?: ""
                    val artists = onboardedPref.split(",").filter { it.isNotBlank() }
                    
                    if (artists.isNotEmpty()) {
                        val fetchedSongs = mutableListOf<Innertube.SongItem>()
                        // برای جلوگیری از طولانی شدن لود، ۳ تا آرتیست رو به صورت رندوم برای آپدیت‌های جدید برمیداره
                        val targetArtists = artists.shuffled().take(3)
                        for (artist in targetArtists) {
                            val res = runCatching {
                                Innertube.searchPage(query = "$artist new music", params = Innertube.SearchFilter.Song.value, fromMusicShelfRendererContent = Innertube.SongItem.Companion::from)?.getOrNull()
                            }.getOrNull()
                            res?.items?.filterIsInstance<Innertube.SongItem>()?.let { fetchedSongs.addAll(it.take(5)) }
                        }
                        // شافل کردن تا میکس جذابی از ریلیزهای جدید به کاربر بده
                        fetchedSongs.shuffled()
                    } else {
                        runCatching {
                            val searchResult = Innertube.searchPage(query = "New Music Releases", params = Innertube.SearchFilter.Song.value, fromMusicShelfRendererContent = Innertube.SongItem.Companion::from)?.getOrNull()
                            searchResult?.items?.filterIsInstance<Innertube.SongItem>()
                        }.getOrNull()
                    }
                }
                """
        with open(fp_vm, "w") as f: f.write(before + new_block + after)

print("Updates injected successfully via Python script!")
