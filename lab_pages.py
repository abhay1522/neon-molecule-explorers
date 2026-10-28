"""All seven pages of the Cheminformatics Virtual Laboratory."""
import pandas as pd
import streamlit as st

import chem_utils as cu
import ui_helpers as ui
from report_utils import build_pdf


# ----------------------------- shared widgets -----------------------------
def _load_example(page):
    st.session_state[f"{page}_smiles"] = cu.EXAMPLES[st.session_state[f"{page}_ex"]]


def smiles_picker(page, label="Enter SMILES"):
    """SMILES box (left) + example dropdown and Load Example button (right)."""
    key = f"{page}_smiles"
    if key not in st.session_state:
        st.session_state[key] = st.session_state["smiles"]
    c1, c2 = st.columns([2, 1])
    with c1:
        st.text_input(label, key=key)
    with c2:
        st.selectbox("Choose Example Molecule", list(cu.EXAMPLES), key=f"{page}_ex")
        st.button("Load Example", key=f"{page}_load", on_click=_load_example, args=(page,))
    smiles = st.session_state[key]
    mol = cu.parse_smiles(smiles)
    if mol is not None:
        st.session_state["smiles"] = smiles
        st.session_state["valid_smiles"] = smiles
    return smiles, mol


def viewer_3d(mol, key):
    style = st.selectbox("Select 3D Model", list(ui.STYLES), key=f"{key}_style")
    block = cu.mol_block_3d(mol)
    if block:
        ui.show_3d(block, style)
    else:
        st.warning("3D coordinates could not be generated for this molecule.")


def csv_bytes(df):
    return df.to_csv(index=False).encode("utf-8")


# --------------------------------- HOME ---------------------------------
def home():
    st.markdown(f"""
    <div style='text-align:center'>
      <h1>🧪 Cheminformatics Virtual Laboratory</h1>
      <h3 style='color:#1f4e79'>{ui.LAB_SUBTITLE}</h3>
      <p style='font-size:1.15rem;font-weight:600'>{ui.LAB_DEPARTMENT_LINE}</p>
    </div>""", unsafe_allow_html=True)
    st.divider()
    st.header("Welcome to the Virtual Laboratory")
    st.write("This interactive virtual laboratory helps students understand important concepts "
             "in cheminformatics and computational chemistry.")
    st.subheader("🧪 What can students do?")
    for item in ["Enter any SMILES notation", "Validate molecular structures", "Generate 2D structures",
                 "Generate interactive 3D structures", "Select different molecular visualization styles",
                 "Calculate complete molecular properties", "Download molecular reports",
                 "Compare multiple molecules", "Complete an assessment",
                 "Generate a personalized final project report"]:
        st.markdown(f"✅ {item}")
    st.subheader("🧬 Example Molecules")
    ex = ["Ethanol", "Benzene", "Phenol", "Acetic Acid", "Aspirin", "Caffeine"]
    st.dataframe(pd.DataFrame({"Molecule": ex, "SMILES": [cu.EXAMPLES[e] for e in ex]}), hide_index=True)
    st.divider()
    st.header("🧑‍💻 Developed by")
    st.markdown(f"**{ui.DEV_NAME}**")
    st.write(ui.DEV_ROLE)
    st.write(ui.DEV_FACULTY)
    st.write(ui.DEV_COLLEGE)
    st.write(f"Register No: {ui.DEV_REG_NO}")
    if ui.DEV_EMAIL:
        st.info(f"📧 For queries, contact: [{ui.DEV_EMAIL}](mailto:{ui.DEV_EMAIL})")


