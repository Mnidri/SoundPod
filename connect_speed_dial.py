import os

home_file = "app/src/main/kotlin/com/github/soundpod/ui/screens/home/HomeScreen.kt"

if os.path.exists(home_file):
    with open(home_file, "r") as f:
        content = f.read()
    
    # پیدا کردن خط مربوط به رندر صفحه اول و جایگزینی آن با ساختار جدید
    old_target = "0 -> QuickPicks(onAlbumClick = navigateToAlbum, onArtistClick = navigateToArtist, onPlaylistClick = { browseId -> navController.navigate(route = Routes.Playlist(id = browseId)) }, onOfflinePlaylistClick = { navController.navigate(route = Routes.BuiltInPlaylist(index = 1)) })"
    
    new_target = """0 -> Column(modifier = Modifier.fillMaxSize()) {
                                    val mockItems = listOf(
                                        FeedItemMock("1", "Daily Mix 1", "Made for you", "https://picsum.photos/400/500"),
                                        FeedItemMock("2", "Discover Mix", "New tracks", "https://picsum.photos/401/500"),
                                        FeedItemMock("3", "Release Radar", "Fresh out", "https://picsum.photos/402/500"),
                                        FeedItemMock("4", "Your Top Songs", "Favorites", "https://picsum.photos/403/500"),
                                        FeedItemMock("5", "Chill Vibes", "Relaxing", "https://picsum.photos/404/500"),
                                        FeedItemMock("6", "Workout", "High energy", "https://picsum.photos/405/500")
                                    )
                                    SpeedDialGrid(items = mockItems, onItemClick = {})
                                    Box(modifier = Modifier.weight(1f)) {
                                        QuickPicks(onAlbumClick = navigateToAlbum, onArtistClick = navigateToArtist, onPlaylistClick = { browseId -> navController.navigate(route = Routes.Playlist(id = browseId)) }, onOfflinePlaylistClick = { navController.navigate(route = Routes.BuiltInPlaylist(index = 1)) })
                                    }
                                }"""
    
    # جایگزینی دقیق
    content = content.replace(old_target, new_target)
    
    with open(home_file, "w") as f:
        f.write(content)
    print("Speed Dial successfully connected to HomeScreen!")
