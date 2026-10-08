#!/usr/bin/env python3
"""Externally pinned launcher; authenticate the verifier before execution."""
from pathlib import Path
import hashlib,sys
EXPECTED_VERIFIER="e6a6d4ffde1d3aa0fd0ea6fc21acb26548cdcfd9921d890b267a9bf87c828876"
EXPECTED_MANIFEST="e1aa37ba35b8f119e6e97c632bbd7d29e049dd94722a1253293e793eb7973305"
def reject(message):
    print("REJECT: "+message,file=sys.stderr);sys.exit(1)
def main():
    here=Path(__file__).absolute().parent
    if len(sys.argv)>3:reject("usage: BOOTSTRAP.py [ROOT [--integrity-only]]")
    root=Path(sys.argv[1]).absolute() if len(sys.argv)>1 else here
    if len(sys.argv)==3 and sys.argv[2]!="--integrity-only":reject("unknown option")
    if root.is_symlink() or not root.is_dir():reject("root symlink or not directory")
    for name in ("BOOTSTRAP.py","VERIFY_PUBLICATION.py","PUBLICATION_MANIFEST.json"):
        p=root/name
        if p.is_symlink() or not p.is_file():reject("missing or symlink trust member")
    if (root/"BOOTSTRAP.py").read_bytes()!=Path(__file__).read_bytes():reject("different bootstrap copy")
    code=(root/"VERIFY_PUBLICATION.py").read_bytes()
    if hashlib.sha256(code).hexdigest()!=EXPECTED_VERIFIER:reject("verifier trust anchor")
    if hashlib.sha256((root/"PUBLICATION_MANIFEST.json").read_bytes()).hexdigest()!=EXPECTED_MANIFEST:reject("manifest trust anchor")
    sys.argv=[str(root/"VERIFY_PUBLICATION.py"),str(root)]+sys.argv[2:]
    exec(compile(code,str(root/"VERIFY_PUBLICATION.py"),"exec"),{"__name__":"__main__","__file__":str(root/"VERIFY_PUBLICATION.py")})
if __name__=="__main__":
    try:main()
    except (OSError,ValueError,TypeError) as e:reject(str(e))
