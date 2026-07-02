import os

def fix_file(path):
    if not os.path.exists(path): return
    with open(path, "r") as f: content = f.read()

    # ۱. اضافه کردن ابزار تشخیص روشنایی رنگ به ایمپورت‌ها
    if "import androidx.compose.ui.graphics.luminance" not in content:
        content = content.replace("import androidx.compose.ui.graphics.*", "import androidx.compose.ui.graphics.*\nimport androidx.compose.ui.graphics.luminance")
        content = content.replace("import androidx.compose.ui.graphics.Color", "import androidx.compose.ui.graphics.Color\nimport androidx.compose.ui.graphics.luminance")

    # ۲. مستقل کردن تم اپلیکیشن از سیستم‌عامل گوشی با بررسی مستقیم بک‌گراند
    content = content.replace("androidx.compose.foundation.isSystemInDarkTheme()", "androidx.compose.material3.MaterialTheme.colorScheme.background.luminance() < 0.5f")

    # ۳. اصلاح شفافیت لایه‌های لایت‌مود دقیقاً مشابه دارک‌مود
    if "HomeScreen" in path:
        content = content.replace("Color.White.copy(alpha = 0.98f)", "Color.White.copy(alpha = 0.75f)")
        content = content.replace("val innerGlassColor = if (isDark) Color.Black.copy(alpha = 0.90f) else Color.White", "val innerGlassColor = if (isDark) Color.Black.copy(alpha = 0.90f) else Color.White.copy(alpha = 0.90f)")

    with open(path, "w") as f: f.write(content)

fix_file("app/src/main/kotlin/com/github/soundpod/ui/screens/home/HomeScreen.kt")
fix_file("app/src/main/kotlin/com/github/soundpod/ui/screens/artist/ArtistScreen.kt")
