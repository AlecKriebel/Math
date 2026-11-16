"""Future root-authorized exact10 installation/commit/push; NOT run in preparation.
Two explicit actions, with separate fixed actual root receipts. No deployment.
Public files, native index, local ref and remote are not one transaction. Failures
stop for root inspection, with literal command streams; no rollback or resume.
Stable sealed/runtime namespaces and cooperative Git writers are assumptions.
"""
import base64
from datetime import datetime,timezone
import json
import os
from pathlib import Path
import stat
import subprocess
import sys
import tempfile
import custody as C

LOCK_BODY=b'root-supported-cycle-focal-exact10-owned-index-sentinel-v1\n'
LOG=[]

def owned_entry(path,fd,missing_ok=False):
    try:p=path.lstat()
    except FileNotFoundError:
        C.need(missing_ok,'owned entry disappeared '+str(path));return False
    f=os.fstat(fd)
    C.need(stat.S_ISREG(p.st_mode) and stat.S_ISREG(f.st_mode) and (p.st_dev,p.st_ino)==(f.st_dev,f.st_ino),'owned ordinary inode '+str(path))
    return True

def write_complete(fd,body):
    view=memoryview(body);offset=0
    while offset<len(view):
        try:n=os.write(fd,view[offset:])
        except InterruptedError:continue
        C.need(isinstance(n,int) and 0<n<=len(view)-offset,'complete write makes progress');offset+=n

def validate_owned_buffer(path,fd,expected):
    owned_entry(path,fd);os.fsync(fd);os.lseek(fd,0,os.SEEK_SET);parts=[]
    while True:
        try:b=os.read(fd,1024*1024)
        except InterruptedError:continue
        if not b:break
        parts.append(b)
    C.need(b''.join(parts)==expected,'same owned FD whole-byte readback');owned_entry(path,fd)

def unlink_owned(path,fd):
    if owned_entry(path,fd,missing_ok=True):path.unlink()

def sync_dir(path):
    fd=os.open(path,os.O_RDONLY)
    try:os.fsync(fd)
    finally:os.close(fd)

def publish_buffer(newraw,destination,lock,lock_fd,mode):
    """Write validated bytes to an owned O_RDWR sibling, not an alternate index.
    Distinct index.lock sentinel remains held through caller's ref/push sequence.
    lstat/fstat/content checks do not remove the final check-to-rename window.
    """
    fd,name=tempfile.mkstemp(prefix='.supported-cycle-focal-index-',dir=destination.parent);temp=Path(name)
    try:
        os.fchmod(fd,mode);write_complete(fd,newraw);validate_owned_buffer(temp,fd,newraw)
        validate_owned_buffer(lock,lock_fd,LOCK_BODY);owned_entry(temp,fd)
        os.replace(temp,destination)
        validate_owned_buffer(destination,fd,newraw)
    finally:
        try:unlink_owned(temp,fd)
        finally:os.close(fd)

def exclusive(path,body,mode=0o600):
    fd=os.open(path,os.O_RDWR|os.O_CREAT|os.O_EXCL,mode)
    try:write_complete(fd,body);validate_owned_buffer(path,fd,body)
    finally:os.close(fd)

def replace_owned_metadata(path,body):
    """Only future runtime metadata. An interrupted checkpoint fails closed."""
    fd,name=tempfile.mkstemp(prefix='.checkpoint-',dir=path.parent);temp=Path(name)
    try:
        write_complete(fd,body);validate_owned_buffer(temp,fd,body);owned_entry(temp,fd);os.replace(temp,path);sync_dir(path.parent)
    finally:
        try:unlink_owned(temp,fd)
        finally:os.close(fd)

