"""Narrow external adapter: native blob GET404, exact cold capture continuation,
and explicit unattempted-integration phase continuation. No new effect method.
"""
import base64,datetime,gzip,hashlib,io,json,os,re,subprocess
from pathlib import Path

def need(ok,msg):
 if not ok:raise RuntimeError(msg)
def pin(raw):return {'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()}
def stat(path):
 s=path.lstat();need(path.is_file() and not path.is_symlink() and s.st_nlink==1 and s.st_mode&0o777==0o600,'Capture must be original mode600 regular single-link file');return {'device':s.st_dev,'inode':s.st_ino,'mode':s.st_mode&0o777,'mtime_ns':s.st_mtime_ns,'size':s.st_size}
def directory(path):
 need(path.is_absolute() and not any(p.is_symlink() for p in [path,*path.parents]) and path.is_dir(),'Capture directory path changed');s=path.stat();need(s.st_mode&0o777==0o700,'Capture directory mode changed');return {'device':s.st_dev,'inode':s.st_ino,'mode':s.st_mode&0o777}
def capture_namespace(path,strict):
 root=directory(path);groups={};expected={}
 for f in sorted(path.iterdir()):
  if f.name.startswith('UNTRUSTED_OUTCOME_'):
   need(re.fullmatch(r'UNTRUSTED_OUTCOME_[A-Za-z0-9_-]+_[a-f0-9]{32}[.]json',f.name),'Unknown core forensic filename');raw=f.read_bytes();need(len(raw)<=32*1024*1024,'Oversized core forensic body');value=strict(raw);need(type(value) is dict and set(value)=={'at','operationally_verified','reconcile_get_only','value'} and type(value['at']) is str and value['operationally_verified'] is False and value['reconcile_get_only'] is True and type(value['value']) is dict,'Malformed core forensic envelope');at=datetime.datetime.fromisoformat(value['at']);need(at.tzinfo is not None and at.utcoffset()==datetime.timedelta(0),'Malformed core forensic timestamp');expected[f.name]={'pin':pin(raw),'stat':stat(f)};continue
  m=re.fullmatch(r'([0-9]{5})_([A-Za-z0-9_-]+)[.]json[.](gz|receipt[.]json)',f.name);need(m is not None,'Unknown/partial capture namespace; GET-only manual reconciliation required');number=int(m[1]);need(number>0 and m[1]==str(number).zfill(5),'Noncanonical capture ordinal');g=groups.setdefault(number,{});need(m[2] not in g or m[3] not in g[m[2]],'Duplicate capture suffix');g.setdefault(m[2],{})[m[3]]=f
  raw=f.read_bytes();expected[f.name]={'pin':pin(raw),'stat':stat(f)}
 need(sorted(groups)==list(range(1,len(groups)+1)),'Capture sequence has gaps')
 for number,labels in groups.items():
  need(len(labels)==1,'Multiple labels share a capture ordinal');pair=next(iter(labels.values()));need(set(pair)=={'gz','receipt.json'},'Partial capture pair holds');receipt=strict(pair['receipt.json'].read_bytes());need(type(receipt) is dict and set(receipt)=={'raw','compressed','lossless'} and receipt['lossless']=='gzip','Capture receipt schema')
  for value in [receipt['raw'],receipt['compressed']]:need(type(value) is dict and set(value)=={'bytes','sha256'} and type(value['bytes']) is int and 0<=value['bytes']<=32*1024*1024 and type(value['sha256']) is str and re.fullmatch('[a-f0-9]{64}',value['sha256']),'Capture typed pin')
  compressed=pair['gz'].read_bytes();need(pin(compressed)==receipt['compressed'],'Capture compressed bytes changed')
  with gzip.GzipFile(fileobj=io.BytesIO(compressed)) as stream:raw=stream.read(receipt['raw']['bytes']+1)
  need(pin(raw)==receipt['raw'],'Capture complete raw bytes changed')
 return len(groups),expected,root

def parse_blob_response(stdout,returncode,identifier,strict):
 need(type(stdout) is bytes and type(returncode) is int and re.fullmatch('[a-f0-9]{40}',identifier),'Typed native blob transport required');head,separator,body=stdout.partition(b'\r\n\r\n');need(separator and len(head)<=65536,'Missing/oversized native HTTP header block');lines=head.splitlines();need(lines,'No native HTTP status');m=re.fullmatch(rb'HTTP/(?:2[.]0|1[.]1) ([1-5][0-9]{2}) [\x20-\x7e]+',lines[0]);need(m is not None,'Malformed native HTTP status');status=int(m[1]);headers={}
 for line in lines[1:]:
  key,colon,value=line.partition(b':');need(colon and re.fullmatch(rb'[A-Za-z0-9-]+',key) and key.lower() not in headers,'Malformed/duplicate native header');headers[key.lower()]=value.strip()
 need(headers.get(b'content-type') in {b'application/json',b'application/json; charset=utf-8'},'Blob response is not observed JSON media type');value=strict(body)
 if status==404:
  need(returncode==1 and type(value) is dict and set(value)=={'message','documentation_url','status'} and value['message']=='Not Found' and value['documentation_url']=='https://docs.github.com/rest/git/blobs#get-a-blob' and type(value['status']) is str and value['status']=='404','Native404/error JSON disagreement; no absence inference');return None
 need(status==200 and returncode==0,'Blob lookup HTTP/CLI did not prove200 or exact404')
 need(type(value) is dict and set(value)=={'sha','node_id','size','url','content','encoding'} and value['sha']==identifier and type(value['sha']) is str and type(value['node_id']) is str and value['node_id'] and type(value['size']) is int and value['size']>=0 and value['url']=='https://api.github.com/repos/AlecKriebel/Math/git/blobs/'+identifier and value['encoding']=='base64' and type(value['content']) is str and re.fullmatch(r'[A-Za-z0-9+/=\r\n]*',value['content']),'Native200 blob envelope/identity differs')
 encoded=value['content'].replace('\r','').replace('\n','');decoded=base64.b64decode(encoded,validate=True);actual=hashlib.sha1(b'blob '+str(len(decoded)).encode()+b'\0'+decoded).hexdigest();need(len(decoded)==value['size'] and actual==identifier,'Native200 blob bytes/size disagree');return value

def provider_class(core,capture_root):
 """Only these three overrides; every service effect remains core.RealProvider."""
 Base=core.RealProvider
 class RecoveryProvider(Base):
  def __init__(self,capture=None):
   super().__init__(capture_root if capture is None else capture);self._capture_root=self.capture_dir;self.sequence,self._capture_expected,self._capture_directory=capture_namespace(self.capture_dir,core.strict_json)
  def verify_captures(self):
   need(self.capture_dir==self._capture_root and directory(self.capture_dir)==self._capture_directory,'Capture root switched');need({p.name for p in self.capture_dir.iterdir()}==set(self._capture_expected),'Capture namespace changed during action')
   for name,expected in self._capture_expected.items():
    f=self.capture_dir/name;need(stat(f)==expected['stat'] and pin(f.read_bytes())==expected['pin'],'Expected prior capture bytes/metadata changed')
  def capture(self,label,raw):
   self.verify_captures();need(type(label) is str and re.fullmatch('[A-Za-z0-9_-]+',label) and type(raw) is bytes and self.sequence<99999 and len(raw)<=32*1024*1024,'Bounded canonical capture required');prior=dict(self._capture_expected);number=self.sequence+1;expected_compressed=gzip.compress(raw,mtime=0);expected_receipt=core.canonical({'raw':pin(raw),'compressed':pin(expected_compressed),'lossless':'gzip'})+b'\n';super().capture(label,raw)
   names={str(number).zfill(5)+'_'+label+'.json.gz',str(number).zfill(5)+'_'+label+'.json.receipt.json'};need({p.name for p in self.capture_dir.iterdir()}==set(prior)|names,'Concurrent capture namespace holds');receipt_raw=(self.capture_dir/(str(number).zfill(5)+'_'+label+'.json.receipt.json')).read_bytes();compressed=(self.capture_dir/(str(number).zfill(5)+'_'+label+'.json.gz')).read_bytes();need(receipt_raw==expected_receipt and compressed==expected_compressed and gzip.decompress(compressed)==raw,'Own complete capture readback differs');expected_new={str(number).zfill(5)+'_'+label+'.json.gz':expected_compressed,str(number).zfill(5)+'_'+label+'.json.receipt.json':expected_receipt}
   self._capture_expected={**prior,**{name:{'pin':pin(expected_new[name]),'stat':stat(self.capture_dir/name)} for name in names}};self.verify_captures()
  def maybe_blob(self,identifier):
   need(type(identifier) is str and re.fullmatch('[a-f0-9]{40}',identifier),'Bad blob lookup');result=subprocess.run(['gh','api','--hostname','github.com','repos/AlecKriebel/Math/git/blobs/'+identifier,'--include'],cwd=core.REPO,capture_output=True,timeout=60)
   # Both exact native stdout and stderr survive even a rejected GET response.
   self.capture('github_blob_http',result.stdout);self.capture('github_blob_stderr',result.stderr);return parse_blob_response(result.stdout,result.returncode,identifier,core.strict_json)
 return RecoveryProvider

def engine_class(core,checker,phase_pin,recovery_binding):
 Base=core.Engine;binding=json.loads(json.dumps(recovery_binding));need(type(binding) is dict and set(binding)=={'recovery_authorization_path','recovery_authorization_sha256','adapter_source_sha256','original_authority_sha256'} and type(binding['recovery_authorization_path']) is str and binding['recovery_authorization_path'] and all(type(binding[k]) is str and re.fullmatch('[a-f0-9]{64}',binding[k]) for k in ['recovery_authorization_sha256','adapter_source_sha256','original_authority_sha256']),'Exact additive authorization binding required')
 class RecoveryEngine(Base):
  def recheck(self):
   super().recheck();checker(self)
  def start(self,key,request):
   if key!='INTEGRATE' or self.action!='integrate':return super().start(key,request)
   self.recheck();old=self.j.read('INTEGRATE_PHASE_INTENT');need(pin(self.j.expected['INTEGRATE_PHASE_INTENT'])==phase_pin,'Original phase intent changed');need(old['operation']=='INTEGRATE' and old['action']=='integrate' and old['request']['head']==self.head and old['request']['parents']==[self.head,old['request']['main']],'Original phase contract differs')
   need(not self.j.keys('GIT_') and not self.j.exists('INTEGRATION_OBJECTS_VERIFIED') and not self.j.exists('INTEGRATION_VERIFIED'),'A Git mutation may already have been attempted; GET-only reconciliation, never repeat')
   need(not self.j.exists('RECOVERY01_INTEGRATION_RESUME_INTENT'),'Recovery already attempted; no second continuation')
   need(type(request) is dict and set(request)=={'head','main','parents'} and request['head']==self.head and type(request['main']) is str and re.fullmatch('[a-f0-9]{40}',request['main']) and request['parents']==[self.head,request['main']],'Fresh continuation planning differs')
   self.record('RECOVERY01_INTEGRATION_RESUME_INTENT',{'at':core.stamp(),'action':'integrate','original_phase_intent':phase_pin,'additive_authorization':binding,'original_request':old['request'],'new_latest_main_request':request,'latest_main_changed':request['main']!=old['request']['main'],'rule':'Root separately authorizes one continuation of only the unattempted Git portion; original phase/header preserved; all effect calls still use core mutate/once/fresh guards'})
 return RecoveryEngine
