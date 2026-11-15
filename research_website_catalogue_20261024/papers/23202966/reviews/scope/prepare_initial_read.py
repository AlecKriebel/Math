#!/usr/bin/env python3
"""Custody copying and fresh Poppler derivatives only; no scientific programme execution."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,shutil,subprocess
A=Path(__file__).resolve().parent;S=A.parents[1]/'sources'
if (A/'SOURCE_INPUT_MANIFEST.json').exists():raise RuntimeError('initial acquisition already prepared')
(A/'.gitignore').write_text('inputs/\nrasters/\nprimary/\nraw/\n__pycache__/\n')
for n in ['inputs','rasters','primary','raw']:(A/n).mkdir()
def now():return datetime.now(timezone.utc).isoformat()
def pin(q):
 b=q.read_bytes();return {'path':str(q),'bytes':len(b),'SHA256':hashlib.sha256(b).hexdigest()}
files=[]
for q in sorted(S.rglob('*')):
 if q.is_symlink():raise ValueError('source symlink')
 if q.is_file():files.append(pin(q))
if len(files)!=79:raise ValueError('source extent')
m=json.loads((S/'SOURCE_READY_MANIFEST.json').read_bytes());seal=json.loads((S/'SOURCE_READY_SEAL.json').read_bytes())
if pin(S/'SOURCE_READY_MANIFEST.json')['SHA256']!=seal['MANIFEST_SHA256']:raise ValueError('source manifest seal')
(A/'SOURCE_INPUT_MANIFEST.json').write_text(json.dumps({'UTC':now(),'complete_source_files':files,'exact_complete_source_directories':[str(q.relative_to(S)) for q in sorted(S.rglob('*')) if q.is_dir()],'source_ready_SHA256':'86264fb9c694c35abcdcae60fd15aaa617627204ceb8e0cd95b09947e4d893dc','source_seal_SHA256':'9a87a851ebab2735927edb66d350168fdb9d20e738ab6a9bc2e85b7f3a93ed63','root135_gate':'CLOSED','prior_record135_scientific_exposure':None},indent=2)+'\n')
(A/'RESEARCH_LOG.md').write_text('# Scope review log — row135 /23202966\n\n- '+now()+' —0%: New scope namespace confirmed absent before preparation. Initial mkdir attempt stopped before any file creation because reviews/ ancestor was absent; corrected by creating only the authorized new scope path. Root comparison gate CLOSED. Only source custody metadata has been read; no prior23202966 scientific opinion exposure known. Prior roles involve unrelated acquisitions/editorial/integration. Source historical unread/null/version flags remain unchanged.\n')
ready=json.loads((S/'SOURCE_READY.json').read_bytes())
for n in ['SOURCE_READY.json','SOURCE_READY_SEAL.json','SOURCE_READY_MANIFEST.json','MANUSCRIPT_CUSTODY.json','ARCHIVE_CUSTODY.json','NATIVE_SCHEMA_TYPES.json','ALL_TRANSPORT_RECEIPTS.json']:(A/'inputs'/n).write_bytes((S/n).read_bytes())
pdf=Path(ready['selected_actual_PDF']['path']);tex=Path(ready['controlling_TeX']['extracted_path']);(A/'inputs/published-manuscript.tex').write_bytes(tex.read_bytes())
for n in ['pdftotext','pdftoppm','pdfinfo']:
 if not shutil.which(n):raise ValueError('existing Poppler missing '+n)
commands=[['pdftotext','-layout',str(pdf),str(A/'published-pdf-text.txt')],['pdftoppm','-r','110','-f','1','-l','6','-png',str(pdf),str(A/'rasters/page')],['pdfinfo',str(pdf)]]
receipts=[]
for cmd in commands:
 start=now();r=subprocess.run(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
 receipts.append({'command':cmd,'UTC_started':start,'UTC_completed':now(),'exit_code':r.returncode,'stdout':r.stdout.decode(),'stderr':r.stderr.decode()})
 if r.returncode:raise ValueError('Poppler failed')
(A/'MANUSCRIPT_DERIVATION_RECEIPTS.json').write_text(json.dumps({'actual_published_PDF':pin(pdf),'actual_controlling_TeX':pin(tex),'ordinary_poppler_only_not_scientific_programmes':True,'actual_commands':receipts,'fresh_own_individual_rasters':[pin(q) for q in sorted((A/'rasters').glob('*.png'))]},indent=2)+'\n')
print(json.dumps({'source_files':len(files),'native_asset_order':[e['original_api_file_object']['key'] for e in ready['all_native_assets_in_original_order']],'fresh_rasters':len(list((A/'rasters').glob('*.png'))),'complete_TeX_lines':len(tex.read_bytes().splitlines()),'scientific_execution':False,'foreign_science_exposure':False}))
