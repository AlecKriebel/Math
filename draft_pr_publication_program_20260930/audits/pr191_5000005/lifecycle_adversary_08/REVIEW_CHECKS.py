#!/usr/bin/env python3
"""Independent compact synthetic checks: python3 -B REVIEW_CHECKS.py.
No real service/Git/native operations. Scratch is removed after execution.
"""
from pathlib import Path
from types import SimpleNamespace as NS
import copy,datetime,hashlib,importlib.util,json,sys,tempfile
sys.dont_write_bytecode=True
OWN=Path(__file__).resolve().parent
PINS=json.loads((OWN/'INPUT_PINS.json').read_text())['inputs']
SRC=Path(next(x['path'] for x in PINS if x['role']=='reviewed runtime' and x['path'].endswith('/lifecycle_common.py'))).parent
RESULTS=[]
def record(name,ok,detail=''):
    RESULTS.append({'name':name,'pass':bool(ok),'detail':str(detail)})
    if not ok:raise AssertionError(name+': '+str(detail))
def reject(name,fn):
    try:fn()
    except (RuntimeError,KeyError,TypeError,ValueError) as e:record(name,True,type(e).__name__+': '+str(e));return
    record(name,False,'unexpected acceptance')
def wire(j):return (json.dumps(j,indent=2)+'\n').encode()
def sha(b):return hashlib.sha256(b).hexdigest()

class Native:
    """Injected in-memory commit/tree/body observations; zero Git/native calls."""
    def __init__(self,m):
        self.mod=m;self.trees={};self.commits={};self.blobs={};self.main=None;self.merged=False;self.meta={'title':'','body':''};self.stale=False;self.calls=[]
        self.m=NS(m=NS(h=NS(warm_selected_directories=lambda *a:None)))
    def tree(self,b):
        b=dict(b);t=sha(wire({k:sha(v) for k,v in sorted(b.items())}))[:40];self.trees[t]=b
        for v in b.values():self.blobs[self.mod.byte_pin(v)['git_blob']]=v
        return t
    def commit(self,b,parents=(),message='Synthetic checkpoint',identity=None):
        t=self.tree(b);c=identity or sha(wire([t,list(parents),message]))[:40]
        self.commits[c]={'sha':c,'tree':{'sha':t},'parents':[{'sha':p} for p in parents],'message':message};return c
    def bodies(self,c):return self.trees[self.commits[c]['tree']['sha']]
    def body_at(self,n,c):return self.bodies(c)[n]
    def lookup(self,t,n):
        b=self.trees[t].get(n)
        return None if b is None else ('100644','blob',self.mod.byte_pin(b)['git_blob'])
    def changed_leaves(self,t1,t2):
        a,b=self.trees[t1],self.trees[t2];return {n for n in set(a)|set(b) if a.get(n)!=b.get(n)}
    def ancestor(self,a,b):return a==b or any(self.ancestor(a,p['sha']) for p in self.commits[b]['parents'] if p['sha'] in self.commits)
    def descend(self,changes):
        b=dict(self.bodies(self.main));b.update(changes);self.main=self.commit(b,[self.main]);return self.main
    def api(self,path,method='GET',body=None):
        self.calls.append((method,path))
        if path=='git/ref/heads/main':return {'object':{'sha':self.main}}
        if path.startswith('pulls/'):return {'head':{'sha':self.mod.HEAD},'state':'closed' if self.merged else 'open','merged':self.merged,'draft':False,**self.meta}
        if path.startswith('compare/'):
            a,b=path[8:].split('...');return {'status':'identical' if a==b else ('ahead' if self.ancestor(a,b) else 'diverged')}
        if path.startswith('git/commits/') and method=='GET':return copy.deepcopy(self.commits[path.split('/')[-1]])
        if path=='git/blobs' and method=='POST':
            import base64
            b=base64.b64decode(body['content']);s=self.mod.byte_pin(b)['git_blob'];self.blobs[s]=b;return {'sha':s}
        if path=='git/trees' and method=='POST':
            b=dict(self.trees[body['base_tree']])
            for e in body['tree']:b[e['path']]=e['content'].encode() if 'content' in e else self.blobs[e['sha']]
            return {'sha':self.tree(b)}
        if path=='git/commits' and method=='POST':
            c=self.commit(self.trees[body['tree']],body['parents'],body['message'])
            if self.stale:self.stale=False;self.descend({'unrelated/concurrent.txt':b'Synthetic concurrent addition\n'})
            return {'sha':c}
        raise AssertionError('Unsupported injected observation '+method+' '+path)

