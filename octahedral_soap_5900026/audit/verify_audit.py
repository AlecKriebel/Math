#!/usr/bin/env python3
"""Verify this independently anchored flat audit packet and replay its checks."""
from pathlib import Path
import argparse,hashlib,json,subprocess,sys,tempfile,shutil

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--manifest-sha256',required=True)
    ap.add_argument('--original-packet',type=Path)
    args=ap.parse_args();root=Path(__file__).resolve().parent
    raw=(root/'AUDIT_MANIFEST.json').read_bytes()
    if hashlib.sha256(raw).hexdigest()!=args.manifest_sha256:raise RuntimeError('Audit manifest anchor mismatch')
    m=json.loads(raw)
    if any(not p.is_file() or p.is_symlink() for p in root.iterdir()):raise RuntimeError('Audit must be a flat nonsymlink directory')
    if {p.name for p in root.iterdir()}!=set(m['files'])|{'AUDIT_MANIFEST.json'}:raise RuntimeError('Audit inventory mismatch')
    for name,meta in m['files'].items():
        if Path(name).name!=name:raise RuntimeError('Invalid inventory path')
        raw=(root/name).read_bytes()
        if len(raw)!=meta['bytes'] or hashlib.sha256(raw).hexdigest()!=meta['sha256']:raise RuntimeError('Audit payload mismatch: '+name)
    for opts in ([],['-O']):
        got=subprocess.check_output([sys.executable]+opts+[str(root/'independent_controls.py')],cwd=root)
        if got!=(root/'INDEPENDENT_RESULTS.json').read_bytes():raise RuntimeError('Independent replay mismatch')
    original_checked=False
    if args.original_packet:
        original=args.original_packet.resolve()
        subprocess.check_output([sys.executable,str(original/'verify_packet.py'),'--manifest-sha256',m['original_manifest_sha256']])
        receipt=json.loads((root/'CORRECTION_RECEIPT.json').read_text())
        if hashlib.sha256((original/'MATHEMATICAL_NOTE.md').read_bytes()).hexdigest()!=receipt['original_sha256']:raise RuntimeError('Original note mismatch')
        with tempfile.TemporaryDirectory(prefix='octahedral-audit-apply-') as td:
            shutil.copy(original/'MATHEMATICAL_NOTE.md',Path(td)/'MATHEMATICAL_NOTE.md')
            p=subprocess.run(['patch','--batch','--fuzz=0','-p1','-i',str(root/'CORRECTION.patch')],cwd=td,capture_output=True,text=True)
            if p.returncode or 'fuzz' in p.stdout or 'offset' in p.stdout:raise RuntimeError('Patch does not apply exactly')
            if (Path(td)/'MATHEMATICAL_NOTE.md').read_bytes()!=(root/'MATHEMATICAL_NOTE_CORRECTED.md').read_bytes():raise RuntimeError('Patch/read-copy disagreement')
        original_checked=True
    print(json.dumps({'result':'PASS_ANCHORED_AUDIT','manifest_sha256':args.manifest_sha256,'payload_files':len(m['files']),'independent_checks':1075,'normal_optimized_identical':True,'original_packet_and_patch_checked':original_checked},sort_keys=True,indent=2))
if __name__=='__main__':main()
