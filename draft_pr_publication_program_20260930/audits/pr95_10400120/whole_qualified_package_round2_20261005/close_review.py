from review_tools import *
import copy
baseline=json.loads((A/'Q_BASELINE.json').read_text())
for e in baseline['files']:
    p=Q/e['file']
    if sha(p)!=e['sha256']or p.stat().st_size!=e['bytes']:raise RuntimeError('Q changed '+e['file'])
for e in baseline['symlinks']:
    p=Q/e['file']
    if not p.is_symlink()or os.readlink(p)!=e['target']:raise RuntimeError('Q control link changed')
regular=set()
for root,dirs,files in os.walk(Q,followlinks=False):
    for name in files:
        p=Path(root)/name
        if not p.is_symlink():regular.add(str(p.relative_to(Q)))
if regular!=set(e['file']for e in baseline['files']):raise RuntimeError('Q coverage changed')
prior=A.parent/'whole_qualified_package_round1_20261005'
for expected,p in [('be4f8abab1cda0ea36fd60b0174bb409570942fe62ee780e9624f8187ac139e2',prior/'REPORT.md'),('30b71243599df77235d73d7c8b118c342f31bb94654ee6648f1e8bf39e98a4c0',prior/'CLOSED_MANIFEST.json')]:
    if sha(p)!=expected:raise RuntimeError('prior changed')
for e in json.loads((prior/'CLOSED_MANIFEST.json').read_text())['files']:
    p=prior/e['file']
    if sha(p)!=e['sha256']or p.stat().st_size!=e['bytes']:raise RuntimeError('prior transitive changed')
# Reconstruct the attack invocation manifests exactly from frozen authored bytes.
inputfolder=A/'attack_input_manifests';inputfolder.mkdir()
base=(Q/'publicfiles/PAYLOAD_MANIFEST.json').read_bytes()
variants={}
for case in ['ancestor_symlink','nested_ancestor_symlink','leaf_symlink','changed_bytes','missing_member']:variants[case]=base
for case in ['duplicate','unsafe_parent','absolute','wrong_schema','removable_assert_after_rehash']:
    d=json.loads(base)
    if case=='duplicate':d['files'].append(d['files'][0])
    elif case=='unsafe_parent':d['files'].append({'file':'../escape','bytes':0,'sha256':'0'*64})
    elif case=='absolute':d['files'].append({'file':'/tmp/escape','bytes':0,'sha256':'0'*64})
    elif case=='wrong_schema':d['schema']='wrong'
    else:
        data=(Q/'publicfiles/verification/independent_checks.py').read_bytes()+b'\nassert True\n'
        for e in d['files']:
            if e['file']=='verification/independent_checks.py':e.update(bytes=len(data),sha256=hashlib.sha256(data).hexdigest())
        (inputfolder/'assert_variant_independent_checks.py').write_bytes(data)
    variants[case]=(json.dumps(d,indent=2,sort_keys=True)+'\n').encode()
for case,data in variants.items():
    p=inputfolder/(case+'.json');p.write_bytes(data)
    for mode in ['normal','optimized']:
        r=json.loads((A/'processes'/('payload_'+case+'_'+mode)/'process.json').read_text())
        if r['inputs'][1]['sha256']!=sha(p):raise RuntimeError('attack input reconstruction mismatch')
receipts=[]
for root in [A/'processes',A/'fresh_normal',A/'fresh_optimized']:
    for p in root.rglob('process.json'):
        d=json.loads(p.read_text())
        if 'pid'not in d or 'exit_code'not in d:raise RuntimeError('unfinished process record')
        for name in ['stdout.bin','stderr.bin']:
            f=p.parent/name
            if sha(f)!=d[name]['sha256']or f.stat().st_size!=d[name]['bytes']:raise RuntimeError('review stream mismatch')
        if 'inputs'in d:
            for e in d['inputs']:
                if 'snapshot'in e:
                    f=p.parent/e['snapshot']
                    if sha(f)!=e['sha256']or f.stat().st_size!=e['bytes']:raise RuntimeError('review input snapshot mismatch')
        receipts.append({'receipt':str(p.relative_to(A)),'pid':d['pid'],'started_utc':d['started_utc'],'ended_utc':d['ended_utc'],'exit_code':d['exit_code']})