class Fixture:
    def __init__(self):
        self.tmp=tempfile.TemporaryDirectory(prefix='scratch_',dir=OWN);self.a=Path(self.tmp.name)
        spec=importlib.util.spec_from_file_location('independent_review08',SRC/'lifecycle_common.py');self.m=importlib.util.module_from_spec(spec);spec.loader.exec_module(self.m)
        self.m.A=self.a;self.tick=0
        def clock():
            self.tick+=1;return (datetime.datetime(2026,10,14,tzinfo=datetime.timezone.utc)+datetime.timedelta(seconds=self.tick)).isoformat()
        self.m.now=clock;self.h=Native(self.m);self.m._helpers=self.h
        self.kit_calls=[];self.publish_count=0;self.unknown_publish=False;self.state='empty';self.append_count=0;self.unknown_append=False
        self.rows=[list(self.m.HEADER),['Synthetic foreign problem','','','Synthetic foreign note']]
        self.inputs();self.m._runtime={'runner':self.runner,'inspect':lambda g:self.m.observe_publication(g,self.runner),'tracker':self.tracker}
    def put(self,n,j):self.m.write(self.a/n,j)
    def binding(self,n):return {'path':n,**self.m.public_pin(self.m.pin(self.a/n))}
    def inputs(self):
        m=self.m
        for n in m.CONTROL_FILES:(self.a/n).write_bytes((SRC/n).read_bytes())
        proof=b'Synthetic proof identity only; no scientific content.\n';self.put('synthetic_proof.md',proof.decode())
        roles={'pdf':'paper.pdf','source':'paper.tex','support':'support.zip','metadata':'deposit.json'}
        for k in ['pdf','source','support']:self.put('packet/'+roles[k],'Synthetic '+k+' bytes only.\n')
        self.put('packet/deposit.json',{'files':[{'path':roles[k]} for k in ['pdf','source','support']]})
        native={n:wire({'UTC':'2026-10-13T00:00:00+00:00','actual_original_PR_merged':False,'case_percent':0,'actual_Zenodo_published':False,'whole_package_reviews_pending':True,'scientific_identity':'synthetic unchanged'}) for n in m.JSON_FACTS}
        native.update({'README.md':b'Synthetic cover PENDING_README end.\n','review/REVIEW.md':b'Synthetic review PENDING_REVIEW end.\n','RESEARCH_LOG.md':b'Synthetic native history.\n','CANDIDATE.md':proof,'PROOF.md':proof})
        originals=[]
        for i in range(16):
            n='original_'+str(i)+'.txt';b=('Synthetic original '+str(i)+'\n').encode();native['ORIGINAL_SUBMISSION/'+n]=b;originals.append({'path':m.NATIVE+n,**m.public_pin(m.byte_pin(b))})
        for i in range(50-len(native)):native['support_'+str(i)+'.txt']=('Synthetic unchanged '+str(i)+'\n').encode()
        for n,b in native.items():
            p=self.a/'integration_preparation/native_template_pending_synthetic'/n;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b)
        self.native=native
        self.put('integration_preparation/PENDING_MANIFEST.json',{'current_template':'native_template_pending_synthetic','files':{n:m.public_pin(m.byte_pin(b)) for n,b in native.items()}})
        self.put('ORIGINAL_FILE_MANIFEST.json',{'original_head':m.HEAD,'files':originals})
        self.put('PR_PROPOSAL.json',{'title':'Synthetic approved publication title','body_before_publication':'Synthetic approved publication body.'})
        self.put('TRACKER_PROPOSAL.json',{'original_problem':'Synthetic own problem','solution_chat_url':'','notes':'Synthetic own publication note'})
        self.put('REVIEW_INPUT.json',{'purpose':'Synthetic immutable review input'})
        reviews=[]
        for i in range(2):
            d={'reviewer_id':'synthetic_science_'+str(i),'disposition':'PASS','authoritative':True}
            for role in ['report','seal','root_authentication']:
                n='synthetic_review_'+str(i)+'_'+role+'.txt';self.put(n,'SYNTHETIC FIXTURE '+role+'\n');d[role]=self.binding(n)
            reviews.append(d)
        opr={'disposition':'PASS'}
        for role in ['report','seal','root_authentication']:
            n='synthetic_lifecycle_'+role+'.txt';self.put(n,'SYNTHETIC FIXTURE '+role+'\n');opr[role]=self.binding(n)
        self.put(m.OP_CLEARANCE,{'status':'ROOT_AUTHENTICATED_OPERATIONAL_LIFECYCLE_CLEARANCE','PR':m.PR,'original_head':m.HEAD,'UTC':'2026-10-13T00:00:00+00:00','all_required_findings_globally_resolved':True,'outstanding_required_repairs':[],'runtime_pins':{n:m.public_pin(m.pin(self.a/n)) for n in m.CONTROL_FILES},'independent_adversary_review':opr})
        base={k:'synthetic' for k in m.CASE_PROTECTED_KEYS}
        base.update(PR=m.PR,problem_id=m.PROBLEM,original_head=m.HEAD,original_QUEUE_status='claimed_solved',original_effort='2/5',mathematical_clearance=True,priority_clearance=False,goal_complete=False,novelty_clearance=False,qualified_credited_note_route_authorized=True,bounded_priority_audit_complete=True,current_primary_overlap_verified=True,scientific_package_ready=True,current_proof='synthetic_proof.md',current_proof_SHA256=sha(proof),historical_only='preserve synthetic history')
        self.put(m.CASE_BASELINE,base);self.put(m.CASE_LOG_BASELINE,'Synthetic trusted case history.\n');self.put(m.CASE_PROJECTION,m.case_scientific_projection(base))
        self.put('ROOT_ORIGINAL_PARENT_AND_QUEUE_GUARD_01.json',{'purpose':'Synthetic queue guard'})
        self.put('INTAKE_CHECKPOINT_ACCEPTANCE.json',{'PR':m.PR,'original_head':m.HEAD,'checkpoint_commit':'1'*40})
        g={'UTC':'2026-10-14T00:00:00+00:00','schema':'PR191_LIFECYCLE_GATE_V1','status':'READY_FOR_AUTHORIZED_PUBLICATION','PR':m.PR,'original_head':m.HEAD,'qualified_note_route_authorized':True,'historical_priority_clearance':False,'all_required_findings_globally_resolved':True,'last_review_required_repairs':0,'whole_package_reviews':reviews,'review_input':self.binding('REVIEW_INPUT.json'),'package_name':'packet','payloads':{n:m.public_pin(m.pin(self.a/'packet'/n)) for n in roles.values()},'paper_files':roles,'current_proof':self.binding('synthetic_proof.md'),'native_proof_paths':['CANDIDATE.md','PROOF.md'],'native_pending_template':'native_template_pending_synthetic','native_pending_manifest':self.binding('integration_preparation/PENDING_MANIFEST.json'),'native_final_template':'native_template_final_synthetic','native_complete_template':'native_template_complete_synthetic','native_json_status_paths':sorted(m.JSON_FACTS),'native_text_status_replacements':{'README.md':'PENDING_README','review/REVIEW.md':'PENDING_REVIEW'},'pr_metadata_proposal':self.binding('PR_PROPOSAL.json'),'tracker_row_proposal':self.binding('TRACKER_PROPOSAL.json'),'public_case_paths':[],'public_case_pins':{n:m.public_pin(m.pin(self.a/n)) for n in [m.OP_CLEARANCE,m.CASE_BASELINE,m.CASE_LOG_BASELINE,m.CASE_PROJECTION]}}
        self.put('ROOT_PUBLICATION_GATE.json',g);self.g=g;self.gh=m.pin(self.a/'ROOT_PUBLICATION_GATE.json')['sha256']
        self.put('CURRENT_CASE_STATUS.json',m.derive_case_ready(base,g,self.gh));self.put('RESEARCH_LOG.md',(self.a/m.CASE_LOG_BASELINE).read_text()+m.ready_case_log_suffix(g['UTC']))
        cells=['','1','2','3',' 5000005 / synthetic ','5','6','7',' claimed_solved ',' 2/5 ',' synthetic PR link ',' synthetic scope ',' ','']
        q='Synthetic queue header\n'+'|'.join(cells)+'\n| foreign unchanged synthetic row |\n'
        prog={'fully_completed_eligible_PRs':list(range(1,39))+[190],'published_PRs':list(range(1,23))+[190],'fully_completed_count':39,'published_count':23,'last_completed_PR':190,'current_PR':191,'dated_eligible_total':99,'last_completed_actual_final_receipt':'audits/pr190_5000007/ROOT_FINAL_FACTUAL_ACCEPTANCE.json','historical_synthetic_key':'keep'}
        b={'unsolved_math_prioritization/QUEUE.md':q.encode(),m.PREFIX+'CURRENT_PROGRESS.json':wire(prog),m.PREFIX+'CURRENT_PROGRESS.md':b'Synthetic prior progress.\n',m.PREFIX+'RESEARCH_LOG.md':b'Synthetic programme history.\n','unrelated/existing.txt':b'Synthetic unrelated.\n'}
        self.h.commit(b,identity=m.ORIGINAL_BASE);self.h.commit(b,[m.ORIGINAL_BASE],identity=m.HEAD);self.h.main=self.h.commit(b,[m.ORIGINAL_BASE],identity='2'*40)
        self.files=[{'name':roles[k],'size':g['payloads'][roles[k]]['bytes'],'sha256':g['payloads'][roles[k]]['sha256']} for k in ['pdf','source','support']]
        self.z={'environment':'production','id':7000008,'state':'published','doi':'10.9999/synthetic-review08','doi_url':'https://doi.org/10.9999/synthetic-review08','record_url':'https://zenodo.org/records/7000008','files':self.files,'metadata_normalizations':[],'doi_resolution':{'status':'resolved'},'receipt_saved':True,'verified_utc':'2026-10-14T00:00:01+00:00'}
    def runner(self,args,**kw):
        cmd=args[6];self.kit_calls.append(cmd)
        if cmd=='check':j={'environment':'production','files':self.files}
        elif cmd=='stage':
            self.state='ready_to_publish';j={'environment':'production','id':7000008,'state':self.state,'files':self.files,'metadata_normalizations':[]}
        elif cmd=='publish':
            self.publish_count+=1;self.state='published';j=copy.deepcopy(self.z)
            if self.unknown_publish:self.unknown_publish=False;return NS(returncode=1,stdout=b'',stderr=b'Synthetic unknown outcome')
        elif cmd=='inspect':j=copy.deepcopy(self.z) if self.state=='published' else {'environment':'production','id':7000008,'state':'ready_to_publish','files':self.files,'metadata_normalizations':[]}
        else:raise AssertionError('Unexpected kit command '+cmd)
        return NS(returncode=0,stdout=json.dumps(j).encode(),stderr=b'')
    def tracker(self,res,method,p,body=None):
        if res=='spreadsheet':return {'spreadsheetId':self.m.SID,'sheets':[{'properties':{'sheetId':self.m.GID,'title':self.m.TAB}}]}
        if method=='append':
            self.append_count+=1;self.rows.append(copy.deepcopy(body['values'][0]));i=len(self.rows)
            if self.unknown_append:self.unknown_append=False;raise RuntimeError('Synthetic unknown append outcome')
            return {'updates':{'updatedRange':f"'Math Puzzles'!A{i}:D{i}",'updatedRows':1,'updatedColumns':4}}
        rng=p['range']
        if rng=="'Math Puzzles'!A1:D1":return {'values':[copy.deepcopy(self.rows[0])]}
        if rng=="'Math Puzzles'!A:D":return {'values':copy.deepcopy(self.rows)}
        return {'values':[copy.deepcopy(self.rows[self.m.own_range(rng)-1])]}
    def publish_track(self,unknown=False):
        m=self.m;m.gate();m.run_zenodo('check');m.run_zenodo('stage');m.run_zenodo('inspect')
        if unknown:self.unknown_publish=True;reject('unknown publication outcome is not success',lambda:m.run_zenodo('publish',7000008))
        m.run_zenodo('publish',7000008);m.run_zenodo('inspect-published');record('publication exactly one publish command',self.publish_count==1,self.kit_calls)
        if unknown:
            self.unknown_append=True;reject('unknown tracker append is not acceptance',lambda:m.record_tracker(self.tracker))
            record('unknown append no acceptance or response',not (self.a/'TRACKER_ACCEPTANCE.json').exists() and not (self.a/'sheets_tracking/APPEND_RESPONSE.json').exists())
        tr=m.record_tracker(self.tracker);record('tracker reconciles without second append',self.append_count==1);m.published_tracked();return tr
    def prepare_merge(self,stale=False):
        m=self.m;cur=m.prepare_native(False);record('native95 full50 original16 valid',len(cur['files'])==50 and sum(n.startswith('ORIGINAL_SUBMISSION/') for n in cur['files'])==16)
        req=m.metadata_request();self.put('PR_METADATA_ACCEPTANCE.json',{'status':'ACTUAL_ORIGINAL_HEAD_METADATA_AND_READY_STATE_ACCEPTED','PR':191,'original_head':m.HEAD,'gate_sha256':self.gh,'request_sha256':m.pin(self.a/'PR_METADATA_REQUEST.json')['sha256']})
        self.h.meta=req['request'];m.final_scope()
        if stale:self.h.stale=True;reject('stale merge parent stops adoption',lambda:m.integration_prepare('merge_preparation_stale'))
        r=m.integration_prepare('merge_preparation_fresh');record('merge scope exact full selected map',set(r['selected_files'])==set(m.read(self.a/'FINAL_MAIN_SCOPE.json')['selected_MAIN_paths']),len(r['selected_files']))
        self.h.main=r['commit'];self.h.merged=True;a=m.integration_accept();record('honest full merge acceptance',a['selected_files']==len(r['selected_files']) and a['DOI']==self.z['doi']);return r,a
    def close(self):self.tmp.cleanup()
