"""Fresh finite website/Git read-only baseline; owned receipts only.
No private stage-writer access, Git mutation, project import, build or science.
"""
from datetime import datetime,timezone
import hashlib
import json
import os
from pathlib import Path
import re
import stat
import struct
import subprocess
import sys
import xml.etree.ElementTree as ET

N=Path(__file__).absolute().parent
P=N.parent.parent
W=Path('/Users/alec/Desktop/alec-dev/aleckriebel.com')
BASE='2b78e689e571e658daa859f29b97a61b9ec479ed'
INDEX='5f9c24f576cca18c466163a9572120f118698ead90eca728199030ba346e8244'
PUSH='e2eedeb3774ab61a83099c03db58316eba19d5cf4e3fdec265e7fe041aa29763'
AUTHORITIES={'23418581':'2fd373bc8776b88f12ab5ca71d8b7d8d6e49143d956798147d5edfb4ec83adc0','23202966':'8b3ef9a219c4e6b46f60d7276abb05e49c3175a62a61921f38646f4070bd5e15','23205305':'431c5951067b0e320185e60be47ad0bd936d3515e420516e0d911344ace1be51'}

def need(ok,why):
    if not ok:raise ValueError(why)

def sha(b):return hashlib.sha256(b).hexdigest()
def descriptor(b):return {'bytes':len(b),'SHA256':sha(b)}

def read(p):
    need(p.resolve()==p and stat.S_ISREG(p.lstat().st_mode),'ordinary real file '+str(p));return p.read_bytes()

def new(name,b):
    path=N/name;need(path.is_relative_to(N),'owned output')
    with path.open('xb') as f:need(f.write(b)==len(b),'complete exclusive receipt')

def extent(root):
    need(root.resolve()==root and stat.S_ISDIR(root.lstat().st_mode),'ordinary real directory')
    files,dirs=[],[]
    def walk(d):
        with os.scandir(d) as rows:
            for e in rows:
                q=Path(e.path);rel=q.relative_to(root).as_posix();m=q.lstat().st_mode
                if stat.S_ISDIR(m):dirs.append(rel);walk(q)
                else:need(stat.S_ISREG(m),'reject symlink/special');files.append(rel)
    walk(root);return sorted(files),sorted(dirs)

