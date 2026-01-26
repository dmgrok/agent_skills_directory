#!/usr/bin/env python3
"""
Build standalone executables for the skills CLI.

Creates single-file executables that don't require Python to be installed.
Supports Windows, macOS, and Linux.

Usage:
    python scripts/build_standalone.py [--onefile] [--clean]

Requirements:
    pip install pyinstaller

Output:
    dist/skills         (Unix)
    dist/skills.exe     (Windows)
"""

import argparse
import platform
import shutil
import subprocess
import sys
from pathlib import Path

# Project root
ROOT = Path(__file__).parent.parent
DIST_DIR = ROOT / "dist"
BUILD_DIR = ROOT / "build"


def check_pyinstaller():
    """Check if PyInstaller is installed."""
    try:
        import PyInstaller
        return True
    except ImportError:
        return False


def get_platform_suffix():
    """Get platform-specific suffix for the executable."""
    system = platform.system().lower()
    machine = platform.machine().lower()
    
    if system == "darwin":
        if machine == "arm64":
            return "macos-arm64"
        return "macos-x64"
    elif system == "windows":
        return "windows-x64"
    elif system == "linux":
        return "linux-x64"
    return f"{system}-{machine}"


def build_executable(onefile: bool = True, include_validation: bool = False):
    """Build the standalone executable."""
    
    print(f"🔨 Building skills CLI for {platform.system()}...")
    
    # Base PyInstaller command
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name", "skills",
        "--noconfirm",
        "--clean",
        # Hidden imports for dynamic modules
        "--hidden-import", "cli.validate",
        "--hidden-import", "cli.loader",
        # Entry point
        str(ROOT / "cli" / "skills.py"),
    ]
    
    if onefile:
        cmd.append("--onefile")
    else:
        cmd.append("--onedir")
    
    # Add validation libraries if requested
    if include_validation:
        cmd.extend([
            "--hidden-import", "detect_secrets",
            "--hidden-import", "semver",
            "--hidden-import", "rapidfuzz",
        ])
    
    # Note: Don't use --target-arch universal2 unless Python itself is universal
    # GitHub Actions runners handle this by using separate Intel/ARM runners
    
    # Run PyInstaller
    print(f"Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, cwd=ROOT)
    
    if result.returncode != 0:
        print("❌ Build failed!")
        return False
    
    # Rename with platform suffix
    suffix = get_platform_suffix()
    exe_name = "skills.exe" if platform.system() == "Windows" else "skills"
    src = DIST_DIR / exe_name
    
    if onefile and src.exists():
        dst_name = f"skills-{suffix}" + (".exe" if platform.system() == "Windows" else "")
        dst = DIST_DIR / dst_name
        shutil.move(src, dst)
        print(f"✅ Built: {dst}")
        print(f"   Size: {dst.stat().st_size / 1024 / 1024:.1f} MB")
    else:
        print(f"✅ Built: {DIST_DIR / exe_name}")
    
    return True


def clean():
    """Clean build artifacts."""
    print("🧹 Cleaning build artifacts...")
    
    for dir_path in [BUILD_DIR, DIST_DIR]:
        if dir_path.exists():
            shutil.rmtree(dir_path)
            print(f"   Removed: {dir_path}")
    
    spec_file = ROOT / "skills.spec"
    if spec_file.exists():
        spec_file.unlink()
        print(f"   Removed: {spec_file}")
    
    print("✅ Clean complete")


def main():
    parser = argparse.ArgumentParser(description="Build standalone skills CLI executable")
    parser.add_argument("--onefile", action="store_true", default=True,
                        help="Create single-file executable (default)")
    parser.add_argument("--onedir", action="store_true",
                        help="Create directory with executable and dependencies")
    parser.add_argument("--with-validation", action="store_true",
                        help="Include validation libraries (larger binary)")
    parser.add_argument("--clean", action="store_true",
                        help="Clean build artifacts")
    
    args = parser.parse_args()
    
    if args.clean:
        clean()
        return
    
    if not check_pyinstaller():
        print("❌ PyInstaller not installed. Run: pip install pyinstaller")
        sys.exit(1)
    
    onefile = not args.onedir
    success = build_executable(onefile=onefile, include_validation=args.with_validation)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
