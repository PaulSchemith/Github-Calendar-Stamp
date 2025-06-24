
# GitHub Contribution Calendar Stamper 🎨

Design your own GitHub contributions graph by creating fake commits with a simple, intuitive interface. This project uses a Tkinter-based calendar grid to simulate the GitHub contribution heatmap and push commits with backdated timestamps.

## 🖼️ Features

- Visual GitHub-style calendar grid (last 365 days).
- Click and drag to "paint" commits.
- Right-click and drag to erase.
- Tooltip showing commit date.
- Legend showing intensity levels (0 to 4+ commits).
- Push commits to GitHub with correct author and timestamps.
- Commits saved in a `log.txt` file to avoid empty commits.

## 📦 Requirements

- Python 3.x
- Git installed and accessible via command line
- Tkinter (usually comes with Python)

## 🚀 Setup & Usage

### 1. Clone this Repository

```bash
git clone https://github.com/PaulSchemith/Github-Calendar-Stamp.git
cd Github-Calendar-Stamp
```

### 2. Edit Git Identity

Edit the Python file and set your Git name and email at the top:

```python
NAME_GITHUB = "Your Name"
EMAIL_GITHUB = "you@example.com"
```

Also update:

```python
GITHUB_REMOTE_URL = "https://github.com/YOUR_USERNAME/YOUR_REPO.git"
BRANCH_NAME = "main"
```

### 3. Run the Application

```bash
python your_script.py
```

You’ll see a window with a GitHub-like calendar grid.

### 4. Draw Your Art 🎨

- Left click and drag to add commits.
- Right click and drag to erase.
- Hover to see the date tooltip.
- Click **"Validate & Push"** to generate and push commits.

### 5. Check Your GitHub Profile

After a few minutes, your GitHub contribution graph will be updated!

## 🧼 Cleaning Up

If you want to remove generated commits later, you can use interactive rebase or delete your Git history carefully.

---

**Disclaimer**: Use responsibly. This tool is for educational and artistic purposes only.
