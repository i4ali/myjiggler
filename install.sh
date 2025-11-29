#!/bin/bash
# Installation script for Mac Mouse Jiggler

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_DIR="/usr/local/bin"
SCRIPT_NAME="jiggler"
VENV_DIR="$SCRIPT_DIR/venv"

echo "⚠️  DEPRECATED: This installation method is deprecated."
echo "   Please use Homebrew installation instead:"
echo ""
echo "     brew tap i4ali/jiggler"
echo "     brew install jiggler"
echo ""
echo "   Continue with legacy installation? (y/N)"
read -r response
if [[ ! "$response" =~ ^[Yy]$ ]]; then
    echo "Installation cancelled. Please use Homebrew instead."
    exit 0
fi
echo ""

echo "🖱️  Installing Mac Mouse Jiggler (legacy method)..."
echo ""

# Check if running on macOS
if [[ "$OSTYPE" != "darwin"* ]]; then
    echo "❌ Error: This script is designed for macOS only."
    exit 1
fi

# Check Python version
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 is not installed."
    echo "   Please install Python 3 from https://www.python.org/"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
echo "✓ Found Python $PYTHON_VERSION"

# Create virtual environment if it doesn't exist
if [ ! -d "$VENV_DIR" ]; then
    echo ""
    echo "🔧 Creating virtual environment..."
    python3 -m venv "$VENV_DIR"
    echo "✓ Virtual environment created"
fi

# Activate virtual environment and install dependencies
echo ""
echo "📦 Installing dependencies in virtual environment..."
source "$VENV_DIR/bin/activate"
pip install --upgrade pip -q
pip install -r "$SCRIPT_DIR/requirements.txt" -q
deactivate
echo "✓ Dependencies installed"

echo ""

# Create wrapper script
WRAPPER_SCRIPT="$SCRIPT_DIR/jiggler"
cat > "$WRAPPER_SCRIPT" << 'EOF'
#!/bin/bash
# Wrapper script for Mac Mouse Jiggler that activates venv

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_PYTHON="$SCRIPT_DIR/venv/bin/python3"

# Check if venv exists
if [ ! -f "$VENV_PYTHON" ]; then
    echo "❌ Error: Virtual environment not found. Please run install.sh first."
    exit 1
fi

# Run jiggler with venv Python
exec "$VENV_PYTHON" "$SCRIPT_DIR/jiggler.py" "$@"
EOF

chmod +x "$WRAPPER_SCRIPT"
echo "✓ Created wrapper script"

# Create symlink to wrapper (not directly to Python script)
if [ -w "$INSTALL_DIR" ]; then
    ln -sf "$WRAPPER_SCRIPT" "$INSTALL_DIR/$SCRIPT_NAME"
    echo "✓ Installed to $INSTALL_DIR/$SCRIPT_NAME"
else
    echo "🔐 Need sudo permissions to install to $INSTALL_DIR"
    sudo ln -sf "$WRAPPER_SCRIPT" "$INSTALL_DIR/$SCRIPT_NAME"
    echo "✓ Installed to $INSTALL_DIR/$SCRIPT_NAME"
fi

echo ""
echo "✅ Installation complete!"
echo ""
echo "Usage: $SCRIPT_NAME [OPTIONS]"
echo "Try: $SCRIPT_NAME --help"
echo ""
