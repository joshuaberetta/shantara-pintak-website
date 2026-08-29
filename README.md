# Shantara Pintak - Personal Website

A clean, professional personal website showcasing education, experience, and areas of focus in humanitarian action and peacebuilding.

Built with a **YAML-based content system** for easy editing, with automated builds and deployment via GitHub Actions.

---

## 🚀 Quick Start

### Prerequisites
- Python 3.11 or higher
- pip (Python package manager)

### Setup
1. Clone this repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Development Mode (Hot Reloading)
Run the dev server with automatic rebuilds:
```bash
python src/dev.py
```

The site will be available at `http://localhost:8000` and will automatically rebuild when you edit [src/content.yaml](src/content.yaml) or [src/template.html](src/template.html).

### Build for Production
Generate the static site:
```bash
python src/build.py
```

The compiled site will be in the `dist/` directory.

---

## 📝 Editing Content

All website content is in **[src/content.yaml](src/content.yaml)**. Edit this file to update:
- Personal information (name, tagline, contact details)
- Focus areas
- Education history
- Work experience
- Work samples (downloadable PDFs)
- Volunteer work
- Colors and fonts
- CTA button text

No HTML knowledge required! The build system automatically compiles YAML content into HTML.

### Adding a Work Sample
1. Drop the PDF into `assets/work-samples/`
2. Add an entry under `work_samples.items` in [src/content.yaml](src/content.yaml):
   ```yaml
   work_samples:
     items:
       - title: "Title shown on the site"
         file: "My Sample.pdf"   # file name inside assets/work-samples/
   ```

`file` is just the file name — the build handles the path and URL escaping, so
spaces and special characters are fine. Clicking a title downloads the PDF. The
build prints a warning if a listed file is missing from `assets/work-samples/`.

### Example Edit
```yaml
hero:
  name: "Your Name"
  tagline: "Your Tagline"
  intro: |
    Your introduction text here...
```

---

## 🎨 Customizing Design

### Colors & Fonts
Edit the `colors` and `fonts` sections in [src/content.yaml](src/content.yaml):
```yaml
colors:
  sand: "#F5F0E8"
  terracotta: "#C4785A"
  # ... more colors

fonts:
  display: "'Cormorant Garamond', Georgia, serif"
  body: "'Outfit', system-ui, sans-serif"
```

### Advanced Styling
For layout changes, edit [src/template.html](src/template.html). It uses Mustache templating syntax:
- `{{variable}}` - Simple variable substitution
- `{{#array}}...{{/array}}` - Loop over arrays
- `{{#object.property}}` - Access nested properties

---

## 🌐 Deploying to GitHub Pages

### Automatic Deployment (Recommended)

The repository includes a GitHub Actions workflow that automatically builds and deploys your site when you push to the `main` branch.

1. **Push your code to GitHub**:
   ```bash
   git add .
   git commit -m "Initial commit"
   git push origin main
   ```

2. **Enable GitHub Pages**:
   - Go to your repository's **Settings**
   - Navigate to **Pages** in the left sidebar
   - Under "Source", select **GitHub Actions**
   - Save

3. **Done!** Your site will be live at `https://YOUR-USERNAME.github.io/REPO-NAME/` within a few minutes.

The workflow runs on every push to `main` and automatically:
- Installs Python dependencies
- Builds the site from YAML
- Deploys to GitHub Pages

### Manual Deployment

If you prefer manual control:
1. Build the site locally: `python src/build.py`
2. Copy the contents of `dist/` to your web server — the build already places the
   profile photo, résumé, and work samples in `dist/assets/`

---

## 📁 Project Structure

```
.
├── src/
│   ├── content.yaml           # ✏️ Edit content here!
│   ├── template.html          # 🎨 HTML template with Mustache syntax
│   ├── build.py               # 🔨 Build script (YAML → HTML)
│   └── dev.py                 # 🔥 Dev server with hot reload
├── assets/                    # 🖼️ Static files, copied to dist/assets/
│   ├── shantara.jpg           #    Profile photo
│   ├── Shantara_Pintak_Resume.pdf
│   └── work-samples/          # 📄 Work sample PDFs
├── requirements.txt           # 📦 Python dependencies
├── .github/
│   └── workflows/
│       └── deploy.yml         # 🚀 GitHub Actions deployment
└── dist/                      # 📤 Build output (generated)
    ├── index.html
    └── assets/
```

---

## 🛠 Technical Details

### Build System
- **Template Engine**: Mustache (via pystache)
- **Content Format**: YAML
- **File Watching**: watchdog
- **Dev Server**: Python's built-in HTTP server

### CI/CD Pipeline
The GitHub Actions workflow ([.github/workflows/deploy.yml](.github/workflows/deploy.yml)):
1. Triggers on push to `main`
2. Sets up Python 3.11
3. Installs dependencies
4. Runs build script
5. Deploys to GitHub Pages

### Why This Approach?
- ✅ **Easy editing**: YAML is simple and readable
- ✅ **Version control**: Track content changes in git
- ✅ **No build tools**: Pure Python, no npm/webpack
- ✅ **Fast deployment**: Automated via GitHub Actions
- ✅ **No CMS needed**: Edit files directly in your editor

---

## 🧪 Testing Locally

1. Make changes to [src/content.yaml](src/content.yaml)
2. The dev server will automatically rebuild
3. Refresh your browser to see changes
4. Once satisfied, commit and push to deploy

---

## 📄 License

Feel free to fork and adapt for your own use!

---

## 💡 Tips

- **Keep resume PDF updated**: Replace `Shantara_Pintak_Resume.pdf` with your latest version
- **Preview before deploy**: Always test with `python dev.py` before pushing
- **Backup content**: The `content.yaml` file is the source of truth
- **Check builds**: Monitor the "Actions" tab in GitHub to ensure successful deploys
