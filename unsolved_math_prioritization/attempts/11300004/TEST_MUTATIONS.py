#!/usr/bin/env python3
"""Exercise the frozen publication boundary using a separate trusted launcher."""
from pathlib import Path
import hashlib,io,json,os,shutil,subprocess,sys,tarfile,tempfile
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
    positives=[];negative=[];structural=[];archive_controls=[];overflow_controls=[]
    with tempfile.TemporaryDirectory(prefix='wild-quadrisecants-wrapper-controls-') as tmp:
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
            p=d/'audit/public/corrected/packet/REPORT.md';p.unlink();p.symlink_to(root/'audit/public/corrected/packet/REPORT.md')
        def symlink_dir(d):
            p=d/'audit/public/corrected/packet';shutil.rmtree(p);p.symlink_to(root/'audit/public/corrected/packet',target_is_directory=True)
        cases.extend([('symlink-proof',symlink_file),('symlink-directory',symlink_dir)])
        def forge(d):
            p=d/'audit/public/ACCEPTANCE.json';j=json.loads(p.read_text());j['novelty_claim']=True;p.write_text(json.dumps(j))
            m=d/'PUBLICATION_MANIFEST.json';j=json.loads(m.read_text())
            for e in j['files']:
                if e['path']=='audit/public/ACCEPTANCE.json':b=p.read_bytes();e.update(bytes=len(b),sha256=sha(b))
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

        for n in ['VERIFY_PUBLICATION.py','BOOTSTRAP.py','audit/public/corrected/freeze/bootstrap.py','audit/public/corrected/packet/verify.py','audit/public/corrected/audit_tools/replay_tests.py','audit/public/independent_archive_replay.py']:
            def code(d,n=n):
                (d/n).write_text('from pathlib import Path\nPath('+repr(str(d/'HOSTILE_EXECUTED'))+').write_text("bad")\n')
            cases.append(('hostile-code:'+n,code))
        for index,(name,mutate) in enumerate(cases):
            d=top/('case-'+str(index));copy(root,d);mutate(d);cp=run(d)
            need(cp.returncode!=0 and not cp.stdout and cp.stderr.startswith(b'REJECT:'),'mutation did not fail closed: '+name)
            need(not (d/'HOSTILE_EXECUTED').exists(),'unauthenticated code executed: '+name)
            negative.append(name)
        for target in ['BOOTSTRAP.py','VERIFY_PUBLICATION.py','PUBLICATION_MANIFEST.json','audit/public/corrected/packet/REPORT.md']:
            for kind in ['symlink','hardlink','fifo','directory']:
                d=top/('typed-'+str(len(negative)));copy(root,d);p=d/target;b=p.read_bytes();p.unlink();outside=top/('outside-'+str(len(negative)));outside.write_bytes(b)
                if kind=='symlink':p.symlink_to(outside)
                elif kind=='hardlink':os.link(outside,p)
                elif kind=='fifo':os.mkfifo(p)
                else:p.mkdir()
                cp=run(d);need(cp.returncode!=0 and not cp.stdout and cp.stderr.startswith(b'REJECT:'),'typed mutation accepted');negative.append(kind+':'+target)
        # Diagnostic-only repinning exercises the schema parser behind the frozen digest.
        # Production bootstrap pins remain unchanged; no mutated Python is executed.
        namespace={'__name__':'publication_schema_diagnostics','__file__':str(root/'VERIFY_PUBLICATION.py')}
        exec(compile((root/'VERIFY_PUBLICATION.py').read_bytes(),str(root/'VERIFY_PUBLICATION.py'),'exec'),namespace)
        reject_type=namespace['Reject']
        for token in ['1e999','-1e999']:
            try:namespace['load']('{"value":'+token+'}')
            except reject_type:overflow_controls.append(token)
            else:raise Failure('overflowed JSON float accepted: '+token)
        need(namespace['load']('{"value":1.25}')=={'value':1.25},'finite JSON float rejected')
        positives.append('finite-json-float')
        repinned=[]
        for label,mutate in [
            ('schema-extra-field',lambda j:j.update(extra=0)),
            ('rank-bool',lambda j:j.update(rank=True)),
            ('approaches-float',lambda j:j.update(approaches=5.0)),
            ('solved-status',lambda j:j.update(disposition='solved')),
            ('files-object',lambda j:j.update(files={})),
            ('files-empty',lambda j:j.update(files=[])),
            ('bytes-bool',lambda j:j['files'][0].update(bytes=True)),
            ('bytes-float',lambda j:j['files'][0].update(bytes=1.0)),
            ('bytes-negative',lambda j:j['files'][0].update(bytes=-1)),
            ('entry-extra-field',lambda j:j['files'][0].update(extra=0)),
            ('entry-duplicate',lambda j:j['files'].append(j['files'][0])),
            ('entry-missing',lambda j:j['files'].pop()),
            ('path-traversal',lambda j:j['files'][0].update(path='../escape')),
            ('path-absolute',lambda j:j['files'][0].update(path='/escape')),
            ('path-dot',lambda j:j['files'][0].update(path='audit/./escape')),
            ('digest-uppercase',lambda j:j['files'][0].update(sha256='A'*64)),
            ('digest-integer',lambda j:j['files'][0].update(sha256=0)),
        ]:
            j=json.loads((root/'PUBLICATION_MANIFEST.json').read_bytes());mutate(j);repinned.append((label,json.dumps(j).encode()))
        repinned.extend([('broken-json',b'{'),('array-root',b'[]'),('duplicate-json-key',b'{"files":[],"files":[]}'),('nonfinite-json',b'{"files":NaN}'),('positive-float-overflow',b'{"files":1e999}'),('negative-float-overflow',b'{"files":-1e999}')])
        for label,raw in repinned:
            d=top/('schema-'+str(len(structural)));copy(root,d);(d/'PUBLICATION_MANIFEST.json').write_bytes(raw)
            namespace['EXPECTED_MANIFEST']=sha(raw)
            try:namespace['authenticate'](d)
            except (reject_type,ValueError):structural.append(label)
            else:raise Failure('malformed repinned schema accepted: '+label)
        def archive(entries):
            buf=io.BytesIO()
            with tarfile.open(fileobj=buf,mode='w:gz') as tar:
                for name,kind,body in entries:
                    e=tarfile.TarInfo(name);e.type=kind;e.size=len(body) if kind==tarfile.REGTYPE else 0
                    if kind in [tarfile.SYMTYPE,tarfile.LNKTYPE]:e.linkname='x'
                    tar.addfile(e,io.BytesIO(body) if kind==tarfile.REGTYPE else None)
            return buf.getvalue()
        cases=[
            ('duplicate-member',[('x',tarfile.REGTYPE,b'x'),('x',tarfile.REGTYPE,b'x')]),
            ('traversal-member',[('../x',tarfile.REGTYPE,b'x')]),
            ('absolute-member',[('/x',tarfile.REGTYPE,b'x')]),
            ('symlink-member',[('x',tarfile.SYMTYPE,b'')]),
            ('hardlink-member',[('x',tarfile.LNKTYPE,b'')]),
            ('fifo-member',[('x',tarfile.FIFOTYPE,b'')]),
            ('directory-substitution',[('x',tarfile.DIRTYPE,b'')]),
            ('extra-member',[('x',tarfile.REGTYPE,b'x'),('y',tarfile.REGTYPE,b'y')]),
            ('wrong-size',[('x',tarfile.REGTYPE,b'xx')]),
            ('wrong-bytes',[('x',tarfile.REGTYPE,b'y')]),
        ]
        need(namespace['archive_members'](archive([('x',tarfile.REGTYPE,b'x')]),{'x':b'x'})==1,'valid archive rejected')
        positives.append('minimal-valid-archive')
        for label,entries in cases:
            try:namespace['archive_members'](archive(entries),{'x':b'x'})
            except reject_type:archive_controls.append(label)
            else:raise Failure('malformed archive accepted: '+label)
        link=top/'symlink-root';link.symlink_to(root,target_is_directory=True);cp=run(link)
        need(cp.returncode!=0 and not cp.stdout and cp.stderr.startswith(b'REJECT:'),'symlink root accepted');negative.append('symlink-root')
    need(snapshot(root)==before,'original publication changed')
    return {'schema':'wild-quadrisecants-publication-controls-v1','status':'pass','positive_count':len(positives),'positive_cases':positives,'repinned_schema_rejections':len(structural),'repinned_schema_cases':structural,'overflow_number_rejections':len(overflow_controls),'overflow_number_cases':overflow_controls,'archive_rejections':len(archive_controls),'archive_cases':archive_controls,'negative_count':len(negative),'rejected_cases':negative,'read_only_write_denied':True,'source_bytes_unchanged':True,'trust_boundary':'Separate trusted original BOOTSTRAP.py authenticates each candidate tree; the bootstrap and manifest hashes must themselves be checked against external pins.'}
if __name__=='__main__':
    try:print(json.dumps(main(),sort_keys=True,indent=2))
    except (Failure,OSError,ValueError,KeyError,TypeError,subprocess.SubprocessError) as e:
        print('REJECT: '+str(e),file=sys.stderr);sys.exit(1)
