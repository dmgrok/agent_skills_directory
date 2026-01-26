# Homebrew formula for Agent Skills CLI
class Skills < Formula
  desc "The package manager for AI agent skills"
  homepage "https://github.com/dmgrok/agent_skills_directory"
  version "0.1.0"
  license "MIT"

  on_macos do
    # ARM64 binary works on both ARM and Intel (via Rosetta 2)
    url "https://github.com/dmgrok/agent_skills_directory/releases/download/v0.1.0/skills-macos-arm64"
    sha256 "104ecd44821c4454d6e25cd000aac62964ce5b22e43df092bbb92d53943824db"
  end

  on_linux do
    url "https://github.com/dmgrok/agent_skills_directory/releases/download/v0.1.0/skills-linux-x64"
    sha256 "fd75929c34f47f0a587efe6f1d6e67d255bc684e5792bc2b6ebc9ad9d1e3ea5e"
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
