#!/usr/bin/env python3
"""Actual corrected helper entrypoints, with strictly in-process API mocks.

Synthetic final acceptance material is confined to deleted private_cases.
This program creates neither a genuine acceptance gate nor service writes.
"""
import base64
import contextlib
import copy
import hashlib
import importlib.util
import io
import json
import os
from pathlib import Path
import shutil
import sys
import tempfile

HERE = Path(__file__).resolve().parent
AUDIT = HERE.parents[1]
PROGRAM = AUDIT.parents[1]
HELPER = PROGRAM / 'repair_pr463_status.py'
EXPECTED_HELPER = '41a77d51024a1b954e3a8bb5e216d18e46bdfe12822bb4d8c5420c56da97106e'
EXPECTED_SYNTHESIS = 'b5418de8d946e88c6c2685b4024623afca16da60dcfc1867d25deac9560c9540'
ORIGINAL = '982fcf87d60c9f8d4ec853d5dd5f4ad6021a6649'
QUEUE = 'unsolved_math_prioritization/QUEUE.md'
BRANCH = json.loads((AUDIT / 'pr_metadata.json').read_text())['headRefName']
URL_PATH = '/AlecKriebel/Math/blob/' + 'a'*40 + '/draft_pr_claimed_solved_400_500_20261011/audits/pr463_6000016/DISPOSITION_SYNTHESIS.md'
CONFIG = [('source_topology','source_topology','RESULT.json'),
          ('global_obstruction','global_obstruction','RESULT.json'),
          ('reproduction','reproduction','RESULT.json'),
          ('priority','priority','DECISION.json'),
          ('candidate_adversary','candidate_adversary','RESULT.json'),
          ('disposition_adversary','disposition_adversary2','RESULT.json')]

def require(condition, message):
    if not condition:
        raise RuntimeError(message)

def digest(data):
    return hashlib.sha256(data).hexdigest()

def write_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2)+'\n')

