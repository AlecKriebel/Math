"""Fresh complete-main public/tracker/PR probes using explicit in-memory adapters."""
from pathlib import Path
import contextlib,copy,hashlib,importlib.util,io,json,shutil,types,datetime
HERE=Path(__file__).resolve().parent;A=HERE.parents[1];SOURCE=A/'publication';WORK=HERE/'scratch_local/whole_main'
def need(c,m):
    if not c:raise RuntimeError(m)
def sha(b):return hashlib.sha256(b).hexdigest()
def obj(p):return json.loads(p.read_text())
def save(p,d):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(d,indent=2)+'\n')
def load(name):
    spec=importlib.util.spec_from_file_location('r2_'+name,SOURCE/(name+'.py'));m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
meta=obj(SOURCE/'zenodo-deposit.json')['metadata'];build=obj(SOURCE/'BUILD_RECEIPT.json')
pub={'environment':'production','state':'published','metadata_normalizations':[],'id':77,'doi':'10.5281/zenodo.77','doi_url':'https://doi.org/10.5281/zenodo.77','record_url':'https://zenodo.org/records/77','url':'https://doi.org/10.5281/zenodo.77','title':meta['title'],'files':[{'name':build[k]['path'],'size':build[k]['bytes'],'sha256':build[k]['sha256']} for k in ['pdf','verification_zip']]}
tracker_module=load('append_tracker')
def fresh(name):
    p=WORK/name/'publication'
    if p.parent.exists():shutil.rmtree(p.parent)
    p.mkdir(parents=True)
    for f in ['zenodo-deposit.json','BUILD_RECEIPT.json','append_tracker.py']:shutil.copyfile(SOURCE/f,p/f)
    save(p/'PUBLICATION_RECEIPT.json',pub);return p

public_results=[]
for case in ['positive']+list(meta)+['id','record_doi','metadata_doi','missing_file','duplicate_file','file_bytes']:
    p=fresh('public_'+case);m=load('check_public_downloads');m.ROOT=p
    remote={'id':77,'doi':pub['doi'],'metadata':copy.deepcopy(meta),'files':[{'key':build[k]['path'],'links':{'self':'https://zenodo.org/mock/'+k}} for k in ['pdf','verification_zip']]}
    remote['metadata']['resource_type']={'type':remote['metadata'].pop('upload_type'),'subtype':remote['metadata'].pop('publication_type')};remote['metadata']['license']={'id':remote['metadata']['license']};remote['metadata']['doi']=pub['doi']
    if case in meta:
        if case=='upload_type':remote['metadata']['resource_type']['type']='dataset'
        elif case=='publication_type':remote['metadata']['resource_type']['subtype']='article'
        elif case=='license':remote['metadata']['license']['id']='other'
        else:remote['metadata'][case]=None
    elif case=='id':remote['id']=78
    elif case=='record_doi':remote['doi']='10.5281/zenodo.78'
    elif case=='metadata_doi':remote['metadata']['doi']='10.5281/zenodo.78'
    elif case=='missing_file':remote['files'].pop()
    elif case=='duplicate_file':remote['files'].append(remote['files'][0])
    calls=[]
    def fetch(url,limit):
        calls.append(url)
        if url=='https://zenodo.org/api/records/77':return json.dumps(remote).encode()
        k=url.rsplit('/',1)[-1];data=(SOURCE/build[k]['path']).read_bytes();return data+b'x' if case=='file_bytes' else data
    m.fetch=fetch
    try:
        with contextlib.redirect_stdout(io.StringIO()):m.main()
    except Exception as e:ok=False;error=str(e)
    else:ok=True;error=None
    need(ok==(case=='positive'),'public main corruption incorrectly handled '+case)
    public_results.append({'case':case,'completed':ok,'error':error,'public_fetches':len(calls)})

