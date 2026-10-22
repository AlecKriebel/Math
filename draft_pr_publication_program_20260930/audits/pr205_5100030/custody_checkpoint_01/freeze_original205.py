"""PR205 original native-byte custody only. GETs and new local case files only."""
import sys
if sys.flags.optimize or not sys.dont_write_bytecode:raise RuntimeError('Ordinary Python -B required')
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import base64,datetime,hashlib,json,os,re,subprocess
D=Path(__file__).resolve().parent;A=D.parent
HEAD='e8d7e925d19698edcb75822e40ca5ac820eb4388';NATIVE='unsolved_math_prioritization/attempts/5100030/';Q='unsolved_math_prioritization/QUEUE.md'
INTAKE='ROOT_ORIGINAL_STATUS_ONLY_INTAKE_01.json';INTAKE_PIN={'bytes':4046,'sha256':'a719ec4d6cdd1a36620f02df1f18ae06fd5a3e5804972d1a3d96b349e88fb178'}
TREES={}
def need(ok,message):
    if not ok:raise RuntimeError(message)
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def pin(raw):return {'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()}
def bpin(raw):return {**pin(raw),'git_blob':hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()}
def enc(obj):return (json.dumps(obj,indent=2,allow_nan=False)+'\n').encode()
def sha(value):return re.fullmatch('[0-9a-f]{40}',str(value)) is not None
def api(path):
    need(path in ('pulls/205','pulls/205/commits?per_page=100') or re.fullmatch(r'git/(commits|trees|blobs)/[0-9a-f]{40}',path) is not None,'GET allowlist')
    result=subprocess.run(['gh','api','repos/AlecKriebel/Math/'+path,'--method','GET'],capture_output=True,timeout=90)
    need(result.returncode==0,'Authenticated GET failed '+path+' '+result.stderr.decode(errors='replace')[:200]);return json.loads(result.stdout)
def save(path,raw):
    need(path.resolve().is_relative_to(A),'New case output scope');path.parent.mkdir(parents=True,exist_ok=True)
    with path.open('xb') as stream:need(stream.write(raw)==len(raw),'Short custody write');stream.flush();os.fchmod(stream.fileno(),0o444);os.fsync(stream.fileno())
    fd=os.open(path.parent,os.O_RDONLY|os.O_DIRECTORY)
    try:os.fsync(fd)
    finally:os.close(fd)
def tree(oid):
    need(sha(oid),'Native tree request')
    if oid in TREES:return TREES[oid]
    j=api('git/trees/'+oid);need(j['sha']==oid and j.get('truncated') is False and isinstance(j['tree'],list),'Native tree identity/truncation');rows=j['tree']
    need(len({x['path'] for x in rows})==len(rows),'Duplicate native tree name')
    for x in rows:
        need(isinstance(x['path'],str) and x['path'] not in ('','.','..') and '/' not in x['path'] and '\0' not in x['path'],'Native tree path')
        need((x['mode'],x['type']) in (('040000','tree'),('100644','blob'),('100755','blob'),('120000','blob'),('160000','commit')) and sha(x['sha']),'Native mode/type/OID schema')
    ordered=sorted(rows,key=lambda x:x['path'].encode()+(b'/' if x['type']=='tree' else b''));need(rows==ordered,'Native tree canonical order')
    raw=b''.join(x['mode'].lstrip('0').encode()+b' '+x['path'].encode()+b'\0'+bytes.fromhex(x['sha']) for x in ordered)
    need(hashlib.sha1(b'tree '+str(len(raw)).encode()+b'\0'+raw).hexdigest()==oid,'Full native tree SHA1');TREES[oid]=j;return j
def lookup(root,path):
    current=root
    for i,name in enumerate(path.split('/')):
        matches=[x for x in tree(current)['tree'] if x['path']==name]
        if not matches:return None
        need(len(matches)==1,'Ambiguous native path');x=matches[0]
        if i==len(path.split('/'))-1:return x
        need(x['type']=='tree','Nondirectory native parent');current=x['sha']
def walk(root,prefix=''):
    result={}
    for x in tree(root)['tree']:
        path=prefix+x['path']
        if x['type']=='tree':result.update(walk(x['sha'],path+'/'))
        else:need(x['type']=='blob' and x['mode'] in ('100644','100755'),'Nonregular original file');result[path]=x
    return result
def identity(x):return None if x is None else (x['mode'],x['type'],x['sha'])
def delta(left,right,prefix=''):
    if left==right:return []
    old={x['path']:x for x in tree(left)['tree']} if left else {};new={x['path']:x for x in tree(right)['tree']} if right else {};result=[]
    for name in sorted(old.keys()|new.keys()):
        x,y=old.get(name),new.get(name)
        if identity(x)==identity(y):continue
        if (x is None or x['type']=='tree') and (y is None or y['type']=='tree'):result+=delta(x['sha'] if x else None,y['sha'] if y else None,prefix+name+'/')
        else:need((x is None or x['type']=='blob') and (y is None or y['type']=='blob'),'Original type change');result.append(prefix+name)
    return result
def blob(row):
    need(row is not None and row['type']=='blob','Native blob required');j=api('git/blobs/'+row['sha']);need(j['encoding']=='base64','Native blob encoding')
    raw=base64.b64decode(''.join(j['content'].split()),validate=True);need(j['sha']==row['sha']==bpin(raw)['git_blob'] and j['size']==len(raw) and ('size' not in row or row['size']==len(raw)),'Native blob size/SHA1');return raw
def unchanged(pr,intake):
    p=intake['PR_metadata'];need(pr['number']==205 and pr['head']['sha']==HEAD and pr['head']['ref']=='dot/math-5100030' and pr['base']['ref']=='main' and pr['state']=='open' and pr['draft'] is True and pr['merged'] is False,'Original PR identity/state')
    for k in ('title','body','created_at','updated_at','commits','changed_files'):need(pr[k]==p[k],'Original metadata changed '+k)
def main():
    raw=(A/INTAKE).read_bytes();need(pin(raw)==INTAKE_PIN,'Root status intake pin');intake=json.loads(raw)
    need(intake['PR']==205 and str(intake['problem_id'])=='5100030' and intake['original_head']==HEAD and intake['original_status']=='claimed_solved','Original eligibility')
    pr=api('pulls/205');unchanged(pr,intake);listed=api('pulls/205/commits?per_page=100');need(len(listed)==pr['commits']==3,'Original author commit count')
    chain=[];current=HEAD
    for unused in listed:
        c=api('git/commits/'+current);need(c['sha']==current and len(c['parents'])==1,'Original linear single-parent chain');chain.append(c);current=c['parents'][0]['sha']
    base=api('git/commits/'+current);need(base['sha']==current and [c['sha'] for c in reversed(chain)]==[c['sha'] for c in listed],'Exact original range base/chain');co=chain[0]
    root=lookup(co['tree']['sha'],NATIVE.rstrip('/'));need(root is not None and root['type']=='tree','Original native attempt root');files=walk(root['sha']);changes=delta(base['tree']['sha'],co['tree']['sha'])
    need(set(changes)=={Q}|{NATIVE+n for n in files} and len(changes)==pr['changed_files']==18,'Complete original delta contains unexpected path')
    qb=blob(lookup(base['tree']['sha'],Q));qh=blob(lookup(co['tree']['sha'],Q));need(bpin(qh)['git_blob']==intake['original_QUEUE_blob'],'Root original QUEUE blob identity')
    old,new=qb.splitlines(keepends=True),qh.splitlines(keepends=True);need(len(old)==len(new),'Original QUEUE line count');different=[i for i,(x,y) in enumerate(zip(old,new)) if x!=y];need(len(different)==1,'Original foreign QUEUE lines changed');i=different[0]
    marker=b'| 5100030 / AMR-050-0030 |';need(sum(marker in x for x in old)==sum(marker in x for x in new)==1 and marker in old[i] and marker in new[i],'Original own QUEUE identity')
    bc,hc=old[i].decode().rstrip('\n').split('|'),new[i].decode().rstrip('\n').split('|');need(len(bc)==len(hc)==14 and bc[:8]==hc[:8] and (hc[8].strip(),hc[9].strip())==('claimed_solved','1/5') and new[i].decode()==intake['original_QUEUE_row'],'Original BASE/HEAD row custody')
    with ThreadPoolExecutor(max_workers=4) as pool:bodies=dict(zip(files,pool.map(blob,files.values())))
    unchanged(api('pulls/205'),intake);need(pin((A/INTAKE).read_bytes())==INTAKE_PIN,'Root intake changed during custody')
    pins={}
    for name,body in bodies.items():
        need(not Path(name).is_absolute() and '..' not in Path(name).parts,'Original relative archive path');save(A/'original_submitted_head'/name,body);pins[name]={**bpin(body),'mode':files[name]['mode']}
    meta={k:pr[k] for k in ('number','title','body','state','draft','merged','created_at','updated_at','commits','changed_files')};meta.update(original_head=HEAD,original_branch=pr['head']['ref'],base_ref=pr['base']['ref'])
    save(A/'ORIGINAL_PR_METADATA.json',enc(meta));save(A/'original_git_metadata/ORIGINAL_COMMIT.json',enc(co));save(A/'original_git_metadata/RANGE_BASE_COMMIT.json',enc(base));save(A/'original_git_metadata/ORIGINAL_LINEAR_CHAIN.json',enc(chain));save(A/'original_git_metadata/ALL_AUTHENTICATED_NONRECURSIVE_TREES.json',enc(TREES))
    qr={'UTC':now(),'range_base':base['sha'],'original_head':HEAD,'base_QUEUE_blob':bpin(qb),'original_QUEUE_blob':bpin(qh),'base_own_row':{**bpin(old[i]),'text':old[i].decode()},'original_QUEUE_row':{**bpin(new[i]),'text':new[i].decode()},'BASE_status':bc[8].strip(),'BASE_effort':bc[9].strip(),'HEAD_status':hc[8].strip(),'HEAD_effort':hc[9].strip(),'one_based_row':i+1,'foreign_QUEUE_rows_identical':True,'own_only_changed_row':True,'BASE_preimage_is_distinct_from_submitted_HEAD':old[i]!=new[i],'all_queue_bytes_retrievable_by_immutable_native_blob_ID':True};save(A/'ORIGINAL_QUEUE_SINGLE_ROW_RECEIPT.json',enc(qr))
    r={'UTC':now(),'PR':205,'problem_id':5100030,'original_head':HEAD,'original_tree':co['tree']['sha'],'original_sole_parent':co['parents'][0]['sha'],'original_range_base':base['sha'],'original_range_base_tree':base['tree']['sha'],'original_author_commit_count':3,'original_QUEUE_status':hc[8].strip(),'original_QUEUE_effort_cell':hc[9].strip(),'BASE_QUEUE_status':bc[8].strip(),'BASE_QUEUE_effort_cell':bc[9].strip(),'files':pins,'file_count':len(pins),'total_native_bytes':sum(map(len,bodies.values())),'complete_original_delta':changes,'complete_delta_is_exact_native_archive_plus_one_QUEUE_row':True,'foreign_QUEUE_rows_unchanged_at_original_submission':True,'original_QUEUE_blob':bpin(qh),'original_QUEUE_row':pin(new[i]),'BASE_QUEUE_row':pin(old[i]),'Root_status_intake_pin':INTAKE_PIN,'original_PR_metadata':pin((A/'ORIGINAL_PR_METADATA.json').read_bytes()),'authenticated_nonrecursive_trees':len(TREES),'all_nonrecursive_Git_tree_native_identities_verified':True,'all_blob_native_identities_and_bytes_verified':True,'mathematical_clearance':False,'priority_clearance':False,'no_PR_or_native_MAIN_mutation':True,'custody_before_semantic_candidate_review':True,'case_completion_estimate_percent':10,'transport':'Authenticated exact-SHA native Git tree/blob GETs only; native tree/blob SHA1 and byte SHA256/size recomputed; no local Git commands.'};save(A/'ORIGINAL_SUBMISSION_CUSTODY.json',enc(r))
    save(D/'RESEARCH_LOG.md',('# PR205 original custody\n\n'+r['UTC']+' — Complete original immutable byte custody and own-only BASE-to-HEAD QUEUE delta authenticated. Archive available for independent families. Operational intake estimate10%; mathematics and priority NOT CLEARED. No favorable review adopted, publication, native/ref/PR/service mutation or206 intake.\n').encode())
    print(json.dumps({k:r[k] for k in ('UTC','PR','original_head','original_tree','original_sole_parent','original_range_base','file_count','total_native_bytes','authenticated_nonrecursive_trees','mathematical_clearance','priority_clearance')}))
if __name__=='__main__':main()