def native_index(raw):
    need(raw[:4]==b'DIRC' and len(raw)>=32 and hashlib.sha1(raw[:-20]).digest()==raw[-20:],'native index header/checksum')
    version,count=struct.unpack('>II',raw[4:12]);need(version==2 and count==58571,'actual native version2/58571 records')
    pos=12;end=len(raw)-20;entries=[]
    for _ in range(count):
        start=pos;need(pos+62<=end,'complete raw record');flags=struct.unpack('>H',raw[pos+60:pos+62])[0]
        need(flags&0xf000==0,'actual stage0/native flags');stop=raw.find(b'\0',pos+62,end);need(stop>=0,'native path terminator')
        name=raw[pos+62:stop];need(name and flags&0xfff==min(len(name),0xfff),'native exact path length')
        pos=start+((stop-start+1+7)//8)*8;need(pos<=end and not any(raw[stop:pos]),'whole native zero padding')
        mode=struct.unpack('>I',raw[start+24:start+28])[0];oid=raw[start+40:start+60].hex()
        need(mode in (0o100644,0o100755,0o120000,0o160000),'supported actual mode');entries.append((name,raw[start:pos],mode,oid))
    need([x[0] for x in entries]==sorted(set(x[0] for x in entries)),'native unique byte ordering')
    extensions=[]
    while pos<end:
        need(pos+8<=end,'complete extension');kind=raw[pos:pos+4];size=struct.unpack('>I',raw[pos+4:pos+8])[0]
        need(kind==b'TREE' and not extensions and pos+8+size<=end,'known optional TREE only');extensions.append({'kind':'TREE','bytes':size,'SHA256':sha(raw[pos+8:pos+8+size])});pos+=8+size
    need(pos==end,'whole native raw extent')
    protected=[(p,b) for p,b,_,_ in entries if p not in {b'public/research/index.html',b'public/research/sitemap.xml'}]
    need(len(protected)==58569,'58569 records outside two eligible aggregate records')
    fingerprint=sha(b'\0'.join(p+b'\t'+b.hex().encode() for p,b in protected)+b'\0')
    stage=b''.join(('%o %s 0\t'%(mode,oid)).encode()+name+b'\0' for name,_,mode,oid in entries)
    return {'version':version,'records':count,'protected_records':len(protected),'protected_whole_record_SHA256':fingerprint,'extensions':extensions},stage

def main():
    need(sys.argv[1:] in [['pre'],['post']],'only finite pre/post read-only capture');phase=sys.argv[1]
    need(not (N/'FINAL_SEAL.json').exists() and not (N/(phase.upper()+'_BASELINE.json')).exists(),'one exclusive pre-FINAL capture per phase')
    for rid,pin in AUTHORITIES.items():
        b=read(P/('verification/root-editorial-'+rid+'-20261115.json'));need(sha(b)==pin,'actual fixed root editorial adoption');a=json.loads(b)
        if rid=='23418581':need(a['rootCompleteCurrentCopyAndConfigAdopted'] is True and a['productionInstallationAuthorized'] is False,'132 copy adoption not installation')
        else:need(a['root_copy_adopted'] is True and a['production_install_authority'] is False,'135136 copy adoption not installation')
    # No website/Git access has occurred above. Only read-only operations below.
    receipts=[]
    def git(*args):
        need(args[0] in {'rev-parse','symbolic-ref','remote','ls-remote','ls-files','diff'},'read-only Git vocabulary')
        env={k:v for k,v in os.environ.items() if not k.startswith('GIT_')};env['GIT_OPTIONAL_LOCKS']='0'
        argv=['git','-c','core.fsmonitor=false','-c','core.hooksPath=/dev/null',*args];start=datetime.now(timezone.utc).isoformat()
        try:
            r=subprocess.run(argv,cwd=W,env=env,stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=30);out,err,code,timedout=r.stdout,r.stderr,r.returncode,False
        except subprocess.TimeoutExpired as e:out,err,code,timedout=e.output or b'',e.stderr or b'',None,True
        item={'operation':args[0],'arguments':list(args),'started_UTC':start,'completed_UTC':datetime.now(timezone.utc).isoformat(),'actual_exit':code,'timed_out':timedout}
        for label,body in [('stdout',out),('stderr',err)]:
            name='private/%s-git-%02d.%s'%(phase,len(receipts)+1,label);new(name,body);item[label]={'path':str(N/name),**descriptor(body)}
        receipts.append(item)
        if code!=0 or timedout:
            new(phase.upper()+'_FAILED_GIT.json',(json.dumps(receipts,indent=2)+'\n').encode());raise ValueError('read-only Git failure, whole streams retained, no retry')
        return out
    def state():
        need(git('rev-parse','--show-toplevel').decode().strip()==str(W),'actual fixed website checkout')
        need(git('symbolic-ref','HEAD').strip()==b'refs/heads/master','actual master branch')
        ids=git('rev-parse','HEAD','refs/heads/master','HEAD^{tree}').decode().splitlines();need(len(ids)==3 and ids[:2]==[BASE,BASE] and len(ids[2])==40,'actual fixed HEAD/master, observed tree')
        urls=git('remote','get-url','--push','--all','origin').splitlines();need(len(urls)==1 and sha(urls[0])==PUSH,'single actually bound push destination')
        remote=git('ls-remote','--refs',urls[0].decode(),'refs/heads/master');need(remote.split()==[BASE.encode(),b'refs/heads/master'],'actual remote advertisement')
        raw=read(W/'.git/index');need(sha(raw)==INDEX and not os.path.lexists(W/'.git/index.lock'),'actual complete native raw index/no lock')
        return {'HEAD':BASE,'master':BASE,'tree':ids[2],'index':descriptor(raw),'index_mode':stat.S_IMODE((W/'.git/index').lstat().st_mode),'controls':{name:descriptor(read(W/'.git'/name)) for name in ['HEAD','refs/heads/master','config']},'push_URL_SHA256':PUSH,'actual_remote_advertisement':remote.decode()}
    before=state();raw=read(W/'.git/index');native,stage=native_index(raw)
    need(git('ls-files','--stage','-z')==stage,'actual Git native stage tuples exactly match every parsed raw record')
    need(git('diff','--cached','--name-only','--diff-filter=D','-z',BASE)==b'','zero actual staged deletions')
    names,dirs=extent(W/'public');need(len(names)==631,'actual631 public ordinary files')
    fixed=['.firebaserc','firebase.json','.gitignore','README.md','deploy.sh','preview.sh']
    paths=[*(W/'public'/name for name in names),*(W/name for name in fixed),*(W/'.git'/name for name in ['HEAD','refs/heads/master','config'])]
    bodies={str(q):read(q) for q in paths};rows=[{'path':q,**descriptor(b)} for q,b in bodies.items()]
    html=bodies[str(W/'public/research/index.html')]
    graph=json.loads(re.findall(rb'<script type="application/ld\+json">\s*(.*?)\s*</script>',html,re.S)[0])['mainEntity']
    need(graph['numberOfItems']==len(graph['itemListElement'])==96,'actual96 index items')
    need(len(ET.fromstring(bodies[str(W/'public/research/sitemap.xml')]))==97,'actual97 research XML entries')
    for q in ['public/research/index.html','public/research/sitemap.xml','public/research/research.css']:
        new('private/'+phase+'-'+Path(q).name,bodies[str(W/q)])
    new('private/'+phase+'-shared-index.raw',raw)
    need(extent(W/'public')==(names,dirs) and all(read(Path(q))==b for q,b in bodies.items()),'complete public/config/control before-after byte equality')
    after=state();need(after==before and read(W/'.git/index')==raw,'full start/end HEAD/master/tree/rawindex/config/actualremote equality')
    result={'UTC':datetime.now(timezone.utc).isoformat(),'status':'PASS_INDEPENDENT_FRESH_READONLY_BASELINE','phase':phase,'Git':after,'actual_counts':[631,96,97],'public_files':names,'public_directories':dirs,'public_configs_controls':rows,'actual_native_index':native,'actual_staged_deletions':0,'complete_raw_index':{'path':str(N/'private'/(phase+'-shared-index.raw')),**descriptor(raw)},'actual_readonly_Git_receipts':receipts,'programme_HEAD_index_or_refs_read':False,'current_private_stage_writer_accessed':False,'production_mutation':False}
    if phase=='post':
        old=json.loads(read(N/'PRE_BASELINE.json'));need(result['Git']==old['Git'] and rows==old['public_configs_controls'] and names==old['public_files'] and dirs==old['public_directories'],'whole fixed baseline unchanged after private stage audit')
    new(phase.upper()+'_BASELINE.json',(json.dumps(result,indent=2)+'\n').encode())
    print(json.dumps({'status':result['status'],'phase':phase,'actual_counts':[631,96,97],'actual_native_records':58571,'protected_records':58569,'actual_staged_deletions':0,'Git_readonly_commands':len(receipts),'current_stage_writer_accessed':False,'production_mutation':False},sort_keys=True))

if __name__=='__main__':main()