tracker_results=[]
for case in ['positive','exact_existing','duplicate','wrong_B','uncertain_without_row','lost_append_response','wrong_header','renamed_tab','wrong_gid','readback_wrong_D','append_wrong_dimensions']:
    p=fresh('tracker_'+case);m=load('append_tracker');m.ROOT=p;row=m.expected_row(pub,meta['title']);rows=[['Original Problem','Solution Chat URL','DOI','Notes']];appends=[];lost=[case=='lost_append_response']
    if case in ['exact_existing','duplicate','wrong_B']:rows.append(copy.deepcopy(row))
    if case=='duplicate':rows.append(copy.deepcopy(row))
    if case=='wrong_B':rows[1][1]='unapproved nonblank chat'
    if case=='wrong_header':rows[0][1]='Other'
    if case=='uncertain_without_row':save(p/'tracker/INTENT.json',{'row':row})
    def call(parts,params,body=None):
        if parts==['spreadsheets','get']:return {'sheets':[{'properties':{'sheetId':0 if case=='wrong_gid' else m.GID,'title':'Renamed' if case=='renamed_tab' else 'Math Puzzles'}}]}
        if parts==['spreadsheets','values','append']:
            appends.append(copy.deepcopy(body));rows.append(copy.deepcopy(body['values'][0]))
            if lost[0]:lost[0]=False;raise RuntimeError('mocked accepted append with lost response')
            return {'updates':{'updatedRange':"'Math Puzzles'!A2:D2",'updatedRows':1,'updatedColumns':3 if case=='append_wrong_dimensions' else 4}}
        if parts==['spreadsheets','values','get']:
            if params['range']=="'Math Puzzles'!A:D":return {'values':copy.deepcopy(rows)}
            data=copy.deepcopy(rows[1:2])
            if case=='readback_wrong_D':data[0][3]='wrong notes'
            return {'values':data}
        raise RuntimeError('Unexpected tracker operation')
    m.call=call;errors=[]
    for attempt in range(2 if case in ['positive','lost_append_response'] else 1):
        try:
            with contextlib.redirect_stdout(io.StringIO()):m.main()
        except Exception as e:errors.append(str(e));completed=False
        else:completed=True
    need(completed==(case in ['positive','exact_existing','lost_append_response']),'tracker main wrongly handled '+case)
    need(len(appends)<=1,'duplicate append '+case)
    tracker_results.append({'case':case,'completed':completed,'appends':len(appends),'errors':errors,'blank_B':row[1]==''})

def pr_fixture():
    p=fresh('pr');a=p.parent
    for e in obj(HERE/'INPUT_FREEZE.json')['files']:
        dst=a/e['path'];dst.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(A/e['path'],dst)
    save(p/'PUBLICATION_RECEIPT.json',pub);review=a/'reviews/synthetic_r2';review.mkdir(exist_ok=True);(review/'REPORT.md').write_text('synthetic clean fixture');save(review/'VERDICT.json',{'status':'CLEAN'})
    u=load('update_pr_publication');u.ROOT=p;u.REPO=WORK
    gate={'schema':'math-preprint-final-review-gate-v1','pr':1241,'problem_id':11000082,'original_head':u.ORIGINAL,'status':'pass','workflow':{n:sha((p/n).read_bytes()) for n in u.REQUIRED_WORKFLOW},'latest_review':{'status':'CLEAN','report':'../reviews/synthetic_r2/REPORT.md','report_sha256':sha((review/'REPORT.md').read_bytes()),'verdict':'../reviews/synthetic_r2/VERDICT.json','verdict_sha256':sha((review/'VERDICT.json').read_bytes())},'pdf_sha256':build['pdf']['sha256'],'verification_zip_sha256':build['verification_zip']['sha256'],'metadata_sha256':sha((p/'zenodo-deposit.json').read_bytes())};save(p/'FINAL_REVIEW_GATE.json',gate)
    tracker={'spreadsheetId':tracker_module.SID,'gid':tracker_module.GID,'row':tracker_module.expected_row(pub,meta['title']),'updatedRange':"'Math Puzzles'!A22:D22",'readback_verified':True};save(p/'tracker/TRACKER_RECEIPT.json',tracker)
    public={'public_record_identity_verified':True,'all_supplied_metadata_exact':True,'metadata_manifest_sha256':sha((p/'zenodo-deposit.json').read_bytes()),'doi':pub['doi'],'id':77,'doi_url':pub['doi_url'],'record_url':pub['record_url'],'metadata_fields_verified':sorted(meta),'files':[{'name':build[k]['path'],'bytes':build[k]['bytes'],'sha256':build[k]['sha256']} for k in ['pdf','verification_zip']]};save(p/'PUBLIC_DOWNLOAD_VERIFICATION.json',public)
    return u,p,a

