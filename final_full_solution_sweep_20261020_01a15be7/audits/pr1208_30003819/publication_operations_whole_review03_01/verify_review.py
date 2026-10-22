"""Read-only exact custody verifier for this bounded PR1208 review."""
from pathlib import Path
import hashlib,json,stat,zipfile
ROOT=Path(__file__).resolve().parent
def need(ok,message):
    if not ok:raise RuntimeError(message)
def pin(b):return {"bytes":len(b),"sha256":hashlib.sha256(b).hexdigest()}
def main():
    m=json.loads((ROOT/"MANIFEST.json").read_text());entries=m["entries"]
    actual={"."}|{str(p.relative_to(ROOT))for p in ROOT.rglob("*")if p.name!="MANIFEST.json"}
    need(actual==set(entries),"Review closed membership")
    for n,v in entries.items():
        p=ROOT if n=="."else ROOT/n;s=p.lstat()
        need(not p.is_symlink()and stat.S_IMODE(s.st_mode)==v["mode"]and s.st_mtime_ns==v["mtime_ns"],"Review metadata "+n)
        if v["kind"]=="file":need(pin(p.read_bytes())=={"bytes":v["bytes"],"sha256":v["sha256"]},"Review bytes "+n)
        else:need(p.is_dir(),"Review directory "+n)
    cp=json.loads((ROOT/"OWN_SOURCE_COPY.json").read_text());source=Path(cp["root"])
    need({str(p.relative_to(source))for p in source.rglob("*")if p.is_file()}==set(cp["entries"]),"Own source copy closure")
    for n,v in cp["entries"].items():
        p=source/n;s=p.stat()
        need(pin(p.read_bytes())=={"bytes":v["bytes"],"sha256":v["sha256"]}and stat.S_IMODE(s.st_mode)==v["mode"]and s.st_mtime_ns==v["mtime_ns"],"Own source copy changed")
    files=0
    for mp in (ROOT/"private/physical").glob("*.manifest.json"):
        v=json.loads(mp.read_text());archive=mp.parent/v["archive"];need(pin(archive.read_bytes())==v["archive_pin"],"Archive pin")
        with zipfile.ZipFile(archive)as z:
            need(z.testzip()is None and set(z.namelist())=={e["path"]for e in v["entries"]},"Archive closure/CRC")
            for e in v["entries"]:need(pin(z.read(e["path"]))=={"bytes":e["bytes"],"sha256":e["sha256"]},"Archive member");files+=1
    print(json.dumps({"status":"EXACT_CLOSED_REVIEW_PASS","review_files":m["files"],"review_directories":m["directories"],"archived_physical_files":files,"decision":"HOLD","operational_authority":False}))
if __name__=="__main__":main()
