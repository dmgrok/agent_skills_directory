#!/bin/sh
# Agent Skills CLI Installer
# Usage: curl -fsSL https://raw.githubusercontent.com/dmgrok/agent_skills_directory/main/install.sh | sh
#
# This script detects your OS/architecture and installs the appropriate binary.

set -e

REPO="dmgrok/agent_skills_directory"
INSTALL_DIR="${SKILLS_INSTALL_DIR:-$HOME/.local/bin}"
BINARY_NAME="skills"

# Colors (disabled if not interactive)
if [ -t 1 ]; then
    RED='\033[0;31m'
    GREEN='\033[0;32m'
    YELLOW='\033[0;33m'
    BLUE='\033[0;34m'
    NC='\033[0m' # No Color
else
    RED=''
    GREEN=''
    YELLOW=''
    BLUE=''
    NC=''
fi

info() {
    printf "${BLUE}==>${NC} %s\n" "$1"
}

success() {
    printf "${GREEN}==>${NC} %s\n" "$1"
}

warn() {
    printf "${YELLOW}Warning:${NC} %s\n" "$1"
}

error() {
    printf "${RED}Error:${NC} %s\n" "$1" >&2
    exit 1
}

# Detect OS
detect_os() {
    case "$(uname -s)" in
        Linux*)     echo "linux" ;;
        Darwin*)    echo "macos" ;;
        MINGW*|MSYS*|CYGWIN*) echo "windows" ;;
        *)          error "Unsupported operating system: $(uname -s)" ;;
    esac
}

# Detect architecture
detect_arch() {
    case "$(uname -m)" in
        x86_64|amd64)   echo "x64" ;;
        arm64|aarch64)  echo "arm64" ;;
        *)              error "Unsupported architecture: $(uname -m)" ;;
    esac
}

# Get the download URL for the latest release
get_download_url() {
    local os="$1"
    local arch="$2"
    local ext=""
    
    if [ "$os" = "windows" ]; then
        ext=".exe"
    fi
    
    # macOS: Always use ARM64 binary (works on Intel via Rosetta 2)
    # This is because macOS-13 (Intel) GitHub runners were retired
    if [ "$os" = "macos" ]; then
        arch="arm64"
    fi
    
    echo "https://github.com/${REPO}/releases/latest/download/skills-${os}-${arch}${ext}"
}

# Check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Download file
download() {
    local url="$1"
    local dest="$2"
    
    if command_exists curl; then
        curl -fsSL "$url" -o "$dest"
    elif command_exists wget; then
        wget -q "$url" -O "$dest"
    else
        error "Neither curl nor wget found. Please install one of them."
    fi
}

# Main installation
main() {
    info "Installing Agent Skills CLI..."
    
    # Detect platform
    OS=$(detect_os)
    ARCH=$(detect_arch)
    info "Detected platform: ${OS}-${ARCH}"
    
    # Create install directory
    mkdir -p "$INSTALL_DIR"
    
    # Get download URL
    URL=$(get_download_url "$OS" "$ARCH")
    info "Downloading from: $URL"
    
    # Download binary
    TEMP_FILE=$(mktemp)
    if ! download "$URL" "$TEMP_FILE"; then
        rm -f "$TEMP_FILE"
        error "Failed to download. Check if a release exists for your platform."
    fi
    
    # Install binary
    DEST="${INSTALL_DIR}/${BINARY_NAME}"
    if [ "$OS" = "windows" ]; then
        DEST="${DEST}.exe"
    fi
    
    mv "$TEMP_FILE" "$DEST"
    chmod +x "$DEST"
    
    success "Installed to: $DEST"
    
    # Check if install dir is in PATH
    case ":$PATH:" in
        *":$INSTALL_DIR:"*)
            success "Installation complete!"
            ;;
        *)
            warn "$INSTALL_DIR is not in your PATH"
            echo ""
            echo "Add it to your shell profile:"
            echo ""
            echo "  # For bash (~/.bashrc or ~/.bash_profile):"
            echo "  export PATH=\"\$HOME/.local/bin:\$PATH\""
            echo ""
            echo "  # For zsh (~/.zshrc):"
            echo "  export PATH=\"\$HOME/.local/bin:\$PATH\""
            echo ""
            echo "  # For fish (~/.config/fish/config.fish):"
            echo "  set -gx PATH \$HOME/.local/bin \$PATH"
            echo ""
            ;;
    esac
    
    # Verify installation
    if [ -x "$DEST" ]; then
        echo ""
        success "Run 'skills --help' to get started!"
        echo ""
        echo "Quick start:"
        echo "  skills search \"web scraping\"    # Find skills"
        echo "  skills install anthropic/web-researcher  # Install a skill"
        echo "  skills list                      # List installed skills"
    fi
}

# Run
main "$@"
