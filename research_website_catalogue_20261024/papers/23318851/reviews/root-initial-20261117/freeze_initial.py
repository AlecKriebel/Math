from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, stat
R=Path(__file__).resolve().parent
assert not (R/'INITIAL_SEAL.json').exists()
now=datetime.now(timezone.utc).isoformat()
initial={'UTC':now,'record_id':'23318851','sheet_row':194,'gate':'ORIGINAL_ONLY_COMPLETE','INITIAL_completion_percent':100,'full_review_estimate_percent':45,'personally_read':['Entire185lineoriginalTeX','Entire fresh five-page PDF text','All five freshly rendered native PDF pages individually viewed','Complete original nativeAPI including fullDescription and metadata','Source metadata and actual whole-custody manifest'],'source_files_childdirs':[95,16],'source_preservation':'Whole bytes/modes/hidden/empty/topology exact','prior_exposure':['Original author proof, citations, chronology assertions and author-described supporting audits; original assertions are not independent confirmation'],'support_code_or_packaged_audits_read':0,'primary_literature_read':0,'current_family_mathematical_reports_read':0,'scientific_or_source_program_runs':0,'tooling':'One saved fully read data-acquisition script; pdfinfo, pdftotext, pdftoppm all exit0; each literal child stream preserved','independent_reconstruction':'INDEPENDENT_RECONSTRUCTION.md','final_scientific_verdict':None,'follow_up':None,'publication_authority':False,'next_gate':'Checkpoint root and two families INITIALs, then explicit separate continuation for primary/support/source verification'}
(R/'INITIAL.json').write_text(json.dumps(initial,indent=2)+'\n')
(R/'RESEARCH_LOG.md').write_text('# Research log\n\n'+now+' — Original-only INITIAL complete100%; full scientific review estimate45%. Exact claim, independent proof reconstruction and falsifiable checks recorded before opening support, primary literature or peer mathematical reports. Entire native five-page PDF personally viewed; originalTeX and native metadata read. Source95/16 unchanged. No scientific verdict, code execution or outreach. Next: checkpoint and separate continuation.\n')
rows=[]
for f in [R]+sorted(R.rglob('*')):
    assert not f.is_symlink()
    row={'path':str(f.relative_to(R)),'kind':'directory' if f.is_dir() else 'file','mode':oct(stat.S_IMODE(f.stat().st_mode))}
    if f.is_file(): row.update(bytes=f.stat().st_size,SHA256=hashlib.sha256(f.read_bytes()).hexdigest())
    else: row['empty']=not any(f.iterdir())
    rows.append(row)
manifest={'UTC':now,'root':str(R),'payload':rows,'terminal_controls':[{'path':n,'kind':'file','mode':'0o644'} for n in ['INITIAL_MANIFEST.json','INITIAL_SEAL.json']],'only_recursive_hash_exclusions':['INITIAL_MANIFEST.json','INITIAL_SEAL.json'],'files_including_controls':sum(r['kind']=='file' for r in rows)+2,'childdirs':sum(r['kind']=='directory' for r in rows)-1}
(R/'INITIAL_MANIFEST.json').write_text(json.dumps(manifest,indent=2)+'\n')
seal={'UTC':now,'status':'FROZEN_ORIGINAL_ONLY_INITIAL','manifest_SHA256':hashlib.sha256((R/'INITIAL_MANIFEST.json').read_bytes()).hexdigest(),'INITIAL_SHA256':hashlib.sha256((R/'INITIAL.json').read_bytes()).hexdigest(),'files':manifest['files_including_controls'],'childdirs':manifest['childdirs'],'INITIAL_completion_percent':100,'full_review_estimate_percent':45,'follow_up':None,'verdict':None}
(R/'INITIAL_SEAL.json').write_text(json.dumps(seal,indent=2)+'\n')
print(json.dumps(dict(seal,seal_SHA256=hashlib.sha256((R/'INITIAL_SEAL.json').read_bytes()).hexdigest())))