def git(args,body=None,index=None,hook=False,extra_env=None):
    C.need(args[0] in {'rev-parse','symbolic-ref','remote','ls-remote','diff','read-tree','hash-object','update-index','write-tree','commit-tree','cat-file','diff-tree','ls-tree','update-ref','push'},'finite future Git vocabulary')
    env={k:v for k,v in os.environ.items() if not k.startswith('GIT_')}
    env['GIT_OPTIONAL_LOCKS']='0'
    if index is not None:env['GIT_INDEX_FILE']=str(index)
    if extra_env:env.update(extra_env)
    command=['git','-c','core.fsmonitor=false','-c','index.version=2','-c','commit.gpgsign=false','-c','core.hooksPath='+str(C.N/'hooks' if hook else '/dev/null'),*args]
    try:
        r=subprocess.run(command,cwd=C.W,env=env,input=body,stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=60)
        output,error,code,timeout=r.stdout,r.stderr,r.returncode,False
    except subprocess.TimeoutExpired as e:output,error,code,timeout=e.output or b'',e.stderr or b'',None,True
    LOG.append({'UTC':datetime.now(timezone.utc).isoformat(),'argv':command,'alternate_index':str(index) if index else None,'stdin':C.descriptor(body) if body is not None else None,'stdout_base64':base64.b64encode(output).decode(),'stderr_base64':base64.b64encode(error).decode(),'actual_exit':code,'timed_out':timeout})
    replace_owned_metadata(C.RUNTIME/'GIT_LOG.json',C.encoded(LOG))
    C.need(code==0 and not timeout,'actual future Git failure; literal streams preserved; stop, no retry')
    return output

def context():
    prep=C.preparation_seal();o=C.inputs();oids=C.oracle(o)
    old=next(r for r in o['closed_reference_packets'] if r['kind']=='old');oldroot=Path(old['root'])
    baseline=json.loads(C.read(oldroot/'WEBSITE_BASELINE.json'))
    contractb=C.read(C.N/'RUNTIME_CONTRACT.json');contract=json.loads(contractb)
    C.need(contractb==C.encoded(contract),'canonical runtime buffer')
    return prep,o,oids,oldroot,baseline,contract

def root_install(pin,prep,oids,contract):
    b=C.read(C.INSTALL_AUTH);C.need(len(pin)==64 and C.sha(b)==pin,'explicit whole actual root install authority SHA256')
    a=json.loads(b);C.authority(a,oids,prep,C.sha(C.encoded(contract)))
    return b

def public_check(o,oldroot,baseline,installed,head):
    targets={r['path']:r for r in o['exact10']}
    additions=[r['path'] for r in o['exact10'] if r['action']=='add']
    newdirs=sorted({str(Path(r).parent) for r in additions})
    names=sorted([*baseline['public_namespace'],*additions]) if installed else baseline['public_namespace']
    dirs=sorted([*baseline['public_directories'],*newdirs]) if installed else baseline['public_directories']
    C.need(C.extent(C.W/'public')==(names,dirs),'whole finite public files/directories')
    for r in baseline['files']:
        p=Path(r['path']);b=C.read(p)
        if r['role']=='public' and installed and p.relative_to(C.W/'public').as_posix() in targets:
            row=targets[p.relative_to(C.W/'public').as_posix()];C.need(b==C.pinned(Path(row['source']),row),'whole approved aggregate bytes')
        elif p==C.W/'.git/refs/heads/master':C.need(b==head.encode()+b'\n','literal actual master control')
        else:C.need(b==C.pinned(oldroot/r['blob'],r),'all unrelated public/config/control bytes')
    for r in o['exact10']:
        p=C.W/'public'/r['path']
        if installed:C.need(C.read(p)==C.pinned(Path(r['source']),r),'whole exact output')
        elif r['action']=='add':C.need(not os.path.lexists(p),'new leaf absent')

def live(o,oldroot,baseline,installed,head,raw,held_lock=None):
    C.need(git(['rev-parse','--show-toplevel']).decode().strip()==str(C.W),'fixed website repo')
    C.need(git(['symbolic-ref','HEAD']).strip()==b'refs/heads/master','fixed master branch')
    values=git(['rev-parse','HEAD','refs/heads/master']).decode().splitlines();C.need(values==[head,head],'actual HEAD/master')
    if head==C.BASE:C.need(git(['rev-parse','HEAD^{tree}']).strip().decode()==C.TREE,'actual old tree')
    urls=git(['remote','get-url','--push','--all','origin']).splitlines();C.need(len(urls)==1 and C.sha(urls[0])==baseline['Git']['origin_push_URL_SHA256'],'single exact bound push URL')
    C.need(git(['ls-remote','--refs',urls[0].decode(),'refs/heads/master']).split()==[head.encode(),b'refs/heads/master'],'actual remote advertised expected old/new SHA')
    C.need(C.read(C.W/'.git/index')==raw,'complete expected raw shared index buffer')
    if held_lock is None:C.need(not os.path.lexists(C.W/'.git/index.lock'),'no competing native lock')
    else:validate_owned_buffer(C.W/'.git/index.lock',held_lock,LOCK_BODY)
    public_check(o,oldroot,baseline,installed,head)
    # These sources are outside the website; re-read whole pinned originals too.
    C.inputs()
    return urls[0].decode()

