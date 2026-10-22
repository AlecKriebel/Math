"""Complete real read adapters and the sole one-attempt append delegate. Import inert."""
from pathlib import Path
import os,stat,time,datetime,json,base64,gzip,hashlib,http.client,urllib.parse,urllib.request,urllib.error,subprocess,types,threading,concurrent.futures
from ops_core import require,sha,strict_json,canonical,typed_equal
from authority import no_symlinks,Authority

class Capture:
    def __init__(self,path):
        self.path=no_symlinks(path);self.path.mkdir(parents=True,exist_ok=False);self.n=0;self.lock=threading.RLock()
    def save(self,label,value):
        with self.lock:
            p=self.path/(str(self.n).zfill(5)+'_'+label+'.json.gz');self.n+=1;b=canonical(value);z=gzip.compress(b,mtime=0)
            with p.open('xb')as f:os.fchmod(f.fileno(),0o600);f.write(z);f.flush();os.fsync(f.fileno())
            fd=os.open(self.path,os.O_RDONLY)
            try:os.fsync(fd)
            finally:os.close(fd)
            return {'path':str(p),'sha256':sha(b),'bytes':len(b)}
def raw_transport(stdout=b'',stderr=b'',returncode=None,error=None):
    return {'returncode':returncode,'stdout_base64':base64.b64encode(stdout).decode(),'stderr_base64':base64.b64encode(stderr).decode(),'transport_error':error}

