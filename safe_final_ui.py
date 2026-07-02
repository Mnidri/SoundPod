import os
import re

# پیدا کردن مسیر فایل‌ها (پشتیبانی همزمان از پکیج musick و soundpod)
def find_file(relative_path):
    for pkg in ["soundpod", "musick"]:
        path = f"app/src/main/kotlin/com/github/{pkg}/{relative_path}"
        if os.path.exists(path): return path
    return None

auth_file = find_file("ui/screens/auth/AuthScreen.kt")
if auth_file:
    with open(auth_file, "r") as f: content = f.read()
    
    # اضافه کردن اسکرول مستقیم بدون نیاز به ایمپورت
    if "verticalScroll" not in content:
        content = re.sub(
            r'\.padding\(horizontal = 24\.dp\),?', 
            '.padding(horizontal = 24.dp).verticalScroll(androidx.compose.foundation.rememberScrollState()),', 
            content
        )
    
    # اضافه کردن فضای خالی برای جلوگیری از تداخل با مینی‌پلیر
    if "120.dp" not in content:
        content = re.sub(
            r'(Text\("Continue with Google"[^\n]*\n\s*\}\n\s*\})', 
            r'\1\n                Spacer(modifier = Modifier.height(120.dp))', 
            content
        )
        
    with open(auth_file, "w") as f: f.write(content)
    print("AuthScreen UI fixed safely!")

home_file = find_file("ui/screens/home/HomeScreen.kt")
if home_file:
    with open(home_file, "r") as f: content = f.read()
    
    # بزرگ کردن چشمگیر فونت تایتل Musick
    content = re.sub(r'fontSize\s*=\s*44\.sp', 'fontSize = 72.sp', content)
    
    with open(home_file, "w") as f: f.write(content)
    print("HomeScreen UI & Fonts fixed safely!")
