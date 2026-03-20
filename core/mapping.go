package core

import "strings"

type PackageMap struct {
	Arch   string
	Debian string
	Fedora string
}

var packageMapping = map[string]PackageMap{
	"python":           {Arch: "python", Debian: "python3", Fedora: "python3"},
	"python-pip":       {Arch: "python-pip", Debian: "python3-pip", Fedora: "python3-pip"},
	"nodejs":           {Arch: "nodejs", Debian: "nodejs", Fedora: "nodejs"},
	"npm":              {Arch: "npm", Debian: "npm", Fedora: "npm"},
	"go":               {Arch: "go", Debian: "golang-go", Fedora: "golang"},
	"rust":             {Arch: "rust", Debian: "rustc", Fedora: "rust"},
	"cargo":            {Arch: "cargo", Debian: "cargo", Fedora: "cargo"},
	"openjdk":          {Arch: "jdk-openjdk", Debian: "default-jdk", Fedora: "java-21-openjdk-devel"},
	"dotnet":           {Arch: "dotnet-sdk", Debian: "dotnet-sdk-8.0", Fedora: "dotnet-sdk-8.0"},
	"php":              {Arch: "php", Debian: "php", Fedora: "php"},
	"ruby":             {Arch: "ruby", Debian: "ruby-full", Fedora: "ruby"},
	"lua":              {Arch: "lua", Debian: "lua5.4", Fedora: "lua"},
	"gcc":              {Arch: "gcc", Debian: "gcc", Fedora: "gcc"},
	"clang":            {Arch: "clang", Debian: "clang", Fedora: "clang"},
	"cmake":            {Arch: "cmake", Debian: "cmake", Fedora: "cmake"},
	"make":             {Arch: "make", Debian: "make", Fedora: "make"},
	"git":              {Arch: "git", Debian: "git", Fedora: "git"},
	"curl":             {Arch: "curl", Debian: "curl", Fedora: "curl"},
	"wget":             {Arch: "wget", Debian: "wget", Fedora: "wget"},
	"unzip":            {Arch: "unzip", Debian: "unzip", Fedora: "unzip"},
	"zip":              {Arch: "zip", Debian: "zip", Fedora: "zip"},
	"ripgrep":          {Arch: "ripgrep", Debian: "ripgrep", Fedora: "ripgrep"},
	"fd":               {Arch: "fd", Debian: "fd-find", Fedora: "fd-find"},
	"fzf":              {Arch: "fzf", Debian: "fzf", Fedora: "fzf"},
	"bat":              {Arch: "bat", Debian: "bat", Fedora: "bat"},
	"eza":              {Arch: "eza", Debian: "exa", Fedora: "eza"},
	"tmux":             {Arch: "tmux", Debian: "tmux", Fedora: "tmux"},
	"zsh":              {Arch: "zsh", Debian: "zsh", Fedora: "zsh"},
	"fish":             {Arch: "fish", Debian: "fish", Fedora: "fish"},
	"alacritty":        {Arch: "alacritty", Debian: "alacritty", Fedora: "alacritty"},
	"kitty":            {Arch: "kitty", Debian: "kitty", Fedora: "kitty"},
	"neovim":           {Arch: "neovim", Debian: "neovim", Fedora: "neovim"},
	"vim":              {Arch: "vim", Debian: "vim", Fedora: "vim-enhanced"},
	"emacs":            {Arch: "emacs", Debian: "emacs", Fedora: "emacs"},
	"docker":           {Arch: "docker", Debian: "docker.io", Fedora: "docker"},
	"podman":           {Arch: "podman", Debian: "podman", Fedora: "podman"},
	"kubectl":          {Arch: "kubectl", Debian: "kubectl", Fedora: "kubectl"},
	"firefox":          {Arch: "firefox", Debian: "firefox-esr", Fedora: "firefox"},
	"chromium":         {Arch: "chromium", Debian: "chromium", Fedora: "chromium"},
	"brave":            {Arch: "brave-bin", Debian: "brave-browser", Fedora: "brave-browser"},
	"vivaldi":          {Arch: "vivaldi", Debian: "vivaldi-stable", Fedora: "vivaldi-stable"},
	"opera":            {Arch: "opera", Debian: "opera-stable", Fedora: "opera-stable"},
	"librewolf":        {Arch: "librewolf", Debian: "librewolf", Fedora: "librewolf"},
	"vlc":              {Arch: "vlc", Debian: "vlc", Fedora: "vlc"},
	"mpv":              {Arch: "mpv", Debian: "mpv", Fedora: "mpv"},
	"ffmpeg":           {Arch: "ffmpeg", Debian: "ffmpeg", Fedora: "ffmpeg"},
	"obs-studio":       {Arch: "obs-studio", Debian: "obs-studio", Fedora: "obs-studio"},
	"gimp":             {Arch: "gimp", Debian: "gimp", Fedora: "gimp"},
	"inkscape":         {Arch: "inkscape", Debian: "inkscape", Fedora: "inkscape"},
	"blender":          {Arch: "blender", Debian: "blender", Fedora: "blender"},
	"kdenlive":         {Arch: "kdenlive", Debian: "kdenlive", Fedora: "kdenlive"},
	"audacity":         {Arch: "audacity", Debian: "audacity", Fedora: "audacity"},
	"libreoffice":      {Arch: "libreoffice-fresh", Debian: "libreoffice", Fedora: "libreoffice"},
	"thunderbird":      {Arch: "thunderbird", Debian: "thunderbird", Fedora: "thunderbird"},
	"discord":          {Arch: "discord", Debian: "discord", Fedora: "discord"},
	"telegram":         {Arch: "telegram-desktop", Debian: "telegram-desktop", Fedora: "telegram-desktop"},
	"steam":            {Arch: "steam", Debian: "steam-installer", Fedora: "steam"},
	"lutris":           {Arch: "lutris", Debian: "lutris", Fedora: "lutris"},
	"heroic":           {Arch: "heroic-games-launcher-bin", Debian: "heroic", Fedora: "heroic-games-launcher-bin"},
	"mangohud":         {Arch: "mangohud", Debian: "mangohud", Fedora: "mangohud"},
	"flatpak":          {Arch: "flatpak", Debian: "flatpak", Fedora: "flatpak"},
	"postgresql":       {Arch: "postgresql", Debian: "postgresql", Fedora: "postgresql-server"},
	"mysql":            {Arch: "mariadb", Debian: "default-mysql-server", Fedora: "community-mysql-server"},
	"mariadb":          {Arch: "mariadb", Debian: "mariadb-server", Fedora: "mariadb-server"},
	"mongodb":          {Arch: "mongodb-bin", Debian: "mongodb", Fedora: "mongodb"},
	"redis":            {Arch: "redis", Debian: "redis-server", Fedora: "redis"},
	"sqlite":           {Arch: "sqlite", Debian: "sqlite3", Fedora: "sqlite"},
	"vscode":           {Arch: "code", Debian: "code", Fedora: "code"},
	"vscodium":         {Arch: "codium", Debian: "codium", Fedora: "codium"},
	"android-studio":   {Arch: "android-studio", Debian: "android-studio", Fedora: "android-studio"},
}

