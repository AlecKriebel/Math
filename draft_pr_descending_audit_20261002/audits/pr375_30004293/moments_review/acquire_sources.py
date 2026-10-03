#!/usr/bin/env python3
"""Read-only source acquisition. Third-party bytes remain under ignored tmp/."""
import datetime, hashlib, json, pathlib, subprocess

BASE = pathlib.Path(__file__).resolve().parent
PRIVATE = BASE / "tmp" / "sources"
SOURCES = {
    "green_owr2019": "https://ems.press/content/serial-article-files/46829",
    "fgk_arxiv_v3": "https://arxiv.org/pdf/1908.00378v3",
    "fgk_published": "https://link.springer.com/content/pdf/10.1007/s00222-022-01177-y.pdf",
    "mao_song_v2": "https://arxiv.org/pdf/2609.22296v2",
    "tenenbaum_powers": "https://tenenb.perso.math.cnrs.fr/PPP/Delta%28n%5Er%29.pdf",
}

def now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()

def main():
    PRIVATE.mkdir(parents=True, exist_ok=True)
    result = {"started_utc": now(), "private_storage": str(PRIVATE), "sources": []}
    for identity, url in SOURCES.items():
        raw = PRIVATE / (identity + ".pdf")
        cmd = ["/usr/bin/curl", "-L", "--fail", "--silent", "--show-error", url, "-o", str(raw)]
        completed = subprocess.run(cmd, capture_output=True, text=True)
        item = {"identity": identity, "url": url, "access_utc": now(), "command": cmd,
                "returncode": completed.returncode, "stdout": completed.stdout, "stderr": completed.stderr}
        if completed.returncode == 0:
            data = raw.read_bytes()
            item.update(bytes=len(data), sha256=hashlib.sha256(data).hexdigest(), pdf_header=data[:8].decode("ascii", "replace"))
            text_path = PRIVATE / (identity + ".txt")
            extract = subprocess.run(["/opt/homebrew/bin/pdftotext", "-layout", str(raw), str(text_path)], capture_output=True, text=True)
            item["extract"] = {"returncode": extract.returncode, "stdout": extract.stdout, "stderr": extract.stderr}
        result["sources"].append(item)
    result["ended_utc"] = now()
    (BASE / "SOURCE_IDENTITY.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()
