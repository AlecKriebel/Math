"""Independent structural and exact arithmetic review checks, read-only inputs."""
from pathlib import Path,PurePosixPath
from fractions import Fraction as Q
from math import comb
import datetime,hashlib,json,subprocess,zipfile
R=Path(__file__).resolve().parent; A=R.parents[1];P=A/'publication';repo=Path('/Users/alec/Documents/Math')
def need(v,m):
    if not v:raise RuntimeError(m)
def sha(data):return hashlib.sha256(data).hexdigest()
c=json.loads((A/'CURRENT_PR1274_CONTEXT.json').read_text());s=json.loads((A/'SUBMITTED_SNAPSHOT.json').read_text());contract=[]
need(len(c['portable_files'])==173 and len(c['authored_freezes'])==12,'context counts')
for e in c['portable_files']:
    raw=e['path'];n=PurePosixPath(raw);need(str(n)==raw and not n.is_absolute() and '..' not in n.parts,'portable path')
    b=(A/raw).read_bytes();need(len(b)==e['bytes'] and sha(b)==e['sha256'],'portable bytes '+raw)
for reg in c['authored_freezes']:
    manifest=json.loads((A/reg['path']).read_text());rows=manifest[reg['entries_key']];seen=set()
    for e in rows:
        raw=e[reg['path_key']];need(raw not in seen,'duplicate nested');seen.add(raw)
        n=PurePosixPath(raw);need(str(n)==raw and not n.is_absolute() and '..' not in n.parts,'relative nested')
        b=(A/reg['base']/raw).read_bytes();need(len(b)==e[reg['size_key']] and sha(b)==e['sha256'],'nested bytes')
        need(reg['base']+'/'+raw in {p['path'] for p in c['portable_files']},'nested not portable')
    contract.append({'manifest':reg['path'],'entries':len(rows),'declared_schema':[reg[k] for k in ['entries_key','path_key','size_key']]})
# Reconstruct exact archive membership independently, not by source receipts.
expected={x['path'] for x in c['portable_files']}
names={'AUDIT.md','EDITORIAL_MAP.json','PROOF.md','PUBLIC_MANIFEST.json','README.md','SOURCE_VERIFICATION.json'}
expected|={folder+'/'+name for folder in ['current_edition','original_submitted'] for name in names}
expected|={'provenance/'+name for name in ['CURRENT_PR1274_CONTEXT.json','SUBMITTED_SNAPSHOT.json','PRIORITY_ADJUDICATION.json','MATH_GATE.json','COMPILE_RECEIPT.json','LAYOUT_VERIFICATION.json']}
expected|={'manuscript/main.tex','verify.py','MANIFEST.json'}
with zipfile.ZipFile(P/'Beurling_Annihilator_Counterexample_Verification_v1.0.zip') as z:
    need(set(z.namelist())==expected and len(z.namelist())==len(expected)==194,'independent full inventory')
    for name in expected:need(z.read(name)==(P/'verification'/name).read_bytes(),'archive member drift')
# Git reads use fixed immutable original. No index/branch/refs are modified.
parent=subprocess.check_output(['git','rev-list','--parents','-n','1',s['head']],cwd=repo,text=True).split();need(parent==[s['head'],*s['parents']],'original parents')
git_checks=[]
for e in s['files']:
    name=Path(e['path']).name;b=subprocess.check_output(['git','show',s['head']+':'+e['path']],cwd=repo)
    need(b==(A/'submitted'/name).read_bytes()==(A/'current_edition'/name).read_bytes(),'six original bytes')
    need(sha(b)==e['sha256'] and len(b)==e['bytes'],'snapshot hashes')
    git_checks.append({'name':name,'bytes':len(b),'sha256':sha(b)})
# Existing editorial output can be authenticated without an absent older input.
editorial=[];editor=json.loads((A/'submitted/EDITORIAL_MAP.json').read_text())
for item in editor['artifacts']:
    b=(A/'submitted'/item['artifact']).read_bytes();need(len(b)==item['output']['bytes'] and sha(b)==item['output']['sha256'],'editorial output')
    for e in item.get('operations',[]):
        selected=b[e['output_start']:e['output_end']];need(selected==e['replacement_utf8'].encode() and sha(selected)==e['replacement_sha256'],'replacement span')
    for e in item.get('unchanged_ranges',[])+item.get('protected_mathematical_regions',[]):
        selected=b[e['output_start']:e['output_end']];need(len(selected)==e['bytes'] and sha(selected)==e['sha256'],'visible output unchanged span')
    editorial.append({'artifact':item['artifact'],'output_spans_authenticated':True,'absent_historical_input_not_certified':True})
# An independent binomial integral identity, using m beyond retained root range.
math_cases=[]
for m in [1,2,3,17,129,257,513]:
    H=sum((Q(1,k) for k in range(1,m+1)),Q());integral=sum((Q((-1)**(k+1)*comb(m,k),k) for k in range(1,m+1)),Q());need(H==integral,'binomial/H integral')
    for t in [Q(1,1000),Q(1,7),Q(1,2),Q(999,1000)]:
        amp=1-(1-t)**m; p=sum(((1-t)**j for j in range(m)),Q());need(amp==t*p and 0<amp<1,'amplitude')
        primitive=-sum(((1-t)**k/Q(k) for k in range(1,m+1)),Q());g=amp+primitive;need(-H<g<1,'strict output range')
        derivative=p+m*(1-t)**(m-1);need(derivative>0,'positive derivative')
    math_cases.append({'m':m,'harmonic_integral_exact':True,'four_rational_radii':True})
result={'at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'portable_entries':173,'explicit_nested_manifests':contract,'independently_reconstructed_archive_members':194,'original_git_parent':parent,'original_six':git_checks,'editorial_output':editorial,'independent_exact_math':math_cases,'status':'PASS','scope':'Exact arithmetic and current bytes only. Analytic all-m proof independently read separately; historical missing input and old mental exposure not reconstructed.'}
(R/'CONTRACT_CHECKS.json').write_text(json.dumps(result,indent=2)+'\n');print({'status':'PASS','portable':173,'manifests':len(contract),'archive':194,'beyond_root_m':[129,257,513]})
