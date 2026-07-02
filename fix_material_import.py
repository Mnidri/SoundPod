import os

files_to_fix = [
    "app/src/main/kotlin/com/github/soundpod/ui/components/HorizontalTabs.kt",
    "app/src/main/kotlin/com/github/soundpod/ui/screens/artist/ArtistScreen.kt"
]

for fp in files_to_fix:
    if os.path.exists(fp):
        with open(fp, "r") as f:
            content = f.read()
        
        # اگر ایمپورت وجود نداشت، اون رو قبل از اولین ایمپورتِ فایل اضافه کن
        if "import androidx.compose.material3.MaterialTheme" not in content:
            import_idx = content.find("import ")
            if import_idx != -1:
                content = content[:import_idx] + "import androidx.compose.material3.MaterialTheme\n" + content[import_idx:]
                
        with open(fp, "w") as f:
            f.write(content)

print("MaterialTheme import successfully added to missing files!")
