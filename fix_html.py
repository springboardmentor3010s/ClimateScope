import os
import re

directory = r"d:\climateScope"
files = [
    os.path.join(directory, "app.py"),
    os.path.join(directory, "pages", "Climate_Risk_Intelligence.py"),
    os.path.join(directory, "pages", "Executive_Overview.py"),
    os.path.join(directory, "pages", "Extreme_Events_Monitor.py"),
    os.path.join(directory, "pages", "Precipitation_Wind_Intelligence.py"),
    os.path.join(directory, "pages", "Regional_Comparison.py"),
    os.path.join(directory, "pages", "Temperature_Intelligence.py"),
]

def fix_all():
    # 1. Update app.py's render_kpi function
    app_py_path = os.path.join(directory, "app.py")
    with open(app_py_path, "r", encoding="utf-8") as f:
        app_content = f.read()

    old_render_kpi_end = """    st.markdown(
        f\"\"\"
        <div class="kpi-glass-card {glow_class}">
            <div class="kpi-icon">{icon}</div>
            <div class="kpi-label">{title}</div>
            <div class="kpi-value-gradient">{value}</div>
            <div class="kpi-meta-row">
                {delta_html}
                {trend_html}
            </div>
        </div>
        \"\"\",
        unsafe_allow_html=True,
    )"""

    new_render_kpi_end = """    if "kpi_buffer" not in st.session_state:
        st.session_state.kpi_buffer = []
    st.session_state.kpi_buffer.append(f\"\"\"
        <div class="kpi-glass-card {glow_class}">
            <div class="kpi-icon">{icon}</div>
            <div class="kpi-label">{title}</div>
            <div class="kpi-value-gradient">{value}</div>
            <div class="kpi-meta-row">
                {delta_html}
                {trend_html}
            </div>
        </div>
    \"\"\")"""

    app_content = app_content.replace(old_render_kpi_end, new_render_kpi_end)
    app_content = app_content.replace('</ul></div>",', '</ul>",')

    with open(app_py_path, "w", encoding="utf-8") as f:
        f.write(app_content)

    # 2. Update all files to replace stray </div> and opening wrappers
    flush_code = """        if "kpi_buffer" in st.session_state and st.session_state.kpi_buffer:
            st.markdown(f"<div class='kpi-grid'>{''.join(st.session_state.kpi_buffer)}</div>", unsafe_allow_html=True)
            st.session_state.kpi_buffer = []"""
            
    for filepath in files:
        if not os.path.exists(filepath):
            continue
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
            
        # Delete opening kpi-grid and kpi-row
        content = re.sub(r'[ \t]*st\.markdown\([\'"]<div class=[\'"]kpi-(grid|row)[\'"]>[\'"], unsafe_allow_html=True\)\r?\n', '', content)
        
        # Replace st.markdown("</div>") with flush logic
        content = re.sub(r'[ \t]*st\.markdown\([\'"]</div>[\'"], unsafe_allow_html=True\)\r?\n', flush_code + "\n", content)
        
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)

if __name__ == "__main__":
    fix_all()
    print("Done fixing HTML.")
