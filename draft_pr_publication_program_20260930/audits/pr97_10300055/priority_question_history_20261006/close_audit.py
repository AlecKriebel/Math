#!/usr/bin/env python3
"""Close this bounded audit with source-integrity verification and a SHA256 manifest."""
from pathlib import Path
import datetime, hashlib, json, os
root=Path(__file__).resolve().parent
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
reg=json.loads((root/'SOURCE_REGISTER.json').read_text())
errors=[]
for item in reg['borrowed_read_only_inputs']:
    p=Path(item['path'])
    if not p.is_file() or p.stat().st_size!=item['bytes'] or sha(p)!=item['sha256']:
        errors.append('Borrowed input changed: '+str(p))
for source in reg['retrieved_primary_sources']:
    for key in ['file_pin','text_pin']:
        if key in source:
            x=source[key];p=Path(x['path'])
            if not p.is_file() or p.stat().st_size!=x['bytes'] or sha(p)!=x['sha256']:
                errors.append('Retrieved source integrity mismatch: '+str(p))
    r=source['retrieval']
    if r.get('kind')=='pdf':
        if Path(r['destination']).read_bytes()[:4]!=b'%PDF':errors.append('Bad PDF')
        if r.get('text_extraction',{}).get('exit')!=0:errors.append('Failed text extraction')
v=json.loads((root/'VERDICT.json').read_text())
candidate=[x for x in reg['borrowed_read_only_inputs'] if x['path'].endswith('/repaired_verification_candidate_v1/CANDIDATE.md')][0]
if v['candidate_sha256']!=candidate['sha256']:errors.append('Candidate pin differs in verdict')
verification={'UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'actual_operator_pid':os.getpid(),'borrowed_input_count':len(reg['borrowed_read_only_inputs']),'successful_retrieval_count':len(reg['retrieved_primary_sources']),'candidate_sha256':candidate['sha256'],'errors':errors,'passed':not errors,'meaning':'Artifact/source-integrity checks only, not a mathematical or historical novelty proof.'}
(root/'CLOSURE_CHECK.json').write_text(json.dumps(verification,indent=2)+'\n')
if errors:raise SystemExit(json.dumps(verification))
visual={'source_pdf':str(root.parent/'primary_source_cache_20261005/calegari2002.pdf'),'source_pdf_sha256':sha(root.parent/'primary_source_cache_20261005/calegari2002.pdf'),'printed_page':29,'physical_pdf_page':29,'render_argv':['/opt/homebrew/bin/pdftoppm','-f','29','-l','29','-r','85','-png','-singlefile','../primary_source_cache_20261005/calegari2002.pdf','calegari2002_page29'],'render_exec_chunk_id':'cc09b0','render_exit_code':0,'render_process_pid':'not captured; no PID fabricated','image':'calegari2002_page29.png','image_sha256':sha(root/'calegari2002_page29.png'),'visual_inspection':'Tool view_image used and page actually inspected; question labels, inherited hypotheses and contact-tightness wording verified.','image_file_mtime_UTC':datetime.datetime.fromtimestamp((root/'calegari2002_page29.png').stat().st_mtime,datetime.timezone.utc).isoformat()}
(root/'PAGE_VISUAL_CHECK.json').write_text(json.dumps(visual,indent=2)+'\n')
manifest_path=root/'CLOSED_MANIFEST.json'
entries=[]
for p in sorted(root.rglob('*')):
    if p==manifest_path:continue
    if p.is_symlink():raise SystemExit('Unexpected symlink '+str(p))
    if p.is_file():entries.append({'path':str(p.relative_to(root)),'bytes':p.stat().st_size,'sha256':sha(p)})
manifest={'schema':'closed-sha256-manifest-v1','closed_UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'scope':'Every regular file recursively in this history-audit folder except CLOSED_MANIFEST.json itself; its own SHA256 is reported externally. Borrowed inputs separately pinned below.','file_count':len(entries),'entries':entries,'borrowed_read_only_inputs':reg['borrowed_read_only_inputs'],'candidate_sha256':candidate['sha256'],'authority':'Research evidence only; no service or publication authority.'}
manifest_path.write_text(json.dumps(manifest,indent=2)+'\n')
for x in entries:
    p=root/x['path']
    if p.stat().st_size!=x['bytes'] or sha(p)!=x['sha256']:raise SystemExit('Closure mismatch')
print(json.dumps({'closed':True,'file_count':len(entries),'manifest_sha256':sha(manifest_path),'report_sha256':sha(root/'REPORT.md'),'verdict_sha256':sha(root/'VERDICT.json'),'candidate_sha256':candidate['sha256'],'closure_check':verification}))

