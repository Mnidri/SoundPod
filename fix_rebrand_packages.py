import os

files_to_fix = [
    "app/src/main/kotlin/com/github/soundpod/ui/screens/home/HomeScreen.kt",
    "app/src/main/kotlin/com/github/soundpod/ui/screens/auth/AuthScreen.kt"
]

for fp in files_to_fix:
    if os.path.exists(fp):
        with open(fp, "r") as f:
            content = f.read()
        
        # برگرداندن پکیج‌نیم کدها به Musick (هماهنگ با بقیه فایل‌های پروژه)
        content = content.replace("com.github.soundpod", "com.github.musick")
        
        with open(fp, "w") as f:
            f.write(content)

print("Packages successfully synced to Musick!")
