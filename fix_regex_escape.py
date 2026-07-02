import os

fps = [
    "app/src/main/kotlin/com/github/soundpod/ui/screens/album/AlbumScreen.kt",
    "app/src/main/kotlin/com/github/musick/ui/screens/album/AlbumScreen.kt"
]

for fp in fps:
    if os.path.exists(fp):
        with open(fp, "r") as f:
            code = f.read()
        
        # تبدیل \d به \\d برای رفع ارور کامپایلر کاتلین
        code = code.replace('Regex("=w\\d+-h\\d+")', 'Regex("=w\\\\d+-h\\\\d+")')
        code = code.replace('Regex("=s\\d+")', 'Regex("=s\\\\d+")')
        
        with open(fp, "w") as f:
            f.write(code)

print("Regex escape sequences perfectly fixed for Kotlin!")
