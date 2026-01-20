# LMN Tool (Lightweight Mod Navigation Tool)

Easily update and toggle Balatro mods, save/load mod profiles, and launch straight into the game.

---
## Requirements
- Linux (tested on SteamOS)
- MacOS
- git (for updating mods via the manager)
- bash (default shell)


## Features
- Toggle mods on/off with a simple menu  
- Update GitHub-based mods with a single command  
- Save and load mod profiles for different setups  
- Launch Balatro directly from the manager  
- Lightweight and Linux-friendly design  

---

## Quick Installation

1. **Clone this repo into your Mods parent folder**
```bash
git clone https://github.com/SonfiveTV/LMN-Tool.git
```

The structure should look like this:
```
<Balatro Parent Folder>/
├── Mods/
│ ├── <your installed mods>
└── LMN-Tool/
  ├── LMN-Tool.sh
  ├── config.sh
  └── profiles/ # can be empty initially
```

2. **Make the scripts executable** (if needed):
```bash
chmod +x tools/*.sh
```
3. **Run the tool**:
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

> **Note:** Some folders like `lovely`, `Steamodded`, and `smods` are protected and will not show in the mod menu by default.


## Configuration
You can edit `tools/config.sh` to adjust paths, protected mods, update exclusions, or change how Balatro is launched. The default setup works for most Linux users.

## Troubleshooting
- If the tool does not launch Balatro, ensure Steam is installed and logged in.
- Make sure the `tools/*.sh` scripts are executable (`chmod +x tools/*.sh`).
- Git must be installed for updating mods.




