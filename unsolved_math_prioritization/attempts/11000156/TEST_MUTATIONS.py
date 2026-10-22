#!/usr/bin/env python3
"""Exercise the frozen publication boundary using a separate trusted launcher."""
from pathlib import Path
import hashlib,json,os,shutil,subprocess,sys,tempfile,runpy
class Failure(Exception):pass
def need(c,m):
    if not c:raise Failure(m)
def sha(b):return hashlib.sha256(b).hexdigest()
def snapshot(r):return {str(p.relative_to(r)):sha(p.read_bytes()) for p in r.rglob('*') if p.is_file() and not p.is_symlink()}
def thaw(r):
    r.chmod(0o755)
    for p in r.rglob('*'):
        if not p.is_symlink():p.chmod(0o755 if p.is_dir() else 0o644)
def copy(src,dst):shutil.copytree(src,dst);thaw(dst)
def main():
    need(len(sys.argv)==1,'no arguments supported')
    root=Path(__file__).resolve().parent;before=snapshot(root);flags=[] if sys.flags.optimize==0 else ['-O' if sys.flags.optimize==1 else '-OO']
    def run(r,integrity=False,env=None,cwd=None):
        args=[sys.executable,'-I','-S','-B']+flags+[str(root/'BOOTSTRAP.py'),str(r)]+(['--integrity-only'] if integrity else [])
        return subprocess.run(args,cwd=cwd or r.parent,env=env,stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=180)
    positives=[];negative=[]
    with tempfile.TemporaryDirectory(prefix='boundary-twist-wrapper-controls-') as tmp:
        top=Path(tmp)
        for label,readonly in [('relocated',False),('relocated-read-only',True)]:
            d=top/label;copy(root,d)
            if readonly:
                for p in d.rglob('*'):p.chmod(0o555 if p.is_dir() else 0o444)
                d.chmod(0o555);denied=False
                try:(d/'UNEXPECTED_WRITE').write_bytes(b'x')
                except PermissionError:denied=True
                need(denied,'read-only permissions not enforced')
            cp=run(d,True);need(cp.returncode==0 and cp.stderr==b'','positive control rejected')
            need(snapshot(d)==before,'positive copy changed');positives.append(label);thaw(d)
        hostile=top/'hostile import directory';hostile.mkdir()
        marker=hostile/'HOSTILE_IMPORT_EXECUTED'
        for name in ['json.py','hashlib.py','sitecustomize.py']:
            (hostile/name).write_text('from pathlib import Path\nPath('+repr(str(marker))+').write_text("bad")\n')
        env=dict(os.environ,PYTHONPATH=str(hostile),PYTHONSTARTUP=str(hostile/'json.py'))
        cp=run(root,False,env=env,cwd=hostile)
        need(cp.returncode==0 and not cp.stderr and not marker.exists(),'hostile imports executed')
        positives.append('hostile-import-isolation')
        cases=[]
        for n in sorted(before):
            cases.append(('byte:'+n,lambda d,n=n:(d/n).write_bytes((d/n).read_bytes()+b'!')))
            cases.append(('missing:'+n,lambda d,n=n:(d/n).unlink()))
        cases.extend([
            ('extra-file',lambda d:(d/'EXTRA.txt').write_text('unexpected')),
            ('extra-empty-directory',lambda d:(d/'EXTRA').mkdir()),
            ('fifo',lambda d:os.mkfifo(d/'FIFO')),
            ('malformed-manifest',lambda d:(d/'PUBLICATION_MANIFEST.json').write_bytes(b'{')),
            ('duplicate-key-manifest',lambda d:(d/'PUBLICATION_MANIFEST.json').write_bytes(b'{"files":[],"files":[]}')),
        ])
        def symlink_file(d):
            p=d/'original/packet/REPORT.md';p.unlink();p.symlink_to(root/'original/packet/REPORT.md')
        def symlink_dir(d):
            p=d/'original/packet';shutil.rmtree(p);p.symlink_to(root/'original/packet',target_is_directory=True)
        cases.extend([('symlink-proof',symlink_file),('symlink-directory',symlink_dir)])
        def forge(d):
            p=d/'audit/corrected_distribution/packet/STATUS.json';j=json.loads(p.read_text());j['main_problem_resolved']=True;p.write_text(json.dumps(j))
            m=d/'PUBLICATION_MANIFEST.json';j=json.loads(m.read_text())
            for e in j['files']:
                if e['path']=='audit/corrected_distribution/packet/STATUS.json':b=p.read_bytes();e.update(bytes=len(b),sha256=sha(b))
            m.write_text(json.dumps(j))
        cases.append(('self-consistent-solved-forgery',forge))
        for label,change in [
            ('boolean-size',lambda j:j['files'][0].update(bytes=True)),
            ('path-traversal',lambda j:j['files'][0].update(path='../escape')),
            ('absolute-path',lambda j:j['files'][0].update(path='/escape')),
            ('duplicate-entry',lambda j:j['files'].append(j['files'][0])),
            ('invalid-digest',lambda j:j['files'][0].update(sha256='no')),
            ('nonfinite-size',lambda j:j['files'][0].update(bytes=float('nan'))),
        ]:
            def malformed(d,change=change):
                p=d/'PUBLICATION_MANIFEST.json';j=json.loads(p.read_text());change(j);p.write_text(json.dumps(j))
            cases.append(('manifest-'+label,malformed))

        for n in ['VERIFY_PUBLICATION.py','BOOTSTRAP.py','original/bootstrap.py','original/packet/verify.py','audit/independent_checks.py']:
            def code(d,n=n):
                (d/n).write_text('from pathlib import Path\nPath('+repr(str(d/'HOSTILE_EXECUTED'))+').write_text("bad")\n')
            cases.append(('hostile-code:'+n,code))
        for index,(name,mutate) in enumerate(cases):
            d=top/('case-'+str(index));copy(root,d);mutate(d);cp=run(d)
            need(cp.returncode!=0 and not cp.stdout and cp.stderr.startswith(b'REJECT:'),'mutation did not fail closed: '+name)
            need(not (d/'HOSTILE_EXECUTED').exists(),'unauthenticated code executed: '+name)
            negative.append(name)
        for target in ['BOOTSTRAP.py','VERIFY_PUBLICATION.py','PUBLICATION_MANIFEST.json','original/packet/REPORT.md']:
            for kind in ['symlink','hardlink','fifo','directory']:
                d=top/('typed-'+str(len(negative)));copy(root,d);p=d/target;b=p.read_bytes();p.unlink();outside=top/('outside-'+str(len(negative)));outside.write_bytes(b)
                if kind=='symlink':p.symlink_to(outside)
                elif kind=='hardlink':os.link(outside,p)
                elif kind=='fifo':os.mkfifo(p)
                else:p.mkdir()
                cp=run(d);need(cp.returncode!=0 and not cp.stdout and cp.stderr.startswith(b'REJECT:'),'typed mutation accepted');negative.append(kind+':'+target)
        cli=[]
        for args in [['--problems','missing'],['--research-results','missing'],['--integrity-only','--source-dir','missing'],['--integrity-only','--problems','missing','--research-results','missing']]:
            cp=subprocess.run([sys.executable,'-I','-S','-B',*flags,str(root/'BOOTSTRAP.py'),str(root),*args],capture_output=True,timeout=30)
            need(cp.returncode!=0 and not cp.stdout and cp.stderr.startswith(b'REJECT:'),'invalid optional inputs accepted');cli.append(args)
        # Parser tests deliberately substitute only the manifest pin in the
        # trusted verifier's in-memory namespace; these do not claim to test
        # the original external integrity anchor.
        module=runpy.run_path(str(root/'VERIFY_PUBLICATION.py'))
        auth=module['authenticate']; repinned=[]
        malformed=[
            ('top-level-list',lambda j:[]),
            ('extra-field',lambda j:dict(j,extra=1)),
            ('boolean-problem-id',lambda j:dict(j,problem_id=True)),
            ('boolean-turns',lambda j:dict(j,turns=True)),
            ('false-solved',lambda j:dict(j,disposition='solved')),
            ('files-object',lambda j:dict(j,files={})),
            ('empty-files',lambda j:dict(j,files=[])),
            ('boolean-size',lambda j:(j['files'][0].update(bytes=True) or j)),
            ('negative-size',lambda j:(j['files'][0].update(bytes=-1) or j)),
            ('floating-size',lambda j:(j['files'][0].update(bytes=1.0) or j)),
            ('extra-record-field',lambda j:(j['files'][0].update(extra=1) or j)),
            ('bad-digest',lambda j:(j['files'][0].update(sha256='A'*64) or j)),
            ('duplicate-path',lambda j:(j['files'].append(j['files'][0]) or j)),
            ('traversal',lambda j:(j['files'][0].update(path='../escape') or j)),
            ('absolute',lambda j:(j['files'][0].update(path='/escape') or j)),
            ('empty-path',lambda j:(j['files'][0].update(path='') or j)),
        ]
        for name,change in malformed:
            d=top/('parser-'+name);copy(root,d);p=d/'PUBLICATION_MANIFEST.json';p.write_text(json.dumps(change(json.loads(p.read_text()))))
            auth.__globals__['EXPECTED_MANIFEST']=sha(p.read_bytes());rejected=False
            try:auth(d)
            except (module['Reject'],ValueError,TypeError,KeyError):rejected=True
            need(rejected,'repinned parser case accepted: '+name);repinned.append(name)
        for name,raw in [('duplicate-json-keys',b'{"files":[],"files":[]}'),('nonfinite-json',b'{"files":NaN}'),('malformed-json',b'{')]:
            d=top/('parser-'+name);copy(root,d);p=d/'PUBLICATION_MANIFEST.json';p.write_bytes(raw);auth.__globals__['EXPECTED_MANIFEST']=sha(raw);rejected=False
            try:auth(d)
            except (module['Reject'],ValueError,TypeError,KeyError):rejected=True
            need(rejected,'repinned JSON case accepted: '+name);repinned.append(name)
        link=top/'symlink-root';link.symlink_to(root,target_is_directory=True);cp=run(link)
        need(cp.returncode!=0 and not cp.stdout and cp.stderr.startswith(b'REJECT:'),'symlink root accepted');negative.append('symlink-root')
    need(snapshot(root)==before,'original publication changed')
    return {'schema':'boundary-twist-publication-controls-v1','status':'pass','positive_count':len(positives),'positive_cases':positives,'optional_input_rejections':len(cli),'negative_count':len(negative),'repinned_schema_negative_count':len(repinned),'repinned_schema_cases':repinned,'rejected_cases':negative,'read_only_write_denied':True,'source_bytes_unchanged':True,'trust_boundary':'Separate trusted original BOOTSTRAP.py authenticates each candidate tree; the bootstrap and manifest hashes must themselves be checked against external pins.'}
if __name__=='__main__':
    try:print(json.dumps(main(),sort_keys=True,indent=2))
    except (Failure,OSError,ValueError,KeyError,TypeError,subprocess.SubprocessError) as e:
        print('REJECT: '+str(e),file=sys.stderr);sys.exit(1)
