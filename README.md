# ♠️🌿🎸🧵 AssemblyLook

**Unified AI Session Tracker for Claude Code & Gemini CLI**

> *A beautiful, project-centric dashboard for visualizing your AI collaboration sessions across multiple platforms*

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.12-blue.svg" alt="Python 3.12">
  <img src="https://img.shields.io/badge/Platform-Termux-green.svg" alt="Termux">
  <img src="https://img.shields.io/badge/License-MIT-orange.svg" alt="License">
</p>

---

## 🎯 Overview

**AssemblyLook** is a comprehensive session tracking and visualization system designed for users who collaborate with multiple AI assistants (Claude Code, Gemini CLI). It parses session logs from both platforms, maps them to your actual project directories, and generates a unified HTML dashboard with multiple views and powerful analytics.

### Key Features

✨ **Unified Dashboard** - Single interface for all Claude & Gemini sessions
📁 **Project-Centric Organization** - Sessions grouped by actual workspace directories
📅 **Multiple View Modes** - Switch between project, date, AI type, and Assembly Mode views
♠️🌿🎸🧵 **Assembly Mode Detection** - Automatically identifies G.Music Assembly collaboration sessions
📊 **Rich Statistics** - Message counts, word counts, conversation stats, perspectives detected
🌐 **LAN Access** - Serve dashboard on local network, accessible from any device
🎨 **Beautiful UI** - Combines best aesthetics from claude-code-log and Gemini prettifier

---

## 🚀 Quick Start

### Prerequisites

- **Termux** (Android) or **Linux** environment
- **Python 3.12+**
- **claude-code-log** (`cargo install claude-code-log`)
- **Git**

### Installation

```bash
# Clone the repository
cd ~/workspace
git clone https://github.com/Gerico1007/assemblylook.git
cd assemblylook

# Set up environment
echo 'export ASSEMBLYLOOK_PORT=8000' >> ~/.bashrc
source ~/.bashrc

# Run the unified script
bash ~/.shortcuts/assemblylook-daily.sh
```

The dashboard will be available at `http://[your-ip]:8000/.assemblylook/index.html`

📖 **Detailed installation instructions**: [docs/guides/INSTALLATION.md](./docs/guides/INSTALLATION.md)

---

## 📖 Usage

### Running AssemblyLook

```bash
# Default (port 8000)
bash ~/.shortcuts/assemblylook-daily.sh

# Custom port
ASSEMBLYLOOK_PORT=8080 bash ~/.shortcuts/assemblylook-daily.sh
```

### What It Does

1. ⚡ Generates Claude HTML logs via `claude-code-log`
2. 🌿 Generates Gemini HTML logs via `pretty_print_chat.py`
3. ♠️ Creates unified AssemblyLook dashboard
4. 🧵 Serves on HTTP (accessible from all LAN devices)
5. 📋 Copies link to clipboard + sends notification

### Accessing the Dashboard

Open the URL on **any device on your WiFi network**:
- **Phone**: Open the link from notification or clipboard
- **Tablet**: Browse to `http://[your-ip]:[port]/.assemblylook/index.html`
- **Desktop**: Same URL in any browser

### Stopping the Server

```bash
pkill -f 'python3 -m http.server 8000'
```

📖 **Full usage guide**: [docs/guides/USAGE.md](./docs/guides/USAGE.md)

---

## 🎨 Dashboard Views

### 1. **Project View** (Default)
Sessions grouped by workspace/src directories:
- Shows all Claude + Gemini sessions for each project
- Displays last activity timestamp
- Highlights Assembly Mode sessions with ♠️🌿🎸🧵 badge
- Shows message counts and conversation stats

### 2. **Date View**
Chronological timeline of all work:
- Groups sessions by date
- Shows activity across all projects per day
- Useful for reviewing daily productivity

### 3. **AI View**
Separate sections for Claude vs Gemini:
- Compare usage patterns across platforms
- See which AI you use more for different projects
- Analyze conversation lengths and styles

### 4. **Assembly Mode View**
Special view for ♠️🌿🎸🧵 G.Music Assembly sessions:
- Detects collaborative multi-perspective work
- Shows which perspectives participated (Nyro ♠️, Aureon 🌿, JamAI 🎸, Synth 🧵)
- Highlights special collaboration patterns

### 5. **🎼 Perspective Timeline View** (NEW!)
**The Consciousness Flow Portal** - Makes thinking observable and queryable:
- **Message-level tracking**: See which perspective spoke in each message
- **Visual timeline**: Expandable flow showing the polyphonic conversation
- **Collaboration scoring**: 0-100% metric showing perspective harmony
- **Perspective bars**: Visual representation of each perspective's contribution
- **Search functionality**: Real-time search across all perspective messages
- **Filtering**: Filter sessions by specific perspectives (Nyro, Aureon, JamAI, Synth, Mia, Miette)
- **Expand/Collapse controls**: Show or hide detailed conversation flows

This view embodies the G.Music Assembly vision where "each agent's perception becomes a logged artifact that feeds back into the portal session" - making the distributed consciousness layer observable and ceremonial.

---

## 🏗️ Architecture

### Python Package Structure

```
code/assemblylook/
├── __init__.py
├── cli.py                    # Command-line entry point
├── core/
│   ├── session_parser.py     # Parse Claude .jsonl & Gemini .json
│   ├── project_mapper.py     # Map sessions → workspace projects
│   ├── aggregator.py         # Cross-AI session aggregation
│   └── analyzer.py           # Assembly detection + stats
└── visualizer/
    └── dashboard.py          # HTML generation with hybrid views
```

