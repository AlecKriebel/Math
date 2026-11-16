#!/usr/bin/env python3
"""Bounded RAM/owned-temp mechanism tests; never invokes a release mode."""
from pathlib import Path
import ast,base64,datetime,hashlib,json,os,stat,struct,subprocess,tempfile
P=Path('/Users/alec/Documents/Math/research_website_catalogue_20261024')
N=P/'verification/next-three-production-release-sol-20261116'
O=P/'verification/next-three-production-audit-sol-20261116'
W=Path('/Users/alec/Desktop/alec-dev/aleckriebel.com')
CODE=N/'release_next_three.py'; EXPECTED='266bb054694b5996680757de6205ace307cb846b996c8164ac1a26bb76335159'
source=CODE.read_bytes(); assert hashlib.sha256(source).hexdigest()==EXPECTED
selected={'need','utc','sha','pin','packed','inode','mode','safe','held','read','write_all','sync_dir','new_file','event','entries','transaction','authorization'}
mod=ast.parse(source); nodes=[n for n in mod.body if isinstance(n,ast.FunctionDef)and n.name in selected]
assert {n.name for n in nodes}==selected
ns={k:v for k,v in globals().items()if k in ['Path','datetime','hashlib','json','os','stat','struct']};ns['LOG']=None
exec(compile(ast.Module(body=nodes,type_ignores=[]),str(CODE)+' [selected functions only]','exec'),ns)
rows=[]
def record(name,fn,reject=False):
 try:result=fn()
 except (ValueError,FileExistsError,IndexError,struct.error)as e:
  if not reject:raise
  rows.append({'case':name,'rejected':True,'reason':str(e)});return
 if reject:raise AssertionError('Unexpected acceptance: '+name)
 rows.append({'case':name,'accepted_expected':True,'detail':result})
def rawindex(records,extension=b''):
 b=b'DIRC'+struct.pack('>II',2,len(records))+b''.join(records)+extension;return b+hashlib.sha1(b).digest()
def entry(name,flags=0,oid=b'\1'*20):
 b=bytearray(62);b[24:28]=struct.pack('>I',0o100644);b[40:60]=oid;b[60:62]=struct.pack('>H',flags|min(len(name),0xfff));b.extend(name+b'\0');b.extend(b'\0'*((-len(b))%8));return bytes(b)
base=[entry(b'a'),entry(b'b',0x8000),entry(b'z')]
record('index accepts valid stage-zero plus assume-unchanged raw flag',lambda:{k.decode():hashlib.sha256(v[0]).hexdigest()for k,v in ns['entries'](rawindex(base)).items()})
record('index rejects stage-one hidden unrelated record',lambda:ns['entries'](rawindex([entry(b'a'),entry(b'b',0x1000)])),True)
record('index rejects unsupported extended flags',lambda:ns['entries'](rawindex([entry(b'a',0x4000)])),True)
record('index rejects forged checksum',lambda:ns['entries'](rawindex(base)[:-1]+b'!'),True)
record('index rejects duplicate path ordinal',lambda:ns['entries'](rawindex([entry(b'a'),entry(b'a')])),True)
record('index rejects LINK split-index extension',lambda:ns['entries'](rawindex(base,b'link'+struct.pack('>I',0))),True)
actual=(W/'.git/index').read_bytes();parsed=ns['entries'](actual);protected=[v[0]for k,v in parsed.items()if k not in {b'public/research/index.html',b'public/research/sitemap.xml'}]
record('actual58585 protected raw records independently match INITIAL',lambda:len(protected)if len(protected)==58585 and hashlib.sha256(b''.join(protected)).hexdigest()==json.loads((O/'INITIAL.json').read_bytes())['W']['protected_raw_records_ordered_SHA256']else (_ for _ in()).throw(AssertionError('raw mismatch')))
with tempfile.TemporaryDirectory(prefix='mechanism-fixtures-',dir=O)as temp:
 root=Path(temp);real=root/'regular';real.write_bytes(b'unchanged fixture')
 record('held ordinary source read',lambda:ns['read'](real).decode())
 alias=root/'source-alias';alias.symlink_to(real)
 record('source leaf symlink rejected',lambda:ns['read'](alias),True)
 directory=root/'directory';directory.mkdir();(directory/'file').write_bytes(b'ordinary');da=root/'target-parent-alias';da.symlink_to(directory,target_is_directory=True)
 record('source/target ancestor symlink rejected',lambda:ns['safe'](da/'file'),True)
 dest=root/'exclusive';record('exclusive new file creates durable complete owned buffer',lambda:(ns['new_file'](dest,b'complete'),ns['read'](dest).decode())[1])
 record('exclusive leaf collision rejects overwrite',lambda:ns['new_file'](dest,b'replacement'),True)
 # Transaction functions are redirected exclusively to owned ephemeral directories.
 ns['N']=root;ns['W']=root;lock_root=root/'transactions';root.chmod(0o755)
 t,check,lockfd=ns['transaction']('install',b'owned fixture authorization');check()
 record('transaction uses authorization SHA directory and retained exact lock',lambda:{'transaction':t.name,'authorization_sha':hashlib.sha256(b'owned fixture authorization').hexdigest(),'same':t.name==hashlib.sha256(b'owned fixture authorization').hexdigest()})
 record('same authorization cannot reacquire fixed owned lock',lambda:ns['transaction']('install',b'owned fixture authorization'),True)
 lock=root/'ACTIVE_INSTALL.lock';body=lock.read_bytes();lock.unlink();lock.write_bytes(body);lock.chmod(0o600)
 record('same lock bytes on replacement inode rejected',check,True)
 ns['LOG'].close();os.close(lockfd);ns['LOG']=None
 # Model only configuration precedence. These commands read W/config and one owned include;
 # they perform no push, ls-remote, remote contact or configuration mutation.
 cfg=root/'ambient-push.ini';cfg.write_text('[remote "origin"]\n\tpushurl = https://example.invalid/unapproved.git\n')
 env={k:v for k,v in os.environ.items()if not k.startswith('GIT_')};env.update(GIT_OPTIONAL_LOCKS='0',GIT_INDEX_VERSION='2',GIT_TERMINAL_PROMPT='0')
 opts=['git','--no-optional-locks','-c','core.hooksPath=/dev/null','-c','core.fsmonitor=false','-c','remote.origin.mirror=false','-c','include.path='+str(cfg)]
 fetch=subprocess.run(opts+['remote','get-url','origin'],cwd=W,env=env,capture_output=True,check=True).stdout.decode().strip()
 push=subprocess.run(opts+['remote','get-url','--push','origin'],cwd=W,env=env,capture_output=True,check=True).stdout.decode().strip()
 rows.append({'case':'ambient pushurl bypasses fetch-only destination fence','fetch_url':fetch,'push_url':push,'current_fetch_check_passes':fetch=='https://github.com/AlecKriebel/aleckriebel.com.git','different_push_destination':push!=fetch,'remote_contact':False,'qualification':'Owned CLI include models equivalent inherited system/global configuration; no actual global config changed.'})
print(json.dumps({'helper_SHA256':EXPECTED,'tests':rows,'fixture_scope':'RAM and temporary directory under audit ownership only; removed on completion','release_modes_executed':[],'remote_contact':False,'W_or_Math_mutations':False},indent=2))
