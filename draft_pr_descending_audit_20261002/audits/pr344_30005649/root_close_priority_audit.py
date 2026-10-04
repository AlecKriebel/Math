"""One-shot root closure with native verifier receipts; reviewed payloads stay unchanged."""
from pathlib import Path
import datetime,hashlib,json,stat,subprocess,sys
A=Path(__file__).resolve().parent
N=A/'priority_audit'
AUTH=A/'ROOT_PRIORITY_CLOSURE_AUTHORIZATION.json'
OUT=A/'root_priority_private/priority_closure001'
def utc():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def pin(p):
    b=p.read_bytes()
    return dict(bytes=len(b),sha256=hashlib.sha256(b).hexdigest(),mode=stat.S_IMODE(p.stat().st_mode))
def snapshot():
    result={}
    for p in sorted(N.rglob('*')):
        assert not p.is_symlink()
        if p.is_file():result[p.relative_to(N).as_posix()]=pin(p)
    return result
auth=json.loads(AUTH.read_text())
assert auth['one_time_closure_authorized'] is True
assert pin(N/'DRAFT_AUDIT_MANIFEST.json')['sha256']==auth['whole_manifest_sha256']
assert pin(N/'public_report/PUBLIC_MANIFEST.json')['sha256']==auth['public_manifest_sha256']
seal=Path(auth['permitted_seal_path'])
assert seal==N/'stage3_verification_runs/root_closure001/SEAL.json'
assert not seal.exists() and not OUT.exists() and not (A/'ROOT_PRIORITY_ACCEPTANCE.json').exists()
before=snapshot()
OUT.mkdir()
receipts=[]
for label,target in [('public',N/'public_report/verify_public.py'),('whole',N/'verify_audit_readonly.py')]:
    argv=[sys.executable,'-B',str(target)]
    start=utc()
    proc=subprocess.run(argv,cwd=A,capture_output=True)
    (OUT/(label+'.stdout')).write_bytes(proc.stdout)
    (OUT/(label+'.stderr')).write_bytes(proc.stderr)
    record=dict(argv=argv,cwd=str(A),started_utc=start,completed_utc=utc(),actual_exit=proc.returncode,
                interpreter=pin(Path(sys.executable).resolve()),python_version=sys.version,
                target=pin(target),orchestrator=pin(Path(__file__)),authorization=pin(AUTH),
                stdout=pin(OUT/(label+'.stdout')),stderr=pin(OUT/(label+'.stderr')))
    receipt=OUT/(label+'.native_receipt.json')
    receipt.write_text(json.dumps(record,indent=2)+'\n')
    receipts.append(dict(path=str(receipt),**pin(receipt)))
    print(label,'actual exit',proc.returncode)
    print(proc.stdout.decode())
    assert proc.returncode==0 and not proc.stderr
assert before==snapshot()
gaps=json.loads((N/'public_report/GAPS.json').read_text())
assert not gaps['unresolved_proof_premises']
decision=dict(utc=utc(),status='PRIORITY_ACCEPTED_BOUNDED_APPLICATION_NO_FIRST_PRIORITY_CERTIFICATE',
              priority_percent=100,math_percent=100,workflow_percent=45,
              first_priority_certified=False,first_application_certified=False,continuing_openness_certified=False,
              exact_result=json.loads((A/'ROOT_MATHEMATICAL_ACCEPTANCE.json').read_text())['strongest_verified_result'],
              historical_scope_limits=[g for g in gaps['gaps'] if g['id']!='G07'],
              family_public_manifest_sha256=auth['public_manifest_sha256'],family_whole_manifest_sha256=auth['whole_manifest_sha256'],
              native_verifier_receipts=receipts,closure_authorization=pin(AUTH),
              scientific_adjudication='Classical module, nonselfduality, supersingular completion/factor mechanism and finite Honda lifting credited. Explicit answer to the question as posed by Takao accepted. No continuing-openness or historical-first certificate; retained13 limits do not leave a mathematical premise unresolved.',
              readback_scope='Complete final report/stronger-theory/addendum/gaps/verifiers/plan/log; all revised source/version/search fields compared with previously fully reviewed records; whole667-entry manifest inventory and17 external pins checked natively; preserved365 archival rows and281 unchanged live rows included in replay. No claim to read every primary paper in full.',
              pr_merged=False,published=False)
seal.parent.mkdir(parents=True)
seal.write_text(json.dumps(dict(decision,reviewed_payloads_unchanged=True,
    evidence_boundary='Root decision and closure metadata supported by separate actual verifier-process receipts; not an exit receipt for its own creation.'),indent=2)+'\n')
after=snapshot()
assert {k:v for k,v in after.items() if k not in before}=={seal.relative_to(N).as_posix():pin(seal)}
assert {k:after[k] for k in before}==before
decision['family_seal']=dict(path=str(seal),**pin(seal))
(A/'ROOT_PRIORITY_ACCEPTANCE.json').write_text(json.dumps(decision,indent=2)+'\n')
print(json.dumps(decision,indent=2))
