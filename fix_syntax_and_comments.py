import os

file_path = "app/src/main/kotlin/com/github/soundpod/ui/screens/home/HomeScreen.kt"

if os.path.exists(file_path):
    with open(file_path, "r") as f:
        content = f.read()
    
    # تصحیح کامنت‌های اشتباه به فرمت استاندارد کاتلین
    content = content.replace("# کادر دوم: پریمیوم طلایی", "// کادر دوم: پریمیوم طلایی")
    content = content.replace("# کادر سوم: ترنسلیت هوشمند", "// کادر سوم: ترنسلیت هوشمند")
    content = content.replace("# کادر چهارم: تنظیمات", "// کادر چهارم: تنظیمات")
    
    # اطمینان از ایمپورت دقیق مسیرهای ناوبری پکیج
    if "import com.github.soundpod.ui.navigation.Routes" not in content and "import com.github.soundpod.ui.navigation.*" not in content:
        content = content.replace("package com.github.soundpod.ui.screens.home", 
                                  "package com.github.soundpod.ui.screens.home\nimport com.github.soundpod.ui.navigation.Routes")

    with open(file_path, "w") as f:
        f.write(content)
    print("Syntax and comment styles successfully fixed!")
else:
    print("HomeScreen file not found!")
