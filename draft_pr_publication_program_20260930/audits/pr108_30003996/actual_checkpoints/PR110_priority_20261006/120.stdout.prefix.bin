"""Read-only authentication of the submitted problem and prior-report pair."""
from pathlib import Path
import sqlite3,json,hashlib,datetime,os
A=Path(__file__).resolve().parent
D=A/'original_head_authentication_20261006'
R=Path('/Users/alec/Documents/Math/unsolved_math_prioritization')
pins=[]
def require(c,m):
    if not c:raise RuntimeError(m)
def pin(path):
    h=hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda:f.read(1024*1024),b''):h.update(chunk)
    pins.append({'path':str(path),'bytes':path.stat().st_size,'sha256':h.hexdigest()})
def read(rel):
    path=R/rel;pin(path);return json.loads(path.read_text())
problems=read('cache/problems.json');prior=read('cache/research_results.json')
catalog=read('catalog.json');dataset=read('manifest.json')
db=R/'cache/catalog.sqlite';pin(db)
for item in pins:
    name=Path(item['path']).name
    if name in ['problems.json','research_results.json']:
        require(dataset['files'][name]['bytes']==item['bytes'] and dataset['files'][name]['sha256']==item['sha256'],'dataset manifest mismatch')
with sqlite3.connect('file:'+str(db)+'?mode=ro&immutable=1',uri=True) as connection:
    revision=connection.execute('SELECT revision FROM metadata').fetchone()[0]
    row=connection.execute('SELECT payload,report FROM records WHERE key=?',('5100032',)).fetchone()
require(revision==dataset['revision'],'dataset revision')
require(row is not None,'selected SQL row missing')
payload=json.loads(row[0]);report=None if row[1] is None else json.loads(row[1])
raw=[r for r in problems if r['id']==5100032]
selected=[r for r in catalog if str(r['id'])=='5100032']
require(len(raw)==len(selected)==1,'unique source/catalog row')
raw=raw[0];selected=selected[0];code=raw['problem_number']
submitted=json.loads((D/'original_attempt/source_record.json').read_text())
submitted_prior_path=D/'original_attempt/prior_imported_report.json'
submitted_prior=json.loads(submitted_prior_path.read_text()) if submitted_prior_path.exists() else None
require(raw==payload==submitted,'submitted/raw/SQL equality')
require(raw['problem_number']==selected['problem_number']==code,'problem code')
require(prior.get(code,{})==report,'raw/SQL prior report normalization')
if submitted_prior_path.exists():
    require(submitted_prior==report,'submitted prior report equality')
else:
    require(code not in prior and report=={},'authenticated no-join uses native empty-dict normalization')
if report is not None and 'research_classification' in payload:
    require(payload['research_classification']==report['classification'],'classification pair')
(D/'SELECTED_IMPORTED_PRIOR_REPORT.json').write_text(json.dumps(report,indent=2)+'\n')
require(selected['review_hash']==hashlib.sha256(json.dumps([payload,report],sort_keys=True).encode()).hexdigest(),'catalog review hash')
result={'schema':'pr110-sourcepair-authentication/v1','UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'actual_reader_PID':os.getpid(),'problem_id':5100032,'problem_code':code,'dataset_revision':revision,
        'submitted_source_equals_raw_and_SQL':True,'submitted_prior_equals_raw_and_SQL':submitted_prior_path.exists(),
        'authenticated_no_join_prior_report':code not in prior and report=={},
        'catalog_review_hash_verified':True,'catalog_selected':selected,'input_pins':pins,
        'original_budget':'2/5','new_central_proof_search_turns':0,
        'mathematical_clearance':False,'priority_clearance':False}
(D/'SOURCEPAIR_AUTHENTICATION.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
print(json.dumps({k:v for k,v in result.items() if k not in ['catalog_selected','input_pins']}))
