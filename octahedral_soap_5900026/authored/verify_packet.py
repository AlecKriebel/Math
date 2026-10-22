#!/usr/bin/env python3
"""Verify an externally anchored source-free packet and replay its diagnostics."""
import argparse,hashlib,json,subprocess,sys
from pathlib import Path

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--manifest-sha256',required=True)
    args=ap.parse_args()
    root=Path(__file__).resolve().parent
    data=(root/'MANIFEST.json').read_bytes()
    if hashlib.sha256(data).hexdigest()!=args.manifest_sha256:
        raise RuntimeError('External manifest anchor mismatch')
    m=json.loads(data)
    expected=set(m['files'])|{'MANIFEST.json'}
    if any(not p.is_file() or p.is_symlink() for p in root.iterdir()):
        raise RuntimeError('Unexpected directory or symlink in flat packet')
    actual={p.name for p in root.iterdir()}
    if actual!=expected:raise RuntimeError('Packet inventory mismatch')
    for name,row in m['files'].items():
        if Path(name).name!=name:raise RuntimeError('Invalid inventory path')
        p=root/name
        if p.is_symlink():raise RuntimeError('Symlink not allowed')
        b=p.read_bytes()
        if len(b)!=row['bytes'] or hashlib.sha256(b).hexdigest()!=row['sha256']:
            raise RuntimeError('Payload mismatch: '+name)
    expected_output=(root/'CHECK_RESULTS.json').read_bytes()
    for options in ([],['-O']):
        out=subprocess.check_output([sys.executable]+options+[str(root/'check_exact.py')],cwd=root)
        if out!=expected_output:raise RuntimeError('Diagnostic output mismatch: '+str(options))
    print(json.dumps({'result':'PASS_ANCHORED_PACKET_AND_REPLAYS','files':len(m['files']),
                      'normal_and_optimized_outputs_match':True,'manifest_sha256':args.manifest_sha256},sort_keys=True,indent=2))
if __name__=='__main__':main()
