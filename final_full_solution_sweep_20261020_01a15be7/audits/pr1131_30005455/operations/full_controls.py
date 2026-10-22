#!/usr/bin/env python3
"""Operations03 repair controls, adapted from read-and-pinned operations02 adversary.
Run only through externally verified bootstrap in a NEW private mirror.
All real networking, token loading and process creation are disabled before source
bootstrap/module loading. The service models perform only in-memory events.
"""
if not globals().get('_PR1131_SOURCE_VERIFIED',False):raise RuntimeError('Use externally hash-verified bootstrap')
import argparse,base64,contextlib,copy,datetime,hashlib,http.client,importlib.util,io,json,marshal,os,socket,ssl,struct,subprocess,sys,types,urllib.request,uuid
from pathlib import Path
from urllib.parse import parse_qs,urlsplit
EXPECTED=_PR1131_EXECUTION['operations_sha256']
BOOT=_PR1131_EXECUTION['bootstrap_sha256']
ATTEMPTS=[]
def blocked(*a,**k):ATTEMPTS.append('blocked external path');raise RuntimeError('Reviewer forbids network/process execution')
# Block interfaces before any project code, including the source bootstrap.
socket.socket=blocked;socket.create_connection=blocked;socket.getaddrinfo=blocked
http.client.HTTPConnection=blocked;http.client.HTTPSConnection=blocked
urllib.request.urlopen=blocked;urllib.request.OpenerDirector.open=blocked
subprocess.run=blocked;subprocess.Popen=blocked;subprocess.call=blocked;subprocess.check_call=blocked;subprocess.check_output=blocked
os.system=blocked;os.popen=blocked;os.spawnv=blocked;os.spawnve=blocked;os.execv=blocked;os.execve=blocked

def sha(b):return hashlib.sha256(b).hexdigest()
def need(v,m):
    if not v:raise RuntimeError(m)
def dump(p,v):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(v,indent=2,ensure_ascii=False)+'\n')
@contextlib.contextmanager
def patch(*changes):
    prior=[]
    try:
        for o,k,v in changes:prior.append((o,k,getattr(o,k)));setattr(o,k,v)
        yield
    finally:
        for o,k,v in reversed(prior):setattr(o,k,v)
def rejects(fn):
    try:fn()
    except Exception as e:return {'type':type(e).__name__,'message':str(e)}
    raise RuntimeError('Fault accepted')

def load_bundle(mirror):
    ops=mirror/'final_full_solution_sweep_20261020_01a15be7/audits/pr1131_30005455/operations'
    load,ctx=_PR1131_BOOTSTRAP(ops,EXPECTED,BOOT)
    modules={n:load(n) for n in ['ops_common','collect_live','integrate_remote','native_policy','publish_and_ledger','check_package']}
    z=modules['ops_common'].zenodo
    z.token_for=lambda *a,**k:'OFFLINE_SENTINEL_NO_CREDENTIAL'
    z.doi_status=lambda doi:{'status':'offline_mock','url':'https://doi.org/'+doi}
    return ops,modules,load,{'load_verified':_PR1131_BOOTSTRAP}

class Git:
    def __init__(self,c,ops):
        self.c=c;self.ops=ops;self.blobs={};self.trees={};self.commits={};self.writes=[]
        pkg=c.package();queue=b'| 1347 | 30005455 / OWR-12697708-008 | Target | 0.0752 | 5.0 | 3 | 2023 | queued | 0/5 |  |  |  |\n'
        common={'README_ROOT.md':b'root sibling\n',c.QUEUE:queue,'unsolved_math_prioritization/attempts/555/KEEP.md':b'sibling attempt\n','unsolved_math_prioritization/UNCHANGED.md':b'unselected\n'}
        self.parent='2'*40;self.main='1'*40
        self.save_commit(self.parent,common,[])
        original={**common,**{c.PROBLEM+'/'+n:pkg['source']['original/'+n] for n in c.ORIGINALS}}
        self.save_commit(c.ORIGINAL,original,[self.parent])
        self.save_commit(self.main,{**common,'NEW_ROOT.md':b'concurrent root\n',c.PROBLEM+'/CONCURRENT_EXTRA.md':b'preserve selected extra\n'},[self.parent])
        self.head=c.ORIGINAL
        self.pr=json.loads((ops/'private/live_8e3a39143bb740ef9053274be751a820/pr.json').read_bytes())
        self.pr.update(number=1131,state='open',merged=False,draft=True,title=json.loads((ops/'READ_ONLY_OBSERVATIONS.json').read_bytes())['original_pr_title'])
        self.pr['head']={'sha':self.head,'ref':c.BRANCH,'repo':{'full_name':c.REPOSITORY}}
        self.pr['base']={'sha':self.main,'ref':'main','repo':{'full_name':c.REPOSITORY}}
        self.pr['node_id']='OFFLINE_PR_NODE'
        need(c.sha(self.pr['body'].encode())==json.loads((ops/'READ_ONLY_OBSERVATIONS.json').read_bytes())['original_pr_body_sha256'],'Raw PR capture body mismatch')
    def blob(self,b):
        h=hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest();self.blobs[h]=b;return h
    def tree(self,flat):
        nested={}
        for n,b in flat.items():
            parts=n.split('/');cur=nested
            for part in parts[:-1]:cur=cur.setdefault(part,{})
            cur[parts[-1]]=b
        def build(v):
            es=[]
            for n,b in sorted(v.items()):
                if isinstance(b,dict):es.append({'path':n,'mode':'040000','type':'tree','sha':build(b)})
                else:es.append({'path':n,'mode':'100644','type':'blob','sha':self.blob(b)})
            h=sha(json.dumps(es,sort_keys=True).encode())[:40];self.trees[h]=es;return h
        return build(nested)
    def flatten(self,tree,prefix=''):
        out={}
        for e in self.trees[tree]:
            n=prefix+e['path']
            if e['type']=='tree':out.update(self.flatten(e['sha'],n+'/'))
            else:out[n]=self.blobs[e['sha']]
        return out
    def save_commit(self,identifier,flat,parents):
        t=self.tree(flat);self.commits[identifier]={'sha':identifier,'tree':{'sha':t},'parents':[{'sha':p} for p in parents]};return identifier
    def test_merge(self):
        h=sha((self.main+self.head+'test').encode())[:40]
        self.commits[h]={'sha':h,'tree':copy.deepcopy(self.commits[self.head]['tree']),'parents':[{'sha':self.main},{'sha':self.head}]}
        return h
    def get(self,endpoint):
        if endpoint=='pulls/1131':
            pr=copy.deepcopy(self.pr);pr['head']['sha']=self.head;pr['base']['sha']=self.main
            if not pr['merged']:pr.update(mergeable=True,merge_commit_sha=self.test_merge())
            return pr
        if endpoint=='git/ref/heads/main':return {'object':{'sha':self.main}}
        if endpoint.startswith('git/commits/'):return copy.deepcopy(self.commits[endpoint.rsplit('/',1)[1]])
        if endpoint.startswith('git/blobs/'):
            h=endpoint.rsplit('/',1)[1];return {'sha':h,'encoding':'base64','content':base64.b64encode(self.blobs[h]).decode()}
        if endpoint.startswith('git/trees/'):
            h=endpoint.split('/')[-1].split('?')[0];es=copy.deepcopy(self.trees[h])
            if '?' in endpoint:
                def expand(tree,prefix=''):
                    r=[]
                    for e in self.trees[tree]:
                        r.append({**e,'path':prefix+e['path']})
                        if e['type']=='tree':r.extend(expand(e['sha'],prefix+e['path']+'/'))
                    return r
                es=expand(h)
            return {'sha':h,'truncated':False,'tree':es}
        raise RuntimeError('Unhandled Git GET '+endpoint)
    def write(self,endpoint,method,body):
        self.writes.append({'endpoint':endpoint,'method':method,'body':copy.deepcopy(body)})
        if endpoint=='git/blobs':return {'sha':self.blob(base64.b64decode(body['content']))}
        if endpoint=='git/trees':
            flat=self.flatten(body['base_tree'])
            for e in body['tree']:need(e['mode']=='100644' and e['type']=='blob','Bad tree write');flat[e['path']]=self.blobs[e['sha']]
            return {'sha':self.tree(flat)}
        if endpoint=='git/commits':
            h=sha(json.dumps(body,sort_keys=True).encode())[:40];self.commits[h]={'sha':h,'tree':{'sha':body['tree']},'parents':[{'sha':p} for p in body['parents']]};return copy.deepcopy(self.commits[h])
        if endpoint.startswith('git/refs/heads/'):
            need(body['force'] is False,'Forced update');need(self.head in [p['sha'] for p in self.commits[body['sha']]['parents']],'Non-descendant update');self.head=body['sha'];return {'object':{'sha':self.head}}
        if endpoint=='pulls/1131':self.pr['body']=body['body'];return copy.deepcopy(self.pr)
        if endpoint=='graphql':self.pr['draft']=False;return {'data':{'markPullRequestReadyForReview':{'pullRequest':{'id':self.pr['node_id'],'isDraft':False}}}}
        if endpoint=='pulls/1131/merge':
            need(body['sha']==self.head and body['merge_method']=='merge','Bad merge payload');h=self.test_merge();self.main=h;self.pr.update(merged=True,state='closed',merge_commit_sha=h);return {'merged':True,'sha':h}
        raise RuntimeError('Unhandled Git mutation '+endpoint)

