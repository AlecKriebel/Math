"""Read-only primary-source fetcher; all bodies stay in ignored sources/private/."""
from pathlib import Path
from urllib.request import Request, urlopen
import concurrent.futures
import datetime
import hashlib
import json
import subprocess
import sys

HERE = Path(__file__).resolve().parent


def fetch(row):
    name, url = row
    if Path(name).name != name:
        raise ValueError("A source name must be a basename")
    result = {"path": name, "requested_url": url,
              "fetched_utc": datetime.datetime.now(datetime.timezone.utc).isoformat()}
    target = HERE / "sources" / "private" / name
    try:
        with urlopen(Request(url, headers={"User-Agent": "Mozilla/5.0"}), timeout=40) as response:
            body = response.read()
            target.write_bytes(body)
            allowed = {"content-type", "content-length", "date", "etag", "last-modified", "cache-control", "location"}
            result.update(status=response.status, resolved_url=response.url,
                          headers={key: value for key, value in response.headers.items()
                                   if key.lower() in allowed}, bytes=len(body),
                          is_pdf_content=body.startswith(b"%PDF"),
                          sha256=hashlib.sha256(body).hexdigest(),
                          md5=hashlib.md5(body).hexdigest())
        if body.startswith(b"%PDF"):
            subprocess.run(["pdftotext", "-layout", str(target), str(target.with_suffix(".txt"))],
                           check=True, capture_output=True)
    except Exception as error:
        result["error"] = type(error).__name__ + ": " + str(error)
    return result


if __name__ == "__main__":
    inputs = json.loads(Path(sys.argv[1]).read_text())
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as pool:
        results = list(pool.map(fetch, inputs.items()))
    destination = HERE / sys.argv[2]
    if destination.exists():
        raise FileExistsError(destination)
    destination.write_text(json.dumps(results, indent=2) + "\n")
    for row in results:
        print(row["path"], row.get("bytes"), row.get("sha256"), row.get("error"))
