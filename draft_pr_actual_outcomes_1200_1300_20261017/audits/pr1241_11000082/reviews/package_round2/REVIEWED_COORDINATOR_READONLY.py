from pathlib import Path
import hashlib,json,runpy,subprocess,sys,zipfile
REPO=Path('/Users/alec/Documents/Math');A=REPO/'draft_pr_actual_outcomes_1200_1300_20261017/audits/pr1241_11000082';P=A/'publication'
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def require(c,m):
 if not c:raise RuntimeError(m)
action=sys.argv[1];require(action in {'stage','inspect','publish','inspect-doi'},'Unsupported action')
g=json.loads((P/'FINAL_REVIEW_GATE.json').read_text());u=runpy.run_path(str(P/'update_pr_publication.py'));u['validate_workflow_gate'](g)
for n,k in [('Johnson_Filtration_Multiplicity_Note_v1.0.pdf','pdf_sha256'),('Johnson_Filtration_Multiplicity_Verification_v1.0.zip','verification_zip_sha256'),('zenodo-deposit.json','metadata_sha256'),('manuscript/main.tex','source_sha256')]:require(digest(P/n)==g[k],'Reviewed release drift '+n)
review_dir=(P/g['latest_review']['verdict']).resolve().parent
freeze_path=review_dir/'INPUT_FREEZE.json'
require(digest(freeze_path)==g['latest_review']['input_freeze_sha256'],'Latest review input-freeze anchor differs')
freeze=json.loads(freeze_path.read_text())
for e in freeze['files']:
 b=(A/e['path']).read_bytes();require(len(b)==e['bytes'] and hashlib.sha256(b).hexdigest()==e['sha256'],'Frozen input drift '+e['path'])
for e in freeze['external_readonly_inputs']:
 b=Path(e['path']).read_bytes();require(len(b)==e['bytes'] and hashlib.sha256(b).hexdigest()==e['sha256'],'Reviewed kit drift')
runpy.run_path(str(P/'build_package.py'))['document_bindings']()
with zipfile.ZipFile(P/'Johnson_Filtration_Multiplicity_Verification_v1.0.zip') as z:
 require(z.read('manuscript/main.tex')==(P/'manuscript/main.tex').read_bytes(),'Reviewed archive source drift')
 for n in ['ACCEPTANCE.json','ACCEPTANCE.md','AUDIT.md','MANIFEST.json','PROOF.md','README.md','SOURCES.json','VERIFICATION.json']:require(z.read('current_edition/'+n)==(A/'current_edition'/n).read_bytes(),'Current edition drift '+n)
if action in {'stage','publish'}:
 snapshot=json.loads((A/'SUBMITTED_SNAPSHOT.json').read_text())
 raw=subprocess.check_output(['gh','pr','view','1241','--repo','AlecKriebel/Math','--json','state,isDraft,headRefOid,headRefName,body'],text=True)
 live=json.loads(raw)
 require(live['state']=='OPEN' and live['isDraft'] is True and live['headRefOid']==snapshot['head'] and live['headRefName']==snapshot['branch'] and hashlib.sha256(live['body'].encode()).hexdigest()==snapshot['body_sha256'],'Live original draft/head/body changed; no deposit mutation')
 remote=subprocess.check_output(['git','ls-remote','origin','refs/heads/'+snapshot['branch']],cwd=REPO,text=True).split()
 require(remote and remote[0]==snapshot['head'],'Live branch changed; no deposit mutation')
 tracker=runpy.run_path(str(P/'append_tracker.py'))
 tabmeta=tracker['call'](['spreadsheets','get'],{'spreadsheetId':tracker['SID'],'fields':'sheets.properties'})
 tab=next(item['properties'] for item in tabmeta['sheets'] if item['properties']['sheetId']==tracker['GID'])
 require(tab['title']=='Math Puzzles','Tracker tab changed; no deposit mutation')
 rows=tracker['call'](['spreadsheets','values','get'],{'spreadsheetId':tracker['SID'],'range':"'Math Puzzles'!A:D",'valueRenderOption':'UNFORMATTED_VALUE'}).get('values',[])
 require(rows and rows[0]==['Original Problem','Solution Chat URL','DOI','Notes'],'Tracker headers changed; no deposit mutation')
 require(not any(any('11000082' in str(cell) or 'AMR-109-0082' in str(cell) for cell in row) for row in rows),'Existing problem row; reconcile before deposit mutation')
 if action=='publish':require(not (P/'PUBLICATION_RECEIPT.json').exists(),'Published receipt already exists; use read-only inspect instead')
cmd=[sys.executable,'-B',str(REPO/'zenodo_deposit_tool/zenodo.py'),'inspect' if action=='inspect-doi' else action,str(P/'zenodo-deposit.json')]
if action=='publish':
 s=json.loads((P/'STAGE_RECEIPT.json').read_text());require(type(s['id']) is int and s['id']>0,'Missing known draft');cmd+=['--confirm-id',str(s['id'])]
if action=='inspect-doi':cmd+=['--check-doi']
r=subprocess.run(cmd,cwd=REPO,capture_output=True,text=True,timeout=180)
local=A/'_local';(local/('zenodo_'+action+'.stdout')).write_text(r.stdout);(local/('zenodo_'+action+'.stderr')).write_text(r.stderr)
if r.returncode:raise RuntimeError('Kit '+action+' failed; known-state read-only reconciliation required. Returncode '+str(r.returncode))
d=json.loads(r.stdout);require(d.get('metadata_normalizations',[])==[],'Nonexact metadata; no further mutation')
name={'stage':'STAGE_RECEIPT.json','inspect':'STAGE_INSPECT.json','publish':'PUBLICATION_RECEIPT.json','inspect-doi':'DOI_INSPECT.json'}[action]
(P/name).write_text(json.dumps(d,indent=2)+'\n')
print(json.dumps({k:d[k] for k in ['id','state','doi','doi_url','record_url','metadata_normalizations','doi_resolution','receipt_saved'] if k in d},indent=2))
