#!/usr/bin/env python3
"""
Balatro Mod Terminal
Cross-platform Python version (Linux / macOS / Windows)
"""

import os
import sys
import subprocess
import json
import urllib.request
import time
from pathlib import Path

def set_window_title(title: str):
    """Set the console/terminal window title cross-platform."""
    if sys.platform.startswith("win"):
        # Windows CMD / PowerShell
        os.system(f"title {title}")
    elif sys.platform.startswith("linux") or sys.platform == "darwin":
        # Linux and macOS terminals (ANSI escape sequence)
        print(f"\033]0;{title}\007", end="")

# Call this at the very start of your script
set_window_title("Balatro Mod Terminal")


# ================= CONFIG =================

BASE_DIR = Path(__file__).resolve().parent
PROFILES_DIR = BASE_DIR / "profiles"
MODS_DIR = BASE_DIR.parent / "Mods"
BALATRO_APPID = "2379780"

PROTECTED_MODS = {"lovely", "Steamodded", "smods"}
UPDATE_EXCLUDE = {"PokermonPlus"}

LAUNCH_METHOD = "steam"

MAC_LOVELY_SCRIPT = (
    Path.home()
    / "Library/Application Support/Steam/steamapps/common/Balatro/run_lovely_macos.sh"
)

# -------- Mod index config (NOW SAFE) --------

MOD_INDEX_REPO = "https://api.github.com/repos/skyline69/balatro-mod-index/contents/mods"
CACHE_DIR = BASE_DIR / ".cache"
MOD_INDEX_CACHE = CACHE_DIR / "mod_index.json"
CACHE_TTL = 60 * 60 * 6  # 6 hours

# ==========================================

PROFILES_DIR.mkdir(exist_ok=True)



def clear():
    os.system("cls" if os.name == "nt" else "clear")


def list_mods():
    mods = []
    for d in MODS_DIR.iterdir():
        if not d.is_dir():
            continue
        if d.name in PROTECTED_MODS:
            continue
        mods.append(d)
    return sorted(mods, key=lambda p: p.name.lower())


def is_enabled(mod):
    return not (mod / ".lovelyignore").exists()


def toggle_mod(mod):
    ignore = mod / ".lovelyignore"
    if ignore.exists():
        ignore.unlink()
        # print(f"Enabled  {mod.name}")
    else:
        ignore.touch()
        # print(f"Disabled {mod.name}")

MOD_INDEX_DIR = CACHE_DIR / "balatro-mod-index"

def ensure_mod_index():
    if not MOD_INDEX_DIR.exists():
        print("Cloning mod index...")
        subprocess.run(["git", "clone",
                        "https://github.com/skyline69/balatro-mod-index.git",
                        str(MOD_INDEX_DIR)])
    else:
        print("Updating mod index...")
        subprocess.run(["git", "-C", str(MOD_INDEX_DIR), "pull"])

    # Build index
    mods_dir = MOD_INDEX_DIR / "mods"
    mods = []
    for folder in mods_dir.iterdir():
        if not folder.is_dir():
            continue
        meta_file = folder / "meta.json"
        if not meta_file.exists():
            continue
        meta = json.loads(meta_file.read_text())
        mods.append({
            "name": meta.get("name", folder.name),
            "author": meta.get("author", "Unknown"),
            "repo": meta.get("repo")
        })
    return mods



