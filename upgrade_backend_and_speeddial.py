import os

# ۱. آپدیت مغز اپلیکیشن (ViewModel) برای گرفتن دیتای کارت غول‌پیکر و تازه‌های رسمی
vm_path = "app/src/main/kotlin/com/github/soundpod/viewmodels/home/QuickPicksViewModel.kt"
if os.path.exists(vm_path):
    with open(vm_path, "r") as f: content = f.read()
    
    # اضافه کردن متغیر Hero Card
    if "var dailyDiscoverResult" not in content:
        content = content.replace(
            "var newReleasesResult: Result<List<Innertube.SongItem>>? by mutableStateOf(null)",
            "var newReleasesResult: Result<List<Innertube.SongItem>>? by mutableStateOf(null)\n    var dailyDiscoverResult: Result<Innertube.SongItem>? by mutableStateOf(null)"
        )
    
    # بهبود منطقِ گرفتن آهنگ‌ها (استخراج دیتای خالص یوتیوب)
    old_new_releases_logic = "val fallbackRes = runCatching { Innertube.searchPage(query = \"New Music Releases\", params = Innertube.SearchFilter.Song.value, fromMusicShelfRendererContent = Innertube.SongItem.Companion::from)?.getOrNull() }.getOrNull()"
    new_releases_logic = """
                    // گرفتن دیتای رسمی و باکیفیت برای New Releases و Hero Card
                    val recommendations = runCatching { Innertube.recommendations()?.getOrNull() }.getOrNull()
                    val hero = recommendations?.filterIsInstance<Innertube.SongItem>()?.firstOrNull()
                    if (hero != null) dailyDiscoverResult = Result.success(hero)
                    
                    val fallbackRes = runCatching { Innertube.searchPage(query = "Latest global single releases", params = Innertube.SearchFilter.Song.value, fromMusicShelfRendererContent = Innertube.SongItem.Companion::from)?.getOrNull() }.getOrNull()
    """
    if "val hero =" not in content:
        content = content.replace(old_new_releases_logic, new_releases_logic)
        
    with open(vm_path, "w") as f: f.write(content)

# ۲. تزریق سرعت رعدآسا به Speed Dial در رابط کاربری
ui_path = "app/src/main/kotlin/com/github/soundpod/ui/screens/home/QuickPicks.kt"
if os.path.exists(ui_path):
    with open(ui_path, "r") as f: content = f.read()
    
    # اضافه کردن حافظه موقت لمس (instantPlayId)
    if "var instantPlayId by remember { mutableStateOf<String?>(null) }" not in content:
        content = content.replace(
            "val quickPicksCustomGenre by rememberPreference(quickPicksCustomGenreKey, \"Psaltic music\")",
            "val quickPicksCustomGenre by rememberPreference(quickPicksCustomGenreKey, \"Psaltic music\")\n    var instantPlayId by androidx.compose.runtime.remember { androidx.compose.runtime.mutableStateOf<String?>(null) }"
        )
    
    # تغییر منطق ساخت Speed Dial برای آوردن آهنگ کلیک شده به رتبه ۱
    old_speed_dial_logic = """val speedDialItems = remember(recentHistory, related.songs) {
                val historyMocks = recentHistory.map { song ->
                    FeedItemMock(id = song.id, title = song.title, subtitle = song.artistsText ?: "", thumbnailUrl = extractHighResUrlLocal(song.thumbnailUrl))
                }
                val recommendedMocks = related.songs?.mapNotNull { song ->
                    song.info?.endpoint?.videoId?.let { videoId ->
                        FeedItemMock(id = videoId, title = song.info?.name.orEmpty(), subtitle = song.authors?.firstOrNull()?.name.orEmpty(), thumbnailUrl = extractHighResUrlLocal(song.thumbnail?.url))
                    }
                } ?: emptyList()
                
                // ادغام، حذف تکراری‌ها و نگه داشتن دقیق ۲۴ آیتم
                (historyMocks + recommendedMocks).distinctBy { it.id }.take(24)
            }"""
            
    new_speed_dial_logic = """val speedDialItems = androidx.compose.runtime.remember(recentHistory, related.songs, instantPlayId) {
                val historyMocks = recentHistory.map { song ->
                    FeedItemMock(id = song.id, title = song.title, subtitle = song.artistsText ?: "", thumbnailUrl = extractHighResUrlLocal(song.thumbnailUrl))
                }
                val recommendedMocks = related.songs?.mapNotNull { song ->
                    song.info?.endpoint?.videoId?.let { videoId ->
                        FeedItemMock(id = videoId, title = song.info?.name.orEmpty(), subtitle = song.authors?.firstOrNull()?.name.orEmpty(), thumbnailUrl = extractHighResUrlLocal(song.thumbnail?.url))
                    }
                } ?: emptyList()
                
                val combined = (historyMocks + recommendedMocks).distinctBy { it.id }.toMutableList()
                
                // جادوی سرعت: اگر آهنگی کلیک شده، در کسری از ثانیه بکشش اول لیست!
                instantPlayId?.let { clickedId ->
                    val index = combined.indexOfFirst { it.id == clickedId }
                    if (index != -1) {
                        val item = combined.removeAt(index)
                        combined.add(0, item)
                    }
                }
                
                combined.take(24)
            }"""
            
    if "instantPlayId?.let" not in content:
        content = content.replace(old_speed_dial_logic, new_speed_dial_logic)
        
        # متصل کردن همه کلیک‌ها به این حافظه موقت
        content = content.replace("binder?.player?.forcePlay(mediaItem)", "instantPlayId = mediaItem.mediaId\n                            binder?.player?.forcePlay(mediaItem)")
        
        with open(ui_path, "w") as f: f.write(content)

print("Backend Upgraded & Speed Dial Reactivity Fixed!")
