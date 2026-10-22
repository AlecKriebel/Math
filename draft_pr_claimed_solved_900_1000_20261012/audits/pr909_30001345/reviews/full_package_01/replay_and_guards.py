#!/usr/bin/env python3
"""Fresh reviewer-controlled replay/negative controls, outside the candidate.

Run with trusted Python -I -B. Each actual copy is independently authenticated
before code execution. Reanchored malformed manifests are deliberate parser
tests, never represented as authentic releases. Fixtures remain private in tmp/.
"""
from pathlib import Path
import argparse, hashlib, importlib.util, json, os, shutil, subprocess, sys, tempfile

HERE=Path(__file__).absolute().parent
ROOT=HERE.parent.parent
PIN='0189e0ecd7bb39a1ed3899ee785cfc9f48bae7fdf386cd3002fd0a4849b70313'
ZIP_PIN='291becf72ccd6345701711ab8523cf0966b042ce147e907cefdeb4bece014fd0'
PACK=HERE/'tmp/extracted'
PYTHON=Path(sys.executable)
def require(ok,label):
    if not ok:raise RuntimeError(label)
def sha(b):return hashlib.sha256(b).hexdigest()
def authenticate(p):
    raw=(p/'PACKAGE_MANIFEST.json').read_bytes();require(sha(raw)==PIN,'external manifest')
    m=json.loads(raw);files=m['files']
    actual={x.relative_to(p).as_posix() for x in p.rglob('*') if x.is_file()}
    require(actual==set(files)|{'PACKAGE_MANIFEST.json'},'own exact file inventory')
    for n,x in files.items():
        b=(p/n).read_bytes();require(len(b)==x['bytes'] and sha(b)==x['sha256'],'own payload: '+n)
def env(opt=None):
    e=dict(os.environ,PYTHONDONTWRITEBYTECODE='1')
    for n in ('PYTHONOPTIMIZE','PYTHONPATH','PYTHONHOME'):e.pop(n,None)
    if opt:e['PYTHONOPTIMIZE']=opt
    return e
def invoke(p,flags=(),args=(),opt=None,limit=30):
    return subprocess.run([str(PYTHON),'-B',*flags,str(p/'verify_package.py'),*map(str,args)],
        cwd=HERE/'tmp',env=env(opt),capture_output=True,text=True,timeout=limit)
