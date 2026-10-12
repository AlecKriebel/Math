#!/usr/bin/env python3
from pathlib import Path, PurePosixPath
import hashlib, json, stat, zipfile

HERE=Path(__file__).resolve().parent
archive=HERE/"verification.zip"
target=HERE/"archive_replay"
target.mkdir(exist_ok=False)
items=[]; seen=set()
with zipfile.ZipFile(archive) as z:
    for info in z.infolist():
        p=PurePosixPath(info.filename)
        if info.filename in seen or p.is_absolute() or '..' in p.parts or '\\' in info.filename:
            raise RuntimeError("Unsafe or duplicate archive path: "+info.filename)
        seen.add(info.filename)
        mode=info.external_attr>>16
        if stat.S_ISLNK(mode): raise RuntimeError("Symlink archive entry: "+info.filename)
        if info.is_dir():
            (target/str(p)).mkdir(parents=True,exist_ok=True)
            continue
        body=z.read(info)
        out=target/str(p); out.parent.mkdir(parents=True,exist_ok=True); out.write_bytes(body)
        permissions=stat.S_IMODE(mode) or 0o644
        out.chmod(permissions)
        items.append({"path":str(p),"bytes":len(body),"sha256":hashlib.sha256(body).hexdigest(),"archive_mode_octal":format(permissions,"04o")})
inventory={"archive_sha256":hashlib.sha256(archive.read_bytes()).hexdigest(),"regular_files":len(items),"duplicate_paths":False,"traversal_paths":False,"symlinks":False,"payloads":items}
(HERE/"ARCHIVE_INVENTORY.json").write_text(json.dumps(inventory,indent=2)+"\n")
print(json.dumps({"archive_sha256":inventory["archive_sha256"],"regular_files":len(items),"paths":[i["path"] for i in items]},indent=2))