# --------------------------------- THEORY --------------------------------
def theory():
    st.title("📖 Theory")
    with st.expander("What is Cheminformatics?", expanded=True):
        st.write("Cheminformatics (chemoinformatics) uses computers and data science to store, search, "
                 "analyse and predict the properties of chemical structures. It is widely used in drug "
                 "discovery, materials science and toxicology.")
    with st.expander("SMILES notation"):
        st.write("SMILES (Simplified Molecular Input Line Entry System) writes a molecule as a line of text.")
        st.markdown("""
- **Atoms:** `C`, `N`, `O` … (aliphatic); lowercase `c`, `n`, `o` are aromatic atoms.
- **Bonds:** single is implicit, `=` double, `#` triple.
- **Branches:** parentheses, e.g. `CC(=O)O` for acetic acid.
- **Rings:** matching digits, e.g. `c1ccccc1` for benzene.
        """)
        st.dataframe(pd.DataFrame({"Molecule": ["Methane", "Ethanol", "Acetic acid", "Benzene"],
                                   "SMILES": ["C", "CCO", "CC(=O)O", "c1ccccc1"]}), hide_index=True)
    with st.expander("2D and 3D molecular representation"):
        st.write("A 2D drawing shows connectivity (which atoms are bonded). A 3D model adds spatial "
                 "coordinates, so bond angles, shape and size can be studied. 3D coordinates are generated "
                 "by embedding and then energy-minimising with a force field (MMFF).")
    with st.expander("Molecular descriptors"):
        st.dataframe(pd.DataFrame({
            "Descriptor": ["Molecular Weight", "LogP", "TPSA", "H-Bond Donors", "H-Bond Acceptors",
                           "Rotatable Bonds", "Ring Count", "Fraction Csp3"],
            "Meaning": ["Mass of one mole (g/mol)", "Lipophilicity (octanol/water partition)",
                        "Polar surface area of N, O and attached H (Å²)", "N–H and O–H groups",
                        "N and O atoms that can accept H-bonds", "Flexible single bonds",
                        "Number of rings", "Fraction of sp³ carbons (saturation / 3D character)"]}), hide_index=True)
    with st.expander("Sigma (σ) and Pi (π) bonds"):
        st.write("Every single bond is one σ bond. A double bond = 1σ + 1π and a triple bond = 1σ + 2π. "
                 "The lab counts bonds including hydrogens, e.g. ethanol has 8 σ bonds and 0 π bonds.")
    with st.expander("Lipinski's Rule of Five"):
        st.write("A molecule is more likely to be orally bioavailable if it has at most one violation of:")
        st.dataframe(pd.DataFrame({"Property": ["Molecular weight", "LogP", "H-bond donors", "H-bond acceptors"],
                                   "Limit": ["≤ 500", "≤ 5", "≤ 5", "≤ 10"]}), hide_index=True)
    with st.expander("Structure–property relationships"):
        st.write("Small structural changes alter properties: adding –OH raises polarity and lowers LogP, "
                 "while adding carbon chains or rings raises LogP and molecular weight.")


# ---------------------------- MOLECULAR VISUALIZATION ----------------------------
def visualization():
    st.title("🧬 Molecular Visualization Laboratory")
    st.info("Enter a new SMILES or load an example. The selected molecule will be used across the laboratory pages.")
    smiles, mol = smiles_picker("viz")
    if mol is None:
        st.error("Invalid SMILES. Please check the notation.")
        return
    st.success("Valid Molecular Structure!")
    b = cu.basic_info(mol, smiles)
    c1, c2 = st.columns([1.2, 1])
    with c1:
        st.header("2D Molecular Structure")
        ui.show_svg(cu.draw_svg(mol))
    with c2:
        st.header("Molecular Information")
        st.markdown(f"**Input SMILES:** {b['input']}")
        st.markdown(f"**Canonical SMILES:** {b['canonical']}")
        st.markdown(f"**Formula:** {b['formula']}")
        st.markdown(f"**Heavy Atoms:** `{b['heavy_atoms']}`")
        st.markdown(f"**Total Atoms (including H):** `{b['total_atoms']}`")
        st.markdown(f"**Heavy-Atom Bonds:** `{b['heavy_bonds']}`")
        st.markdown(f"**Sigma (σ) Bonds:** `{b['sigma']}`")
        st.markdown(f"**Pi (π) Bonds:** `{b['pi']}`")
        st.markdown(f"**Total Bonds (σ + π):** `{b['total_bonds']}`")
    st.divider()
    st.header("🌐 3D Molecular Visualization")
    viewer_3d(mol, "viz")


