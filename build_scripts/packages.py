from common import SimpleRustPackage, InstallAll, Release, Tool


class bat(SimpleRustPackage, Tool):
    version = "0.24.0"
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
    homepage = "https://github.com/sharkdp/pastel"
    description = "pastel is a command-line Tool to generate, analyze, convert and manipulate colors. It supports many different color formats and color spaces like RGB (sRGB HSL, CIELAB, CIELCh) as well as ANSI 8-bit and 24-bit representations."


class fd(SimpleRustPackage, Tool):
    version = "9.0.0"
    homepage = "https://github.com/sharkdp/fd"
    description = "fd is a program to find entries in your filesystem. It is a simple, fast and user-friendly alternative to find"


class procs(SimpleRustPackage, Tool):
    version = "0.14.4"
    homepage = "https://github.com/dalance/procs"
    description = "modern replacement for ps"


class grex(SimpleRustPackage, Tool):
    version = "1.4.4"
    homepage = "https://github.com/pemistahl/grex"
    description = "grex is meant to simplify the tedious task of creating regular expressions. It does so by automatically generating a single regular expression from user-provided test cases."


class broot(SimpleRustPackage, Tool):
    version = "1.32.0"
    homepage = "https://github.com/Canop/broot"
    description = "A better way to navigate directories"


class exa(SimpleRustPackage, Tool):
    version = "0.10.1"
    homepage = "https://github.com/ogham/exa"
    description = "exa is a modern replacement for the venerable file-listing command-line program ls"


class sd(SimpleRustPackage, Tool):
    version = "1.0.0"
    homepage = "https://github.com/chmln/sd"
    description = "sd is an intuitive find & replace CLI."


class dust(SimpleRustPackage, Tool):
    version = "0.9.0"
    homepage = "https://github.com/bootandy/dust"
    description = "Dust is a more intuitive version of `du`, used for displaying disk usage statistics."


class ripgrep(SimpleRustPackage, Tool):
    binary_names = ["rg"]
    version = "14.1.0"
    homepage = "https://github.com/BurntSushi/ripgrep"
    description = "ripgrep is a line-oriented search Tool that recursively searches the current directory for a regex pattern."


class bottom(SimpleRustPackage, Tool):
    binary_names = ["btm"]
    version = "1.32.0"
    homepage = "https://github.com/Canop/broot"
    description = "A better way to navigate directories"


class erdtree(SimpleRustPackage, Tool):
    package_name = "erdtree"
    binary_names = ["erd"]
    version = "3.1.2"
    homepage = "https://github.com/solidiquis/erdtree"
    description = "A modern, vibrant, and multi-threaded file-tree visualizer and disk usage analyzer that respects hidden files and .gitignore rules by default - basically if tree and du had a baby."


class release(Release, Tool):
    package_name = 'release'
    version = "1.0.0"
    homepage = "https://github.com/appcove/developer-software"
    description = "This package install neccesary files for AppcoveDevSoftware"


class delta(SimpleRustPackage, Tool):
    package_name = "delta"
    version = "0.16.5"
    homepage = "https://github.com/dandavison/delta"
    description = "Modern CLI git diff analizer (requires manual setup)"


class jaq(SimpleRustPackage, Tool):
    package_name = "jaq"
    version = "1.3.0"
    homepage = "https://github.com/01mf02/jaq"
    description = "A jq clone focussed on correctness, speed, and simplicity"


class install_everything(InstallAll, Tool):
    package_name = 'everything'
    version = "1.0.1"
    depends = "fzf, jq, tig, git, git-lfs, sshfs, vim, rsync, curl, tree"
    homepage = "https://github.com/appcove/developer-software"
    description = "This package install all the available tools in AppcoveDevSoftware"
