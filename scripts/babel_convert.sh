#!/bin/bash

# check if openbabel is installed (MacOS)
if ! command -v obabel >/dev/null 2>&1; then
    echo "Error: obabel is not installed." >&2
    echo "You can install it using Homebrew: brew install open-babel" >&2
    exit 1
fi

echo "obabel is installed. running the conversion..."
root="assets/"

# Remove water molecules and add essential polar hydrogens
obabel "${root}/human_cd44_full.pdb" -O "${root}/cd44_cleaned.pdb" -d -h

# Convert to PDBQT format for AutoDock Vina
obabel "${root}/cd44_cleaned.pdb" -O "${root}/cd44_target.pdbqt" -xr --partialcharge gasteiger
echo "conversion complete."`