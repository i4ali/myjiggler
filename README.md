# Mac Mouse Jiggler

A lightweight, native command-line mouse jiggler for macOS that prevents your Mac from going to sleep by moving the mouse cursor periodically.

## Features

- **Native macOS Support**: Uses Core Graphics API for flawless performance on Mac
- **Multiple Movement Patterns**: Choose from gentle, circular, or random movements
- **Customizable Intervals**: Control how often the mouse moves
- **Duration Control**: Run indefinitely or for a specific time period
- **Minimal Movement**: Default 1-pixel movement is virtually invisible
- **Graceful Shutdown**: Clean exit with Ctrl+C
- **No External Dependencies**: Uses built-in macOS frameworks

## Requirements

- macOS (tested on macOS 10.14+)
- Python 3.6 or higher
- pyobjc-framework-Quartz (installed automatically by install script)

## Installation

### Quick Install

```bash
./install.sh
```

This will:
1. Check for Python 3
2. Create a virtual environment (venv)
3. Install the required `pyobjc-framework-Quartz` package in venv (not in system Python)
4. Create a wrapper script that activates the venv
5. Attempt to create a symlink in `/usr/local/bin` (requires sudo)

**Important:** The install script will prompt for your password to create a global symlink. After installation, you can run `jiggler` from any directory.

If the install script fails at the symlink step, run this manually:

```bash
sudo ln -sf "$(pwd)/jiggler" /usr/local/bin/jiggler
```

### Manual Installation (Without install.sh)

```bash
# Create virtual environment
python3 -m venv venv

# Activate venv and install dependencies
source venv/bin/activate
pip install -r requirements.txt
deactivate

# Make scripts executable
chmod +x jiggler.py
chmod +x jiggler

# Create global symlink (optional, for running from anywhere)
sudo ln -sf "$(pwd)/jiggler" /usr/local/bin/jiggler
```

### Running Without Global Installation

If you don't want to install globally, you can run the jiggler from the project directory:

```bash
./jiggler [OPTIONS]
```

## Usage

### Basic Usage

```bash
# Run with defaults (jiggle every 60 seconds)
./jiggler.py

# Or if installed globally
jiggler
```

### Command-Line Options

```
usage: jiggler.py [-h] [-i SECONDS] [-d PIXELS] [-t MINUTES]
                  [-p {gentle,circular,random}] [-q] [--version]

Options:
  -h, --help            Show help message and exit
  -i, --interval SECONDS
                        Seconds between each jiggle (default: 60)
  -d, --distance PIXELS
                        Pixels to move the mouse (default: 1)
  -t, --time MINUTES    Total duration in minutes (default: run indefinitely)
  -p, --pattern {gentle,circular,random}
                        Movement pattern (default: gentle)
  -q, --quiet           Quiet mode - suppress status messages
  --version             Show version and exit
```

### Examples

```bash
# Jiggle every 30 seconds
./jiggler.py -i 30

# Jiggle every 2 minutes, move 5 pixels
./jiggler.py -i 120 -d 5

# Run for 30 minutes then stop
./jiggler.py -t 30

# Use circular pattern every 45 seconds
./jiggler.py -p circular -i 45

# Random pattern in quiet mode
./jiggler.py -p random -q

# Aggressive jiggling for presentations
./jiggler.py -i 30 -d 10 -p circular
```

## Movement Patterns

### Gentle (default)
Moves the mouse right by specified distance, then immediately back. Virtually invisible with default 1-pixel distance.

### Circular
Moves the mouse in a small circle around its current position. More noticeable but still subtle with small distances.

### Random
Random small movements in different directions. Natural-looking movement pattern.

## Use Cases

- **Long-running processes**: Keep your Mac awake during long downloads, uploads, or processing tasks
- **Presentations**: Prevent screen from sleeping during demos or presentations
- **Remote sessions**: Keep remote desktop connections active
- **Monitoring**: Keep display on while monitoring dashboards or logs
- **Video calls**: Prevent sleep during long meetings (when not actively using keyboard/mouse)

## How It Works

The jiggler uses macOS's native Core Graphics framework (`Quartz.CoreGraphics`) to:
1. Get the current mouse position
2. Move the mouse by a small amount
3. Optionally return it to the original position
4. Wait for the specified interval
5. Repeat

This method is:
- **Efficient**: Native API calls with minimal CPU usage
- **Reliable**: Works flawlessly on all Mac machines
- **Safe**: No third-party dependencies or external executables
- **Respectful**: Returns mouse to original position (in gentle/circular modes)

## Stopping the Jiggler

Press `Ctrl+C` to stop the jiggler gracefully. It will display statistics about the run:
- Total number of jiggles performed
- Total runtime

## Troubleshooting

### "Import Quartz could not be resolved"

Make sure the virtual environment is set up correctly:
```bash
# From the project directory
source venv/bin/activate
pip install -r requirements.txt
deactivate
```

Or run the install script:
```bash
./install.sh
```

### Permission Issues

On macOS 10.14 (Mojave) and later, you may need to grant Accessibility permissions:
1. Open System Preferences → Security & Privacy → Privacy tab
2. Select "Accessibility" in the left sidebar
3. Click the lock to make changes
4. Add Terminal (or iTerm2, or your terminal app) to the list
5. Restart your terminal

### Script Not Found

If you get "command not found" after installation:
```bash
# Check if /usr/local/bin is in your PATH
echo $PATH

# If not, add to ~/.zshrc or ~/.bash_profile
export PATH="/usr/local/bin:$PATH"
```

## Uninstallation

```bash
# Remove symlink
sudo rm /usr/local/bin/jiggler

# Optionally remove Python package
pip3 uninstall pyobjc-framework-Quartz
```

## Technical Details

- **Language**: Python 3
- **Framework**: Quartz.CoreGraphics (Core Graphics)
- **APIs Used**:
  - `CGEventCreateMouseEvent`: Create mouse movement events
  - `CGEventPost`: Post events to the system
  - `CGEventGetLocation`: Get current cursor position
- **CPU Usage**: < 0.1% during idle, brief spike during jiggle
- **Memory Usage**: ~15-20 MB

## License

MIT License - Feel free to use, modify, and distribute.

## Contributing

Contributions are welcome! Feel free to submit issues or pull requests.

## Author

Created for Mac users who need a reliable, native mouse jiggler solution.

## Changelog

### v1.0.0 (2025-01-29)
- Initial release
- Support for multiple movement patterns
- Configurable intervals and durations
- Native macOS Core Graphics implementation
- Graceful shutdown handling
