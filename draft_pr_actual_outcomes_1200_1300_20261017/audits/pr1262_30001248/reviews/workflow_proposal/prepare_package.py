#!/usr/bin/env python3
"""Prepare only explicit current eight-file edition after exact actual gates."""
from pathlib import Path
import json, runpy, shutil
ROOT=Path(__file__).resolve().parent
AUDIT=ROOT.parent
EDITION=AUDIT/'current_edition'
PACKAGE=ROOT/'verification'

def checker():
    path=ROOT/'verification/verify.py'
    if not path.exists():path=ROOT/'verification_verify.py'
    return runpy.run_path(str(path))
def save(path,obj):path.write_text(json.dumps(obj,indent=2)+'\n')
def load_context():return checker()['load_context'](AUDIT,ROOT)

def main():
    v=checker();context=load_context()
    snapshot=json.loads((AUDIT/'SUBMITTED_SNAPSHOT.json').read_text());v['authenticate_snapshot'](AUDIT/'submitted',snapshot)
    # Authenticate all inputs before any package/edition write. No historical
    # prose or metadata is mined as a fallback for missing current records.
    v['need'](not EDITION.is_symlink() and not PACKAGE.is_symlink(),'unsafe edition/package directory')
    EDITION.mkdir(exist_ok=True);PACKAGE.mkdir(exist_ok=True)
    v['need'](not any(p.name not in v['NAMES'] for p in EDITION.iterdir()),'unexpected current edition child')
    for name,text in context['edition_text'].items():(EDITION/name).write_text(text)
    for name,record in context['structured_records'].items():save(EDITION/name,record)
    save(EDITION/'MANIFEST.json',{'schema':'triangle-modular-threshold-current-edition-manifest-v1','problem_id':30001248,'members':sorted(v['NAMES']),'self_hash_excluded':'MANIFEST.json','entries':[{'file':name,**v['binding'](EDITION/name)} for name in sorted(v['NAMES']-{'MANIFEST.json'})],'novelty_certified':False,'scope':'Explicit current mathematical edition; independent acceptance/priority records required, no preparation clearance implied.'})
    v['authenticate_edition'](EDITION)
    verifier=(PACKAGE/'verify.py').read_bytes()
    for child in PACKAGE.iterdir():
        if child.name=='verify.py':continue
        v['need'](not child.is_symlink(),'unexpected package symlink')
        if child.is_dir():shutil.rmtree(child)
        else:child.unlink()
    def copy(source,raw):
        dest=v['member'](PACKAGE,raw);dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(source,dest)
    for name in sorted(v['NAMES']):copy(EDITION/name,'current_edition/'+name);copy(AUDIT/'submitted'/name,'original_submitted/'+name)
    for name in ['CURRENT_PR1262_CONTEXT.json','SUBMITTED_SNAPSHOT.json','PRIORITY_ADJUDICATION.json','MATH_GATE.json']:copy(AUDIT/name,'provenance/'+name)
    for name in ['COMPILE_RECEIPT.json','LAYOUT_VERIFICATION.json']:copy(ROOT/name,'provenance/'+name)
    copy(ROOT/'manuscript/main.tex','manuscript/main.tex')
    for entry in context['portable_files']:copy(v['member'](AUDIT,entry['path']),entry['path'])
    v['need']((PACKAGE/'verify.py').read_bytes()==verifier,'portable verifier changed')
    print(json.dumps({'current_edition_files':8,'original_submitted_files':8,'portable_files':sum(p.is_file() for p in PACKAGE.rglob('*')),'scope':'Explicit context and allowlisted authored evidence/receipts; no source inventory is interpreted as retained third-party bodies.'}))
if __name__=='__main__':main()
