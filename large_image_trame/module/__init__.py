from pathlib import Path

# Compute local path to serve
serve_path = str(Path(__file__).with_name("serve").resolve())

# Serve directory for JS/CSS files
serve = {"__large_image_trame": serve_path}

# List of JS files to load (usually from the serve path above)
scripts = ["__large_image_trame/vue-large_image_trame.umd.min.js"]

# List of CSS files to load (usually from the serve path above)
styles = ["__large_image_trame/vue-large_image_trame.css"]

vuetify_config = {}

# List of Vue plugins to install/load
vue_use = ["large_image_trame", ("trame_vuetify", vuetify_config)]

# Uncomment to add entries to the shared state
# state = {}


# Optional if you want to execute custom initialization at module load
def setup(app, **kwargs):
    """Method called at initialization with possibly some custom keyword arguments"""
    pass
