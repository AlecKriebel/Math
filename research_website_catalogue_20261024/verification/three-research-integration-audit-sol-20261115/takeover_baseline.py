"""Fresh finite W baseline; explicit read-only Git environment, no status call.
Reuse authenticated old native raw index and stage stream by byte reference.
No W/.git writes, project imports, build, science or current writer access.
"""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,os,re,stat,struct,subprocess,sys,xml.etree.ElementTree as ET
N=Path(__file__).absolute().parent
W=Path('/Users/alec/Desktop/alec-dev/aleckriebel.com')
def need(x,s):
    if not x: raise ValueError(s)
def pin(b):return {'bytes':len(b),'SHA256':hashlib.sha256(b).hexdigest()}
def read(p):
    need(p.resolve()==p and stat.S_ISREG(p.lstat().st_mode),'ordinary real file '+str(p))
    return p.read_bytes()
def extent(root):
    need(root.resolve()==root and stat.S_ISDIR(root.lstat().st_mode),'ordinary root')
    fs,ds=[],[]
    def walk(d):
        for e in os.scandir(d):
            p=Path(e.path);r=p.relative_to(root).as_posix();m=p.lstat().st_mode
            if stat.S_ISDIR(m):ds.append(r);walk(p)
            else:need(stat.S_ISREG(m),'reject link/special');fs.append(r)
    walk(root);return sorted(fs),sorted(ds)
