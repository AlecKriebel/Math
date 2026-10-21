"""Fresh own-folder reproduction of exact PR126 closure evidence; explicit guards."""
from pathlib import Path
import datetime, hashlib, json, os, subprocess, sys

F = Path(__file__).resolve().parent
B = F.parent
O = B / 'original_head_authentication_20261006/original_attempt'
PY = '/opt/homebrew/Cellar/python@3.14/3.14.6/Frameworks/Python.framework/Versions/3.14/bin/python3.14'

def require(condition, message):
    if not condition:
        raise RuntimeError(message)

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def original_binding():
    return {str(p.relative_to(O)): {'bytes':p.stat().st_size,'sha256':digest(p)}
            for p in sorted(O.rglob('*')) if p.is_file()}

before = original_binding()
auth = json.loads((B/'original_head_authentication_20261006/ORIGINAL_AUTHENTICATION.json').read_text())
require(len(before)==16, 'Unexpected original inventory')
require(all(before[x['path']]=={'bytes':x['bytes'],'sha256':x['sha256']} for x in auth['original_files']), 'Original body mismatch')
results=[]
for family, repair, optimized, corrupt in [
    ('author',False,False,False),
    ('independent',False,False,False),
    ('independent',False,False,True),
    ('independent',False,True,True),
    ('independent',True,False,False),
    ('independent',True,True,False),
    ('independent',True,False,True),
    ('independent',True,True,True),
]:
    label=f'{family}_repair{int(repair)}_optimized{int(optimized)}_corrupt{int(corrupt)}'
    r=F/'isolated_reproduction'/label
    r.mkdir(parents=True,exist_ok=False)
    code_name='verify.py' if family=='author' else 'independent_checks.py'
    code=(O/(code_name if family=='author' else 'review/'+code_name)).read_text()
    if repair:
        marker='    assert p,cat\n'
        require(code.count(marker)==1,'Repair marker ambiguous')
        code=code.replace(marker,'    if not p:\n        raise AssertionError(cat)\n')
    if corrupt:
        marker='C = ((8, -11), (3, -4))' if family=='author' else 'C=((8,-11),(3,-4))'
        replacement='C = ((8, -11), (4, -4))' if family=='author' else 'C=((8,-11),(4,-4))'
        require(code.count(marker)==1,'Corruption marker ambiguous')
        code=code.replace(marker,replacement)
    (r/code_name).write_text(code)
    candidate=r/'CANDIDATE.md' if family=='author' else r/'author_replay/CANDIDATE.md'
    candidate.parent.mkdir(parents=True,exist_ok=True)
    candidate.write_bytes((O/'CANDIDATE.md').read_bytes())
    command=[PY,'-E','-S','-B','-P']+(['-O'] if optimized else [])+[str(r/code_name)]
    run=subprocess.run(command,cwd=r,capture_output=True,timeout=30)
    (r/'stdout.txt').write_bytes(run.stdout)
    (r/'stderr.txt').write_bytes(run.stderr)
    receipt=r/('verification.json' if family=='author' else 'independent_checks.json')
    submitted=O/('verification.json' if family=='author' else 'review/independent_checks.json')
    expected_pass=(not corrupt) or (family=='independent' and optimized and not repair)
    require((run.returncode==0)==expected_pass, 'Unexpected diagnostic outcome '+label)
    require(receipt.exists()==expected_pass,'Unexpected receipt existence '+label)
    data=json.loads(receipt.read_bytes()) if receipt.exists() else None
    if expected_pass:
        require(receipt.read_bytes()==submitted.read_bytes(),'Receipt byte mismatch '+label)
        require((data.get('total_assertions') or data.get('exact_assertions'))==(311 if family=='author' else 3156),'Wrong count '+label)
    results.append({'case':label,'command':command,'returncode':run.returncode,
                    'verifier_sha256':digest(r/code_name),'receipt_written':receipt.exists(),
                    'receipt_byte_identical_to_submitted':receipt.read_bytes()==submitted.read_bytes() if receipt.exists() else None,
                    'receipt_sha256':digest(receipt) if receipt.exists() else None,
                    'control_count':(data.get('total_assertions') or data.get('exact_assertions')) if data else None,
                    'stdout_sha256':hashlib.sha256(run.stdout).hexdigest(),'stderr_sha256':hashlib.sha256(run.stderr).hexdigest()})

def mm(x,y):
    return tuple(tuple(sum(x[i][k]*y[k][j] for k in range(2)) for j in range(2)) for i in range(2))
def inv(x):
    require(x[0][0]*x[1][1]-x[0][1]*x[1][0]==1,'Inverse determinant')
    return ((x[1][1],-x[0][1]),(-x[1][0],x[0][0]))
A=((3,1),(2,1)); BB=((1,-2),(-1,3)); C=((8,-11),(3,-4))
X=((0,1),(-1,0));Y=((-2,-1),(3,1));I=((1,0),(0,1))
binding={
    'BKL_Eq4':mm(mm(A,BB),inv(A))==C,
    'BKL_Eq8':mm(A,BB)==mm(C,A)==mm(BB,C)==((2,-3),(1,-1)),
    'AB_braid':mm(mm(A,BB),A)==mm(mm(BB,A),BB)==((0,-1),(1,0)),
    'AC_braid':mm(mm(A,C),A)==mm(mm(C,A),C)==((7,-10),(5,-7)),
    'BC_braid':mm(mm(BB,C),BB)==mm(mm(C,BB),C)==((5,-13),(2,-5)),
    'source_pair':mm(X,Y)==A and mm(Y,X)==BB and mm(X,X)==((-1,0),(0,-1)) and mm(mm(Y,Y),Y)==I,
    'distinct':len({A,BB,C})==3,
    'pair_noncommutation':all(mm(u,v)!=mm(v,u) for u,v in ((A,BB),(A,C),(BB,C))),
    'determinant_one_trace_four':all(m[0][0]*m[1][1]-m[0][1]*m[1][0]==1 and m[0][0]+m[1][1]==4 for m in (A,BB,C)),
}
require(all(binding.values()),'Independent primary-to-matrix binding failure')
gate=json.loads((B/'MATHEMATICAL_SOURCE_GATE_20261006.json').read_text())
gate_members={p:digest(Path(p))==h for p,h in gate['reviewed_artifact_hashes'].items()}
require(all(gate_members.values()),'Gate member changed')
after=original_binding()
require(before==after,'Original bytes changed')
out={'schema':'pr126-fresh-disposition-comment-reproduction/v1','UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),
     'actual_operator_PID':os.getpid(),'interpreter':sys.version,'cases':results,
     'independent_primary_to_matrix_binding':binding,'mathematical_gate_member_hashes_match':gate_members,
     'original16_unchanged':True,'original16':before,'original_effort':'1/5','new_proof_search_turns':0,
     'all_required_diagnostics_as_expected':True,'no_shared_writer_or_service_mutation':True}
(F/'COMMENT_CLAIMS_REPRODUCTION.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
print(json.dumps({'PASS':True,'UTC':out['UTC'],'PID':out['actual_operator_PID'],'cases':[{k:r[k] for k in ('case','returncode','receipt_written','receipt_byte_identical_to_submitted','control_count')} for r in results],'primary_binding':binding,'original16_unchanged':True},indent=2))
