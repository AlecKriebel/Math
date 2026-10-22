"""Read-only retrieval of supplementary primary leads supplied during review."""
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import json
from retrieve_public import retrieve

REQUESTS = [
    ("ganita2017", "https://bharataganitaparisad.com/wp-content/uploads/2017/07/chapter-1-vol67.pdf"),
    ("naudts_zhang2018", "https://repository.uantwerpen.be/docman/irua/6c9ab9/152812.pdf"),
    ("naudts_zhang2017", "https://sites.lsa.umich.edu/m3lab/wp-content/uploads/sites/1376/2024/11/2017-GSI_25_Chapter-Naudts-and-Zhang.pdf"),
    ("naudts_zhang2019", "https://www.simis.cn/wp-content/uploads/2024/05/2019-Naudts-and-Zhang-GSI-volume-chapter.pdf"),
]
if __name__ == "__main__":
    with ThreadPoolExecutor(max_workers=4) as pool:
        records = list(pool.map(retrieve, REQUESTS))
    (Path(__file__).resolve().parent / "SUPPLEMENTARY_RETRIEVAL.json").write_text(json.dumps(records, indent=2) + "\n")
    print(json.dumps(records, indent=2))