class Native:
    def __init__(self,ops,c):
        self.ops=ops;self.c=c;self.base='https://zenodo.org';self.metadata,self.uploads=c.zenodo.load_manifest(ops/'proposed/preprint/zenodo-deposit.json')
        self.present={};self.published=False;self.allocated=False;self.calls=[];self.fault=None;self.after=None;self.lost=False
        ref=ops/'private/repair_native_reference'
        self.lr=json.loads((ref/'published_owned_legacy_23408971.json').read_bytes());self.nr=json.loads((ref/'published_native_23408971.json').read_bytes());self.fr=json.loads((ref/'published_files_23408971.json').read_bytes());self.publicref=json.loads((ref/'published_public_legacy_23408971.json').read_bytes())
        self.owner=self.lr['owner'];self.bucket=str(uuid.UUID(int=900));self.fileids={e['name']:str(uuid.UUID(int=1000+i)) for i,e in enumerate(self.uploads)}
    def records(self):
        md={**copy.deepcopy(self.metadata),'doi':'10.5281/zenodo.777','prereserve_doi':{'doi':'10.5281/zenodo.777','recid':777},'access_right':'open','imprint_publisher':'Zenodo','language':'eng'}
        l={**copy.deepcopy(self.lr),'id':777,'record_id':777,'conceptrecid':'778','conceptdoi':'10.5281/zenodo.778','owner':self.owner,'doi':'10.5281/zenodo.777','doi_url':'https://doi.org/10.5281/zenodo.777','metadata':md,'submitted':self.published,'state':'done' if self.published else 'unsubmitted','files':[],'links':{'bucket':'https://zenodo.org/api/files/'+self.bucket,'html':'https://zenodo.org/uploads/777'}}
        n=copy.deepcopy(self.nr);n.update(id='777',is_published=self.published,is_draft=not self.published,status='published' if self.published else 'draft',custom_fields={},versions={'index':1,'is_latest':True})
        n['pids']={'doi':{'identifier':l['doi'],'provider':'datacite','client':'datacite'}}
        if self.published:n['pids']['oai']={'identifier':'oai:zenodo.org:777','provider':'oai'}
        n['parent'].update(id='778',pids={'doi':{'identifier':'10.5281/zenodo.778','provider':'datacite','client':'datacite'}},communities={})
        n['parent']['access']={'owned_by':{'user':str(self.owner)},'settings':{'allow_user_requests':False,'allow_guest_requests':False,'accept_conditions_text':None,'secret_link_expiration':0}}
        n['access']={'record':'public','files':'public','embargo':{'active':False,'reason':None},'status':'open'}
        n['metadata']={k:copy.deepcopy(self.nr['metadata'][k]) for k in ['resource_type','languages','rights']}
        n['metadata'].update(title=self.metadata['title'],publisher='Zenodo',publication_date=self.metadata['publication_date'],version=self.metadata['version'],description=self.metadata['description'],creators=[{'person_or_org':{'type':'personal','name':'Kriebel, Alec','given_name':'Alec','family_name':'Kriebel','identifiers':[{'scheme':'orcid','identifier':'0009-0001-9320-500X'}]},'affiliations':[{'name':'Independent researcher'}]}],subjects=[{'subject':v} for v in self.metadata['keywords']],related_identifiers=[{'identifier':v['identifier'],'scheme':v['scheme'],'relation_type':{'id':v['relation'].lower()}} for v in self.metadata['related_identifiers']],references=[{'reference':v} for v in self.metadata['references']])
        n['files']={'enabled':True,'order':[],'count':len(self.present),'total_bytes':sum(e['size'] for e in self.present.values()),'entries':{}}
        n['media_files']={'enabled':False,'order':[],'count':0,'total_bytes':0,'entries':{}}
        fc={'enabled':True,'links':copy.deepcopy(self.fr['links']),'entries':[],'default_preview':None,'order':[]}
        template=next(iter(self.nr['files']['entries'].values()));ft=self.fr['entries'][0]
        for name,e in self.present.items():
            i=next(i for i,v in enumerate(self.uploads) if v['name']==name);fid=self.fileids[name];ext=name.rsplit('.',1)[1];mime='application/'+ext;route='https://zenodo.org/api/records/777'+('' if self.published else '/draft')+'/files/'+name;links={'self':route,'content':route+'/content'}
            l['files'].append({'filename':name,'id':fid,'checksum':e['md5'],'filesize':e['size']})
            n['files']['entries'][name]={**copy.deepcopy(template),'id':fid,'key':name,'ext':ext,'size':e['size'],'checksum':'md5:'+e['md5'],'mimetype':mime,'storage_class':'L','metadata':{},'access':{'hidden':False},'links':copy.deepcopy(links)}
            fc['entries'].append({**copy.deepcopy(ft),'key':name,'file_id':fid,'version_id':str(uuid.UUID(int=2000+i)),'bucket_id':self.bucket,'checksum':'md5:'+e['md5'],'size':e['size'],'mimetype':mime,'storage_class':'L','metadata':{},'access':{'hidden':False},'links':copy.deepcopy(links),'transfer':{'type':'L'},'status':'completed'})
        if self.fault:self.fault(l,n,fc)
        return l,n,fc
    def get(self,i):need(i==777,'Wrong target ID');return self.records()[0]
    def native_get(self,i,draft=False):need(i==777 and draft is (not self.published),'Wrong native state');return self.records()[1]
    def request(self,method,url):need(method=='GET' and url=='https://zenodo.org/api/records/777'+('' if self.published else '/draft')+'/files','Wrong finalized-file GET');return self.records()[2]
    def create(self,md):need(not self.allocated and md==self.metadata,'Repeated create/metadata');self.calls.append('create');self.allocated=True;return self.get(777)
    def upload(self,b,e):need(b=='https://zenodo.org/api/files/'+self.bucket,'Wrong upload destination');self.calls.append('upload:'+e['name']);self.present[e['name']]=e;return {}
    def update(self,i,md):need(i==777 and md==self.metadata,'Wrong update');self.calls.append('update');return self.get(777)
    def publish(self,i):
        need(i==777 and not self.published,'Repeated publication');self.calls.append('publish');self.published=True
        if self.after:self.fault=self.after
        if self.lost:raise self.c.zenodo.DepositError('Simulated response lost after POST success')
        return self.get(777)
    def public(self):
        l,n,f=self.records();p={**copy.deepcopy(self.publicref),**l,'status':'published','owners':[self.owner]};p['metadata']=copy.deepcopy(l['metadata']);md=p['metadata'];md.pop('upload_type');md.pop('publication_type');md['resource_type']={'type':'publication','subtype':'preprint','title':'Preprint'};md['license']={'id':self.metadata['license']};md['relations']={'version':[{'index':0,'is_last':True,'parent':{'pid_type':'recid','pid_value':'778'}}]};return p

