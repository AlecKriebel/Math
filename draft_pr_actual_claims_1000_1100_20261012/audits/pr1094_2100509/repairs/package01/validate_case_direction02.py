"""Supplement: invoke scripts through case aliases, target canonical case."""
from pathlib import Path
import datetime, hashlib, json, shutil, subprocess, sys, zipfile
sys.dont_write_bytecode=True
R=Path('/Users/alec/Documents/Math/draft_pr_actual_claims_1000_1100_20261012/audits/pr1094_2100509/repairs/package01')
A=R.parent.parent;P=A/'preprint_v1_0';T=R/'tmp'
def need(ok,msg):
    if not ok:raise ValueError(msg)
def sha(b):return hashlib.sha256(b).hexdigest()
def pins(root):
    return {p.relative_to(root).as_posix():sha(p.read_bytes()) for p in root.rglob('*') if p.is_file() and not p.is_symlink()}
def main():
    root=T/'kitroot'
    if T.exists():
        need(pins(root)==pins(P/'kit'),'resumed disposable extraction differs from canonical kit')
    else:
        root.mkdir(parents=True)
        with zipfile.ZipFile(P/'pr1094_supportkit_v1.0.zip') as archive:archive.extractall(root)
    before=pins(root);rows=[]
    for optimized in (False,True):
        py=[sys.executable,'-B']+(['-O'] if optimized else [])
        for alias_name in ('KITROOT','KiTrOoT'):
            alias=root.with_name(alias_name)
            need(alias.samefile(root),'case-alias premise not supplied by actual filesystem')
            for script,flag in (('run_checks.py','--out'),('build_support.py','--out'),('build_pdf.py','--out-dir')):
                target=root/'absent1'/'absent2'/'fresh'
                args=py+[str(alias/'scripts'/script),flag,str(target)]
                done=subprocess.run(args,cwd=root,capture_output=True)
                need(done.returncode!=0 and (b'output physically overlaps protected kit' in done.stderr or b'output overlaps protected kit' in done.stderr),'reverse-case alias was not rejected')
                need(pins(root)==before and not (root/'absent1').exists(),'reverse-case test changed protected input')
                rows.append({'optimized':optimized,'argv':args,'exit':done.returncode,
                    'script_root_alias':str(alias),'output_root':str(root),'samefile_premise':True,
                    'stdout':done.stdout.decode(errors='replace'),'stderr':done.stderr.decode(errors='replace'),
                    'stdout_sha256':sha(done.stdout),'stderr_sha256':sha(done.stderr)})
    cleanup=[{'path':p.relative_to(R).as_posix(),'bytes':p.stat().st_size,'sha256':sha(p.read_bytes())}
             for p in sorted(T.rglob('*')) if p.is_file() and not p.is_symlink()]
    report={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS',
        'scope':'Additional direction: script/ROOT invoked through uppercase or mixed-case aliases; output uses lower-case canonical protected tree and two absent intermediate components.',
        'commands':rows,'command_count':len(rows),'expected_rejections':len(rows),
        'ordinary_optimized_all_three_writers':True,'all_case_identity_premises_actually_samefile':True,
        'protected_extraction_unchanged':True,'new_compile_or_render':False,'services_performed':False}
    (R/'CASE_DIRECTION_SUPPLEMENT.json').write_text(json.dumps(report,indent=2)+'\n')
    shutil.rmtree(T)
    (R/'OWN_CASE_SUPPLEMENT_CLEANUP.json').write_text(json.dumps({'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'records':cleanup,'only_own_tmp_removed':True},indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k!='commands'},indent=2))
if __name__=='__main__':main()
