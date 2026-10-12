"""Source-first, read-only authentication; preserve actual retrieval failures."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,subprocess,sqlite3
A=Path(__file__).resolve().parent;P=A.parents[1];R=P.parent
D=A/'source_inputs';D.mkdir(exist_ok=False)
utc=lambda:datetime.now(timezone.utc).isoformat()
sha=lambda b:hashlib.sha256(b).hexdigest()
def run(label,args):
    t=utc();q=subprocess.run(args,cwd=R,capture_output=True)
    for s,b in [('stdout',q.stdout),('stderr',q.stderr)]:(D/(label+'.'+s)).write_bytes(b)
    j=dict(argv=args,cwd=str(R),started_utc=t,ended_utc=utc(),exit_code=q.returncode,
           stdout_bytes=len(q.stdout),stdout_sha256=sha(q.stdout),stderr_bytes=len(q.stderr),stderr_sha256=sha(q.stderr))
    (D/(label+'.execution.json')).write_text(json.dumps(j,indent=2)+'\n')
    return q,j
db=sqlite3.connect('file:'+str(R/'unsolved_math_prioritization/cache/catalog.sqlite')+'?mode=ro',uri=True)
row=db.execute('SELECT payload,report FROM records WHERE key=?',('9900002',)).fetchone();assert row
problem=json.loads(row[0]);prior=json.loads(row[1])
reviewhash=sha(json.dumps([problem,prior],sort_keys=True).encode())
record=dict(review_hash=reviewhash,problem=problem,prior_research=prior)
(D/'imported_record.json').write_text(json.dumps(record,indent=2,ensure_ascii=False)+'\n')
catalog=json.loads((R/'unsolved_math_prioritization/catalog.json').read_bytes())
item=next(x for x in catalog if str(x['id'])=='9900002');assert item['review_hash']==reviewhash
(D/'catalog_record.json').write_text(json.dumps(item,indent=2,ensure_ascii=False)+'\n')
literal=problem.get('statement') or problem.get('problem_statement') or ''
if not literal:print('problem_keys',list(problem))
(D/'problem_payload.json').write_text(json.dumps(problem,indent=2,ensure_ascii=False)+'\n')
captures=[];primary=None
for scheme in ['https','http']:
    url=scheme+'://cms.dm.uba.ar/depto/public/Some%20Open%20Problems-preprint.pdf'
    q,j=run('primary_'+scheme,['curl','--fail','--silent','--show-error','--location','--max-time','45',url])
    captures.append(j)
    if q.returncode==0 and q.stdout.startswith(b'%PDF-'):
        (D/'Some_Open_Problems_preprint.pdf').write_bytes(q.stdout);primary=dict(url=url,bytes=len(q.stdout),sha256=sha(q.stdout));break
receipt=dict(utc=utc(),status='SOURCE_INPUTS_AUTHENTICATED_PRIMARY_RETRIEVED' if primary else 'SOURCE_INPUTS_AUTHENTICATED_PRIMARY_ACCESS_PENDING',
    problem='9900002',review_hash=reviewhash,imported_record_sha256=sha((D/'imported_record.json').read_bytes()),
    primary=primary,native_retrievals=captures,source_first=True,candidate_proof_not_read=True,
    math_acceptance=False,workflow_percent=5,no_person_contacted=True)
(A/'ROOT_SOURCE_INTAKE.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps(receipt,indent=2))
