#!/usr/bin/env python3
"""Fixed external-bootstrap attacks and parser controls, all optimization modes."""
from pathlib import Path
import copy,hashlib,json,os,shutil,subprocess,sys,tempfile

def need(x,m):
    if not x:raise RuntimeError(m)
def sha(b):return hashlib.sha256(b).hexdigest()
def main():
    need(len(sys.argv)==2,'usage: TEST_MUTATIONS.py PACKET');root=Path(sys.argv[1]).absolute();bootstrap=root/'BOOTSTRAP.py'
    modes=[('normal',[]),('O',['-O']),('OO',['-OO'])];results=[]
    before={str(p.relative_to(root)):sha(p.read_bytes()) for p in root.rglob('*') if p.is_file()}
    def run(mode,target,cwd=None,env=None,args=()):
        p=subprocess.run([sys.executable,'-I','-S','-B',*mode,str(bootstrap),str(target),'--integrity-only',*args],cwd=cwd,env=env,capture_output=True,timeout=30)
        return {'exit_code':p.returncode,'stdout':p.stdout.decode(),'stderr':p.stderr.decode()}
    def record(name,label,r,accepted):
        need((r['exit_code']==0 and r['stderr']=='') if accepted else (r['exit_code']==1 and r['stderr'].startswith('REJECT: ') and 'Traceback' not in r['stderr']),'wrong outcome: '+name)
        results.append({'case':name,'mode':label,'expected':'PASS' if accepted else 'REJECT','passed':True,**r})
    with tempfile.TemporaryDirectory(prefix='hexagon-fixed-controls-') as td:
        temp=Path(td)
        for label,flags in modes:record('baseline',label,run(flags,root),True)
        attacks=['report','audit','native-checker','manifest','verifier','bootstrap','missing-file','extra-file','extra-empty-directory','symlink-file','symlink-directory','fifo','refreshed-whole-attacker-package','optional-in-integrity','one-corpus-only']
        for name in attacks:
            d=temp/name;shutil.copytree(root,d)
            for p in [d,*d.rglob('*')]:p.chmod(0o755 if p.is_dir() else 0o644)
            target={'report':'author/REPORT.md','audit':'audit/AUDIT.md','native-checker':'author/check_geometry.py','manifest':'PUBLICATION_MANIFEST.json','verifier':'VERIFY_PUBLICATION.py','bootstrap':'BOOTSTRAP.py'}.get(name)
            args=[]
            if target:
                p=d/target;p.write_bytes(p.read_bytes()+b'\n# changed\n')
            elif name=='missing-file':(d/'author/fixtures.json').unlink()
            elif name=='extra-file':(d/'unexpected.txt').write_text('unexpected')
            elif name=='extra-empty-directory':(d/'unexpected').mkdir()
            elif name=='symlink-file':
                p=d/'author/fixtures.json';p.unlink();p.symlink_to(root/'author/fixtures.json')
            elif name=='symlink-directory':shutil.rmtree(d/'audit');(d/'audit').symlink_to(root/'audit',target_is_directory=True)
            elif name=='fifo':os.mkfifo(d/'unexpected-fifo')
            elif name=='refreshed-whole-attacker-package':
                p=d/'author/REPORT.md';p.write_text('False complete proof claim.')
                manifest=d/'PUBLICATION_MANIFEST.json';m=json.loads(manifest.read_bytes())
                for row in m['files']:
                    if row['path']=='author/REPORT.md':row.update(bytes=p.stat().st_size,sha256=sha(p.read_bytes()))
                old=sha(manifest.read_bytes());manifest.write_text(json.dumps(m));new=sha(manifest.read_bytes())
                verifier=d/'VERIFY_PUBLICATION.py';old_v=sha(verifier.read_bytes());verifier.write_bytes(verifier.read_bytes().replace(old.encode(),new.encode()))
                boot=d/'BOOTSTRAP.py';boot.write_bytes(boot.read_bytes().replace(old.encode(),new.encode()).replace(old_v.encode(),sha(verifier.read_bytes()).encode()))
            elif name=='optional-in-integrity':args=['--source-dir',str(temp)]
            elif name=='one-corpus-only':args=['--problems',str(temp/'missing')]
            for label,flags in modes:record(name,label,run(flags,d,args=args),False)
        # These intentionally bypass only the pin to test the strict parser itself.
        # They are NOT package-acceptance tests and never run mutant package code.
        base=json.loads((root/'PUBLICATION_MANIFEST.json').read_bytes());variants=[]
        mutations=[('bool-id',lambda m:m.update(problem_id=True)),('float-id',lambda m:m.update(problem_id=3091.0)),('wrong-rank',lambda m:m.update(rank=1057)),('wrong-status',lambda m:m.update(status='solved')),('float-turns',lambda m:m.update(turns=5.0)),('true-resolution',lambda m:m.update(full_target_resolved=True)),('integer-resolution',lambda m:m.update(full_target_resolved=0)),('extra-key',lambda m:m.update(extra=1)),('missing-key',lambda m:m.pop('rank')),('object-files',lambda m:m.update(files={})),('empty-files',lambda m:m.update(files=[])),('duplicate-entry',lambda m:m['files'].__setitem__(1,m['files'][0])),('unsafe-path',lambda m:m['files'][0].update(path='../escape')),('absolute-path',lambda m:m['files'][0].update(path='/escape')),('empty-component',lambda m:m['files'][0].update(path='author//REPORT.md')),('backslash-path',lambda m:m['files'][0].update(path='author\\REPORT.md')),('boolean-size',lambda m:m['files'][0].update(bytes=True)),('float-size',lambda m:m['files'][0].update(bytes=1.0)),('negative-size',lambda m:m['files'][0].update(bytes=-1)),('hash-type',lambda m:m['files'][0].update(sha256=7)),('hash-format',lambda m:m['files'][0].update(sha256='Z'*64)),('entry-extra-key',lambda m:m['files'][0].update(extra=1))]
        for name,fn in mutations:
            obj=copy.deepcopy(base);fn(obj);variants.append((name,json.dumps(obj).encode()))
        variants.extend([('duplicate-json-key',b'{"rank":1058,'+(root/'PUBLICATION_MANIFEST.json').read_bytes().lstrip()[1:]),('nonfinite-NaN',b'{"rank":NaN}'),('nonfinite-Infinity',b'{"rank":Infinity}'),('nonfinite-minus-Infinity',b'{"rank":-Infinity}'),('overflow-number',b'{"rank":1e999}'),('negative-overflow-number',b'{"rank":-1e999}'),('nonobject',b'[]'),('invalid-json',b'{')])
        harness=temp/'strict_schema.py';harness.write_text('''import importlib.util,sys
from pathlib import Path
spec=importlib.util.spec_from_file_location('trusted',sys.argv[1]);v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)
try:v.validate_manifest(v.load(Path(sys.argv[2]).read_bytes()))
except (v.Reject,ValueError,TypeError,KeyError) as e:print('REJECT: '+str(e),file=sys.stderr);sys.exit(1)
print('ACCEPTED')
''')
        for name,raw in variants:
            inp=temp/(name+'.json');inp.write_bytes(raw)
            for label,flags in modes:
                p=subprocess.run([sys.executable,'-I','-S','-B',*flags,str(harness),str(root/'VERIFY_PUBLICATION.py'),str(inp)],capture_output=True,timeout=30)
                record('strict-parser/'+name,label,{'exit_code':p.returncode,'stdout':p.stdout.decode(),'stderr':p.stderr.decode()},False)
        hostile=temp/'hostile';hostile.mkdir();marker=temp/'EXECUTED'
        for name in ['json','hashlib','pathlib','subprocess','sitecustomize','usercustomize']:(hostile/(name+'.py')).write_text('open('+repr(str(marker))+',"w").write("executed")\nraise RuntimeError("hostile import")\n')
        env=dict(os.environ,PYTHONPATH=str(hostile),PYTHONSTARTUP=str(hostile/'json.py'))
        for label,flags in modes:record('hostile-cwd-pythonpath',label,run(flags,root,cwd=hostile,env=env),True)
        need(not marker.exists(),'hostile module executed')
    after={str(p.relative_to(root)):sha(p.read_bytes()) for p in root.rglob('*') if p.is_file()};need(before==after,'originals changed')
    print(json.dumps({'schema':'hexagon-fixed-boundary-controls-v1','status':'PASS','fixed_external_bootstrap_sha256':sha(bootstrap.read_bytes()),'fixed_bootstrap_used_for_all_package_attacks':True,'package_attack_rejections':len(attacks)*3,'strict_parser_rejections':len(variants)*3,'baseline_and_hostile_passes':6,'hostile_modules_executed':False,'originals_unchanged':True,'results':results},sort_keys=True,indent=2))
if __name__=='__main__':main()
