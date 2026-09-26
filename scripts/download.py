import json
import os
import urllib.request
from pathlib import Path

root_dir = Path(__file__).resolve().parent.parent
asset_path = root_dir / "assets"
asset_path.mkdir(parents=True, exist_ok=True)

UNIPROT_ID = "P16070"  # CD44
PDB_FILENAME = asset_path / "human_cd44_full.pdb"


def alphafold_pdb_url(uniprot_id: str) -> str:
    api_url = f"https://alphafold.ebi.ac.uk/api/prediction/{uniprot_id}"
    with urllib.request.urlopen(api_url) as response:
        predictions = json.load(response)
    if not predictions:
        raise ValueError(f"No AlphaFold prediction for UniProt {uniprot_id}")
    return predictions[0]["pdbUrl"]


if not os.path.exists(PDB_FILENAME):
    print(f"Downloading CD44 structure from AlphaFold (UniProt={UNIPROT_ID})...")
    pdb_url = alphafold_pdb_url(UNIPROT_ID)
    urllib.request.urlretrieve(pdb_url, PDB_FILENAME)
    print(f"Downloaded successfully from {pdb_url}")
else:
    print(f"File {PDB_FILENAME} already exists.")
