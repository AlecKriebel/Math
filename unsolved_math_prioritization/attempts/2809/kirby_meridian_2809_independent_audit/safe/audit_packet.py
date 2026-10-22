#!/usr/bin/env python3
"""Read-only audit of the pinned author archive; mutations occur only in temp copies."""
import argparse, ast, hashlib, json, os, shutil, subprocess, sys, tempfile, zipfile
from pathlib import Path, PurePosixPath

PIN='14809993ffccbb97cc3510d7a17df91ad375bc85cf02bd6a9c430c31c12673c3'
NAMES={'LITERATURE.md','MANIFEST.json','PROOFS.md','README.md','RESEARCH_LOG.md',
       'RESULTS.json','SOURCE_VERIFICATION.json','verify.py'}
H=lambda b:hashlib.sha256(b).hexdigest()

def need(ok,label):
    if not ok:raise RuntimeError(label)

def manifest(root):
    items=json.loads((root/'MANIFEST.json').read_text())['files']
    actual={p.name for p in root.iterdir() if p.is_file() and p.name!='MANIFEST.json'}
    need(len(items)==len({e['path'] for e in items}),'duplicate manifest paths')
    need(actual=={e['path'] for e in items},'manifest membership')
    for e in items:
        need(PurePosixPath(e['path']).name==e['path'],'manifest path')
        b=(root/e['path']).read_bytes()
        need(len(b)==e['bytes'] and H(b)==e['sha256'],'manifest bytes: '+e['path'])

def refresh(root):
    d=json.loads((root/'MANIFEST.json').read_text())
    for e in d['files']:
        b=(root/e['path']).read_bytes();e.update(bytes=len(b),sha256=H(b))
    (root/'MANIFEST.json').write_text(json.dumps(d))

def execute(root,opt):
    env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1')
    p=subprocess.run([sys.executable,*(['-O'] if opt else []),str(root/'verify.py')],
                     cwd=root.parent,capture_output=True,env=env,timeout=30)
    return p.returncode,p.stdout

def main():
    a=argparse.ArgumentParser();a.add_argument('archive',type=Path);a.add_argument('--author-directory',type=Path)
    args=a.parse_args();raw=args.archive.read_bytes();need(H(raw)==PIN,'archive pin mismatch')
    report={'problem_id':2809,'author_zip_bytes':len(raw),'author_zip_sha256':H(raw),
            'original_untouched':True,'ordinary_and_optimized':[], 'integrity_mutations':[],
            'semantic_mutations':[],'documented_guard_limits':[]}
    with tempfile.TemporaryDirectory(prefix='meridian_audit_') as tmp:
        base=Path(tmp);target=base/'renamed'/'unrelated';target.mkdir(parents=True)
        with zipfile.ZipFile(args.archive) as z:
            members=z.infolist();expected={'kirby_meridian_2809/'+n for n in NAMES}
            need(len(members)==8 and {x.filename for x in members}==expected,'archive exact membership')
            need(z.testzip() is None,'ZIP CRC')
            for x in members:
                need(not x.is_dir() and ((x.external_attr>>16)&0o170000)!=0o120000,'nonregular archive member')
                (target/PurePosixPath(x.filename).name).write_bytes(z.read(x))
        manifest(target)
        need(not any(isinstance(n,ast.Assert) for n in ast.walk(ast.parse((target/'verify.py').read_text()))),'assert guard found')
        if args.author_directory:
            need({p.name for p in args.author_directory.iterdir() if p.is_file()}==NAMES,'author directory membership')
            for n in NAMES:need((target/n).read_bytes()==(args.author_directory/n).read_bytes(),'original/archive byte mismatch')
            report['all_live_author_files_match_archive']=True
        result=(target/'RESULTS.json').read_bytes()
        for optimized in (False,True):
            rc,out=execute(target,optimized);need(rc==0 and out==result,'author replay mismatch')
            report['ordinary_and_optimized'].append({'optimized':optimized,'exit_code':rc,'exact_results_match':True,'checks':json.loads(out)['total_checks']})
        for change in ('corrupt_proof','extra_file','missing_proof','corrupt_saved_results'):
            mutant=base/change;shutil.copytree(target,mutant)
            if change=='corrupt_proof':
                with (mutant/'PROOFS.md').open('ab') as f:f.write(b'\ncorruption\n')
            if change=='extra_file':(mutant/'UNEXPECTED.txt').write_text('audit-only mutation')
            if change=='missing_proof':(mutant/'PROOFS.md').unlink()
            if change=='corrupt_saved_results':(mutant/'RESULTS.json').write_text('{}\n')
            for optimized in (False,True):
                rc,_=execute(mutant,optimized);need(rc!=0,'integrity mutation undetected')
                report['integrity_mutations'].append({'mutation':change,'optimized':optimized,'rejected':True})
        mutations={
          'drop_sign_guard':('if d < 0 or d*d < 4*r:','if d*d < 4*r:'),
          'drop_second_cap_square':('d = n*n*B*B - P*P - Q*Q','d = n*n*B*B - P*P'),
          'double_determinant_scaling':('r = P*P*Q*Q - n*n*A0*A0','r = P*P*Q*Q - n**4*A0*A0'),
          'max_instead_of_sum_caps':('F(p[i]+p[j], abs(a[i]-a[j]))','F(max(p[i],p[j]), abs(a[i]-a[j]))'),
          'equality_reported_strict':("return 'strict' if d*d > 4*r else 'at_most'","return 'strict' if d*d >= 4*r else 'at_most'"),
          'impossible_active_guard':('def algebra_controls():','def algebra_controls():\n    require(False, "injected_active_guard")')}
        for name,(old,new) in mutations.items():
            mutant=base/name;shutil.copytree(target,mutant);p=mutant/'verify.py';s=p.read_text()
            need(s.count(old)==1,'mutation does not uniquely select code: '+name)
            p.write_text(s.replace(old,new));refresh(mutant) # Isolate semantic detection from hash detection.
            for optimized in (False,True):
                rc,_=execute(mutant,optimized);need(rc!=0,'semantic mutation undetected: '+name)
                report['semantic_mutations'].append({'mutation':name,'optimized':optimized,'manifest_recomputed':True,'rejected':True})
        for name in ('absent_manifest','extra_nested_file'):
            mutant=base/name;shutil.copytree(target,mutant)
            if name=='absent_manifest':(mutant/'MANIFEST.json').unlink()
            else:
                (mutant/'nested').mkdir();(mutant/'nested'/'UNEXPECTED.txt').write_text('audit-only mutation')
            modes=[]
            for optimized in (False,True):
                rc,out=execute(mutant,optimized);modes.append({'optimized':optimized,'exit_code':rc,'results_unchanged':out==result})
            report['documented_guard_limits'].append({'condition':name,'runs':modes,
                'interpretation':'The author verifier is not a mandatory recursive archive guard. The independent exact ZIP-member check covers the frozen archive.'})
    need(H(args.archive.read_bytes())==PIN,'archive changed during audit')
    report.update(status='PASS_WITH_DOCUMENTED_GUARD_LIMITS',python_assert_guards=0,
                  author_algebra_checks=10768,independent_archive_membership_check=True,
                  full_conjecture_certified=False)
    print(json.dumps(report,indent=2,sort_keys=True))
if __name__=='__main__':main()
