from common import RustPackage, InstallAll, Tool

class everything(InstallAll, Tool):
    version = "1.1.0"
    depends = "fzf, jq, tig, git, git-lfs, sshfs, vim, rsync, curl, tree"
    homepage = "https://github.com/appcove/developer-software"
    description = "This package install all the available tools in AppcoveDevSoftware"

# Tool Packages
class bat(RustPackage, Tool):
    version = "0.25.0"
    homepage = "https://github.com/sharkdp/bat"
    description = "A cat clone with syntax highlighting and Git integration"

class git_excess(RustPackage, Tool):
    package_name = "git-excess"
    binaries = ["git-sdif", "git-srep", "git-embed", "egit"]
    version = "1.1.0"
    git = "https://github.com/appcove/git-excess"
    homepage = "https://github.com/appcove/git-excess"
    description = "AppCove's internal Git Tools"

class pastel(RustPackage, Tool):
    version = "0.10.0"
    homepage = "https://github.com/sharkdp/pastel"
    description = "pastel is a command-line Tool to generate, analyze, convert and manipulate colors. It supports many different color formats and color spaces like RGB (sRGB HSL, CIELAB, CIELCh) as well as ANSI 8-bit and 24-bit representations."

class fd_find(RustPackage, Tool):
    version = "10.3.0"
    package_name = "fd-find"
    binaries = ["fd"]
    homepage = "https://github.com/sharkdp/fd"
    description = "fd is a program to find entries in your filesystem. It is a simple, fast and user-friendly alternative to find"

class procs(RustPackage, Tool):
    version = "0.14.10"
    homepage = "https://github.com/dalance/procs"
    description = "modern replacement for ps"

class grex(RustPackage, Tool):
    version = "1.4.5"
    homepage = "https://github.com/pemistahl/grex"
    description = "grex is meant to simplify the tedious task of creating regular expressions. It does so by automatically generating a single regular expression from user-provided test cases."

class broot(RustPackage, Tool):
    version = "1.49.1"
    homepage = "https://github.com/Canop/broot"
    description = " A new file manager "

class exa(RustPackage, Tool):
    version = "0.10.1"
    homepage = "https://github.com/ogham/exa"
    description = "exa is a modern replacement for the venerable file-listing command-line program ls"

class sd(RustPackage, Tool):
    version = "1.0.0"
    homepage = "https://github.com/chmln/sd"
    description = "sd is an intuitive find & replace CLI."

class dust(RustPackage, Tool):
    version = "1.2.3"
    package_name = "du-dust"
    binaries = ["dust"]
    homepage = "https://github.com/bootandy/dust"
    description = "Dust is a more intuitive version of `du`, used for displaying disk usage statistics."

class ripgrep(RustPackage, Tool):
    binaries = ["rg"]
    version = "14.1.1"
    homepage = "https://github.com/BurntSushi/ripgrep"
    description = "ripgrep is a line-oriented search Tool that recursively searches the current directory for a regex pattern."

class bottom(RustPackage, Tool):
    binaries = ["btm"]
    version = "0.11.1"
    homepage = "https://github.com/ClementTsang/bottom"
    description = " A customizable cross-platform graphical process/system monitor for the terminal. Supports Linux, macOS, and Windows"

class erdtree(RustPackage, Tool):
    package_name = "erdtree"
    binaries = ["erd"]
    version = "3.1.2"
    homepage = "https://github.com/solidiquis/erdtree"
    description = "A modern, vibrant, and multi-threaded file-tree visualizer and disk usage analyzer that respects hidden files and .gitignore rules by default - basically if tree and du had a baby."

class git_delta(RustPackage, Tool):
    package_name = "git-delta"
    binaries = ["delta"]
    version = "0.18.2"
    homepage = "https://github.com/dandavison/delta"
    description = "Modern CLI git diff analizer (requires manual setup)"

class jaq(RustPackage, Tool):
    package_name = "jaq"
    version = "2.3.0"
    homepage = "https://github.com/01mf02/jaq"
    description = "Just another JSON query tool "
