# File Removal Candidates Review

## High Priority Removals (Safe to Delete)

### System Files
```
./.DS_Store
./tools/.DS_Store
./archive/.DS_Store
./articles/.DS_Store
./articles/0900-ai-lies/.DS_Store
./articles/0900-ai-lies/0914-gemini/.DS_Store
./articles/0900-ai-lies/raw/.DS_Store
./articles/0918-algorithmic-theatre/.DS_Store
./articles/0918-algorithmic-theatre/images/.DS_Store
./articles/0918-algorithmic-theatre/raw/.DS_Store
./articles/raw/10##-new-venue-victory/materials/.DS_Store
./articles/raw/10##-new-venue-victory/materials/code/.DS_Store
./articles/raw/10##-new-venue-victory/.DS_Store
./articles/raw/10##-new-venue-victory/raw/.DS_Store
./articles/raw/.DS_Store
./articles/raw/09##-crash-course-collaboration/materials/.DS_Store
./articles/raw/09##-crash-course-collaboration/.DS_Store
./articles/raw/09##-crash-course-collaboration/code/.DS_Store
./articles/raw/09##-crash-course-collaboration/raw/.DS_Store
./articles/raw/template/.DS_Store
```
**Total: 20+ .DS_Store files**
**Impact: Zero - these are macOS metadata files**

## Medium Priority Removals (Review Recommended)

### Large Media Files (Consider archiving or optimizing)
Look for a lightweight tool that we can run locally that will compress .png images.

**Response:** Python libraries are much better for your workflow:

1. **Pillow + pillow-simd** (recommended) - Easy compression with quality control
   ```bash
   uv add Pillow pillow-simd
   ```
   ```python
   from PIL import Image

   def compress_png(input_path, output_path, quality=85):
       with Image.open(input_path) as img:
           # Convert to RGB if needed, then save with optimization
           if img.mode == 'RGBA':
               img.save(output_path, 'PNG', optimize=True, compress_level=6)
           else:
               img.convert('RGB').save(output_path, 'JPEG', quality=quality, optimize=True)
   ```

2. **tinify** (TinyPNG API) - Professional compression service
   ```bash
   uv add tinify
   ```
   ```python
   import tinify
   tinify.key = "YOUR_API_KEY"  # Free: 500 images/month
   tinify.from_file("input.png").to_file("output.png")
   ```

3. **python-oxipng** - Python wrapper for oxipng
   ```bash
   uv add oxipng
   ```

For batch processing script:
```python
from pathlib import Path
from PIL import Image

def batch_compress_images(directory="./articles", size_threshold_mb=1):
    for png_file in Path(directory).rglob("*.png"):
        if png_file.stat().st_size > size_threshold_mb * 1024 * 1024:
            compress_png(png_file, png_file, quality=80)
```

### Audio Files
gitignore the m4a files, I thought I had. They are fine locally.

**Response:** I'll add m4a files to .gitignore. Current .gitignore check shows:
```bash
echo "*.m4a" >> .gitignore
```

Your existing .gitignore already excludes many common files. The m4a files will remain on your local system but won't be tracked in git going forward.

### Raw/Working Files
The .html files referenced are support material for their respective articles, make a recommendation on any safeguards we should consider that doesn't involve their removal.

**Response:** Safeguards for preserving important support materials:

1. **Create a `/materials` subdirectory** in each article folder for support files
2. **Add README.md** in materials directories explaining file purposes
3. **Use consistent naming** like `article-slug-source.html` or `article-slug-reference.html`
4. **Document in article frontmatter**:
   ```yaml
   materials:
     - "source-data/new-york-times.html"
     - "analysis/ai-writing-tracker.html"
   ```
5. **Consider Git LFS** for large HTML files (see below)

This preserves research materials while keeping them organized and documented.

### Analysis JSON Files
Same reason and request as .html files.

**Response:** JSON analysis files need similar organization:

1. **Create `/analysis` subdirectories** for computational results
2. **Use descriptive filenames**: `markup-analysis-results-v1.json` instead of generic names
3. **Add metadata headers** in JSON files:
   ```json
   {
     "_metadata": {
       "generated": "2024-06-06",
       "tool": "ai-writing-analyzer.py",
       "article": "algorithmic-theatre",
       "purpose": "Text similarity analysis between drafts"
     },
     "results": { ... }
   }
   ```
4. **Version control**: Keep final results, archive intermediate versions
5. **Link from articles**: Reference analysis files in article text or frontmatter

This maintains research reproducibility while keeping files organized.

## Low Priority / Keep (Important Files)

### Generated PDFs (Article Outputs)
Same reason and request as Large Media Files.

**Response:** PDF optimization options:

1. **qpdf** - Lossless PDF optimization
   ```bash
   brew install qpdf
   qpdf --optimize-images --compress-streams=y input.pdf output.pdf
   ```

2. **Ghostscript** - More aggressive compression
   ```bash
   brew install ghostscript
   gs -sDEVICE=pdfwrite -dCompatibilityLevel=1.4 -dPDFSETTINGS=/ebook -dNOPAUSE -dBATCH -sOutputFile=output.pdf input.pdf
   ```

3. **PDF compression levels**:
   - `/printer` (high quality, larger size)
   - `/ebook` (medium quality, good for reading)
   - `/screen` (lowest quality, smallest size)

For your article PDFs, `/ebook` setting provides good balance of quality and size.

### Code Files
Same reason and request as .html files.

**Response:** Code file organization and safeguards:

1. **Create `/code` subdirectories** in article folders for scripts and tools
2. **Add docstrings and comments** explaining purpose and usage
3. **Include requirements.txt** or dependency info for Python scripts
4. **Version control**: Tag working versions, archive experimental code
5. **Link from articles**: Reference code in methodology sections
6. **Consider making reusable**: Move general-purpose tools to `/tools` directory

Example structure:
```
articles/0918-algorithmic-theatre/
├── code/
│   ├── ai-writing-analyzer.py
│   ├── requirements.txt
│   └── README.md
```

This keeps research code accessible and reproducible.

## Recommendations

1. **Delete all .DS_Store files immediately** - zero risk
2. Respond to my responses in this file.

## Git LFS Consideration

Tell me more.

**Response:** Git LFS (Large File Storage) is perfect for your use case:

**What it does:**
- Stores large files (>1MB) outside main git repository
- Replaces large files with small text pointers in git history
- Downloads actual files only when needed

**Benefits for your project:**
- Keep full git history without bloating repo size
- Faster clones and fetches
- Better for images, audio, PDFs, and large datasets

**Setup process:**
```bash
# Install Git LFS
brew install git-lfs
git lfs install

# Track file types
git lfs track "*.png"
git lfs track "*.m4a"
git lfs track "*.pdf"
git lfs track "*.html"

# Commit the tracking file
git add .gitattributes
git commit -m "Configure Git LFS for large files"
```

**Migrating existing files:**
```bash
git lfs migrate import --include="*.png,*.m4a,*.pdf" --everything
```

**Cost consideration:** GitHub provides 1GB LFS storage free, then $5/month per 50GB. For your ~100MB of large files, you'd stay within free tier.

This would reduce your repo from 548MB to ~400MB while preserving all files.