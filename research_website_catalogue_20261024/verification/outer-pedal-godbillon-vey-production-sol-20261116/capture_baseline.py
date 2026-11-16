#!/usr/bin/env python3
"""One finite read-only baseline capture. Prints data; creates no file or lock."""
from pathlib import Path
import datetime, hashlib, json, os, re, stat, struct, subprocess

P=Path('/Users/alec/Documents/Math/research_website_catalogue_20261024')
M=P.parent
W=Path('/Users/alec/Desktop/alec-dev/aleckriebel.com')
EXPECTED_INDEX='1959097114e85b4e451c3dca1a2bcf35cf1592442378633688d85d8416d69a7e'
ENV={key:value for key,value in os.environ.items() if not key.startswith('GIT_')}
ENV['GIT_OPTIONAL_LOCKS']='0'
queries=[]

def need(ok,label):
    if not ok: raise ValueError(label)
def pin(data): return {'bytes':len(data),'SHA256':hashlib.sha256(data).hexdigest()}
def read(path):
    need(all(not q.is_symlink() for q in [path,*path.parents]),'no symlink path')
    first=path.lstat();need(stat.S_ISREG(first.st_mode),'regular file')
    data=path.read_bytes();last=path.lstat()
    need((first.st_dev,first.st_ino,first.st_size,first.st_mtime_ns,first.st_ctime_ns)==(last.st_dev,last.st_ino,last.st_size,last.st_mtime_ns,last.st_ctime_ns),'stable whole file')
    return data
def row(path): return {**pin(read(path)),'mode':stat.S_IMODE(path.lstat().st_mode)}
def git(*args,cwd=W,absent=False):
    result=subprocess.run(['git','--no-optional-locks','-c','core.fsmonitor=false','-c','core.hooksPath=/dev/null',*args],cwd=cwd,env=ENV,capture_output=True)
    queries.append({'cwd':str(cwd),'args':list(args),'exit':result.returncode,'stdout':pin(result.stdout),'stderr':pin(result.stderr)})
    need(result.returncode==0 or (absent and result.returncode==1 and not result.stdout and not result.stderr),'read-only Git query: '+repr(args)+' '+result.stderr.decode(errors='replace'))
    return result.stdout
def census(root):
    files={};dirs={}
    def walk(directory):
        need(not directory.is_symlink(),'ordinary directory');before=directory.lstat()
        dirs[directory.relative_to(root).as_posix()]=stat.S_IMODE(before.st_mode)
        for path in sorted(directory.iterdir()):
            kind=path.lstat().st_mode
            if stat.S_ISDIR(kind):walk(path)
            elif stat.S_ISREG(kind):files[path.relative_to(root).as_posix()]=row(path)
            else:raise ValueError('special public path')
        after=directory.lstat();need((before.st_ino,before.st_mtime_ns,before.st_ctime_ns)==(after.st_ino,after.st_mtime_ns,after.st_ctime_ns),'stable public directory')
    walk(root);return files,dirs