def source_fixture(root, config):
    program = root / 'draft_pr_claimed_solved_400_500_20261011'
    audit = program / 'audits/pr463_6000016'
    audit.mkdir(parents=True)
    row = (AUDIT / 'selected_queue_row.md').read_text().strip()
    header = '| Rank | ID / code | Problem | EV | Impact (/10) | Difficulty | Proposed | Status | Turns | Chat | Findings | DOI |'
    sentinel = '| 492 | 6000015 / OTHER | Adjacent | 1 | 2 | 3 | 1998 | unsolved | 5/5 | adjacent-chat | adjacent-finding | adjacent-doi |'
    queue = ('prefix sentinel\n'+header+'\n|---|---|---|---|---|---|---|---|---|---|---|---|\n'+sentinel+'\n'+row+'\ntrailer sentinel\n').encode()
    if 'queue_status' in config:
        queue = queue.replace(b'| claimed_solved |', ('| '+config['queue_status']+' |').encode())
    if config.get('crlf'):
        queue = queue.replace(b'\n', b'\r\n')
    if config.get('no_terminal_newline'):
        queue = queue.rstrip(b'\n')
    if config.get('duplicate_row'):
        queue += row.encode()+b'\n'
    if config.get('missing_row'):
        queue = b'\n'.join(x for x in queue.split(b'\n') if b'6000016 /' not in x)
    paths = ['SOURCE_RECEIPT.json','pr_metadata.json','selected_queue_row.md','DISPOSITION_SYNTHESIS.md',
             'reviews/priority/APPLICABILITY_CHAIN.md','reviews/priority/SOURCE_RECEIPT.json','reviews/priority/SEARCH_COVERAGE.md']
    paths += [str(p.relative_to(AUDIT)) for p in (AUDIT/'source_snapshot').rglob('*') if p.is_file()]
    reviews = []
    for family,directory,result_name in CONFIG:
        report='reviews/'+directory+'/REPORT.md'; result='reviews/'+directory+'/'+result_name
        if family != 'disposition_adversary':
            paths += [report,result]
        reviews.append({'family':family,'reviewer':'/root/pr463_'+directory,
                        'report_path':report,'result_path':result,'unresolved_disposition_issues':0,
                        'raw_blocking_issues':None if family=='priority' else 1 if family=='candidate_adversary' else 0})
    for relative in paths:
        target=audit/relative;target.parent.mkdir(parents=True,exist_ok=True)
        target.write_bytes((AUDIT/relative).read_bytes())
    source=json.loads((audit/'SOURCE_RECEIPT.json').read_text());source['queue_sha256']=digest(queue)
    write_json(audit/'SOURCE_RECEIPT.json',source)
    final_report='reviews/disposition_adversary2/REPORT.md';final_result='reviews/disposition_adversary2/RESULT.json'
    (audit/final_report).parent.mkdir(parents=True,exist_ok=True)
    (audit/final_report).write_text('SYNTHETIC PRIVATE FIXTURE ONLY. Not a completed reviewer report.\n')
    write_json(audit/final_result,{'reviewer':'/root/pr463_disposition_adversary2','pr':463,'problem_id':'6000016',
               'frozen_head':ORIGINAL,'blocking_issues':0,'unresolved_disposition_issues':0,
               'required_corrections':0,'unresolved_mathematical_gaps':0,
               'reviewed_helper_sha256':EXPECTED_HELPER,'reviewed_synthesis_sha256':EXPECTED_SYNTHESIS,
               'retained_original_publication_blockers':1,'proposed_status':'already_solved',
               'fixture_warning':'Private modeled input, never accepted evidence'})
    paths += [final_report,final_result]
    gate={'verdict':'ACCEPTED_PRIORITY_CLASSIFICATION','pr':463,'problem_id':'6000016','original_head':ORIGINAL,
          'recommended_status':'already_solved','acceptance_scope':'one_row_priority_correction_then_immediate_skip',
          'root_read_entire_final_reports':True,'helper_sha256':EXPECTED_HELPER,'reviews':reviews,
          'retained_original_publication_blockers':1,'published_disposition_url':'https://github.com'+URL_PATH,
          'published_disposition_sha256':EXPECTED_SYNTHESIS}
    if config.get('file_update'):
        relative,field,value=config['file_update']; obj=json.loads((audit/relative).read_text());obj[field]=value
        write_json(audit/relative,obj)
    if config.get('file_delete_key'):
        relative,field=config['file_delete_key']; obj=json.loads((audit/relative).read_text());obj.pop(field,None)
        write_json(audit/relative,obj)
    if config.get('malformed_file'):
        (audit/config['malformed_file']).write_text('{malformed json')
    if config.get('source_duplicate'):
        p=audit/'SOURCE_RECEIPT.json';obj=json.loads(p.read_text());obj['files'][-1]=copy.deepcopy(obj['files'][0]);write_json(p,obj)
    gate['reviewed_files']=[{'path':relative,'bytes':(audit/relative).stat().st_size,
                            'sha256':digest((audit/relative).read_bytes())} for relative in paths]
    for field,value in config.get('gate_updates',{}).items():gate[field]=value
    for field in config.get('gate_delete',[]):gate.pop(field,None)
    if config.get('review_update'):
        index,values=config['review_update'];gate['reviews'][index].update(values)
    if config.get('review_remove'):gate['reviews'].pop()
    if config.get('review_duplicate'):gate['reviews'][-1]=copy.deepcopy(gate['reviews'][0])
    if config.get('evidence_remove'):
        gate['reviewed_files']=[x for x in gate['reviewed_files'] if x['path']!=config['evidence_remove']]
    if config.get('evidence_duplicate'):gate['reviewed_files'].append(copy.deepcopy(gate['reviewed_files'][0]))
    if config.get('evidence_update'):gate['reviewed_files'][0].update(config['evidence_update'])
    if config.get('evidence_unrelated_only'):
        p=audit/'unrelated.md';p.write_text('unrelated\n');gate['reviewed_files']=[{'path':'unrelated.md','bytes':p.stat().st_size,'sha256':digest(p.read_bytes())}]
    if config.get('drift_file'):(audit/config['drift_file']).write_bytes(b'drift\n')
    if config.get('evidence_symlink'):
        target=audit/config['evidence_symlink'];copy_path=audit/'aliased-evidence'
        copy_path.write_bytes(target.read_bytes());target.unlink();target.symlink_to(copy_path)
    if not config.get('missing_gate'):write_json(audit/'PRIORITY_DISPOSITION_GATE.json',gate)
    if config.get('malformed_gate'):(audit/'PRIORITY_DISPOSITION_GATE.json').write_text('{bad')
    if config.get('prior_operation'):(audit/'STATUS_REPAIR_OPERATION.json').write_text('{}')
    if config.get('output_attack'):
        name,kind=config['output_attack'];target=audit/name;sentinelpath=audit/'outside-sentinel';sentinelpath.write_text('intact')
        if kind=='symlink':target.symlink_to(sentinelpath)
        elif kind=='dangling':target.symlink_to(audit/'absent')
        elif kind=='hardlink':os.link(sentinelpath,target)
        elif kind=='directory':target.mkdir()
        elif kind=='fifo':os.mkfifo(target)
    return program,audit,queue

