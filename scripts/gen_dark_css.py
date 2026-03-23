import re

with open('.streamlit/climate_scope_light.css', 'r', encoding='utf-8') as f:
    css = f.read()

# 1. Base Backgrounds: Slate 900
css = css.replace('linear-gradient(135deg, #f8fafc 0%, #eef2ff 50%, #f0f9ff 100%)', 'linear-gradient(135deg, #0f172a 0%, #172033 50%, #1e293b 100%)')
css = css.replace('#ffffff', '#1e293b') # Cards
css = css.replace('#f8fafc', '#0f172a') # Page background
css = css.replace('#f1f5f9', '#1e293b') # Hover states / secondary
css = css.replace('linear-gradient(180deg, #ffffff 0%, #f8fafc 100%)', '#172033')
css = css.replace('linear-gradient(90deg, #f8fafc, #ffffff, #f8fafc)', 'linear-gradient(90deg, #0f172a, #1e293b, #0f172a)')

# 2. Base Text: High Contrast Lights
css = css.replace('#1e293b', '#f8fafc')
css = css.replace('#334155', '#e2e8f0')
css = css.replace('#475569', '#cbd5e1')
css = css.replace('#64748b', '#94a3b8')

# 3. Base Borders: Muted Slate
css = css.replace('#e2e8f0', '#334155')
css = css.replace('#cbd5e1', '#475569')

# 4. Glass Cards: Transparent slate
css = css.replace('rgba(255,255,255,0.8)', 'rgba(30,41,59,0.7)')
css = css.replace('rgba(255,255,255,0.4)', 'rgba(15,23,42,0.5)')
css = css.replace('rgba(255, 255, 255, 0.9)', 'rgba(30,41,59,0.85)')
css = css.replace('rgba(255, 255, 255, 0.6)', 'rgba(30,41,59,0.5)')

# 5. Accent Gradients -> Professional Indigo/Blue
css = css.replace('linear-gradient(135deg, #4f46e5, #7c3aed, #2563eb)', 'linear-gradient(135deg, #3b82f6, #6366f1, #8b5cf6)')
css = css.replace('linear-gradient(135deg, #4f46e5, #7c3aed)', 'linear-gradient(135deg, #3b82f6, #6366f1)')
css = css.replace('linear-gradient(90deg, rgba(99,102,241,0.08), rgba(139,92,246,0.08))', 'linear-gradient(90deg, rgba(59,130,246,0.1), rgba(99,102,241,0.1))')
css = css.replace('rgba(99,102,241,0.2)', 'rgba(59,130,246,0.25)')

# 6. Specific Text Overrides
css = css.replace('color: #0f172a;', 'color: #f8fafc;')
# Reduce text shadow glow on transparent
css = css.replace('color: transparent;', 'color: transparent; text-shadow: 0 0 10px rgba(59,130,246,0.15);')

# 7. Holographic KPI Glows (Keep them subtle and elegant)
css = css.replace('rgba(99,102,241,0.15)', 'rgba(59,130,246,0.15)') # cool-glow
css = css.replace('rgba(139,92,246,0.12)', 'rgba(99,102,241,0.15)')
css = css.replace('rgba(37,99,235,0.15)', 'rgba(56,189,248,0.15)')
css = css.replace('rgba(56,189,248,0.12)', 'rgba(14,165,233,0.15)')

css = css.replace('rgba(244,63,94,0.12)', 'rgba(239,68,68,0.15)') # danger-glow
css = css.replace('rgba(225,29,72,0.1)', 'rgba(220,38,38,0.15)')
css = css.replace('rgba(245,158,11,0.15)', 'rgba(245,158,11,0.15)') # warm-glow
css = css.replace('rgba(249,115,22,0.1)', 'rgba(234,88,12,0.15)')

css = css.replace('rgba(16,185,129,0.12)', 'rgba(16,185,129,0.15)') # green
css = css.replace('rgba(5,150,105,0.1)', 'rgba(5,150,105,0.15)')

# 8. Force Streamlit Base Elements to be dark (Slate overrides)
hard_dark_overrides = '''
/* Slate 900 Targetting */
.stSelectbox div[data-baseweb="select"] > div {
    background-color: #1e293b !important;
    border-color: #334155 !important;
    color: #f8fafc !important;
}
.stSelectbox div[data-baseweb="select"] span {
    color: #f8fafc !important;
}
.stSlider div[data-baseweb="slider"] .st-bc {
    background-color: #334155 !important;
}
.stToggle div[data-testid="stWidgetLabel"] p {
    color: #3b82f6 !important;
    font-weight: 500;
}
button.st-emotion-cache-121stq9 {
    background-color: #1e293b !important;
    border: 1px solid #334155 !important;
    color: #f8fafc !important;
}
button.st-emotion-cache-121stq9:hover {
    border-color: #3b82f6 !important;
    box-shadow: 0 0 8px rgba(59,130,246,0.2) !important;
}
'''
css += hard_dark_overrides

with open('.streamlit/climate_scope_dark.css', 'w', encoding='utf-8') as f:
    f.write(css)
print('Professional Slate Palette applied.')
