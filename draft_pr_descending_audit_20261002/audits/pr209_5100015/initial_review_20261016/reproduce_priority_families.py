"""Reproduce inspected priority-comparison programs from sealed isolated copies."""
from pathlib import Path
from datetime import datetime,timezone
from concurrent.futures import ThreadPoolExecutor
import hashlib,json,shutil,subprocess

D=Path(__file__).resolve().parent
R=D/'root_reproduction_03'
R.mkdir(exist_ok=False)
PY='/Users/alec/Documents/Math/draft_pr_descending_audit_20261002/audits/pr256_5100017/initial_review_20261013/reproduction_environment/bin/python'
specs=[('priority_author_updates_01','check_comparison.py','COMPARISON_CHECK_RESULTS.json',{'created_utc'}),('priority_classical_general_01','bridge_verify.py','bridge_results.json',set())]

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def job(spec):
    name,script,result,ignored_keys=spec
    F=D/name
    m=F/'AUTHORED_MANIFEST.json'
    frozen=m.read_bytes()
    obj=json.loads(frozen)
    rows=obj.get('files',obj.get('payloads'))
    def validate():
        assert m.read_bytes()==frozen
        for row in rows:
            p=F/row['path']
            assert p.resolve().is_relative_to(F.resolve()) and not p.is_symlink()
            assert p.stat().st_size==row['bytes'] and sha(p)==row['sha256'],str(p)
    validate()
    out=R/name
    out.mkdir()
    shutil.copyfile(F/script,out/script)
    expected=json.loads((F/result).read_text())
    with (out/'stdout.txt').open('wb') as stdout,(out/'stderr.txt').open('wb') as stderr:
        run=subprocess.run([PY,'-B',str(out/script)],cwd=out,stdout=stdout,stderr=stderr,timeout=300)
    assert run.returncode==0 and not (out/'stderr.txt').read_bytes(),name
    actual=json.loads((out/result).read_text())
    ignored=[]
    for k in ignored_keys:
        assert k in expected and k in actual
        ignored.append(dict(field=k,original=expected.pop(k),replay=actual.pop(k)))
    assert actual==expected,(name,'Scientific output differs')
    identical=(out/result).read_bytes()==(F/result).read_bytes()
    if not ignored_keys:assert identical,name
    validate()
    receipt=dict(utc=datetime.now(timezone.utc).isoformat(),status='PASS',family=name,source_manifest_sha256=hashlib.sha256(frozen).hexdigest(),sealed_payloads=len(rows),all_payloads_before_after_verified=True,program_sha256=sha(F/script),original_result_sha256=sha(F/result),replay_result_sha256=sha(out/result),all_scientific_fields_exact=True,result_byte_identical=identical,ignored_fields=ignored,original_family_unchanged=True,exit_code=0,stderr_bytes=0,limitations='Exact finite arithmetic and non-interval high-precision diagnostics corroborate written universal bridges; no historical priority or first-publication certificate.')
    (out/'ROOT_REPLAY_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps(receipt,indent=2),flush=True)
    return receipt

with ThreadPoolExecutor(max_workers=2) as pool:
    results=list(pool.map(job,specs))
(R/'ROOT_PRIORITY_REPRODUCTION.json').write_text(json.dumps(dict(utc=datetime.now(timezone.utc).isoformat(),status='PASS',jobs=results,no_original_file_or_external_mutations=True),indent=2)+'\n')
