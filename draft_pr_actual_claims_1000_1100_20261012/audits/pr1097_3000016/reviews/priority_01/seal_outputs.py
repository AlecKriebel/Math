#!/usr/bin/env python3
"""Seal existing public audit outputs after reading and verification; no sources copied."""
from pathlib import Path
import datetime,hashlib,json
ROOT=Path(__file__).resolve().parent
def pin(path):
    b=path.read_bytes()
    return {'path':str(path.relative_to(ROOT)),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def write(name,obj): (ROOT/name).write_text(json.dumps(obj,indent=2,ensure_ascii=False)+'\n')
def main():
    stamp=datetime.datetime.now(datetime.timezone.utc).isoformat()
    if json.loads((ROOT/'CHECK_NORMAL.json').read_text()) != json.loads((ROOT/'CHECK_OPTIMIZED.json').read_text()):
        raise RuntimeError('complete result mismatch')
    rows=[pin(p) for p in sorted(ROOT.rglob('*')) if p.is_file() and p.relative_to(ROOT).parts[0] not in ('sources','scratch','__pycache__') and p.name not in ('OUTPUT_PINS.json','FINAL_SEAL.json')]
    write('OUTPUT_PINS.json',{'utc':stamp,'scope':'All public review outputs except this manifest and separate terminal seal; primary PDFs/text/pixels remain private or cleaned captured-stage derivatives.','records':rows})
    manifest=pin(ROOT/'OUTPUT_PINS.json')
    write('FINAL_SEAL.json',{'utc':stamp,'status':'PRIORITY_AUDIT_TERMINAL_QUALIFIED','head_oid':'ad7b0eeef847da65afe1b691705cfa6e832e8201','manifest':manifest,'sealed_public_output_count':len(rows),'input_pins':pin(ROOT/'INPUT_PINS.json'),'input_preservation':pin(ROOT/'INPUT_PRESERVATION.json'),'report':pin(ROOT/'REPORT.md'),'verdict':pin(ROOT/'VERDICT.json'),'derivations':pin(ROOT/'PRIOR_COMPARISON_DERIVATIONS.md'),'priority':'UNKNOWN','publication_or_merge_ready':False,'qualification':'A completed bounded priority audit with required attribution changes for subsequent preparation, not a novelty guarantee.'})
    # Reopen everything after writing, then independently rehash every record.
    for r in json.loads((ROOT/'OUTPUT_PINS.json').read_text())['records']:
        if pin(ROOT/r['path'])!=r: raise RuntimeError('output pin mismatch '+r['path'])
    print(json.dumps({'status':'SEALED_AND_REOPENED','outputs':len(rows),'manifest':manifest,'terminal_seal':pin(ROOT/'FINAL_SEAL.json')}))
if __name__=='__main__': main()
