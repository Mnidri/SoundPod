import os

# ۱. اضافه کردن جریان زنده تاریخچه به ViewModel
viewmodel_file = "app/src/main/kotlin/com/github/soundpod/viewmodels/home/QuickPicksViewModel.kt"
if os.path.exists(viewmodel_file):
    with open(viewmodel_file, "r") as f: content = f.read()
    
    if "val recentHistoryFlow" not in content:
        content = content.replace("class QuickPicksViewModel : ViewModel() {", "class QuickPicksViewModel : ViewModel() {\n    val recentHistoryFlow = com.github.musick.db.lastPlayed(24)")
        with open(viewmodel_file, "w") as f: f.write(content)

# ۲. متصل کردن رابط کاربری Speed Dial به این جریان زنده
quick_picks = "app/src/main/kotlin/com/github/soundpod/ui/screens/home/QuickPicks.kt"
if os.path.exists(quick_picks):
    with open(quick_picks, "r") as f: content = f.read()
    
    # اطمینان از وجود ایمپورت‌های لازم
    if "import androidx.compose.runtime.collectAsState" not in content:
         content = content.replace("import androidx.compose.runtime.Composable", "import androidx.compose.runtime.Composable\nimport androidx.compose.runtime.collectAsState\nimport androidx.compose.runtime.remember")
    
    old_logic = """val speedDialItems = related.songs?.take(24)?.mapNotNull { song ->
                song.info?.endpoint?.videoId?.let { videoId ->
                    FeedItemMock(
                        id = videoId,
                        title = song.info?.name.orEmpty(),
                        subtitle = song.authors?.firstOrNull()?.name.orEmpty(),
                        thumbnailUrl = extractHighResUrlLocal(song.thumbnail?.url)
                    )
                }
            } ?: emptyList()"""
            
    new_logic = """// خواندن جریان زنده تاریخچه
            val recentHistory by viewModel.recentHistoryFlow.collectAsState(initial = emptyList())
            
            // ترکیب تاریخچه زنده با پیشنهادهای یوتیوب (اولویت با آهنگ‌های تازه پلی‌شده)
            val speedDialItems = remember(recentHistory, related.songs) {
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
            
    if "val recentHistory by viewModel.recentHistoryFlow" not in content:
        content = content.replace(old_logic, new_logic)
        with open(quick_picks, "w") as f: f.write(content)

print("Speed Dial is now reactive and real-time!")
