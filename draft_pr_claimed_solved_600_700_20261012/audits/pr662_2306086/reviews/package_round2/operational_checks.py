#!/usr/bin/env python3
"""Fresh operational fixtures using actual paper bytes and no live services."""
import contextlib
import copy
import datetime
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import types

HERE=Path(__file__).absolute().parent
A=HERE.parents[1]
TMP=HERE/'tmp'
TMP.mkdir(exist_ok=True)
checks=[]

def load(path,name):
    m=types.ModuleType(name);m.__file__=str(path)
    exec(compile(path.read_bytes(),str(path),'exec'),m.__dict__)
    return m

M=load(A/'prepare_integration.py','round2_integration')
T=load(A/'record_tracker.py','round2_tracker')
DOI='10.5281/zenodo.999999999'

def check(label,ok):
    if not bool(ok):raise ValueError(label)
    checks.append({'label':label,'status':'PASS'})

def rejects(label,f):
    try:f()
    except (ValueError,FileNotFoundError,OSError,KeyError,TypeError):
        checks.append({'label':label,'status':'REJECTED_AS_REQUIRED'})
    else:raise ValueError('accepted invalid fixture: '+label)

@contextlib.contextmanager
def patched(m,**values):
    saved={n:getattr(m,n) for n in values}
    for n,v in values.items():setattr(m,n,v)
    try:yield
    finally:
        for n,v in saved.items():setattr(m,n,v)

def put(path,data):
    path.parent.mkdir(exist_ok=True,parents=True);path.write_bytes(data)

def fixture(root):
    shutil.copytree(A/'native',root/'native')
    put(root/'SCOPE_AND_SNAPSHOT.json',(A/'SCOPE_AND_SNAPSHOT.json').read_bytes())
    records={}
    for n in M.PUB_NAMES:
        data=(A/'publication'/n).read_bytes();put(root/'publication'/n,data)
        records[n]={'bytes':len(data),'sha256':M.sha(data)}
    rounds=[]
    for i in (1,2):
        name=f'reviews/fixture{i}/REPORT.json';data=M.json_bytes({'synthetic':True,'reviewer':i})
        put(root/name,data);rounds.append({'reviewer_id':f'explicit-synthetic-{i}','report_path':name,
            'report_sha256':M.sha(data),'mandatory_findings':0,'optional_findings':0})
    accepted={'schema':'pr662-accepted-publication-inputs-v1','pr':662,'problem_id':'2306086',
        'original_head':M.ORIGINAL,'ready_for_publication':True,'files':records,'whole_package_review_rounds':rounds}
    put(root/'ACCEPTED_PUBLICATION_INPUTS.json',M.json_bytes(accepted))
    receipt={'environment':'production','state':'published','receipt_saved':True,'title':M.TITLE,
        'id':999999999,'doi':DOI,'doi_url':'https://doi.org/'+DOI,'record_url':'https://zenodo.org/records/999999999',
        'verified_utc':'synthetic-first-inspection','doi_resolution':{'status':'resolved','http_status':200},
        'metadata_normalizations':[], 'files':[{'name':n,'size':records[n]['bytes'],'sha256':records[n]['sha256']} for n in M.UPLOAD_NAMES]}
    put(root/'first.json',M.json_bytes(receipt));put(root/'second.json',M.json_bytes(receipt|{'verified_utc':'synthetic-second-inspection'}))
    return accepted,receipt

