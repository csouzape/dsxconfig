package core

type PackageMap struct {
	Arch   string
	Debian string
	Fedora string
}

var packageMapping = map[string]PackageMap{
	"python":      {Arch: "python", Debian: "python3", Fedora: "python3"},
	"python-pip":  {Arch: "python-pip", Debian: "python3-pip", Fedora: "python3-pip"},
	"neovim":      {Arch: "neovim", Debian: "neovim", Fedora: "neovim"},
	"nodejs":      {Arch: "nodejs", Debian: "nodejs", Fedora: "nodejs"},
	"npm":         {Arch: "npm", Debian: "npm", Fedora: "npm"},
	"docker":      {Arch: "docker", Debian: "docker.io", Fedora: "docker-ce"},
	"vlc":         {Arch: "vlc", Debian: "vlc", Fedora: "vlc"},
	"git":         {Arch: "git", Debian: "git", Fedora: "git"},
	"htop":        {Arch: "htop", Debian: "htop", Fedora: "htop"},
	"curl":        {Arch: "curl", Debian: "curl", Fedora: "curl"},
	"wget":        {Arch: "wget", Debian: "wget", Fedora: "wget"},
	"unzip":       {Arch: "unzip", Debian: "unzip", Fedora: "unzip"},
	"ffmpeg":      {Arch: "ffmpeg", Debian: "ffmpeg", Fedora: "ffmpeg"},
	"obs-studio":  {Arch: "obs-studio", Debian: "obs-studio", Fedora: "obs-studio"},
	"libreoffice": {Arch: "libreoffice-fresh", Debian: "libreoffice", Fedora: "libreoffice"},
	"thunderbird": {Arch: "thunderbird", Debian: "thunderbird", Fedora: "thunderbird"},
	"gimp":        {Arch: "gimp", Debian: "gimp", Fedora: "gimp"},
	"inkscape":    {Arch: "inkscape", Debian: "inkscape", Fedora: "inkscape"},
	"alacritty":   {Arch: "alacritty", Debian: "alacritty", Fedora: "alacritty"},
	"kitty":       {Arch: "kitty", Debian: "kitty", Fedora: "kitty"},
	"fzf":         {Arch: "fzf", Debian: "fzf", Fedora: "fzf"},
	"tmux":        {Arch: "tmux", Debian: "tmux", Fedora: "tmux"},
	"zsh":         {Arch: "zsh", Debian: "zsh", Fedora: "zsh"},
	"fish":        {Arch: "fish", Debian: "fish", Fedora: "fish"},
	"bat":         {Arch: "bat", Debian: "bat", Fedora: "bat"},
	"ripgrep":     {Arch: "ripgrep", Debian: "ripgrep", Fedora: "ripgrep"},
	"fd":          {Arch: "fd", Debian: "fd-find", Fedora: "fd-find"},
	"eza":         {Arch: "eza", Debian: "exa", Fedora: "eza"},
	"flatpak":     {Arch: "flatpak", Debian: "flatpak", Fedora: "flatpak"},
	"steam":       {Arch: "steam", Debian: "steam", Fedora: "steam"},
	"lutris":      {Arch: "lutris", Debian: "lutris", Fedora: "lutris"},
	"mangohud":    {Arch: "mangohud", Debian: "mangohud", Fedora: "mangohud"},
}

// MapPackage receives a package name and target distro, returns the equivalent name
func MapPackage(name string, target Distro) string {
	for _, m := range packageMapping {
		if m.Arch == name || m.Debian == name || m.Fedora == name {
			switch target {
			case Arch:
				return m.Arch
			case Debian:
				return m.Debian
			case Fedora:
				return m.Fedora
			}
		}
	}
	return name
}
