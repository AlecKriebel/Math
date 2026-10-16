#!/usr/bin/env python3
"""Independent R4 audit; mutations happen before launch and are receipted."""
from pathlib import Path
import concurrent.futures, hashlib, json, os, shutil, socket, stat, subprocess, sys, time, zipfile, warnings

HERE = Path(__file__).resolve().parent
AUDIT = HERE.parent
TREE = AUDIT.parents[1] / 'work/pr826_revision_r2'
WORK = HERE / 'replay'
OUTER = '9b9a4745e417b15acfbd5a9115adb0f5a7f6a78b010b94be10cb81072e0bf022'
INNER = '19d20ccc3b5533a45d262f7c784e052555b3bf8cc47d9a2b76bc17ab5eda9360'
CHECKER = 'ed19078665c832c52c405c29169cf621a6670499845b046ca970475bef40ceed'
BUILDER = '22d85ce61149b201e93149f61a26e0571f3cdf8f0fdb0c99d8c73b4589ce423a'
PREF = 'publication_20261014/'
sha = lambda b: hashlib.sha256(b).hexdigest()
def need(ok, why):
    if not ok: raise RuntimeError(why)
def inventory(root):
    return {str(p.relative_to(root)): sha(p.read_bytes()) if p.is_file() else ('directory' if p.is_dir() else 'nonregular')
            for p in sorted(root.rglob('*')) if not p.is_symlink()}
def pin_tree(root, name, pin):
    need(sha((root/name).read_bytes()) == pin, 'independent manifest pin')
    d=json.loads((root/name).read_bytes()); names={e['path'] for e in d['files']}
    actual={str(p.relative_to(root)) for p in root.rglob('*') if p.is_file()}
    need(actual == names|{name}, 'independent closed inventory')
    for e in d['files']:
        p=root/e['path']; b=p.read_bytes()
        need(stat.S_ISREG(p.lstat().st_mode) and len(b)==e['bytes'] and sha(b)==e['sha256'], e['path'])
def refresh(root, name):
    p=root/name; d=json.loads(p.read_bytes())
    for row in d['files']:
        raw=(root/row['path']).read_bytes(); row.update(bytes=len(raw),sha256=sha(raw))
    p.write_text(json.dumps(d,indent=2,sort_keys=True)+'\n'); return sha(p.read_bytes())