class Objects:
    def __init__(self,u,a,mode):
        self.u=u;self.mode=mode;self.events=[];self.blobs={};self.trees={};self.commits={};self.original={e['path']:(a/'submitted'/Path(e['path']).name).read_bytes() for e in obj(a/'SUBMITTED_SNAPSHOT.json')['files']};self.original['unrelated/preserved.txt']=b'preserved';self.root=self.make_tree(self.original);self.remote=u.ORIGINAL;self.api=u.ORIGINAL;self.body=obj(a/'LIVE_PR_PREFLIGHT.json')['body'];self.lag=False;self.lostpush=mode=='lost_push';self.lostbody=mode=='lost_body'
    def make_tree(self,files):
        nested={}
        for n,b in files.items():
            q=n.split('/');d=nested
            for x in q[:-1]:d=d.setdefault(x,{})
            d[q[-1]]=b
        def store(d):
            rows=[]
            for n,v in sorted(d.items()):
                if isinstance(v,dict):oid=store(v);rows.append(b'040000 tree '+oid.encode()+b'\t'+n.encode())
                else:oid=hashlib.sha1(b'blob '+str(len(v)).encode()+b'\0'+v).hexdigest();self.blobs[oid]=v;rows.append(b'100644 blob '+oid.encode()+b'\t'+n.encode())
            raw=b'\0'.join(rows)+b'\0';oid=hashlib.sha1(b'tree '+raw).hexdigest();self.trees[oid]=raw;return oid
        return store(nested)
    def flatten(self,t):
        if t==self.u.ORIGINAL:t=self.root
        if t in self.commits:t=self.commits[t]['tree']
        out={}
        for row in self.trees[t].split(b'\0'):
            if not row:continue
            head,name=row.split(b'\t');mode,kind,oid=head.decode().split();name=name.decode()
            if kind=='tree':out.update({name+'/'+n:b for n,b in self.flatten(oid).items()})
            else:out[name]=self.blobs[oid]
        return out
    def git(self,*args,data=None):
        cmd=args[0]
        if cmd=='branch':return b'main\n'
        if cmd=='rev-parse':return (next(e['blob'] for e in obj(self.u.ROOT.parent/'SUBMITTED_SNAPSHOT.json')['files'] if e['path']==args[1].split(':',1)[1])+'\n').encode()
        if cmd=='ls-tree':return self.trees[self.root if args[2]==self.u.ORIGINAL else args[2]]
        if cmd=='mktree':oid=hashlib.sha1(b'tree '+data).hexdigest();self.trees[oid]=data;return oid.encode()
        if cmd=='hash-object':oid=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest();self.blobs[oid]=data;return oid.encode()
        if cmd=='commit-tree':
            oid=hashlib.sha1(args[1].encode()+data).hexdigest();self.commits[oid]={'tree':args[1],'parent':args[3]};self.events.append('commit');return oid.encode()
        if cmd=='update-ref':self.events.append('private_ref');return b''
        if cmd=='rev-list':return (args[-1]+' '+self.commits[args[-1]]['parent']+'\n').encode()
        if cmd=='diff-tree':
            changed=sorted(n for n,b in self.flatten(args[-1]).items() if self.original.get(n)!=b);return ('\n'.join(changed)+'\n').encode()
        if cmd=='show':c,n=args[1].split(':',1);return self.flatten(c)[n]
        if cmd=='ls-remote':return (self.remote+' refs/heads/'+self.u.BRANCH+'\n').encode()
        if cmd=='push':
            need(args[1]=='origin' and args[2].endswith(':refs/heads/'+self.u.BRANCH) and '--force' not in args,'unapproved push')
            self.events.append('nonforce_pinned_push');self.remote=args[2].split(':')[0]
            if self.mode=='api_lag':self.lag=True
            else:self.api=self.remote
            if self.lostpush:self.lostpush=False;raise RuntimeError('accepted push lost response')
            return b''
        raise RuntimeError('Forbidden unmodeled Git call '+repr(args))
    def pr(self):return {'headRefName':self.u.BRANCH,'headRefOid':self.api,'state':'OPEN','isDraft':True,'body':self.body}
    def run(self,args,**kwargs):
        need(args[:3]==['gh','pr','edit'],'unmodeled subprocess');self.events.append('body_edit');self.body=Path(args[-1]).read_text()
        if self.lostbody:self.lostbody=False;return types.SimpleNamespace(returncode=1,stderr='accepted body lost response')
        return types.SimpleNamespace(returncode=0,stderr='')

