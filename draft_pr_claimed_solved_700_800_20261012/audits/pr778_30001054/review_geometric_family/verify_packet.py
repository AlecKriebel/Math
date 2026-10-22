#!/usr/bin/env python3
"""Read-only recursive custody verification; optional current-input identity."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import stat

def require(condition,message):
    if not condition:
        raise ValueError(message)

def scan(root):
    files = {}
    dirs = []
    def walk(path,rel):
        entries = sorted(os.scandir(path), key=lambda x:x.name)
        require(bool(entries), "empty directory: " + (rel or "."))
        for ent in entries:
            name = rel + "/" + ent.name if rel else ent.name
            mode = ent.stat(follow_symlinks=False).st_mode
            require(not stat.S_ISLNK(mode), "symlink: " + name)
            if stat.S_ISDIR(mode):
                dirs.append(name)
                walk(Path(ent.path),name)
            elif stat.S_ISREG(mode):
                if name == "MANIFEST.json":
                    continue
                data = Path(ent.path).read_bytes()
                files[name] = {"bytes":len(data),"sha256":hashlib.sha256(data).hexdigest()}
            else:
                raise ValueError("special entry: " + name)
    walk(root,"")
    return files,dirs

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--current-inputs",action="store_true")
    args = parser.parse_args()
    root = Path(__file__).resolve().parent
    # Root itself may not be a symlink; child check does not follow links.
    require(not Path(__file__).parent.is_symlink(), "packet root is a symlink")
    require(stat.S_ISREG((root/"MANIFEST.json").lstat().st_mode), "manifest is not a regular file")
    got,dirs = scan(root)
    manifest = json.loads((root/"MANIFEST.json").read_text())
    require(got == manifest["files"], "recursive file inventory differs")
    require(sorted(dirs) == manifest["directories"], "directory inventory differs")
    result = {"custody":"PASS","files":len(got),"directories":len(dirs),
              "mtime_used":False,"current_inputs":"NOT_CHECKED"}
    if args.current_inputs:
        identity = json.loads((root/"INPUT_IDENTITY.json").read_text())
        for rec in identity["files"]:
            p = root/rec["path"]
            require(not p.is_symlink(), "current input is symlink")
            data = p.read_bytes()
            require(len(data)==rec["bytes"] and hashlib.sha256(data).hexdigest()==rec["sha256"],
                    "current input mismatch: "+rec["path"])
        result["current_inputs"] = "PASS_SEPARATE_FROM_CUSTODY"
    print(json.dumps(result,sort_keys=True))

if __name__ == "__main__":
    main()
