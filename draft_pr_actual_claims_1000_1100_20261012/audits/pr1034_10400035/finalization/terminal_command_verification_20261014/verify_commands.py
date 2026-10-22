"""Independent bounded final administration verification and documented replay."""
import datetime
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import time
import zipfile

HERE=Path(__file__).resolve().parent
AUDIT=HERE.parent.parent
PR=int(AUDIT.name.split('_')[0][2:])
PUB=AUDIT/('publication' if PR==1034 else 'preprint')
FINAL=AUDIT/'finalization/terminal_admin_20261014'
ARCHIVE=PUB/('source_audit_kit.zip' if PR==1034 else 'pr1037_supportkit_v1.0.zip')
PYTHON=sys.executable if PR==1034 else str(AUDIT/'reviews/package_02/.venv/bin/python')
RECEIPTS=[]

def require(ok,why):
    if not ok:raise RuntimeError(why)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def record(p):return {'path':str(p.relative_to(AUDIT)),'bytes':p.stat().st_size,'sha256':sha(p)}
def save(p,obj):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(obj,indent=2,ensure_ascii=False)+'\n')
def run(name,command,cwd,expected=0):
    start=time.perf_counter();r=subprocess.run(command,cwd=cwd,capture_output=True)
    (HERE/(name+'.stdout')).write_bytes(r.stdout);(HERE/(name+'.stderr')).write_bytes(r.stderr)
    row={'name':name,'command':command,'cwd':str(cwd.relative_to(HERE)),'exit_code':r.returncode,'elapsed_seconds':time.perf_counter()-start,'stdout_sha256':hashlib.sha256(r.stdout).hexdigest(),'stderr_sha256':hashlib.sha256(r.stderr).hexdigest(),'expected':'success' if expected==0 else 'rejection'}
    require(r.returncode==0 if expected==0 else r.returncode!=0,'unexpected process result: '+name)
    RECEIPTS.append(row);return r
def normalize(obj,volatile):
    if isinstance(obj,dict):return {k:normalize(v,volatile) for k,v in obj.items() if k not in volatile}
    if isinstance(obj,list):return [normalize(v,volatile) for v in obj]
    return obj
def verify_old_and_output_pins():
    baseline=json.loads((FINAL/'INPUT_PINS.json').read_text())['files']
    changes=json.loads((FINAL/'CHANGE_INVENTORY.json').read_text())
    mutable=set(changes['allowed_existing_mutations'])
    for row in baseline:
        if row['path'] not in mutable:
            require(record(AUDIT/row['path'])==row,'nonwhitelisted byte changed '+row['path'])
    finalpin=json.loads((FINAL/'OUTPUT_PINS.json').read_text())
    for row in finalpin['files']:
        p=FINAL/row['path'];r=record(p);r['path']=row['path'];require(r==row,'finalization output seal changed')
    for row in finalpin['final_audit_payload_files']:
        require(record(AUDIT/row['path'])==row,'final audit payload seal changed')
    return len(baseline),len(finalpin['files']),len(finalpin['final_audit_payload_files'])
def fresh_extraction(path):
    path.mkdir(parents=True)
    with zipfile.ZipFile(ARCHIVE) as z:
        require(z.testzip() is None,'CRC differs');z.extractall(path)
    return path/'publication' if PR==1034 else path
def refresh1034(root):
    pin=root/'PACKAGE_INPUT_PINS.json';obj=json.loads(pin.read_text())
    for row in obj['files']:
        p=root.parent/row['path'];row['bytes']=p.stat().st_size;row['sha256']=sha(p)
    save(pin,obj)
