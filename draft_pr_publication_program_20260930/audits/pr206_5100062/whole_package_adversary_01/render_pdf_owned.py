"""Read-only PDF rendering/extraction, with audit-owned output and logs."""
from pathlib import Path
import json
import subprocess
from datetime import datetime, timezone

OWN = Path(__file__).resolve().parent
PDF = OWN.parent / "publication_package_v1/focal_inverse_area_product.pdf"


def main():
    out = OWN / "pdf_review"
    out.mkdir(exist_ok=False)
    attempts = []
    for label, argv in [
        ("pdfinfo", ["/opt/homebrew/bin/pdfinfo", str(PDF)]),
        ("pdftotext", ["/opt/homebrew/bin/pdftotext", "-layout", str(PDF), str(out / "paper.txt")]),
        ("pdftoppm", ["/opt/homebrew/bin/pdftoppm", "-r", "110", "-png", str(PDF), str(out / "page")]),
        ("tectonic_help", ["/opt/homebrew/bin/tectonic", "--help"]),
    ]:
        p = subprocess.run(argv, capture_output=True, text=True, timeout=60, cwd=OWN)
        attempts.append({"label": label, "utc": datetime.now(timezone.utc).isoformat(), "argv": argv, "exit": p.returncode, "stdout": p.stdout, "stderr": p.stderr})
        if p.returncode:
            raise RuntimeError("Tool failed: "+label)
    (out / "tool_runs.json").write_text(json.dumps(attempts, indent=2)+"\n")
    print(json.dumps({"status": "PASS", "pngs": [str(x) for x in sorted(out.glob("page-*.png"))], "tools": attempts}, indent=2))


if __name__ == "__main__":
    main()
