"""Independent staged publisher fault controls: owned synthetic paths only."""
from pathlib import Path
import datetime,hashlib,json,os,tempfile,types
HERE=Path(__file__).resolve().parent
CASE=HERE.parent

def pin(raw):return {'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()}
def module(name,path,raw):
    m=types.ModuleType(name);m.__file__=str(path);exec(compile(raw,str(path),'exec'),m.__dict__);return m

def main():
    src=(CASE/'root_terminal_source_preparation_02/ROOT_TERMINAL_INSPECTION.py').read_bytes()
    primitive=(CASE/'native_administrative_preparation_01/native212_primitives.py').read_bytes()
    assert pin(primitive)=={'bytes':16405,'sha256':'5971428cd56b4fbbabb41a985f6a36599aea4f69e46fa048f88b971e405d9df9'}
    results=[]
    with tempfile.TemporaryDirectory(prefix='_owned_publisher_independent_',dir=HERE) as tmp:
        for label in ['success','guard_fail','pending_file_fsync','pending_dir_fsync','pending_mode',
                      'pending_inode','link_known_collision','unknown_link_absent','unknown_link_present',
                      'published_dir_fsync','published_readback','identity_first','identity_last',
                      'pending_cleanup','cleanup_dir_fsync','existing_final']:
            checkout=Path(tmp)/label/'checkout';a=checkout/'program/audits/pr212_30005310'
            s=a/'root_terminal_source_preparation_02';b=a/'native_administrative_preparation_01'
            s.mkdir(parents=True);b.mkdir()
            t=module('owned_publisher_'+label,s/'ROOT_TERMINAL_INSPECTION.py',src)
            e=module('owned_primitives_'+label,b/'native212_primitives.py',primitive)
            target=a/'ROOT_ACTUAL_ADMINISTRATIVE_SKIP_VERIFICATION_01.json'
            payload=t.enc({'explicitly_synthetic':True,'accepted':True,'advance_to_next_PR_authorized_now':True})
            events=[];identity_calls=0;guard_calls=0
            def pending():return list(a.glob('.pr212-root-terminal-pending-*'))
            class Ops:
                fsyncs=0;links=0
                def fsync(self,fd):
                    self.fsyncs+=1;events.append('fsync'+str(self.fsyncs))
                    failures={'pending_file_fsync':1,'pending_dir_fsync':2,'published_dir_fsync':3,'cleanup_dir_fsync':4}
                    if label in failures and self.fsyncs==failures[label]:raise OSError('owned synthetic durability failure')
                    if label=='published_readback' and self.fsyncs==3:
                        target.chmod(0o644);target.write_bytes(b'owned synthetic changed final')
                    return os.fsync(fd)
                def link(self,*args,**kwargs):
                    self.links+=1;events.append('link')
                    if label=='unknown_link_absent':raise OSError('owned uncertain link without actual link')
                    if label=='link_known_collision':target.write_bytes(b'owned incumbent');target.chmod(0o444)
                    os.link(*args,**kwargs)
                    if label=='unknown_link_present':raise OSError('owned uncertain link after actual link')
                def unlink(self,*args,**kwargs):
                    events.append('unlink')
                    if label=='pending_cleanup':raise OSError('owned pending cleanup failure')
                    return os.unlink(*args,**kwargs)
            ops=Ops()
            def final_guard():
                nonlocal guard_calls
                guard_calls+=1;events.append('final_guard')
                assert not target.exists() and len(pending())==1
                assert t.readonly(pending()[0])==payload and ops.fsyncs>=2
                if label=='guard_fail':raise RuntimeError('owned mutable guard failure before publication')
                if label=='pending_mode':pending()[0].chmod(0o644)
                if label=='pending_inode':
                    p=pending()[0];p.unlink();p.write_bytes(payload);p.chmod(0o444)
            def identity_guard():
                nonlocal identity_calls
                identity_calls+=1;events.append('identity'+str(identity_calls))
                assert target.exists()
                if label=='identity_first' or label=='identity_last' and identity_calls==2:
                    raise RuntimeError('owned immutable identity uncertainty')
                assert target.read_bytes()==payload
            if label=='existing_final':target.write_bytes(b'owned incumbent');target.chmod(0o444)
            outcome='success';details=None
            try:t.exclusive_root_receipt(e,target,payload,final_guard,identity_guard,local_ops=ops)
            except t.TerminalPublicationUncertain as ex:outcome='publication_uncertain';details=ex.details
            except (RuntimeError,OSError) as ex:outcome=type(ex).__name__
            if label=='success':
                assert outcome=='success' and target.read_bytes()==payload and not pending()
                assert guard_calls==1 and identity_calls==2 and ops.links==1
                assert events.index('fsync2')<events.index('final_guard')<events.index('link')<events.index('identity1')
            elif label in ['guard_fail','pending_file_fsync','pending_dir_fsync','pending_mode','pending_inode']:
                assert not target.exists() and ops.links==0 and outcome!='success'
                if label=='pending_inode':assert len(pending())==1
            elif label=='existing_final':
                assert outcome=='FileExistsError' and target.read_bytes()==b'owned incumbent' and ops.links==0 and guard_calls==0
            else:
                assert outcome=='publication_uncertain' and details['final_file_may_exist'] is True
                assert details['automatic_retry_overwrite_or_unlink_final_forbidden'] is True and ops.links==1
                if label=='unknown_link_absent':assert not target.exists()
                elif label=='link_known_collision':assert target.read_bytes()==b'owned incumbent'
                elif label=='published_readback':assert target.read_bytes()==b'owned synthetic changed final'
                else:assert target.read_bytes()==payload
            assert guard_calls<=1
            results.append({'name':label,'outcome':outcome,'events':events,'guard_calls':guard_calls,
                'identity_calls':identity_calls,'link_dispatches':ops.links,'final_exists':target.exists(),
                'pending_entries':len(pending()),'uncertainty_stage':details['stage'] if details else None})
    out={'UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS','scenario_count':len(results),
        'source_pin':pin(src),'primitive_pin':pin(primitive),'scenarios':results,'all_owned_fixtures_removed':True,
        'hooks':'Unchanged repaired publisher and ParentHandle. Explicit local_ops delegates actual owned fsync/link/unlink and injects declared faults; explicit final/identity guards inspect only synthetic paths. These are independent controls, not the producer test code. No production inspector context/Runtime/lock/gate/receipt/current-five/native/ref/PR/intake action.',
        'production_actions':0,'meaning':'Tests atomic publication, failure classification and no overwrite/final unlink. A post-dispatch exception can conservatively report uncertainty even if final is absent; actual durability/Root authority is not established by these fixtures.'}
    (HERE/'PUBLISHER_RESULTS.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({'status':'PASS','scenarios':len(results),'source_pin':pin(src),'production_actions':0}))
if __name__=='__main__':main()