class RealProvider:
    def __init__(self,config,gate,capture,verify,authority=None):
        self.config=config;self.config_bytes=canonical(config);self.gate=gate;self.capture=capture;self.verify=verify;self.authority=authority;self.client=None;self.append_attempts=0;self.bound_case_path=Path(config['case']);self.direct_guard=None
    def now(self):return time.monotonic()
    def stamp(self):return datetime.datetime.now(datetime.timezone.utc).isoformat()
    def binary(self,name):
        pin=self.config['programs'][name];p=no_symlinks(pin['path']);b=p.read_bytes();require(len(b)==pin['bytes']and sha(b)==pin['sha256'],'Exact external CLI executable changed');return str(p)
    def run_read(self,name,args,label):
        command=[self.binary(name),*args];r=subprocess.run(command,capture_output=True,timeout=90)
        self.capture.save(label,{'args':args,**raw_transport(r.stdout,r.stderr,r.returncode)});require(r.returncode==0,'Read-only CLI failed');return r.stdout
    def gws(self,parts,params,body=None):
        require(parts in [['get'],['values','batchGetByDataFilter']],'Numeric observer is read-only')
        args=['sheets','spreadsheets',*parts,'--params',json.dumps(params)]
        if body is not None:args+=['--json',json.dumps(body,ensure_ascii=False)]
        return strict_json(self.run_read('gws',args,'numeric_raw'))
    def owned_page(self,page):
        require(type(page)is int and 1<=page<=10000,'Owned page bound')
        if self.client is None:
            p=no_symlinks(self.config['account_tool']['path']);b=p.read_bytes();require(sha(b)==self.config['account_tool']['sha256'],'Account read-client source drift')
            m=types.ModuleType('_verified_owned_get_client');m.__file__=str(p);exec(compile(b,str(p),'exec',optimize=0),m.__dict__);self.client=(m.token_for('production'),m.USER_AGENT)
        con=http.client.HTTPSConnection('zenodo.org',timeout=60)
        try:
            con.request('GET','/api/deposit/depositions?'+urllib.parse.urlencode({'page':page,'size':25,'sort':'mostrecent'}),headers={'Authorization':'Bearer '+self.client[0],'User-Agent':self.client[1],'Accept':'application/json'})
            r=con.getresponse();b=r.read(16*1024*1024+1);self.capture.save('owned_raw',{'page':page,'status':r.status,'body_base64':base64.b64encode(b).decode()});require(type(r.status)is int and r.status==200 and len(b)<=16*1024*1024,'Owned GET failed or exceeded bound');return b
        finally:con.close()
    def complete_owned_and_local(self):
        passes=[]
        for unused in range(2):
            records={};raw_pages=[]
            for page in range(1,10001):
                raw=self.owned_page(page);values=strict_json(raw);require(type(values)is list and len(values)<=25,'Owned raw full page type/count');raw_pages.append(raw.decode('utf-8'))
                for v in values:
                    require(type(v)is dict and type(v.get('id'))is int and v['id']>0 and type(v.get('metadata'))is dict and type(v.get('files'))is list,'Full typed owned record')
                    k=str(v['id']);require(k not in records,'Repeated owned ID across pages');records[k]=v
                if not values:break
            else:raise RuntimeError('Missing empty terminal page')
            require(records,'Empty owned account requires separate review');passes.append({'records':records,'raw_pages':raw_pages,'http_statuses':[200]*len(raw_pages),'terminal_empty_page':len(raw_pages)})
        require(typed_equal(passes[0]['records'],passes[1]['records']),'Complete owned passes drift')
        directory=no_symlinks(Path(self.config['local_root'])/'.zenodo-state');require(directory.is_dir(),'Local state directory missing');namespace=sorted(p.name for p in directory.glob('*.json'));local=[]
        for name in namespace:
            p=no_symlinks(directory/name);b=p.read_bytes();v=strict_json(b);manifest=None
            for key in ['manifest','manifest_path']:
                if type(v.get(key))is str:
                    q=Path(v[key]);q=q if q.is_absolute()else Path(self.config['local_root'])/q;q=no_symlinks(q)
                    require(q.is_file(),'Referenced local scientific manifest missing');mb=q.read_bytes();manifest={'path':str(q),'sha256':sha(mb),'value':strict_json(mb)};break
            local.append({'state':{'path':str(p),'sha256':sha(b),'value':v},'scientific_manifest':manifest})
        require(namespace==sorted(p.name for p in directory.glob('*.json')),'Local namespace changed while reading')
        for x in local:
            require(sha(no_symlinks(x['state']['path']).read_bytes())==x['state']['sha256'],'Local state changed while collecting')
            if x['scientific_manifest']:require(sha(no_symlinks(x['scientific_manifest']['path']).read_bytes())==x['scientific_manifest']['sha256'],'Local scientific manifest changed while collecting')
        return {'passes':passes,'local':local}
    def public_one(self,r):
        if r['role']=='pr':
            n=r['pr'];require(type(n)is int and n>0,'Exact PR number');b=self.run_read('gh',['api','repos/AlecKriebel/Math/pulls/'+str(n)],'public_pr_raw');body=strict_json(b);require(type(body.get('number'))is int and body['number']==n,'PR identity');return {'status':200,'final_url':r['url'],'bytes':len(b),'sha256':sha(b),'complete':True,'body':body}
        url=r['url'];u=urllib.parse.urlsplit(url);require(u.scheme=='https'and u.hostname and not u.username and not u.password,'Unauthenticated HTTPS source required')
        request=urllib.request.Request(url,headers={'User-Agent':'Math-existing-publication-audit/2.0 (read-only)'})
        try:response=urllib.request.urlopen(request,timeout=45)
        except urllib.error.HTTPError as e:response=e
        with response:
            h=hashlib.sha256();n=0;parts=[]
            while True:
                b=response.read(65536)
                if not b:break
                n+=len(b);require(n<=50*1024*1024,'Complete source exceeds50MiB bound');h.update(b)
                if not r.get('stream_hash_only',False):require(n<=2*1024*1024,'Metadata exceeds2MiB bound');parts.append(b)
            v={'status':response.status,'final_url':response.url,'bytes':n,'sha256':h.hexdigest(),'complete':True}
            if not r.get('stream_hash_only',False):
                raw=b''.join(parts)
                self.capture.save('public_raw',{'key':r['key'],'url':url,**v,'body_base64':base64.b64encode(raw).decode()})
                if r.get('parse')=='json':v['body']=strict_json(raw)
                else:v['body']=raw.decode('utf-8')
            else:self.capture.save('public_complete_stream',{'key':r['key'],'url':url,**v,'payload_retained':False})
            return v
    def complete_publication_source_observations(self):
        self.public_started=self.now();requests=self.gate['public_requests'];out={}
        with concurrent.futures.ThreadPoolExecutor(max_workers=6)as pool:
            futures={pool.submit(self.public_one,r):r for r in requests}
            for f in concurrent.futures.as_completed(futures):out[futures[f]['key']]=f.result()
        require(set(out)=={r['key']for r in requests},'Complete publication roles missing');return {'all_required_roles_observed':True,'responses':out}
    def preserve_observation(self,label,value):self.capture.save(label,value)
    def preserve_failure(self,value):
        original={n:base64.b64encode(b).decode()for n,b in self.journal.expected.items()}if hasattr(self,'journal')else None
        self.capture.save('failure',{'failure':value,'expected_original_journal_buffers':original})
    def check_integrity(self,plan_bytes,source_hash,journal=None):
        self.verify();require(self.authority is not None,'Real authority parser absent');self.authority.check()
        require(canonical(self.config)==self.config_bytes and typed_equal(self.gate,self.authority.gate),'Captured runtime configuration/gate changed')
        require(self.authority.source_sha==source_hash and self.authority.plan_bytes==plan_bytes,'Captured authority context changed')
        if journal is not None:journal.check()
        self.verify()
    def new_journal(self,path,Journal):
        require(isinstance(self.authority,Authority)and Path(path)==self.bound_case_path,'Fixed authorized SAMECASE only');self.authority.check();return Journal(no_symlinks(path))
    def append_once(self,request):
        require(isinstance(self.authority,Authority)and callable(self.direct_guard),'Unarmed append delegate')
        require(self.append_attempts==0,'Never retry an append delegate');self.append_attempts=1
        command=[self.binary('gws'),'sheets','spreadsheets','batchUpdate','--params',json.dumps({'spreadsheetId':self.config['book']}),'--json',json.dumps(request,ensure_ascii=False)]
        self.direct_guard() # Last application guard before the actual process delegate.
        try:
            r=subprocess.run(command,capture_output=True,timeout=120);out=raw_transport(r.stdout,r.stderr,r.returncode)
        except subprocess.TimeoutExpired as e:out=raw_transport(e.stdout or b'',e.stderr or b'',None,'TimeoutExpired')
        except Exception as e:out=raw_transport(error=type(e).__name__)
        # Preserve exact original binary stdout/stderr before any decoding or interpretation.
        self.journal.save('ORIGINAL_APPEND_TRANSPORT.json',out)
        self.capture.save('ORIGINAL_APPEND_TRANSPORT',out)
        return {'returncode':out['returncode'],'stdout':base64.b64decode(out['stdout_base64']).decode('utf-8',errors='strict'),'transport_error':out['transport_error']}
