# 🪐 PHANTOM (Saturn) - Setup & Usage Guide

## 📋 What is PHANTOM?
PHANTOM is a customizable command-line assistant with AI capabilities, note-taking, web tools, and personalized commands. Think of it as your own terminal-based helper!

---

## 🚀 Quick Setup (5 minutes)

### Step 1: Install Python
**If you don't have Python installed:**
1. Go to https://www.python.org/downloads/
2. Download Python 3.8 or newer
3. **IMPORTANT:** During installation, check "Add Python to PATH"
4. Click "Install Now"

**Check if Python is installed:**
- Open Command Prompt (Windows) or Terminal (Mac/Linux)
- Type: `python --version`
- Should show something like "Python 3.12.x"

### Step 2: Save the Program
1. Create a folder somewhere easy to find (e.g., `C:\PHANTOM\` or `~/phantom/`)
2. Save the Python code as `PHANTOM.py` in that folder

### Step 3: Run PHANTOM
**Windows:**
```
1. Open Command Prompt
2. Navigate to your folder: cd C:\PHANTOM
3. Run: python PHANTOM.py
```

**Mac/Linux:**
```
1. Open Terminal
2. Navigate to your folder: cd ~/phantom
3. Run: python3 PHANTOM.py
```

---

## 🎨 CUSTOMIZATION (Make it Yours!)

Open `PHANTOM.py` in any text editor and find this section near the top:

```python
# ============================================
# 🎨 EASY CUSTOMIZATION - CHANGE THESE! 🎨
# ============================================
PROGRAM_NAME = "Saturn"
PROGRAM_TAGLINE = "Just like this program its the coolest planet"

# 💀 Change the ASCII art below
ASCII_ART = """
    [Your ASCII art here]
"""
```

**Change the name and tagline to anything you want!**
- `PROGRAM_NAME`: What the program calls itself
- `PROGRAM_TAGLINE`: A fun description
- `ASCII_ART`: Your custom logo (find ASCII art at asciiart.eu)

---

## 📚 BASIC COMMANDS

### Getting Started
```
help                    - Show all commands
listcolors              - See available colors
setcolor cyan           - Change text color
rgb on                  - Enable rainbow mode 🌈
clear screen            - Clear the terminal
banner                  - Show the logo again
exit                    - Quit PHANTOM
```

### Notes & Memory
```
note Buy milk           - Save a quick note
notes                   - View all your notes
clear notes             - Delete all notes

teach dogs: Dogs are loyal pets    - Teach PHANTOM something
what do you know about dogs        - Ask what it knows
forget dogs                        - Remove saved info
```

### Web Tools
```
open youtube.com        - Open a website
search cute cats        - Google search
ping google.com         - Check if site is online
ip                      - Show your IP addresses
```

### System Tools
```
time                    - Current time and date
calc 2 + 2 * 5         - Basic calculator
```

### Custom Commands
```
add command music: open spotify.com    - Create your own command
list commands                          - See custom commands
remove command music                   - Delete a command
```

---

## 🤖 AI FEATURES (Optional)

PHANTOM can have AI conversation abilities!

### Setup AI (One-time, ~5 minutes)
1. Download Ollama from https://ollama.com
2. Install Ollama
3. In PHANTOM, type: `check dependencies`
4. Type: `install requests` (if needed)
5. Type: `download` (downloads AI model, ~2GB)
6. Wait 2-5 minutes for download

### Using AI
```
ask What is Python?
ask Write a haiku about coding
ask Explain quantum physics simply
```

**Note:** First AI response might be slow while Ollama starts up!

---

## 🔧 TROUBLESHOOTING

### "Python is not recognized"
- Reinstall Python and check "Add to PATH" during installation
- Or use full path: `C:\Python312\python.exe PHANTOM.py`

### "ModuleNotFoundError: requests"
- In PHANTOM, type: `install requests`
- Or manually: `pip install requests`

### AI not working
1. Check dependencies: `check dependencies`
2. Make sure Ollama is running (check system tray/menu bar)
3. Try: `download` to reinstall the model

### Colors not showing
- Some terminals don't support colors (like older Windows CMD)
- Try Windows Terminal (free from Microsoft Store)
- Or use PowerShell instead

### Program closes immediately
- Don't double-click the .py file!
- Open Command Prompt/Terminal first, then run it
- Or create a .bat file (Windows):
  ```batch
  @echo off
  python PHANTOM.py
  pause
  ```

---

## 🚀 AUTO-START ON WINDOWS BOOT (REQUIRED)

**PHANTOM is designed to start automatically when Windows starts!**

### Complete Setup:

1. **Create your PHANTOM folder:**
   - Recommended: `C:\PHANTOM\`
   - Put `PHANTOM.py` in this folder

2. **Create PHANTOM.bat file:**
   - In the same folder (`C:\PHANTOM\`), create a new text file
   - Rename it to `PHANTOM.bat` (not .txt!)
   - Right-click → Edit, and paste this:
   ```batch
   @echo off
   cd /d C:\PHANTOM
   python PHANTOM.py
   pause
   ```
   - **Important:** Change `C:\PHANTOM` if you used a different folder!
   - Save and close

3. **Add to Windows Startup:**
   - Press `Windows + R` on your keyboard
   - Type: `shell:startup` and press Enter
   - This opens your Startup folder
   - **Copy BOTH files into this folder:**
     - `PHANTOM.py`
     - `PHANTOM.bat`
   - Close the window

4. **Test it:**
   - Restart your computer
   - PHANTOM should open automatically in a terminal window!

### Your Startup Folder Will Look Like:
```
📁 Startup (opened via shell:startup)
   📄 PHANTOM.py
   📄 PHANTOM.bat
```

**Note:** The error you saw means one of these files was missing from the Startup folder!

---

## 💡 TIPS & TRICKS

1. **Startup Script:** Type commands on separate lines in a .txt file, then paste them all at once

2. **Custom Commands Ideas:**
   ```
   add command reddit: open reddit.com
   add command weather: open weather.com
   add command gmail: open gmail.com
   ```

4. **Keyboard Shortcuts:**
   - `Ctrl+C` - Interrupts current operation (doesn't quit)
   - `Ctrl+L` or type `clear screen` - Clear terminal
   - Up Arrow - Previous command (terminal feature)

5. **Save Your Work:** All notes, commands, and knowledge are saved automatically in `~/.phantom/`

---

## 📁 FILE LOCATIONS

PHANTOM saves data in your home directory:
- **Windows:** `C:\Users\YourName\.phantom\`
- **Mac/Linux:** `~/.phantom/`

Files saved:
- `knowledge.json` - Things you taught it
- `commands.json` - Custom commands
- `notes.json` - Your notes
- `settings.json` - Color and preferences

You can delete these to reset PHANTOM to defaults.

---

## ⚠️ IMPORTANT NOTES

- **Custom commands execute shell commands** - Only add commands you trust!
- **Internet required** for web searches, opening sites, and AI
- **AI is local** - Your conversations never leave your computer
- **Data is stored locally** - Everything stays on your machine

---

## 🎯 EXAMPLE SESSION

```
Saturn> setcolor magenta
✓ Color changed to magenta

Saturn> note Remember to call mom
✓ Note saved

Saturn> teach python: A programming language for beginners
✓ Learned about 'python'

Saturn> what do you know about python
📖 python: A programming language for beginners

Saturn> calc 15 * 12
🔢 15 * 12 = 180

Saturn> time
🕐 03:45 PM, October 28, 2025

Saturn> ask What's 2+2?
🧠 Thinking...
🤖 The answer is 4...

Saturn> exit
👋 Goodbye!
```

---

## 🆘 Need More Help?

- Python Help: https://www.python.org/about/gettingstarted/
- Ollama Docs: https://ollama.com/docs
- ASCII Art: https://www.asciiart.eu/

**Enjoy your personalized assistant! 🚀**
