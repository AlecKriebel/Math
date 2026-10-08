#!/usr/bin/env python3
"""Externally pinned launcher. Verify this file's external hash before running."""
from pathlib import Path
import hashlib,sys
EXPECTED_VERIFIER="e0ca5a053b39a82f842e0c5c96b2d241255ca1c647bfb539039854398ee10205"
EXPECTED_MANIFEST="cbe331b23a13155d585e0da046c4bdff4079404ac216e7d60ca13c4285c8b445"
def reject(message):
    print("REJECT: "+message,file=sys.stderr);sys.exit(1)
def main():
    here=Path(__file__).absolute().parent
    args=sys.argv[1:]
    root=Path(args.pop(0)).absolute() if args and not args[0].startswith('--') else here
    if root.is_symlink() or not root.is_dir():reject("root symlink or not directory")
    for name in ("BOOTSTRAP.py","VERIFY_PUBLICATION.py","PUBLICATION_MANIFEST.json"):
        p=root/name
        if p.is_symlink() or not p.is_file():reject("missing or nonregular trust member")
    if (root/"BOOTSTRAP.py").read_bytes()!=Path(__file__).read_bytes():reject("different bootstrap copy")
    code=(root/"VERIFY_PUBLICATION.py").read_bytes()
    if hashlib.sha256(code).hexdigest()!=EXPECTED_VERIFIER:reject("verifier external pin")
    if hashlib.sha256((root/"PUBLICATION_MANIFEST.json").read_bytes()).hexdigest()!=EXPECTED_MANIFEST:reject("manifest external pin")
    sys.argv=[str(root/"VERIFY_PUBLICATION.py"),str(root)]+args
    exec(compile(code,str(root/"VERIFY_PUBLICATION.py"),"exec"),{"__name__":"__main__","__file__":str(root/"VERIFY_PUBLICATION.py")})
if __name__=="__main__":
    try:main()
    except (OSError,ValueError,TypeError) as e:reject(str(e))