def inputs():
    with tempfile.TemporaryDirectory(prefix='round2-actual-payload-',dir=TMP) as tmp:
        root=Path(tmp);accepted,receipt=fixture(root)
        with patched(M,A=root,ACCEPTANCE=root/'ACCEPTED_PUBLICATION_INPUTS.json'):
            run=lambda:M.publication_inputs(root/'publication',DOI,root/'first.json',root/'second.json')
            good=run();check('real accepted eleven files and 101-member archive bind',len(good['files'])==11 and len(good['members'])==101)
            for label,change in [('boolean record ID',{'id':True}),('concept DOI instead of record DOI',{'doi':'10.5281/zenodo.999999998'}),
                ('matching checksum but omitted file',{'files':receipt['files'][:1]}),('unreviewed metadata normalization',{'metadata_normalizations':['any']})]:
                put(root/'second.json',M.json_bytes(receipt|change));rejects(label,run)
            put(root/'second.json',M.json_bytes(receipt|{'verified_utc':'synthetic-second-inspection'}))
            for label,change in [('false accepted flag',{'ready_for_publication':False}),('only one review',{'whole_package_review_rounds':accepted['whole_package_review_rounds'][:1]})]:
                put(M.ACCEPTANCE,M.json_bytes(accepted|change));rejects(label,run)
            put(M.ACCEPTANCE,M.json_bytes(accepted))
            shared=copy.deepcopy(accepted);shared['whole_package_review_rounds'][1]['report_path']=shared['whole_package_review_rounds'][0]['report_path']
            shared['whole_package_review_rounds'][1]['report_sha256']=shared['whole_package_review_rounds'][0]['report_sha256']
            put(M.ACCEPTANCE,M.json_bytes(shared));rejects('different reviewer identities cannot reuse one report',run)
            put(M.ACCEPTANCE,M.json_bytes(accepted))
            p=root/'publication/CLAIM_SCOPE.json';old=p.read_bytes();p.unlink();p.symlink_to(root/'SCOPE_AND_SNAPSHOT.json')
            rejects('accepted payload symlink rejected before reading',run);p.unlink();p.write_bytes(old)
            check('fixture restored to exact initial validation',run()['validation']==good['validation'])
            generated=M.build_publication(good,DOI,'explicit-synthetic-timestamp')
            check('publication native path is sibling and original remains24',len(good['original'])==24 and all(not n.startswith(M.PREFIX) for n in generated))
            text=generated['PUBLICATION.md'].decode()
            check('generated public narrative retains qualifications',all(n in text for n in ('Jenkins (1960)','Aleksandrov-Popova (1973)','No historical firstness','unrefereed','internal AI review is not human peer review')))
            manifest=json.loads(generated['PUBLICATION_MANIFEST.json'])
            check('generated directory manifest binds all other bytes',len(manifest['files'])==len(generated)-1 and all(r['bytes']==len(generated[r['path']]) and r['sha256']==M.sha(generated[r['path']]) for r in manifest['files']))
        snapshot=json.loads((A/'SCOPE_AND_SNAPSHOT.json').read_bytes())
        cells=snapshot['queue_row'].encode().split(b'|');cells[8]=b' queued ';cells[9]=b' 0/5 ';cells[11]=b'  '
        for ending in (b'\n',b'\r\n',b''):
            original=b'|'.join(cells)+ending;changed,receipt=M.patch_queue(original,DOI,snapshot['queue_row'])
            after=changed.rstrip(b'\r\n').split(b'|')
            check('queue exact cells and line ending '+repr(ending),[j for j in range(14) if after[j]!=cells[j]]==[8,9,11] and
                  (changed.endswith(ending) if ending else not changed.endswith(b'\n')) and after[8].strip()==b'claimed_solved' and after[9].strip()==b'5/5')
        for status in (b' already_solved ',b' unsolved ',b' claimed_solved ',b' investigating '):
            changed=cells[:];changed[8]=status
            rejects('different main target status cannot be overwritten '+status.decode(),lambda changed=changed:M.patch_queue(b'|'.join(changed),DOI,snapshot['queue_row']))
        for bad in ('10.5281/zenodo.0','10.5281/zenodo.01','10.5281/zenodo.1/x','https://doi.org/'+DOI,DOI+'\n',DOI.upper()):
            rejects('DOI identity rejects '+repr(bad),lambda bad=bad:M.valid_doi(bad))

class Sheet:
    def __init__(self,pending,fault):
        self.pending=pending;self.fault=fault;self.rows=[T.HEADERS[:]];self.writes=0;self.trace=[]
    def call(self,resource,method,params,body=None):
        self.trace.append((resource,method))
        if resource=='spreadsheets':return {'sheets':[{'properties':{'sheetId':T.GID,'title':T.TAB}}]}
        if method=='append':
            self.writes+=1
            journal=json.loads(self.pending.read_bytes())
            check('sticky publication-bound intent exists before synthetic dispatch '+str(len(checks)),journal['doi']==DOI and journal['row']==T.wanted_row(DOI))
            check('exact append flags '+str(len(checks)),params['valueInputOption']=='RAW' and params['insertDataOption']=='INSERT_ROWS' and params['includeValuesInResponse'] is True)
            if self.fault=='timeout-before':raise OSError('explicit synthetic pre-append timeout')
            self.rows.append(body['values'][0][:])
            if self.fault=='timeout-after':raise OSError('explicit synthetic post-append timeout')
            result={'spreadsheetId':T.ID,'updates':{'updatedRange':"'Math Puzzles'!A2:D2",'updatedRows':1,'updatedColumns':4,'updatedCells':4,'updatedData':{'values':body['values']}}}
            if self.fault=='bool-count':result['updates']['updatedRows']=True
            if self.fault=='suffix-range':result['updates']['updatedRange']+='garbage'
            if self.fault=='different-row-range':result['updates']['updatedRange']="'Math Puzzles'!A2:D3"
            return result
        if params['range'].endswith('A1:D1'):return {'values':[T.HEADERS[:] ]}
        if params['range'].endswith('A:D'):return {'values':copy.deepcopy(self.rows)}
        return {'values':[self.rows[1][:]]}

