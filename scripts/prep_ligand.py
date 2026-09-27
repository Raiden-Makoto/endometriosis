from rdkit import Chem # type: ignore
from rdkit.Chem import AllChem # type: ignore
from meeko import MoleculePreparation, PDBQTWriterLegacy #type: ignore
from pathlib import Path
import argparse # smiles will come from command line
import uuid # for unique ligand file name

def main():
    parser = argparse.ArgumentParser(description="Prepare a ligand for docking.")
    parser.add_argument("--smiles", type=str, required=True, help="SMILES string of the ligand.")
    args = parser.parse_args()

    root_dir = Path(__file__).resolve().parent.parent
    ligand_path = root_dir / "ligands"
    if not ligand_path.exists():
        ligand_path.mkdir(parents=True, exist_ok=True)

    smiles = args.smiles
    ligand_file = ligand_path / f"ligand_{uuid.uuid4()}.pdbqt"

    molecule = Chem.MolFromSmiles(smiles)
    if molecule is None:
        raise ValueError(f"Failed to parse SMILES string: {smiles}")

    molecule = Chem.AddHs(molecule)
    AllChem.EmbedMolecule(molecule)
    AllChem.MMFFOptimizeMolecule(molecule)

    preparator = MoleculePreparation()
    mol_setups = preparator.prepare(molecule)
    writer = PDBQTWriterLegacy()
    pdbqt_string = writer.write_string(mol_setups[0])[0]

    with open(ligand_file, "w") as f:
        f.write(pdbqt_string)

    print("Created test ligand file successfully.")

if __name__ == "__main__":
    main()