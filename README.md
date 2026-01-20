# LMN Tool (Lightweight Mod Navigation Tool)

Easily update and toggle Balatro mods, save/load mod profiles, and launch straight into Balatro.

---
## Requirements
- python
- git (for updating mods via the manager)


## Features
- Toggle mods on/off with a simple menu  
- Update GitHub-based mods with a single command  
- Save and load mod profiles for different setups  
- Launch Balatro directly from the manager  

---

## Quick Installation

**(Option 1) Clone this repo into your Mod's parent folder**
```bash
git clone https://github.com/SonfiveTV/LMN-Tool.git
```

**(Option 2) Download and extract the latest Release into your Mod's parent folder**

The structure should look like this:
```
<Balatro Parent Folder>/
├── Mods/
│ ├── <your installed mods>
└── LMN-Tool/
  ├── LMN-Tool.py
  └── profiles/
```

## Configuration
If your folder setup is the same as shown above, no path configuration should be required, however if you would like to have the tool placed elsewhere you will need to define custom paths in `LMN-Tool.py`

`PROTECTED_MODS` is a table containing any mods assumed to always be enabled and/or hidden from the Mods list. By default this includes `lovely`, `Steamodded`, and `smods`.

`UPDATE_EXCLUDE` is a table containing any Mods you don't want the `Update` function to touch 

## Usage
**Toggle mods**: Enter numbers separated by spaces (e.g., `1 4 7`)<br>
**Update mods**: Press `U` to pull updates for Git cloned mods<br>
**Save profile**: Press `S` to save the current setup as a profile<br>
**Load profile**: Press `L` to select and apply a saved profile<br>
**Launch Balatro**: Press `O` to launch Balatro<br>
**Quit**: Press `Q` to exit<br>



