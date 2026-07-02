import os

files_to_fix = [
    "app/src/main/kotlin/com/github/soundpod/ui/screens/artist/ArtistScreen.kt",
    "app/src/main/kotlin/com/github/soundpod/ui/components/HorizontalTabs.kt"
]

for fp in files_to_fix:
    if os.path.exists(fp):
        with open(fp, "r") as f:
            lines = f.readlines()
        
        # چک می‌کنیم اگر ایمپورت از قبل وجود نداشت، اضافه‌اش کنیم
        content = "".join(lines)
        if "import androidx.compose.material3.MaterialTheme" not in content:
            # پیدا کردن خط پکیج و اضافه کردن ایمپورت دقیقاً زیر همون خط
            for i, line in enumerate(lines):
                if line.startswith("package "):
                    lines.insert(i + 1, "\nimport androidx.compose.material3.MaterialTheme\n")
                    break
            
            with open(fp, "w") as f:
                f.writelines(lines)
            print(f"Force-imported MaterialTheme into {os.path.basename(fp)}")
        else:
            print(f"MaterialTheme already exists in {os.path.basename(fp)}")

