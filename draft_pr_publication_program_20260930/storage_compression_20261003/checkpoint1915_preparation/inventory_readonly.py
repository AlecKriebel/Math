"""Readonly two completed index copies, bounded custody/metadata and live-index distinction."""
import base64,datetime,hashlib,json,os,stat,subprocess,sys
from pathlib import Path
P=Path('/Users/alec/Documents/Math/draft_pr_publication_program_20260930')
D=P/'checkpoints/checkpoint_20261003_1915_preparation/actual_run_root1915'
TARGETS={'checkpoint1915-private':D/'PRIVATE_CHECKPOINT_INDEX','checkpoint1915-reconciled':D/'RECONCILED_REAL_INDEX'}
FIELDS=('st_dev','st_ino','st_mode','st_nlink','st_uid','st_gid','st_size','st_rdev','st_atime_ns','st_mtime_ns','st_ctime_ns','st_flags','st_blocks','st_blksize','st_birthtime')
def utc():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def stable(s):return {k:v for k,v in s.items() if k!='st_atime_ns'}
def stats(p):
    s=p.lstat();return {k:getattr(s,k) for k in FIELDS}
def digest(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        for b in iter(lambda:f.read(1048576),b''):h.update(b)
    return h.hexdigest()
def ref(p):return dict(path=str(p),bytes=p.stat().st_size,sha256=digest(p),full_mode=stat.S_IMODE(p.stat().st_mode))
record=dict(role='READONLY_INVENTORY_NOT_COMPRESSION',pid=os.getpid(),argv=sys.argv,executable=sys.executable,
            cwd=os.getcwd(),start_utc=utc(),candidates={},commands=[],custody={})
def command(argv,accepted=(0,),hash_only=False,env=None):
    start=utc();c=subprocess.Popen(argv,stdout=subprocess.PIPE,stderr=subprocess.PIPE,env=env);out,err=c.communicate()
    r=dict(argv=argv,pid=c.pid,start_utc=start,end_utc=utc(),exit=c.returncode,stderr_base64=base64.b64encode(err).decode())
    if hash_only:r.update(stdout_bytes=len(out),stdout_sha256=hashlib.sha256(out).hexdigest(),stdout_retained=False,stdout_policy='Complete readonly enumeration returned in memory, not copied')
    else:r['stdout_base64']=base64.b64encode(out).decode()
    record['commands'].append(r);assert c.returncode in accepted,'Readonly child failed'
    return out
for label,pin in [('plan','ee3fa96513119923e71326e318b4e2c0ff273b8b3ba6aa6071bc6d69c0f5f98e'),
                  ('commit','70adc6812c01301ff39d6697f17b3cbb816b0dc6f8528183618d21a1b85d26e5'),
                  ('publication','083083876cf8dfcc65bae5f966bed7b01268c6f1e365e41d50f069a0443de024')]:
    f={'plan':D/'PLAN.json','commit':D/'COMMIT_RECEIPT.json','publication':P/'checkpoints/ROOT_CHECKPOINT_1915_PUBLICATION_20261003.json'}[label]
    assert digest(f)==pin;record['custody'][label]=ref(f)
plan=json.loads((D/'PLAN.json').read_bytes());receipt=json.loads((D/'COMMIT_RECEIPT.json').read_bytes())
pub=json.loads((P/'checkpoints/ROOT_CHECKPOINT_1915_PUBLICATION_20261003.json').read_bytes())
assert plan['actual_stager_pid']==21726 and receipt['actual_committer_pid']==22257
assert receipt['status']=='PASS_LOCAL_EXACT_SCOPE_CHECKPOINT' and pub['status']=='EXACT_OWNED_CHECKPOINT_PUSHED'
assert receipt['commit']==pub['commit']=='08adf9cb444d365fd148a2bb3e2951a7f49c6808'
for op in pub['operations']:
    if op['kind'] not in ['stage','commit','push']:continue
    for z in op['complete_CAP4']:
        f=P.parent/z['path'];assert ref(f)==dict(z,path=str(f))
    cap=json.loads((P.parent/op['complete_CAP4'][0]['path']).read_bytes())
    assert cap['pid']==op['actual_pid'] and cap['completed'] and cap['actual_execution'] and cap['exit_code']==0 and cap['status']=='PASS'
record['custody']['genuine_stage_commit_push_pids']=[21726,22257,22644]
for key,path in TARGETS.items():
    assert path.exists() and not any(q.is_symlink() for q in (path,)+tuple(path.parents))
    before=stats(path);assert stat.S_ISREG(before['st_mode']) and before['st_nlink']==1 and not before['st_flags']&stat.UF_COMPRESSED
    body=digest(path);namesraw=command(['/usr/bin/xattr',str(path)]);assert len(namesraw)<=16384
    names=namesraw.decode().splitlines();assert len(names)<=64 and len(names)==len(set(names));attrs={}
    for name in names:
        out=command(['/usr/bin/xattr','-px',name,str(path)]);assert len(out)<=262144
        value=bytes.fromhex(out.decode('ascii'));assert len(value)<=65536;attrs[name]=base64.b64encode(value).decode()
    acl=command(['/bin/ls','-lde',str(path)]).splitlines()[1:];after=stats(path);assert stable(before)==stable(after)
    record['candidates'][key]=dict(path=str(path),status='ELIGIBLE_STABLE',pre_read_stat=before,stat=after,
      sha256=body,allocated_bytes=after['st_blocks']*512,full_mode=stat.S_IMODE(after['st_mode']),xattrs=attrs,
      acl_base64=[base64.b64encode(v).decode() for v in acl])
    if key=='checkpoint1915-private':assert body==plan['private_index']['sha256'] and after['st_size']==plan['private_index']['bytes']
lsof=command(['/usr/sbin/lsof','-Fpcfatn']+[str(v) for v in TARGETS.values()],(0,1));record['target_lsof_stdout']=base64.b64encode(lsof).decode()
live=Path('/Users/alec/Documents/Math/.git/index');before=stats(live);body=digest(live);after=stats(live);assert stable(before)==stable(after)
record['live_index_distinction']=dict(path=str(live),stat=after,sha256=body,eligible=False,never_modify=True,
     different_inodes=all(z['stat']['st_ino']!=after['st_ino'] for z in record['candidates'].values()),
     reconciled_hash_equals_later_live_receipt=record['candidates']['checkpoint1915-reconciled']['sha256']==receipt['foreign_after']['real_index']['sha256'])
env=os.environ.copy()
for k in list(env):
    if k.startswith('GIT_'):env.pop(k)
env.update(GIT_OPTIONAL_LOCKS='0',GIT_NO_REPLACE_OBJECTS='1',GIT_DIR='/Users/alec/Documents/Math/.git',GIT_WORK_TREE='/Users/alec/Documents/Math')
tables={}
for key,path in [('reconciled',TARGETS['checkpoint1915-reconciled']),('live',live)]:
    e=dict(env,GIT_INDEX_FILE=str(path));out=command(['git','-C','/Users/alec/Documents/Math','ls-files','--stage','-z'],hash_only=True,env=e)
    tables[key]=dict(whole_stage_table_bytes=len(out),whole_stage_table_sha256=hashlib.sha256(out).hexdigest(),entries=sum(bool(v) for v in out.split(b'\0')))
    assert tables[key]['entries']>0,'Whole repository table cannot be empty'
    assert digest(path)==(body if key=='live' else record['candidates']['checkpoint1915-reconciled']['sha256'])
record['reconciled_and_live_stage_entry_tables']=tables
record['reconciled_and_live_stage_entries_equal']=tables['reconciled']==tables['live']
record['end_utc']=utc();record['compression_executed']=False;record['production_helper_imported']=False
print(json.dumps(record,indent=2,sort_keys=True))