def browse_mods():
    

    # Ensure mod index repo is cloned/updated
    MOD_INDEX_DIR = BASE_DIR / ".mod_index"
    if MOD_INDEX_DIR.exists():
        # update repo
        subprocess.run(["git", "pull"], cwd=MOD_INDEX_DIR)
    else:
        subprocess.run(["git", "clone", "https://github.com/skyline69/balatro-mod-index.git", str(MOD_INDEX_DIR)])

    clear()
    print("Browse Mods")
    print("-----------\n")

    # Gather mods from the cloned index
    mods = []
    mods_root = MOD_INDEX_DIR / "mods"
    for folder in mods_root.iterdir():
        if not folder.is_dir():
            continue

        meta_file = folder / "meta.json"
        if not meta_file.exists():
            continue

        try:
            meta = json.loads(meta_file.read_text())
        except Exception:
            continue

        repo_url = meta.get("repo")
        # Extract repo name for folder
        if repo_url:
            repo_name = Path(urllib.parse.urlparse(repo_url).path).name.replace(".git", "")
        else:
            repo_name = folder.name  # fallback

        mods.append({
            "title": meta.get("title", folder.name),
            "author": meta.get("author", "Unknown"),
            "repo": repo_url,
            "repo_name": repo_name
        })

    # Search prompt
    query = input("Search mods (title or author): ").strip().lower()
    if not query:
        return

    results = [
        m for m in mods
        if query in m["title"].lower() or query in m["author"].lower()
    ]

    if not results:
        print("\nNo matching mods found.")
        input("\nPress Enter to return...")
        return

    results = results[:20]  # cap results

    print("\nResults:")
    for i, mod in enumerate(results, 1):
        print(f"{i:2}) {mod['title']} — {mod['author']}")

    choice = input(
        "\nEnter numbers to install, or ENTER to cancel:\n> "
    ).strip()

    if not choice:
        return

    for part in choice.split():
        if not part.isdigit():
            continue

        idx = int(part) - 1
        if idx < 0 or idx >= len(results):
            continue

        mod = results[idx]
        dest = MODS_DIR / mod["repo_name"]

        if dest.exists():
            print(f"Skipping {mod['title']} (already installed)")
            continue

        if not mod.get("repo"):
            print(f"Skipping {mod['title']} (no repo URL)")
            continue

        print(f"Installing {mod['title']}...")
        subprocess.run(
            ["git", "clone", mod["repo"], str(dest)],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

    input("\nDone. Press Enter to return...")



def display_menu(mods):
    clear()
    print("Balatro Mod Terminal")
    print("--------------------\n")

    for i, mod in enumerate(mods, 1):
        status = "[ON ]" if is_enabled(mod) else "[OFF]"
        print(f"{i:2}) {status} {mod.name}")

    print("""
Commands:
  # = Toggle mod(s)
  P = Play
  U = Update mods
  B = Browse mod index
  S = Save profile
  L = Load profile
  Q = Quit
""")


def save_profile(mods):
    name = input("Enter profile name to save: ").strip()
    if not name:
        return

    path = PROFILES_DIR / f"{name}.profile"
    with path.open("w") as f:
        for mod in mods:
            if is_enabled(mod):
                f.write(mod.name + "\n")

    print(f"Profile '{name}' saved.")



def load_profile(mods):
    profiles = list(PROFILES_DIR.glob("*.profile"))
    if not profiles:
        print("No profiles saved.")

        return

    print("\nSaved profiles:")
    for i, p in enumerate(profiles, 1):
        print(f"{i}) {p.stem}")

    choice = input("Select profile number: ").strip()
    if not choice.isdigit():
        return

    idx = int(choice) - 1
    if idx < 0 or idx >= len(profiles):
        return

    enabled = {line.strip() for line in profiles[idx].read_text().splitlines()}

    for mod in mods:
        ignore = mod / ".lovelyignore"
        if mod.name in enabled:
            ignore.unlink(missing_ok=True)
        else:
            ignore.touch()

    print("Profile loaded.")



def update_mods(mods):
    print("Updating mods...\n")
    for mod in mods:
        if mod.name in UPDATE_EXCLUDE:
            continue
        if not (mod / ".git").exists():
            continue

        print(f"Updating {mod.name}")
        subprocess.run(["git", "pull"], cwd=mod)

    input("Press Enter to continue...")




def launch_balatro():
    print("Launching Balatro...")

    if sys.platform.startswith("linux"):
        subprocess.Popen(["steam", f"steam://rungameid/{BALATRO_APPID}"],
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    elif sys.platform == "darwin":
        subprocess.Popen(["open", f"steam://rungameid/{BALATRO_APPID}"])

    elif sys.platform.startswith("win"):
        subprocess.Popen(["cmd", "/c", "start", "", f"steam://rungameid/{BALATRO_APPID}"],
                         shell=True)

    else:
        print("Unsupported OS")

    # No sleep needed — main loop continues and menu stays active

def main():
    while True:
        mods = list_mods()
        display_menu(mods)
        choice = input("Enter choice: ").strip()

        if not choice:
            continue

        upper = choice.upper()

        if upper == "Q":
            break
        elif upper == "P":
            launch_balatro()
        elif upper == "U":
            update_mods(mods)
        elif upper == "S":
            save_profile(mods)
        elif upper == "B":
            browse_mods()
        elif upper == "L":
            load_profile(mods)
        else:
            for part in choice.split():
                if part.isdigit():
                    idx = int(part) - 1
                    if 0 <= idx < len(mods):
                        toggle_mod(mods[idx])



if __name__ == "__main__":
    main()
