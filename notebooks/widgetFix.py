import nbformat
from nbformat import read, write

in_path = "01_ingest_and_index.ipynb"   # change to your downloaded file name
out_path = "01_ingest_and_index.fixed.ipynb"

nb = nbformat.read(in_path, as_version=nbformat.NO_CONVERT)

md = nb.get("metadata", {})
widgets = md.get("widgets", None)

# If widgets metadata exists but is missing required state, add it.
# Some notebooks store widgets metadata under a mimetype key; handle both cases.
if isinstance(widgets, dict):
    if "state" not in widgets:
        widgets["state"] = {}
    # If it is a mimetype mapping, ensure each nested dict has state too.
    for k, v in list(widgets.items()):
        if isinstance(v, dict) and k != "state" and "state" not in v:
            v["state"] = {}
    md["widgets"] = widgets
    nb["metadata"] = md

nbformat.write(nb, out_path)
print("Wrote:", out_path)
