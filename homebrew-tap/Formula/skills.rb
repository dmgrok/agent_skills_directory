# Homebrew formula for Agent Skills CLI
# To use: brew tap dmgrok/tap && brew install skills
# Or: brew install dmgrok/tap/skills
#
# This formula is auto-updated by GitHub Actions when a new release is published.

class Skills < Formula
  desc "The package manager for AI agent skills"
  homepage "https://github.com/dmgrok/agent_skills_directory"
  version "0.1.0"
  license "MIT"

  on_macos do
    on_arm do
      url "https://github.com/dmgrok/agent_skills_directory/releases/latest/download/skills-macos-arm64"
      sha256 "PENDING_FIRST_RELEASE"
    end
    on_intel do
      url "https://github.com/dmgrok/agent_skills_directory/releases/latest/download/skills-macos-x64"
      sha256 "PENDING_FIRST_RELEASE"
    end
  end

  on_linux do
    url "https://github.com/dmgrok/agent_skills_directory/releases/latest/download/skills-linux-x64"
    sha256 "PENDING_FIRST_RELEASE"
  end

  def install
    if OS.mac?
      if Hardware::CPU.arm?
        bin.install "skills-macos-arm64" => "skills"
      else
        bin.install "skills-macos-x64" => "skills"
      end
    else
      bin.install "skills-linux-x64" => "skills"
    end
  end

  test do
    assert_match "skills", shell_output("#{bin}/skills --version")
  end
end
