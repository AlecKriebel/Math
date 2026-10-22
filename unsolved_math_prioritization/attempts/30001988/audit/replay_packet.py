#!/usr/bin/env python3
"""Read-only replay and adversarial inventory checks in disposable copies."""
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
EXPECTED='767185ee51afce74a4227eb090aa4e896503ddbf186cc236e5deedadb4b51ab2'

def run(root,script):
    p=subprocess.run([sys.executable,'-B',str(root/script)],cwd=root,capture_output=True,text=True)
    return p

def require(test,msg):
    if not test: raise RuntimeError(msg)

def main():
    packet=Path(sys.argv[1]).resolve() if len(sys.argv)>1 else Path(__file__).resolve().parent.parent/'packet'
    before={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in packet.iterdir() if p.is_file()}
    require(before['SHA256SUMS.json']==EXPECTED,'wrong frozen packet')
    outputs={}
    for script in ('verify_manifest.py','verify.py'):
        p=run(packet,script)
        require(p.returncode==0,p.stderr)
        outputs[script]=json.loads(p.stdout)
    require(outputs['verify.py']==json.loads((packet/'CONTROL_RESULTS.json').read_text()),'recorded controls disagree')
    mutations={}
    for kind in ('altered_bytes','missing_file','extra_file'):
        with tempfile.TemporaryDirectory(prefix='rank654-audit-') as td:
            q=Path(td)/'packet'; shutil.copytree(packet,q)
            if kind=='altered_bytes':
                with (q/'PROOF.md').open('ab') as f:f.write(b'\nAudit mutation.\n')
            elif kind=='missing_file':(q/'README.md').unlink()
            else:(q/'UNEXPECTED.txt').write_text('audit test only\n')
            p=run(q,'verify_manifest.py')
            require(p.returncode!=0,'manifest accepted '+kind)
            mutations[kind]='rejected'
    after={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in packet.iterdir() if p.is_file()}
    require(before==after,'original packet changed')
    print(json.dumps({'passed':True,'frozen_manifest_sha256':EXPECTED,
                      'packet_scripts':outputs,'recorded_controls_match_replay':True,
                      'manifest_mutation_tests':mutations,'original_packet_unchanged':True},indent=2))
if __name__=='__main__':main()