def faults():
    faultrows=[]
    for control in ['protected_paper','pending_state','nonzero_terminal','wrong_root_report']:
        root=fresh_extraction(HERE/'faults'/control)
        if control=='protected_paper':
            p=root/('research_note.tex' if PR==1034 else 'paper/forest_transfer_catalan.tex');p.write_bytes(p.read_bytes()+b'\n% administrative fault control\n')
        elif control=='pending_state':
            p=root/('evidence/CURRENT_REVIEW_STATE.json' if PR==1034 else 'CURRENT_REVIEW_STATE.json');obj=json.loads(p.read_text());obj['publication_ready']=False;save(p,obj)
        elif control=='nonzero_terminal':
            p=root/('evidence/package_02/VERDICT.json' if PR==1034 else 'evidence/whole_20261014/package_02/VERDICT.json');obj=json.loads(p.read_text());obj['severity_counts' if PR==1034 else 'issue_counts']['P3']=1;save(p,obj)
        else:
            p=root/('evidence/package_02/REPORT.md' if PR==1034 else 'evidence/whole_20261014/package_02/REPORT.md');p.write_bytes(p.read_bytes()+b'\nRoot-hash mismatch adversarial control.\n')
        # Refresh only scratch PR1034 candidate pins so terminal gates, rather than
        # merely the generic input-pin mismatch, must reject these mutations.
        if PR==1034:refresh1034(root)
        r=run('FAULT_'+control,[sys.executable,'-B','build_package.py' if PR==1034 else 'build_supportkit.py'],root,expected=1)
        text=r.stderr.decode()
        expected={'protected_paper':'protected reviewed' if PR==1034 else 'protected reviewed paper','pending_state':'terminal ready' if PR==1034 else 'accepted terminal ready','nonzero_terminal':'terminal review not zero' if PR==1034 else 'terminal actionable','wrong_root_report':'root accepted terminal record' if PR==1034 else 'root-adopted terminal'}[control]
        require(expected in text,'control did not hit intended explicit gate: '+control)
        faultrows.append({'control':control,'intended_gate':expected,'rejected':True,'scratch_only':True,'generic_input_pins_refreshed_to_force_specific_gate':PR==1034})
    return faultrows
def replay1034(root):
    out=[]
    for family,relative,file in [('degree_two','reviews/degree_two_01/checks','check_degree_two.py'),('degree_seven','reviews/degree_seven_01/artifacts','independent_wheel_check.py')]:
        source=root.parent/relative
        for optimized in [False,True]:
            target=HERE/'replay'/(family+('_O' if optimized else '_normal'));shutil.copytree(source,target)
            r=run(family+('_O' if optimized else '_normal'),[PYTHON,'-B']+(['-O'] if optimized else [])+[file],target)
            if family=='degree_two':
                actual=json.loads((target/'CHECK_RESULT.json').read_text());original=json.loads((source/'CHECK_RESULT.json').read_text())
                require(normalize(actual,{'utc'})==normalize(original,{'utc'}),'degree-two nonvolatile replay differs')
                out.append({'family':family,'optimized':optimized,'semantic_equal_to_packaged_output':True,'volatile_keys':['utc']})
            else:
                original=json.loads((source/'WHEEL_RESULT.json').read_text())
                require(json.loads(r.stdout)==normalize(original,{'checked_utc','normal_and_optimized_outputs_identical'}),'wheel mathematical payload replay differs')
                out.append({'family':family,'optimized':optimized,'semantic_equal_to_packaged_mathematical_output':True,'historical_receipt_only_keys':['checked_utc','normal_and_optimized_outputs_identical']})
    return out
def replay1037(root):
    out=[]
    for mode in ['symbolic','exterior','n4tree']:
        source=root/'evidence/fresh_20261013/transfer_01';target=HERE/'replay'/('transfer_'+mode);shutil.copytree(source,target)
        original=json.loads((source/('CHECK_RESULTS_'+mode+'.json')).read_text())
        run('transfer_'+mode,[PYTHON,'-B','fresh_checks.py','--mode',mode],target)
        actual=json.loads((target/('CHECK_RESULTS_'+mode+'.json')).read_text())
        a=[r for r in actual if r['name'] not in {'execution environment','complete'}]
        b=[r for r in original if r['name'] not in {'execution environment','complete'}]
        require(a==b,'transfer substantive replay differs '+mode)
        out.append({'family':'transfer','mode':mode,'ordinary_python_only':True,'substantive_records':len(a),'exact_equal':True})
    source=root/'evidence/fresh_20261013/invariant_01';target=HERE/'replay/invariant';shutil.copytree(source,target)
    run('invariant_all',[PYTHON,'-B','verify_invariants.py','--mode','all','--max-m','6','--max-n','7','--max-r','6','--output','NEW_RESULTS.json'],target)
    actual=json.loads((target/'NEW_RESULTS.json').read_text());original=json.loads((source/'CHECK_RESULTS.json').read_text())
    volatile={'elapsed_seconds','finished_utc','python','started_utc'}
    require(normalize(actual,volatile)==normalize(original,volatile),'invariant nonvolatile replay differs')
    out.append({'family':'invariant','ordinary_python_only':True,'nonvolatile_exact_equal':True,'volatile_keys':sorted(volatile)})
    return out
