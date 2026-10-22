#!/usr/bin/env python3
"""Final read-only complete frozen candidate authentication.
Usage: python -I -S -B final_authentication.py CANDIDATE REVIEW
"""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,stat,sys
def pin(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def require(ok,why):
    if not ok:raise ValueError(why)
def main():
    C=Path(sys.argv[1]);R=Path(sys.argv[2]);A=C.parent.parent;rows=[]
    for p in sorted(C.rglob('*')):
        if p.is_dir():continue
        s=p.lstat();require(stat.S_ISREG(s.st_mode) and stat.S_IMODE(s.st_mode)==0o644,'regular0644')
        rows.append({'path':p.relative_to(C).as_posix(),'git_mode':'100644',**pin(p.read_bytes())})
    frozen=json.loads((A/'FROZEN_CANDIDATE_CORE.json').read_bytes());h=hashlib.sha256(json.dumps(rows,sort_keys=True,separators=(',',':')).encode()).hexdigest()
    require(rows==frozen['files'] and h=='c06bf8dfd12c840d0f4af7af32ef6253de1c9f8d3b47f7a0618dedd7fd17ed2b','all253 exact frozen rows')
    for row in json.loads((A/'SOURCE_MANIFEST.json').read_bytes())['files']:
        require(pin((A/'source'/row['path']).read_bytes())=={k:row[k] for k in ['bytes','sha256']},'original source remains unchanged')
    hist=C/'verification/history/note_author_01';manifest=json.loads((hist/'SAFE_MANIFEST.json').read_bytes())
    for row in manifest['files']:require(pin((hist/row['path']).read_bytes())=={k:row[k] for k in ['bytes','sha256']},'author history safe envelope')
    require((C/'post-lie-note.pdf').read_bytes()==(A/'private_pdf_build/note.pdf').read_bytes(),'actual rendered PDF binding')
    renders=json.loads((C/'verification/root_evidence/PDF_RENDER_RECEIPT.json').read_bytes())
    for row in renders['pages']:require(pin((A/'private_pdf_build'/row['name']).read_bytes())=={k:row[k] for k in ['bytes','sha256']},'render image unchanged')
    require(pin((R/'private_tmp/pdf-text.stdout.bin').read_bytes())==renders['extracted_text'],'independent actual PDF text binding')
    result={'utc':datetime.now(timezone.utc).isoformat(),'status':'PASS','core_files':len(rows),'core_sha256':h,'all_regular_0644':True,'all253_identical_to_external_freeze':True,'all18_original_sources_unchanged':True,'candidate_mutation_detected':False,'history_snapshot_manifest_rows_authenticated':len(manifest['files']),'actual_pdf_equals_render_input':True,'actual_pdf_extraction_matches_render_text':True,'all4_render_image_pins_unchanged':True}
    (R/'AUTHENTICATION_FINAL.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n');print(json.dumps(result,sort_keys=True))
if __name__=='__main__':main()
