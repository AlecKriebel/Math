"""Narrow preserved record fields and PDF pixel reproducibility; no third-party text copying."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import subprocess

OWN = Path(__file__).resolve().parent
CASE = OWN.parent


def main():
    output = OWN / "final_readbacks"
    output.mkdir(exist_ok=False)
    records = []
    for name in ("ORIGINAL_PR_METADATA.json","original_submitted_head/source_record.json","priority_audit_01/private_acquisition_cache/zenodo_23096994.json"):
        f = CASE / name
        data = json.loads(f.read_text())
        selected = {k:v for k,v in data.items() if k in ("created_at","updated_at","head","created","modified","id","doi","publication_date","version","sha","commit","committer","committedDate","date")}
        if "metadata" in data:
            selected["metadata_selected"] = {k:v for k,v in data["metadata"].items() if k in ("publication_date","version","title")}
        records.append({"path":str(f),"bytes":f.stat().st_size,"sha256":hashlib.sha256(f.read_bytes()).hexdigest(),"top_level_keys":list(data),"selected":selected})
    book = CASE / "priority_audit_01/private_acquisition_cache/poncelet_surprises_preview.pdf"
    p = subprocess.run(["/opt/homebrew/bin/pdftotext","-f","1","-l","15","-layout",str(book),"-"],capture_output=True,text=True,timeout=60)
    if p.returncode:
        raise RuntimeError("Book extraction failed")
    lines = p.stdout.splitlines()
    hits = [line.strip() for line in lines if "Invariant area product" in line]
    if not hits:
        raise RuntimeError("Book TOC heading absent")
    records.append({"path":str(book),"bytes":book.stat().st_size,"sha256":hashlib.sha256(book.read_bytes()).hexdigest(),"observed_toc_heading":hits,"full_section_read":False})
    rendered = output / "rebuilt_pages"
    rendered.mkdir()
    argv = ["/opt/homebrew/bin/pdftoppm","-r","110","-png",str(OWN / "tex_rebuild/focal_inverse_area_product.pdf"),str(rendered / "page")]
    r = subprocess.run(argv,cwd=OWN,capture_output=True,text=True,timeout=60)
    run = {"argv":argv,"exit":r.returncode,"stdout":r.stdout,"stderr":r.stderr}
    if r.returncode:
        raise RuntimeError("Rebuilt render failed")
    pixels = []
    for page in range(1,7):
        original = OWN / ("pdf_review/page-"+str(page)+".png")
        rebuilt = rendered / ("page-"+str(page)+".png")
        equal = original.read_bytes() == rebuilt.read_bytes()
        pixels.append({"page":page,"png_byte_identical":equal,"original_sha256":hashlib.sha256(original.read_bytes()).hexdigest(),"rebuilt_sha256":hashlib.sha256(rebuilt.read_bytes()).hexdigest()})
        if not equal:
            raise RuntimeError("Page render differs")
    result = {"status":"PASS","utc":datetime.now(timezone.utc).isoformat(),"records":records,"render_run":run,"pixels":pixels}
    (output / "results.json").write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps(result,indent=2))


if __name__ == "__main__":
    main()
