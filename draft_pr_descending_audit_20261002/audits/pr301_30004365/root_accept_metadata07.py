"""Authenticate the closed fresh review; this grants no writer lease."""
from pathlib import Path
from datetime import datetime, timezone
import gzip, hashlib, json, os, stat, sys

A = Path(__file__).resolve().parent
D = A / 'metadata_completion_adversary_07'
W = A / 'branch_correction_metadata_completion_v01'
sha = lambda b: hashlib.sha256(b).hexdigest()
load = lambda p: json.loads(Path(p).read_bytes())
def need(x, why):
    if not x:
        raise RuntimeError(why)
def pin(p):
    p = Path(p)
    need(p.is_file() and not p.is_symlink(), 'literal complete file')
    b = p.read_bytes()
    return dict(path=str(p), bytes=len(b), sha256=sha(b), mode=stat.S_IMODE(p.stat().st_mode))
def same_logical(p, x):
    b = Path(p).read_bytes()
    need(len(b) == x['bytes'] and sha(b) == x['sha256'], 'complete logical body')
    return b
def main():
    need(not sys.flags.optimize, 'explicit unoptimized checks')
    manifest = load(D/'MANIFEST.json')
    seal = load(D/'FINAL_SEAL.json')
    need(pin(D/'MANIFEST.json')['sha256'] == '66dbf09fc05c62659e6fdcc55594c281409c9881c5a358f8f6610deeb711bd6b', 'announced closed manifest')
    need(pin(D/'FINAL_SEAL.json')['sha256'] == '37ecdafca4851808ed874d64bcea6e3b0d8de6ce530eea0906d5a43015c20325', 'announced closed seal')
    files = manifest['files']
    excluded = manifest['excluded_terminal_roles']
    actual = {str(p.relative_to(D)): pin(p) for p in D.rglob('*') if p.is_file()}
    need(len(actual) == 156 and set(actual) == {x['relative'] for x in files} | set(excluded), 'entire closed 156-file domain')
    need(len(files) == 148 and sum(x['bytes'] for x in files) == 794366, 'whole payload count and size')
    for x in files:
        need({k: actual[x['relative']][k] for k in ['bytes','sha256','mode']} == {k:x[k] for k in ['bytes','sha256','mode']}, 'each frozen payload body/mode')
    need(all(x['mode'] == 0o444 for x in actual.values()), 'all 156 closed file permissions')
    need(stat.S_IMODE(D.stat().st_mode) == 0o555 and all(stat.S_IMODE(p.stat().st_mode) == 0o555 for p in D.rglob('*') if p.is_dir()), 'all closed directory permissions')
    need(sum(x['bytes'] for x in actual.values()) == 827360, 'whole closed domain bytes')
    need(sha(json.dumps(files,sort_keys=True,separators=(',',':')).encode()) == seal['payload_domain_sha256'] and seal['payload_count'] == len(files) and seal['payload_bytes'] == 794366, 'noncircular payload seal')
    need(seal['unresolved_issues'] == [] and seal['execution_authority'] is False, 'closed review has no authority')
    verdict = load(D/'VERDICT.json')
    need(verdict['status'] == 'PASS_EXACT_METADATA_ONLY_COMPLETION_SOURCE_REVIEW' and verdict['unresolved_issues'] == [] and verdict['execution_authority'] is False, 'exact independent verdict')
    for key,n,h in [('source','integrate_correction.py','7f52beff29b3e11336b7e95d7b5bebe1394c5338826662abe78c238d4fd3024e'),('launcher','launch_exact_correction.py','29e6b907b6e593670ab16a6001ebdd8519f1f6d88163d46d7214e9cb70a2ffc9'),('plan','PLAN.json','d8d05db96eb4ef13b9ea48fd5754fe1ebb03f43af3ee6b46b856a4cb92701537'),('conditional_ROOT_helper','root_gate_and_readback.py','2c17b179e6ae32d7cd31046c45e8bbc339215e197bf0606290dfc6fd3bcbb4c9')]:
        need(pin(W/n) == verdict[key] and pin(W/n)['sha256'] == h and pin(W/n)['mode'] == 0o444, 'exact reviewed executable role')
    native = []
    dirs = sorted((D/'native').iterdir())
    need(len(dirs) == 13 and all(p.is_dir() for p in dirs), 'all 13 actual reviewer native captures')
    for c in dirs:
        q,s,e = [load(c/n) for n in ['REQUEST.json','START.json','END.json']]
        need(e['actual_pid'] == s['actual_pid'] > 0 and q['recorder_pid'] == s['recorder_pid'] == e['recorder_pid'], 'actual native child/recorder identities')
        need(datetime.fromisoformat(q['utc']) <= datetime.fromisoformat(s['utc']) <= datetime.fromisoformat(e['utc']), 'native request/start/end chronology')
        need(e['exit_code'] == (1 if c.name in ['audit_complete_v01','audit_complete_v02'] else 0), 'two failed harnesses retained; all remaining completed')
        same_logical(q['recorder_source']['path'],q['recorder_source'])
        for i,a in enumerate(q['argv']):
            z=c/f'source_{i}.gz'
            if z.exists():
                b=gzip.decompress(z.read_bytes())
                rows=[x for x in q['sources'] if x['path'] == a]
                need(len(rows)==1 and len(b)==rows[0]['bytes'] and sha(b)==rows[0]['sha256'] and b==Path(a).read_bytes(), 'complete actual prelaunch source')
        streams={}
        for n in ['stdout','stderr']:
            b=gzip.decompress((c/(n+'.gz')).read_bytes())
            need(len(b)==e[n]['bytes'] and sha(b)==e[n]['sha256'], 'both complete native streams')
            streams[n]=b
        if c.name=='close_review':
            need(e['actual_pid']==seal['actual_finalizer_pid']==58856 and e['recorder_pid']==58855, 'actual completed terminal finalizer')
            out=json.loads(streams['stdout'])
            need(out['manifest']['sha256']==pin(D/'MANIFEST.json')['sha256'] and out['seal']['sha256']==pin(D/'FINAL_SEAL.json')['sha256'] and out['payload_count']==148 and not streams['stderr'], 'terminal stdout binds actual final manifest/seal')
        native.append(dict(relative=c.name,request=pin(c/'REQUEST.json'),started=pin(c/'START.json'),execution=pin(c/'END.json'),actual_PID=e['actual_pid'],actual_recorder_PID=e['recorder_pid'],exit_code=e['exit_code']))
    audit=load(D/'AUDIT_RESULT.json');helper=load(D/'HELPER_AUDIT_RESULT.json');controls=load(D/'ISOLATED_AUTHORITY_CONTROLS.json')
    need(audit['explicit_check_count']==1739 and audit['old_native_capture_count']==113 and audit['old_native_mutation_count']==1 and audit['old_metadata_attempt_count']==0 and audit['old_actual_push_PID']==45620 and audit['old_outer_failed_exit']==1 and audit['unresolved_issues']==[], 'bounded independent source and old actual-capture findings')
    need(helper['explicit_check_count']==44 and helper['unresolved_issues']==[] and controls['case_count']==12 and all(x['passed_or_rejected_as_expected'] and x['actual_native_commands']==0 for x in controls['cases']), 'bounded helper and isolated authority controls')
    ledger=load(D/'READ_SCOPE_LEDGER.json')
    need(ledger['limits'] and ledger['explicit_native_audit_checks']==1739 and ledger['old_metadata_attempt_count']==0, 'review limits and scope retained')
    for p,x in ledger['complete_file_reads'].items():
        b=Path(p).read_bytes()
        need(len(b)==x['bytes'] and sha(b)==x['sha256'], 'all complete read-custody bodies still authentic')
    old=load(D/'OLD_NATIVE_COMMAND_LEDGER.json')
    need(len(old)==113 and [x['relative'] for x in old]==[str(n) for n in range(1,114)] and sum(x['mutation'] for x in old)==1 and old[107]['actual_PID']==45620 and old[107]['exit_code']==0, 'complete actual prior mutation ledger')
    record=dict(status='ROOT_ACCEPTS_EXACT_PR301_METADATA_ONLY_COMPLETION_V01',UTC=datetime.now(timezone.utc).isoformat(),actual_ROOT_PID=os.getpid(),ROOT_source=pin(__file__),source=pin(W/'integrate_correction.py'),launcher=pin(W/'launch_exact_correction.py'),plan=pin(W/'PLAN.json'),conditional_ROOT_helper=pin(W/'root_gate_and_readback.py'),unresolved_issues=[],review_directory=str(D),review_manifest=pin(D/'MANIFEST.json'),review_seal=pin(D/'FINAL_SEAL.json'),review_verdict=pin(D/'VERDICT.json'),review_report=pin(D/'REPORT.md'),review_derivations=pin(D/'DERIVATIONS.md'),read_scope=pin(D/'READ_SCOPE_LEDGER.json'),whole_closed_file_count=156,whole_closed_bytes=827360,actual_native_captures=native,old_successful_single_push_and_failed_API_attempt_preserved=True,old_metadata_attempt_count=0,independent_bounded_checks=dict(custody_source=1739,helper=44,isolated_authority=12),ROOT_semantic_reads=['complete proposed operator, launcher, plan and conditional ROOT helper','complete independent report, derivations, verdict, scope and limitations','complete final audit harness, helper harness, isolated controls, recorder and finalizer'],scientific_acceptance_scope='Inherited exact final v04 science and qualified adverse priority; no new proof or primary-source audit claimed here.',execution_authority=False,fresh_sole_grant_required=True,independent_actual_ROOT_readback_required=True,workflow_complete=False,overall_goal_complete=False,scope='One exact previously unattempted PR301 title/body edit; no repeated push or other Git mutation; OPEN/DRAFT credited already_solved correction, no paper/DOI/tracker/merge/close.')
    target=W/'ROOT_OPERATIONAL_REVIEW_ACCEPTANCE.json'
    with target.open('x') as f:json.dump(record,f,indent=2);f.write('\n')
    target.chmod(0o444)
    print(json.dumps(dict(status=record['status'],acceptance=pin(target)),indent=2))
if __name__=='__main__':main()