class World:
    def __init__(self,ops,modules):
        self.ops=ops;self.m=modules;self.c=modules['ops_common'];self.git=Git(self.c,ops);self.native=Native(ops,self.c);self.sheet=json.loads((ops/'private/live_8e3a39143bb740ef9053274be751a820/ledger.json').read_bytes());self.rows=copy.deepcopy(self.sheet['values']);self.accounts=[]
        for i in range(1,9):self.accounts+=json.loads((ops/f'private/live_8e3a39143bb740ef9053274be751a820/account_a_page_{i}.json').read_bytes())
        need(len(self.accounts)==197,'Not actual197 fixture');self.events=[];self.appends=0;self.append_mode=None;self.gate_hook=None;self.get_hook=None;self.doi_bad=False;self.bytes_bad=False;self.public_bad=False;self.account_fault=None;self.response_fault=None;self.tab_gid=1254632077;self.target_title='Math Puzzles';self.read_fault=None;self.numeric_calls=0;self.formula_fault=False;self.replace_before_append=False
    def records(self):return copy.deepcopy(self.accounts)+([self.native.get(777)] if self.native.allocated else [])
    def connection(self,*a,**k):
        world=self
        class Conn:
            def request(self,method,url,headers):
                need(method=='GET' and headers['Authorization']=='Bearer OFFLINE_SENTINEL_NO_CREDENTIAL','Unexpected account method/auth');self.target=url
            def getresponse(self):
                p=int(parse_qs(urlsplit(self.target).query)['page'][0]);rs=world.records()
                if world.account_fault:rs=world.account_fault(rs,p)
                b=json.dumps(rs[(p-1)*25:p*25]).encode();world.events.append({'account_page':p,'records':len(rs[(p-1)*25:p*25])})
                return types.SimpleNamespace(status=200,read=lambda limit:b)
            def close(self):pass
        return Conn()
    def book(self):
        return {'spreadsheetId':self.c.SHEET,'sheets':[{'properties':{'sheetId':self.tab_gid,'title':self.target_title,'sheetType':'GRID','gridProperties':{'rowCount':1177,'columnCount':43}}}]}
    def command(self,argv,body=None):
        if argv[0]=='gws':
            params=json.loads(argv[argv.index('--params')+1]);need(params.get('spreadsheetId')==self.c.SHEET,'Wrong workbook request')
            if argv[3]=='get':return self.book()
            payload=json.loads(argv[argv.index('--json')+1])
            if argv[3:5]==['values','batchGetByDataFilter']:
                grid={'sheetId':1254632077,'startColumnIndex':0,'endColumnIndex':43}
                need(payload in [{'dataFilters':[{'gridRange':grid}],'majorDimension':'ROWS','valueRenderOption':mode} for mode in ['UNFORMATTED_VALUE','FORMULA']],'Numeric read differs')
                need(self.tab_gid==1254632077,'Intended numeric tab does not exist')
                response={'spreadsheetId':self.c.SHEET,'valueRanges':[{'dataFilters':[{'gridRange':grid}],'valueRange':{'majorDimension':'ROWS','range':"'Math Puzzles'!A1:AQ1177",'values':copy.deepcopy(self.rows)}}]}
                if self.formula_fault and payload['valueRenderOption']=='FORMULA':response['valueRanges'][0]['valueRange']['values'][-1][0]='=CONCAT("masked")'
                self.numeric_calls+=1
                if self.read_fault:self.read_fault(response)
                return response
            need(argv[3]=='batchUpdate','Unexpected GWS path')
            if self.replace_before_append:self.tab_gid=999999999
            a=payload['requests'][0]['appendCells'];row=[v['userEnteredValue']['stringValue'] for v in a['rows'][0]['values']]
            expected={'requests':[{'appendCells':{'sheetId':1254632077,'rows':[{'values':[{'userEnteredValue':{'stringValue':v}} for v in row]}],'fields':'userEnteredValue'}}],'includeSpreadsheetInResponse':True,'responseIncludeGridData':False}
            need(payload==expected and len(row)==4 and a['sheetId']==self.tab_gid,'Wrong numeric append destination/payload')
            self.appends+=1;self.rows.append(copy.deepcopy(row))
            if self.append_mode=='lost':raise RuntimeError('Lost append success response')
            if self.append_mode=='prior_row_drift':self.rows[1][0]+=' changed'
            if self.append_mode=='duplicate':self.rows.append(copy.deepcopy(row))
            response={'spreadsheetId':self.c.SHEET,'replies':[{}],'updatedSpreadsheet':self.book()}
            self.events.append({'appended_gid':self.tab_gid})
            if self.response_fault:self.response_fault(response)
            return response
        need(argv[0]=='gh','Unexpected process path');endpoint=argv[4].removeprefix('repos/'+self.c.REPOSITORY+'/')
        if '--method' not in argv and endpoint!='graphql':
            if self.get_hook:self.get_hook(endpoint)
            return self.git.get(endpoint)
        return self.git.write(endpoint,argv[argv.index('--method')+1] if '--method' in argv else 'POST',body)
    def fetch(self,url,limit):
        if url=='https://zenodo.org/api/records/777':
            p=self.native.public()
            if self.public_bad:p['metadata']['copyright']='unreviewed'
            return json.dumps(p).encode(),200,url
        if url.startswith('https://zenodo.org/records/777/files/'):
            name=url.split('/files/')[1].split('?')[0];e=next(v for v in self.native.uploads if v['name']==name);b=e['path'].read_bytes()
            if self.bytes_bad:b=b[:-1]+bytes([b[-1]^1])
            return b,200,url
        need(url=='https://doi.org/10.5281/zenodo.777','Wrong DOI target');return b'landing',200,('https://zenodo.org/records/888' if self.doi_bad else 'https://zenodo.org/records/777')
    def clearance(self):
        c=json.loads((self.ops/'ROOT_OPERATIONAL_CLEARANCE.example.json').read_bytes());c.update(operations_manifest_sha256=EXPECTED,bootstrap_sha256=BOOT,publication_ready=True,unresolved_operational_findings=[],root_complete_reports_read_and_all_seals_verified=True,allowed_actions=['integrate','pr-description','ready','merge','stage','publish','ledger'],instructions='OFFLINE FIXTURE ONLY: no authority outside this private mirror')
        dump(self.ops/'runtime/ROOT_OPERATIONAL_CLEARANCE.json',c);return sha((self.ops/'runtime/ROOT_OPERATIONAL_CLEARANCE.json').read_bytes())
    @contextlib.contextmanager
    def installed(self):
        z=self.c.zenodo;changes=[(self.c,'command',self.command),(http.client,'HTTPSConnection',self.connection),(z,'ZenodoClient',lambda *a:self.native),(self.m['integrate_remote'],'command',self.command),(self.m['publish_and_ledger'],'command',self.command),(self.m['publish_and_ledger'],'fetch',self.fetch)]
        if self.gate_hook:
            live=self.m['collect_live'];actual=live.collect
            def wrapped(*a,**k):
                r=actual(*a,**k);self.gate_hook(*a,**k);return r
            changes += [(self.m['integrate_remote'],'collect',wrapped),(self.m['publish_and_ledger'],'collect',wrapped)]
        with patch(*changes):yield
    def args(self,action):return types.SimpleNamespace(action=action,expected_pr_head=self.git.head,clearance_sha256=self.clearance_sha,operations_sha256=EXPECTED,deposit_id=None if action=='stage' else 777)
    def integrate(self):
        ir=self.m['integrate_remote'];a=self.args('integrate');a.expected_pr_head=self.c.ORIGINAL;return ir.integrate(a)
    def through_merge(self):
        ir=self.m['integrate_remote'];self.integrate();ir.describe(self.args('pr-description'));ir.mark_ready(self.args('ready'));ir.test_merge(self.args('verify-test-merge'));return ir.merge(self.args('merge'))
    def stage_publish(self):
        pub=self.m['publish_and_ledger'];pub.lifecycle(self.args('stage'));return pub.lifecycle(self.args('publish'))

