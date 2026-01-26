# Homebrew formula for Agent Skills CLI
# To use: brew tap dmgrok/tap && brew install skills
# Or: brew install dmgrok/tap/skills
#
# This formula is auto-updated by GitHub Actions when a new release is published.
# Note: ARM64 binary works on Intel Macs via Rosetta 2.

class Skills < Formula
  desc "The package manager for AI agent skills"
  homepage "https://github.com/dmgrok/agent_skills_directory"
  version "0.1.0"
  license "MIT"

  on_macos do
    # ARM64 binary works on both Apple Silicon and Intel (via Rosetta 2)
    url "https://github.com/dmgrok/agent_skills_directory/releases/latest/download/skills-macos-arm64"
    sha256 "PENDING_FIRST_RELEASE"
  end

  on_linux do
    url "https://github.com/dmgrok/agent_skills_directory/releases/latest/download/skills-linux-x64"
    sha256 "PENDING_FIRST_RELEASE"
  end

  def install
    if OS.mac?
      bin.install "skills-macos-arm64" => "skills"
    else
      bin.install "skills-linux-x64" => "skills"
    end
  end

  test do
    assert_match "skills", shell_output("#{bin}/skills --version")
  end
end
