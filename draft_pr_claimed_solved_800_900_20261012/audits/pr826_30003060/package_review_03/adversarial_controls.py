#!/usr/bin/env python3
"""Fresh independent adversarial controls; fixture pins are structural test authority only."""
from pathlib import Path
import copy, datetime, hashlib, io, json, os, shutil, socket, stat, subprocess, sys, time, warnings, zipfile
R=Path(__file__).resolve().parent; A=R.parent
S=json.loads((A/'PACKAGE_SEAL_R2.json').read_text()); T=Path(S['assembly_tree'])
I=T/'publication_20261014/verification_package'; D=R/'replays/independent malformed fixtures'
if D.exists():shutil.rmtree(D)
D.mkdir()
checks=[]
def sha(b):return hashlib.sha256(b).hexdigest()
def record(label,p,expect_success=False,timeout=False,marker=None,extra=None):
    passed=(p=='TIMEOUT') if timeout else p!='TIMEOUT' and ((p.returncode==0)==expect_success)
    if marker and marker.exists():passed=False
    row={'label':label,'passed':passed,'expected_success':expect_success,'expected_historical_timeout':timeout}
    if p=='TIMEOUT':row.update({'timeout':True})
    else:row.update({'returncode':p.returncode,'stderr_tail':p.stderr[-700:],'stdout_bytes':len(p.stdout)})
    if extra:row.update(extra)
    checks.append(row)
def run(cmd,cwd='/',env=None,timeout=10):
    try:return subprocess.run(cmd,cwd=cwd,env=env,capture_output=True,text=True,timeout=timeout)
    except subprocess.TimeoutExpired:return 'TIMEOUT'
def fixture(source,label):
    root=D/label;shutil.copytree(source,root);return root
def pin(root,outer=False):return sha((root/('PUBLICATION_MANIFEST.json' if outer else 'package_index.json')).read_bytes())
def rebind(root,outer=False):
    index=root/('PUBLICATION_MANIFEST.json' if outer else 'package_index.json');m=json.loads(index.read_text())
    for row in m['files']:
        p=root/row['path']
        if p.is_file() and not p.is_symlink():row['bytes']=p.stat().st_size;row['sha256']=sha(p.read_bytes())
    index.write_text(json.dumps(m,indent=2)+'\n');return pin(root,outer)
def vcmd(root,opt=False,outer=False,flags=None):
    return [sys.executable,*(flags if flags is not None else ['-I','-S','-B']),*(['-O'] if opt else []),str(root/('verify_publication.py' if outer else 'verify_package.py'))]
def builder(root,opt,out=None,checker=None):
    return [sys.executable,'-I','-S','-B',*(['-O'] if opt else []),str(checker or A/'preprint/build_verification.py'),'--from-package',str(root),'--trusted-index-sha256',S['index_sha256'],'--output-root',str(out or D/('out '+root.name+str(opt)))]
def replace_special(p,kind):
    raw=p.read_bytes() if p.is_file() else None
    if p.is_dir():shutil.rmtree(p)
    else:p.unlink()
    sock=None
    if kind=='fifo':os.mkfifo(p)
    elif kind=='directory':p.mkdir()
    elif kind=='symlink':
        q=D/('target '+str(len(checks)));q.write_bytes(raw or b'');p.symlink_to(q)
    elif kind=='socket':
        sock=socket.socket(socket.AF_UNIX)
        previous=Path.cwd()
        try:os.chdir(p.parent);sock.bind(p.name)
        finally:os.chdir(previous)
    return sock
