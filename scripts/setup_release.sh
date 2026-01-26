#!/bin/bash
# Setup script for Homebrew tap and first release
# Run this after creating the homebrew-tap repo on GitHub

set -e

GITHUB_USER="dmgrok"
MAIN_REPO="agent_skills_directory"
TAP_REPO="homebrew-tap"
VERSION="${1:-0.1.0}"

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
NC='\033[0m'

info() { printf "${BLUE}==>${NC} %s\n" "$1"; }
success() { printf "${GREEN}==>${NC} %s\n" "$1"; }
warn() { printf "${YELLOW}==>${NC} %s\n" "$1"; }
error() { printf "${RED}Error:${NC} %s\n" "$1" >&2; exit 1; }

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
MAIN_DIR="$(dirname "$SCRIPT_DIR")"
PARENT_DIR="$(dirname "$MAIN_DIR")"

echo ""
echo "╔═══════════════════════════════════════════════════════════╗"
echo "║     Agent Skills - Homebrew Tap & Release Setup           ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo ""

# Step 1: Check prerequisites
info "Checking prerequisites..."

if ! command -v git &> /dev/null; then
    error "git is not installed"
fi

if ! command -v gh &> /dev/null; then
    warn "GitHub CLI (gh) not installed. Some steps will need manual action."
    warn "Install with: brew install gh"
    HAS_GH=false
else
    HAS_GH=true
fi

# Step 2: Check if homebrew-tap repo exists on GitHub
info "Checking if ${GITHUB_USER}/${TAP_REPO} exists on GitHub..."

if $HAS_GH; then
    if gh repo view "${GITHUB_USER}/${TAP_REPO}" &> /dev/null; then
        success "Repo ${GITHUB_USER}/${TAP_REPO} exists"
    else
        info "Creating ${GITHUB_USER}/${TAP_REPO} on GitHub..."
        gh repo create "${GITHUB_USER}/${TAP_REPO}" --public --description "Homebrew formulae for ${GITHUB_USER} projects"
        success "Created ${GITHUB_USER}/${TAP_REPO}"
    fi
else
    echo ""
    warn "Please create the repo manually:"
    echo "  1. Go to: https://github.com/new"
    echo "  2. Name: ${TAP_REPO}"
    echo "  3. Make it Public"
    echo "  4. Don't initialize with README"
    echo ""
    read -p "Press Enter after creating the repo..."
fi

# Step 3: Clone and populate homebrew-tap
info "Setting up local homebrew-tap..."

TAP_DIR="${PARENT_DIR}/${TAP_REPO}"

if [ -d "$TAP_DIR" ]; then
    warn "Directory ${TAP_DIR} already exists, updating..."
    cd "$TAP_DIR"
    git pull origin main 2>/dev/null || git pull origin master 2>/dev/null || true
else
    cd "$PARENT_DIR"
    git clone "https://github.com/${GITHUB_USER}/${TAP_REPO}.git" || \
    git clone "git@github.com:${GITHUB_USER}/${TAP_REPO}.git"
fi

# Copy formula files
info "Copying formula files..."
cp -r "${MAIN_DIR}/homebrew-tap/"* "${TAP_DIR}/" 2>/dev/null || true

cd "$TAP_DIR"
git add .
git commit -m "feat: add skills formula v${VERSION}" 2>/dev/null || warn "No changes to commit in tap"
git push origin main 2>/dev/null || git push origin master 2>/dev/null || git push -u origin main

success "Homebrew tap updated"

# Step 4: Commit main repo changes and create release
info "Preparing main repository for release..."

cd "$MAIN_DIR"

# Check for uncommitted changes
if [ -n "$(git status --porcelain)" ]; then
    info "Committing changes in main repo..."
    git add .
    git commit -m "feat: standalone builds, install script, homebrew tap support"
fi

# Push to main
git push origin main 2>/dev/null || git push

# Create and push tag
info "Creating release tag v${VERSION}..."

if git rev-parse "v${VERSION}" >/dev/null 2>&1; then
    warn "Tag v${VERSION} already exists"
    read -p "Delete and recreate? (y/N) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        git tag -d "v${VERSION}"
        git push origin --delete "v${VERSION}" 2>/dev/null || true
    else
        error "Aborted. Use a different version: ./scripts/setup_release.sh 0.1.1"
    fi
fi

git tag "v${VERSION}"
git push origin "v${VERSION}"

success "Tag v${VERSION} pushed!"

# Step 5: Summary
echo ""
echo "╔═══════════════════════════════════════════════════════════╗"
echo "║                      🎉 All Done!                         ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo ""
echo "GitHub Actions is now building binaries for all platforms."
echo "This takes about 5-10 minutes."
echo ""
echo "Monitor progress at:"
echo "  https://github.com/${GITHUB_USER}/${MAIN_REPO}/actions"
echo ""
echo "Once complete, users can install with:"
echo ""
echo "  ${GREEN}# One-liner (any platform)${NC}"
echo "  curl -fsSL https://raw.githubusercontent.com/${GITHUB_USER}/${MAIN_REPO}/main/install.sh | sh"
echo ""
echo "  ${GREEN}# Homebrew (macOS/Linux)${NC}"
echo "  brew install ${GITHUB_USER}/tap/skills"
echo ""
echo "  ${GREEN}# Direct download${NC}"
echo "  https://github.com/${GITHUB_USER}/${MAIN_REPO}/releases/latest"
echo ""

# Optional: Open browser to watch the action
if $HAS_GH; then
    read -p "Open GitHub Actions in browser? (Y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Nn]$ ]]; then
        open "https://github.com/${GITHUB_USER}/${MAIN_REPO}/actions" 2>/dev/null || \
        xdg-open "https://github.com/${GITHUB_USER}/${MAIN_REPO}/actions" 2>/dev/null || \
        echo "Open: https://github.com/${GITHUB_USER}/${MAIN_REPO}/actions"
    fi
fi
