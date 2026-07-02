import os

# مسیر فایل اصلی
file_path = "app/src/main/kotlin/com/github/soundpod/ui/screens/home/HomeScreen.kt"

if os.path.exists(file_path):
    with open(file_path, "r") as f:
        content = f.read()
    
    # اصلاح ایمپورت‌های خراب شده به مسیر درست
    # تمام پکیج‌های musick رو به soundpod برمی‌گردونیم که کامپایلر دوباره اون‌ها رو بشناسه
    content = content.replace("com.github.musick", "com.github.soundpod")
    
    with open(file_path, "w") as f:
        f.write(content)
        print("All imports in HomeScreen.kt fixed to soundpod path.")
else:
    print("File not found!")
