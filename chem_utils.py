"""RDKit helper functions for the Cheminformatics Virtual Laboratory."""
from rdkit import Chem
from rdkit.Chem import AllChem, Crippen, Descriptors, Lipinski, rdMolDescriptors
from rdkit.Chem.Draw import rdMolDraw2D

EXAMPLES = {
    "Ethanol": "CCO",
    "Benzene": "c1ccccc1",
    "Phenol": "Oc1ccccc1",
    "Acetic Acid": "CC(=O)O",
    "Aspirin": "CC(=O)Oc1ccccc1C(=O)O",
    "Caffeine": "CN1C=NC2=C1C(=O)N(C(=O)N2C)C",
    "Paracetamol (PCM)": "CC(=O)Nc1ccc(O)cc1",
    "Ibuprofen": "CC(C)Cc1ccc(cc1)C(C)C(=O)O",
    "Water": "O",
    "Methane": "C",
    "Glucose": "OCC1OC(O)C(O)C(O)C1O",
    "Nicotine": "CN1CCCC1c1cccnc1",
    "Dopamine": "NCCc1ccc(O)c(O)c1",
    "Metformin": "CN(C)C(=N)N=C(N)N",
}


def parse_smiles(smiles):
    """Return an RDKit Mol or None if the SMILES is invalid/empty."""
    if not smiles or not smiles.strip():
        return None
    try:
        return Chem.MolFromSmiles(smiles.strip())
    except Exception:
        return None


def bond_counts(mol):
    """Sigma / pi / total bond counts (hydrogens included, Kekule form)."""
    mh = Chem.AddHs(mol)
    k = Chem.Mol(mh)
    try:
        Chem.Kekulize(k, clearAromaticFlags=True)
    except Exception:
        k = mh
    sigma = pi = 0
    for b in k.GetBonds():
        order = int(round(b.GetBondTypeAsDouble()))
        sigma += 1
        pi += max(order - 1, 0)
    return sigma, pi, sigma + pi


def basic_info(mol, smiles):
    sigma, pi, total = bond_counts(mol)
    return {
        "input": smiles.strip(),
        "canonical": Chem.MolToSmiles(mol),
        "formula": rdMolDescriptors.CalcMolFormula(mol),
        "atoms": mol.GetNumAtoms(),
        "heavy_atoms": mol.GetNumHeavyAtoms(),
        "total_atoms": Chem.AddHs(mol).GetNumAtoms(),
        "heavy_bonds": mol.GetNumBonds(),
        "sigma": sigma,
        "pi": pi,
        "total_bonds": total,
    }


def descriptors(mol):
    return {
        "mw": round(Descriptors.MolWt(mol), 3),
        "exact_mw": round(Descriptors.ExactMolWt(mol), 4),
        "logp": round(Crippen.MolLogP(mol), 3),
        "tpsa": round(rdMolDescriptors.CalcTPSA(mol), 2),
        "hbd": Lipinski.NumHDonors(mol),
        "hba": Lipinski.NumHAcceptors(mol),
        "rotb": Lipinski.NumRotatableBonds(mol),
        "rings": rdMolDescriptors.CalcNumRings(mol),
        "fsp3": round(rdMolDescriptors.CalcFractionCSP3(mol), 3),
    }


def lipinski_violations(d):
    return sum([d["mw"] > 500, d["logp"] > 5, d["hbd"] > 5, d["hba"] > 10])


def property_table(mol, smiles):
    """Ordered list of (Property, Value-as-string) for the full table / CSV."""
    b, d = basic_info(mol, smiles), descriptors(mol)
    rows = [
        ("Input SMILES", b["input"]), ("Canonical SMILES", b["canonical"]),
        ("Molecular Formula", b["formula"]), ("Molecular Weight", d["mw"]),
        ("Exact Molecular Weight", d["exact_mw"]), ("LogP", d["logp"]),
        ("TPSA", d["tpsa"]), ("Hydrogen Bond Donors", d["hbd"]),
        ("Hydrogen Bond Acceptors", d["hba"]), ("Rotatable Bonds", d["rotb"]),
        ("Ring Count", d["rings"]), ("Fraction Csp3", d["fsp3"]),
        ("Heavy Atoms", b["heavy_atoms"]), ("Total Atoms (including H)", b["total_atoms"]),
        ("Heavy-Atom Bonds", b["heavy_bonds"]), ("Sigma Bonds", b["sigma"]),
        ("Pi Bonds", b["pi"]), ("Total Bonds (sigma + pi)", b["total_bonds"]),
    ]
    return [(k, str(v)) for k, v in rows]


def draw_svg(mol, w=700, h=420):
    d = rdMolDraw2D.MolDraw2DSVG(w, h)
    d.DrawMolecule(mol)
    d.FinishDrawing()
    return d.GetDrawingText()


def draw_png_bytes(mol, w=500, h=350):
    """PNG bytes for the PDF report (None if Cairo drawing is unavailable)."""
    try:
        d = rdMolDraw2D.MolDraw2DCairo(w, h)
        d.DrawMolecule(mol)
        d.FinishDrawing()
        return d.GetDrawingText()
    except Exception:
        return None


def mol_block_3d(mol):
    """3D coordinates as a MOL block (None if embedding fails)."""
    mh = Chem.AddHs(mol)
    if AllChem.EmbedMolecule(mh, randomSeed=42) != 0:
        if AllChem.EmbedMolecule(mh, useRandomCoords=True, randomSeed=42) != 0:
            return None
    try:
        AllChem.MMFFOptimizeMolecule(mh, maxIters=500)
    except Exception:
        pass
    return Chem.MolToMolBlock(mh)
