#!/usr/bin/env python3
"""Explicit once-reviewed administrative payload reseal, outside delivered CLI."""
import hashlib, json, zipfile, datetime
from pathlib import Path
W=Path(__file__).resolve().parent
A=W.parents[1]; D=A/'preprint_v1_0'; K=D/'verification_kit'
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def dump(p,d): p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
def main():
    if (W/'SEAL.json').exists(): raise RuntimeError('Sealed stage cannot be rewritten')
    for p in [D/'README.md',K/'README.md']:
        s=p.read_text().replace('Real compilation and all seven page views were last checked in complete whole01 on unchanged TeX/PDF; this bounded repair performs no new compilation or visual review.', 'At repair01, complete whole01 had checked actual compilation and all seven unchanged pages; that repair made no new compilation or visual-review claim.')
        s=s.replace('Real compilation and all seven page views were last checked by complete whole01 on the unchanged paper. This bounded interface repair makes no new compilation or page-view claim;', 'At repair01, complete whole01 had checked compilation and all seven unchanged pages. That interface repair made no new compilation or page-view claim;')
        s=s.replace('`FINAL_VERIFICATION.json` records checks and current review boundaries.', '`FINAL_VERIFICATION.json` records the original preparation checks and its dated review boundary.')
        p.write_text(s)
    names=sorted(p.relative_to(K).as_posix() for p in K.rglob('*') if p.is_file())
    dump(K/'ALLOWLIST.json',{'schema_version':1,'scope':'Explicit sorted current payload, including MANIFEST.json; historical archives already present are captured history. No current archive, binding or PDF is included.','members':names})
    dump(K/'MANIFEST.json',{'schema_version':1,'self_hash_scope':'All allowlisted members except MANIFEST.json','files':[{'path':n,'bytes':(K/n).stat().st_size,'sha256':sha(K/n)} for n in names if n!='MANIFEST.json']})
    zpath=D/'verification_kit.zip'
    with zpath.open('wb') as f:
        with zipfile.ZipFile(f,'w',compression=zipfile.ZIP_STORED) as z:
            for n in names:
                i=zipfile.ZipInfo('verification_kit/'+n,(2026,10,14,0,0,0)); i.create_system=3; i.external_attr=0o100644<<16; i.compress_type=zipfile.ZIP_STORED; i.flag_bits=0
                z.writestr(i,(K/n).read_bytes())
    binding=json.loads((W/'before/preprint_v1_0/EXTERNAL_BINDING.json').read_text())
    binding['as_of_utc']=datetime.datetime.now(datetime.timezone.utc).isoformat()
    binding['scope']='External noncircular terminal administrative binding, pending separate ROOT integrity adoption. Prior bindings remain exact captured history; no publication or human refereeing is certified.'
    binding['manifest_sha256']=sha(K/'MANIFEST.json')
    binding['archive']={'filename':zpath.name,'bytes':zpath.stat().st_size,'sha256':sha(zpath)}
    binding['external_files']=[{'filename':n,'bytes':(D/n).stat().st_size,'sha256':sha(D/n)} for n in ['CURRENT_STATUS_REPAIR01.json','README.md','TERMINAL_ADMIN_STAGE.json','deposit_metadata.json','metadata.json','preprint.tex','research_metadata.json']]
    dump(D/'EXTERNAL_BINDING.json',binding)
    dump(W/'ARCHIVE_BUILD.json',{'status':'PASS','archive':binding['archive'],'members':len(names),'hashed_payloads':len(names)-1,'builder_scope':'Explicit administrative reseal; delivered build_archive.py verifies existing pins and never reseals.'})
    print(json.dumps(json.loads((W/'ARCHIVE_BUILD.json').read_text()),indent=2))
if __name__=='__main__':main()
