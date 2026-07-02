import os

path = "app/src/main/kotlin/com/github/soundpod/viewmodels/home/QuickPicksViewModel.kt"
if os.path.exists(path):
    with open(path, "r") as f: content = f.read()

    start_str = "val newReleasesDeferred = async<List<Innertube.SongItem>?>"
    start_idx = content.find(start_str)
    end_str = "val relatedDeferreds ="
    end_idx = content.find(end_str, start_idx)

    if start_idx != -1 and end_idx != -1:
        new_logic = """val newReleasesDeferred = async<List<Innertube.SongItem>?> {
                    var interleaved: List<Innertube.SongItem>? = null
                    try {
                        // دریافت خالص دیتا از ۴ ستون دیتابیس
                        val historySongs = runCatching { com.github.musick.db.lastPlayed(100).first() }.getOrNull() ?: emptyList()
                        val favSongs = runCatching { com.github.musick.db.favorites().first() }.getOrNull() ?: emptyList()
                        val searchQueries = runCatching { com.github.musick.db.queries("").first() }.getOrNull() ?: emptyList()

                        // استخراج متن و نام خواننده‌ها
                        val historyArtists = historySongs.mapNotNull { it.artistsText }.flatMap { it.split(Regex(" & |, | x | • ")) }
                        val favArtists = favSongs.mapNotNull { it.artistsText }.flatMap { it.split(Regex(" & |, | x | • ")) }
                        val searchTexts = searchQueries.map { it.toString() }.flatMap { it.split(" ") }

                        val onboardedPref = appContext.getSharedPreferences("preferences", android.content.Context.MODE_PRIVATE).getString("onboardingSelectedArtists", "") ?: ""
                        val onboardedArtists = onboardedPref.split(",")

                        // ساخت سوپرفیلتر قدرتمند سلیقه
                        val myLovedArtists = (historyArtists + favArtists + onboardedArtists + searchTexts)
                            .map { it.trim().lowercase() }
                            .filter { it.length > 2 }
                            .toSet()

                        // دریافت ۱۰۰ آهنگ جدید گلوبال از شاهرگ یوتیوب موزیک
                        val exploreRes = runCatching { Innertube.searchPage(query = "FEmusic_new_releases", params = "", fromMusicShelfRendererContent = Innertube.SongItem.Companion::from)?.getOrNull() }.getOrNull()
                        val globalNewReleases = exploreRes?.items?.filterIsInstance<Innertube.SongItem>() ?: emptyList()

                        if (myLovedArtists.isNotEmpty() && globalNewReleases.isNotEmpty()) {
                            // اعمال سوپرفیلتر روی آهنگ‌های جدید
                            val filteredSongs = globalNewReleases.filter { song ->
                                val songArtist = song.asMediaItem.mediaMetadata.artist?.toString()?.lowercase() ?: ""
                                val songTitle = song.asMediaItem.mediaMetadata.title?.toString()?.lowercase() ?: ""
                                myLovedArtists.any { beloved -> songArtist.contains(beloved) || songTitle.contains(beloved) }
                            }
                            interleaved = if (filteredSongs.isNotEmpty()) filteredSongs.distinctBy { it.key } else globalNewReleases.take(8)
                        } else {
                            interleaved = globalNewReleases.take(8)
                        }
                    } catch (e: Exception) { e.printStackTrace() }
                    interleaved
                }
                """
        content = content[:start_idx] + new_logic + content[end_idx:]
        with open(path, "w") as f: f.write(content)
        print("4-Pillar Super Filter Injected Successfully!")