def checkpoint(phase,contract,prep,auth_sha,approval_sha=None):
    replace_owned_metadata(C.RUNTIME/'GIT_LOG.json',C.encoded(LOG))
    names=contract['phases'][phase]['files'];files={n:C.descriptor(C.read(C.RUNTIME/n)) for n in names}
    s={'phase':phase,'preparation_seal_SHA256':prep,'runtime_contract_SHA256':C.sha(C.encoded(contract)),'root_authority_SHA256':auth_sha,'root_commit_approval_SHA256':approval_sha,'files':files}
    replace_owned_metadata(C.RUNTIME/'STATE.json',C.encoded(s))
    return C.runtime(C.RUNTIME,contract,prep,C.oracle(json.loads(C.read(C.N/'INPUT_ORACLE.json'))))

def safe_parent(path):
    C.need(path.is_relative_to(C.W/'public'),'exact public destination')
    q=path.parent
    while q!=C.W:
        C.need(q.resolve()==q and stat.S_ISDIR(q.lstat().st_mode),'ordinary existing public ancestor');q=q.parent

def article_write(path,body,old=None):
    safe_parent(path)
    if old is None:C.need(not os.path.lexists(path),'no-clobber article leaf')
    else:C.need(C.read(path)==old,'exact expected-before aggregate')
    fd,name=tempfile.mkstemp(prefix='.exact10-',dir=path.parent);temp=Path(name)
    try:
        os.fchmod(fd,0o644);write_complete(fd,body);validate_owned_buffer(temp,fd,body)
        if old is None:os.link(temp,path)  # Atomic no-clobber, same fully validated inode.
        else:
            C.need(C.read(path)==old,'aggregate expected-before immediately before replace')
            owned_entry(temp,fd);os.replace(temp,path)
        validate_owned_buffer(path,fd,body);sync_dir(path.parent)
    finally:
        try:unlink_owned(temp,fd)
        finally:os.close(fd)

def validate_commit(commit,oids):
    C.need(len(commit)==40 and bytes.fromhex(commit).hex()==commit,'actual immutable commit OID')
    data=git(['cat-file','commit',commit]);header=data.split(b'\n\n',1)[0].splitlines()
    trees=[x[5:].decode() for x in header if x.startswith(b'tree ')];parents=[x[7:].decode() for x in header if x.startswith(b'parent ')]
    C.need(len(trees)==1 and parents==[C.BASE],'exact one parent and tree')
    diff=git(['diff-tree','--no-renames','--no-commit-id','--name-only','-r','-z',C.BASE,commit])
    C.need(diff.split(b'\0')[:-1]==[p.encode() for p in sorted(oids)],'whole actual commit tree diff exactly ten paths')
    entries=git(['ls-tree','-r','-z',commit,'--',*sorted(oids)]).split(b'\0')[:-1]
    expected=[b'100644 blob '+oids[p].encode()+b'\t'+p.encode() for p in sorted(oids)]
    C.need(entries==expected,'actual tree exact ten modes and candidate blob identities')
    return trees[0]

