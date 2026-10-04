"""Independent source fetch. No candidate files are read by this script."""
import concurrent.futures
import datetime as dt
import hashlib
import json
import pathlib
import subprocess
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parent
SOURCES = [
    ("hayman_lingham", "https://arxiv.org/pdf/1809.07200v2", "8e28fd4403a07e4e19a9816b7efaafddf9f475d59cf8c34a8255cb03833ed4f0"),
    ("demailly_exey", "https://www-fourier.univ-grenoble-alpes.fr/~demailly/manuscripts/ex%2Bey1.pdf", "3b1186f5d3bc3da17069d57736adc740a9546cda63523c7ff69b029a7e534a3a"),
    ("demailly_cras", "https://www-fourier.univ-grenoble-alpes.fr/~demailly/manuscripts/cras_ex%2Bey1.pdf", "eabbfed01fd1ed874dc431482e46a931876652b41d7a3b0139f35f83042ab31b"),
    ("lin_zaidenberg", "https://arxiv.org/pdf/alg-geom/9611020v2", "a54890d8478b4d8aa5ad9778f865afdc11a2d3ee48638993286da6a5b92b1dda"),
    ("class_b", "https://arxiv.org/pdf/1502.00492v2", "b466809a0cf69cf881fbc1a60cc5811800d5a1e35262d6ebf2003f704cccabdc"),
]

def fetch(item):
    name, url, expected = item
    rec = {"id": name, "requested_url": url, "routing_sha256": expected,
           "started_utc": dt.datetime.now(dt.timezone.utc).isoformat()}
    try:
        with urllib.request.urlopen(url, timeout=40) as r:
            raw = r.read()
            rec.update(final_url=r.url, http_status=r.status,
                       content_type=r.headers.get("content-type"))
        path = ROOT / "private_sources" / (name + ".pdf")
        path.write_bytes(raw)
        rec.update(bytes=len(raw), sha256=hashlib.sha256(raw).hexdigest(),
                   routing_hash_matches=hashlib.sha256(raw).hexdigest() == expected)
        p = subprocess.run(["pdftotext", "-layout", str(path), str(path.with_suffix(".txt"))],
                           capture_output=True, text=True)
        rec.update(extraction_exit=p.returncode, extraction_stderr=p.stderr)
        if path.with_suffix(".txt").exists():
            rec["extracted_sha256"] = hashlib.sha256(path.with_suffix(".txt").read_bytes()).hexdigest()
    except Exception as e:
        rec["failure"] = type(e).__name__ + ": " + str(e)
    rec["finished_utc"] = dt.datetime.now(dt.timezone.utc).isoformat()
    return rec

if __name__ == "__main__":
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as pool:
        rows = list(pool.map(fetch, SOURCES))
    receipt = {"method": "independent urllib primary URL downloads and pdftotext layout extraction",
               "earlier_web_access_failure": {"url": SOURCES[1][1], "failure": "web open internal error"},
               "sources": rows}
    (ROOT / "PRIMARY_ACCESS_RECEIPTS.json").write_text(json.dumps(receipt, indent=2) + "\n")
    print(json.dumps(rows, indent=2))
