# Shared palette and style constants for the climate dashboard.
# Use these values in chart functions for cohesive theming.

# A discrete palette used for the Climate Risk Intelligence charts.
# These colors are chosen to emphasize risk severity (cooler = safer, warmer = higher risk).
CLIMATE_PALETTE = [
    "#2E7D32",  # green (low risk)
    "#F9A825",  # amber (moderate risk)
    "#D32F2F",  # red (high risk)
    "#6A1B9A",  # deep purple
    "#1565C0",  # blue
]

# A palette for the Precipitation & Wind Intelligence charts.
# Designed to evoke water and atmosphere with cool blues and teal accents.
PW_PALETTE = [
    "#1B4F72",  # deep ocean blue
    "#138D75",  # teal
    "#5499C7",  # sky blue
    "#7DCEA0",  # mint
    "#F4D03F",  # sun highlight
]

# A neon palette for line charts where high-contrast pop is desired.
NEON_PALETTE = [
    "#39FF14",  # electric green
    "#FF00FF",  # neon magenta
    "#00FFFF",  # neon cyan
    "#FFD700",  # neon yellow
    "#FF4500",  # neon orange
]

# A recommended continuous scale for heatmaps / choropleths.
CLIMATE_CONTINUOUS = "reds"