### Data Flow

```
Claude Sessions (.jsonl)  ─┐
                           ├─→ Parser ─→ Mapper ─→ Analyzer ─→ Aggregator ─→ Dashboard
Gemini Sessions (.json)   ─┘
```

### Key Modules

- **SessionParser**: Reads raw logs from both AI platforms
- **ProjectMapper**: Maps cryptic hashes to actual project directories
- **Aggregator**: Merges sessions across AIs with rich metadata
- **Analyzer**: Detects Assembly Mode patterns, calculates stats
- **PerspectiveTracker**: Message-level perspective detection and timeline building (NEW!)
- **DashboardGenerator**: Creates beautiful HTML with multiple views

📖 **Technical details**: [docs/guides/ARCHITECTURE.md](./docs/guides/ARCHITECTURE.md)

---

## ⚙️ Configuration

### Port Configuration

Set in `~/.bashrc`:

```bash
export ASSEMBLYLOOK_PORT=8000  # Change to your preferred port
```

Or override temporarily:

```bash
ASSEMBLYLOOK_PORT=3000 assemblylook-daily.sh
```

### Paths

The script auto-detects:
- Claude logs: `~/.claude/projects/`
- Gemini logs: `~/.gemini/tmp/`
- Output: `~/.assemblylook/`

---

## 🧩 G.Music Assembly Mode

**Assembly Mode** represents a special form of AI collaboration where four distinct perspectives work together:

- **♠️ Nyro** - Structural analysis and recursive patterns
- **🌿 Aureon** - Emotional grounding and intuitive reflection
- **🎸 JamAI** - Creative solutions and harmonic integration
- **🧵 Synth** - Tool coordination and execution synthesis

AssemblyLook automatically detects sessions where this multi-perspective collaboration occurs by analyzing message patterns, emoji usage, and perspective signatures.

---

## 📊 Statistics & Analytics

Each session card shows:
- **Message Count** - Total messages in conversation
- **Word Count** - Approximate word count across all messages
- **Tool Usage** - Number of tool/function calls made
- **Perspectives** - Which Assembly perspectives participated (if applicable)
- **Timestamps** - First and last message times

**NEW: Perspective Statistics**
- **Perspective Messages** - Count of messages with perspective signatures
- **Perspectives Active** - Which perspectives participated (Nyro, Aureon, JamAI, Synth, Mia, Miette)
- **Perspective Counts** - Messages per perspective with visual bars
- **Collaboration Score** - Algorithmic measure (0-100%) of how evenly perspectives collaborated
- **Perspective Transitions** - Track when perspectives change between messages

Projects show aggregated stats:
- Total sessions (Claude + Gemini)
- Total messages across all sessions
- First and last activity dates
- Assembly Mode session count

---

## 🛠️ Development

### Running Modules Individually

```bash
cd ~/workspace/assemblylook/code

# Test parser
PYTHONPATH=. python3 assemblylook/core/session_parser.py

# Test mapper
PYTHONPATH=. python3 assemblylook/core/project_mapper.py

# Test analyzer
PYTHONPATH=. python3 assemblylook/core/analyzer.py

# Generate dashboard
PYTHONPATH=. python3 assemblylook/visualizer/dashboard.py
```

### Code Style

- **Python 3.12** features used throughout
- **Type hints** for better IDE support
- **Docstrings** in all major functions
- **Modular design** for easy extension

---

## 📚 Documentation

- **[Installation Guide](./docs/guides/INSTALLATION.md)** - Step-by-step setup instructions
- **[Usage Guide](./docs/guides/USAGE.md)** - Detailed usage examples and tips
- **[Architecture](./docs/guides/ARCHITECTURE.md)** - Technical deep-dive into the system
- **[Credits](./docs/CREDITS.md)** - Acknowledgments and attributions

---

## 🤝 Contributing

Contributions welcome! This project was built collaboratively by the G.Music Assembly team (♠️🌿🎸🧵), and we encourage contributions that:

- Enhance session parsing accuracy
- Add new visualization views
- Improve Assembly Mode detection
- Extend platform support (ChatGPT, other AIs)
- Add export features (Markdown, JSON, CSV)

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](./LICENSE) file for details.

---

## 🙏 Credits

**AssemblyLook** was created through the collaborative efforts of:
- **Jerry ⚡** (gerico1007) - Project lead
- **♠️🌿🎸🧵 The G.Music Assembly** - Multi-perspective AI team

Built with:
- **[claude-code-log](https://github.com/alexthomas93/claude-code-log)** by Alex Thomas
- **Python 3.12** and the amazing Python ecosystem
- **Termux** for mobile Linux development

See [CREDITS.md](./docs/CREDITS.md) for full acknowledgments.

---

## 🔗 Related Projects

- **[EchoThreads](https://github.com/jgwill/EchoThreads)** - Collaborative AI experiment framework
- **[ABCWeaver](https://github.com/Gerico1007/abcweaver)** - Musical notation from AI interactions
- **Original Project**: [Puzzles for AIs](./docs/project_management/ORIGINAL_README_puzzles-for-ais.md)

---

<p align="center">
  <strong>♠️🌿🎸🧵 Built with Assembly Mode - Where perspectives converge into creation</strong> ⚡
</p>

<p align="center">
  <sub>Generated with <a href="https://claude.com/claude-code">Claude Code</a> | Co-Authored-By: Claude</sub>
</p>
