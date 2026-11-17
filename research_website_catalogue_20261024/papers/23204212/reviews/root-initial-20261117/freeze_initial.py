from pathlib import Path
from datetime import datetime, timezone
import hashlib,json,stat
R=Path(__file__).resolve().parent
assert not (R/'INITIAL_SEAL.json').exists()
now=datetime.now(timezone.utc).isoformat()
initial={'UTC':now,'record_id':'23204212','sheet_row':192,'gate':'ORIGINAL_ONLY_COMPLETE','INITIAL_completion_percent':100,'full_review_estimate_percent':25,'personally_read':['Entire original main.tex','All four fresh PDF text pages','All four fresh native PDF page pixels separately viewed','Complete native recordAPI and Description','Actual source custody manifest'],'source_files_childdirs':[55,14],'source_preservation':'Whole bytes/modes/hidden/empty/topology exact','prior_exposure':['Original author proof and author-described upstream audit/chronology assertions; not independent confirmation'],'support_code_or_packaged_audits_read':0,'primary_literature_read':0,'current_family_mathematical_reports_read':0,'scientific_or_source_program_runs':0,'data_acquisition':'One saved fully read original data reader, pdfinfo/pdftotext/pdftoppm each exit0; literal child streams retained','independent_reconstruction':'INDEPENDENT_RECONSTRUCTION.md','final_verdict':None,'follow_up':None,'publication_authority':False,'next_gate':'Checkpoint and explicit separate continuation'}
(R/'INITIAL.json').write_text(json.dumps(initial,indent=2)+'\n')
(R/'RESEARCH_LOG.md').write_text('# Research log\n\n'+now+' — Original-only gate100%; full scientific review estimate25%. Entire original manuscript/metadata and four native PDF pages read before support, primary or current-peer reports. Source55/14 exact; independent conditional deduction, boundaries and falsification checks preserved. No scientific run, verdict or contact. Freeze, checkpoint, then separate continuation.\n')
rows=[]
for f in [R]+sorted(R.rglob('*')):
 assert not f.is_symlink()
 e={'path':str(f.relative_to(R)),'kind':'directory' if f.is_dir() else 'file','mode':oct(stat.S_IMODE(f.stat().st_mode))}
 if f.is_file():e.update(bytes=f.stat().st_size,SHA256=hashlib.sha256(f.read_bytes()).hexdigest())
 else:e['empty']=not any(f.iterdir())
 rows.append(e)
manifest={'UTC':now,'root':str(R),'payload':rows,'terminal_controls':[{'path':n,'kind':'file','mode':'0o644'} for n in ['INITIAL_MANIFEST.json','INITIAL_SEAL.json']],'only_recursive_hash_exclusions':['INITIAL_MANIFEST.json','INITIAL_SEAL.json'],'files_including_controls':sum(r['kind']=='file' for r in rows)+2,'childdirs':sum(r['kind']=='directory' for r in rows)-1}
(R/'INITIAL_MANIFEST.json').write_text(json.dumps(manifest,indent=2)+'\n')
seal={'UTC':now,'status':'FROZEN_ORIGINAL_ONLY_INITIAL','manifest_SHA256':hashlib.sha256((R/'INITIAL_MANIFEST.json').read_bytes()).hexdigest(),'INITIAL_SHA256':hashlib.sha256((R/'INITIAL.json').read_bytes()).hexdigest(),'files':manifest['files_including_controls'],'childdirs':manifest['childdirs'],'INITIAL_completion_percent':100,'full_review_estimate_percent':25,'verdict':None,'follow_up':None}
(R/'INITIAL_SEAL.json').write_text(json.dumps(seal,indent=2)+'\n')
print(json.dumps(dict(seal,seal_SHA256=hashlib.sha256((R/'INITIAL_SEAL.json').read_bytes()).hexdigest())))