def load_module(path,name):
    spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--output',type=Path,default=HERE/'REPLAY_AND_GUARDS.json')
    args=ap.parse_args()
    require(sys.flags.optimize==0 and sys.flags.isolated==1,'review harness must be isolated and normal')
    require(sha((ROOT/'publication/rough-m-arrangements-source-verification-v1.0.zip').read_bytes())==ZIP_PIN,'archive pin')
    authenticate(PACK)
    result={'status':'PASS','package_manifest_sha256':PIN,'full_replays':[],'negative_controls':[]}
    with tempfile.TemporaryDirectory(dir=HERE/'tmp',prefix='independent_controls_') as td:
        work=Path(td)
        copy=work/'authenticated package [spaces]';shutil.copytree(PACK,copy);authenticate(copy)
        outputs=[]
        for label,flags,opt in [('normal',[],None),('O',['-O'],None),('OO',['-OO'],None),('environment2',[],'2')]:
            p=invoke(copy,flags,['--expected-manifest',PIN,'--pdf',ROOT/'publication/output/pdf/note.pdf','--workdir',work/'replays'],opt,180)
            require(p.returncode==0,label+' full replay failed: '+p.stderr)
            o=json.loads(p.stdout);require(o['status']=='PASS' and o['worker_optimization']==0,'worker result')
            require(all(x['optimization']==0 and x['isolated']==1 for x in o['child_execution_guards']),'child guards')
            outputs.append(o);result['full_replays'].append({'outer_mode':label,'status':'PASS','worker_optimization':0,'all4_child_guards_pass':True,'result_sha256':sha(p.stdout.encode())})
        require(all(o==outputs[0] for o in outputs),'same results in all modes');authenticate(copy)
        def record(label,p):
            require(p.returncode!=0,label+' wrongly accepted');result['negative_controls'].append({'case':label,'rejected':True,'exit_code':p.returncode,'diagnostic_sha256':sha(p.stderr.encode())})
        def edit_manifest(p,fn):
            f=p/'PACKAGE_MANIFEST.json';m=json.loads(f.read_bytes());fn(m);f.write_text(json.dumps(m));return sha(f.read_bytes())
        tests=[
          ('schema_float',lambda p:edit_manifest(p,lambda m:m.update(schema_version=1.0))),
          ('pr_float',lambda p:edit_manifest(p,lambda m:m.update(pr=909.0))),
          ('length_float',lambda p:edit_manifest(p,lambda m:m['files']['note.tex'].update(bytes=float(m['files']['note.tex']['bytes'])))),
          ('self_list',lambda p:edit_manifest(p,lambda m:m['files'].update({'PACKAGE_MANIFEST.json':m['files']['note.tex']}))),
          ('wrong_original_head',lambda p:edit_manifest(p,lambda m:m.update(original_pr_head='f'*40))),
          ('unlisted_empty_directory',lambda p:(p/'unlisted').mkdir()),
          ('missing_note',lambda p:(p/'note.tex').unlink()),
          ('symbolic_directory',lambda p:(p/'unlisted-link').symlink_to(copy/'reviews',target_is_directory=True)),
          ('manifest_fifo',lambda p:((p/'PACKAGE_MANIFEST.json').unlink(),os.mkfifo(p/'PACKAGE_MANIFEST.json'))),
          ('payload_tamper',lambda p:(p/'note.tex').write_text('False note.\n')),
        ]
        for label,change in tests:
            fixture=work/'fixture';shutil.copytree(PACK,fixture);authenticate(fixture)
            returned=change(fixture);pin=returned if type(returned) is str and len(returned)==64 else PIN
            record(label,invoke(fixture,['-OO'],['--expected-manifest',pin,'--integrity-only'],limit=8));shutil.rmtree(fixture)
        for label,new in [('duplicate_key','{"pr":909,'),('nonfinite_key','{"unused":NaN,')]:
            fixture=work/'fixture';shutil.copytree(PACK,fixture);authenticate(fixture)
            p=fixture/'PACKAGE_MANIFEST.json';p.write_text(p.read_text().replace('{',new,1));pin=sha(p.read_bytes())
            record(label,invoke(fixture,args=['--expected-manifest',pin,'--integrity-only']));shutil.rmtree(fixture)
        record('wrong_external_anchor',invoke(copy,args=['--expected-manifest','0'*64,'--integrity-only']))
        record('full_replay_missing_external_anchor',invoke(copy,args=['--workdir',work/'noanchor']))
        record('workdir_inside_package',invoke(copy,args=['--expected-manifest',PIN,'--workdir',copy/'bad-work']))
        fake=work/'wrong.pdf';fake.write_bytes(b'%PDF-wrong')
        record('separate_pdf_mismatch',invoke(copy,args=['--expected-manifest',PIN,'--integrity-only','--pdf',fake]))
        fake.unlink();fake.symlink_to(copy/'note.pdf')
        record('separate_pdf_symlink',invoke(copy,args=['--expected-manifest',PIN,'--integrity-only','--pdf',fake]))
        # Test the reviewed functions on an authenticated copy, then deliberately
        # corrupt one post-copy mathematical checker rather than its wrapper.
        authenticate(copy);m=load_module(copy/'verify_package.py','review_copy_guard')
        for actual,expected,label in [(True,1,'bool_int'),(1.0,1,'float_int'),({'x':1},{'x':True},'nested_type')]:
            try:m.equivalent(actual,expected)
            except RuntimeError:result['negative_controls'].append({'case':'strict_result_'+label,'rejected':True})
            else:raise RuntimeError('strict result mismatch accepted')
        marker=work/'must-not-execute';original=m.shutil.copytree
        def corrupt(source,dest,*a,**kw):
            out=original(source,dest,*a,**kw)
            if Path(dest).name=='package':
                (Path(dest)/'reviews/invariant_family/verify_invariants.py').write_text('from pathlib import Path\nPath('+repr(str(marker))+').write_text("executed")\n')
            return out
        m.shutil.copytree=corrupt
        try:
            try:m.worker(copy,PIN,work)
            except RuntimeError as exc:require('Payload fingerprint mismatch' in str(exc),'wrong copy failure')
            else:raise RuntimeError('corrupted actual checker copy accepted')
        finally:m.shutil.copytree=original
        require(not marker.exists(),'corrupted checker executed')
        result['negative_controls'].append({'case':'postcopy_mathematical_checker_corruption','rejected_before_execution':True,'marker_created':False})
        false=work/'false.py';false.write_text('assert False, "reviewer deliberate failure"\nprint("UNSAFE_PASS")\n')
        p=subprocess.run([str(PYTHON),'-I','-B',str(copy/'run_checked.py'),str(false)],env=env('2'),cwd=work,capture_output=True,text=True,timeout=8)
        require(p.returncode!=0 and 'AssertionError' in p.stderr and 'UNSAFE_PASS' not in p.stdout,'assert active')
        g=json.loads(p.stderr.splitlines()[0]);require(g['child_optimization']==0 and g['child_isolated']==1,'assert child flags')
        result['negative_controls'].append({'case':'deliberate_false_assertion_inherited_environment2','rejected':True,'child_optimization':0,'child_isolated':1})
        authenticate(copy)
        require(not list(copy.rglob('*.pyc')) and not list(copy.rglob('__pycache__')),'copy created bytecode')
    authenticate(PACK)
    result.update(all_full_replay_results_identical=True,negative_control_count=len(result['negative_controls']),
      candidate_bytes_unchanged=True,bytecode_created_in_authenticated_package=False,
      limits='Trusted runtime/OS/dependencies/SHA256; no sandbox, signature, concurrent hostile replacement protection, formal proof or priority certification. Schema fixtures intentionally use recalculated anchors only to reach parser checks.')
    args.output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'status':result['status'],'full_replays':len(result['full_replays']),'negative_controls':len(result['negative_controls'])}))
if __name__=='__main__':main()
