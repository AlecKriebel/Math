"""Hash decoded article payloads and retrieve classical-source supplements."""
from pathlib import Path
import datetime
import hashlib
import json
import urllib.request
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parent

def digest(data):
    return hashlib.sha256(data).hexdigest()

def payloads(path):
    reader = PdfReader(path)
    pages = []
    for page_number, page in enumerate(reader.pages, 1):
        resources = page.get("/Resources", {})
        xobjects = resources.get("/XObject", {})
        if hasattr(xobjects, "get_object"):
            xobjects = xobjects.get_object()
        images = []
        for name, reference in sorted(xobjects.items()):
            obj = reference.get_object()
            if obj.get("/Subtype") == "/Image":
                decoded = obj.get_data()
                images.append({"name": name, "width": obj.get("/Width"),
                               "height": obj.get("/Height"),
                               "decoded_bytes": len(decoded), "decoded_sha256": digest(decoded)})
        content = page.get_contents()
        pages.append({"pdf_page_one_based": page_number,
                      "printed_page": page_number + 350 if page_number > 1 else None,
                      "content_stream_sha256": digest(content.get_data()) if content else None,
                      "images": images})
    return {"metadata": {str(k): str(v) for k, v in reader.metadata.items()},
            "page_count": len(reader.pages), "pages": pages}

result = {"inspected_at_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
          "duren_initial": payloads(ROOT / ".cache/duren_1981_eth.pdf"),
          "supplementary_retrievals": []}
sources = [
    ("duren_1981_eth_second", "https://www.e-periodica.ch/cntmng?pid=com-001%3A1981%3A56%3A%3A30&bot=1"),
    ("pfluger_1971", "https://www.acadsci.fi/mathematica/1971/no489pp01-32.pdf"),
    ("brickman_wilken_1974", "https://www.ams.org/journals/proc/1974-042-02/S0002-9939-1974-0328057-1/S0002-9939-1974-0328057-1.pdf"),
]
for name, url in sources:
    item = {"source_id": name, "requested_url": url,
            "retrieved_at_utc": datetime.datetime.now(datetime.timezone.utc).isoformat()}
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0", "Cache-Control": "no-cache"})
        with urllib.request.urlopen(req, timeout=45) as response:
            data = response.read()
            item.update(status=response.status, resolved_url=response.url, bytes=len(data),
                        sha256=digest(data), content_type=response.headers.get("Content-Type"))
        if not data.startswith(b"%PDF"):
            raise RuntimeError("Non-PDF response")
        path = ROOT / ".cache" / f"{name}.pdf"
        path.write_bytes(data)
        item["cache_path"] = str(path.relative_to(ROOT))
        item["page_count"] = len(PdfReader(path).pages)
        if name == "duren_1981_eth_second":
            result["duren_second"] = payloads(path)
            result["duren_fresh_article_payloads_equal"] = (
                result["duren_initial"]["pages"][1:] == result["duren_second"]["pages"][1:])
            result["old_author_binary_equivalence"] = "not testable: old PDF not present in frozen package"
    except Exception as error:
        item["error"] = repr(error)
    result["supplementary_retrievals"].append(item)
    print(json.dumps(item))
(ROOT / "SOURCE_CONTENT_CHECK.json").write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps({"duren_fresh_article_payloads_equal": result.get("duren_fresh_article_payloads_equal")}))
