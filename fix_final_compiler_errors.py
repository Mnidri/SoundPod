import os
import re

# ۱. جایگزینی با آدرس مطلق برای رفع ارور Dark Theme بدون نیاز به ایمپورت
tab_files = [
    "app/src/main/kotlin/com/github/soundpod/ui/components/HorizontalTabs.kt",
    "app/src/main/kotlin/com/github/soundpod/ui/screens/artist/ArtistScreen.kt"
]

for fp in tab_files:
    if os.path.exists(fp):
        with open(fp, "r") as f: content = f.read()
        
        # پاکسازی ایمپورت‌های احتمالیِ خراب
        content = content.replace("import androidx.compose.foundation.isSystemInDarkTheme\n", "")
        # جایگذاری مسیر کامل و مستقیم
        content = content.replace("isSystemInDarkTheme()", "androidx.compose.foundation.isSystemInDarkTheme()")
        
        with open(fp, "w") as f: f.write(content)
        print(f"Absolute dark theme path injected into: {os.path.basename(fp)}")

# ۲. تطبیق خودکار و هوشمند پکیج‌نیم HomeScreen با بقیه پروژه
home_file = "app/src/main/kotlin/com/github/soundpod/ui/screens/home/HomeScreen.kt"
qp_file = "app/src/main/kotlin/com/github/soundpod/ui/screens/home/QuickPicks.kt"

# تشخیص پکیج فعلی پروژه از روی فایل سالم گیت‌هاب
actual_pkg = "com.github.soundpod"
if os.path.exists(qp_file):
    with open(qp_file, "r") as f:
        if "package com.github.musick" in f.read():
            actual_pkg = "com.github.musick"
            print("Detected base package: com.github.musick")
        else:
            print("Detected base package: com.github.soundpod")

if os.path.exists(home_file):
    with open(home_file, "r") as f: content = f.read()
    
    # همگام‌سازی اجباریِ پکیج‌ها و ایمپورت‌ها با پکیج اصلی
    if actual_pkg == "com.github.musick":
        content = content.replace("package com.github.soundpod", "package com.github.musick")
        content = content.replace("import com.github.soundpod", "import com.github.musick")
    elif actual_pkg == "com.github.soundpod":
        content = content.replace("package com.github.musick", "package com.github.soundpod")
        content = content.replace("import com.github.musick", "import com.github.soundpod")
        
    with open(home_file, "w") as f: f.write(content)
    print("HomeScreen package synchronized successfully!")
