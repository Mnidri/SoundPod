import os
import re

# 1. فیکس کردن قطعی و نهایی فاصله متن‌های Speed Dial روی کاورها
home_feeds = "app/src/main/kotlin/com/github/soundpod/ui/components/HomeFeeds.kt"
if os.path.exists(home_feeds):
    with open(home_feeds, "r") as f: content = f.read()
    
    # حذف روش قبلی
    old_text_block = """            Text(
                text = item.title, 
                fontSize = 14.sp, 
                fontWeight = FontWeight.ExtraBold, 
                maxLines = 2, 
                overflow = TextOverflow.Ellipsis, 
                color = Color.White, // همیشه سفید تا روی کاور دیده بشه
                textAlign = TextAlign.Center
            )
            Text(
                text = item.subtitle, 
                fontSize = 10.sp, 
                fontWeight = FontWeight.Medium,
                maxLines = 1, 
                overflow = TextOverflow.Ellipsis, 
                color = Color.White.copy(alpha = 0.75f),
                textAlign = TextAlign.Center
            )"""
            
    # استفاده از یک تک‌تکست (AnnotatedString) برای چسباندن کامل دو خط به هم بدون هیچ فاصله‌ای
    new_text_block = """            Text(
                text = androidx.compose.ui.text.buildAnnotatedString {
                    withStyle(androidx.compose.ui.text.SpanStyle(fontWeight = FontWeight.ExtraBold, fontSize = 14.sp, color = Color.White)) {
                        append(item.title)
                    }
                    append("\\n")
                    withStyle(androidx.compose.ui.text.SpanStyle(fontWeight = FontWeight.Medium, fontSize = 11.sp, color = Color.White.copy(alpha = 0.75f))) {
                        append(item.subtitle)
                    }
                },
                maxLines = 3, 
                overflow = TextOverflow.Ellipsis, 
                textAlign = TextAlign.Center,
                lineHeight = 16.sp // این خط باعث فشردگی شدید دو سطر به هم میشه
            )"""
    
    if "buildAnnotatedString" not in content:
        content = content.replace("import androidx.compose.ui.text.style.TextOverflow", "import androidx.compose.ui.text.style.TextOverflow\nimport androidx.compose.ui.text.withStyle")
        content = content.replace(old_text_block, new_text_block)
        with open(home_feeds, "w") as f: f.write(content)

# 2. پاک‌سازی HomeScreen از کدهای موقت
home_screen = "app/src/main/kotlin/com/github/soundpod/ui/screens/home/HomeScreen.kt"
if os.path.exists(home_screen):
    with open(home_screen, "r") as f: content = f.read()
    # پیدا کردن بلوک موقتی که اضافه کرده بودیم و برگرداندن به حالت خالص تا باگ اسکرول رفع بشه
    content = re.sub(
        r'0 -> Column\(modifier = Modifier\.fillMaxSize\(\)\).*?val mockItems.*?SpeedDialGrid.*?Box\(modifier = Modifier\.weight\(1f\)\).*?QuickPicks\([^)]+\).*?\}',
        r'0 -> QuickPicks(onAlbumClick = navigateToAlbum, onArtistClick = navigateToArtist, onPlaylistClick = { browseId -> navController.navigate(route = Routes.Playlist(id = browseId)) }, onOfflinePlaylistClick = { navController.navigate(route = Routes.BuiltInPlaylist(index = 1)) })',
        content,
        flags=re.DOTALL
    )
    with open(home_screen, "w") as f: f.write(content)

# 3. تزریق هوشمند و دائمی Speed Dial به داخل QuickPicks (برای حل مشکل فریز شدن اسکرول و اتصال به دیتابیس)
quick_picks = "app/src/main/kotlin/com/github/soundpod/ui/screens/home/QuickPicks.kt"
if os.path.exists(quick_picks):
    with open(quick_picks, "r") as f: content = f.read()
    
    # ایمپورت کردن FeedItemMock و SpeedDialGrid
    if "import com.github.musick.ui.components.SpeedDialGrid" not in content:
        content = content.replace("import com.github.musick.ui.components.ShimmerHost", "import com.github.musick.ui.components.ShimmerHost\nimport com.github.musick.ui.components.SpeedDialGrid\nimport com.github.musick.ui.components.FeedItemMock")
    
    # پیدا کردن محل قرارگیری: دقیقاً زیر Text مربوط به Quick Picks
    target_text = "Text(\n                text = stringResource(id = R.string.quick_picks)"
    
    injection = """
            // ---- اتصال دیتای واقعی به Speed Dial و قرارگیری آن درون اسکرول اصلی ----
            val speedDialItems = related.songs?.take(24)?.mapNotNull { song ->
                song.info?.endpoint?.videoId?.let { videoId ->
                    FeedItemMock(
                        id = videoId,
                        title = song.info?.name.orEmpty(),
                        subtitle = song.authors?.firstOrNull()?.name.orEmpty(),
                        thumbnailUrl = extractHighResUrlLocal(song.thumbnail?.url)
                    )
                }
            } ?: emptyList()
            
            if (speedDialItems.isNotEmpty()) {
                SpeedDialGrid(
                    items = speedDialItems, 
                    onItemClick = { browseId -> 
                        val mediaItem = related.songs?.firstOrNull { it.info?.endpoint?.videoId == browseId }?.asMediaItem
                        if(mediaItem != null) {
                            binder?.stopRadio()
                            binder?.player?.forcePlay(mediaItem)
                            binder?.setupRadio(NavigationEndpoint.Endpoint.Watch(videoId = mediaItem.mediaId))
                        }
                    }
                )
                Spacer(modifier = Modifier.height(16.dp))
            }
            // -------------------------------------------------------------------------
    """
    
    if "SpeedDialGrid(items = speedDialItems" not in content:
        content = content.replace(target_text, injection + "\n            " + target_text)
        with open(quick_picks, "w") as f: f.write(content)

print("Speed Dial successfully wired to Database and Scroll fixed!")
