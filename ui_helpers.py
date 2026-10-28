"""Sidebar, footer, header and 3D viewer helpers (same layout as the reference lab)."""
import json
import streamlit as st
import streamlit.components.v1 as components

# ===================== EDIT YOUR DETAILS HERE =====================
DEV_NAME = "Abhay Raj"
DEV_ROLE = "B.Tech CSE (AI/ML) – Section C"
DEV_COLLEGE = "SRM Institute of Science and Technology, Tiruchirappalli"
DEV_REG_NO = "RA2611026050168"
DEV_EMAIL = ""   # e.g. "abhay@gmail.com"  (leave "" to hide the contact box)
LAB_SUBTITLE = "SRM Institute of Science and Technology, Tiruchirappalli"
LAB_DEPARTMENT_LINE = "Faculty of Engineering and Technology | School of Sciences | Division of Chemistry"
# ==================================================================

NAV = [
    "Home", "Theory", "Molecular Visualization",
    " Molecular Properties Report", "Structure–Property Analysis",
    " Assessment", " Final Project Report",
]
OBJECTIVES = ["SMILES notation", "Molecular representation", "2D visualization",
              "3D visualization", "Molecular descriptors", "Structure-property relationships"]


def init_state():
    st.session_state.setdefault("smiles", "CCO")
    st.session_state.setdefault("valid_smiles", "CCO")
    st.session_state.setdefault("student_name", DEV_NAME.upper())
    st.session_state.setdefault("reg_no", DEV_REG_NO)


def render_sidebar():
    with st.sidebar:
        st.title("🧪 Virtual Lab")
        page = st.radio("Navigation", NAV, key="nav")
        st.divider()
        st.subheader("🧑‍🎓 Student Information")
        st.text_input("Student Name", key="student_name")
        st.text_input("Registration Number", key="reg_no")
        st.subheader("🎓 Learning Objectives")
        st.write("Students can learn:")
        st.markdown("\n".join(f"- {o}" for o in OBJECTIVES))
    return page


def footer():
    st.divider()
    st.caption("Cheminformatics Virtual Laboratory | Developed using Python, Streamlit and RDKit")


def show_svg(svg, height=440):
    """2D structure on a white rounded canvas, scaled to the column width."""
    svg = svg.replace("width='700px' height='420px'", "width='100%'")
    components.html(f"<div style='background:#fff;border-radius:12px;padding:8px'>{svg}</div>", height=height)


STYLES = {
    "Ball and Stick": "{stick:{radius:0.15}, sphere:{scale:0.3}}",
    "Stick": "{stick:{radius:0.2}}",
    "Space Filling": "{sphere:{}}",
    "Line": "{line:{}}",
}

_VIEWER = """
<script src="https://cdnjs.cloudflare.com/ajax/libs/3Dmol/2.0.4/3Dmol-min.js"></script>
<div id="v" style="width:100%;height:420px;position:relative;border-radius:12px;overflow:hidden"></div>
<script>
 const v = $3Dmol.createViewer("v", {backgroundColor:"white"});
 v.addModel(__MOL__, "sdf");
 v.setStyle({}, __STYLE__);
 v.zoomTo(); v.render();
</script>"""


def show_3d(molblock, style="Ball and Stick"):
    html = _VIEWER.replace("__MOL__", json.dumps(molblock)).replace("__STYLE__", STYLES[style])
    components.html(html, height=430)