def install(auth_pin):
    prep,o,oids,oldroot,baseline,contract=context();authb=root_install(auth_pin,prep,oids,contract)
    # This is the first mutation, possible only after actual future authority.
    C.RUNTIME.mkdir();exclusive(C.RUNTIME/'ROOT_AUTHORITY.json',authb)
    exclusive(C.RUNTIME/'GIT_LOG.json',b'[]\n')
    raw=C.read(Path(o['raw_index_reference']));newraw=C.splice(raw,oids)
    pre={'parent':C.BASE,'index_SHA256':C.INDEX,'gitpaths':sorted(oids),'protected_raw_SHA256':C.PROTECTED}
    exclusive(C.RUNTIME/'PRE_INSTALL.json',C.encoded(pre));checkpoint('INSTALL_STARTED',contract,prep,auth_pin)
    live(o,oldroot,baseline,False,C.BASE,raw)
    dirs=sorted({(C.W/'public'/r['path']).parent for r in o['exact10'] if r['action']=='add'})
    C.need(len(dirs)==2,'two new article roots')
    for d in dirs:C.need(not os.path.lexists(d),'new article root absent');safe_parent(d);d.mkdir();sync_dir(d.parent)
    oldfiles={Path(r['path']):r for r in baseline['files']}
    for r in o['exact10']:
        destination=C.W/'public'/r['path'];before=C.pinned(oldroot/oldfiles[destination]['blob'],oldfiles[destination]) if r['action']=='replace' else None
        article_write(destination,C.pinned(Path(r['source']),r),before)
    live(o,oldroot,baseline,True,C.BASE,raw)
    alternate=C.RUNTIME/'commit.index';C.need(not os.path.lexists(alternate),'fresh separate HEAD-seeded index')
    git(['read-tree',C.BASE],index=alternate)
    for r in o['exact10']:
        body=C.pinned(Path(r['source']),r);oid=git(['hash-object','-w','--no-filters','--stdin'],body=body).strip().decode();path='public/'+r['path']
        C.need(oid==oids[path],'actual unchanged candidate blob')
        git(['update-index','--add','--cacheinfo','100644',oid,path],index=alternate)
    diff=git(['diff','--cached','--no-renames','--name-only','-z',C.BASE],index=alternate)
    C.need(diff.split(b'\0')[:-1]==[p.encode() for p in sorted(oids)],'HEAD-seeded alternate diff exactly ten')
    git(['diff','--cached','--check',C.BASE],index=alternate)
    tree=git(['write-tree'],index=alternate).strip().decode()
    commit=git(['commit-tree',tree,'-p',C.BASE],body=b'Publish supported-cycle and focal-distance research articles\n').strip().decode()
    C.need(validate_commit(commit,oids)==tree,'actual prepared commit tree')
    live(o,oldroot,baseline,True,C.BASE,raw)
    exclusive(C.RUNTIME/'shared-index.approved',newraw)
    pending={'parent':C.BASE,'commit':commit,'tree':tree,'gitpaths':sorted(oids),'blob_OIDs':oids,'commit_index_SHA256':C.sha(C.read(alternate)),'approved_index_SHA256':C.sha(newraw),'protected_raw_SHA256':C.PROTECTED,'root_authority_SHA256':auth_pin,'publication_authorized':False}
    exclusive(C.RUNTIME/'PENDING_COMMIT.json',C.encoded(pending));checkpoint('INSTALLED',contract,prep,auth_pin)
    print(json.dumps({'status':'INSTALLED_COMMIT_PENDING_SEPARATE_ROOT_APPROVAL','pending':str(C.RUNTIME/'PENDING_COMMIT.json'),'commit':commit,'local_ref_and_remote_unchanged':True,'deployment_performed':False},sort_keys=True))

