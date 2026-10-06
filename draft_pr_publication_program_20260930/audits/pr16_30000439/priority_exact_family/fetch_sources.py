"""Fetch bounded-audit sources; preserve payloads only in ignored tmp."""
from pathlib import Path
import datetime, hashlib, json, subprocess, urllib.request

ROOT = Path(__file__).resolve().parent
SOURCES = {
    "owr_2006": "https://ems.press/content/serial-article-files/46044",
    "brehm_sarkaria_1992": "https://archive.mpim-bonn.mpg.de/id/eprint/1946/1/preprint_1992_52.pdf",
    "few_vertices": "https://arxiv.org/pdf/2109.04855",
    "newman_current": "https://arxiv.org/pdf/2212.09576",
    "newman_v1": "https://arxiv.org/pdf/2212.09576v1",
    "lee_nevo_v1": "https://arxiv.org/pdf/2307.14195v1",
    "lee_nevo_v3": "https://arxiv.org/pdf/2307.14195v3",
    "brehm_mobius_1983": "https://www.ams.org/journals/proc/1983-089-03/S0002-9939-1983-0715878-1/S0002-9939-1983-0715878-1.pdf",
    "surface_realization_2010": "https://www.or.uni-bonn.de/~hougardy/paper/SurfaceRealization.pdf",
    "winter_2_complexes_2024": "https://martinwintermath.github.io/pdf/publications/2_complexes_in_R4.pdf",
    "matousek_book": "https://webhomes.maths.ed.ac.uk/~v1ranick/papers/matousek1x.pdf",
    "brehm_schild_1995": "https://www.math.ucdavis.edu/~deloera/MISC/LA-BIBLIO/trunk/BrehmUlli/Brehm4.pdf",
    "heise_et_al_2014": "https://opikhurko.warwick.ac.uk/E/HeisePanagiotouPikhurkoTaraz14dcg.pdf",
    "newman_metadata": "https://arxiv.org/abs/2212.09576",
    "lee_nevo_metadata": "https://arxiv.org/abs/2307.14195",
    "few_vertices_metadata": "https://arxiv.org/abs/2109.04855",
    "lee_nevo_published": "https://link.springer.com/article/10.1007/s00454-026-00856-4",
    "newman_journal_record": "https://www.sciencedirect.com/science/article/pii/S0012365X26003559",
    "skopenkov_hypergraph_survey": "https://arxiv.org/pdf/1402.0658",
    "abrahamsen_kleist_miltzow_2023": "https://drops.dagstuhl.de/opus/volltexte/2023/17851/pdf/LIPIcs-SoCG-2023-1.pdf",
    "novik_2000": "https://link.springer.com/content/pdf/10.1007/PL00009501.pdf",
    "adiprasito_benedetti_current": "https://arxiv.org/pdf/1403.5217",
    "adiprasito_benedetti_v1": "https://arxiv.org/pdf/1403.5217v1",
    "adiprasito_patakova_current": "https://arxiv.org/pdf/2404.12265",
    "adiprasito_patakova_metadata": "https://arxiv.org/abs/2404.12265",
    "parsa_skopenkov_joins": "https://arxiv.org/pdf/2003.12285",
    "parsa_smith_joins": "https://arxiv.org/pdf/2103.02563",
    "melikhov_joins_products": "https://arxiv.org/pdf/2210.04015",
}

def main():
    ledger_path = ROOT / "source_hash_ledger.json"
    ledger = json.loads(ledger_path.read_text()) if ledger_path.exists() else {}
    (ROOT / "tmp").mkdir(exist_ok=True)
    for key, url in SOURCES.items():
        if key in ledger and ledger[key].get("sha256"):
            continue
        accessed = datetime.datetime.now(datetime.timezone.utc).isoformat()
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Independent mathematical literature audit/1.0"})
            with urllib.request.urlopen(req, timeout=90) as r:
                data, final_url, headers = r.read(), r.url, dict(r.headers)
            path = ROOT / "tmp" / (key + ".pdf")
            path.write_bytes(data)
            if data.startswith(b"%PDF"):
                subprocess.run(["pdftotext", "-layout", str(path), str(path.with_suffix(".txt"))], check=True)
            ledger[key] = {"url": url, "resolved_url": final_url, "accessed_utc": accessed,
                           "sha256": hashlib.sha256(data).hexdigest(), "bytes": len(data),
                           "payload": "tmp/" + path.name, "http_last_modified": headers.get("Last-Modified"),
                           "http_content_type": headers.get("Content-Type")}
        except Exception as e:
            ledger[key] = {"url": url, "accessed_utc": accessed, "error": str(e)}
        ledger_path.write_text(json.dumps(ledger, indent=2) + "\n")
        print(key, ledger[key].get("sha256", ledger[key].get("error")))

if __name__ == "__main__":
    main()
