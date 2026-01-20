#!/bin/bash
# ==================================================
# LMN Tool – User Configuration
# ==================================================
# This file contains all user-specific settings.
# Only edit this file — do NOT edit mod-toggle.sh.
# ==================================================

# Get the directory this config file lives in
PARENT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

MODS_DIR="${MODS_DIR:-$PARENT_DIR/../Mods}"
PROFILES_DIR="${PROFILES_DIR:-$PARENT_DIR/profiles}"

# Paths relative to config.sh
BALATRO_DIR="$MODS_DIR/.."
BALATRO_APPID=2379780



# --------------------------------------------------
# Mod protection rules
# --------------------------------------------------

# These folders are never shown/toggled in the manager
PROTECTED_MODS=(
    "lovely"
    "Steamodded"
    "smods"
)

# --------------------------------------------------
# Update rules
# --------------------------------------------------

# Mods that should not be updated via git
UPDATE_EXCLUDE=(
    "PokermonPlus"
)

# --------------------------------------------------
# Launch settings
# --------------------------------------------------

# How Balatro is launched: "steam" or "wine"
LAUNCH_METHOD="steam"
