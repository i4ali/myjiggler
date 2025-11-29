class Jiggler < Formula
  include Language::Python::Virtualenv

  desc "Mac Mouse Jiggler - Prevents your Mac from going to sleep"
  homepage "https://github.com/i4ali/myjiggler"
  url "https://github.com/i4ali/myjiggler/archive/refs/tags/v1.0.0.tar.gz"
  sha256 "ac7e10756d335fbd56b176bb421f149dfe6747fff2536d357ed0001b52d0e8f8"
  license "MIT"
  head "https://github.com/i4ali/myjiggler.git", branch: "main"

  depends_on "python@3.14"
  depends_on :macos

  def install
    # Let pip install dependencies from pyproject.toml
    # This uses pre-built wheels when available
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
