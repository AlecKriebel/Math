"""Fresh local archive reproduction and independent operator controls.
All writes are confined to this review directory; no publication/upload actions.
"""
from pathlib import Path
from fractions import Fraction as F
from datetime import datetime, timezone
import hashlib, json, os, subprocess, sys, zipfile

BASE = Path(__file__).resolve().parent
PACKAGE = BASE.parent / 'publication_package_v1'
MEMBERS = ['LICENSE-CODE.txt', 'LICENSE-TEXT.md', 'README.md', 'SHA256SUMS',
           'SOURCE_QUALIFICATIONS.md', 'VERIFICATION_PROVENANCE.json', 'VERIFICATION_RECORD.json',
           'build_verification_zip.py', 'integer_endpoint_discontinuity.tex',
           'expected_results.json', 'verify_integer_endpoint.py']

def now(): return datetime.now(timezone.utc).isoformat()
def pin(body): return {'bytes':len(body), 'sha256':hashlib.sha256(body).hexdigest()}
def save(name, obj): (BASE/name).write_text(json.dumps(obj, indent=2, sort_keys=True)+'\n')

def run(name, argv, cwd, environment=None):
    # Preserve complete prelaunch inputs before Popen; this is real process capture.
    env = os.environ.copy()
    env.pop('PYTHONOPTIMIZE', None)
    if environment: env.update(environment)
    pre = {'operator_pid':os.getpid(), 'start_utc':now(), 'argv':argv,
           'cwd':str(cwd), 'operator':pin(Path(__file__).read_bytes()),
           'environment_override':environment or {},
           'checker':pin((cwd/'verify_integer_endpoint.py').read_bytes())}
    save(name+'.PRELAUNCH.json', pre)
    proc = subprocess.Popen(argv, cwd=cwd, env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = proc.communicate(timeout=90)
    (BASE/(name+'.stdout.bin')).write_bytes(stdout)
    (BASE/(name+'.stderr.bin')).write_bytes(stderr)
    cap = dict(pre, child_pid=proc.pid, end_utc=now(), exit_code=proc.returncode,
               stdout=pin(stdout), stderr=pin(stderr), actual_execution=True)
    save(name+'.CAPTURE.json', cap)
    return proc.returncode, stdout, stderr

def add(a,b):
    q=dict(a)
    for m,c in b.items(): q[m]=q.get(m,F(0))+c
    return {m:c for m,c in q.items() if c}
def scale(a,c): return {m:v*c for m,v in a.items() if v*c}
def mul(a,b):
    q={}
    for (i,j),c in a.items():
        for (k,l),d in b.items():
            if i+j+k+l <= 2: q[i+k,j+l]=q.get((i+k,j+l),F(0))+c*d
    return {m:c for m,c in q.items() if c}
def lap(a): return 2*(a.get((2,0),F(0))+a.get((0,2),F(0)))

def independent_operator_control():
    # Nonorthogonal J, nonlinear quadratic f, nonzero scalar gradient and Hessian.
    # Build the inverse through order two by composing f(G(y)), then evaluate v(G).
    J=[[F(2),F(1)],[F(1),F(3)]]
    # Use a nonsymmetric J to distinguish HH^T from H^TH.
    J=[[F(2),F(1)],[F(-1),F(3)]]
    H=[[F(3,7),F(-1,7)],[F(1,7),F(2,7)]]
    Q=[[[F(2),F(3)],[F(3),F(4)]], [[F(-2),F(1)],[F(1),F(6)]]]
    V=[[F(4),F(5)],[F(5),F(-2)]]; gradient=[F(7),F(-3)]
    coords=[{(1,0):F(1)},{(0,1):F(1)}]
    linear=[add(scale(coords[0],H[i][0]),scale(coords[1],H[i][1])) for i in range(2)]
    inverse=[]
    for i in range(2):
        jet=linear[i]
        for a in range(2):
            for j in range(2):
                for k in range(2): jet=add(jet,scale(mul(linear[j],linear[k]),-H[i][a]*Q[a][j][k]/2))
        inverse.append(jet)
    for a in range(2):
        composed={}
        for i in range(2): composed=add(composed,scale(inverse[i],J[a][i]))
        for j in range(2):
            for k in range(2): composed=add(composed,scale(mul(inverse[j],inverse[k]),Q[a][j][k]/2))
        assert composed == coords[a]
    scalar={}
    for i in range(2): scalar=add(scalar,scale(inverse[i],gradient[i]))
    for j in range(2):
        for k in range(2): scalar=add(scalar,scale(mul(inverse[j],inverse[k]),V[j][k]/2))
    A=[[sum(H[i][a]*H[j][a] for a in range(2)) for j in range(2)] for i in range(2)]
    wrongA=[[sum(H[a][i]*H[a][j] for a in range(2)) for j in range(2)] for i in range(2)]
    B=[-sum(H[i][a]*Q[a][j][k]*A[j][k] for a in range(2) for j in range(2) for k in range(2)) for i in range(2)]
    principal=sum(A[i][j]*V[i][j] for i in range(2) for j in range(2))
    drift=sum(B[i]*gradient[i] for i in range(2))
    direct=lap(scalar)
    assert direct == principal+drift
    assert direct != principal and principal != sum(wrongA[i][j]*V[i][j] for i in range(2) for j in range(2))
    return {'direct_inverse_composition_laplacian':str(direct), 'principal_HHt':str(principal),
            'drift':str(drift), 'incorrect_principal_HtH':str(sum(wrongA[i][j]*V[i][j] for i in range(2) for j in range(2))),
            'nonlinear_inverse_recomposition_exact':True, 'finite_control_not_universal_proof':True}

def main():
    if not __debug__: raise RuntimeError('Run this review operator without optimization')
    archive=PACKAGE/'integer-endpoint-discontinuity-verification-v1.zip'
    isolated=BASE/'isolated_archive'
    isolated.mkdir(exist_ok=False)
    member_pins={}
    with zipfile.ZipFile(archive) as z:
        assert z.namelist()==MEMBERS and z.testzip() is None
        for info in z.infolist():
            assert info.filename in MEMBERS and '/' not in info.filename
            assert info.date_time==(1980,1,1,0,0,0) and (info.external_attr>>16)==0o100644
            body=z.read(info.filename)
            assert body==(PACKAGE/info.filename).read_bytes()
            (isolated/info.filename).write_bytes(body)
            member_pins[info.filename]=pin(body)
    rows=[line.split('  ',1) for line in (isolated/'SHA256SUMS').read_text().splitlines()]
    assert len(rows)==10 and {name for digest,name in rows}==set(MEMBERS)-{'SHA256SUMS'}
    for digest,name in rows: assert member_pins[name]['sha256']==digest
    save('ARCHIVE_MEMBER_CHECK.json', {'observed_utc':now(), 'archive':pin(archive.read_bytes()), 'members':member_pins,
          'exact_11_members_and_10_checksum_rows':True, 'regular_file_modes_and_normalized_timestamps':True})
    py=sys.executable
    code,out,err=run('checker_normal',[py,'-B','verify_integer_endpoint.py'],isolated)
    assert code==0 and not err and out==(isolated/'expected_results.json').read_bytes()
    result=json.loads(out)
    counts={k:result[k] for k in ['geometric_control_count','logarithm_recurrence_control_count','Beltrami_degree_control_count','rational_metric_reconstruction_control_count']}
    assert list(counts.values())==[5,35,328,6]
    for name,args,env in [('checker_O',[py,'-B','-O','verify_integer_endpoint.py'],None),
                          ('checker_ENV',[py,'-B','verify_integer_endpoint.py'],{'PYTHONOPTIMIZE':'1'})]:
        code,out,err=run(name,args,isolated,env)
        assert code!=0 and not out and b'Assertions must be enabled' in err
    code,out,err=run('archive_build',[py,'-B','build_verification_zip.py'],isolated)
    assert code==0 and not err
    assert (isolated/archive.name).read_bytes()==archive.read_bytes()
    code,out,err=run('archive_overwrite_refusal',[py,'-B','build_verification_zip.py'],isolated)
    assert code!=0 and not out and b'Refusing overwrite' in err
    save('INDEPENDENT_OPERATOR_CONTROL.json',independent_operator_control())
    record=json.loads((isolated/'VERIFICATION_RECORD.json').read_text())
    assert record['actual_run']['manuscript']['sha256']==member_pins['integer_endpoint_discontinuity.tex']['sha256']
    assert record['actual_run']['checker']['sha256']==member_pins['verify_integer_endpoint.py']['sha256']
    assert record['expected_results']['sha256']==pin((isolated/'expected_results.json').read_bytes())['sha256']
    save('REPRODUCTION_SUMMARY.json',{'completed_utc':now(),'operator_pid':os.getpid(),'counts':counts,
          'exact_normal_stdout_match':True,'optimized_flag_and_environment_refused':True,
          'fresh_archive_bytes_identical':True,'archive_overwrite_refused':True,
          'archive_record_consistent_with_current_source':True,'universal_proof_claimed_by_finite_testing':False})
    print(json.dumps({'status':'PASS_FRESH_REPRODUCTION_AND_PACKAGE_CONTROLS','counts':counts,
                      'independent_operator_control':independent_operator_control()},indent=2,sort_keys=True))

if __name__=='__main__': main()
