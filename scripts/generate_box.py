from Bio.PDB import PDBParser # type: ignore
import numpy as np # type: ignore
import os
from pathlib import Path

root_dir = Path(__file__).resolve().parent.parent
asset_path = root_dir / "assets"
cd44_filepath = asset_path / "cd44_cleaned.pdb"

if not os.path.exists(cd44_filepath):
    raise FileNotFoundError(f"File {cd44_filepath} not found")

parser = PDBParser(QUIET=True)
structure = parser.get_structure("cd44", cd44_filepath)

v6_coords = []
for model in structure:
    for chain in model:
        for residue in chain:
            residue_number = residue.id[1] # (' ', resseq, icode)[1]
            if 402 <= residue_number <= 408: # exon v6 cNRWHE
                # this exact 5-mer is the required docking interface that causes endometrial cells to stick
                for atom in residue:
                    v6_coords.append(atom.get_coord())

if not v6_coords:
    raise ValueError("No atoms matched residue range 403-407 in structure.")

coords = np.array(v6_coords, dtype=np.float32)
center = np.mean(coords, axis=0)
span = (np.max(coords, axis=0) - np.min(coords, axis=0))
boundary = np.maximum(span + 10.0, 22.0) 

config_content = f"""
# AutoDock Vina Grid Configuration for CD44v6
center_x = {center[0]:.4f}
center_y = {center[1]:.4f}
center_z = {center[2]:.4f}
size_x = {boundary[0]:.4f}
size_y = {boundary[1]:.4f}
size_z = {boundary[2]:.4f}
"""

with open(asset_path / "cd44_v6_box.txt", "w") as f:
    f.write(config_content)

print("Successfully generated box configuration for CD44v6 using Bio.PDB.")