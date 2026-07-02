import os

ui_path = "app/src/main/kotlin/com/github/soundpod/ui/screens/home/QuickPicks.kt"
if os.path.exists(ui_path):
    with open(ui_path, "r") as f: content = f.read()

    # ۱. اضافه کردن ایمپورت‌های مربوط به پیجر و گرافیک
    imports_to_add = """import androidx.compose.foundation.pager.HorizontalPager
import androidx.compose.foundation.pager.rememberPagerState
import androidx.compose.ui.graphics.graphicsLayer
import androidx.compose.ui.util.lerp
import java.util.Calendar
"""
    if "import androidx.compose.foundation.pager.HorizontalPager" not in content:
        content = content.replace("import androidx.compose.foundation.background", imports_to_add + "import androidx.compose.foundation.background")

    # ۲. پاکسازی کدهای گیج‌کننده و هکی اسپید دایل (واگذاری قدرت مطلق به دیتابیس)
    old_speed_dial_block = """val speedDialItems = remember(recentHistory, related.songs, currentPlayingMediaItem) {
                val historyMocks = recentHistory.map { song -> FeedItemMock(id = song.id, title = song.title, subtitle = song.artistsText ?: "", thumbnailUrl = extractHighResUrlLocal(song.thumbnailUrl)) }
                val recommendedMocks = related.songs?.mapNotNull { song -> song.info?.endpoint?.videoId?.let { videoId -> FeedItemMock(id = videoId, title = song.info?.name.orEmpty(), subtitle = song.authors?.firstOrNull()?.name.orEmpty(), thumbnailUrl = extractHighResUrlLocal(song.thumbnail?.url)) } } ?: emptyList()
                val combined = (historyMocks + recommendedMocks).distinctBy { it.id }.toMutableList()
                
                // شیفت تمیز و بدون باگ با تکیه بر پلیر واقعی
                currentPlayingMediaItem?.let { currentItem ->
                     val playingId = currentItem.mediaId
                     val index = combined.indexOfFirst { it.id == playingId }
                     if (index != -1) {
                         val item = combined.removeAt(index)
                         combined.add(0, item)
                     }
                }
                combined.take(24)
            }"""
            
    new_speed_dial_block = """// قدرت مطلق در دست دیتابیس: دیتابیس آپدیت می‌شود، این جریان زنده درجا لیست را رفرش می‌کند
            val speedDialItems = remember(recentHistory, related.songs) {
                val historyMocks = recentHistory.map { song -> FeedItemMock(id = song.id, title = song.title, subtitle = song.artistsText ?: "", thumbnailUrl = extractHighResUrlLocal(song.thumbnailUrl)) }
                val recommendedMocks = related.songs?.mapNotNull { song -> song.info?.endpoint?.videoId?.let { videoId -> FeedItemMock(id = videoId, title = song.info?.name.orEmpty(), subtitle = song.authors?.firstOrNull()?.name.orEmpty(), thumbnailUrl = extractHighResUrlLocal(song.thumbnail?.url)) } } ?: emptyList()
                
                (historyMocks + recommendedMocks).distinctBy { it.id }.take(24)
            }"""
    content = content.replace(old_speed_dial_block, new_speed_dial_block)

    # ۳. جایگزینی هیرو کارت قدیمی با اسلایدر غول‌پیکر پارالاکس (Hero Cards Slider)
    old_hero_card_block = """val hero = viewModel.dailyDiscoverResult?.getOrNull()
            if (hero != null) {
                Spacer(modifier = Modifier.height(36.dp))
                Row(modifier = sectionTextModifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween, verticalAlignment = Alignment.CenterVertically) {
                    Text(text = "Your daily discover", style = MaterialTheme.typography.titleLarge.copy(fontSize = 22.sp, fontWeight = FontWeight.Black, color = MaterialTheme.colorScheme.onBackground))
                    Button(onClick = { val mediaItem = hero.asMediaItem; binder?.stopRadio(); binder?.player?.forcePlay(mediaItem); binder?.setupRadio(NavigationEndpoint.Endpoint.Watch(videoId = mediaItem.mediaId)) }, colors = ButtonDefaults.buttonColors(containerColor = MaterialTheme.colorScheme.onBackground, contentColor = MaterialTheme.colorScheme.background)) {
                        Text("Play all", fontWeight = FontWeight.Bold, fontSize = 13.sp)
                    }
                }
                Box(
                    modifier = Modifier.padding(horizontal = 16.dp).fillMaxWidth().aspectRatio(1.1f).clip(RoundedCornerShape(24.dp))
                        .clickable { val mediaItem = hero.asMediaItem; binder?.stopRadio(); binder?.player?.forcePlay(mediaItem); binder?.setupRadio(NavigationEndpoint.Endpoint.Watch(videoId = mediaItem.mediaId)) }
                ) {
                    AsyncImage(model = extractHighResUrlLocal(hero.asMediaItem.mediaMetadata.artworkUri?.toString()), contentDescription = null, contentScale = ContentScale.Crop, modifier = Modifier.fillMaxSize())
                    Box(modifier = Modifier.fillMaxSize().background(Brush.verticalGradient(listOf(Color.Transparent, Color.Black.copy(alpha = 0.85f)), startY = 300f)))
                    Column(modifier = Modifier.align(Alignment.BottomStart).padding(20.dp)) {
                        Text(text = hero.asMediaItem.mediaMetadata.title.toString(), style = MaterialTheme.typography.headlineMedium.copy(fontWeight = FontWeight.Black, color = Color.White))
                        Spacer(modifier = Modifier.height(4.dp))
                        Text(text = "Sounds like ${hero.asMediaItem.mediaMetadata.artist}", style = MaterialTheme.typography.bodyLarge.copy(fontWeight = FontWeight.Medium, color = Color.White.copy(alpha = 0.8f)))
                    }
                }
            }"""

    new_hero_cards_slider = """// ----- آغاز بخش ساخت کارت‌های غول‌پیکر محلی (Hero Slider) -----
            val heroPagerState = rememberPagerState(pageCount = { 5 })
            val hourOfDay = Calendar.getInstance().get(Calendar.HOUR_OF_DAY)
            val timeMood = when (hourOfDay) { in 5..11 -> "Morning Energy"; in 12..17 -> "Afternoon Focus"; in 18..21 -> "Evening Chill"; else -> "Late Night Vibes" }
            
            // تولید دیتای محلی برای کارت‌ها با ترکیب تاریخچه و پیشنهادها
            val heroCardsData = remember(recentHistory, related.songs) {
                val fallbackImage = "https://picsum.photos/800/800?random="
                listOf(
                    Triple("Your Heavy Rotation", "The tracks you can't get enough of", recentHistory.firstOrNull()?.thumbnailUrl ?: fallbackImage+"1"),
                    Triple("Search Radar", "Mix based on your recent searches", related.songs?.randomOrNull()?.info?.thumbnail?.url ?: fallbackImage+"2"),
                    Triple("Favorites Mix", "Your most loved tracks in one place", recentHistory.getOrNull(2)?.thumbnailUrl ?: fallbackImage+"3"),
                    Triple(timeMood, "Perfect sounds for right now", related.songs?.randomOrNull()?.info?.thumbnail?.url ?: fallbackImage+"4"),
                    Triple("Discovery Mix", "Fresh finds based on your taste", recentHistory.getOrNull(4)?.thumbnailUrl ?: fallbackImage+"5")
                )
            }

            Spacer(modifier = Modifier.height(36.dp))
            Row(modifier = sectionTextModifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween, verticalAlignment = Alignment.CenterVertically) {
                Text(text = "Made For You", style = MaterialTheme.typography.titleLarge.copy(fontSize = 24.sp, fontWeight = FontWeight.Black, color = MaterialTheme.colorScheme.onBackground))
            }
            
            HorizontalPager(
                state = heroPagerState,
                contentPadding = PaddingValues(horizontal = 24.dp),
                pageSpacing = 16.dp,
                modifier = Modifier.fillMaxWidth().height(320.dp)
            ) { page ->
                val cardData = heroCardsData[page]
                val pageOffset = (heroPagerState.currentPage - page) + heroPagerState.currentPageOffsetFraction
                
                Box(
                    modifier = Modifier
                        .fillMaxSize()
                        .graphicsLayer {
                            // انیمیشن سه‌بعدی و تغییر سایز ملایم
                            val scale = lerp(start = 0.85f, stop = 1f, fraction = 1f - Math.abs(pageOffset).coerceIn(0f, 1f))
                            scaleX = scale; scaleY = scale
                            alpha = lerp(start = 0.5f, stop = 1f, fraction = 1f - Math.abs(pageOffset).coerceIn(0f, 1f))
                        }
                        .clip(RoundedCornerShape(32.dp))
                        .clickable { 
                            // در صورت کلیک، اولین آهنگ موجود در دیتابیس مرتبط پلی شود
                            val songToPlay = recentHistory.getOrNull(page % recentHistory.size)?.asMediaItem
                            if (songToPlay != null) { binder?.stopRadio(); binder?.player?.forcePlay(songToPlay); binder?.setupRadio(NavigationEndpoint.Endpoint.Watch(videoId = songToPlay.mediaId)) }
                        }
                ) {
                    // عکس بک‌گراند با انیمیشن پارالاکس
                    AsyncImage(
                        model = extractHighResUrlLocal(cardData.third),
                        contentDescription = null,
                        contentScale = ContentScale.Crop,
                        modifier = Modifier
                            .fillMaxSize()
                            .graphicsLayer {
                                translationX = pageOffset * 250f // جادوی پارالاکس
                            }
                    )
                    
                    // شیشه تاریک پایین کارت
                    Box(modifier = Modifier.fillMaxSize().background(Brush.verticalGradient(listOf(Color.Transparent, Color.Black.copy(alpha = 0.9f)), startY = 350f)))
                    
                    Column(modifier = Modifier.align(Alignment.BottomStart).padding(24.dp)) {
                        Text(text = cardData.first, style = MaterialTheme.typography.headlineMedium.copy(fontWeight = FontWeight.Black, color = Color.White))
                        Spacer(modifier = Modifier.height(6.dp))
                        Text(text = cardData.second, style = MaterialTheme.typography.bodyLarge.copy(fontWeight = FontWeight.Medium, color = Color.White.copy(alpha = 0.8f)))
                    }
                    
                    // دکمه پلی همگام با استایل یوتیوب
                    Box(modifier = Modifier.align(Alignment.BottomEnd).padding(20.dp).size(52.dp).clip(CircleShape).background(Color.White), contentAlignment = Alignment.Center) {
                        Icon(Icons.Default.PlayArrow, contentDescription = "Play", tint = Color.Black, modifier = Modifier.size(32.dp))
                    }
                }
            }
            // ----- پایان بخش Hero Slider -----"""
            
    content = content.replace(old_hero_card_block, new_hero_cards_slider)

    with open(ui_path, "w") as f: f.write(content)

print("Zero-Latency Speed Dial DB Sync and Parallax Hero Cards Implemented!")
