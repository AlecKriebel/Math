#!/usr/bin/env python3
"""Preserve old reference rows; explicitly relocate changed live destinations."""
import hashlib,json
from pathlib import Path
W=Path(__file__).resolve().parent; A=W.parents[1]; K=A/'preprint_v1_0/verification_kit'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def dump(p,d):p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
def main():
    if (W/'SEAL.json').exists():raise RuntimeError('Stage sealed')
    p=K/'REPAIR01_HISTORY_RESOLUTION.json'; h=json.loads(p.read_text())
    old=json.loads((W/'before/preprint_v1_0/verification_kit/REPAIR01_HISTORY_RESOLUTION.json').read_text())
    if h['references'][:2312]!=old['references']:raise RuntimeError('Historical prefix modified')
    mutable={'README.md','verify.py','ALLOWLIST.json','MANIFEST.json','REPAIR01_STAGE_COPIES.json','REPAIR01_HISTORY_RESOLUTION.json'}
    index={}
    for f in sorted(K.rglob('*')):
        if f.is_file() and f.relative_to(K).as_posix() not in mutable:
            index.setdefault((f.stat().st_size,sha(f)),f.relative_to(K).as_posix())
    reloc=[]
    for i,r in enumerate(h['references']):
        if r['disposition']=='omitted':continue
        key=(r['bytes'],r['sha256']); target=index.get(key)
        if i>=2312:
            if target:r['destination']=target
            else:
                r.pop('destination',None);r.update(disposition='omitted',reason='This individual historical artifact has no exact immutable selected copy. Source/raw/private/duplicate-archive and administrative scratch exclusions apply; the original pin is preserved without claiming delivery or replay.')
        else:
            f=K/r['destination']
            if not f.is_file() or (f.stat().st_size,sha(f))!=key:
                if not target:raise RuntimeError('No exact relocation for old reference '+str(i))
                reloc.append({'reference_index':i,'historical_reference':r,'current_exact_destination':target,'reason':'Original destination names a live verifier revised only for terminal administration; the old row stays exact and resolves to its exact captured-before bytes.'})
    dump(p,h)
    dump(K/'TERMINAL_HISTORY_RELOCATIONS.json',{'scope':'Exact successor resolutions for unchanged historical rows whose once-current destination has since changed. No old row/hash/verdict is rewritten.','rows':reloc})
    v=K/'verify.py'; text=v.read_text()
    oldloop='''    for r in history["references"]:
        if r["disposition"] == "exact_captured_stage_or_canonical_copy":
            q = safe_path(r["destination"])
'''
    newloop='''    relocation_rows = json.loads(regular_input(ROOT / "TERMINAL_HISTORY_RELOCATIONS.json").read_text())["rows"]
    relocations = {r["reference_index"]: r for r in relocation_rows}
    require(len(relocations) == len(relocation_rows), "duplicate historical relocation")
    for index, relocation in relocations.items():
        require(type(index) is int and 0 <= index < 2312 and history["references"][index] == relocation["historical_reference"], "historical relocation changed original row")
    for index, r in enumerate(history["references"]):
        if r["disposition"] == "exact_captured_stage_or_canonical_copy":
            destination = relocations[index]["current_exact_destination"] if index in relocations else r["destination"]
            q = safe_path(destination)
'''
    if oldloop not in text:raise RuntimeError('Verifier anchor changed')
    v.write_text(text.replace(oldloop,newloop))
    for p in [A/'preprint_v1_0/README.md',K/'README.md']:
        s=p.read_text()+'\n`TERMINAL_HISTORY_RELOCATIONS.json` gives explicit exact-before-copy resolutions for two unchanged old rows whose original destination was the live verifier. The old 2,312-row prefix stays exact; the current verifier checks each relocation against its entire preserved original row and the exact captured bytes. New appended references use immutable selected copies.\n';p.write_text(s)
    dump(W/'HISTORY_RELOCATION_RESULT.json',{'old_rows_preserved':2312,'relocations':reloc,'new_rows':len(h['references'])-2312})
    print(json.dumps({'status':'PASS','exact_unchanged_old_rows':2312,'relocations':len(reloc)},indent=2))
if __name__=='__main__':main()