# ---------------------------- PROPERTIES REPORT ----------------------------
def properties():
    st.title("📊 Complete Molecular Properties Report")
    st.info("Enter any valid SMILES notation. The system will automatically generate a complete "
            "molecular properties report.")
    st.header("Select or Enter Your Molecule")
    smiles, mol = smiles_picker("prop", "Enter New SMILES")
    st.caption("Once you enter a valid SMILES or load an example, the complete 2D/3D structures and "
               "molecular properties below are generated for the same molecule.")
    if mol is None:
        st.error("Invalid SMILES. Please check the notation.")
        return
    st.success("Valid Molecular Structure Detected!")
    b, d = cu.basic_info(mol, smiles), cu.descriptors(mol)
    c1, c2 = st.columns([1.2, 1])
    with c1:
        st.header("🧬 2D Molecular Structure")
        ui.show_svg(cu.draw_svg(mol))
    with c2:
        st.header("📋 Basic Information")
        st.markdown(f"**Input SMILES:** {b['input']}")
        st.markdown(f"**Canonical SMILES:** {b['canonical']}")
        st.markdown(f"**Molecular Formula:** {b['formula']}")
        st.markdown(f"**Atoms:** `{b['atoms']}`")
        st.markdown(f"**Heavy Atoms:** `{b['heavy_atoms']}`")
        st.markdown(f"**Heavy-Atom Bonds:** `{b['heavy_bonds']}`")
        st.markdown(f"**Sigma (σ) Bonds:** `{b['sigma']}`")
        st.markdown(f"**Pi (π) Bonds:** `{b['pi']}`")
        st.markdown(f"**Total Bonds (σ + π):** `{b['total_bonds']}`")
    st.divider()
    st.header("📊 Important Molecular Properties")
    r1 = st.columns(4)
    r1[0].metric("Molecular Weight", f"{d['mw']} g/mol")
    r1[1].metric("LogP", d["logp"])
    r1[2].metric("TPSA", f"{d['tpsa']} Å²")
    r1[3].metric("Ring Count", d["rings"])
    r2 = st.columns(4)
    r2[0].metric("H-Bond Donors", d["hbd"])
    r2[1].metric("H-Bond Acceptors", d["hba"])
    r2[2].metric("Rotatable Bonds", d["rotb"])
    r2[3].metric("Fraction Csp3", d["fsp3"])
    st.divider()
    st.header("📑 Complete Molecular Property Table")
    rows = cu.property_table(mol, smiles)
    df = pd.DataFrame(rows, columns=["Property", "Value"])
    st.dataframe(df, hide_index=True, height=500)
    st.download_button("⬇️ Download Properties Report (CSV)", csv_bytes(df), "molecular_properties.csv", "text/csv")
    if st.button("📄 Generate Molecular PDF Report", key="prop_pdf"):
        pdf = build_pdf("Molecular Properties Report", ui.LAB_SUBTITLE, rows, cu.draw_png_bytes(mol),
                        st.session_state["student_name"], st.session_state["reg_no"])
        st.download_button("⬇️ Download PDF", pdf, "molecular_report.pdf", "application/pdf", key="prop_pdf_dl")
    st.divider()
    st.header("🌐 3D Molecular Visualization")
    viewer_3d(mol, "prop")


# ---------------------------- STRUCTURE-PROPERTY ANALYSIS ----------------------------
DEFAULT_LIST = ("Ethanol,CCO\nBenzene,c1ccccc1\nPhenol,Oc1ccccc1\n"
                "Acetic Acid,CC(=O)O\nAspirin,CC(=O)Oc1ccccc1C(=O)O")


def analysis():
    st.title("📈 Structure–Property Analysis")
    st.write("Compare the properties of multiple molecules. Enter one molecule per line in the format:")
    st.markdown("**Molecule Name, SMILES**")
    text = st.text_area("Enter Molecules", DEFAULT_LIST, height=215, key="ana_text")
    rows, bad = [], []
    for line in text.splitlines():
        if not line.strip():
            continue
        if "," not in line:
            bad.append(line)
            continue
        name, smi = (p.strip() for p in line.rsplit(",", 1))
        mol = cu.parse_smiles(smi)
        if mol is None:
            bad.append(line)
            continue
        d = cu.descriptors(mol)
        rows.append({"Molecule": name, "MW": d["mw"], "LogP": d["logp"], "TPSA": d["tpsa"],
                     "HBD": d["hbd"], "HBA": d["hba"], "Rotatable Bonds": d["rotb"], "Ring Count": d["rings"]})
    for b in bad:
        st.warning(f"Could not read line: {b}")
    if not rows:
        st.info("Enter at least one valid 'Name, SMILES' line.")
        return
    df = pd.DataFrame(rows)
    st.dataframe(df, hide_index=True)
    st.header("📋 Comparison Table")
    st.download_button("⬇️ Download Comparison Table (CSV)", csv_bytes(df), "comparison_table.csv", "text/csv")


