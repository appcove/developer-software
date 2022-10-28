from common import SimpleRustPackage, InstallAll, Release, Tool


class bat(SimpleRustPackage, Tool):
    version = "0.22.1"
    homepage = "https://github.com/sharkdp/bat"
    description = "A cat clone with syntax highlighting and Git integration"


class git_excess(SimpleRustPackage, Tool):
    package_name = "git-excess"
    binary_names = ["git-sdif", "git-srep", "git-embed", "egit"]
    version = "1.0.1"
    homepage = "https://github.com/appcove/git-excess"
    description = "AppCove's internal git Tool"


class pastel(SimpleRustPackage, Tool):
    version = "0.9.0"
    homepage = "https://github.com/sharkdp/pastel/tree/3719824a56fb9eb92eb960068e513b95486756a7"
    description = "pastel is a command-line Tool to generate, analyze, convert and manipulate colors. It supports many different color formats and color spaces like RGB (sRGB HSL, CIELAB, CIELCh) as well as ANSI 8-bit and 24-bit representations."


class fd(SimpleRustPackage, Tool):
    version = "8.4.0"
    homepage = "https://github.com/sharkdp/fd"
    description = "fd is a program to find entries in your filesystem. It is a simple, fast and user-friendly alternative to find"


class procs(SimpleRustPackage, Tool):
    version = "0.13.2"
    homepage = "https://github.com/dalance/procs"
    description = "modern replacement for ps"


class grex(SimpleRustPackage, Tool):
    version = "1.4.0"
    homepage = "https://github.com/pemistahl/grex"
    description = "grex is meant to simplify the tedious task of creating regular expressions. It does so by automatically generating a single regular expression from user-provided test cases."


class broot(SimpleRustPackage, Tool):
    version = "1.16.0"
    homepage = "https://github.com/Canop/broot"
    description = "A better way to navigate directories"


class exa(SimpleRustPackage, Tool):
    version = "0.10.1"
    homepage = "https://github.com/ogham/exa"
    description = "exa is a modern replacement for the venerable file-listing command-line program ls"


class sd(SimpleRustPackage, Tool):
    version = "0.7.6"
    homepage = "https://github.com/chmln/sd"
    description = "sd is an intuitive find & replace CLI."


class dust(SimpleRustPackage, Tool):
    version = "0.8.3"
    homepage = "https://github.com/bootandy/dust"
    description = "Dust is a more intuitive version of `du`, used for displaying disk usage statistics."


class ripgrep(SimpleRustPackage, Tool):
    binary_names = ["rg"]
    version = "13.0.0"
    homepage = "https://github.com/BurntSushi/ripgrep"
    description = "ripgrep is a line-oriented search Tool that recursively searches the current directory for a regex pattern."


class bottom(SimpleRustPackage, Tool):
    binary_names = ["btm"]
    version = "1.16.0"
    homepage = "https://github.com/Canop/broot"
    description = "A better way to navigate directories"


class release(Release, Tool):
    package_name = 'release'
    version = "1.0.0"
    homepage = "https://github.com/appcove/developer-software"
    description = "This package install neccesary files for AppcoveDevSoftware"


class install_everything(InstallAll, Tool):
    package_name = 'everything'
    version = "1.0.0"
    homepage = "https://github.com/appcove/developer-software"
    description = "This package install all the available tools in AppcoveDevSoftware"
