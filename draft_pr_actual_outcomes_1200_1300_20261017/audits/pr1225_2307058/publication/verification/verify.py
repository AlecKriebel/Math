#!/usr/bin/env python3
"""Authenticate authored archive bindings; no numeric proof certificate claimed."""
from pathlib import Path,PurePosixPath
import hashlib,json
ROOT=Path(__file__).resolve().parent
def need(c,m):
    if not c:raise ValueError(m)
def check_binding(p,e):
    b=p.read_bytes();need(len(b)==e['bytes'],'size '+str(p));need(hashlib.sha256(b).hexdigest()==e['sha256'],'digest '+str(p))
def safe(raw):
    need(isinstance(raw,str) and bool(raw),'invalid member');rel=PurePosixPath(raw)
    need(not rel.is_absolute() and '..' not in rel.parts and str(rel)==raw,'unsafe member');return raw
def authenticate_nested_manifests(root):
    """Only authored content manifests, not omitted-source receipt inventories."""
    checked=[];names={'MANIFEST.json','FREEZE_MANIFEST.json','CROSS_MANIFEST.json','CROSS_FREEZE_MANIFEST.json'}
    for path in sorted(p for p in root.rglob('*.json') if p.name in names and p!=root/'MANIFEST.json'):
        obj=json.loads(path.read_text());need(('entries' in obj)!=('files' in obj),'ambiguous nested schema '+str(path));entries=obj.get('entries',obj.get('files'))
        need(isinstance(entries,list) and len(entries)>0,'invalid nested manifest')
        base=path.parent
        if path.relative_to(root).as_posix()=='priority/independent/evidence/MANIFEST.json':base=path.parent.parent
        seen=set()
        for entry in entries:
            raw=safe(entry.get('file',entry.get('path')));need(raw not in seen,'duplicate nested member');seen.add(raw);check_binding(base/raw,entry)
        checked.append({'path':path.relative_to(root).as_posix(),'base':base.relative_to(root).as_posix(),'entries':len(entries)})
    return checked
def main():
    manifest=json.loads((ROOT/'MANIFEST.json').read_text());seen=set()
    for e in manifest['files']:
        raw=safe(e['path']);need(raw not in seen,'duplicate root member');seen.add(raw);check_binding(ROOT/raw,e)
    actual={p.relative_to(ROOT).as_posix() for p in ROOT.rglob('*') if p.is_file() and '__pycache__' not in p.parts}
    need(actual==seen|{'MANIFEST.json'},'unlisted/missing archive member')
    nested=authenticate_nested_manifests(ROOT)
    original=json.loads((ROOT/'provenance/SUBMITTED_SNAPSHOT.json').read_text())
    for e in original['files']:
        b=(ROOT/'original_submitted'/Path(e['path']).name).read_bytes();need(len(b)==e.get('bytes',e.get('size')),'submitted size');need(hashlib.sha256(b).hexdigest()==e['sha256'],'submitted digest');need(hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==e['blob'],'submitted Git object identity')
    required={'original_submitted/MANIFEST.json','current_edition/MANIFEST.json','reviews/analytic_adversary/FREEZE_MANIFEST.json','reviews/source_question_family/MANIFEST.json','reviews/riesz_route_adversary/FREEZE_MANIFEST.json','priority/independent/evidence/MANIFEST.json','priority/independent/CROSS_MANIFEST.json','priority/adversary/FREEZE_MANIFEST.json','priority/adversary/CROSS_FREEZE_MANIFEST.json','priority/corollary_verifier/FREEZE_MANIFEST.json'}
    need({x['path'] for x in nested}==required,'required authored freeze inventory differs')
    print(json.dumps({'status':'PASS','authenticated_members':len(seen),'submitted_files':len(original['files']),'all_nested_manifests':nested,'limits':'Verifies byte bindings and original Git identities only. Mathematical conclusions and independence/priority claims rest on written arguments and documented acts. Omitted third-party source bodies and unavailable historical execution bodies are not reauthenticated; their inventories are receipts only.'},indent=2))
if __name__=='__main__':main()
