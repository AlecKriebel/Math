#!/usr/bin/env python3
"""Exercise the frozen publication boundary using a separate trusted launcher."""
from pathlib import Path
import copy as copying
import hashlib,io,json,os,shutil,stat,subprocess,sys,tempfile,tarfile
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
    # Execute semantic validators directly after authenticating the real packet.
    baseline=run(root,True);need(baseline.returncode==0 and not baseline.stderr,'untrusted baseline')
    ns={'__name__':'publication_validator_tests','__file__':str(root/'VERIFY_PUBLICATION.py')}
    exec(compile((root/'VERIFY_PUBLICATION.py').read_bytes(),ns['__file__'],'exec'),ns)
    files,dirs=ns['inventory'](root);manifest=ns['load'](files['PUBLICATION_MANIFEST.json']);claims=ns['load'](files['CLAIMS.json']);semantic=[]
    def reject_semantic(name,call):
        try:call()
        except (ns['Reject'],ValueError,TypeError,KeyError,UnicodeError,tarfile.TarError):semantic.append(name)
        else:raise Failure('semantic mutation accepted: '+name)
    for name,edit in [
        ('bool-id',lambda j:j.update(problem_id=True)),('float-id',lambda j:j.update(problem_id=2304003.0)),
        ('bool-turns',lambda j:j.update(proof_turns=False)),('float-turns',lambda j:j.update(proof_turns=5.0)),
        ('float-rank',lambda j:j.update(rank=1032.0)),('wrong-scope',lambda j:j.update(scope='all polygons')),
        ('extra-field',lambda j:j.update(extra=True)),('missing-field',lambda j:j.pop('rank')),
        ('files-object',lambda j:j.update(files={})),('empty-files',lambda j:j.update(files=[])),
        ('boolean-size',lambda j:j['files'][0].update(bytes=True)),('float-size',lambda j:j['files'][0].update(bytes=float(j['files'][0]['bytes']))),
        ('negative-size',lambda j:j['files'][0].update(bytes=-1)),('missing-size',lambda j:j['files'][0].pop('bytes')),
        ('hash-type',lambda j:j['files'][0].update(sha256=1)),('uppercase-hash',lambda j:j['files'][0].update(sha256=j['files'][0]['sha256'].upper())),
        ('duplicate-entry',lambda j:j['files'].append(j['files'][0])),('entry-list',lambda j:j['files'].__setitem__(0,[])),
        ('extra-entry-key',lambda j:j['files'][0].update(extra=True)),
        *[(label,lambda j,p=p:j['files'][0].update(path=p)) for label,p in [('path-up','../escape'),('path-absolute','/escape'),('path-dot','a/./b'),('path-empty','a//b'),('path-backslash','a\\b'),('path-nonstr',1)]],
    ]:
        j=copying.deepcopy(manifest);edit(j);reject_semantic('manifest:'+name,lambda j=j:ns['validate_manifest'](j,files,dirs))
    for key,v in claims.items():
        j=copying.deepcopy(claims)
        j[key]=(int(v) if type(v) is bool else float(v) if type(v) is int else None)
        reject_semantic('claims-type:'+key,lambda j=j:ns['exact'](j,claims))
    for key in ['novelty_claimed','full_problem_resolved','formal_certification','human_peer_review_claimed','source_documents_included','dataset_contents_included','private_coordination_included']:
        j=copying.deepcopy(claims);j[key]=True;reject_semantic('claims-scope:'+key,lambda j=j:ns['exact'](j,claims))
    for name,b in [('duplicate',b'{"x":1,"x":2}'),('nested-duplicate',b'{"x":{"a":1,"a":2}}'),('nan',b'{"x":NaN}'),('infinity',b'[Infinity]'),('minus-infinity',b'[-Infinity]'),('overflow',b'{"x":1e999}'),('negative-overflow',b'[-1e999]'),('malformed',b'{'),('invalid-utf8',b'{\xff}'),('trailing',b'{}{}')]:reject_semantic('json:'+name,lambda b=b:ns['load'](b))
    for label,names,kind,data in [('duplicate',['ok','ok'],tarfile.REGTYPE,b'x'),('traversal',['../ok'],tarfile.REGTYPE,b'x'),('symlink',['ok'],tarfile.SYMTYPE,b'x'),('fifo',['ok'],tarfile.FIFOTYPE,b'x'),('wrong-bytes',['ok'],tarfile.REGTYPE,b'y'),('absolute',['/ok'],tarfile.REGTYPE,b'x')]:
        stream=io.BytesIO()
        with tarfile.open(fileobj=stream,mode='w:gz',format=tarfile.USTAR_FORMAT) as t:
            for name in names:
                e=tarfile.TarInfo(name);e.type=kind;e.mode=0o444;e.size=len(data) if kind==tarfile.REGTYPE else 0
                t.addfile(e,io.BytesIO(data) if kind==tarfile.REGTYPE else None)
        reject_semantic('archive:'+label,lambda b=stream.getvalue():ns['archive_members'](b,{'ok':b'x'}))
    with tempfile.TemporaryDirectory(prefix='bounded-polynomial-wrapper-controls-') as tmp:
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
        cp=run(root,True,env=env,cwd=hostile)
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
            p=d/'accepted/audit/public/MATHEMATICAL_AUDIT.md';p.unlink();p.symlink_to(root/'accepted/audit/public/MATHEMATICAL_AUDIT.md')
        def symlink_dir(d):
            p=d/'accepted/original/public';shutil.rmtree(p);p.symlink_to(root/'accepted/original/public',target_is_directory=True)
        cases.extend([('symlink-proof',symlink_file),('symlink-directory',symlink_dir)])
        def forge(d):
            p=d/'CLAIMS.json';j=json.loads(p.read_text());j['novelty_claimed']=True;p.write_text(json.dumps(j))
            m=d/'PUBLICATION_MANIFEST.json';j=json.loads(m.read_text())
            for e in j['files']:
                if e['path']=='CLAIMS.json':b=p.read_bytes();e.update(bytes=len(b),sha256=sha(b))
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

        for n in ['VERIFY_PUBLICATION.py','BOOTSTRAP.py','accepted/original/external/bootstrap.py','accepted/original/public/verify.py','accepted/audit/public/independent_checks.py']:
            def code(d,n=n):
                (d/n).write_text('from pathlib import Path\nPath('+repr(str(d/'HOSTILE_EXECUTED'))+').write_text("bad")\n')
            cases.append(('hostile-code:'+n,code))
        for index,(name,mutate) in enumerate(cases):
            d=top/('case-'+str(index));copy(root,d);mutate(d);cp=run(d)
            need(cp.returncode!=0 and not cp.stdout and cp.stderr.startswith(b'REJECT:'),'mutation did not fail closed: '+name)
            need(not (d/'HOSTILE_EXECUTED').exists(),'unauthenticated code executed: '+name)
            negative.append(name)
        for target in ['BOOTSTRAP.py','VERIFY_PUBLICATION.py','PUBLICATION_MANIFEST.json','accepted/audit/public/MATHEMATICAL_AUDIT.md']:
            for kind in ['symlink','hardlink','fifo','directory']:
                d=top/('typed-'+str(len(negative)));copy(root,d);p=d/target;b=p.read_bytes();p.unlink();outside=top/('outside-'+str(len(negative)));outside.write_bytes(b)
                if kind=='symlink':p.symlink_to(outside)
                elif kind=='hardlink':os.link(outside,p)
                elif kind=='fifo':os.mkfifo(p)
                else:p.mkdir()
                cp=run(d);need(cp.returncode!=0 and not cp.stdout and cp.stderr.startswith(b'REJECT:'),'typed mutation accepted');negative.append(kind+':'+target)
        link=top/'symlink-root';link.symlink_to(root,target_is_directory=True);cp=run(link)
        need(cp.returncode!=0 and not cp.stdout and cp.stderr.startswith(b'REJECT:'),'symlink root accepted');negative.append('symlink-root')
    need(snapshot(root)==before,'original publication changed')
    return {'schema':'bounded-polynomial-publication-controls-v1','status':'pass','semantic_negative_count':len(semantic),'semantic_rejected_cases':semantic,'positive_count':len(positives),'positive_cases':positives,'negative_count':len(negative),'rejected_cases':negative,'read_only_write_denied':True,'source_bytes_unchanged':True,'trust_boundary':'Separate trusted original BOOTSTRAP.py authenticates each candidate tree; the bootstrap and manifest hashes must themselves be checked against external pins.'}
if __name__=='__main__':
    try:print(json.dumps(main(),sort_keys=True,indent=2))
    except (Failure,OSError,ValueError,KeyError,TypeError,subprocess.SubprocessError) as e:
        print('REJECT: '+str(e),file=sys.stderr);sys.exit(1)
