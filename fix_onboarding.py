import os, re

# ۱. اصلاح لوگوی هوم اسکرین (سایز ۳۶ + سایه نرم)
fp_home = "app/src/main/kotlin/com/github/soundpod/ui/screens/home/HomeScreen.kt"
if not os.path.exists(fp_home): fp_home = "app/src/main/kotlin/com/github/musick/ui/screens/home/HomeScreen.kt"

if os.path.exists(fp_home):
    with open(fp_home, "r") as f: code = f.read()
    new_title = """title = { 
                    Text(
                        text = "Musick", 
                        fontSize = 36.sp, 
                        fontWeight = FontWeight.Bold, 
                        fontFamily = FontFamily.Serif, 
                        letterSpacing = (-1).sp, 
                        color = textColor,
                        style = androidx.compose.ui.text.TextStyle(
                            shadow = androidx.compose.ui.graphics.Shadow(
                                color = textColor.copy(alpha = 0.5f), 
                                blurRadius = 24f
                            )
                        )
                    ) 
                },"""
    code = re.sub(r"title = \{.*?\n.*?\n.*?\},", new_title, code, flags=re.DOTALL)
    with open(fp_home, "w") as f: f.write(code)

# ۲. بازنویسی کامل Onboarding (بک‌گراند مشکی مطلق، لود هوشمند کاورها و اضافه‌شدن آرتیست‌ها به پایین لیست)
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

    val bgColor = Color.Black // مشکی مطلق AMOLED
    val textColor = Color.White

    LaunchedEffect(Unit) {
        scope.launch(Dispatchers.IO) {
            val topNames = listOf("The Weeknd", "Amir Tataloo", "Drake", "Shadmehr Aghili", "Travis Scott", "Reza Pishro")
            val list = mutableListOf<Innertube.ArtistItem>()
            for (name in topNames) {
                val res = Innertube.searchPage(query = name, params = Innertube.SearchFilter.Artist.value, fromMusicShelfRendererContent = Innertube.ArtistItem.Companion::from)?.getOrNull()
                res?.items?.filterIsInstance<Innertube.ArtistItem>()?.firstOrNull()?.let { list.add(it) }
            }
            withContext(Dispatchers.Main) { 
                mainFeed = list
                isLoading = false 
            }
        }
    }

    fun fetchSimilarArtists(artistName: String) {
        scope.launch(Dispatchers.IO) {
            val songRes = Innertube.searchPage(query = artistName, params = Innertube.SearchFilter.Song.value, fromMusicShelfRendererContent = Innertube.SongItem.Companion::from)?.getOrNull()
            val firstSong = songRes?.items?.filterIsInstance<Innertube.SongItem>()?.firstOrNull()
            
            if (firstSong != null) {
                val related = Innertube.relatedPage(firstSong.key)?.getOrNull()
                val simArtists = related?.artists?.filterIsInstance<Innertube.ArtistItem>() ?: emptyList()
                if (simArtists.isNotEmpty()) {
                    withContext(Dispatchers.Main) {
                        // افزودن به انتهای لیست (بدون جایگزینی قبلی‌ها)
                        mainFeed = (mainFeed + simArtists).distinctBy { it.key }
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
        AnimatedVisibility(visible = selectedArtists.isNotEmpty()) {
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
            Spacer(modifier = Modifier.height(40.dp))
            Text("Choose artists you like.", fontSize = 28.sp, fontWeight = FontWeight.Black, color = textColor, textAlign = TextAlign.Center, modifier = Modifier.fillMaxWidth().padding(horizontal = 24.dp))
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
                                AsyncImage(model = extractUrl(artist.thumbnail?.toString()), contentDescription = null, modifier = Modifier.fillMaxSize(), contentScale = ContentScale.Crop)
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
                                    fetchSimilarArtists(artist.info?.name?.toString() ?: "")
                                } 
                            }
                        ) {
                            Box(contentAlignment = Alignment.Center, modifier = Modifier.fillMaxWidth().aspectRatio(1f)) {
                                Box(modifier = Modifier.fillMaxSize().clip(CircleShape).background(Color(0xFF1E1E1E)))
                                AsyncImage(
                                    model = extractUrl(artist.thumbnail?.toString()), 
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

fun extractUrl(rawThumb: String?): String {
    if (rawThumb == null) return ""
    val extracted = if (rawThumb.contains("url=")) {
        Regex("url=([^,)]+)").find(rawThumb)?.groupValues?.get(1) ?: rawThumb
    } else rawThumb
    return if (extracted.startsWith("//")) "https:$extracted" else extracted
}
"""
with open(fp_onb, "w") as f: f.write(code_onboarding)

# ۳. جایگذاری امن و هوشمندِ آرتیست‌های کاربر در بخش New Releases
fp_vm = "app/src/main/kotlin/com/github/soundpod/viewmodels/home/QuickPicksViewModel.kt"
if not os.path.exists(fp_vm): fp_vm = "app/src/main/kotlin/com/github/musick/viewmodels/home/QuickPicksViewModel.kt"

if os.path.exists(fp_vm):
    with open(fp_vm, "r") as f: code_vm = f.read()
    
    old_release_block = 'val searchResult = Innertube.searchPage(query = "New Music Releases", params = Innertube.SearchFilter.Song.value, fromMusicShelfRendererContent = Innertube.SongItem.Companion::from)?.getOrNull()'
    
    # استفاده از سینتکس امن بدون درگیری با کاراکترهای بش
    new_release_block = """val onboardedPref = appContext.getSharedPreferences("preferences", android.content.Context.MODE_PRIVATE).getString("onboardingSelectedArtists", "") ?: ""
                        val releaseQuery = if (onboardedPref.isNotBlank()) {
                            val artists = onboardedPref.split(",")
                            val randomArtist = artists.randomOrNull() ?: ""
                            randomArtist + " new songs"
                        } else {
                            "New Music Releases"
                        }
                        val searchResult = Innertube.searchPage(query = releaseQuery, params = Innertube.SearchFilter.Song.value, fromMusicShelfRendererContent = Innertube.SongItem.Companion::from)?.getOrNull()"""
    
    if old_release_block in code_vm:
        code_vm = code_vm.replace(old_release_block, new_release_block)
        with open(fp_vm, "w") as f: f.write(code_vm)

print("All features implemented safely!")