def main():
    need(sys.argv[1:]==[] and not (N/'INITIAL_SEAL.json').exists(),'fresh capture before INITIAL')
    oldb=read(N/'PRE_BASELINE.json');old=json.loads(oldb)
    rawold=read(Path(old['complete_raw_index']['path']))
    need(pin(rawold)=={k:old['complete_raw_index'][k] for k in ['bytes','SHA256']},'authenticate old whole native reference')
    need(pin(rawold)=={'bytes':9002656,'SHA256':'5f9c24f576cca18c466163a9572120f118698ead90eca728199030ba346e8244'},'fixed original raw index')
    receipts=[]
    def git(*args,reference=None):
        need(args[0] in {'rev-parse','symbolic-ref','remote','ls-remote','ls-files','diff'},'finite read-only Git vocabulary')
        env={k:v for k,v in os.environ.items() if not k.startswith('GIT_')};env['GIT_OPTIONAL_LOCKS']='0'
        start=datetime.now(timezone.utc).isoformat()
        r=subprocess.run(['git','-c','core.fsmonitor=false','-c','core.hooksPath=/dev/null',*args],cwd=W,env=env,stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=30)
        row={'operation':args[0],'arguments':list(args) if args[0]!='ls-remote' else ['ls-remote','<bound_push_URL>','refs/heads/master'],'UTC_start':start,'UTC_end':datetime.now(timezone.utc).isoformat(),'exit_code':r.returncode,'stdout':pin(r.stdout),'stderr':{**pin(r.stderr),'literal':r.stderr.decode(errors='replace')},'GIT_OPTIONAL_LOCKS':'0'}
        if reference:
            need(r.stdout==read(reference),'exact whole old stage stream');row['stdout']['unchanged_reference']=str(reference)
        elif args[0]!='remote':row['stdout']['literal']=r.stdout.decode(errors='replace')
        receipts.append(row);need(r.returncode==0 and not r.stderr,'actual clean Git read-only result')
        return r.stdout
    def state():
        need(git('rev-parse','--show-toplevel').decode().strip()==str(W),'fixed checkout')
        need(git('symbolic-ref','HEAD')==b'refs/heads/master\n','fixed master branch')
        ids=git('rev-parse','HEAD','refs/heads/master','HEAD^{tree}').decode().splitlines()
        need(ids==['2b78e689e571e658daa859f29b97a61b9ec479ed','2b78e689e571e658daa859f29b97a61b9ec479ed','4392815cea2aab48096a321869e0e30ae616ecbc'],'fixed HEAD master tree')
        urls=git('remote','get-url','--push','--all','origin').splitlines()
        need(len(urls)==1 and hashlib.sha256(urls[0]).hexdigest()==old['Git']['push_URL_SHA256'],'same bound push destination')
        remote=git('ls-remote','--refs',urls[0].decode(),'refs/heads/master')
        need(remote.decode()==old['Git']['actual_remote_advertisement'],'same actual remote advertisement')
        raw=read(W/'.git/index');need(raw==rawold and not os.path.lexists(W/'.git/index.lock'),'exact original raw index restored and no lock')
        need(raw[:4]==b'DIRC' and hashlib.sha1(raw[:-20]).digest()==raw[-20:] and struct.unpack('>II',raw[4:12])==(2,58571),'whole native header count checksum')
        controls={name:pin(read(W/'.git'/name)) for name in ['HEAD','refs/heads/master','config']}
        return {'HEAD':ids[0],'master':ids[1],'tree':ids[2],'index':pin(raw),'index_mode':stat.S_IMODE((W/'.git/index').lstat().st_mode),'controls':controls,'push_URL_SHA256':hashlib.sha256(urls[0]).hexdigest(),'actual_remote_advertisement':remote.decode()}
    before=state();need(before==old['Git'],'whole original Git baseline unchanged')
    git('ls-files','--stage','-z',reference=N/'private/pre-git-06.stdout')
    need(git('diff','--cached','--name-only','--diff-filter=D','-z',before['HEAD'])==b'','zero staged deletions')
    fs,ds=extent(W/'public');need(fs==old['public_files'] and ds==old['public_directories'],'exact entire public namespace')
    rows=[]
    for expected in old['public_configs_controls']:
        p=Path(expected['path']);actual={'path':str(p),**pin(read(p))};need(actual==expected,'whole public/config/control bytes '+str(p));rows.append(actual)
    index=read(W/'public/research/index.html')
    graph=json.loads(re.findall(rb'<script type="application/ld\+json">\s*(.*?)\s*</script>',index,re.S)[0])['mainEntity']
    need(graph['numberOfItems']==len(graph['itemListElement'])==96,'actual ItemList 96')
    sitemap=ET.fromstring(read(W/'public/research/sitemap.xml'));need(len(sitemap)==97,'actual sitemap97')
    need(len(fs)==631 and len(rows)==640,'actual631 public and640 files with config/controls')
    for r in rows:need(pin(read(Path(r['path'])))=={k:r[k] for k in ['bytes','SHA256']},'whole end bytes unchanged')
    need(extent(W/'public')==(fs,ds) and state()==before,'end complete namespace/Git equality')
    result={'UTC':datetime.now(timezone.utc).isoformat(),'status':'FRESH_TAKEOVER_READONLY_BASELINE_PASS','prior_baseline_reference':{'path':str(N/'PRE_BASELINE.json'),**pin(oldb)},'Git':before,'actual_public_files':631,'actual_public_directories':len(ds),'actual_ItemList':96,'actual_sitemap':97,'public_configs_controls_rehashed':640,'native_records':58571,'protected_native_records':58569,'actual_staged_deletions':0,'native_raw_reference':old['complete_raw_index'],'no_duplicate_native_index_or_stage_copy':True,'whole_public_file_directory_and_hash_list_reference':'PRE_BASELINE.json','all_public_config_control_bytes_rechecked_twice':True,'Git_readonly_receipts':receipts,'current_writer_folder_accessed':False,'production_mutation':False,'incident_qualification':'Earlier unguarded takeover git status refreshed40native cached statrecords. Incident retained separately; this PASS is fresh after root-owned guarded restoration, not a retroactive claim that no refresh occurred.'}
    with (N/'TAKEOVER_BASELINE_CURRENT.json').open('x') as f:json.dump(result,f,indent=2);f.write('\n')
    print(json.dumps({k:result[k] for k in ['status','actual_public_files','actual_ItemList','actual_sitemap','native_records','protected_native_records','actual_staged_deletions','current_writer_folder_accessed']}))
if __name__=='__main__':main()