var explicitFallbacks = map[Distro]map[string][]string{
	Arch: {
		"code":           {"codium"},
		"google-chrome":  {"chromium", "brave-bin"},
		"firefox-esr":    {"firefox"},
		"docker.io":      {"docker", "podman"},
		"default-jdk":    {"jdk-openjdk"},
		"fd-find":        {"fd"},
		"exa":            {"eza"},
		"steam-installer": {"steam"},
	},
	Debian: {
		"code":               {"codium", "vscodium"},
		"google-chrome":      {"chromium", "brave-browser"},
		"firefox":            {"firefox-esr"},
		"docker":             {"docker.io", "podman"},
		"jdk-openjdk":        {"default-jdk"},
		"fd":                 {"fd-find"},
		"eza":                {"exa"},
		"steam":              {"steam-installer"},
		"postgresql-server":  {"postgresql"},
	},
	Fedora: {
		"code":            {"codium"},
		"google-chrome":   {"chromium", "brave-browser"},
		"firefox-esr":     {"firefox"},
		"docker.io":       {"docker", "podman"},
		"default-jdk":     {"java-21-openjdk-devel"},
		"fd-find":         {"fd"},
		"exa":             {"eza"},
		"steam-installer": {"steam"},
	},
}

var heuristicFallbacks = map[string][]string{
	"chrome":   {"chromium", "brave-browser", "firefox"},
	"brave":    {"chromium", "firefox"},
	"vivaldi":  {"chromium", "firefox"},
	"opera":    {"chromium", "firefox"},
	"code":     {"code", "codium", "neovim"},
	"vscode":   {"code", "codium"},
	"codium":   {"codium", "code"},
	"jdk":      {"default-jdk", "openjdk", "java-21-openjdk-devel"},
	"java":     {"default-jdk", "openjdk"},
	"docker":   {"docker", "docker.io", "podman"},
	"mysql":    {"mariadb-server", "default-mysql-server"},
	"postgres": {"postgresql", "postgresql-server"},
	"telegram": {"telegram-desktop"},
}

func MapPackage(name string, target Distro) string {
	n := normalizePkg(name)
	for _, m := range packageMapping {
		if normalizePkg(m.Arch) == n || normalizePkg(m.Debian) == n || normalizePkg(m.Fedora) == n {
			mapped := targetForDistro(m, target)
			if mapped != "" {
				return mapped
			}
		}
	}
	return name
}

func PackageFallbacks(name string, target Distro) []string {
	n := normalizePkg(name)
	seen := map[string]struct{}{}
	var out []string
	add := func(pkg string) {
		pkg = strings.TrimSpace(pkg)
		if pkg == "" {
			return
		}
		k := normalizePkg(pkg)
		if k == n {
			return
		}
		if _, ok := seen[k]; ok {
			return
		}
		seen[k] = struct{}{}
		out = append(out, pkg)
	}

	for _, m := range packageMapping {
		if normalizePkg(m.Arch) == n || normalizePkg(m.Debian) == n || normalizePkg(m.Fedora) == n {
			add(targetForDistro(m, target))
		}
	}

	if byDistro, ok := explicitFallbacks[target]; ok {
		if arr, ok := byDistro[n]; ok {
			for _, alt := range arr {
				add(alt)
			}
		}
	}

	for key, arr := range heuristicFallbacks {
		if strings.Contains(n, key) {
			for _, alt := range arr {
				add(alt)
			}
		}
	}

	return out
}

func RecommendPackage(name string, target Distro) string {
	alts := PackageFallbacks(name, target)
	if len(alts) == 0 {
		return ""
	}
	return alts[0]
}

func targetForDistro(m PackageMap, target Distro) string {
	switch target {
	case Arch:
		return m.Arch
	case Debian:
		return m.Debian
	case Fedora:
		return m.Fedora
	default:
		return ""
	}
}

func normalizePkg(name string) string {
	return strings.ToLower(strings.TrimSpace(name))
}
