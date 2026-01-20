#!/bin/bash

# ===== BOOTSTRAP =====
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
source "$SCRIPT_DIR/config.sh"

# Ensure profiles folder exists
mkdir -p "$PROFILES_DIR"

# ===== FUNCTIONS =====

display_mods() {
    clear
    echo "     LMN Tool"
    echo "------------------"

    mods=()
    i=1

    for dir in "$MODS_DIR"/*/; do
        mod="$(basename "$dir")"

        # Skip protected mods
        if [[ " ${PROTECTED_MODS[*]} " == *" $mod "* ]]; then
            continue
        fi

        mods+=("$mod")

        if [[ -f "$MODS_DIR/$mod/.lovelyignore" ]]; then
            status="[OFF]"
        else
            status="[ON ]"
        fi

        printf "%2d) %s %s\n" "$i" "$status" "$mod"
        ((i++))
    done
}

toggle_mods() {
    for CHOICE in "$@"; do
        [[ "$CHOICE" =~ ^[0-9]+$ ]] || continue
        INDEX=$((CHOICE - 1))

        [[ "$INDEX" -ge 0 && "$INDEX" -lt "${#mods[@]}" ]] || continue

        MOD="${mods[$INDEX]}"
        IGNORE="$MODS_DIR/$MOD/.lovelyignore"

        if [[ -f "$IGNORE" ]]; then
            rm "$IGNORE"
            echo "Enabled  $MOD"
        else
            touch "$IGNORE"
            echo "Disabled $MOD"
        fi
    done

    sleep 0.4
}

save_profile() {
    read -p "Enter profile name to save: " NAME
    [[ -z "$NAME" ]] && return

    FILE="$PROFILES_DIR/$NAME.profile"
    : > "$FILE"

    for MOD in "${mods[@]}"; do
        [[ ! -f "$MODS_DIR/$MOD/.lovelyignore" ]] && echo "$MOD" >> "$FILE"
    done

    echo "Profile '$NAME' saved."
    sleep 0.8
}

load_profile() {
    profiles=("$PROFILES_DIR"/*.profile)
    [[ ! -e "${profiles[0]}" ]] && echo "No profiles saved." && sleep 1 && return

    echo
    echo "Saved profiles:"
    for i in "${!profiles[@]}"; do
        echo "$((i+1))) $(basename "${profiles[$i]}" .profile)"
    done

    read -p "Select profile number: " CHOICE
    [[ "$CHOICE" =~ ^[0-9]+$ ]] || return

    INDEX=$((CHOICE - 1))
    [[ "$INDEX" -ge 0 && "$INDEX" -lt "${#profiles[@]}" ]] || return

    PROFILE="${profiles[$INDEX]}"

    # Disable all
    for MOD in "${mods[@]}"; do
        touch "$MODS_DIR/$MOD/.lovelyignore"
    done

    # Enable profile mods
    while read -r MOD; do
        rm -f "$MODS_DIR/$MOD/.lovelyignore"
    done < "$PROFILE"

    echo "Profile loaded."
    sleep 0.6
}

run_updater() {
    echo "Updating mods..."
    for MOD in "${mods[@]}"; do
        [[ " ${UPDATE_EXCLUDE[*]} " == *" $MOD "* ]] && continue
        [[ -d "$MODS_DIR/$MOD/.git" ]] || continue

        echo "Updating $MOD"
        (cd "$MODS_DIR/$MOD" && git pull)
    done

    read -p "Press Enter to return to menu..."
}

launch_balatro() {
    OS_NAME="$(uname)"

    if [[ "$OS_NAME" == "Darwin" ]]; then
        echo "Launching Balatro (macOS, modded)..."

        LOVELY_SCRIPT="$HOME/Library/Application Support/Steam/steamapps/common/Balatro/run_lovely_macos.sh"

        if [[ ! -f "$LOVELY_SCRIPT" ]]; then
            echo "ERROR: run_lovely_macos.sh not found."
            echo "Balatro mods cannot be launched via Steam on macOS."
            read -p "Press Enter to return..."
            return
        fi

        sh "$LOVELY_SCRIPT" >/dev/null 2>&1 &
        sleep 1
        return
    fi

    # Linux / other
    echo "Launching Balatro via Steam..."
    steam "steam://rungameid/$BALATRO_APPID" >/dev/null 2>&1 &
    sleep 1
}

# ===== MAIN LOOP =====
while true; do
    display_mods

    echo
    echo "Commands:"
    echo "  Numbers → Toggle mods (space-separated)"
    echo "  U = Update mods"
    echo "  S = Save profile"
    echo "  L = Load profile"
    echo "  O = Launch Balatro"
    echo "  Q = Quit"
    echo

    read -p "Enter your choice: " INPUT
    INPUT_UPPER=$(echo "$INPUT" | tr '[:lower:]' '[:upper:]')

    case "$INPUT_UPPER" in
        U) run_updater ;;
        S) save_profile ;;
        L) load_profile ;;
        O) launch_balatro ;;
        Q) exit 0 ;;
        *)
            read -ra CHOICES <<< "$INPUT"
            toggle_mods "${CHOICES[@]}"
            ;;
    esac
done
