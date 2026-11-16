"""Narrow new source-only controls. No Git command, website or runtime access.
Only owned temporary FD fixtures under private/, removed before final closure.
Runtime content/extent fixtures are in-memory and have no actual authority.
"""
import copy
import json
import os
from pathlib import Path
import runpy
import tempfile
import custody as C
import mechanism as M

RESULTS=[]

def check(name,condition):
    C.need(condition,'control '+name);RESULTS.append({'control':name,'result':'PASS'})

def rejected(name,call):
    try:call()
    except (ValueError,FileNotFoundError) as e:RESULTS.append({'control':name,'result':'EXPECTED_REJECTION','actual_error':str(e)})
    else:raise ValueError('expected rejection missing '+name)

def native(o,oids):
    raw=C.read(Path(o['raw_index_reference']));targets={x.encode() for x in oids}
    old=C.parse_index(raw,targets);newraw=C.splice(raw,oids);new=C.parse_index(newraw,targets)
    check('actual58561-protected-record-bodies-identical',old['protected']==new['protected'] and len(old['protected'])==58561)
    check('actual58563-to58571-version2-checksum-and-only-TREE-invalidated',old['count']==58563 and new['count']==58571 and old['version']==new['version']==2 and len(old['extensions'])==1 and old['extensions'][0][0]=='TREE' and new['extensions']==[])
    rejected('corrupt-original-index-byte',lambda:C.splice(raw[:100]+bytes([raw[100]^1])+raw[101:],oids))
    mutated=dict(oids);mutated.pop(next(iter(mutated)));rejected('nine-path-plan-not-exact10',lambda:C.splice(raw,mutated))
    return newraw

def descriptors():
    with tempfile.TemporaryDirectory(prefix='fd-controls-',dir=C.N/'private') as d:
        root=Path(d);lock=root/'index.lock';index=root/'index'
        M.exclusive(index,b'old-index');fd=os.open(lock,os.O_RDWR|os.O_CREAT|os.O_EXCL,0o600)
        try:
            M.write_complete(fd,M.LOCK_BODY);short_calls=[];write=os.write
            def short(f,b):short_calls.append(len(b));return write(f,b[:7])
            os.write=short
            try:M.publish_buffer(b'new-validated-index'*100,index,lock,fd,0o640)
            finally:os.write=write
            check('short-write-loop-exercised',len(short_calls)>2)
            check('exact-validated-buffer-installed-owned-mode-preserved',index.read_bytes()==b'new-validated-index'*100 and (index.stat().st_mode&0o777)==0o640)
            check('distinct-index-lock-retained-through-publication-return',M.owned_entry(lock,fd) and lock.read_bytes()==M.LOCK_BODY)
            M.validate_owned_buffer(lock,fd,M.LOCK_BODY)
            rejected('same-FD-content-mismatch',lambda:M.validate_owned_buffer(lock,fd,b'wrong'))
            os.write=lambda *_:0
            try:rejected('zero-write-cannot-loop-forever',lambda:M.write_complete(fd,b'x'))
            finally:os.write=write
        finally:
            try:M.unlink_owned(lock,fd)
            finally:os.close(fd)
        check('owned-lock-cleaned-and-owned-FD-closed',not os.path.lexists(lock))
        foreign=root/'foreign';foreign.write_bytes(b'foreign')
        for kind in ('symlink','foreign-inode'):
            fd=os.open(lock,os.O_RDWR|os.O_CREAT|os.O_EXCL,0o600)
            try:
                lock.unlink()
                if kind=='symlink':lock.symlink_to(foreign)
                else:lock.write_bytes(b'foreign-entry')
                rejected('reject-substituted-'+kind,lambda:M.unlink_owned(lock,fd))
                check('never-unlinked-'+kind,os.path.lexists(lock) and foreign.read_bytes()==b'foreign')
                lock.unlink()
            finally:os.close(fd)
        check('no-extra-sibling-after-success-or-rejection',sorted(x.name for x in root.iterdir())==['foreign','index'])
        rejected('closed-namespace-extra-empty-directory',lambda:closed_fixture(root,True))
        fifo=root/'fifo';os.mkfifo(fifo)
        try:rejected('closed-namespace-reject-FIFO',lambda:C.extent(root))
        finally:fifo.unlink()

def closed_fixture(root,extra):
    before=C.extent(root)
    if extra:(root/'unlisted-empty').mkdir()
    try:C.need(C.extent(root)==before,'exact declared directory set changed')
    finally:
        if extra:(root/'unlisted-empty').rmdir()

def hook():
    accepted=runpy.run_path(str(C.N/'hooks/pre-push'))['accepted'];commit='1'*40;url='https://fixture.invalid/exact10.git'
    env={'EXACT10_PARENT':C.BASE,'EXACT10_COMMIT':commit,'EXACT10_URL_SHA256':C.sha(url.encode())}
    body=(commit+' '+commit+' refs/heads/master '+C.BASE+'\n').encode()
    check('strict-one-approved-update-actual-advertisement',accepted(['origin',url],env,body))
    for name,b in [('wrong-actual-remote-old-SHA',body.replace(C.BASE.encode(),b'0'*40)),('extra-ref',body+body),('deletion',body.replace(commit.encode(),b'0'*40))]:check('hook-reject-'+name,not accepted(['origin',url],env,b))
    check('hook-reject-different-destination',not accepted(['origin',url+'x'],env,body))