def index_records(data):
    need(data[:4]==b'DIRC' and struct.unpack('>I',data[4:8])[0]==2,'v2 native index')
    need(hashlib.sha1(data[:-20]).digest()==data[-20:],'native index checksum')
    records={};position=12;previous=None
    for unused in range(struct.unpack('>I',data[8:12])[0]):
        start=position;flags=struct.unpack('>H',data[start+60:start+62])[0]
        need(not flags&0x7000,'ordinary stage-zero v2 records')
        end=data.index(b'\0',start+62);name=data[start+62:end]
        position=start+((end+1-start+7)//8)*8
        need(name and (previous is None or previous<name) and not any(data[end+1:position]),'sorted whole raw records/padding')
        need(flags&0xfff==min(len(name),0xfff),'byte pathname length')
        records[name]=(data[start:position],struct.unpack('>I',data[start+24:start+28])[0],data[start+40:start+60].hex())
        previous=name
    start=position;extensions=[]
    while position<len(data)-20:
        signature=data[position:position+4];size=struct.unpack('>I',data[position+4:position+8])[0]
        need(signature==b'TREE' and position+8+size<=len(data)-20,'only derived TREE extension')
        extensions.append({'signature':'TREE','payload_bytes':size});position+=8+size
    need(position==len(data)-20 and len(extensions)==1,'exact sole extension extent')
    return records,{'offset':start,**pin(data[start:-20]),'extensions':extensions}

initial_W_index=read(W/'.git/index');initial_M_index=read(M/'.git/index')
need(pin(initial_W_index)=={'bytes':9051646,'SHA256':EXPECTED_INDEX} and row(W/'.git/index')['mode']==0o644,'exact current W index lease')
need(hashlib.sha256(initial_M_index).hexdigest()=='91b10d938f7d737226662bbff3b07016dcc0e501376a045811ab4e930c6fbb11','Math index lease')
head=git('rev-parse','HEAD').strip().decode();tree=git('rev-parse','HEAD^{tree}').strip().decode()
need(head=='ff36a8299805d9a6196a3d5b081d354c87627056' and tree=='06197e4738ecd7e2aee392455f5cc734523380a0','current W HEAD/tree')
need(git('symbolic-ref','HEAD').strip()==b'refs/heads/master','existing master')
need(git('rev-parse','HEAD',cwd=M).strip()==b'a4ce3c37dad209339e490d18dcced6c48cf912d2','Math local HEAD')
need(git('symbolic-ref','HEAD',cwd=M).strip()==b'refs/heads/main','Math main')
records,extension=index_records(initial_W_index);need(len(records)==58667,'current raw record count')
tree_raw=git('ls-tree','-r','-z','--full-tree',tree);parts=tree_raw.split(b'\0');need(parts.pop()==b'','NUL tree framing')
head_entries={}
for part in parts:
    header,name=part.split(b'\t',1);bits,kind,oid=header.split();need(name not in head_entries,'unique HEAD path')
    head_entries[name]=(int(bits,8),oid.decode())
foreign=[{'path_hex':name.hex(),'index':records.get(name,(None,None,None))[1:],'HEAD':head_entries.get(name)} for name in sorted(set(records)|set(head_entries)) if records.get(name,(None,None,None))[1:]!=head_entries.get(name)]
aggregates={b'public/research/index.html',b'public/research/sitemap.xml'}
need(aggregates<=set(records),'two existing aggregate records')
protected=b''.join(value[0] for name,value in records.items() if name not in aggregates)
files,dirs=census(W/'public');need(len(files)==727 and len(dirs)==364,'whole current public extent')
index_text=read(W/'public/research/index.html').decode();typed=re.search(r'<script type="application/ld\+json">(.*?)</script>',index_text,re.S)[1]
visible=re.findall(r'<li\b[^>]*>[\s\S]*?</li>',index_text);entity=json.loads(typed)['mainEntity']
sitemap=read(W/'public/research/sitemap.xml').decode();nodes=re.findall(r'<url>[\s\S]*?</url>',sitemap)
need(len(visible)==len(entity['itemListElement'])==entity['numberOfItems']==118 and len(nodes)==119,'current aggregates')
origin='https://github.com/AlecKriebel/aleckriebel.com.git'
routing_args=('config','--null','--show-origin','--show-scope','--get-regexp',r'^(remote\.origin\.(url|pushurl|mirror|vcs)|url\..*\.(insteadof|pushinsteadof))$')
routing_before=git(*routing_args);vcs=git('config','--null','--get-all','remote.origin.vcs',absent=True)
fetch=git('remote','get-url','--all','origin');push=git('remote','get-url','--push','--all','origin')
need(not vcs and fetch==push==(origin+'\n').encode() and routing_before==git(*routing_args),'stable exact effective singleton routing')
config={str(path):row(path) for path in [W/'.git/config',W/'.git/HEAD',W/'firebase.json',W/'public/research/research.css',M/'.git/config',M/'.git/HEAD']}
adoption=P/'verification/root-162163-editorial-adoption-20261116.json'
need(row(adoption)['SHA256']=='ca6f45fd2ac2525be3e2b7760e0e0330ee532240e0e906f6db777a279fd446fd','private copy source authority')
need(read(W/'.git/index')==initial_W_index and read(M/'.git/index')==initial_M_index,'both native indexes unchanged')
need(git('rev-parse','HEAD').strip().decode()==head and git('rev-parse','HEAD',cwd=M).strip()==b'a4ce3c37dad209339e490d18dcced6c48cf912d2','closing local HEAD guards')
print(json.dumps({'UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'READONLY_BASELINE_CAPTURE_SCOPE_IMPLEMENTATION_ON_HOLD','W_HEAD':head,'W_tree':tree,'W_index':row(W/'.git/index'),'M_HEAD':'a4ce3c37dad209339e490d18dcced6c48cf912d2','M_index':row(M/'.git/index'),'index_records':len(records),'HEAD_tree_raw':pin(tree_raw),'HEAD_tree_records':len(head_entries),'foreign_staging_semantic_differences':foreign,'native_extension':extension,'protected_raw_records_excluding_two_aggregates':{'count':len(records)-2,**pin(protected)},'public_files':files,'public_directories_including_root':dirs,'visible_items_raw':visible,'typed_script_complete_raw':typed,'sitemap_nodes_raw':nodes,'configuration_guards':config,'routing':{'configuration':pin(routing_before),'effective_fetch_URL_SHA256':hashlib.sha256(fetch).hexdigest(),'effective_push_URL_SHA256':hashlib.sha256(push).hexdigest(),'intended_origin':origin,'origin_vcs_absent':True},'private_two_copy_adoption':{'path':str(adoption),**row(adoption)},'read_only_Git_queries':queries,'shared_index_refresh_or_write_tree_private_index_network_mutation':False,'release_helper_executions':0,'stage_or_third_copy_discovery':False,'production_authority':False},indent=2,ensure_ascii=False))
