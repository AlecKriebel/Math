"""Independent read-only review harness; mutations only in disposable copies."""
from pathlib import Path
import datetime, hashlib, json, os, shutil, stat, subprocess, sys, tempfile, zipfile, warnings

HERE=Path(__file__).resolve().parent
AUDIT=HERE.parent
SEAL=json.loads((AUDIT/'PACKAGE_SEAL_R1.json').read_text())
ASSEMBLY=Path(SEAL['assembly_tree'])
PORTABLE=ASSEMBLY/'publication_20261014/verification_package'
RECORDS=[]
FLAGS=['-I','-S','-B']

def digest(raw): return hashlib.sha256(raw).hexdigest()
def require(ok,msg):
    if not ok: raise RuntimeError(msg)

def run(cmd,cwd,env=None,timeout=25):
    try:
        q=subprocess.run(cmd,cwd=cwd,env=env,capture_output=True,text=True,timeout=timeout)
        return {'returncode':q.returncode,'stdout':q.stdout,'stderr':q.stderr,'timed_out':False}
    except subprocess.TimeoutExpired:
        return {'returncode':None,'stdout':'','stderr':'','timed_out':True}

def receipt(label,q,expected_rejection=True):
    ok=not q['timed_out'] and ((q['returncode']!=0) if expected_rejection else (q['returncode']==0 and not q['stderr']))
    RECORDS.append({'control':label,'passed':ok,'expected_rejection':expected_rejection,**q})
    return ok

def rewrite_index(root,name,change):
    p=root/name; data=json.loads(p.read_bytes());change(data);raw=(json.dumps(data,sort_keys=True,indent=2)+'\n').encode();p.write_bytes(raw);return digest(raw)

def rehash(root,index_name,relative):
    raw=(root/relative).read_bytes()
    def update(data):
        row=next(r for r in data['files'] if r['path']==relative);row['bytes']=len(raw);row['sha256']=digest(raw)
    return rewrite_index(root,index_name,update)

