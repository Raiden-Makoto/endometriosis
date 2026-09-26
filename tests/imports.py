import os
from vina import Vina # type: ignore
import rdkit # type: ignore
from rdkit import Chem # type: ignore
import meeko # type: ignore


cores = os.cpu_count()
allocated_cores = cores // 2 # allocate half the CPU cores

test = Vina(sf_name="vina", cpu=allocated_cores)
print(f"Vina is uing {allocated_cores} CPU cores.")
print(f"Imported packages successfully. RDKit version {rdkit.__version__}")