def runtime(oids,newraw):
    contract=json.loads(C.read(C.N/'RUNTIME_CONTRACT.json'));prep='4'*64
    template=json.loads(C.read(C.N/'ROOT_INSTALL_AUTHORITY_TEMPLATE.json'))
    rejected('disabled-install-template-is-not-actual-authority',lambda:C.authority(template,oids,prep,C.sha(C.encoded(contract))))
    a=copy.deepcopy(template);a.update(template_not_root_receipt=False,production_installation_authorized=True,current_mechanism_fully_adopted=True,independent_mechanism_audit_adopted=True,independent_mechanism_audit_SHA256='3'*64,preparation_seal_SHA256=prep,expected_blob_OIDs=oids)
    ab=C.encoded(a);authsha=C.sha(ab)
    pending={'parent':C.BASE,'commit':'1'*40,'tree':'2'*40,'gitpaths':sorted(oids),'blob_OIDs':oids,'protected_raw_SHA256':C.PROTECTED,'commit_index_SHA256':C.sha(b'fixture-not-a-Git-index'),'approved_index_SHA256':C.sha(newraw),'root_authority_SHA256':authsha}
    pb=C.encoded(pending)
    approval={'schema':'root-supported-cycle-focal-commit-v1','authority':'root','template_not_root_receipt':False,'publication_authorized':True,'preparation_seal_SHA256':prep,'root_install_authority_SHA256':authsha,'pending_commit_receipt_SHA256':C.sha(pb),**{k:pending[k] for k in ('parent','commit','tree','gitpaths','approved_index_SHA256','protected_raw_SHA256')}}
    available={'ROOT_AUTHORITY.json':ab,'GIT_LOG.json':b'[]\n','PRE_INSTALL.json':C.encoded({'parent':C.BASE,'index_SHA256':C.INDEX,'gitpaths':sorted(oids)}),'PENDING_COMMIT.json':pb,'commit.index':b'fixture-not-a-Git-index','shared-index.approved':newraw,'ROOT_COMMIT_APPROVAL.json':C.encoded(approval),'PRE_PUBLICATION.json':C.encoded({'parent':C.BASE,'commit':pending['commit'],'index_SHA256':C.INDEX}),'PUBLICATION.json':C.encoded({'commit':pending['commit'],'tree':pending['tree'],'index_SHA256':C.sha(newraw),'protected_raw_SHA256':C.PROTECTED,'remote_advertised_master':pending['commit']})}
    read,extent=C.read,C.extent;root=C.N/'private/not-created-runtime-fixture'
    try:
        for phase,plan in contract['phases'].items():
            buffers={n:available[n] for n in plan['files']}
            s={'phase':phase,'preparation_seal_SHA256':prep,'runtime_contract_SHA256':C.sha(C.encoded(contract)),'root_authority_SHA256':authsha,'root_commit_approval_SHA256':C.sha(available['ROOT_COMMIT_APPROVAL.json']) if phase=='PUBLISHED' else None,'files':{n:C.descriptor(b) for n,b in buffers.items()}}
            buffers['STATE.json']=C.encoded(s);actual_dirs=[]
            C.read=lambda p:buffers[p.name]
            C.extent=lambda p:(sorted(buffers),actual_dirs)
            check('finite-runtime-'+phase,C.runtime(root,contract,prep,oids)['phase']==phase)
            actual_dirs.append('unlisted-empty');rejected('runtime-reject-extra-directory-'+phase,lambda:C.runtime(root,contract,prep,oids));actual_dirs.clear()
            buffers['anonymous-future-state']=b'x';rejected('runtime-reject-unlisted-file-'+phase,lambda:C.runtime(root,contract,prep,oids));buffers.pop('anonymous-future-state')
            if phase=='PUBLISHED':
                broken=json.loads(buffers['PUBLICATION.json']);broken['commit']='5'*40;buffers['PUBLICATION.json']=C.encoded(broken)
                s['files']['PUBLICATION.json']=C.descriptor(buffers['PUBLICATION.json']);buffers['STATE.json']=C.encoded(s)
                rejected('rehashed-runtime-wrong-published-commit',lambda:C.runtime(root,contract,prep,oids))
    finally:C.read,C.extent=read,extent
    check('no-runtime-files-created',not os.path.lexists(root))

def main():
    C.need(not (C.N/'FINAL_SEAL.json').exists(),'new controls only before immutable FINAL')
    o=json.loads(C.read(C.N/'INPUT_ORACLE.json'));oids=C.oracle(o);newraw=native(o,oids)
    descriptors();hook();runtime(oids,newraw)
    print(json.dumps({'status':'PASS_NEW_BOUNDED_EXACT10_CONTROLS','controls':RESULTS,'count':len(RESULTS),'approved_raw_index_SHA256':C.sha(newraw),'website_Git_or_actual_runtime_access':False,'actual_production_authority':False},indent=2,sort_keys=True))

if __name__=='__main__':main()