def trackers():
    for fault in ('none','timeout-before','timeout-after','bool-count','suffix-range','different-row-range'):
        with tempfile.TemporaryDirectory(prefix='round2-tracker-',dir=TMP) as tmp:
            root=Path(tmp);pending=root/'intent.json';service=Sheet(pending,fault)
            ready={'doi':DOI,'row':T.wanted_row(DOI),'publication_validation':{'synthetic_binding':'frozen-pdf-and-zip'}}
            with patched(T,A=root,PENDING=pending,call=service.call):
                if fault=='none':
                    first=T.append_once(ready);second=T.append_once(ready)
                    check('second call reads existing row without append',service.writes==1 and first['already_present'] is False and second['already_present'] is True)
                else:
                    rejects('append fault '+fault,lambda:T.append_once(ready))
                    check('all ambiguous/invalid responses retain sticky intent '+fault,pending.exists() and json.loads(pending.read_bytes())['action_outcome'].startswith('unconfirmed'))
                    if fault=='timeout-before':
                        rejects('absent DOI after timeout cannot trigger retry',lambda:T.append_once(ready));check('only one dispatch after absent timeout',service.writes==1)
                    elif fault=='timeout-after':
                        service.fault='none';receipt=T.append_once(ready)
                        check('present DOI after timeout reconciles entirely by reads',service.writes==1 and receipt['already_present'] is True and json.loads(pending.read_bytes())['action_outcome']=='confirmed')
                    altered=ready|{'publication_validation':{'synthetic_binding':'other'}}
                    rejects('sticky intent cannot bind another publication '+fault,lambda:T.pending_record(altered))
    row=T.wanted_row(DOI)
    for variant in (DOI,'doi: '+DOI,'HTTPS://DX.DOI.ORG/'+DOI.upper()+'/'):
        check('canonical DOI duplicate recognized '+variant,T.doi_matches([T.HEADERS,['','',variant]],DOI)==[2])
    for variant in (DOI+'.1','https://doi.org/'+DOI+'/other','x'+DOI):
        check('DOI prefix does not false-match '+variant,T.doi_matches([T.HEADERS,['','',variant]],DOI)==[])
    rejects('two prior DOI rows prevent append',lambda:T.exact_existing([T.HEADERS,row,row],row,DOI))
    rejects('prior DOI row with altered notes prevents append',lambda:T.exact_existing([T.HEADERS,row[:3]+['other']],row,DOI))
    with tempfile.TemporaryDirectory(prefix='round2-durable-',dir=TMP) as tmp:
        root=Path(tmp)
        with patched(M,A=root):
            p=root/'receipt.json';M.write_json(p,{'test':1})
            check('receipt complete and regular',json.loads(p.read_bytes())=={'test':1} and not p.is_symlink())
            p.unlink();p.symlink_to(root/'another');rejects('journal symlink cannot be overwritten',lambda:M.write_json(p,{'test':2}))
            with M.action_lock('operation.lock'):
                def another():
                    with M.action_lock('operation.lock'):pass
                rejects('parallel operator blocked by nonblocking lock',another)

def trees():
    with tempfile.TemporaryDirectory(prefix='round2-tree-',dir=TMP) as tmp:
        repo=Path(tmp)/'repo';repo.mkdir();subprocess.run(['git','init','-q','-b','main',str(repo)],check=True)
        subprocess.run(['git','config','user.name','Synthetic offline review'],cwd=repo,check=True)
        subprocess.run(['git','config','user.email','synthetic@example.invalid'],cwd=repo,check=True)
        with patched(M,REPO=repo):
            files={'outside.txt':b'untouched','sub/other.txt':b'other shard','same-prefix/file':b'prefix','sub/target/before':b'before'}
            old=M.files_tree(files)
            objectid=M.git('hash-object','-w','--stdin',input=b'outside.txt').strip()
            old=M.splice(old,'unrelated-link',b'120000 blob '+objectid)
            old=M.splice(old,'unrelated-executable',b'100755 blob '+objectid)
            new=M.splice(old,'sub/target',b'040000 tree '+M.files_tree({'fresh':b'new'}).encode())
            check('recursive tree splice changes only requested subtree',set(M.git('diff','--name-only',old,new).decode().splitlines())=={'sub/target/before','sub/target/fresh'})
            for path in ('outside.txt','sub/other.txt','same-prefix','unrelated-link','unrelated-executable'):
                check('mode and object ID preserve '+path,M.git('ls-tree',old,'--',path)==M.git('ls-tree',new,'--',path))
            rejects('non-tree ancestor cannot be replaced by recursion',lambda:M.splice(old,'outside.txt/escape',b'100644 blob '+objectid))
            check('toy repository index remains absent',not(repo/'.git/index').exists())

def main():
    inputs();trackers();trees()
    report={'status':'PASS','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'checks':len(checks),
        'optimized':sys.flags.optimize>0,'no_live_services_or_real_repository_mutations':True,
        'synthetic_publication_receipts_and_review_reports_explicit':True,
        'results':checks,'source_pins':{n:{'bytes':len((A/n).read_bytes()),'sha256':M.sha((A/n).read_bytes())} for n in ('prepare_integration.py','record_tracker.py','ACCEPTED_PR_DESCRIPTION.template.md')}}
    target=HERE/('OPERATIONAL_CHECKS.optimized.json' if sys.flags.optimize else 'OPERATIONAL_CHECKS.normal.json')
    target.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({'status':'PASS','checks':len(checks),'optimized':sys.flags.optimize>0}))

if __name__=='__main__':main()