def main():
    WORK.mkdir(exist_ok=False)
    hostile=WORK/'hostile cwd with spaces'; hostile.mkdir(); marker=hostile/'MARKER'
    for name in ['sitecustomize','usercustomize','json','hashlib','subprocess','zipfile','fractions']:
        (hostile/(name+'.py')).write_text('raise RuntimeError("hostile module imported")\n')
    env=dict(os.environ,PYTHONPATH=str(hostile),PYTHONHOME=str(hostile),TMPDIR=str(WORK),TMP=str(WORK),TEMP=str(WORK))
    baseline=WORK/'relocated assembly with spaces'; shutil.copytree(TREE,baseline)
    inner=baseline/(PREF+'verification_package'); pre=baseline/(PREF+'preprint')
    pin_tree(baseline,'PUBLICATION_MANIFEST.json',OUTER);pin_tree(inner,'package_index.json',INNER)
    need(sha((inner/'verify_package.py').read_bytes())==CHECKER,'startup verifier bytes')
    need(sha((pre/'build_verification.py').read_bytes())==BUILDER,'startup builder bytes')
    before=inventory(baseline); results=[]
    def call(script,args=(),opt=False,flags=None,cwd=None,timeout=120):
        t=time.monotonic()
        try:
            r=subprocess.run([sys.executable,*(flags if flags is not None else ['-I','-S','-B']),*(['-O'] if opt else []),str(script),*map(str,args)],
                             cwd=cwd or hostile,env=env,capture_output=True,text=True,timeout=timeout)
            return dict(returncode=r.returncode,stdout=r.stdout,stderr=r.stderr,seconds=time.monotonic()-t,timed_out=False)
        except subprocess.TimeoutExpired:
            return dict(returncode=None,stdout='',stderr='',seconds=time.monotonic()-t,timed_out=True)
    def positive(kind,opt):
        s=inner/'verify_package.py' if kind=='portable' else baseline/'verify_publication.py'
        r=call(s,[INNER if kind=='portable' else OUTER,'--full'],opt,timeout=240)
        need(r['returncode']==0 and not r['stderr'],kind+' full '+str(opt)+r['stderr'])
        data=json.loads(r.pop('stdout')); (HERE/(kind+('_optimized' if opt else '_normal')+'.json')).write_text(json.dumps(data,indent=2)+'\n')
        r.update(test=kind+' full',optimized=opt,status=data['status'])
        return r
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:
        for r in ex.map(lambda k: positive(*k),[(k,o) for k in ['portable','outer'] for o in [False,True]]):results.append(r)
    need(inventory(baseline)==before,'full commands modified package')
    for opt in [False,True]:
        output=WORK/('rebuild '+str(opt));r=call(pre/'build_verification.py',['--from-package','../verification_package','--trusted-index-sha256',INNER,'--output-root',output],opt,cwd=pre)
        need(r['returncode']==0 and not r['stderr'],'assembled cwd builder '+r['stderr'])
        need((output/'verification.zip').read_bytes()==(pre/'verification.zip').read_bytes(),'ZIP not reproduced')
        need((output/'package_index.json').read_bytes()==(pre/'package_index.json').read_bytes(),'index not reproduced')
        results.append(dict(test='assembled-cwd byte-exact rebuild',optimized=opt,receipt=json.loads(r['stdout'])))
    counter=0
    def fixture(label,mutate,outer=False,repin=False,expected='reject'):
        nonlocal counter
        for opt in [False,True]:
            counter+=1; root=WORK/('fixture '+str(counter)); shutil.copytree(baseline if outer else inner,root)
            before_mut=inventory(root)
            # Explicitly invoke mutation; receipt proves an applied mutation, not a vacuous pristine run.
            mutate(root)
            after_mut=inventory(root)
            need(before_mut!=after_mut or label.startswith('symlink'),'fixture mutation absent: '+label)
            manifest='PUBLICATION_MANIFEST.json' if outer else 'package_index.json'
            pin=(sha((root/manifest).read_bytes()) if label.startswith('index unsafe ') else refresh(root,manifest)) if repin else (OUTER if outer else INNER)
            script=root/('verify_publication.py' if outer else 'verify_package.py')
            r=call(script,[pin],opt,timeout=8)
            need(not r['timed_out'] and r['returncode']!=0 and '"status": "PASS"' not in r['stdout'],label+' accepted or blocked')
            results.append(dict(test=label,optimized=opt,mutation_applied=True,derived_fixture_pin=repin,
                changed=sorted(k for k in set(before_mut)|set(after_mut) if before_mut.get(k)!=after_mut.get(k)),**r))
            shutil.rmtree(root)
    fixture('changed file',lambda r:(r/'README.md').write_bytes(b'changed'))
    fixture('same-size file',lambda r:(r/'README.md').write_bytes(b'X'+(r/'README.md').read_bytes()[1:]))
    fixture('missing file',lambda r:(r/'README.md').unlink())
    fixture('extra file',lambda r:(r/'extra').write_bytes(b'x'))
    fixture('extra directory',lambda r:(r/'extra directory').mkdir())
    def symlink(r):
        p=r/'README.md';p.unlink();p.symlink_to(inner/'README.md')
    fixture('symlink member',symlink)
    def fifo(r):
        p=r/'README.md';p.unlink();os.mkfifo(p)
    fixture('FIFO member',fifo)
    def sock(r):
        p=r/'README.md';p.unlink();s=socket.socket(socket.AF_UNIX);previous=Path.cwd()
        try: os.chdir(r);s.bind('README.md')
        finally:os.chdir(previous);s.close()
    fixture('socket member',sock)
    fixture('index same-size substitution',lambda r:(r/'package_index.json').write_bytes(b'X'+(r/'package_index.json').read_bytes()[1:]))
    def duplicate_key(r):
        p=r/'package_index.json';p.write_bytes(p.read_bytes().replace(b'{',b'{"problem_id":30003060,',1))
    # These parser fixtures derive a new pin without changing the already-authenticated program.
    for label,mutation in [('duplicate JSON key',duplicate_key)]:
        for opt in [False,True]:
            root=WORK/('parser '+str(opt));shutil.copytree(inner,root);mutation(root)
            pin=sha((root/'package_index.json').read_bytes());r=call(root/'verify_package.py',[pin],opt)
            need(r['returncode']!=0 and 'duplicate JSON key' in r['stderr'],'duplicate parser control')
            results.append(dict(test=label,optimized=opt,mutation_applied=True,derived_fixture_pin=True,**r));shutil.rmtree(root)
    def index_edit(root,kind):
        p=root/'package_index.json';d=json.loads(p.read_bytes())
        if kind=='duplicate inventory path':d['files'].append(d['files'][0])
        else:d['files'][0]['path']=kind
        p.write_text(json.dumps(d)+'\n')
    for kind in ['duplicate inventory path','../escape','/absolute','a/../b','./README.md','a//b','a\\b']:
        fixture('index unsafe '+kind,lambda r,k=kind:index_edit(r,k),repin=True)
    def mismatch(root,kind):
        p=root/(PREF+'preprint/'+('metadata.json' if kind=='metadata' else 'output/pdf/note.pdf'))
        if kind=='metadata':d=json.loads(p.read_bytes());d['version']='wrong';p.write_text(json.dumps(d))
        else:p.write_bytes(b'wrong PDF')
    for k in ['metadata','PDF']:fixture(k+' disagreement',lambda r,k=k:mismatch(r,k),outer=True,repin=True)
    def zipmut(root,kind):
        p=root/(PREF+'preprint/verification.zip');tmp=root/'replacement.zip'
        with zipfile.ZipFile(p) as src,zipfile.ZipFile(tmp,'w') as dest:
            for e in src.infolist():
                if kind=='missing' and e.filename=='README.md':continue
                if kind=='type' and e.filename=='README.md':e.external_attr=(stat.S_IFLNK|0o777)<<16
                dest.writestr(e,src.read(e))
            with warnings.catch_warnings():
                warnings.simplefilter('ignore')
                if kind=='duplicate':dest.writestr('README.md',b'x')
                if kind=='traversal':dest.writestr('../escape',b'x')
        tmp.replace(p)
    for k in ['missing','duplicate','traversal','type']:fixture('malformed ZIP '+k,lambda r,k=k:zipmut(r,k),outer=True,repin=True)
    for kind in ['portable','outer']:
        script=inner/'verify_package.py' if kind=='portable' else baseline/'verify_publication.py'; pin=INNER if kind=='portable' else OUTER
        for flags in [['-I','-S'],['-I','-B'],['-S','-B']]:
            r=call(script,[pin],flags=flags);need(r['returncode']!=0,'missing interpreter flags accepted')
            results.append(dict(test=kind+' missing flags',flags=flags,**r))
    for generation in ['r1','r2']:
        original_source=AUDIT.parents[1]/('work/pr826_revision_'+generation)/(PREF+'preprint/build_verification.py')
        source=WORK/(generation+' disposable-builder.py');shutil.copyfile(original_source,source)
        for kind in (['fifo'] if generation=='r1' else ['fifo','socket','directory','symlink']):
            for opt in [False,True]:
                root=WORK/(generation+' '+kind+' '+str(opt));shutil.copytree(inner,root)
                p=root/'package_index.json';p.unlink()
                if kind=='fifo':os.mkfifo(p)
                elif kind=='socket':
                    s=socket.socket(socket.AF_UNIX);previous=Path.cwd()
                    try:os.chdir(root);s.bind('package_index.json')
                    finally:os.chdir(previous);s.close()
                elif kind=='directory':p.mkdir()
                else:p.symlink_to(inner/'package_index.json')
                output=WORK/('output '+generation+' '+kind+' '+str(opt));
                r=call(source,['--from-package',root,'--trusted-index-sha256',INNER,'--output-root',output],opt,timeout=1)
                need(r['timed_out'] if generation=='r1' else (not r['timed_out'] and r['returncode']!=0 and 'regular file' in r['stderr']),generation+' nonregular behavior')
                need(not output.exists(),'failed builder wrote output')
                results.append(dict(test=generation+' builder index '+kind,optimized=opt,mutation_applied=True,**r));shutil.rmtree(root)
    for opt in [False,True]:
        output=WORK/('canary '+str(opt));output.mkdir();(output/'KEEP').write_bytes(b'canary')
        r=call(pre/'build_verification.py',['--from-package',inner,'--trusted-index-sha256',INNER,'--output-root',output],opt)
        need(r['returncode']!=0 and inventory(output)=={'KEEP':sha(b'canary')},'output canary altered')
        results.append(dict(test='builder output canary preserved',optimized=opt,**r))
        for target in ['verify_package.py','package_index.json']:
            root=WORK/('substitution '+str(opt)+' '+target);shutil.copytree(inner,root)
            (root/target).write_bytes(b'raise RuntimeError("should never execute")\n')
            output=WORK/('substitution-output '+str(opt)+' '+target)
            r=call(pre/'build_verification.py',['--from-package',root,'--trusted-index-sha256',INNER,'--output-root',output],opt)
            need(r['returncode']!=0 and not output.exists() and 'should never execute' not in r['stderr'],'substitution executed')
            results.append(dict(test='builder rejects '+target+' substitution before execution',optimized=opt,mutation_applied=True,**r));shutil.rmtree(root)
    need(inventory(baseline)==before,'baseline inputs changed')
    (HERE/'REPLAY_AND_CONTROLS.json').write_text(json.dumps(dict(status='PASS',test_count=len(results),results=results,
        caveat='Derived fixture pins test structural guards, never replacement authority. No OS sandbox or race resistance certified.'),indent=2)+'\n')
    print(json.dumps(dict(status='PASS',test_count=len(results))))
if __name__=='__main__':main()
