"""Inert entry. Caller must verify this file before initial execution; see commands."""
from pathlib import Path
import argparse,hashlib,types
def main(argv=None):
    p=argparse.ArgumentParser();p.add_argument('--bootstrap-sha256',required=True);p.add_argument('--source-manifest-sha256',required=True);p.add_argument('--gate-sha256',required=True)
    p.add_argument('--activation-sha256');p.add_argument('--root-review-sha256');p.add_argument('--independent-review-sha256')
    p.add_argument('mode',choices=['preflight-readonly','execute-reviewed','reconcile-readonly']);a=p.parse_args(argv)
    q=Path(__file__).resolve().with_name('bootstrap.py');b=q.read_bytes()
    if hashlib.sha256(b).hexdigest()!=a.bootstrap_sha256:raise RuntimeError('Externally pinned bootstrap mismatch')
    m=types.ModuleType('_captured_verified_bootstrap');m.__file__=str(q);exec(compile(b,str(q),'exec',optimize=0),m.__dict__)
    modules,verify=m.load_verified(a.source_manifest_sha256)
    return modules['bridge'].main(a,verify,modules)
if __name__=='__main__':main()
