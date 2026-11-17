from pathlib import Path
from hashlib import sha256
from datetime import datetime, timezone, timedelta
import json, os, stat, sys

P = Path('/Users/alec/Documents/Math/research_website_catalogue_20261024')
V = P / 'verification'
N = V / 'hafnian-retract-production-prepare-sol-20261117'
E = V / 'hafnian-retract-production-root-executions-20261117'

def read_json(path):
    return json.loads(path.read_text())

def packed(value):
    return (json.dumps(value, sort_keys=True, separators=(',', ':'), ensure_ascii=False) + '\n').encode()

def pin(path):
    return dict(path=str(path), bytes=path.stat().st_size,
                SHA256=sha256(path.read_bytes()).hexdigest(), mode=format(stat.S_IMODE(path.stat().st_mode), '04o'))

def census(root):
    files, directories = [], []
    for path in sorted(root.rglob('*')):
        assert not path.is_symlink()
        row = dict(path=path.relative_to(root).as_posix(), mode=format(stat.S_IMODE(path.stat().st_mode), '04o'))
        if path.is_file():
            row.update(bytes=path.stat().st_size, SHA256=sha256(path.read_bytes()).hexdigest())
            files.append(row)
        else:
            assert path.is_dir()
            directories.append(row)
    return dict(root=str(root), root_mode=format(stat.S_IMODE(root.stat().st_mode), '04o'),
                files=files, directories=directories, regular_files=len(files), child_directories=len(directories))

assert sys.argv[1] in ('preflight', 'verify-installed', 'install', 'publish')
mode = sys.argv[1]
p = read_json(N / 'PLAN.json')
assert pin(N / 'PLAN.json')['SHA256'] == '682ae4747c3004aef1b74fb8bce7f43b76984c427353419a7e8c770e941fa2a1'
assert pin(N / 'release_two.py')['SHA256'] == '6a831b55fbd1d49196619e047e6461d36c9171da94f5ede8d45cdd8148d5b734'
bindings = dict(helper=pin(N / 'release_two.py'), PLAN=pin(N / 'PLAN.json'),
                controls=p['controls'], record_ids=p['record_ids'], scope_paths=p['scope_paths'],
                runtime_root=p['runtime_root'], website_HEAD=p['website_HEAD'], website_tree=p['website_tree'],
                website_index=p['website_index'], Math_native_main=p['Math_native_main'],
                stage_review_pending_during_preparation=True)
helper_audit_path = V / 'hafnian-retract-production-audit-sol-20261117/FINAL.json'
helper_audit = read_json(helper_audit_path)
assert pin(helper_audit_path)['SHA256'] == 'c4097bee1f854db2362148f6ac85c5bb754f7e8ce371fee0d8cfdc831e508faa'
helper_review = dict(audit_FINAL=pin(helper_audit_path), actual_schema_present=True,
    actual_schema=helper_audit['schema'], actual_status_present=True, actual_status=helper_audit['status'],
    root_personally_read_complete_helper_PLAN_and_audit=True,
    root_adopts_all_findings_for_exact_current_helper_PLAN=True,
    root_resolution=dict(classification='ALL_STATIC_FINDINGS_RESOLVED_FOR_EXACT_ACTION',
        rationale='Root read all1260 actual saved helper lines, complete PLAN and full independent static report/FINAL/findings; fresh18file audit custody accepted. No blocking static flaw. Final effective runtime ignore verified separately; active current-state checks still mandatory.',
        helper=bindings['helper'], PLAN=bindings['PLAN']))
