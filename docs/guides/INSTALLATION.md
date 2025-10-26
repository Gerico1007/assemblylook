# Installation Guide

**♠️🌿🎸🧵 AssemblyLook - Unified AI Session Tracker**

This guide will walk you through installing AssemblyLook from scratch on Termux (Android) or Linux.

---

## Prerequisites

### Required Software

1. **Termux** (for Android) or **Linux** terminal
2. **Python 3.12+**
3. **Git**
4. **Rust/Cargo** (for claude-code-log)
5. **Claude Code** or **Gemini CLI** (at least one)

### Check Current Versions

```bash
python3 --version    # Should be 3.12 or higher
git --version
cargo --version
```

---

## Step 1: Install System Dependencies

### On Termux (Android)

```bash
# Update packages
pkg update && pkg upgrade

# Install required packages
pkg install python git rust

# Install Termux:API (for notifications and clipboard)
# Download from F-Droid or GitHub releases
pkg install termux-api
```

### On Linux (Debian/Ubuntu)

```bash
sudo apt update
sudo apt install python3 python3-pip git curl

# Install Rust (if not already installed)
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
source $HOME/.cargo/env
```

---

## Step 2: Install claude-code-log

```bash
# Install via Cargo
cargo install claude-code-log

# Verify installation
claude-code-log --version
```

**Note**: This may take several minutes to compile.

---

## Step 3: Clone AssemblyLook Repository

```bash
# Navigate to workspace directory (create if needed)
mkdir -p ~/workspace
cd ~/workspace

# Clone the repository
git clone https://github.com/Gerico1007/assemblylook.git
cd assemblylook
```

---

## Step 4: Set Up Python Environment

AssemblyLook uses pure Python with no external dependencies, so no virtualenv is needed.

### Verify Python Installation

```bash
python3 -c "import sys; print(f'Python {sys.version}')"
```

Should show Python 3.12 or higher.

---

## Step 5: Configure Environment Variables

### Add to `.bashrc`

Edit your `.bashrc` file:

```bash
nano ~/.bashrc
```

Add these lines at the end:

```bash
# ♠️🌿🎸🧵 AssemblyLook Server Configuration
export ASSEMBLYLOOK_PORT=8000  # Default port for session tracker
```

Save and reload:

```bash
source ~/.bashrc
```

### Verify Configuration

```bash
echo $ASSEMBLYLOOK_PORT
# Should output: 8000
```

---

## Step 6: Install AssemblyLook Script

### Option A: Copy Script to ~/.shortcuts (Recommended)

```bash
# Create shortcuts directory if it doesn't exist
mkdir -p ~/.shortcuts

# Copy the script
cp ~/workspace/assemblylook/code/assemblylook-daily.sh ~/.shortcuts/

# Make executable
chmod +x ~/.shortcuts/assemblylook-daily.sh
```

### Option B: Create Symlink

```bash
mkdir -p ~/.shortcuts
ln -s ~/workspace/assemblylook/code/assemblylook-daily.sh ~/.shortcuts/assemblylook-daily.sh
```

---

## Step 7: Configure Gemini Converter (if using Gemini)

If you use Gemini CLI, you need the prettifier script:

```bash
# Ensure the Gemini converter exists
ls -la ~/.shortcuts/gemini_converter_tool/code/Gemini\ CLI\ logs\ prettifier/pretty_print_chat.py
```

If it doesn't exist, the AssemblyLook script will notify you and continue with Claude-only support.

---

## Step 8: Test Installation

### Run a Test

```bash
bash ~/.shortcuts/assemblylook-daily.sh
```

### Expected Output

```
♠️🌿🎸🧵 G.MUSIC ASSEMBLY — AssemblyLook Unified Session Tracker
================================================================

🎸 [1/4] Generating Claude logs...
  ✓ Claude logs generated

🌿 [2/4] Generating Gemini logs...
  ✓ Gemini logs generated

♠️ [3/4] Generating AssemblyLook unified dashboard...
[1/5] Parsing sessions...
  ✓ Found X Claude sessions
  ✓ Found Y Gemini sessions
... (additional output)

================================================================
✅ AssemblyLook Server Active
================================================================
📡 Dashboard: http://192.168.x.x:8000/.assemblylook/index.html
📋 Link copied to clipboard
🛑 To stop: pkill -f 'python3 -m http.server 8000'
```

### Access the Dashboard

Open the URL shown in your browser from any device on your WiFi network.

---

## Troubleshooting

### Issue: "claude-code-log not found"

**Solution**: Ensure Rust/Cargo is installed and in PATH:

```bash
cargo --version
echo $PATH | grep cargo
```

If missing, add to `.bashrc`:

```bash
export PATH="$HOME/.cargo/bin:$PATH"
source ~/.bashrc
```

### Issue: "No network connection found"

**Solution**: Ensure you're connected to WiFi:

```bash
ifconfig | grep "inet "
```

Should show at least one IP address besides `127.0.0.1`.

### Issue: "Python 3.12 not found"

**Solution**: Update Python:

```bash
# Termux
pkg install python

# Linux
sudo apt install python3.12
```

### Issue: "Permission denied" on script

**Solution**: Make the script executable:

```bash
chmod +x ~/.shortcuts/assemblylook-daily.sh
```

### Issue: "Port 8000 already in use"

**Solution**: Choose a different port:

```bash
ASSEMBLYLOOK_PORT=8080 bash ~/.shortcuts/assemblylook-daily.sh
```

Or kill the existing server:

```bash
pkill -f 'python3 -m http.server 8000'
```

### Issue: Dashboard shows but session links don't work

**Solution**: This is normal if you're serving from the wrong directory. The script automatically serves from `~` so all absolute paths work correctly.

Verify server is running from home directory:

```bash
ps aux | grep "http.server"
```

Should show: `python3 -m http.server 8000 --bind 0.0.0.0` with working directory as `/data/data/com.termux/files/home`.

---

## Verification Checklist

✅ Python 3.12+ installed
✅ Git installed
✅ claude-code-log installed and in PATH
✅ AssemblyLook cloned to `~/workspace/assemblylook`
✅ Environment variable `ASSEMBLYLOOK_PORT` set in `.bashrc`
✅ Script copied to `~/.shortcuts/assemblylook-daily.sh`
✅ Script is executable (`chmod +x`)
✅ Test run successful
✅ Dashboard accessible from browser

---

## Next Steps

- **[Usage Guide](./USAGE.md)** - Learn how to use AssemblyLook effectively
- **[Architecture](./ARCHITECTURE.md)** - Understand how it works under the hood
- **[Main README](../../README.md)** - Overview and features

---

**♠️🌿🎸🧵 Installation Complete!** You're ready to track your AI sessions! ⚡
