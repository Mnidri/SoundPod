import os

home_feeds = "app/src/main/kotlin/com/github/soundpod/ui/components/HomeFeeds.kt"
if os.path.exists(home_feeds):
    with open(home_feeds, "r") as f: content = f.read()
    # مربعی کردن کاورها
    content = content.replace(".aspectRatio(0.8f)", ".aspectRatio(1f)")
    # حذف فاصله بین دو متن
    content = content.replace("Spacer(modifier = Modifier.height(4.dp))", "")
    # کمی ظریف‌تر کردن سایز فونت برای جا شدن در مربع
    content = content.replace("fontSize = 15.sp,", "fontSize = 14.sp,")
    content = content.replace("fontSize = 11.sp,", "fontSize = 10.sp,")
    with open(home_feeds, "w") as f: f.write(content)

home_screen = "app/src/main/kotlin/com/github/soundpod/ui/screens/home/HomeScreen.kt"
if os.path.exists(home_screen):
    with open(home_screen, "r") as f: content = f.read()
    
    old_mock = """val mockItems = listOf(
                                        FeedItemMock("1", "Daily Mix 1", "Made for you", "https://picsum.photos/400/500"),
                                        FeedItemMock("2", "Discover Mix", "New tracks", "https://picsum.photos/401/500"),
                                        FeedItemMock("3", "Release Radar", "Fresh out", "https://picsum.photos/402/500"),
                                        FeedItemMock("4", "Your Top Songs", "Favorites", "https://picsum.photos/403/500"),
                                        FeedItemMock("5", "Chill Vibes", "Relaxing", "https://picsum.photos/404/500"),
                                        FeedItemMock("6", "Workout", "High energy", "https://picsum.photos/405/500")
                                    )"""
    
    # داینامیک کردن برای ساخت ۲۴ کاور تصادفی و با کیفیت
    new_mock = """val mockItems = (1..24).map { 
                                        FeedItemMock(it.toString(), "Mix $it", "Recommended", "https://picsum.photos/500/500?random=$it") 
                                    }"""
    
    content = content.replace(old_mock, new_mock)
    with open(home_screen, "w") as f: f.write(content)

print("UI fixes applied successfully!")