def main():
    (HERE/'disposable').mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='independent controls with spaces ',dir=HERE/'disposable') as td:
        scratch=Path(td).resolve();hostile=scratch/'hostile cwd';hostile.mkdir();marker=scratch/'executed marker'
        for name in ['json','hashlib','subprocess','sitecustomize','usercustomize','zipfile']:
            (hostile/(name+'.py')).write_text('from pathlib import Path\nPath('+repr(str(marker))+').touch()\nraise RuntimeError("hostile import")\n')
        env=dict(os.environ,PYTHONPATH=str(hostile),PYTHONHOME=str(hostile),PYTHONOPTIMIZE='2')
        for lane,source,index_name,script,pin in [('portable',PORTABLE,'package_index.json','verify_package.py',SEAL['index_sha256']),('outer',ASSEMBLY,'PUBLICATION_MANIFEST.json','verify_publication.py',SEAL['outer_manifest_sha256'])]:
            counter=0
            def fixture():
                nonlocal counter
                counter+=1;p=scratch/f'{lane} fixture {counter}';shutil.copytree(source,p);return p
            for optimized in [False,True]:
                flags=FLAGS+(['-O'] if optimized else []);suffix=' optimized' if optimized else ' normal'
                root=fixture();q=run([sys.executable,*flags,str(root/script),pin],hostile,env);receipt(lane+' relocated hostile startup'+suffix,q,False)
                for label,mutation in [
                    ('missing member',lambda r:(r/'README.md').unlink()),
                    ('extra member',lambda r:(r/'unindexed.txt').write_text('extra')),
                    ('same-size member mutation',lambda r:(r/'README.md').write_bytes(bytes([((r/'README.md').read_bytes()[0]^1)])+(r/'README.md').read_bytes()[1:])),
                    ('empty directory',lambda r:(r/'unindexed empty').mkdir()),
                    ('member symlink',lambda r:((r/'README.md').unlink(),(r/'README.md').symlink_to(source/'README.md'))),
                    ('directory symlink',lambda r:(r/'unindexed link').symlink_to(source,target_is_directory=True)),
                    ('member FIFO',lambda r:((r/'README.md').unlink(),os.mkfifo(r/'README.md'))),
                    ('index symlink',lambda r:((r/index_name).unlink(),(r/index_name).symlink_to(source/index_name))),
                    ('index FIFO',lambda r:((r/index_name).unlink(),os.mkfifo(r/index_name))),
                ]:
                    root=fixture();mutation(root);q=run([sys.executable,*flags,str(root/script),pin],hostile,env);receipt(lane+' '+label+suffix,q)
                root=fixture();receipt(lane+' wrong external pin'+suffix,run([sys.executable,*flags,str(root/script),'0'*64],hostile,env))
                for label,change in [
                    ('duplicate inventory',lambda d:d['files'].append(dict(d['files'][0]))),
                    ('traversal path',lambda d:d['files'][0].update(path='../outside')),
                    ('absolute path',lambda d:d['files'][0].update(path='/outside')),
                    ('backslash path',lambda d:d['files'][0].update(path='a\\b')),
                    ('dot alias path',lambda d:d['files'][0].update(path='./'+d['files'][0]['path'])),
                    ('boolean size',lambda d:d['files'][0].update(bytes=True)),
                ]:
                    root=fixture();fixture_pin=rewrite_index(root,index_name,change);receipt(lane+' coherent-fixture '+label+suffix,run([sys.executable,*flags,str(root/script),fixture_pin],hostile,env))
                root=fixture();raw=(root/index_name).read_text();raw=raw[:-2]+',"problem_id":30003060}\n';(root/index_name).write_text(raw);receipt(lane+' coherent-fixture duplicate JSON key'+suffix,run([sys.executable,*flags,str(root/script),digest(raw.encode())],hostile,env))
            root=fixture()
            for flagset in [[],['-I','-B'],['-S','-B'],['-I','-S']]:
                receipt(lane+' missing required startup flags '+repr(flagset),run([sys.executable,*flagset,str(root/script),pin],scratch))
            root=fixture();(root/script).write_text('from pathlib import Path\nPath('+repr(str(marker))+').touch()\n')
            # Independent external startup gate: never launch unbound replacement.
            trusted=digest((source/script).read_bytes());bound=digest((root/script).read_bytes())==trusted
            RECORDS.append({'control':lane+' substituted entrypoint rejected before launch','passed':not bound and not marker.exists(),'expected_rejection':True,'launched':False})

        # Independently challenge outer semantic checks with coherent fixture pins.
        for label,mutate in [
            ('metadata disagreement',lambda root:(root/'publication_20261014/preprint/metadata.json').write_text('{}\n')),
            ('PDF disagreement',lambda root:(root/'publication_20261014/preprint/output/pdf/note.pdf').write_bytes(b'bad PDF')),
        ]:
            root=scratch/label;shutil.copytree(ASSEMBLY,root);mutate(root)
            relative='publication_20261014/preprint/'+('metadata.json' if label.startswith('metadata') else 'output/pdf/note.pdf')
            fixture_pin=rehash(root,'PUBLICATION_MANIFEST.json',relative);receipt('outer coherent-fixture '+label,run([sys.executable,*FLAGS,str(root/'verify_publication.py'),fixture_pin],hostile,env))
        for label in ['duplicate','traversal','symlink','missing','extra']:
            root=scratch/('ZIP '+label);shutil.copytree(ASSEMBLY,root);zpath=root/'publication_20261014/preprint/verification.zip';original=zpath.read_bytes();zpath.unlink()
            import io
            with zipfile.ZipFile(io.BytesIO(original)) as src,zipfile.ZipFile(zpath,'w') as dst:
                for entry in src.infolist():
                    if label=='missing' and entry.filename=='README.md':continue
                    if label=='symlink' and entry.filename=='README.md':entry.external_attr=(stat.S_IFLNK|0o777)<<16
                    dst.writestr(entry,src.read(entry))
                with warnings.catch_warnings():
                    warnings.simplefilter('ignore')
                    if label=='duplicate':dst.writestr('README.md',b'duplicate')
                    if label=='traversal':dst.writestr('../outside',b'escape')
                    if label=='extra':dst.writestr('extra.txt',b'extra')
            fixture_pin=rehash(root,'PUBLICATION_MANIFEST.json','publication_20261014/preprint/verification.zip');receipt('outer coherent-fixture ZIP '+label,run([sys.executable,*FLAGS,str(root/'verify_publication.py'),fixture_pin],hostile,env))

        # Genuine documented builder executions from assembled preprint cwd.
        pre=ASSEMBLY/'publication_20261014/preprint';builder=pre/'build_verification.py'
        for optimized in [False,True]:
            output=scratch/('rebuilt output O' if optimized else 'rebuilt output normal')
            cmd=[sys.executable,*FLAGS,*(['-O'] if optimized else []),str(builder),'--from-package','../verification_package','--trusted-index-sha256',SEAL['index_sha256'],'--output-root',str(output)]
            q=run(cmd,pre,timeout=90);ok=receipt('actual assembled-cwd deterministic builder '+str(optimized),q,False)
            if ok:
                exact=all((output/n).read_bytes()==(pre/n).read_bytes() for n in ['package_index.json','verification.zip']);RECORDS.append({'control':'byte-identical rebuilt ZIP/index '+str(optimized),'passed':exact,'expected_rejection':False})
        for label in ['wrong pin','changed checker','nonempty output','inside input','same input','missing output','FIFO member','symlink index','FIFO index']:
            root=scratch/('builder '+label);shutil.copytree(PORTABLE,root);output=scratch/('builder output '+label);pin=SEAL['index_sha256']
            if label=='wrong pin':pin='0'*64
            if label=='changed checker':(root/'verify_package.py').write_text('from pathlib import Path\nPath('+repr(str(marker))+').touch()\n')
            if label=='nonempty output':output.mkdir();(output/'existing.txt').write_text('preserve')
            if label=='inside input':output=root/'out'
            if label=='same input':output=root
            if label=='FIFO member':(root/'README.md').unlink();os.mkfifo(root/'README.md')
            if label=='symlink index':(root/'package_index.json').unlink();(root/'package_index.json').symlink_to(PORTABLE/'package_index.json')
            if label=='FIFO index':(root/'package_index.json').unlink();os.mkfifo(root/'package_index.json')
            cmd=[sys.executable,*FLAGS,str(builder),'--from-package',str(root),'--trusted-index-sha256',pin]
            if label!='missing output':cmd+=['--output-root',str(output)]
            q=run(cmd,hostile,env,timeout=3 if label=='FIFO index' else 25);receipt('builder '+label,q)
            require(not marker.exists(),'substituted checker executed')
        require(not marker.exists(),'hostile import executed')
        RECORDS.append({'control':'hostile/substituted execution marker absent','passed':not marker.exists(),'expected_rejection':False})
    result={'timestamp_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'control_count':len(RECORDS),'failed_controls':[r['control'] for r in RECORDS if not r['passed']],'derived_fixture_pins_are_not_authorized_replacements':True,'not_an_OS_sandbox_test':True,'records':RECORDS}
    (HERE/'INDEPENDENT_CONTROLS.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='records'},indent=2))

if __name__=='__main__':main()
