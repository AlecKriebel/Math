"""Authenticate source payloads and retrieve primary definitions before candidate proof reading."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, shutil, sqlite3, subprocess
A = Path(__file__).resolve().parent
R = A.parents[2]
D = A/'source_inputs_private'
D.mkdir(exist_ok=False)
sha = lambda b: hashlib.sha256(b).hexdigest()
utc = lambda: datetime.now(timezone.utc).isoformat()
def require(c,label):
    if not c:
        raise RuntimeError(label)
def run(label,args,ok=(0,)):
    started = utc()
    q = subprocess.run(args,cwd=R,capture_output=True)
    for k,b in [('stdout',q.stdout),('stderr',q.stderr)]:
        (D/(label+'.'+k)).write_bytes(b)
    e = {'argv':args,'cwd':str(R),'started_utc':started,'ended_utc':utc(),'exit_code':q.returncode,
         'stdout_bytes':len(q.stdout),'stdout_sha256':sha(q.stdout),'stderr_bytes':len(q.stderr),'stderr_sha256':sha(q.stderr)}
    (D/(label+'.execution.json')).write_text(json.dumps(e,indent=2)+'\n')
    require(q.returncode in ok,'Native input retrieval failed: '+label)
    return q,e
manifest = json.loads((R/'unsolved_math_prioritization/manifest.json').read_bytes())
require(manifest['revision'] == '37e53eabe540fb458758e198be61634bd02ee008','Revision changed')
data = {}
for name,p in manifest['files'].items():
    b = (R/'unsolved_math_prioritization/cache'/name).read_bytes()
    require(len(b) == p['bytes'] and sha(b) == p['sha256'],'Raw source changed')
    data[name] = json.loads(b)
hits = [x for x in data['problems.json'] if str(x['id']) == '30005303']
require(len(hits) == 1,'Raw ID not unique')
problem = hits[0]
require(sum(x['problem_number'] == problem['problem_number'] for x in data['problems.json']) == 1,'Report join not unique')
prior = data['research_results.json'][problem['problem_number']]
db = sqlite3.connect('file:'+str(R/'unsolved_math_prioritization/cache/catalog.sqlite')+'?mode=ro',uri=True)
row = db.execute('SELECT payload,report FROM records WHERE key=?',('30005303',)).fetchone()
require(row and json.loads(row[0]) == problem and json.loads(row[1]) == prior,'Read-only database differs from raw source')
db.close()
frozen = A/'snapshot/unsolved_math_prioritization/attempts/30005303/source_record.json'
require(json.loads(frozen.read_bytes()) == problem,'Submitted source record differs')
review_hash = sha(json.dumps([problem,prior],sort_keys=True).encode())
catalog = json.loads((R/'unsolved_math_prioritization/catalog.json').read_bytes())
entry = next(x for x in catalog if str(x['id']) == '30005303')
require(entry['review_hash'] == review_hash,'Catalog source/report hash differs')
for name,obj in [('problem_payload.json',problem),('prior_research.json',prior),('catalog_record.json',entry)]:
    (D/name).write_text(json.dumps(obj,indent=2,ensure_ascii=False)+'\n')
q,fetch = run('primary_fetch',['/usr/bin/curl','--fail','--silent','--show-error','--location','--max-time','45','https://ems.press/content/serial-article-files/46992'])
require(q.stdout.startswith(b'%PDF-'),'Primary content is not PDF')
pdf = D/'OWR-2022-55.pdf'
pdf.write_bytes(q.stdout)
text_tool,render_tool = shutil.which('pdftotext'),shutil.which('pdftoppm')
require(text_tool and render_tool,'Primary PDF inspection tools unavailable')
run('primary_text',[text_tool,'-layout',str(pdf),str(D/'OWR-2022-55.txt')])
run('primary_pages',[render_tool,'-f','5','-l','7','-scale-to','1800','-png',str(pdf),str(D/'primary_page')])
receipt = {'utc':utc(),'status':'PASS_SOURCE_RAW_IMPORT_AND_PRIMARY_BINARY_RETRIEVED',
    'original_pr_head':'895f2ba037e71bac054b58f1a4be7bb4d5dbd53a','problem_id':'30005303',
    'raw_revision':manifest['revision'],'raw_files':manifest['files'],'unique_source_id_and_report_join':True,
    'raw_problem_report_equal_readonly_database':True,'submitted_source_record_equal_raw':True,
    'review_hash':review_hash,'problem_source_record_sha256':sha(frozen.read_bytes()),
    'prior_research_sha256':sha((D/'prior_research.json').read_bytes()),
    'primary_pdf':{'url':'https://ems.press/content/serial-article-files/46992','bytes':len(q.stdout),'sha256':sha(q.stdout)},
    'native_fetch':fetch,'primary_pages_rendered':[3125,3126,3127],
    'primary_visual_inspection_pending':True,'candidate_proof_not_read':True,
    'prior_research_prose_not_read':True,'source_first_families_active':['lattice_factorization','markov_closure'],
    'math_percent':0,'workflow_percent':7,'no_external_contact':True}
(A/'ROOT_SOURCE_INTAKE.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps(receipt,indent=2))