def main():
    require(PR in {1034,1037},'PR scope');require(not (HERE/'OUTPUT_PINS.json').exists(),'verification already sealed')
    now=datetime.datetime.now(datetime.timezone.utc).isoformat()
    save(HERE/'INPUT_PINS.json',{'utc':now,'files':[record(ARCHIVE),record(FINAL/'OUTPUT_PINS.json'),record(FINAL/'INPUT_PINS.json'),record(FINAL/'CHANGE_INVENTORY.json'),record(FINAL/'FINAL_SEAL.json'),record(FINAL/'FINAL_INTEGRITY.json')],'protected_finalizer_seals_are_unchanged':True})
    (HERE/'RESEARCH_LOG.md').write_text(f'# PR{PR} terminal command verification\n\n{now}: 15% of bounded command verification. Independently rechecking every input/output pin and explicit ready-builder control, then ordinary documented clean extraction/replay commands. No mathematical change, compiler or service action.\n')
    counts=verify_old_and_output_pins()
    root=fresh_extraction(HERE/'clean_extraction')
    run('CLEAN_BUILDER',[sys.executable,'-B','build_package.py' if PR==1034 else 'build_supportkit.py'],root)
    require((root/ARCHIVE.name).read_bytes()==ARCHIVE.read_bytes(),'documented clean builder byte mismatch')
    controls=faults()
    with (HERE/'RESEARCH_LOG.md').open('a') as out:out.write(f'\n{datetime.datetime.now(datetime.timezone.utc).isoformat()}: 65%. Independent all-file pin/custody checks pass; documented extracted builder reproduces exact ZIP. All four fault mutations rejected at intended explicit terminal gate. Documented arithmetic replay continues from copied extracted programs only.\n')
    replay=replay1034(root) if PR==1034 else replay1037(root)
    require(verify_old_and_output_pins()==counts,'custody count differs after replay')
    now=datetime.datetime.now(datetime.timezone.utc).isoformat()
    save(HERE/'VERIFICATION.json',{'utc':now,'pr':PR,'status':'PASS_ADMIN_ONLY_PARENT_ADOPTION_PENDING','original_input_files_rehashed':counts[0],'finalizer_output_files_rehashed':counts[1],'final_audit_payload_files_rehashed':counts[2],'archive':record(ARCHIVE),'clean_builder_byte_exact':True,'explicit_fault_controls':controls,'documented_finite_replays':replay,'process_receipts':RECEIPTS,'unchanged_pdf_not_recompiled':True,'historical_optimized_graph_comparator_replayed':False,'PR1037_optimized_graph_comparator_unsupported':True,'compiler_Git_index_branch_remote_services_outreach':False,'no_original_source_checker_report_or_sealed_finalizer_change':True})
    with (HERE/'RESEARCH_LOG.md').open('a') as out:out.write(f'\n{now}: 100% of bounded command verification; 95% of parent finalization pending root adoption. All four controls reject, all documented ordinary finite commands pass and match frozen nonvolatile/substantive outputs. Finalizer output seal/all protected bytes rechecked unchanged. Compiler intentionally not run for unchanged PDF.\n')
    (HERE/'REPORT.md').write_text(f'# PR{PR} separate terminal command verification\n\nPASS: documented clean extracted builder produces the identical final ZIP. Four scratch-only mutations (protected paper, readiness false, actionable terminal verdict, root-adopted report mismatch) reject at the intended explicit gate. PR1034 scratch input pins were refreshed before each rejection so the specific terminal gates were tested. Every baseline nonwhitelisted byte and every finalizer output/payload seal was independently rehashed unchanged before and after replay.\n\nDocumented finite programs ran from fresh extracted copies: {len(replay)} ordinary/allowed optimized executions, all matching frozen substantive or nonvolatile results. PR1037 historical graph comparator was run only under ordinary Python; its unsupported optimized mode remains expressly excluded. These executions check reproduction, without introducing a mathematical review or changing existing checker code/output. Detailed commands, timings, stdout/stderr hashes and comparisons are in VERIFICATION.json.\n\nNo compiler was run for the unchanged PDF. No Git, index, branch, remote, service or contact action occurred. The proposed finalizer seals remain untouched; parent root administrative adoption is pending, readiness is true and publication stays service-held at preceding PR1032.\n')
    outputs=[record(p) for p in sorted(HERE.iterdir()) if p.is_file() and p.name!='OUTPUT_PINS.json']
    save(HERE/'OUTPUT_PINS.json',{'utc':now,'self_excluded':True,'files':outputs,'private_scratch_extraction_replay_fault_trees_excluded':True,'scratch_outputs_pinned_by_process_receipts_and_comparison_results':True,'no_late_writes_after_seal':True})
    print(json.dumps({'pr':PR,'status':'PASS','documented_replays':len(replay),'explicit_faults':len(controls),'baseline_files':counts[0],'finalizer_outputs':counts[1]}))
if __name__=='__main__':main()
