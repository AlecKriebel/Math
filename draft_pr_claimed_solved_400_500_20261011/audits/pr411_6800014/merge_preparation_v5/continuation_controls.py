#!/usr/bin/env python3
"""Offline ADMIN continuation controls. Never contacts a service or reads assets.

Genuine prior administration JSON is read once through pins. Private fixtures
rewrite their case path and are expressly synthetic. Fake API/CLI outcomes are
not production success or fresh native verification.
"""
import argparse,ast,base64,copy,datetime,hashlib,importlib.util,json,os
from pathlib import Path
import subprocess,sys,threading,types
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent
BASE='e4c9bd76594127b23cf6439df0b2c7a965f39b8f027d6debdb7cdf8e393aaa14'

def require(value,msg):
    if not value:raise RuntimeError(msg)
def sha(raw):return hashlib.sha256(raw).hexdigest()
def pretty(v):return (json.dumps(v,sort_keys=True,indent=2,ensure_ascii=False)+'\n').encode()
def load(path):
    s=importlib.util.spec_from_file_location('admin_v5',path);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m

class World:
    def __init__(self,m,root,spec,originals):
        self.m,self.case=m,root;root.mkdir(parents=True,exist_ok=False)
        self.spec=copy.deepcopy(spec);self.docs={}
        for key,ref in self.spec.items():
            if isinstance(ref,dict):
                self.docs[key]=json.loads(originals[ref['path']]) if key!='prior_journal' else originals[ref['path']]
                p=root/ref['path'];p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(originals[ref['path']])
        self.root=root/self.spec['journal_root']
        cli=self.docs['prior_cli_native'];argv=cli['argv']
        for flag,value in [('--case',str(root)),('--journal-root',str(self.root))]:argv[argv.index(flag)+1]=value
        self.save('prior_cli_native')
        self.write_spec()
        self.plan=copy.deepcopy(self.docs['prior_plan'])
        self.plan['helper_sha256']=sha((HERE/'pr411_admin.py').read_bytes())
        self.plan['native_evidence']['sheet_freshness_deadline_utc']=(datetime.datetime.now(datetime.timezone.utc)+datetime.timedelta(minutes=10)).strftime('%Y-%m-%dT%H:%M:%SZ')
        self.plan['pre_intent_continuation']={'descriptor':self.ref}
        self.originals={key:(root/ref['path']).read_bytes() for key,ref in self.spec.items() if isinstance(ref,dict)}
    def save(self,key,join=True):
        d=self.docs[key];raw=d if isinstance(d,bytes) else (self.m.encoded(d)+b'\n' if key=='prior_claim' else pretty(d))
        p=self.case/self.spec[key]['path'];p.write_bytes(raw);self.spec[key]['sha256']=sha(raw)
        if join and key in ('prior_claim','prior_journal','prior_stop','prior_cli_native'):
            self.docs['root_stop_acceptance']['pins'][self.spec[key]['path']]=sha(raw)
            self.save('root_stop_acceptance',False)
    def write_spec(self):
        self.descriptor=self.case/'descriptor.json';self.descriptor.write_bytes(pretty(self.spec));self.ref={'path':'descriptor.json','sha256':sha(self.descriptor.read_bytes())}
        if hasattr(self,'plan'):self.plan['pre_intent_continuation']={'descriptor':self.ref}
    def validate(self):return self.m.pre_intent_continuation(self.case,self.root,self.ref,self.plan)
    def journal(self,run='successor'):
        return self.m.Journal(self.root,run,'merge',self.plan['expected_head'],sha(self.m.encoded(self.m.canonical_plan(self.plan))),
                              (self.case,self.ref,self.plan))
    def unchanged(self):
        require(all((self.case/self.spec[k]['path']).read_bytes()==v for k,v in self.originals.items()),'original synthetic custody changed')
    def events(self,run='successor'):return [json.loads(x) for x in (self.root/run/'journal.jsonl').read_bytes().splitlines()]
    def approval(self):return {'format':'pr411-explicit-administration-approval-v1','phase':'merge','plan_sha256':sha(self.m.encoded(self.m.canonical_plan(self.plan))), 'expected_head':self.plan['expected_head'],'expected_main':self.plan['main_head'],'authorize_one_phase':True}

