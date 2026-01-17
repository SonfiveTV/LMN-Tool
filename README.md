# LMN Tool (Lightweight Mod Navigation Tool)

Easily update and toggle Balatro mods, save/load mod profiles, and launch straight into the game.

---

## Features

- Toggle mods on/off with a simple menu  
- Update GitHub-based mods with a single command  
- Save and load mod profiles for different setups  
- Launch Balatro directly from the manager  
- Lightweight and Linux-friendly design  

---

## Quick Installation (Release ZIP)

1. **Download the latest release** from [GitHub Releases](https://github.com/yourusername/LMN-Tool/releases).

2. **Extract the ZIP** into the **parent folder of your `Mods/` directory**, so the structure looks like this:
```
<Balatro Parent Folder>/
├── Mods/
│ ├── <your installed mods>
└── tools/
  ├── LMN-Tool.sh
  ├── config.sh
  └── profiles/ # can be empty initially
```

3. **Make the scripts executable** (if needed):
```bash
chmod +x tools/*.sh
```
4. **Run the tool**:
``` bash
./tools/mod-toggle.sh
```

## Usage
**Toggle mods**: Enter numbers separated by spaces (e.g., `1 4 7`)

**Update mods**: Press `U` to pull updates for GitHub-based mods

**Save profile**: Press `S` to save the current enabled/disabled setup

**Load profile**: Press `L` to select and apply a saved profile

**Launch Balatro**: Press `O` to start the game

**Quit**: Press `Q` to exit
