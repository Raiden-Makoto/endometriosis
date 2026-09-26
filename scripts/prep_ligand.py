from rdkit import Chem # type: ignore
from rdkit.Chem import AllChem # type: ignore
from meeko import MoleculePreparation, PDBQTWriterLegacy #type: ignore
from pathlib import Path

root_dir = Path(__file__).resolve().parent.parent
asset_path = root_dir / "assets"

smiles = "O=C(O)c1ccc(N=Nc2ccc(S(=O)(=O)Nc3ccccn3)cc2)c(O)c1"

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

with open(asset_path / "ligand.pdbqt", "w") as f:
    f.write(pdbqt_string)

print("Created test ligand file successfully.")