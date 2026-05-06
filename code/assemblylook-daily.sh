#!/bin/bash
# ♠️🌿🎸🧵 AssemblyLook Daily Sync & Server
# Unified script to update logs, generate dashboard, and serve.

# Get the directory where the script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
ASSEMBLYLOOK_PORT="${ASSEMBLYLOOK_PORT:-8000}"

echo "♠️🌿🎸🧵 G.MUSIC ASSEMBLY — AssemblyLook Unified Session Tracker"
echo "================================================================"

# 1. Claude logs
echo "🎸 [1/4] Generating Claude logs..."
if command -v claude-code-log &> /dev/null; then
    # Usually claude-code-log handles its own discovery
    claude-code-log
    echo "  ✓ Claude logs generated"
else
    echo "  ! claude-code-log not found, skipping Claude logs"
fi

# 2. Gemini logs
echo "🌿 [2/4] Generating Gemini logs..."
PRETTIFIER_DIR="$PROJECT_ROOT/code/Gemini CLI logs prettifier"
if [ -d "$PRETTIFIER_DIR" ]; then
    cd "$PRETTIFIER_DIR"
    python3 pretty_print_chat.py
    echo "  ✓ Gemini logs generated"
else
    echo "  ! Gemini prettifier not found at $PRETTIFIER_DIR"
fi

# 3. AssemblyLook Dashboard
echo "♠️ [3/4] Generating AssemblyLook unified dashboard..."
cd "$PROJECT_ROOT"
# Ensure PYTHONPATH includes the code directory
export PYTHONPATH="$PROJECT_ROOT/code:$PYTHONPATH"
python3 -m assemblylook.cli

# 4. Serve
echo "🌐 [4/4] Starting server on port $ASSEMBLYLOOK_PORT..."
# Kill existing server if any
pkill -f "python3 -m http.server $ASSEMBLYLOOK_PORT" 2>/dev/null

# Change to HOME to allow absolute path links to work
cd "$HOME"
# Start in background and redirect output to a log file
python3 -m http.server "$ASSEMBLYLOOK_PORT" --bind 0.0.0.0 > /tmp/assemblylook.log 2>&1 &

echo "================================================================"
echo "✅ AssemblyLook Server Active"
echo "================================================================"
# Try to get IP address (Linux/Termux compatible)
IP_ADDR=$(hostname -I | awk '{print $1}' || echo "localhost")
echo "📡 Dashboard: http://$IP_ADDR:$ASSEMBLYLOOK_PORT/.assemblylook/index.html"
echo "🛑 To stop: pkill -f 'python3 -m http.server $ASSEMBLYLOOK_PORT'"
