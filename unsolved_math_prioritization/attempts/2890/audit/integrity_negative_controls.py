#!/usr/bin/env python3
"""Mutation tests use temporary copies only; the original freeze stays untouched."""
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

here=Path(__file__).resolve().parent
author=Path(sys.argv[1]).resolve() if len(sys.argv)>1 else here.parent/'author'
def run(script, source):
    return subprocess.run([sys.executable,'-B',str(script),str(source)],capture_output=True)
baseline=run(here/'verify_audit.py',author)
assert baseline.returncode==0
assert baseline.stdout==(here/'VERIFICATION_RESULTS.json').read_bytes()
mutations=[
 ('changed_author_proof','author','PROOF.md','append'),
 ('changed_author_manifest','author','AUTHOR_MANIFEST.json','append'),
 ('unexpected_author_file','author','UNEXPECTED.txt','create'),
 ('missing_author_file','author','README.md','remove'),
 ('changed_author_results','author','CONTROL_RESULTS.json','append'),
 ('changed_independent_results','audit','INDEPENDENT_RESULTS.json','append'),
]
results=[]
with tempfile.TemporaryDirectory(prefix='universal-cork-audit-') as tmp:
    for index,(name,side,filename,operation) in enumerate(mutations):
        root=Path(tmp)/str(index);root.mkdir()
        for source,label in [(author,'author'),(here,'audit')]:
            target=root/label;target.mkdir()
            for item in source.iterdir():
                if item.is_file():shutil.copyfile(item,target/item.name)
        target=root/side/filename
        if operation=='remove':target.unlink()
        elif operation=='create':target.write_bytes(b'unexpected\n')
        else:target.write_bytes(target.read_bytes()+b'\n')
        observed=run(root/'audit/verify_audit.py',root/'author')
        assert observed.returncode!=0,name
        results.append({'mutation':name,'rejected':True})
after=run(here/'verify_audit.py',author)
assert after.returncode==0 and after.stdout==baseline.stdout
print(json.dumps({'status':'PASS','positive_baseline_passed':True,
 'mutation_count':len(results),'mutations':results,
 'original_freeze_unchanged':True,'all_mutations_confined_to_temporary_copies':True},indent=2,sort_keys=True))