def publish(auth_pin,approval_pin):
    prep,o,oids,oldroot,baseline,contract=context();authb=root_install(auth_pin,prep,oids,contract)
    C.need(C.runtime(C.RUNTIME,contract,prep,oids)['phase']=='INSTALLED','exact durable installed state; no automatic recovery')
    C.need(C.read(C.RUNTIME/'ROOT_AUTHORITY.json')==authb,'same actual install authority')
    LOG.extend(json.loads(C.read(C.RUNTIME/'GIT_LOG.json')))
    pendingb=C.read(C.RUNTIME/'PENDING_COMMIT.json');p=json.loads(pendingb)
    ab=C.read(C.COMMIT_AUTH);C.need(len(approval_pin)==64 and C.sha(ab)==approval_pin,'explicit actual root commit approval SHA256')
    C.commit_authority(json.loads(ab),p,C.sha(pendingb),auth_pin,prep)
    C.need(validate_commit(p['commit'],oids)==p['tree'],'revalidate actual prepared commit')
    raw=C.read(Path(o['raw_index_reference']));newraw=C.splice(raw,oids)
    C.need(newraw==C.read(C.RUNTIME/'shared-index.approved') and C.sha(newraw)==p['approved_index_SHA256'],'already validated exact approved buffer')
    live(o,oldroot,baseline,True,C.BASE,raw)
    index=C.W/'.git/index';mode=stat.S_IMODE(index.lstat().st_mode);lock=C.W/'.git/index.lock'
    C.need(mode==json.loads(C.read(C.N/'PRE_GUARD.json'))['Git']['index_mode'],'preserve fresh originally captured native index file mode')
    fd=os.open(lock,os.O_RDWR|os.O_CREAT|os.O_EXCL,0o600)
    try:
        write_complete(fd,LOCK_BODY);validate_owned_buffer(lock,fd,LOCK_BODY)
        live(o,oldroot,baseline,True,C.BASE,raw,fd)
        exclusive(C.RUNTIME/'ROOT_COMMIT_APPROVAL.json',ab)
        exclusive(C.RUNTIME/'PRE_PUBLICATION.json',C.encoded({'parent':C.BASE,'commit':p['commit'],'index_SHA256':C.INDEX,'approved_index_SHA256':C.sha(newraw)}))
        publish_buffer(newraw,index,lock,fd,mode);sync_dir(index.parent)
        # Native lock remains owned and held. Ref mutation is atomic old-value CAS.
        validate_owned_buffer(lock,fd,LOCK_BODY)
        git(['update-ref','refs/heads/master',p['commit'],C.BASE])
        C.need(C.read(index)==newraw,'exact published raw buffer before push')
        validate_owned_buffer(lock,fd,LOCK_BODY)
        urls=git(['remote','get-url','--push','--all','origin']).splitlines()
        C.need(len(urls)==1 and C.sha(urls[0])==baseline['Git']['origin_push_URL_SHA256'],'actual bound push destination')
        C.need(git(['ls-remote','--refs',urls[0].decode(),'refs/heads/master']).split()==[C.BASE.encode(),b'refs/heads/master'],'actual remote old SHA immediately before strict nonforce push')
        hook_env={'EXACT10_PARENT':C.BASE,'EXACT10_COMMIT':p['commit'],'EXACT10_URL_SHA256':C.sha(urls[0])}
        C.need(stat.S_IMODE((C.N/'hooks/pre-push').lstat().st_mode)==0o555,'sealed executable strict hook')
        git(['push','--porcelain','--no-follow-tags','--recurse-submodules=no','origin',p['commit']+':refs/heads/master'],hook=True,extra_env=hook_env)
        live(o,oldroot,baseline,True,p['commit'],newraw,fd)
        C.need(validate_commit(p['commit'],oids)==p['tree'],'final actual tree still exact')
        exclusive(C.RUNTIME/'PUBLICATION.json',C.encoded({'commit':p['commit'],'tree':p['tree'],'index_SHA256':C.sha(newraw),'protected_raw_SHA256':C.PROTECTED,'remote_advertised_master':p['commit'],'deployment_performed':False}))
        checkpoint('PUBLISHED',contract,prep,auth_pin,approval_pin)
    finally:
        # Reject a substituted symlink or foreign inode; never blindly unlink.
        try:unlink_owned(lock,fd)
        finally:os.close(fd)
    print(json.dumps({'status':'PUBLISHED_EXACT10_AFTER_SEPARATE_ROOT_APPROVAL','commit':p['commit'],'deployment_performed':False},sort_keys=True))

def main():
    args=sys.argv[1:]
    C.need((len(args)==2 and args[0]=='install') or (len(args)==3 and args[0]=='publish'),'future explicit install <actual-root-SHA256> OR publish <install-SHA256> <separate-commit-SHA256>; preparation grants neither')
    if args[0]=='install':install(args[1])
    else:publish(args[1],args[2])

if __name__=='__main__':main()