RESULTS=[]
def result(name,fn):
    try:v=fn();RESULTS.append({'name':name,'status':'PASS','detail':v})
    except Exception as e:RESULTS.append({'name':name,'status':'FAIL','detail':{'type':type(e).__name__,'message':str(e)}})
    print(json.dumps({'completed':name,'status':RESULTS[-1]['status'],'error':RESULTS[-1]['detail'] if RESULTS[-1]['status']=='FAIL' else None}),flush=True)

def run(args):
    mirror=Path(__file__).resolve().parents[4]
    need('private' in mirror.parts and mirror.name=='Math' and (mirror.parent/'COPY_RECEIPT.json').is_file(),'Full controls require a NEW prepared private mirror')
    need(args.output.parent.resolve()==mirror.parent and not args.output.exists() and not args.output.is_symlink(),'Full-control output must be a fresh file in its private fixture root')
    ops,m,load,bootstrap=load_bundle(mirror);c=m['ops_common'];ir=m['integrate_remote'];pub=m['publish_and_ledger'];live=m['collect_live'];native=m['native_policy']
    # Deduplicate byte-identical generated capture files after the real exclusive
    # durable writer/fsync finishes. This conserves local disk without changing
    # file bytes, validation or operation ordering. Originals are never linked.
    dedup={};actual_durable=c.durable
    def compact_durable(path,value):
        actual_durable(path,value)
        body=path.read_bytes();key=sha(body)
        if key in dedup and dedup[key].exists():
            canonical=dedup[key];need(canonical.read_bytes()==body,'Duplicate capture bytes differ')
            temporary=path.with_name(path.name+'.dedup_'+uuid.uuid4().hex)
            try:
                os.link(canonical,temporary)
                need(temporary.read_bytes()==body,'Temporary duplicate link bytes differ')
                os.replace(temporary,path)
            finally:
                if temporary.exists():temporary.unlink()
        else:dedup[key]=path
    for module in m.values():
        if hasattr(module,'durable'):module.durable=compact_durable
    # All future instances use a new private copy of the same public sources.
    count=0
    def fresh_world(label):
        nonlocal count
        count+=1;root=ops/'private'/('independent_'+str(count)+'_'+label);root.mkdir(parents=True)
        # Bind all module globals to a separate intent/capture namespace while
        # retaining the unchanged sealed operations path and scientific package.
        rt=root/'runtime';pr=root/'private';rt.mkdir();pr.mkdir()
        for module in m.values():
            if hasattr(module,'RUNTIME'):module.RUNTIME=rt
            if hasattr(module,'PRIVATE'):module.PRIVATE=pr
        c.zenodo.STATE_DIR=root/'.zenodo-state'
        w=World(ops,m)
        cl=json.loads((ops/'ROOT_OPERATIONAL_CLEARANCE.example.json').read_bytes());cl.update(operations_manifest_sha256=EXPECTED,bootstrap_sha256=BOOT,publication_ready=True,unresolved_operational_findings=[],root_complete_reports_read_and_all_seals_verified=True,allowed_actions=['integrate','pr-description','ready','merge','stage','publish','ledger'],instructions='OFFLINE FIXTURE ONLY; never authorizes original workflow')
        dump(rt/'ROOT_OPERATIONAL_CLEARANCE.json',cl);w.clearance_sha=sha((rt/'ROOT_OPERATIONAL_CLEARANCE.json').read_bytes())
        # collect's local-state scan is a fixed REPO/.zenodo-state path. Mirror
        # that one directory to the same offline state store, never a real path.
        # Patch local-state retrieval into the actual tools below; also expose
        # fake state captures explicitly when target-bearing state is relevant.
        return w
    def whole():
        w=fresh_world('whole');before=w.git.flatten(w.git.commits[w.git.main]['tree']['sha'])
        with w.installed():
            merged=w.through_merge();staged=w.stage_publish();verified=pub.verify_public(w.args('verify-public'));ledger=pub.append_ledger(w.args('ledger'))
        actual=w.git.flatten(w.git.commits[w.git.main]['tree']['sha']);overlay=c.proposal()[1];need(all(actual[n]==b for n,b in before.items()),'Concurrent main files changed');need(all(actual[n]==b for n,b in overlay.items()),'Wrong overlay');need(w.appends==1 and ledger['verified'] and staged['doi']=='10.5281/zenodo.777','Wrong final result')
        return {'integration_head':w.git.head,'selected_files':len([n for n in actual if n.startswith(c.PROBLEM+'/')]),'unselected_preserved':True,'native_writes':w.native.calls,'git_write_methods':[e['method'] for e in w.git.writes],'ledger_appends':w.appends,'ledger_row':ledger['row'],'full_account_pages':len(w.events),'real_network_or_process_calls':0}
    result('whole_workflow_real197_full_gates_native_public_DOI_exact_ledger',whole)
    def describe_title():
        w=fresh_world('describe_title')
        with w.installed():w.integrate()
        orig=w.git.pr['body'];w.gate_hook=lambda *a,**k:w.git.pr.__setitem__('title','Unreviewed concurrent title')
        with w.installed():error=rejects(lambda:ir.describe(w.args('pr-description')))
        writes=[v for v in w.git.writes if v['endpoint']=='pulls/1131'];need(len(writes)==0 and w.git.pr['body']==orig,'Original-title final guard permitted PATCH');need(not (ir.RUNTIME/'PR_DESCRIPTION_VERIFIED.json').exists(),'Unexpected success')
        return {'finding':'F1_description_title_gate_race','body_PATCH_count':0,'unreviewed_title_preserved':w.git.pr['title'],'error':error,'verified_receipt':False,'subsequent_actions_executed':0}
    result('F1_description_title_changed_during_gate_zero_PATCH',describe_title)
    def final_description_ready_merge():
        cases=[]
        for action in ['ready','merge']:
            for field in ['body','title','draft','head']:
                w=fresh_world(action+'_'+field)
                with w.installed():w.integrate();ir.describe(w.args('pr-description'))
                if action=='merge':
                    with w.installed():ir.mark_ready(w.args('ready'))
                before=len(w.git.writes)
                def drift(*a,**k):
                    if field=='head':w.git.head='e'*40
                    elif field=='draft':w.git.pr['draft']=action=='merge'
                    else:w.git.pr[field]='Concurrent drift'
                w.gate_hook=drift
                with w.installed():e=rejects(lambda:(ir.mark_ready if action=='ready' else ir.merge)(w.args(action)))
                need(len(w.git.writes)==before,'Final guard wrote after drift');cases.append({'action':action,'field':field,'writes':0,'error':e})
        return cases
    result('independent_full_gate_ready_merge_final_guards',final_description_ready_merge)
    def native_faults():
        cases={
            'concept_doi_legacy':lambda l,n,f:l.__setitem__('conceptdoi','10.5281/zenodo.999'),
            'native_parent_owner_change':lambda l,n,f:n['parent']['access']['owned_by'].__setitem__('user','999'),
            'legacy_owner_consistent_native_changed':lambda l,n,f:(l.__setitem__('owner',999),n['parent']['access']['owned_by'].__setitem__('user','999')),
            'public_files_access':lambda l,n,f:n['access'].__setitem__('files','restricted'),
            'version_2':lambda l,n,f:n.__setitem__('versions',{'index':2,'is_latest':True}),
            'reserver_ID_bool':lambda l,n,f:l['metadata']['prereserve_doi'].__setitem__('recid',True),
            'metadata_reference_changed':lambda l,n,f:n['metadata']['references'][0].__setitem__('reference','changed'),
            'file_pending':lambda l,n,f:f['entries'][0].__setitem__('status','pending'),
            'file_bucket_change':lambda l,n,f:f['entries'][0].__setitem__('bucket_id',str(uuid.UUID(int=555))),
            'metadata_upload_added':lambda l,n,f:l['files'].append({**l['files'][0],'filename':'extra.pdf'}),
            'native_entry_renamed':lambda l,n,f:n['files']['entries'][next(iter(n['files']['entries']))].__setitem__('key','else.pdf'),
            'unknown_file_field':lambda l,n,f:f['entries'][0].__setitem__('embargo','2029'),
        };out=[]
        for label,fault in cases.items():
            w=fresh_world('native_'+label);w.native.allocated=True;w.native.present={e['name']:e for e in w.native.uploads};guard=pub.GuardedClient(w.args('publish'),'publish',777,w.native)
            # For these isolated semantics, full Git preconditions are separately
            # exercised in whole(); retain actual target policy/observations.
            with patch((pub,'require_action',lambda *a:{}),(pub,'collect',lambda *a,**k:({'at_start':c.stamp()},None,None))):
                guard.get(777);w.native.fault=fault
                try:guard.publish(777);accepted=True;error=None
                except Exception as e:accepted=False;error=str(e)
            need(not accepted and w.native.calls.count('publish')==0,'Native semantic fault reached POST: '+label)
            out.append({'fault':label,'accepted':accepted,'POSTs':w.native.calls.count('publish'),'error':error})
        return out
    result('new_native_semantic_cross_projection_faults',native_faults)
    def recovery(lost,post_fault=False):
        w=fresh_world('recovery')
        with w.installed():
            w.through_merge();pub.lifecycle(w.args('stage'));w.native.lost=lost
            if not lost:w.native.published=True
            if post_fault:w.native.after=lambda l,n,f:n['pids']['doi'].__setitem__('provider','external')
            if post_fault:
                e=rejects(lambda:pub.lifecycle(w.args('publish')));need(w.native.calls.count('publish')==1,'Wrong POST count');need(not (pub.RUNTIME/'ZENODO_PUBLISH_VERIFIED.json').exists(),'Falsely verified')
                return {'POSTs':1,'error':e,'verified':False}
            r=pub.lifecycle(w.args('publish'));need(r['state'] if 'state' in r else r['doi']=='10.5281/zenodo.777','Recovery failed')
        return {'POSTs':w.native.calls.count('publish'),'already_published':not lost,'DOI':r['doi']}
    result('whole_lifecycle_already_published_zero_POST',lambda:recovery(False))
    result('whole_lifecycle_lost_success_one_POST',lambda:recovery(True))
    result('whole_lifecycle_native_postflight_fails_no_verified_receipt',lambda:recovery(True,True))
    def append_unknown(mode):
        w=fresh_world('ledger_'+str(mode))
        with w.installed():
            w.through_merge();w.stage_publish();w.append_mode=mode
            if mode:
                e=rejects(lambda:pub.append_ledger(w.args('ledger')));need(w.appends==1 and (pub.RUNTIME/'LEDGER_APPEND_INTENT.json').exists(),'Missing one-shot intent')
                w.append_mode=None
                if mode=='lost':
                    r=pub.append_ledger(w.args('ledger'));need(r['new_row'] is False and w.appends==1,'Recovery appended twice');intent=json.loads((pub.RUNTIME/'LEDGER_APPEND_INTENT.json').read_bytes());need(intent['sheet_id']==1254632077,'Recovery intent lost numeric identity');return {'append_calls':1,'lost_response_recovery':'exact readback accepted','error':e}
                second=rejects(lambda:pub.append_ledger(w.args('ledger')));need(w.appends==1,'Blind retry');return {'append_calls':1,'first_error':e,'recovery_error':second}
            r=pub.append_ledger(w.args('ledger'));need(r['new_row'] and w.appends==1,'Append failed');return r
    for mode in ['lost','prior_row_drift','duplicate']:result('whole_ledger_unknown_'+mode,lambda mode=mode:append_unknown(mode))
    def public_final():
        out=[]
        for field in ['doi_bad','bytes_bad','public_bad']:
            w=fresh_world(field)
            with w.installed():w.through_merge();w.stage_publish();setattr(w,field,True);e=rejects(lambda:pub.append_ledger(w.args('ledger')))
            need(w.appends==0,'Final public fault appended');out.append({'field':field,'append_calls':0,'error':e})
        return out
    result('whole_public_DOI_bytes_metadata_faults_block_ledger',public_final)
    def account_controls():
        out=[]
        for label in ['positive197','duplicate','changed_second_pass','new_target_lead','schema_column5']:
            w=fresh_world(label)
            if label=='duplicate':w.accounts[26]=copy.deepcopy(w.accounts[0])
            if label=='new_target_lead':w.accounts[0]['metadata']['description']='This solves Problem30005455'
            if label=='schema_column5':w.rows[2].extend(['']*(5-len(w.rows[2])))
            if label=='changed_second_pass':
                readcount=[0]
                def fault(rs,p):
                    if p==1:readcount[0]+=1
                    if readcount[0]>1:rs[0]['metadata']['description']+=' changed'
                    return rs
                w.account_fault=fault
            with w.installed():
                if label=='positive197':g,records,rows=live.collect('before_integration',c.ORIGINAL,cleared=c.clearance(w.clearance_sha,EXPECTED));need(g['account_total']==197 and [p['count'] for p in g['account_pages_a']]==[25]*7+[22,0],'197 account pagination failure');detail={'account_total':197,'pages_a':[p['count'] for p in g['account_pages_a']],'ledger_rows':len(rows),'leads':[e['id'] for e in g['account_leads']]}
                else:detail=rejects(lambda:live.collect('before_integration',c.ORIGINAL,cleared=c.clearance(w.clearance_sha,EXPECTED)))
            out.append({'case':label,'detail':detail})
        return out
    result('actual197_account_pagination_fullGWS_fourcolumn_and_mutations',account_controls)
    def resolver_extra():
        values=['https://doi.org:444/abc','DOI:https://doi.org@unrelated.invalid/abc','https://doi.org/%2561bc','https://shortdoi.org/10.5281/zenodo.777','https://doi.org./10.5281/zenodo.777','ftp://doi.org/10.5281/zenodo.777','https://www.www.doi.org/10.5281/zenodo.777']
        return [{'value':v,'rejection':rejects(lambda v=v:live.identities(v))} for v in values]
    result('new_official_resolver_alias_faults',resolver_extra)
    def raw_schemas():
        ref=ops/'private/repair_native_reference';reference=json.loads((ops/'NATIVE_SCHEMA_REFERENCE.json').read_bytes());out=[]
        for n,p in reference['captures'].items():b=(ref/n).read_bytes();need(len(b)==p['bytes'] and sha(b)==p['sha256'],'Raw fixture pin mismatch')
        # The unrelated draft's explicit copyright must stop under this policy,
        # not be silently deleted when adapting it to intended target metadata.
        w=fresh_world('raw_native');w.native.allocated=True
        l,n,f=w.native.records();actual=json.loads((ref/'draft_native_21753316.json').read_bytes());n['metadata']['copyright']=actual['metadata']['copyright']
        e=rejects(lambda:native.validate_target(l,n,f,w.native.metadata,w.native.uploads,777,False,set()))
        return {'all_raw_native_reference_hashes_checked':len(reference['captures']),'actual_draft_copyright_rejected_intentionally':e,'published_shape_used_in_full_mocked_workflow':True}
    result('actual_published_draft_schema_captures_and_intentional_failclosed',raw_schemas)
    def concept_final_gate():
        w=fresh_world('conceptdoi_final')
        with w.installed():w.through_merge();pub.lifecycle(w.args('stage'))
        calls=[0]
        def late(*a,**k):
            if a[0]=='before_publish':
                calls[0]+=1
                if calls[0]==2:w.native.fault=lambda l,n,f:l.__setitem__('conceptdoi','10.5281/zenodo.999')
        w.gate_hook=late
        with w.installed():e=rejects(lambda:pub.lifecycle(w.args('publish')))
        need(w.native.calls.count('publish')==0 and not (pub.RUNTIME/'ZENODO_PUBLISH_VERIFIED.json').exists(),'Final legacy concept DOI drift reached POST')
        return {'finding':'F4_repaired','final_full_publish_gates':calls[0],'POSTs':0,'publication_verified_receipt':False,'error':e}
    result('F4_full_final_gate_legacy_conceptdoi_drift_zero_POST',concept_final_gate)
    def unknown_stage_and_publish():
        out=[]
        for scenario in ['lost_create_success','lost_upload_success','lost_publish_failure']:
            w=fresh_world(scenario)
            with w.installed():w.through_merge()
            if scenario=='lost_create_success':
                orig=w.native.create
                def action(*a):orig(*a);raise c.zenodo.DepositError('Lost create response')
                w.native.create=action;requested='stage'
            elif scenario=='lost_upload_success':
                orig=w.native.upload
                def action(*a):orig(*a);raise c.zenodo.DepositError('Lost upload response')
                w.native.upload=action;requested='stage'
            else:
                with w.installed():pub.lifecycle(w.args('stage'))
                def action(*a):w.native.calls.append('publish');raise c.zenodo.DepositError('Lost POST; server stayed draft')
                w.native.publish=action;requested='publish'
            with w.installed():
                first=rejects(lambda:pub.lifecycle(w.args(requested)));calls=list(w.native.calls);second=rejects(lambda:pub.lifecycle(w.args(requested)))
            need(w.native.calls==calls,'Unknown outcome repeated a provider write');out.append({'case':scenario,'calls':calls,'first_error':first,'second_error':second,'intent_retained':(pub.RUNTIME/('ZENODO_'+requested.upper()+'_INTENT.json')).exists()})
        return out
    result('whole_unknown_create_partialstage_failedPOST_no_blind_retry',unknown_stage_and_publish)
    def git_unknown_and_conflict():
        out=[]
        for scenario in ['selected_conflict','main_advance_before_ref','lost_ref_response','lost_merge_response']:
            w=fresh_world(scenario)
            if scenario=='selected_conflict':
                old=w.git.flatten(w.git.commits[w.git.main]['tree']['sha']);old[c.PROBLEM+'/PROOF.md']=b'concurrent different proof';w.git.save_commit(w.git.main,old,[w.git.parent])
                with w.installed():e=rejects(w.integrate)
                need(not w.git.writes,'Conflict wrote objects');out.append({'case':scenario,'writes':0,'error':e});continue
            if scenario=='main_advance_before_ref':
                def hook(endpoint):
                    if endpoint=='git/ref/heads/main' and any(v['endpoint']=='git/commits' for v in w.git.writes):
                        new='7'*40;flat=w.git.flatten(w.git.commits[w.git.main]['tree']['sha']);flat['LATER.md']=b'later';w.git.save_commit(new,flat,[w.git.main]);w.git.main=new
                w.get_hook=hook
                with w.installed():e=rejects(w.integrate)
                refs=[v for v in w.git.writes if v['endpoint'].startswith('git/refs/')];need(not refs,'Ref wrote after main drift');out.append({'case':scenario,'ref_writes':0,'error':e});continue
            original=w.git.write
            def fault(endpoint,method,body):
                response=original(endpoint,method,body)
                if endpoint==('pulls/1131/merge' if scenario=='lost_merge_response' else 'git/refs/heads/'+c.BRANCH):raise RuntimeError('Simulated write success with lost response')
                return response
            w.git.write=fault
            with w.installed():
                if scenario=='lost_merge_response':
                    w.integrate();ir.describe(w.args('pr-description'));ir.mark_ready(w.args('ready'));e=rejects(lambda:ir.merge(w.args('merge')));before=len(w.git.writes);second=rejects(lambda:ir.merge(w.args('merge')))
                else:e=rejects(w.integrate);before=len(w.git.writes);second=rejects(w.integrate)
                publication_error=rejects(lambda:pub.lifecycle(w.args('stage')))
            need(len(w.git.writes)==before and not w.native.calls,'Unknown Git response retried/publication followed');out.append({'case':scenario,'writes_after_retry':0,'publication_calls':0,'error':e,'second_error':second,'publication_error':publication_error})
        return out
    result('whole_git_selected_conflict_main_drift_unknown_ref_merge',git_unknown_and_conflict)
    def nested_aliases():
        out=[]
        values=['https://unrelated.invalid/?related=//shortdoi.org/abc','https://unrelated.invalid/?related=%252f%252fshortdoi.org%252fabc','https://unrelated.invalid/#//doi.org/abc','https://unrelated.invalid/?r=//doi.org/abc','10/abc','10/abc!','10/abc|','10/abc—','<p>10/abc!</p>','"10/abc"','%252210%252fabc%2522','OWR 10/2019 pp. 111-112 DOI 10.4171/OWR/2019/10; 10/abc']
        for position in ['ledger','account','account_key','local_state_key']:
            for value in values:
                w=fresh_world('nested_alias_'+position)
                if position=='ledger':w.rows.append(['Ordinary unrelated result','',value,''])
                elif position=='account':w.accounts[0]['metadata']['description']=value
                elif position=='account_key':w.accounts[0]['metadata'][value]='ordinary'
                else:
                    state_repo=c.PRIVATE/'state_repo';directory=state_repo/'.zenodo-state';directory.mkdir(parents=True);dump(directory/'alias_key.json',{'id':999001,value:'ordinary'})
                with w.installed(),patch(*([(live,'REPO',state_repo)] if position=='local_state_key' else [])):e=rejects(lambda:live.collect('before_integration',c.ORIGINAL,cleared=c.clearance(w.clearance_sha,EXPECTED)))
                need(not w.appends and not w.native.calls,'Alias fault caused writes')
                out.append({'position':position,'value':value,'absence_gate_rejected':True,'error':e})
        return out
    result('F2_nested_and_terminal_aliases_full197_account_ledger_gate',nested_aliases)
    def ledger_tab_and_response():
        out=[]
        faults={
            'wrong_top_workbook':lambda r:r.__setitem__('spreadsheetId','OTHER_WORKBOOK'),
            'wrong_nested_workbook':lambda r:r['updatedSpreadsheet'].__setitem__('spreadsheetId','OTHER_WORKBOOK'),
            'wrong_nested_gid':lambda r:r['updatedSpreadsheet']['sheets'][0]['properties'].__setitem__('sheetId',999999999),
            'wrong_replies_count':lambda r:r.__setitem__('replies',[{},{}]),
            'renamed_same_numeric_tab_after_append':lambda r:r['updatedSpreadsheet']['sheets'][0]['properties'].__setitem__('title','Concurrent renamed tab'),
            'unexpected_values_append_shape':lambda r:r.__setitem__('updates',{'updatedRows':1,'updatedColumns':4,'updatedCells':4,'updatedData':{'values':[['bogus']]}}),
        }
        for case in ['replaced_title_gid','replaced_after_last_gate',*faults]:
            w=fresh_world(case)
            with w.installed():w.through_merge();w.stage_publish()
            if case=='replaced_title_gid':w.tab_gid=999999999
            elif case=='replaced_after_last_gate':w.replace_before_append=True
            else:w.response_fault=faults[case]
            with w.installed():e=rejects(lambda:pub.append_ledger(w.args('ledger')))
            need(w.appends==(0 if case in {'replaced_title_gid','replaced_after_last_gate'} else 1),'Wrong append count')
            need(not (pub.RUNTIME/'LEDGER_VERIFIED.json').exists(),'Malformed ledger response falsely verified')
            if case!='replaced_title_gid':
                intent=json.loads((pub.RUNTIME/'LEDGER_APPEND_INTENT.json').read_bytes());need(intent['sheet_id']==1254632077 and intent['spreadsheet_id']==c.SHEET,'Stable-ID intent absent')
            out.append({'case':case,'verified':False,'appends':w.appends,'error':e})
        return out
    result('F3_D1_full_numeric_ledger_identity_response_faults',ledger_tab_and_response)
    def numeric_readback_faults():
        faults={
            'workbook':lambda r:r.__setitem__('spreadsheetId','OTHER'),
            'gid':lambda r:r['valueRanges'][0]['dataFilters'][0]['gridRange'].__setitem__('sheetId',999999999),
            'dimension':lambda r:r['valueRanges'][0]['valueRange'].__setitem__('majorDimension','COLUMNS'),
            'range':lambda r:r['valueRanges'][0]['valueRange'].__setitem__('range',"'Wrong tab'!Z9:AC9"),
            'extra_match':lambda r:r['valueRanges'].append(copy.deepcopy(r['valueRanges'][0])),
            'missing_blank_B':lambda r:r['valueRanges'][0]['valueRange']['values'][-1].pop(1),
            'extra_column':lambda r:r['valueRanges'][0]['valueRange']['values'][-1].append('UNREVIEWED'),
        };out=[]
        for label,fault in faults.items():
            w=fresh_world('readback_'+label)
            with w.installed():w.through_merge();w.stage_publish()
            def response_hook(r):w.read_fault=fault
            w.response_fault=response_hook
            with w.installed():e=rejects(lambda:pub.append_ledger(w.args('ledger')))
            need(w.appends==1 and not (pub.RUNTIME/'LEDGER_VERIFIED.json').exists(),'Bad numeric readback accepted')
            out.append({'field':label,'appends':1,'verified':False,'error':e})
        return out
    result('D1_numeric_readback_gid_ROWS_range_count_echo_faults',numeric_readback_faults)
    def formula_ambiguity():
        w=fresh_world('formula_ambiguity')
        with w.installed():w.through_merge();w.stage_publish()
        w.response_fault=lambda r:setattr(w,'formula_fault',True)
        with w.installed():e=rejects(lambda:pub.append_ledger(w.args('ledger')))
        need(w.appends==1 and not (pub.RUNTIME/'LEDGER_VERIFIED.json').exists(),'Formula ambiguity verified')
        return {'appends':1,'verified':False,'error':e}
    result('D1_numeric_formula_unformatted_literal_crosscheck',formula_ambiguity)
    def alias_boundaries():
        bad=['https://ordinary.invalid/?r=custom:doi.org/10.5281/zenodo.777','https://ordinary.invalid/#ftp://doi.org/10.5281/zenodo.777','10/abc','10%2fabc','"10/abc"',"'10/abc'",'OWR 10/2019 pp. 111-112 x10.4171/OWR/2019/10','OWR 10/2019 pp. 111-112 10.4171/OWR/2019/100','OWR 10/2019 pp. 111-112 10.4171/OWR/2019/10/extra','OWR 10/2019 pp. 111-112 10.4171/OWR/2019/10.extra','OWR 10/2019 pp. 111-112 10.4171/OWR/2019/10; 10/abc']
        bad.append('https://ordinary.invalid/?'+('&r=//unrelated.invalid/'*600))
        for v in bad:rejects(lambda v=v:live.identities(v))
        good=['https://ordinary.invalid/10/2019/06','https://ordinary.invalid/10/21tkt-1.pdf','https://ordinary.invalid/path/doi.org/abc','https://ordinary.invalid/path//doi.org/abc','https://ordinary.invalid/path/shortdoi.org/abc','https://ordinary.invalid/path;doi.org/abc','https://ordinary.invalid/path:shortdoi.org/abc','OWR 10/2019 pp. 111-112 10.4171/OWR/2019/10','OWR 10/2019 pp. 111-112 https://doi.org/10.4171/OWR/2019/10']
        for v in good:need(live.identities(v)==set(),'Ordinary path or exact source bibliography falsely flagged')
        family=0
        for host in ['doi.org','www.doi.org','dx.doi.org','shortdoi.org','www.shortdoi.org','dx.shortdoi.org']:
            for suffix in ['', '.', '%2e']:
                for prefix in ['//','https://','ftp://','custom:','']:
                    for context in ['https://unrelated.invalid/?r=','https://unrelated.invalid/#']:
                        v=context+prefix+host+suffix+'/abc';rejects(lambda v=v:live.identities(v));family+=1
        return {'terminal_and_mixed_bibliography_rejections':len(bad),'ordinary_path_and_exact_bibliography_controls':len(good),'nested_resolver_family_rejections':family,'original_string_boundaries_scanned':True}
    result('F2_terminal_boundaries_mixed_bibliography_unrelated_paths',alias_boundaries)
    def encoded_semantic_collectors():
        targets=['https://github.com/AlecKriebel/Math/pull/%31%31%33%31','%33%30%30%30%35%34%35%35','OWR-%31%32%36%39%37%37%30%38-008','&#51;&#48;&#48;&#48;&#53;&#52;&#53;&#53;','https://github.com/AlecKriebel/Math/pull/&#49;&#49;&#51;&#49;']
        out=[]
        for value in targets:
            for column in range(4):
                w=fresh_world('semantic_ledger');row=['','','',''];row[column]=value;w.rows.append(row)
                with w.installed():e=rejects(lambda:live.collect('before_integration',c.ORIGINAL,cleared=c.clearance(w.clearance_sha,EXPECTED)))
                need('ledger lead' in e['message'],'Encoded ledger semantic control failed for another reason')
                out.append({'where':'ledger','column':column+1,'value':value,'gate_rejected':True})
            for field in ['value','key']:
                w=fresh_world('semantic_account_'+field);record=next(r for r in w.accounts if r['id']!=23408971 and not any(live.semantic(t) for t in live.strings(live.projection(r))))
                if field=='value':record['metadata']['description']=value
                else:record['metadata'][value]='ordinary unrelated description'
                with w.installed():e=rejects(lambda:live.collect('before_integration',c.ORIGINAL,cleared=c.clearance(w.clearance_sha,EXPECTED)))
                need('account lead' in e['message'],'Encoded account semantic control failed for another reason')
                out.append({'where':'account_'+field,'value':value,'gate_rejected':True})
            for field in ['value','key']:
                w=fresh_world('semantic_state_'+field);state_repo=c.PRIVATE/'state_repo';directory=state_repo/'.zenodo-state';directory.mkdir(parents=True)
                value_object={'id':999001,'description':value} if field=='value' else {'id':999001,value:'ordinary'}
                dump(directory/'encoded.json',value_object)
                with w.installed(),patch((live,'REPO',state_repo)):
                    e=rejects(lambda:live.collect('before_integration',c.ORIGINAL,cleared=c.clearance(w.clearance_sha,EXPECTED)))
                need('local deposit state' in e['message'],'Encoded local-state semantic control failed for another reason')
                out.append({'where':'local_state_'+field,'value':value,'gate_rejected':True})
        return {'controls':out,'complete197_account_and181_ledger_fixtures':True,'real_mutations':0}
    result('F2_decoded_PR_problem_source_every_column_account_keys_localstate',encoded_semantic_collectors)
    def unicode_source_context():
        prefixes=['α','é','９','x\u0301','α‿','α\u200e','&#945;','&alpha;','%CE%B1','%26%23945%3B']
        out=[]
        for prefix in prefixes:
            source=prefix+'10.4171/OWR/2025/10';citation='OWR 10/2025 pp. 111-112'
            for where in ['ledger','account_reference','account_key']:
                w=fresh_world('unicode_source_'+where)
                if where=='ledger':w.rows.append([citation,'',source,''])
                else:
                    record=next(r for r in w.accounts if r['id']!=23408971 and not any(live.semantic(t) for t in live.strings(live.projection(r))) and '2025' not in live.bibliography_years(live.strings(live.projection(r))))
                    record['metadata']['references']=[citation,source] if where=='account_reference' else [citation]
                    if where=='account_key':record['metadata'][source]='ordinary'
                with w.installed():e=rejects(lambda:live.collect('before_integration',c.ORIGINAL,cleared=c.clearance(w.clearance_sha,EXPECTED)))
                need('Bare short DOI' in e['message'],'Unicode source-boundary control failed for another reason')
                out.append({'where':where,'prefix':prefix,'gate_rejected':True})
        for source in ['10.4171/OWR/2025/10','https://doi.org/10.4171/OWR/2025/10','&#49;&#48;.4171/OWR/2025/10']:
            need(live.row_ids(['OWR 10/2025 pp. 111-112','',source,''])==set(),'Properly bounded bibliography failed')
            rejects(lambda source=source:live.row_ids(['OWR 10/2025 pp. 111-112','',source,'10/abc']))
        return {'controls':out,'proper_source_positive_controls':3,'mixed_terminal_alias_rejected':3}
    result('F2_Unicode_HTML_percent_source_DOI_boundaries_full_collectors',unicode_source_context)
    def loader_interactions():
        # A failed storage optimization must preserve the already durable
        # generated capture. Faults never touch original/copied input files.
        directory=c.PRIVATE/'dedup_preservation';directory.mkdir()
        payload={'preservation_control':uuid.uuid4().hex};canonical=directory/'canonical.json'
        compact_durable(canonical,payload);expected=canonical.read_bytes()
        def storage_failure(*a,**k):raise OSError(28,'Offline injected allocation failure')
        for function in ['link','replace']:
            target=directory/(function+'_failure.json')
            with patch((os,function,storage_failure)):
                e=rejects(lambda:compact_durable(target,payload))
            need(e['type']=='OSError' and target.read_bytes()==expected and canonical.read_bytes()==expected,'Generated capture lost after dedup allocation failure')
            need(not list(directory.glob(target.name+'.dedup_*')),'Failed optimization left a temporary link')
        loader,ctx=bootstrap['load_verified'](ops,EXPECTED,BOOT);marker=ops/'private/UNTRUSTED_EXECUTED';originals={}
        poison=types.ModuleType('ops_common');poison.POISON=True
        for name in ['ops_common.py']:
            path=ops/name;originals[path]=path.read_bytes();path.write_bytes(originals[path]+b'\nraise RuntimeError("Unverified changed on-disk source ran")\n')
        dep=mirror/'zenodo_deposit_tool/zenodo.py';originals[dep]=dep.read_bytes();dep.write_bytes(originals[dep]+b'\nraise RuntimeError("Changed dependency ran")\n')
        try:
            with patch((sys,'modules',{**sys.modules,'ops_common':poison,'zenodo':poison})):
                mod=loader('publish_and_ledger');need(hasattr(mod,'GuardedClient'),'Verified loader selected poisoned module')
        finally:
            for path,body in originals.items():path.write_bytes(body)
        freshload,_=bootstrap['load_verified'](ops,EXPECTED,BOOT);freshload('ops_common').package()
        return {'checked_buffers_survive_disk_change_after_verification':True,'project_sys_modules_poison_ignored':True,'shared_dependency_checked_buffer_used':True,'complete_package_pass_after_restore':True,'inputs_restored':True,'generated_capture_preserved_on_link_and_replace_allocation_failures':True}
    result('independent_source_loader_postverification_buffers_and_sysmodules',loader_interactions)
    def offline_existing():
        off=load('offline_controls');path=off.PRIVATE/'REPLAY_ORIGINAL_CONTROLS.json';sys.argv=['offline_controls','--output',str(path)]
        with contextlib.redirect_stdout(io.StringIO()):r=off.main()
        v=json.loads(path.read_bytes());need(r==0 and not v['network_attempts'] and len(v['controls'])==21,'Existing repaired controls failed')
        return {'groups':21,'all_pass':all(v['status']=='PASS' for v in v['controls']),'network_attempts':0,'note':'additional corroboration, not independent design'}
    result('copied_sealed_repair_controls_crosscheck',offline_existing)
    # Source/data bytes in the base private mirror must remain exact; generated
    # captures and nested controls are confined to excluded private/runtime areas.
    receipt=json.loads((mirror.parent/'COPY_RECEIPT.json').read_bytes());changed=[]
    for n,p in receipt['files'].items():
        b=(mirror/n).read_bytes()
        if {'bytes':len(b),'sha256':sha(b)}!=p:changed.append(n)
    need(not changed,'Copied original bytes changed')
    output={'mode':sys.flags.optimize,'isolated':bool(sys.flags.isolated),'no_site':bool(sys.flags.no_site),'target_operations_sha256':EXPECTED,'bootstrap_sha256':BOOT,'controls':RESULTS,'failures':[r for r in RESULTS if r['status']!='PASS'],'blocked_external_attempts':ATTEMPTS,'actual_external_mutations':0,'copied_inputs_unchanged':True,'publication_ready':False,'findings_require_parent_adjudication':True}
    dump(args.output,output);print(json.dumps({'mode':sys.flags.optimize,'groups':len(RESULTS),'failures':output['failures'],'blocked_external_attempts':ATTEMPTS,'external_mutations':0}))
    return int(bool(output['failures'] or ATTEMPTS))
def main():
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);a=p.parse_args();return run(a)
if __name__=='__main__':raise SystemExit(main())