# --------------------------------- ASSESSMENT ---------------------------------
QUIZ = [
    ("What does SMILES stand for?",
     ["Simplified Molecular Input Line Entry System", "Standard Molecular Isotope Listing and Entry System",
      "Simple Molecule Identification and Labelling Scheme", "Systematic Molecular Ionic Link Entry System"], 0),
    ("Which SMILES represents ethanol?", ["CO", "CCO", "C=O", "CC=O"], 1),
    ("In SMILES, lowercase letters such as 'c' indicate:", ["Charged atoms", "Chiral centres", "Aromatic atoms", "Isotopes"], 2),
    ("A C=C double bond contains:", ["2 sigma bonds", "1 sigma + 1 pi bond", "2 pi bonds", "1 sigma + 2 pi bonds"], 1),
    ("According to Lipinski's rule, the molecular weight should be at most:", ["200 Da", "300 Da", "500 Da", "1000 Da"], 2),
    ("A higher positive LogP value means the molecule is more:", ["Water soluble", "Lipophilic", "Acidic", "Radioactive"], 1),
    ("TPSA is the surface area contributed by:", ["Carbon atoms", "Halogens", "Polar atoms (N, O and attached H)", "All hydrogens"], 2),
    ("How many rings are present in benzene?", ["0", "1", "2", "3"], 1),
    ("Fraction Csp3 describes:", ["Fraction of aromatic carbons", "Fraction of sp³ carbons", "Fraction of carbonyl carbons", "Fraction of charged atoms"], 1),
    ("Which bond count does ethanol (CCO, with H) have?", ["8 sigma, 0 pi", "7 sigma, 1 pi", "9 sigma, 0 pi", "6 sigma, 2 pi"], 0),
]


def assessment():
    st.title("📝 Assessment")
    st.write("Answer all questions and submit to see your score.")
    with st.form("quiz_form"):
        answers = []
        for i, (q, opts, _) in enumerate(QUIZ, 1):
            answers.append(st.radio(f"**Q{i}. {q}**", opts, index=None, key=f"quiz_{i}"))
        submitted = st.form_submit_button("Submit Assessment")
    if submitted:
        if any(a is None for a in answers):
            st.warning("Please answer every question before submitting.")
            return
        score = sum(a == QUIZ[i][1][QUIZ[i][2]] for i, a in enumerate(answers))
        st.session_state["quiz_score"] = score
        (st.success if score >= 7 else st.warning)(
            f"{st.session_state['student_name']} – Score: {score} / {len(QUIZ)}")
        for i, (q, opts, ans) in enumerate(QUIZ):
            ok = answers[i] == opts[ans]
            st.markdown(f"{'✅' if ok else '❌'} **Q{i + 1}.** Correct answer: {opts[ans]}")


# --------------------------------- FINAL REPORT ---------------------------------
def final_report():
    st.title("📄 Final Student Molecular Analysis Report")
    st.write("This report uses the latest valid SMILES entered in the Molecular Properties Report page.")
    st.session_state.setdefault("final_name", st.session_state["student_name"])
    st.session_state.setdefault("final_reg", st.session_state["reg_no"])
    st.session_state.setdefault("final_smiles", st.session_state["valid_smiles"])
    name = st.text_input("Student Name for Report", key="final_name")
    reg = st.text_input("Registration Number for Report", key="final_reg")
    smiles = st.text_input("SMILES for Final Report", key="final_smiles")
    mol = cu.parse_smiles(smiles)
    if mol is None:
        st.error("Invalid SMILES. Please enter a valid molecule.")
        return
    st.success("Valid molecule ready for the final report.")
    b, d = cu.basic_info(mol, smiles), cu.descriptors(mol)
    st.markdown(f"**Molecular Formula:** {b['formula']}")
    st.markdown(f"**Molecular Weight:** `{d['mw']}` g/mol")
    st.markdown(f"**Sigma Bonds:** `{b['sigma']}`")
    st.markdown(f"**Pi Bonds:** `{b['pi']}`")
    if st.button("📄 Generate Personalized Final Project Report", key="final_btn"):
        rows = cu.property_table(mol, smiles)
        if "quiz_score" in st.session_state:
            rows.append(("Assessment Score", f"{st.session_state['quiz_score']} / {len(QUIZ)}"))
        pdf = build_pdf("Final Student Molecular Analysis Report", ui.LAB_SUBTITLE, rows,
                        cu.draw_png_bytes(mol), name, reg)
        st.success("Report generated!")
        st.download_button("⬇️ Download Final Report (PDF)", pdf, "final_project_report.pdf",
                           "application/pdf", key="final_dl")