class FakeAPI:
    def __init__(self,audit,queue,config):
        self.audit=audit;self.queue=queue;self.config=config;self.calls=[];self.ref=ORIGINAL
        self.ref_reads=0;self.pr_reads=0;self.patches=0;self.new_bytes=None
    def __call__(self,endpoint,payload=None,method='POST'):
        self.calls.append({'endpoint':endpoint,'method':method,'mutation':payload is not None})
        if endpoint.startswith('contents/'):
            expected='contents/draft_pr_claimed_solved_400_500_20261011/audits/pr463_6000016/DISPOSITION_SYNTHESIS.md?ref='+'a'*40
            require(endpoint==expected,'Unexpected published immutable path')
            data=(self.audit/'DISPOSITION_SYNTHESIS.md').read_bytes()
            if self.config.get('remote_bytes_drift'):data+=b'changed'
            return {'type':self.config.get('remote_type','file'),'path':self.config.get('remote_path',endpoint[9:].split('?')[0]),
                    'encoding':self.config.get('remote_encoding','base64'),'content':base64.b64encode(data).decode()}
        if endpoint=='pulls/463':
            self.pr_reads+=1;head=self.config.get('head',ORIGINAL)
            if self.pr_reads==self.config.get('head_changed_on_read'):head='0'*40
            return {'state':self.config.get('state','open'),'draft':self.config.get('draft',True),
                    'head':{'sha':head,'ref':self.config.get('head_ref',BRANCH),'repo':{'full_name':self.config.get('head_repo','AlecKriebel/Math')}},
                    'base':{'ref':self.config.get('base','main'),'repo':{'full_name':self.config.get('base_repo','AlecKriebel/Math')}}}
        if endpoint.startswith('git/ref/heads/'):
            self.ref_reads+=1
            if self.ref_reads==self.config.get('ref_changed_on_read'):self.ref='0'*40
            return {'object':{'sha':self.config.get('ref',self.ref)}}
        if endpoint=='git/commits/'+ORIGINAL:return {'tree':{'sha':'original-tree'}}
        if endpoint=='git/trees/original-tree':return {'tree':[{'path':'unsolved_math_prioritization','sha':'queue-tree','type':'tree','mode':'040000'}]}
        if endpoint=='git/trees/queue-tree':return {'tree':[{'path':'QUEUE.md','sha':'original-blob','type':self.config.get('queue_type','blob'),'mode':self.config.get('queue_mode','100644')}]}
        if endpoint=='git/blobs/original-blob':
            data=self.queue+(b'drift' if self.config.get('queue_bytes_drift') else b'')
            return {'content':base64.b64encode(data).decode()}
        if endpoint=='git/blobs':
            require(payload['encoding']=='base64','Incorrect blob encoding');self.new_bytes=base64.b64decode(payload['content']);return {'sha':'new-blob'}
        if endpoint=='git/trees':
            require(payload=={'base_tree':'original-tree','tree':[{'path':QUEUE,'mode':'100644','type':'blob','sha':'new-blob'}]},'Unexpected paths/tree')
            return {'sha':'new-tree'}
        if endpoint=='git/commits':
            require(payload['tree']=='new-tree' and payload['parents']==[ORIGINAL],'Unexpected commit parent/tree');return {'sha':'b'*40}
        if endpoint.startswith('compare/'):
            require(endpoint=='compare/'+ORIGINAL+'...'+'b'*40,'Unexpected compare input')
            return {'files':[{'filename':self.config.get('compare_file',QUEUE)}]}
        if endpoint.startswith('git/refs/heads/'):
            require(method=='PATCH' and payload=={'sha':'b'*40,'force':False},'Unexpected ref update')
            self.patches+=1
            if self.config.get('uncertain_failed'):raise RuntimeError('Modeled unchanged uncertain update')
            self.ref='b'*40
            if self.config.get('uncertain_success'):raise RuntimeError('Modeled successful uncertain response')
            return {'object':{'sha':self.ref}}
        if endpoint=='git/blobs/new-blob':
            data=self.new_bytes+(b'drift' if self.config.get('new_blob_drift') else b'')
            return {'content':base64.b64encode(data).decode()}
        raise RuntimeError('Unimplemented mock endpoint '+endpoint)

