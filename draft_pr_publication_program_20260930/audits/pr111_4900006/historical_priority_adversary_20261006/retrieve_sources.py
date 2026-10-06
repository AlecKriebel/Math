"""Read-only bounded public retrieval; no credentials or external outreach."""
from pathlib import Path
import concurrent.futures, datetime, hashlib, json, subprocess

ROOT = Path(__file__).resolve().parent
SOURCES = [
    ("eft1991_official_pdf", "https://link.springer.com/content/pdf/10.1007/BF01049491.pdf"),
    ("eft1991_official_landing", "https://link.springer.com/article/10.1007/BF01049491"),
    ("iucat_title_search", "https://iucat.iu.edu/catalog?search_field=all_fields&q=An+abstract+theory+of+L-exponents"),
    ("iu_scholarworks_search", "https://scholarworks.iu.edu/dspace/search?query=Eden%20L-exponents"),
    ("eden2017_author_retrospective", "https://pde.iyte.edu.tr/wp-content/uploads/sites/166/2015/12/booklet.pdf"),
    ("eden_cv_author", "https://tubitak.gov.tr/tubitak_content_files/haber/kamuoyu_duyurusu/Alp_Eden.pdf"),
]

def retrieve(item):
    key, url = item
    body = ROOT / "private_retrieval" / (key + ".body")
    headers = ROOT / "private_retrieval" / (key + ".headers")
    started = datetime.datetime.now(datetime.timezone.utc).isoformat()
    cmd = ["/usr/bin/curl", "--silent", "--show-error", "--location", "--max-time", "40", "--max-filesize", "12000000", "--dump-header", str(headers), "--output", str(body), "--write-out", "%{http_code}\n%{url_effective}\n%{content_type}\n%{size_download}\n", url]
    try:
        p = subprocess.run(cmd, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=45, check=False)
        data = body.read_bytes() if body.exists() else b""
        return {"key": key, "url": url, "started_utc": started, "finished_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(), "returncode": p.returncode, "curl_metadata": p.stdout.decode(errors="replace"), "stderr": p.stderr.decode(errors="replace"), "private_body": str(body.relative_to(ROOT)), "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest(), "pdf_magic": data.startswith(b"%PDF-")}
    except subprocess.TimeoutExpired as e:
        return {"key": key, "url": url, "started_utc": started, "timeout": True, "stdout": (e.stdout or b"").decode(errors="replace"), "stderr": (e.stderr or b"").decode(errors="replace")}

if __name__ == "__main__":
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        records = list(executor.map(retrieve, SOURCES))
    out = {"schema": "pr111-historical-public-retrieval/v1", "records": records, "copyright_material_private_ignored": True, "no_access_circumvention": True}
    (ROOT / "PUBLIC_RETRIEVAL_RECEIPT.json").write_text(json.dumps(out, indent=2, sort_keys=True) + "\n")
    print(json.dumps(out, indent=2, sort_keys=True))