def mutate(root,kind,outer):
    index=root/('PUBLICATION_MANIFEST.json' if outer else 'package_index.json')
    target=root/('README.md' if outer else 'note.tex')
    directory=root/('author' if outer else 'algebra_audit_01')
    if kind=='missing':target.unlink()
    elif kind=='extra':(root/'extra').write_bytes(b'x')
    elif kind=='same_size':
        b=bytearray(target.read_bytes());b[len(b)//2]^=1;target.write_bytes(b)
    elif kind=='empty_dir':(root/'empty extra').mkdir()
    elif kind=='member_symlink':replace_special(target,'symlink')
    elif kind=='member_fifo':replace_special(target,'fifo')
    elif kind=='member_dir':replace_special(target,'directory')
    elif kind=='member_socket':return replace_special(target,'socket')
    elif kind=='index_fifo':replace_special(index,'fifo')
    elif kind=='index_symlink':replace_special(index,'symlink')
    elif kind=='index_dir':replace_special(index,'directory')
    elif kind=='index_socket':return replace_special(index,'socket')
    elif kind=='directory_symlink':
        dest=D/('saved '+str(len(checks)));shutil.move(directory,dest);directory.symlink_to(dest,target_is_directory=True)
    elif kind=='directory_fifo':replace_special(directory,'fifo')
    elif kind=='directory_file':
        shutil.rmtree(directory);directory.write_bytes(b'wrong type')
for outer in [False,True]:
    source=T if outer else I
    for opt in [False,True]:
        prefix=('outer' if outer else 'portable')+str(opt)
        for mutation in ['missing','extra','same_size','empty_dir','member_symlink','member_fifo','member_dir','member_socket','index_fifo','index_symlink','index_dir','index_socket','directory_symlink','directory_fifo','directory_file']:
            root=fixture(source,prefix+mutation);sock=mutate(root,mutation,outer);p=run(vcmd(root,opt,outer)+[S['outer_manifest_sha256'] if outer else S['index_sha256']]);record(prefix+' '+mutation,p)
            if sock:sock.close()
        for flagset in [[],['-I','-B'],['-I','-S']]:
            record(prefix+' missing flags '+str(flagset),run(vcmd(source,opt,outer,flagset)+[S['outer_manifest_sha256'] if outer else S['index_sha256']]))
        record(prefix+' wrong external pin',run(vcmd(source,opt,outer)+['0'*64]))
        for mutation in ['duplicate_keys','duplicate_rows','traversal','absolute','backslash','alias','double_slash','self_index','size_bool','size_string']:
            root=fixture(source,prefix+mutation);idx=root/('PUBLICATION_MANIFEST.json' if outer else 'package_index.json');m=json.loads(idx.read_text())
            if mutation=='duplicate_keys':idx.write_text('{"schema":"bad",'+idx.read_text()[1:])
            else:
                if mutation=='duplicate_rows':m['files'].append(copy.deepcopy(m['files'][0]))
                elif mutation=='size_bool':m['files'][0]['bytes']=True
                elif mutation=='size_string':m['files'][0]['bytes']=str(m['files'][0]['bytes'])
                else:m['files'][0]['path']={'traversal':'../escape','absolute':'/escape','backslash':'x\\y','alias':'./README.md','double_slash':'a//b','self_index':idx.name}[mutation]
                idx.write_text(json.dumps(m))
            record(prefix+' coherent fixture '+mutation,run(vcmd(root,opt,outer)+[pin(root,outer)]),extra={'fixture_pin_not_public_authority':True})
        hostile=D/(prefix+' hostile cwd');hostile.mkdir();marker=hostile/'executed'
        for mod in ['sitecustomize','usercustomize','hashlib','json','subprocess','zipfile','pathlib']:(hostile/(mod+'.py')).write_text('from pathlib import Path\nPath('+repr(str(marker))+').touch()\nraise Exception("hostile")\n')
        env=dict(os.environ,PYTHONPATH=str(hostile),PYTHONHOME=str(hostile),PYTHONOPTIMIZE='2')
        record(prefix+' hostile cwd/environment',run(vcmd(source,opt,outer)+[S['outer_manifest_sha256'] if outer else S['index_sha256']],cwd=hostile,env=env),expect_success=True,marker=marker)
for opt in [False,True]:
    for which in ['package_index.json','verify_package.py','note.tex','algebra_audit_01']:
        kinds=['fifo','directory','symlink','socket'] if which!='algebra_audit_01' else ['fifo','symlink']
        for kind in kinds:
            # Use short names to stay within the Unix socket pathname limit.
            root=fixture(I,'b'+str(len(checks)));sock=replace_special(root/which,kind);out=D/('output '+str(len(checks)))
            p=run(builder(root,opt,out),timeout=3);record('builder '+str(opt)+' '+which+' '+kind,p,extra={'output_absent':not out.exists()})
            if out.exists():checks[-1]['passed']=False
            if sock:sock.close()
    root=fixture(I,'builderchecker'+str(opt));marker=D/('checker executed '+str(opt));(root/'verify_package.py').write_text('from pathlib import Path\nPath('+repr(str(marker))+').touch()\n')
    record('builder rejects substituted verifier before launch '+str(opt),run(builder(root,opt)),marker=marker)
    # A coherent changed index is still unauthorized under the original external pin.
    rebind(root);record('builder rejects coherent substitution original pin '+str(opt),run(builder(root,opt)),marker=marker)
    out=D/('nonempty '+str(opt));out.mkdir();canary=out/'canary';canary.write_bytes(b'preserve')
    record('builder preserves nonempty output '+str(opt),run(builder(I,opt,out)),extra={'canary_preserved':canary.read_bytes()==b'preserve','entries':len(list(out.iterdir()))})
    for out in [I,I/'nested output']:
        record('builder refuses input/nested output '+str(opt)+str(out.name),run(builder(I,opt,out)))
    old=fixture(Path(json.loads((A/'PACKAGE_SEAL_R1.json').read_text())['assembly_tree'])/'publication_20261014/verification_package','old FIFO '+str(opt));replace_special(old/'package_index.json','fifo')
    record('historical R1 FIFO reproduced '+str(opt),run(builder(old,opt,checker=old/'build_verification.py'),timeout=2),timeout=True)
for opt in [False,True]:
    for what in ['metadata','pdf','zip_duplicate','zip_traversal','zip_alias','zip_symlink','zip_fifo','zip_missing','zip_extra']:
        root=fixture(T,'coherent outer '+str(opt)+what);pre=root/'publication_20261014/preprint'
        if what=='metadata':
            m=json.loads((pre/'metadata.json').read_text());m['creators'][0]['orcid']='bad';(pre/'metadata.json').write_text(json.dumps(m))
        elif what=='pdf':
            p=pre/'output/pdf/note.pdf';p.write_bytes(p.read_bytes()+b' ')
        else:
            p=pre/'verification.zip';buf=io.BytesIO(p.read_bytes())
            with zipfile.ZipFile(buf) as src,zipfile.ZipFile(p,'w') as dst:
                for n,inf in enumerate(src.infolist()):
                    if what=='zip_missing' and n==0:continue
                    data=src.read(inf)
                    if what=='zip_symlink' and n==0:inf.external_attr=(stat.S_IFLNK|0o777)<<16
                    if what=='zip_fifo' and n==0:inf.external_attr=(stat.S_IFIFO|0o600)<<16
                    dst.writestr(inf,data)
                if what=='zip_duplicate':
                    with warnings.catch_warnings():warnings.simplefilter('ignore');dst.writestr(src.infolist()[0],src.read(src.infolist()[0]))
                if what in ['zip_traversal','zip_extra']:dst.writestr('../escaped' if what=='zip_traversal' else 'extra',b'x')
                if what=='zip_alias':dst.writestr('./README.md',b'x')
        record('outer coherent fixture '+str(opt)+' '+what,run(vcmd(root,opt,True)+[rebind(root,True)]),extra={'fixture_pin_not_public_authority':True})
for outer in [False,True]:
    source=T if outer else I;name='verify_publication.py' if outer else 'verify_package.py'
    approved=sha((source/name).read_bytes())
    for opt in [False,True]:
        root=fixture(source,'startup binding '+str(outer)+str(opt));script=root/name;marker=D/('bad startup '+str(outer)+str(opt))
        script.write_text('from pathlib import Path\nPath('+repr(str(marker))+').touch()\n')
        refused=sha(script.read_bytes())!=approved
        checks.append({'label':'independent external startup hash refuses substituted entrypoint '+str(outer)+str(opt),'passed':refused and not marker.exists(),'startup_executed':False,'original_entrypoint_sha256':approved})
receipt={'timestamp_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'control_count':len(checks),'all_passed':all(x['passed'] for x in checks),'controls':checks,'threat_model':'Static malformed tree and startup controls; fixture pins test structure, not public authorization. No race, hostile OS/Python or sandbox guarantee.'}
(R/'INDEPENDENT_CONTROLS.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps({'control_count':len(checks),'all_passed':receipt['all_passed'],'failed':[r for r in checks if not r['passed']]}))
