#!/usr/bin/env python3
"""Actual current clean interfaces, full mathematics and guard regressions."""
import datetime, hashlib, json, os, shutil, subprocess, sys, zipfile
from pathlib import Path
sys.dont_write_bytecode=True
W=Path(__file__).resolve().parent; A=W.parents[1];D=A/'preprint_v1_0';S=W/'scratch';K=S/'clean_check/verification_kit'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def pins(root):return {p.relative_to(root).as_posix():{'bytes':p.stat().st_size,'sha256':sha(p)} for p in sorted(root.rglob('*')) if p.is_file() and not p.is_symlink() and not p.is_relative_to(W)}
def need(v,m):
    if not v:raise RuntimeError(m)
def dump(p,d):p.write_text(json.dumps(d,indent=2)+'\n')
receipt=W/'ACTUAL_COMMAND_RECEIPTS.jsonl';need(not receipt.exists(),'Never erase an actual attempt')
S.mkdir();(S/'temp').mkdir();env=dict(os.environ,TMPDIR=str(S/'temp'),PYTHONDONTWRITEBYTECODE='1')
canonical=pins(A)
with zipfile.ZipFile(D/'verification_kit.zip') as z:z.extractall(S/'clean_check')
initial={p.relative_to(K).as_posix():sha(p) for p in K.rglob('*') if p.is_file()};rows=[]
def run(label,args,cwd=K,success=True,needle=None):
    started=datetime.datetime.now(datetime.timezone.utc).isoformat()
    r=subprocess.run([str(x) for x in args],cwd=cwd,env=env,capture_output=True,text=True,timeout=300)
    row={'utc':started,'label':label,'argv':[str(x) for x in args],'cwd':str(cwd),'expected_success':success,'returncode':r.returncode,'stdout':r.stdout,'stderr':r.stderr,'free_bytes_after':shutil.disk_usage(W).free}
    with receipt.open('a') as f:f.write(json.dumps(row)+'\n')
    rows.append(row);need((r.returncode==0)==success,'Actual command failed '+label+' '+r.stderr[-1200:])
    if needle:need(needle in r.stderr,'Wrong actual rejection '+label)
    return r
for opt in [False,True]:
    prefix=[sys.executable,'-B','-I']+(['-O'] if opt else [])
    run('default current verifier',prefix+['verify.py']);run('full portable adapters',prefix+['run_checks.py'])
    run('complete mathematical and custody fault suite',prefix+['fault_checks.py'])
    run('full mathematical JSON capture',prefix+[W/'fullmath_capture.py'])
    run('strict required external binding',prefix+['verify.py','--require-binding','--binding',D/'EXTERNAL_BINDING.json','--pdf',D/'preprint.pdf','--archive',D/'verification_kit.zip'])
    run('independent finite mechanisms',prefix+[A/'reviews/package_03/independent_checks03.py'])
    for fault,needle in [('omit_conjugates','Independent insertion identity'),('wrong_parity','Independent mod-2 alternation')]:run('independent injected '+fault,prefix+[A/'reviews/package_03/independent_checks03.py',fault],success=False,needle=needle)
    output=S/('rebuilt-O.zip' if opt else 'rebuilt.zip');run('fresh external deterministic rebuild',prefix+['build_archive.py','--output',output]);need(sha(output)==sha(D/'verification_kit.zip'),'Rebuild differs')
    # Preserve exact output pin before removing only this owned rebuild.
    with (W/'OWNED_EARLY_CLEANUP.jsonl').open('a') as f:f.write(json.dumps({'path':str(output),'bytes':output.stat().st_size,'sha256':sha(output),'reason':'Remove only owned temporary rebuild after exact delivered-ZIP comparison.'})+'\n')
    output.unlink()
run('complete output guards with internal normal and optimized cases',[sys.executable,'-B','-I',K/'output_guard_checks.py'])
run('independent semantic guard regressions both modes',[sys.executable,'-B','-I',W/'semantic_regressions.py'],cwd=W)
run('actual repository native uploader LOCAL check',[sys.executable,'-B',A.parents[2]/'zenodo_deposit_tool/zenodo.py','check',D/'deposit_metadata.json'],cwd=A.parents[2])
need({p.relative_to(K).as_posix():sha(p) for p in K.rglob('*') if p.is_file()}==initial,'Extracted kit changed')
need(pins(A)==canonical,'Canonical files changed during reproduction')
need((W/'FULL_MATHEMATICAL_OUTPUT_COMPARISON.json').read_bytes()==(W/'FULL_MATHEMATICAL_OUTPUT_COMPARISON_O.json').read_bytes(),'Normal/-O full mathematics differs')
guard=json.loads(next(r['stdout'] for r in rows if r['label'].startswith('complete output guards')))
semantic=json.loads((W/'INDEPENDENT_SEMANTIC_RESULTS.json').read_text())
need(guard['status']=='PASS' and semantic['status']=='PASS','Guard summaries')
dump(W/'REPRODUCTION_SUMMARY.json',{'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS','actual_driver_commands':len(rows),'canonical_files_unchanged':len(canonical),'extracted_files_unchanged':len(initial),'normal_optimized_full_math_identical':True,'full_math_identical_to_adopted_whole03':True,'guard_rejections':guard['rejection_count'],'guard_protected_files':guard['protected_file_count'],'physical_case_rejections':sum(r.get('fault','').startswith('physical-case') for r in guard['rejections']),'independent_semantic_commands':semantic['actual_commands'],'local_native_uploader_check_passed':True,'new_compile_render_or_view':False,'publication_ready':False,'issues_resolved':False,'published':False,'services_held_at':1032})
print(json.dumps(json.loads((W/'REPRODUCTION_SUMMARY.json').read_text()),indent=2))
