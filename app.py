"""Cheminformatics Virtual Laboratory – entry point.  Run: streamlit run app.py"""
import streamlit as st

st.set_page_config(page_title="Cheminformatics Virtual Laboratory", page_icon="⚗️", layout="wide")

import lab_pages as lp
import ui_helpers as ui

ui.init_state()
page = ui.render_sidebar()

ROUTES = {
    ui.NAV[0]: lp.home,
    ui.NAV[1]: lp.theory,
    ui.NAV[2]: lp.visualization,
    ui.NAV[3]: lp.properties,
    ui.NAV[4]: lp.analysis,
    ui.NAV[5]: lp.assessment,
    ui.NAV[6]: lp.final_report,
}
ROUTES[page]()
ui.footer()
