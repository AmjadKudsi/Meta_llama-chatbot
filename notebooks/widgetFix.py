# widgetFix.py
import sys
from pathlib import Path
import nbformat

def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: python widgetFix.py <notebookname>.ipynb")
        return 2

    in_path = Path(sys.argv[1]).expanduser().resolve()
    if not in_path.exists():
        print(f"Error: file not found: {in_path}")
        return 2
    if in_path.suffix.lower() != ".ipynb":
        print(f"Error: input must be a .ipynb file: {in_path}")
        return 2

    out_path = in_path.with_name(f"{in_path.stem}_fixed{in_path.suffix}")

    nb = nbformat.read(str(in_path), as_version=nbformat.NO_CONVERT)

    md = nb.get("metadata", {})
    widgets = md.get("widgets", None)

    # If widgets metadata exists but is missing required state, add it.
    # Some notebooks store widgets metadata under a mimetype key; handle both cases.
    if isinstance(widgets, dict):
        if "state" not in widgets:
            widgets["state"] = {}
        for k, v in list(widgets.items()):
            if isinstance(v, dict) and k != "state" and "state" not in v:
                v["state"] = {}
        md["widgets"] = widgets
        nb["metadata"] = md

    nbformat.write(nb, str(out_path))
    print("Wrote:", out_path)
    return 0

if __name__ == "__main__":
    raise SystemExit(main())