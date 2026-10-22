#!/usr/bin/env python3
"""Independent operations02 controls. Run only under -I -S in a new private mirror.
All real networking, token loading and process creation are disabled before source
bootstrap/module loading. The service models perform only in-memory events.
"""
import argparse,base64,contextlib,copy,datetime,hashlib,http.client,importlib.util,io,json,marshal,os,socket,ssl,struct,subprocess,sys,types,urllib.request,uuid
from pathlib import Path
from urllib.parse import parse_qs,urlsplit
HERE=Path(__file__).resolve().parent
EXPECTED='da72b199f9b4eec35eef87b18eccecacb55c3ae7f32b3f9d44a2f961d2832168'
BOOT='b42765748e6e73518ef21195bbc475f70f7b76215665bf60071bdaa35fcc857f'
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
    b=(ops/'bootstrap.py').read_bytes();need(sha(b)==BOOT,'External bootstrap changed before exec')
    ns={'__file__':str(ops/'bootstrap.py'),'__name__':'review_checked_bootstrap'}
    exec(compile(b,str(ops/'bootstrap.py'),'exec'),ns)
    load,ctx=ns['load_verified'](ops,EXPECTED,BOOT)
    modules={n:load(n) for n in ['ops_common','collect_live','integrate_remote','native_policy','publish_and_ledger','check_package']}
    z=modules['ops_common'].zenodo
    z.token_for=lambda *a,**k:'OFFLINE_SENTINEL_NO_CREDENTIAL'
    z.doi_status=lambda doi:{'status':'offline_mock','url':'https://doi.org/'+doi}
    return ops,modules,load,ns

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
        need(len(self.accounts)==197,'Not actual197 fixture');self.events=[];self.appends=0;self.append_mode=None;self.gate_hook=None;self.get_hook=None;self.doi_bad=False;self.bytes_bad=False;self.public_bad=False;self.account_fault=None;self.response_fault=None;self.tab_gid=1254632077
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
    def command(self,argv,body=None):
        if argv[0]=='gws':
            if 'get' in argv:
                v=copy.deepcopy(self.sheet);v['values']=copy.deepcopy(self.rows);return v
            need('append' in argv,'Unexpected GWS path');params=json.loads(argv[argv.index('--params')+1]);payload=json.loads(argv[argv.index('--json')+1]);row=payload['values'][0]
            need(params=={'spreadsheetId':self.c.SHEET,'range':"'Math Puzzles'!A:D",'valueInputOption':'RAW','insertDataOption':'INSERT_ROWS','includeValuesInResponse':True},'Append params differ');self.appends+=1;self.rows.append(copy.deepcopy(row));n=len(self.rows)
            if self.append_mode=='lost':raise RuntimeError('Lost append success response')
            if self.append_mode=='prior_row_drift':self.rows[1][0]+=' changed'
            if self.append_mode=='duplicate':self.rows.append(copy.deepcopy(row))
            response={'spreadsheetId':self.c.SHEET,'updates':{'spreadsheetId':self.c.SHEET,'updatedRows':1,'updatedColumns':4,'updatedCells':4,'updatedRange':f"'Math Puzzles'!A{n}:D{n}",'updatedData':{'majorDimension':'ROWS','range':f"'Math Puzzles'!A{n}:D{n}",'values':[row]}}}
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
    mirror=args.mirror.resolve();ops,m,load,bootstrap=load_bundle(mirror);c=m['ops_common'];ir=m['integrate_remote'];pub=m['publish_and_ledger'];live=m['collect_live'];native=m['native_policy']
    # Deduplicate byte-identical generated capture files after the real exclusive
    # durable writer/fsync finishes. This conserves local disk without changing
    # file bytes, validation or operation ordering. Originals are never linked.
    dedup={};actual_durable=c.durable
    def compact_durable(path,value):
        actual_durable(path,value)
        body=path.read_bytes();key=sha(body)
        if key in dedup and dedup[key].exists():
            path.unlink();os.link(dedup[key],path)
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
        writes=[v for v in w.git.writes if v['endpoint']=='pulls/1131'];need(len(writes)==1 and w.git.pr['body']!=orig,'Counterexample not reproduced');need(not (ir.RUNTIME/'PR_DESCRIPTION_VERIFIED.json').exists(),'Unexpected success')
        return {'finding':'F1_description_title_gate_race','body_PATCH_count':1,'unreviewed_title_preserved':w.git.pr['title'],'error':error,'verified_receipt':False,'subsequent_actions_executed':0}
    result('counterexample_description_title_changed_during_gate_still_PATCHes',describe_title)
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
                    r=pub.append_ledger(w.args('ledger'));need(r['new_row'] is False and w.appends==1,'Recovery appended twice');return {'append_calls':1,'lost_response_recovery':'exact readback accepted','error':e}
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
        with w.installed():r=pub.lifecycle(w.args('publish'))
        need(w.native.calls.count('publish')==1 and (pub.RUNTIME/'ZENODO_PUBLISH_VERIFIED.json').exists(),'Final conceptdoi gap not reproduced')
        with w.installed():e=rejects(lambda:pub.append_ledger(w.args('ledger')))
        return {'finding':'F4_legacy_conceptDOI_inconsistency_accepted_before_POST','final_full_publish_gates':calls[0],'POSTs':1,'publication_verified_receipt':True,'legacy_conceptdoi':'10.5281/zenodo.999','native_concept_id':778,'ledger_appends':w.appends,'later_ledger_error':e,'limit':'Native record/DOI/parent remain correct; contradictory legacy concept field is the demonstrated scope.'}
    result('counterexample_full_final_gate_legacy_conceptdoi_drift',concept_final_gate)
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
        values=['https://unrelated.invalid/?related=//shortdoi.org/abc','https://unrelated.invalid/?related=%252f%252fshortdoi.org%252fabc','https://unrelated.invalid/#//doi.org/abc','https://unrelated.invalid/?r=//doi.org/abc']
        for value in values:
            w=fresh_world('nested_alias');w.rows.append(['Ordinary unrelated result','',value,''])
            with w.installed():
                gate,records,rows=live.collect('before_integration',c.ORIGINAL,cleared=c.clearance(w.clearance_sha,EXPECTED))
            need(gate['ledger_leads']==[],'Counterexample changed behavior')
            out.append({'value':value,'full_gate_accepted_absence':True,'ledger_leads':[],'account_total':gate['account_total']})
        return {'finding':'F2_embedded_resolver_reference_not_reviewed','controls':out,'limit':'No claim that unrelated URL itself resolves as DOI; the explicit embedded separate reference is unresolved.'}
    result('counterexample_nested_protocol_relative_resolver_full_gate',nested_aliases)
    def ledger_tab_and_response():
        out=[]
        for case in ['replaced_title_gid','wrong_response_ids_and_range']:
            w=fresh_world(case)
            if case=='replaced_title_gid':w.tab_gid=999999999
            else:
                def malformed(r):
                    r['spreadsheetId']='OTHER_WORKBOOK';r['updates']['spreadsheetId']='OTHER_WORKBOOK';r['updates']['updatedData']['majorDimension']='COLUMNS';r['updates']['updatedData']['range']="'Wrong tab'!Z9:AC9"
                w.response_fault=malformed
            with w.installed():w.through_merge();w.stage_publish();v=pub.append_ledger(w.args('ledger'))
            need(v['verified'] and w.appends==1,'Control did not reach verified append')
            out.append({'case':case,'verified':True,'appends':1,'actual_mock_tab_gid':w.tab_gid,'intended_gid':1254632077,'readback_exact':True})
        return {'finding':'F3_unbound_stable_ledger_tab_identity','controls':out,'response_only_case_is_evidence_incompleteness_not_demonstrated_wrong_destination':True}
    result('counterexample_full_ledger_tab_gid_and_response_identity',ledger_tab_and_response)
    def loader_interactions():
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
        return {'checked_buffers_survive_disk_change_after_verification':True,'project_sys_modules_poison_ignored':True,'shared_dependency_checked_buffer_used':True,'complete_package_pass_after_restore':True,'inputs_restored':True}
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
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--mirror',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args();raise SystemExit(run(a))