adoption_path = V / 'root-hafnian-retract-corrected-stage-adoption-20261117.json'
assert pin(adoption_path)['SHA256'] == '6976d6953ce3c10775077257321ae7bdb809a1898d96ef95efadcd3785166dc6'
audit_root = V / 'hafnian-retract-stage-audit-continuation-sol-20261117'
audit = read_json(audit_root / 'FINAL.json')
assert pin(audit_root / 'FINAL.json')['SHA256'] == '32f304fa1ef31a62897d384ba0785b39a3b357e6931cb99a9668fa99c43465dc'
assert pin(audit_root / 'OWNED_MANIFEST.json')['SHA256'] == '9aefd0049fc758708dd61972944e87a3369832eae28586ea2c4573597769e845'
stage_review = dict(root_adoption=pin(adoption_path), root_adoption_semantics=read_json(adoption_path),
    audit_FINAL=pin(audit_root / 'FINAL.json'), audit_manifest=pin(audit_root / 'OWNED_MANIFEST.json'),
    audit_snapshot=census(audit_root), actual_schema_present=True, actual_schema=audit['schema'],
    actual_status_present=True, actual_status=audit['status'],
    root_resolution=dict(classification='ALL_28_STAGE_CRITERIA_ACCEPTED_FOR_EXACT_STAGE',
        rationale='Root personally read all670 builder lines, entire diff, complete accepted copies and current independent28criteria/REPORT/FINAL; fresh1622file custody verifies exact stage and both audit lanes. Earlier producer/auditor failures remain distinct, no generic future-parser certificate inferred.',
        criterion_count=28, all_criteria_accepted=True, root_personally_read_complete_stage_and_audit=True,
        stage_FINAL=p['controls']['stage_FINAL'], stage_manifest=p['controls']['stage_manifest'],
        audit_FINAL=pin(audit_root / 'FINAL.json'), audit_manifest=pin(audit_root / 'OWNED_MANIFEST.json')))
kind = 'readonly' if mode in ('preflight', 'verify-installed') else mode
phase = 'installed' if mode in ('verify-installed', 'publish') else 'before_install'
now = datetime.now(timezone.utc)
nonce = os.urandom(32).hex()
a = dict(schema=p['authority_schema'], action={'readonly':'READONLY_EXACT11_PREFLIGHT',
    'install':'INSTALL_EXACT11_FILESYSTEM', 'publish':'PUBLISH_EXACT11_GIT'}[kind],
    phase=phase, bindings=bindings, concurrency='ROOT_SERIALIZED_NO_OTHER_W_WRITER',
    root_asserts_nonce_fresh=True, root_asserts_no_other_W_writer=True,
    deployment_authorized=False, Sheet_authorized=False, AA=None, follow_up=None,
    issued_UTC=now.isoformat(), expires_UTC=(now+timedelta(seconds=3600)).isoformat(), nonce=nonce,
    helper_review=helper_review, stage_review=stage_review)
if kind == 'readonly':
    a['request_fingerprint_SHA256'] = sha256(packed(dict(bindings=bindings, phase=phase, nonce=nonce))).hexdigest()
else:
    previous = read_json(Path(sys.argv[2]))
    assert previous['status'] == ('READONLY_INSTALLED_PREFLIGHT' if kind == 'publish' else 'READONLY_PREINSTALL_PREFLIGHT')
    assert previous['state']['bindings'] == bindings
    a['preflight_SHA256'] = previous['preflight_SHA256']
if kind == 'publish':
    install_result = read_json(Path(sys.argv[3]))
    success = Path(install_result['transaction']) / 'SUCCESS.json'
    assert read_json(success) == install_result
    a.update(installation_SUCCESS=pin(success), author_name=p['author_name'], author_email=p['author_email'],
             commit_date=now.replace(microsecond=0).isoformat())
E.mkdir(exist_ok=True)
history = E / 'authority-history'
history.mkdir(exist_ok=True)
target = Path(p['authority_paths'][kind])
if target.exists():
    old = target.read_bytes()
    archive = history / (sha256(old).hexdigest() + '.json')
    if archive.exists():
        assert archive.read_bytes() == old
    else:
        archive.write_bytes(old)
        archive.chmod(0o644)
raw = packed(a)
new_history = history / (sha256(raw).hexdigest() + '.json')
assert not new_history.exists()
new_history.write_bytes(raw)
new_history.chmod(0o644)
target.write_bytes(raw)
target.chmod(0o644)
print(json.dumps(dict(mode=mode, phase=phase, authority=str(target), bytes=len(raw),
                      SHA256=sha256(raw).hexdigest(), expires_UTC=a['expires_UTC'])))
