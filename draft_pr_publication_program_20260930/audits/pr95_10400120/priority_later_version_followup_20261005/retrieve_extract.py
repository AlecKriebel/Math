from pathlib import Path
import urllib.request, urllib.error, datetime, hashlib, json, os, subprocess, sys
P = Path(__file__).resolve().parent
def now(): return datetime.datetime.now(datetime.timezone.utc).isoformat()
def sha(b): return hashlib.sha256(b).hexdigest()
def retrieve(name, url):
    r = {"name": name, "url": url, "UTC_start": now(), "operator_PID": os.getpid(), "method": "urllib.request.Request/urlopen", "user_agent": "IndependentSourceAudit/1.0", "timeout_seconds": 35}
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "IndependentSourceAudit/1.0"})
        with urllib.request.urlopen(req, timeout=35) as f:
            b = f.read(); r.update({"status": f.status, "effective_url": f.url, "headers": dict(f.headers.items())})
    except urllib.error.HTTPError as e:
        b = e.read(); r.update({"status": e.code, "effective_url": e.url, "headers": dict(e.headers.items()), "error": str(e)})
    except Exception as e:
        b = b""; r.update({"error": repr(e)})
    suffix = ".pdf" if b.startswith(b"%PDF-") else ".html" if b else ".empty"
    path = P / "private_sources" / (name + suffix); path.write_bytes(b)
    r.update({"UTC_finish": now(), "path": str(path.relative_to(P)), "bytes": len(b), "sha256": sha(b), "magic": repr(b[:12]), "PDF": b.startswith(b"%PDF-")})
    (P / "processes" / ("retrieval_" + name + ".json")).write_text(json.dumps(r, indent=2) + "\n")
    print(json.dumps({k: r.get(k) for k in ["name", "status", "bytes", "sha256", "PDF", "error"]}), flush=True)
    if r["PDF"]:
        argv = ["/opt/homebrew/bin/pdftotext", "-layout", str(path), str(path.with_suffix(".txt"))]
        q = {"operator_PID": os.getpid(), "UTC_start": now(), "argv": argv, "script_sha256": sha(Path(__file__).read_bytes()), "source_sha256": r["sha256"]}
        proc = subprocess.Popen(argv, stdout=subprocess.PIPE, stderr=subprocess.PIPE); q["child_PID"] = proc.pid
        out, err = proc.communicate()
        q.update({"UTC_finish": now(), "exit": proc.returncode, "stdout": out.decode(errors="replace"), "stderr": err.decode(errors="replace")})
        q["extraction_sha256"] = sha(path.with_suffix(".txt").read_bytes()) if path.with_suffix(".txt").exists() else None
        (P / "processes" / ("extract_" + name + ".json")).write_text(json.dumps(q, indent=2) + "\n")
    return r
if __name__ == "__main__":
    requests = [
        ("gang_v2", "https://arxiv.org/pdf/0912.4664v2"),
        ("gang_abs_v2", "https://arxiv.org/abs/0912.4664v2"),
        ("kubo_yokoyama_v2", "https://arxiv.org/pdf/2108.09300v2"),
        ("kubo_yokoyama_abs_v2", "https://arxiv.org/abs/2108.09300v2"),
        ("kubo_yokoyama_final", "https://link.springer.com/content/pdf/10.1007/JHEP04(2022)074.pdf"),
        ("kubo_yokoyama_final_metadata", "https://link.springer.com/article/10.1007/JHEP04(2022)074"),
        ("gang_final", "https://link.springer.com/content/pdf/10.3938/jkps.74.1119.pdf"),
        ("gang_final_metadata", "https://link.springer.com/article/10.3938/jkps.74.1119"),
    ]
    if len(sys.argv) > 1: requests = [r for r in requests if r[0] in sys.argv[1:]]
    for name, url in requests: retrieve(name, url)
