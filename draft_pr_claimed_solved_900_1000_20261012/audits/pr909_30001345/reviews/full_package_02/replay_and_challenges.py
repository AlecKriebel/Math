"""Reviewer02 full replay and additional operative-boundary countercontrols."""
import argparse,hashlib,importlib.util,json,os,shutil,subprocess,sys
from pathlib import Path

R=Path(__file__).absolute().parent
ROOT=R/'private/extracted'
PIN='0189e0ecd7bb39a1ed3899ee785cfc9f48bae7fdf386cd3002fd0a4849b70313'
PY=Path('/Users/alec/Documents/Math/draft_pr_claimed_solved_900_1000_20261012/audits/pr906_30006419/reviews/computation_family/tmp/venv/bin/python')
def need(c,s):
    if not c:raise RuntimeError(s)
def sha(b):return hashlib.sha256(b).hexdigest()
def main(output):
    work=R/'private/replay_work';work.mkdir(exist_ok=True)
    need(sha((ROOT/'PACKAGE_MANIFEST.json').read_bytes())==PIN,'external anchor')
    outputs=[];rows=[]
    for mode,flags,op in [('normal',[],None),('O',['-O'],None),('OO',['-OO'],None),('env2',[],'2')]:
        env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1');env.pop('PYTHONOPTIMIZE',None)
        if op:env['PYTHONOPTIMIZE']=op
        p=subprocess.run([str(PY),*flags,'-B',str(ROOT/'verify_package.py'),'--expected-manifest',PIN,'--pdf',str(ROOT/'note.pdf'),'--workdir',str(work)],cwd=work,env=env,capture_output=True,text=True,timeout=900)
        (R/'private'/f'replay_{mode}.stdout').write_text(p.stdout);(R/'private'/f'replay_{mode}.stderr').write_text(p.stderr)
        need(p.returncode==0,mode+': '+p.stderr);v=json.loads(p.stdout);need(v['status']=='PASS' and v['worker_optimization']==0,'normal worker')
        outputs.append(p.stdout);rows.append({'mode':mode,'output_sha256':sha(p.stdout.encode()),'result':v})
        print('full replay',mode,'PASS',flush=True)
    need(len(set(outputs))==1,'same output')
    spec=importlib.util.spec_from_file_location('v02',ROOT/'verify_package.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
    negatives=[]
    def rejects(name,f):
        try:f()
        except Exception as e:negatives.append({'case':name,'rejected':True,'exception':type(e).__name__,'reason':str(e)[:160]});return
        raise RuntimeError('accepted negative: '+name)
    for raw in [b'{"pr":909,"pr":909}',b'{"x":NaN}',b'{"x":Infinity}',b'{"x":-Infinity}']:
        rejects('strict_json_'+raw.decode(),lambda raw=raw:m.strict_json(raw))
    for a,b in [(True,1),(1.0,1),([{'x':False}],[{'x':0}]),({'x':1},{'x':1.0}),([1],[1,2]),({'a':1},{'b':1})]:
        rejects('exact_result_types_'+repr((a,b)),lambda a=a,b=b:m.equivalent(a,b))
    m.equivalent({'x':[1,True,None,'1']},{'x':[1,True,None,'1']})
    # Reanchored structural mutations reach each validation boundary instead of
    # being rejected trivially by the original external manifest hash.
    fixture=R/'private/fixture';shutil.copytree(ROOT,fixture,dirs_exist_ok=True)
    raw=(fixture/'PACKAGE_MANIFEST.json').read_bytes()
    for name,change in [('float_pr',lambda d:d.update(pr=909.0)),('bool_bytes',lambda d:d['files']['note.tex'].update(bytes=True)),('float_schema',lambda d:d.update(schema_version=1.0)),('wrong_head',lambda d:d.update(original_pr_head='0'*40)),('negative_length',lambda d:d['files']['note.tex'].update(bytes=-1)),('case_hash',lambda d:d['files']['note.tex'].update(sha256=d['files']['note.tex']['sha256'].upper()))]:
        d=json.loads(raw);change(d);b=(json.dumps(d)+'\n').encode();(fixture/'PACKAGE_MANIFEST.json').write_bytes(b)
        rejects(name,lambda b=b:m.validate(fixture,sha(b)))
    (fixture/'PACKAGE_MANIFEST.json').write_bytes(raw)
    # A reanchored malicious original proof still cannot redefine historical
    # identity: rewrite the original manifest payload as well as its outer map.
    original=fixture/'original_packet/PACKAGE_MANIFEST.json';old=original.read_bytes();original.write_bytes(old+b' ')
    d=json.loads(raw);d['files']['original_packet/PACKAGE_MANIFEST.json']={'bytes':len(old)+1,'sha256':sha(old+b' ')};b=json.dumps(d).encode();(fixture/'PACKAGE_MANIFEST.json').write_bytes(b)
    rejects('reanchored_original_manifest_still_hits_fixed_pin',lambda:m.validate(fixture,sha(b)))
    original.write_bytes(old);(fixture/'PACKAGE_MANIFEST.json').write_bytes(raw)
    rejects('bad_external_pin',lambda:m.validate(fixture,'0'*64))
    (fixture/'empty_extra').mkdir();rejects('extra_empty_directory',lambda:m.validate(fixture,PIN))
    (fixture/'empty_extra').rmdir()
    fifo=fixture/'fifo';os.mkfifo(fifo);rejects('FIFO_nonblocking',lambda:m.validate(fixture,PIN));fifo.unlink()
    link=fixture/'note.pdf';save=link.read_bytes();link.unlink();link.symlink_to(ROOT/'note.pdf');rejects('symlink_payload',lambda:m.validate(fixture,PIN));link.unlink();link.write_bytes(save)
    m.validate(fixture,PIN)
    # Corrupt actual COPIED mathematical verifier (not the wrapper), with a
    # marker proving no injected code ran. Controlled import in isolated child.
    harness=R/'private/copied_math_boundary.py';harness.write_text('''import importlib.util,json,sys\nfrom pathlib import Path\nr=Path(sys.argv[1]);w=Path(sys.argv[2]);pin=sys.argv[3];marker=w/"executed"\ns=importlib.util.spec_from_file_location("v",r/"verify_package.py");m=importlib.util.module_from_spec(s);s.loader.exec_module(m)\nc=m.shutil.copytree\ndef copy(a,b,*args,**kwargs):\n z=c(a,b,*args,**kwargs)\n if Path(b).name=="package":(Path(b)/"reviews/invariant_family/verify_invariants.py").write_text("from pathlib import Path\\nPath("+repr(str(marker))+").write_text(\\"BAD\\")\\n")\n return z\nm.shutil.copytree=copy\ntry:m.worker(r,pin,w)\nexcept RuntimeError as e:\n if "Payload fingerprint mismatch: reviews/invariant_family/verify_invariants.py" not in str(e):raise\nelse:raise RuntimeError("not rejected")\nif marker.exists():raise RuntimeError("executed injected math")\nprint(json.dumps({"status":"PASS","copied_math_rejected_before_execution":True,"marker_created":False}))\n''')
    p=subprocess.run([str(PY),'-I','-B',str(harness),str(ROOT),str(work),PIN],cwd=work,capture_output=True,text=True,timeout=30);need(p.returncode==0,p.stderr);copy_result=json.loads(p.stdout)
    # False assertion under real inherited optimization still runs normally
    # once the wrapper is launched with -I.
    false=R/'private/false_assert.py';false.write_text('assert False, "review02 false math"\nprint("UNSAFE_PASS")\n')
    env=dict(os.environ,PYTHONOPTIMIZE='2');p=subprocess.run([str(PY),'-I','-B',str(ROOT/'run_checked.py'),str(false)],env=env,capture_output=True,text=True,timeout=10)
    need(p.returncode!=0 and 'AssertionError' in p.stderr and 'UNSAFE_PASS' not in p.stdout,'active false assertion')
    result={'status':'PASS','full_modes':rows,'outputs_identical':True,'reviewer_negative_cases':len(negatives),'negative_controls':negatives,'actual_copied_math_boundary':copy_result,'inherited_optimize_false_assertion_rejected':True,'finite_controls_not_analytic_or_priority_proof':True}
    output.write_text(json.dumps(result,indent=2)+'\n')
    print('additional challenges',len(negatives),'PASS',flush=True)
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,default=R/'REPLAY_AND_CHALLENGES.json');args=ap.parse_args();main(args.output)
