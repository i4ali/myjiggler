class Jiggler < Formula
  include Language::Python::Virtualenv

  desc "Mac Mouse Jiggler - Prevents your Mac from going to sleep"
  homepage "https://github.com/i4ali/myjiggler"
  url "https://github.com/i4ali/myjiggler/archive/refs/tags/v1.0.0.tar.gz"
  sha256 "REPLACE_WITH_ACTUAL_SHA256_AFTER_GITHUB_RELEASE"
  license "MIT"
  head "https://github.com/i4ali/myjiggler.git", branch: "main"

  depends_on "python@3.14"
  depends_on :macos

  # PyObjC dependency - get actual SHA256 from PyPI
  # https://pypi.org/project/pyobjc-framework-Quartz/12.1/#files
  resource "pyobjc-core" do
    url "https://files.pythonhosted.org/packages/48/d8/c28b3e39a59e11ea05e9bd50c6d1afd5a334d90c6f3afb7d5cd651ac032f/pyobjc_core-12.1.tar.gz"
    sha256 "f0e8c149ba2a6c75c5a35c520fa7ac38439f17b40cbc3c2ffef5f3da2d28656f"
  end

  resource "pyobjc-framework-Cocoa" do
    url "https://files.pythonhosted.org/packages/03/61/e6c8fb8f5c4e58ea5ec84f3e29c1e5e39f5c851d24c9e38a3e4d9a67e37c/pyobjc_framework_cocoa-12.1.tar.gz"
    sha256 "5a3a9c8385fb4e5ac3dbcd9dac52fc17ed1a2913a4b03f22dbaafda76f03bedd"
  end

  resource "pyobjc-framework-Quartz" do
    url "https://files.pythonhosted.org/packages/f4/ba/99ebcf6cfd87a8aba92f1f7b06c40766cb5bf76fc0d80f3ae4fe1cf72962/pyobjc_framework_quartz-12.1.tar.gz"
    sha256 "a8c8d0e5e8e56652ecd5a6c35e2eaad50c1c01dc96b5d5e08a61c8bb4f3f8fe6"
  end

  def install
    virtualenv_install_with_resources
  end

  def caveats
    <<~EOS
      On first run, you may need to grant Accessibility permissions:
        System Settings → Privacy & Security → Accessibility
        Add your terminal app to the list

      This allows the jiggler to control the mouse cursor.
    EOS
  end

  test do
    assert_match "Mac Mouse Jiggler", shell_output("#{bin}/jiggler --help")
    assert_match "1.0.0", shell_output("#{bin}/jiggler --version")
  end
end