pids=sorted(set(r['pid']for r in receipts));termination=[]
for pid in pids:
    try:os.kill(pid,0);exists=True
    except ProcessLookupError:exists=False
    except PermissionError:exists=True
    termination.append({'pid':pid,'exists_at_closure':exists})
if any(r['exists_at_closure']for r in termination):raise RuntimeError('controlled child PID still exists or reused; investigate')
dump(A/'PROCESS_CLOSURE.json',{'UTC':utc(),'records':receipts,'actual_child_pid_checks':termination,'all_terminated':True,'distinct_controlled_child_pids':len(pids),'limits':'Historical Q/prior PIDs are not retested for identity; only this review actual controlled children are checked.'})
dump(A/'FINAL_INTEGRITY.json',{'UTC':utc(),'Q_unchanged_regular_files':len(regular),'Q_unchanged_intentional_links':len(baseline['symlinks']),'prior_round1_transitive_files_unchanged':997,'target_candidate_manifest':sha(Q/'private_notes/FROZEN_CANDIDATE_MANIFEST.json'),'target_preparation_manifest':sha(Q/'PREPARATION_MANIFEST.json'),'all_review_streams_and_child_input_snapshots_verified':True,'attack_manifest_reconstructions_hash_match_invocation_records':True,'all_controlled_children_terminated':True})
with(A/'RESEARCH_LOG.md').open('a')as f:f.write('- '+utc()+': Final Q2032 regular files/four intentional links and prior round1 transitive997 files unchanged; fresh child inputs/streams and reconstructed attack inputs verified; all'+str(len(pids))+' controlled child PIDs absent. Assigned bounded review100% and closed.\n')
files=[]
for p in sorted(A.rglob('*')):
    if p.is_symlink():raise RuntimeError('unexpected review link remains')
    if p.is_file()and p.name not in ['CLOSED_MANIFEST.json','CLOSURE.json']:files.append({'file':str(p.relative_to(A)),'bytes':p.stat().st_size,'sha256':sha(p)})
dump(A/'CLOSED_MANIFEST.json',{'schema':'PR95-round2-closed-bounded-whole-package-review/v1','UTC':utc(),'operator_pid':os.getpid(),'files':files,'symlinks':[],'candidate_manifest_sha256':sha(Q/'private_notes/FROZEN_CANDIDATE_MANIFEST.json'),'preparation_manifest_sha256':sha(Q/'PREPARATION_MANIFEST.json'),'report_sha256':sha(A/'REPORT.md'),'verdict_sha256':sha(A/'VERDICT.json'),'verdict':'PASS_BOUNDED_MATHEMATICS_AND_QUALIFIED_PACKAGE','priority_clearance':False,'publication_clearance':False,'human_peer_review':False,'new_central_proof_search_turns':0,'review_completion_estimate_percent':100,'transitive_evidence':'Frozen Q prep/public manifests verified; prior round1 closed997 entries verified; all review entries hashed here.'})
dump(A/'CLOSURE.json',{'UTC':utc(),'closed_manifest_sha256':sha(A/'CLOSED_MANIFEST.json'),'report_sha256':sha(A/'REPORT.md'),'verdict_sha256':sha(A/'VERDICT.json'),'closed':True,'review_completion_estimate_percent':100,'all_controlled_children_terminated':True,'priority_status':'UNRESOLVED','publication_clearance':False})
print(json.dumps({'closed_manifest_sha256':sha(A/'CLOSED_MANIFEST.json'),'report_sha256':sha(A/'REPORT.md'),'verdict_sha256':sha(A/'VERDICT.json'),'files':len(files),'terminated_child_pids':len(pids)}))
