# Homebrew formula for Agent Skills CLI
class Skillsdir < Formula
  desc "The package manager for AI agent skills"
  homepage "https://github.com/dmgrok/agent_skills_directory"
  version "0.1.0"
  license "MIT"

  on_macos do
    # ARM64 binary works on both ARM and Intel (via Rosetta 2)
    url "https://github.com/dmgrok/agent_skills_directory/releases/download/v0.1.0/skillsdir-macos-arm64"
    sha256 "" # Updated automatically by build-standalone.yml on release
  end

  on_linux do
    url "https://github.com/dmgrok/agent_skills_directory/releases/download/v0.1.0/skillsdir-linux-x64"
    sha256 "" # Updated automatically by build-standalone.yml on release
  end

  def install
    if OS.mac?
      bin.install "skillsdir-macos-arm64" => "skillsdir"
    else
      bin.install "skillsdir-linux-x64" => "skillsdir"
    end
  end

  test do
    assert_match "skillsdir", shell_output("#{bin}/skillsdir --version")
  end
end