def execute(name,config,expected,zero_dispatch=False):
    with tempfile.TemporaryDirectory(prefix='fixture_',dir=HERE/'private_cases') as folder:
        program,audit,queue=source_fixture(Path(folder).resolve(),config)
        spec=importlib.util.spec_from_file_location('corrected_'+name,HELPER)
        module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
        module.PROGRAM=program;module.AUDIT=audit
        if config.get('audit_alias'):
            alias=program/'audit-alias';alias.symlink_to(audit,target_is_directory=True);module.AUDIT=alias
        fake=FakeAPI(audit,queue,config);module.api=fake
        old=sys.argv;sys.argv=[str(HELPER)]+(['--apply'] if config.get('apply',True) else [])
        error=None
        try:
            with contextlib.redirect_stdout(io.StringIO()):module.main()
        except Exception as exc:error={'type':type(exc).__name__,'message':str(exc).replace(folder,'<private-fixture>')}
        finally:sys.argv=old
        accepted=error is None
        require(accepted==expected,name+': unexpected acceptance '+str(error))
        if zero_dispatch:require(not fake.calls,name+': dispatch before invalid gate/output rejection')
        if config.get('queue_status'):require(not any(c['mutation'] for c in fake.calls),'Excluded status mutated')
        if config.get('output_attack'):require((audit/'outside-sentinel').read_text()=='intact','Sentinel overwritten')
        if accepted and config.get('apply',True):
            before=queue.splitlines(keepends=True);after=fake.new_bytes.splitlines(keepends=True)
            require(len(before)==len(after),'Line count changed')
            changed=[i for i,(a,b) in enumerate(zip(before,after)) if a!=b];require(len(changed)==1,'Other row changed')
            a=before[changed[0]];b=after[changed[0]]
            old_cells=a.rstrip(b'\r\n').split(b'|');new_cells=b.rstrip(b'\r\n').split(b'|')
            require([i for i,(u,v) in enumerate(zip(old_cells,new_cells)) if u!=v]==[8,11],'Unexpected changed cells')
            require(new_cells[8].strip()==b'already_solved' and new_cells[9].strip()==b'1/5' and new_cells[12].strip()==b'','Status/count/DOI mismatch')
            require(a[len(a.rstrip(b'\r\n')):]==b[len(b.rstrip(b'\r\n')):],'Selected line ending changed')
            require(fake.patches==1,'Repeated PATCH')
            receipt=json.loads((audit/'STATUS_REPAIR_RECEIPT.json').read_text())
            require(receipt['state']=='status_repair_verified_immediately_excluded','Wrong stopping state')
            require('immediate skip' in receipt['subsequent_scope'],'Stop boundary missing')
        if config.get('uncertain_failed'):require(fake.patches==1,'Uncertain failed update retried')
        return {'case':name,'accepted':accepted,'expected':expected,'error':error,'api_calls':len(fake.calls),
                'mutation_calls':sum(c['mutation'] for c in fake.calls),'patches':fake.patches,'all_dispatches_mocked':True}