def mutate(f,n,change,consume,label):
    p=f.a/n;old=p.read_bytes();j=json.loads(old);change(j);f.put(n,j)
    try:reject(label,consume)
    finally:p.chmod(0o644);p.write_bytes(old)
def main():
    for pin in PINS:
        p=Path(pin['path']);b=p.read_bytes();record('input pin '+p.name,len(b)==pin['bytes'] and sha(b)==pin['sha256'] and format(p.stat().st_mode&0o777,'04o')==pin['mode'])
    f=Fixture()
    try:
        m=f.m;tr=f.publish_track(unknown=True);r,a=f.prepare_merge(stale=True)
        trials=[('DOI',None),('DOI',True),('DOI',7),('DOI',[]),('DOI',{}),('DOI','10.9999/other'),('selected_files',True),('selected_files',1.0),('selected_files',len(r['selected_files'])+1),('selected_files',0),('parents',['other',m.HEAD]),('gate_sha256','0'*64),('scope_sha256','0'*64),('merge_commit','unrelated_commit')]
        for key,value in trials:
            mutate(f,'ROOT_ACTUAL_MERGE_ACCEPTANCE.json',lambda j,k=key,v=value:j.__setitem__(k,v),lambda:m.verify_merge_scope(f.h,f.g,r,True),'merge rejects '+key+'='+repr(value))
        for key,value in [('actual_fresh_reads',True),('actual_fresh_reads',1),('gid',True),('DOI','10.9999/other'),('row',['wrong','','','row'])]:
            mutate(f,'TRACKER_ACCEPTANCE.json',lambda j,k=key,v=value:j.__setitem__(k,v),m.published_tracked,'tracker rejects '+key+'='+repr(value))
        for key,value in [('id',True),('doi','10.9999/other'),('record_url','https://zenodo.org/records/3'),('verified_utc','2099-01-01T00:00:00+00:00')]:
            mutate(f,'ZENODO_PUBLICATION_READBACK.json',lambda j,k=key,v=value:j.__setitem__(k,v),m.published_tracked,'publication rejects '+key+'='+repr(value))
        mutate(f,'PR_METADATA_ACCEPTANCE.json',lambda j:j.__setitem__('request_sha256','0'*64),m.published_tracked,'metadata acceptance rejects wrong request reference')
        mutate(f,'PR_METADATA_REQUEST.json',lambda j:j['request'].__setitem__('title','Other title'),m.published_tracked,'metadata request rejects other title')
        mutate(f,'FINAL_MAIN_SCOPE.json',lambda j:j.__setitem__('native_files',True),m.published_tracked,'scope rejects boolean native count')
        mutate(f,'SCOPED_MERGE_PREPARATION.json',lambda j:j.__setitem__('changed_paths',j['changed_paths']+['other']),lambda:m.verify_merge_scope(f.h,f.g,m.read(f.a/'SCOPED_MERGE_PREPARATION.json')),'preparation rejects wrong changed-path set')
        f.h.descend({'unrelated/allowed.txt':b'Synthetic unrelated addition\n'});m.integration_accept();record('merge accepts unrelated descendant',True)
        selected=next(n for n in r['selected_files'] if n.endswith('synthetic_proof.md'));clean=f.h.main;f.h.descend({selected:b'Plain wrong synthetic identity\n'})
        reject('merge rejects current selected identity drift',m.integration_accept);f.h.main=clean
        f.h.stale=True;reject('stale factual parent stops adoption',lambda:m.factual_prepare('factual_preparation_stale'))
        cur=m.read(f.a/'integration_preparation/CURRENT_TEMPLATE.json');oldcur=(f.a/'integration_preparation/CURRENT_TEMPLATE.json').read_bytes()
        oldnative={n:(f.a/'integration_preparation'/cur['current_template']/n).read_bytes() for n in cur['files']}
        oldcase=(f.a/'CURRENT_CASE_STATUS.json').read_bytes();oldlog=(f.a/'RESEARCH_LOG.md').read_bytes()
        fr=m.factual_prepare('factual_preparation_fresh')
        record('native100 immutable pointer reused after stale retry',(f.a/'integration_preparation/CURRENT_TEMPLATE.json').read_bytes()==oldcur)
        record('native100 all50 exact bytes reused',all((f.a/'integration_preparation'/cur['current_template']/n).read_bytes()==b for n,b in oldnative.items()))
        record('phase100 exact case/log reused',(f.a/'CURRENT_CASE_STATUS.json').read_bytes()==oldcase and (f.a/'RESEARCH_LOG.md').read_bytes()==oldlog)
        historical=[m.read(p) for p in (f.a/'integration_preparation/receipt_history').glob('FINAL_FACTUAL_PREPARATION_*.json')]
        record('retry refreshes parent and archives stale preparation',len(historical)==1 and historical[0]['expected_main']!=fr['expected_main'] and fr['expected_main']==f.h.main and historical[0]['selected_files'][m.CASE+'integration_preparation/CURRENT_TEMPLATE.json']==fr['selected_files'][m.CASE+'integration_preparation/CURRENT_TEMPLATE.json'])
        f.h.main=fr['commit'];f.h.descend({'unrelated/after_factual.txt':b'Synthetic unrelated final change\n'});good=f.h.main
        f.h.descend({selected:b'Ordinary original selected-map mismatch\n'});reject('factual rechecks original selected identity',m.factual_accept);f.h.main=good
        mutate(f,'ROOT_ACTUAL_MERGE_ACCEPTANCE.json',lambda j:j.__setitem__('DOI',None),m.factual_accept,'factual rejects malformed original merge DOI')
        mutate(f,'ROOT_ACTUAL_MERGE_ACCEPTANCE.json',lambda j:j.__setitem__('selected_files',len(r['selected_files'])+1),m.factual_accept,'factual rejects original merge cardinality mismatch')
        out=m.factual_accept();record('full native100 factual acceptance',out['fully_completed_count']==40 and out['published_count']==24 and out['subsequent_status_only_intake_authorized'] is True)
        prog=json.loads(f.h.body_at(m.PREFIX+'CURRENT_PROGRESS.json',fr['commit']));case=json.loads(f.h.body_at(m.CASE+'CURRENT_CASE_STATUS.json',fr['commit']))
        record('prepared case/programme cursor191 pending acceptance',all(j['next_numeric_intake_cursor']==191 and j['actual_factual_checkpoint_accepted'] is False and j['advance_to_next_PR_authorized_now'] is False for j in [prog,case]))
        record('original16 preserved through native100',all(oldnative[n]==b for n,b in f.native.items() if n.startswith('ORIGINAL_SUBMISSION/')))
        # Straightforward successful observations, without injected uncertainty/retries.
        plain=Fixture()
        try:
            plain.publish_track();pr,_=plain.prepare_merge();pf=plain.m.factual_prepare('factual_preparation_plain');plain.h.main=pf['commit']
            pa=plain.m.factual_accept()
            record('straightforward full positive lifecycle',pa['case_percent']==100 and pa['combined_expected_current_identities_checked']==len({**pr['selected_files'],**pf['selected_files']}))
        finally:plain.close()
        # Unknown outcomes with no observed committed change must block a second write.
        pending=Fixture()
        try:
            pm=pending.m;pm.run_zenodo('check');pm.run_zenodo('stage');pm.run_zenodo('inspect');writes=[]
            def unknown_without_publish(args,**kwargs):
                if args[6]=='publish':
                    writes.append('publish');return NS(returncode=1,stdout=b'',stderr=b'Synthetic unresolved outcome')
                return pending.runner(args,**kwargs)
            reject('unconfirmed unpublished outcome blocks success',lambda:pm.run_zenodo('publish',7000008,unknown_without_publish))
            reject('unresolved publish retry blocks second write',lambda:pm.run_zenodo('publish',7000008,unknown_without_publish))
            record('unresolved publication exactly one attempted write',writes==['publish'] and not (pending.a/'ZENODO_PUBLICATION_READBACK.json').exists())
            # Publish is not repeated: supply a read-only observed eventual publication.
            pending.state='published';pm.run_zenodo('publish',7000008)
            appends=[]
            def unknown_without_append(resource,method,params,body=None):
                if method=='append':appends.append('append');raise RuntimeError('Synthetic unresolved append outcome')
                return pending.tracker(resource,method,params,body)
            reject('unconfirmed absent append blocks acceptance',lambda:pm.record_tracker(unknown_without_append))
            reject('unresolved append retry blocks second write',lambda:pm.record_tracker(unknown_without_append))
            record('unresolved tracker exactly one attempted append',appends==['append'] and not (pending.a/'TRACKER_ACCEPTANCE.json').exists())
        finally:pending.close()
        summary={'source_runtime_sha256':sha((SRC/'lifecycle_common.py').read_bytes()),'tests':len(RESULTS),'passed':sum(x['pass'] for x in RESULTS),'failed':sum(not x['pass'] for x in RESULTS),'publish_commands':f.publish_count,'tracker_append_commands':f.append_count,'native_files':len(cur['files']),'original_files':16,'merge_selected_files':len(r['selected_files']),'factual_selected_files':len(fr['selected_files']),'combined_selected_files':out['combined_expected_current_identities_checked'],'real_service_native_git_operations':0,'results':RESULTS}
        output=OWN/'CHECK_RESULTS.json'
        if output.exists():
            if json.loads(output.read_text())!=summary:raise AssertionError('Reproduced results differ from sealed CHECK_RESULTS.json')
        else:output.write_text(json.dumps(summary,indent=2)+'\n')
        print(json.dumps({k:v for k,v in summary.items() if k!='results'},indent=2))
    finally:f.close()
if __name__=='__main__':main()