class FakeAPI:
    def __init__(self,unknown=False):self.writes=[];self.unknown=unknown
    def call(self,method,route,body=None):
        require(method=='PUT' and route=='pulls/411/merge','unexpected synthetic write')
        self.writes.append((method,route,body))
        if self.unknown:raise OSError('synthetic response loss')
        return {'merged':True,'sha':'f'*40}


def execute(w,clean=True,unknown=False,scope=True,approval=None):
    m=w.m;api=FakeAPI(unknown)
    saved=[(name,getattr(m,name)) for name in ('fresh_gate','descendant_main_guard','verify_integrated','verify_merge')]
    m.fresh_gate=lambda *a,**k:({'skip':not scope},{'mergeable':clean,'mergeable_state':'clean' if clean else 'unknown'},b'')
    m.descendant_main_guard=lambda *a,**k:{'synthetic':True}
    m.verify_integrated=lambda *a,**k:{'synthetic':True}
    m.verify_merge=lambda *a,**k:{'synthetic':True,'native_success_certified':False}
    j=w.journal()
    try:
        try:r=m.execute(api,w.plan,{},j,w.approval() if approval is None else approval);accepted=True
        except (m.Stop,OSError):r=None;accepted=False
    finally:
        j.close()
        for name,value in saved:setattr(m,name,value)
    return accepted,api,r


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--case',type=Path,required=True);p.add_argument('--private-dir',type=Path,required=True);a=p.parse_args()
    a.private_dir.mkdir(parents=True,exist_ok=False);m=load(HERE/'pr411_admin.py')
    before=(a.case/'merge_preparation_v4/pr411_admin.py').read_bytes();require(sha(before)==BASE,'V4 pin drift')
    oldtree,newtree=ast.parse(before),ast.parse((HERE/'pr411_admin.py').read_bytes())
    oldnodes={getattr(n,'name','node_'+str(i)):ast.dump(n) for i,n in enumerate(oldtree.body)}
    # Compare named definitions and nondefinition nodes in original positions after removing the new validator.
    filtered=[n for n in newtree.body if getattr(n,'name',None)!='pre_intent_continuation']
    require(len(oldtree.body)==len(filtered),'original top-level inventory changed')
    changed=[getattr(x,'name','node_'+str(i)) for i,(x,y) in enumerate(zip(oldtree.body,filtered)) if ast.dump(x)!=ast.dump(y)]
    require(changed==['Journal','main'],'unauthorized action/evidence guard change')
    spec_path=a.case/'private_sources/merge_preparation_v5/ACTUAL_PREINTENT_DESCRIPTOR.json';spec=json.loads(spec_path.read_bytes());originals={}
    for key,ref in spec.items():
        if isinstance(ref,dict):originals[ref['path']]=m.read_local(a.case,ref['path'],ref['sha256'])
    results=[]
    def control(tag,fn,expected=True):
        w=World(m,a.private_dir/tag,spec,originals)
        try:fn(w);accepted=True;detail='expected boundary completed'
        except (m.Stop,OSError,ValueError,KeyError,TypeError) as e:accepted=False;detail=type(e).__name__+': '+str(e)
        require(accepted is expected,'unexpected control '+tag+': '+detail)
        results.append({'control':tag,'expected_accept':expected,'actual_accept':accepted,'detail':detail})
    def edit(key,fn):
        def action(w):fn(w.docs[key]);w.save(key);w.write_spec();w.validate()
        return action
    control('valid_readonly_descriptor',lambda w:w.validate())
    def success(w):
        j=w.journal();j.close();w.unchanged();require(len(w.events())==1,'new journal not one exclusive event')
        require((w.root/'continuations'/('merge-'+w.plan['expected_head']+'.json')).is_file(),'guard absent')
    control('one_durable_continuation_originals_preserved',success)
    def ordinary(w):m.Journal(w.root,'ordinary','merge',w.plan['expected_head'],sha(m.encoded(m.canonical_plan(w.plan))))
    control('ordinary_lock_bypass_rejected',ordinary,False)
    def double(w):j=w.journal();j.close();w.journal('second')
    control('double_continuation_rejected',double,False)
    control('stopped_run_reuse_rejected',lambda w:w.journal(w.spec['prior_run_id']),False)
    def otherroot(w):x=w.case/'other-root';x.mkdir();m.pre_intent_continuation(w.case,x,w.ref,w.plan)
    control('different_root_rejected',otherroot,False)
    for key,value in [('expected_head','a'*40),('phase','ready'),('main_head','b'*40),('source_head','c'*40),('approved_map_sha256','0'*64)]:
        control('new_plan_drift_'+key,lambda w,k=key,v=value:(w.plan.__setitem__(k,v),w.validate()),False)
    for key,value in [('run_id','wrong'),('phase','ready'),('head','a'*40),('plan_sha256','0'*64),('extra',True)]:
        control('original_claim_'+key,edit('prior_claim',lambda d,k=key,v=value:d.__setitem__(k,v)),False)
    for tag,suffix in [('remote_intent',b'{"event":"intent"}\n'),('ack',b'{"event":"response_received"}\n'),('extra_exclusive',originals[spec['prior_journal']['path']]),('empty_line',b'\n')]:
        control('original_journal_'+tag,edit('prior_journal',lambda d:None) if False else lambda w,s=suffix:(w.docs.__setitem__('prior_journal',w.docs['prior_journal']+s),w.save('prior_journal'),w.write_spec(),w.validate()),False)
    control('original_journal_torn',lambda w:(w.docs.__setitem__('prior_journal',w.docs['prior_journal'][:-1]),w.save('prior_journal'),w.write_spec(),w.validate()),False)
    def journalfield(w,key,value):
        x=json.loads(w.docs['prior_journal']);x[key]=value;w.docs['prior_journal']=m.encoded(x)+b'\n';w.save('prior_journal');w.write_spec();w.validate()
    for key,value in [('head','a'*40),('plan_sha256','0'*64),('at_utc','2999-01-01T00:00:00Z')]:control('original_journal_'+key,lambda w,k=key,v=value:journalfield(w,k,v),False)
    for key,value in [('result','CONFIRMED'),('error_type','Uncertain'),('mutation_resume_permitted',True),('phase','ready')]:control('STOP_'+key,edit('prior_stop',lambda d,k=key,v=value:d.__setitem__(k,v)),False)
    control('STOP_plan_drift',edit('prior_stop',lambda d:d['plan'].__setitem__('source_head','a'*40)),False)
    for key,value in [('original_mutation_intents',1),('original_journal_events',True),('original_acknowledgments',False)]:control('acceptance_'+key,edit('root_stop_acceptance',lambda d,k=key,v=value:d.__setitem__(k,v)),False)
    control('acceptance_pin_divergence',edit('root_stop_acceptance',lambda d:d['pins'].__setitem__(spec['prior_claim']['path'],'0'*64)),False)
    for key,value in [('returncode',False),('stderr_base64',base64.b64encode(b'STOP: other\n').decode())]:control('completed_CLI_'+key,edit('prior_cli_native',lambda d,k=key,v=value:d.__setitem__(k,v)),False)
    control('completed_CLI_wrong_run',edit('prior_cli_native',lambda d:d['argv'].__setitem__(d['argv'].index('--run-id')+1,'wrong')),False)
    control('completed_CLI_wrong_root',edit('prior_cli_native',lambda d:d['argv'].__setitem__(d['argv'].index('--journal-root')+1,'/tmp/wrong')),False)
    def missing(w):(w.case/w.spec['prior_stop']['path']).unlink();w.validate()
    control('missing_original_STOP',missing,False)
    def link(w,key):
        p=w.case/w.spec[key]['path'];p.unlink();p.symlink_to(w.case/w.spec['prior_plan']['path']);w.validate()
    control('original_journal_symlink',lambda w:link(w,'prior_journal'),False)
    def guarddir(w):p=w.root/'continuations';p.symlink_to(w.case);w.journal()
    control('continuation_directory_symlink',guarddir,False)
    def preguard(w,link=False):
        d=w.root/'continuations';d.mkdir();p=d/('merge-'+w.plan['expected_head']+'.json')
        if link:p.symlink_to(w.case/w.spec['prior_plan']['path'])
        else:p.write_bytes(b'{torn')
        w.journal()
    control('existing_torn_guard_consumed',preguard,False)
    control('existing_symlink_guard_consumed',lambda w:preguard(w,True),False)
    def late(w,kind):
        j=w.journal()
        try:
            if kind=='journal':(w.case/w.spec['prior_journal']['path']).write_bytes(w.docs['prior_journal']+b'{"event":"intent"}\n')
            elif kind=='STOP':(w.case/w.spec['prior_stop']['path']).write_bytes(b'{}\n')
            elif kind=='guard':(w.root/'continuations'/('merge-'+w.plan['expected_head']+'.json')).write_bytes(b'{}\n')
            else:w.plan['source_head']='a'*40
            j.add({'event':'intent','method':'PUT','route':'pulls/411/merge'})
        finally:j.close();require(len(w.events())==1,'remote intent written despite drift')
    for kind in ['journal','STOP','guard','plan']:control('late_'+kind+'_drift',lambda w,k=kind:late(w,k),False)
    def race(w):
        outcomes=[];barrier=threading.Barrier(2)
        def attempt(run):
            barrier.wait()
            try:j=w.journal(run);j.close();outcomes.append(True)
            except (m.Stop,OSError):outcomes.append(False)
        threads=[threading.Thread(target=attempt,args=(name,)) for name in ['concurrent1','concurrent2']]
        for t in threads:t.start()
        for t in threads:t.join()
        require(sorted(outcomes)==[False,True],'concurrent double continuation admitted');w.unchanged()
    control('concurrent_successors_exactly_one',race)
    def clean(w):ok,api,r=execute(w);require(ok and len(api.writes)==1 and r['readback']['native_success_certified'] is False,'synthetic merge not exactly one');w.unchanged()
    control('unchanged_execute_one_synthetic_merge',clean)
    def dirty(w):ok,api,r=execute(w,clean=False);require(not ok and not api.writes and len(w.events())==1,'pre-intent dirty merge wrote');w.journal('another')
    control('new_preintent_STOP_guard_stays_consumed',dirty,False)
    def unknown(w):ok,api,r=execute(w,unknown=True);require(not ok and len(api.writes)==1 and any(e['event']=='intent' for e in w.events()),'response-loss boundary missing');w.journal('another')
    control('unknown_remote_write_never_continues',unknown,False)
    def stale(w):w.plan['native_evidence']['sheet_freshness_deadline_utc']='2000-01-01T00:00:00Z';ok,api,r=execute(w);require(not ok and not api.writes,'stale Sheet wrote')
    control('fresh_Sheet_deadline_still_mandatory',stale)
    control('canonical_approval_still_mandatory',lambda w:require(not execute(w,approval={})[0],'bad approval wrote'))
    control('native_claimed_gate_still_mandatory',lambda w:require(not execute(w,scope=False)[0],'scope drift wrote'))
    def direct_reuse(w):
        saved=[(name,getattr(m,name)) for name in ('fresh_gate','descendant_main_guard','verify_integrated','verify_merge')]
        m.fresh_gate=lambda *a,**k:({'skip':False},{'mergeable':True,'mergeable_state':'clean'},b'')
        m.descendant_main_guard=lambda *a,**k:{};m.verify_integrated=lambda *a,**k:{};m.verify_merge=lambda *a,**k:{}
        api=FakeAPI(True);j=w.journal()
        try:
            for _ in range(2):
                try:m.execute(api,w.plan,{},j,w.approval())
                except (m.Stop,OSError):pass
            require(len(api.writes)==1,'same Journal execute reuse retried remote PUT')
            require(sum(e['event']=='intent' for e in w.events())==1,'second intent appended')
            require((w.root/'successor'/'remote_intent_guard.json').is_file(),'durable remote fence absent')
        finally:
            j.close()
            for name,value in saved:setattr(m,name,value)
        w.unchanged()
    control('same_open_Journal_response_loss_never_retries',direct_reuse)
    def direct_race(w):
        j=w.journal();api=FakeAPI();barrier=threading.Barrier(8);outcomes=[]
        body={'sha':w.plan['integrated_head'],'merge_method':'merge','commit_title':'Merge PR411: published result for 6800014'}
        def invoke():
            barrier.wait()
            try:m.mutate(api,j,'PUT','pulls/411/merge',body,w.plan['integrated_head'],lambda answer:m.need(answer.get('merged') is True,'fake response drift'));outcomes.append(True)
            except (m.Stop,OSError):outcomes.append(False)
        try:
            ts=[threading.Thread(target=invoke) for _ in range(8)]
            for t in ts:t.start()
            for t in ts:t.join()
            require(outcomes.count(True)==1 and len(api.writes)==1,'same-object concurrent remote attempts not fenced')
            require(sum(e['event']=='intent' for e in w.events())==1,'same-object concurrent second intent')
        finally:j.close()
        w.unchanged()
    control('same_open_Journal_eight_way_remote_fence',direct_race)
    def failed_append(w):
        j=w.journal();api=FakeAPI();original_write=m.os.write
        body={'sha':w.plan['integrated_head'],'merge_method':'merge','commit_title':'Merge PR411: published result for 6800014'}
        def fail(*args,**kwargs):raise OSError('synthetic first append failure after durable remote fence')
        try:
            m.os.write=fail
            try:m.mutate(api,j,'PUT','pulls/411/merge',body,w.plan['integrated_head'],lambda answer:None)
            except (m.Stop,OSError):pass
            m.os.write=original_write
            try:m.mutate(api,j,'PUT','pulls/411/merge',body,w.plan['integrated_head'],lambda answer:None)
            except (m.Stop,OSError):pass
            require(not api.writes and len(w.events())==1,'post-fence append failure retried')
            require((w.root/'successor'/'remote_intent_guard.json').is_file(),'post-failure fence disappeared')
        finally:m.os.write=original_write;j.close()
    control('durable_remote_fence_consumed_before_failed_append',failed_append)
    def wrong_action(w,kind):
        j=w.journal();body={'sha':w.plan['integrated_head'],'merge_method':'merge','commit_title':'Merge PR411: published result for 6800014'}
        event={'event':'intent','method':'PUT','route':'pulls/411/merge','expected':w.plan['integrated_head'],'native_request_body':body,'body_sha256':sha(m.encoded(body))}
        if kind=='route':event['route']='pulls/412/merge'
        elif kind=='body':event['native_request_body']={**body,'merge_method':'squash'};event['body_sha256']=sha(m.encoded(event['native_request_body']))
        else:event['expected']='a'*40
        try:j.add(event)
        finally:j.close();require(len(w.events())==1,'invalid ordinary merge intent written')
    for kind in ['route','body','expected']:control('continuation_wrong_remote_action_'+kind,lambda w,k=kind:wrong_action(w,k),False)
    def closed_object(w):
        j=w.journal();j.close();original_open=m.os.open;opens=[]
        body={'sha':w.plan['integrated_head'],'merge_method':'merge','commit_title':'Merge PR411: published result for 6800014'}
        event={'event':'intent','method':'PUT','route':'pulls/411/merge','expected':w.plan['integrated_head'],'native_request_body':body,'body_sha256':sha(m.encoded(body))}
        def forbidden(*args,**kwargs):opens.append(args);raise RuntimeError('closed Journal attempted any file open')
        try:
            m.os.open=forbidden
            try:j.add(event)
            except m.Stop:pass
            require(not opens,'closed Journal touched a directory/CWD')
        finally:m.os.open=original_open
        require(not (w.root/'successor'/'remote_intent_guard.json').exists(),'closed object created fence')
    control('closed_Journal_no_relative_open_or_remote_intent',closed_object)
    def preintent_terminal_reuse(w):
        saved=[(name,getattr(m,name)) for name in ('fresh_gate','descendant_main_guard','verify_integrated','verify_merge')]
        state={'clean':False};m.fresh_gate=lambda *a,**k:({'skip':False},{'mergeable':state['clean'],'mergeable_state':'clean' if state['clean'] else 'unknown'},b'')
        m.descendant_main_guard=lambda *a,**k:{};m.verify_integrated=lambda *a,**k:{};m.verify_merge=lambda *a,**k:{}
        j=w.journal();api=FakeAPI()
        try:
            try:m.execute(api,w.plan,{},j,w.approval())
            except (m.Stop,OSError):pass
            receipt=(w.root/'successor'/'receipt.json').read_bytes();state['clean']=True
            try:m.execute(api,w.plan,{},j,w.approval())
            except (m.Stop,OSError):pass
            require(not api.writes and len(w.events())==1,'pre-intent terminal STOP object resumed a remote write')
            require((w.root/'successor'/'receipt.json').read_bytes()==receipt,'original successor terminal receipt overwritten')
            require(not (w.root/'successor'/'remote_intent_guard.json').exists(),'terminal STOP permitted remote fence allocation')
        finally:
            j.close()
            for name,value in saved:setattr(m,name,value)
        w.unchanged()
    control('same_open_Journal_preintent_terminal_STOP_never_resumes',preintent_terminal_reuse)
    def receipt_presence(w,kind):
        j=w.journal();api=FakeAPI();p=w.root/'successor'/'receipt.json'
        if kind=='empty':p.write_bytes(b'')
        elif kind=='torn':p.write_bytes(b'{torn')
        elif kind=='symlink':p.symlink_to(w.case/w.spec['prior_plan']['path'])
        elif kind=='fifo':os.mkfifo(p,0o600)
        else:p.mkdir()
        body={'sha':w.plan['integrated_head'],'merge_method':'merge','commit_title':'Merge PR411: published result for 6800014'}
        try:
            try:m.mutate(api,j,'PUT','pulls/411/merge',body,w.plan['integrated_head'],lambda answer:None)
            except (m.Stop,OSError):pass
            require(not api.writes and len(w.events())==1,'any existing terminal object allowed a remote intent')
            require(not (w.root/'successor'/'remote_intent_guard.json').exists(),'terminal object permitted fence allocation')
        finally:j.close()
    for kind in ['empty','torn','symlink','fifo','directory']:control('any_terminal_receipt_presence_'+kind,lambda w,k=kind:receipt_presence(w,k))
    out={'format':'pr411-v5-offline-continuation-controls-v1','at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'result':'PASS','controls':len(results),'results':results,'source_sha256':sha((HERE/'pr411_admin.py').read_bytes()),'baseline_sha256':BASE,'changed_original_top_level_nodes':changed,'unchanged_original_top_level_nodes':len(filtered)-2,'new_validator':'pre_intent_continuation','native_requests':0,'native_mutations':0,'scientific_files_or_asset_bytes_read':0,'boundary':'Actual local standard-library fixture/journal executions only, with fake API guards/responses and copied path-adjusted ADMIN custody. No production state or fresh native verification. Original genuine operator journal root only read as pinned input; never instantiated/written.'}
    (a.private_dir/'RESULT.json').write_bytes(pretty(out));print(json.dumps(out,sort_keys=True,indent=2))

if __name__=='__main__':main()