def cases():
    items=[('positive_read_only',{'apply':False},True,False),('positive_apply',{},True,False),
           ('positive_crlf',{'crlf':True},True,False),('positive_no_final_newline',{'no_terminal_newline':True},True,False),
           ('uncertain_success',{'uncertain_success':True},True,False),('uncertain_failed',{'uncertain_failed':True},False,False)]
    for name,conf in [('missing_gate',{'missing_gate':True}),('malformed_gate',{'malformed_gate':True}),
        ('empty_evidence',{'gate_updates':{'reviewed_files':[]}}),('unrelated_evidence',{'evidence_unrelated_only':True}),
        ('duplicate_evidence',{'evidence_duplicate':True}),('missing_family',{'review_remove':True}),
        ('duplicate_family',{'review_duplicate':True}),('duplicate_source_object',{'source_duplicate':True}),
        ('prior_operation',{'prior_operation':True})]:items.append((name,conf,False,True))
    for field,value in [('helper_sha256','0'*64),('published_disposition_sha256','0'*64),('root_read_entire_final_reports',False),
        ('acceptance_scope','publication'),('recommended_status','claimed_solved'),('original_head','0'*40),('retained_original_publication_blockers',0),('retained_original_publication_blockers',True)]:
        items.append(('gate_'+field+'_'+str(value),{'gate_updates':{field:value}},False,True))
    for field in ['reviews','reviewed_files','root_read_entire_final_reports','retained_original_publication_blockers']:
        items.append(('missing_'+field,{'gate_delete':[field]},False,True))
    for relative in ['SOURCE_RECEIPT.json','pr_metadata.json','selected_queue_row.md','DISPOSITION_SYNTHESIS.md',
                     'reviews/priority/APPLICABILITY_CHAIN.md','reviews/priority/SOURCE_RECEIPT.json','reviews/priority/SEARCH_COVERAGE.md']:
        items.append(('missing_required_'+relative,{'evidence_remove':relative},False,True))
    for family,directory,resultname in CONFIG:
        for filename in ['REPORT.md',resultname]:
            relative='reviews/'+directory+'/'+filename
            items.append(('missing_final_'+relative,{'evidence_remove':relative},False,True))
        if family!='priority':
            relative='reviews/'+directory+'/'+resultname
            items.append(('wrong_reviewer_'+family,{'file_update':(relative,'reviewer','/root/wrong')},False,True))
            for value in [False,0.0,0 if family=='candidate_adversary' else 1,'0']:
                items.append(('raw_count_'+family+'_'+repr(value),{'file_update':(relative,'blocking_issues',value)},False,True))
        i=[x[0] for x in CONFIG].index(family)
        items.append(('disconnected_report_'+family,{'review_update':(i,{'report_path':'unrelated.md'})},False,True))
        items.append(('disconnected_result_'+family,{'review_update':(i,{'result_path':'unrelated.json'})},False,True))
        items.append(('wrong_identity_'+family,{'review_update':(i,{'reviewer':'/root/wrong'})},False,True))
        items.append(('declared_scope_count_bool_'+family,{'review_update':(i,{'unresolved_disposition_issues':False})},False,True))
        items.append(('declared_raw_erased_'+family,{'review_update':(i,{'raw_blocking_issues':False if family!='priority' else 0})},False,True))
    for relative in [str(p.relative_to(AUDIT)) for p in (AUDIT/'source_snapshot').rglob('*') if p.is_file()]:
        items.append(('missing_frozen_'+relative,{'evidence_remove':relative},False,True))
    for field,value in [('path','../SOURCE_RECEIPT.json'),('path','/tmp/source'),('path','private_cases/source'),
                        ('bytes',True),('bytes',0),('bytes',1),('sha256','0'*64),('sha256','bad')]:
        items.append(('evidence_'+field+'_'+repr(value),{'evidence_update':{field:value}},False,True))
    for relative in ['DISPOSITION_SYNTHESIS.md','reviews/source_topology/REPORT.md','reviews/disposition_adversary2/RESULT.json']:
        items.append(('bound_bytes_drift_'+relative,{'drift_file':relative},False,True))
        items.append(('evidence_symlink_'+relative,{'evidence_symlink':relative},False,True))
    items.append(('aliased_audit_directory',{'audit_alias':True},False,True))
    for field,value in [('pr',464),('problem_id','other'),('head_sha','0'*40),('scope_gate','unsolved')]:
        items.append(('source_identity_'+field,{'file_update':('SOURCE_RECEIPT.json',field,value)},False,True))
    for field,value in [('number',464),('headRefOid','0'*40),('state','CLOSED'),('isDraft',False),('baseRefName','other')]:
        items.append(('metadata_identity_'+field,{'file_update':('pr_metadata.json',field,value)},False,True))
    for directory,gap_name in [('source_topology','mathematical_gaps'),('global_obstruction','unresolved_mathematical_gaps'),('reproduction','remaining_mathematical_gaps')]:
        relative='reviews/'+directory+'/RESULT.json'
        for field,value in [('pr',464),('problem_id','other'),('required_repairs',1),(gap_name,1),('required_repairs',False),(gap_name,0.0)]:
            items.append(('math_result_'+directory+'_'+field+'_'+repr(value),{'file_update':(relative,field,value)},False,True))
    for field,value in [('reviewed_helper_sha256','0'*64),('reviewed_synthesis_sha256','0'*64),
                        ('unresolved_disposition_issues',1),('required_corrections',1),('unresolved_mathematical_gaps',1),
                        ('pr',464),('problem_id','other'),('frozen_head','0'*40)]:
        items.append(('final_result_'+field,{'file_update':('reviews/disposition_adversary2/RESULT.json',field,value)},False,True))
    for field,value in [('status_recommendation','claimed_solved'),('decision_type','new_result'),
                        ('primary_backed_application_gap','unverified'),('first_priority_certified',True)]:
        items.append(('priority_'+field,{'file_update':('reviews/priority/DECISION.json',field,value)},False,True))
    for field in ['unresolved_mathematical_gaps','required_source_proof_repairs','required_repairs_for_proposed_disposition','unresolved_blocking_issues_for_proposed_disposition']:
        items.append(('candidate_'+field,{'file_update':('reviews/candidate_adversary/RESULT.json',field,1)},False,True))
    for field,value in [('required_changes',0),('paper_or_publication_approved',True),('status_recommendation','claimed_solved')]:
        items.append(('candidate_'+field,{'file_update':('reviews/candidate_adversary/RESULT.json',field,value)},False,True))
    for directory,resultname in [('source_topology','RESULT.json'),('priority','DECISION.json'),('disposition_adversary2','RESULT.json')]:
        items.append(('malformed_result_'+directory,{'malformed_file':'reviews/'+directory+'/'+resultname},False,True))
    urls=['https://github.com'+URL_PATH.replace('a'*40,'main'),'https://github.com'+URL_PATH.replace('a'*40,'a'*39),
          'https://github.com'+URL_PATH.replace('a'*40,'A'*40),'https://github.com'+URL_PATH+'?q=1',
          'https://github.com'+URL_PATH+'#fragment','http://github.com'+URL_PATH,'https://evil.example'+URL_PATH,
          'https://github.com'+URL_PATH.replace('/audits/pr463_6000016/','/other/'),
          'https://github.com'+URL_PATH.replace('AlecKriebel/Math','Other/Math')]
    for i,url in enumerate(urls):items.append(('bad_immutable_url_'+str(i),{'gate_updates':{'published_disposition_url':url}},False,True))
    for name,conf in [('remote_bytes_drift',{'remote_bytes_drift':True}),('remote_type',{'remote_type':'directory'}),
        ('remote_path',{'remote_path':'other'}),('remote_encoding',{'remote_encoding':'none'}),
        ('head_drift',{'head':'0'*40}),('ref_drift',{'ref':'0'*40}),('head_ref_drift',{'head_ref':'other'}),
        ('head_repository_drift',{'head_repo':'Other/Math'}),('base_repository_drift',{'base_repo':'Other/Math'}),
        ('base_branch_drift',{'base':'other'}),('draft_drift',{'draft':False}),('closed_state',{'state':'closed'}),
        ('queue_type',{'queue_type':'tree'}),('queue_mode',{'queue_mode':'120000'}),('queue_bytes_drift',{'queue_bytes_drift':True}),
        ('duplicate_row',{'duplicate_row':True}),('missing_row',{'missing_row':True}),('unrelated_compare_path',{'compare_file':'other'}),
        ('new_blob_readback_drift',{'new_blob_drift':True})]:items.append((name,conf,False,False))
    for status in ['already_solved','unsolved','', 'claimed_solved_extra']:
        items.append(('excluded_'+status,{'queue_status':status},False,False))
    for read in [2,3]:
        items.append(('late_ref_drift_'+str(read),{'ref_changed_on_read':read},False,False))
        items.append(('late_head_drift_'+str(read),{'head_changed_on_read':read},False,False))
    for name in ['STATUS_REPAIR_PREFLIGHT.json','STATUS_REPAIR_OPERATION.json','STATUS_REPAIR_RECEIPT.json']:
        for kind in ['symlink','dangling','hardlink','directory','fifo']:
            items.append(('output_'+name+'_'+kind,{'output_attack':(name,kind)},False,True))
    return items

def main():
    require(digest(HELPER.read_bytes())==EXPECTED_HELPER,'Reviewed helper drift')
    require(digest((AUDIT/'DISPOSITION_SYNTHESIS.md').read_bytes())==EXPECTED_SYNTHESIS,'Reviewed synthesis drift')
    (HERE/'private_cases').mkdir(exist_ok=True)
    results=[execute(*c) for c in cases()]
    print(json.dumps({'status':'PASS','helper_sha256':EXPECTED_HELPER,'synthesis_sha256':EXPECTED_SYNTHESIS,
                      'test_count':len(results),'genuine_api_dispatches':0,'fixture_acceptance_is_not_real':True,'results':results},indent=2))

if __name__=='__main__':
    main()