pr_results=[]
for mode in ['positive_idempotent','api_lag','lost_push','lost_body','outside_body','outside_remote']:
    u,p,a=pr_fixture();adapter=Objects(u,a,mode);u.git=adapter.git;u.pr=adapter.pr;u.subprocess=types.SimpleNamespace(run=adapter.run)
    if mode=='outside_body':adapter.body='outside edit'
    if mode=='outside_remote':adapter.remote='c'*40
    errors=[]
    for attempt in range(2 if mode not in ['outside_body','outside_remote'] else 1):
        if attempt and adapter.lag:adapter.api=adapter.remote
        try:
            with contextlib.redirect_stdout(io.StringIO()):u.main()
        except Exception as e:errors.append(str(e));done=False
        else:done=True
    need(done==(mode not in ['outside_body','outside_remote']),'full PR main failed '+mode+repr(errors))
    need(adapter.events.count('nonforce_pinned_push')<=1 and adapter.events.count('body_edit')<=1,'retry duplicate external action')
    if done:
        receipt=obj(p/'PR_BRANCH_RECEIPT.json');commit=receipt['commit'];changed=[n for n,b in adapter.flatten(commit).items() if adapter.original.get(n)!=b];need(len(changed)==13 and adapter.commits[commit]['parent']==u.ORIGINAL and adapter.flatten(commit)['unrelated/preserved.txt']==b'preserved','actual modeled tree contract')
        for key in ['pr','base','branch','paths','files','review_gate_sha256','metadata_sha256','doi','doi_url','record_url','deposit_id','tracker_range','tracker_receipt_sha256','public_verification_receipt_sha256','body_sha256','shared_index_modified']:
            bad=copy.deepcopy(receipt);bad[key]='corrupt saved identity';save(p/'PR_BRANCH_RECEIPT.json',bad)
            try:
                with contextlib.redirect_stdout(io.StringIO()):u.main()
            except RuntimeError:pass
            else:raise RuntimeError('corrupt full-main saved identity accepted '+key)
        save(p/'PR_BRANCH_RECEIPT.json',receipt)
        originalparent=adapter.commits[commit]['parent'];adapter.commits[commit]['parent']='d'*40
        try:
            with contextlib.redirect_stdout(io.StringIO()):u.main()
        except RuntimeError:pass
        else:raise RuntimeError('wrong actual parent accepted')
        adapter.commits[commit]['parent']=originalparent
        actual_flatten=adapter.flatten
        for corruption in ['unexpected_path','different_blob_bytes']:
            def corrupted_flatten(t):
                out=actual_flatten(t)
                if t==commit:
                    if corruption=='unexpected_path':out['foreign/unapproved.txt']=b'bad'
                    else:out[sorted(changed)[0]]=b'different modeled commit blob'
                return out
            adapter.flatten=corrupted_flatten
            try:
                with contextlib.redirect_stdout(io.StringIO()):u.main()
            except RuntimeError:pass
            else:raise RuntimeError('corrupted actual modeled commit accepted '+corruption)
            adapter.flatten=actual_flatten
    pr_results.append({'case':mode,'completed':done,'errors':errors,'events':adapter.events,'actual_tree_13_paths_parent_and_preserved_outside':done,'saved_identity_corruptions_rejected':16 if done else 0,'actual_parent_extra_path_and_blob_corruptions_rejected':3 if done else 0})
save(HERE/'EXTERNAL_AND_PR_RESULTS.json',{'at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'public_complete_main':public_results,'tracker_complete_main':tracker_results,'PR_complete_main':pr_results,'scope':'Actual unmodified helper main functions, ROOT redirected to copies. Public fetch/GWS calls and all Git object/branch/body operations replaced by in-memory adapters; no live application, real Git object/index/ref, API or network operation. Synthetic review gate is positive plumbing fixture, never a real clean verdict. No strict server or concurrency guarantee is inferred.'})
print(json.dumps({'public_main_cases':len(public_results),'tracker_main_cases':len(tracker_results),'PR_main_cases':len(pr_results),'all_expected_outcomes':True}))
