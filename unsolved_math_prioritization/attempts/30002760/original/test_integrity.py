#!/usr/bin/env python3
"""All byte, allowlist and schema mutations must fail under all interpreter modes."""
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

ROOT=Path(__file__).resolve().parent

def need(ok,label):
    if not ok:
        raise ValueError(label)

def main():
    cases=['changed_bytes','missing_file','extra_file','bad_size','bad_hash','directory','symlink','duplicate_manifest_key']
    passed=0
    positive=0
    expected_errors={'changed_bytes':'Byte count mismatch','missing_file':'Manifest allowlist mismatch','extra_file':'Manifest allowlist mismatch','bad_size':'Byte count mismatch','bad_hash':'Digest mismatch','directory':'Unexpected directory or symlink','symlink':'Unexpected directory or symlink','duplicate_manifest_key':'Duplicate JSON key'}
    for mode in [[],['-O'],['-OO']]:
        baseline=subprocess.run([sys.executable,*mode,str(ROOT/'verify_packet.py'),'--integrity-only'],capture_output=True,text=True)
        need(baseline.returncode==0 and 'PASS_INTEGRITY_ONLY' in baseline.stdout,'Integrity baseline failed: '+repr(mode)+' '+baseline.stderr)
        positive+=1
        for name in cases:
            with tempfile.TemporaryDirectory(prefix='transport_integrity_') as td:
                dst=Path(td)/'packet'
                shutil.copytree(ROOT,dst)
                manifest=dst/'FROZEN_MANIFEST.json'
                if name=='changed_bytes':
                    p=dst/'TURN_1.md';p.write_bytes(p.read_bytes()+b'X')
                elif name=='missing_file':
                    (dst/'TURN_2.md').unlink()
                elif name=='extra_file':
                    (dst/'UNEXPECTED.md').write_text('unexpected')
                elif name in {'bad_size','bad_hash'}:
                    obj=json.loads(manifest.read_text())
                    if name=='bad_size':
                        obj['files']['TURN_3.md']['bytes']+=1
                    else:
                        obj['files']['TURN_3.md']['sha256']='0'*64
                    manifest.write_text(json.dumps(obj))
                elif name=='directory':
                    (dst/'UNEXPECTED').mkdir()
                elif name=='symlink':
                    (dst/'TURN_4.md').unlink();(dst/'TURN_4.md').symlink_to('TURN_3.md')
                elif name=='duplicate_manifest_key':
                    text=manifest.read_text().rstrip()
                    manifest.write_text(text[:-1]+',"schema":"sha256-byte-manifest-v1"}')
                result=subprocess.run([sys.executable,*mode,str(dst/'verify_packet.py'),'--integrity-only'],capture_output=True,text=True)
                need(result.returncode!=0 and expected_errors[name] in result.stderr,'Integrity mutation accepted or failed for wrong reason: '+name+' '+repr(mode))
                passed+=1
    print(json.dumps({'status':'PASS_INTEGRITY_NEGATIVES','rejected_mutations':passed,'positive_replays':positive,'cases':cases,'modes':['normal','-O','-OO'],'scope':'Frozen byte/schema checks; does not authenticate a maliciously rewritten manifest.'},indent=2,sort_keys=True))

if __name__=='__main__':
    try:
        main()
    except Exception as exc:
        print(str(exc),file=sys.stderr)
        sys.exit(1)
