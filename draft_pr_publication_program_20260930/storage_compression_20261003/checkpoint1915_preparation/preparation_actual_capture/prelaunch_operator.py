"""Derive two-target unexecuted SOURCE from reviewed V4; no compressor import or run."""
import ast,datetime,difflib,hashlib,json,os,stat
from pathlib import Path
N=Path(__file__).absolute().parent;B=N.parent;P=B.parent
V4=B/'v4_preparation/compress_completed_v4.py'
V4_SHA='742e3d70824fb8c79d0b11c653c9d904633df52bce3b3c1010af93761d6b9579'
def sha(b):return hashlib.sha256(b).hexdigest()
def put(p,b):
    with p.open('xb') as f:f.write(b);f.flush();os.fsync(f.fileno())
def enc(v):return (json.dumps(v,indent=2,sort_keys=True)+'\n').encode()
def replace(s,a,b):
    assert s.count(a)==1,(a,s.count(a));return s.replace(a,b)
def main():
    assert __debug__ and N.name=='checkpoint1915_preparation'
    inv=N/'inventory_corrected_actual_capture/stdout.json';data=inv.read_bytes();assert sha(data)=='18bdcbb033749abc88549d7ff60357b724c4ae7368c9dd978022e1cb7461f586'
    j=json.loads(data);assert j['pid']==39178 and j['compression_executed'] is False
    pins={}
    for key,z in j['candidates'].items():
        f=Path(z['path']);before=f.lstat();h=hashlib.sha256()
        with f.open('rb') as stream:
            for b in iter(lambda:stream.read(1048576),b''):h.update(b)
        after=f.lstat();assert not f.is_symlink() and stat.S_ISREG(after.st_mode) and h.hexdigest()==z['sha256']
        assert all(getattr(before,k)==getattr(after,k)==v for k,v in z['stat'].items() if k!='st_atime_ns')
        pins[key]={k:z[k] for k in ['path','stat','sha256','xattrs','acl_base64']}
    pb=enc(pins);put(N/'INPUT_PINS.json',pb)
    original=V4.read_bytes();assert sha(original)==V4_SHA;s=original.decode()
    s=replace(s,'UNEXECUTED V4 SOURCE: two authenticated completed private checkpoint indexes; actual V2 pilot required.',
              'UNEXECUTED checkpoint1915 SOURCE: completed private/reconciled saved copies only; actual V2 pilot required.')
    s=replace(s,"PINS_SHA = '33c9b858153f5162f5c853a7f7a2fae7589666eb1237affd75127656266db202'","PINS_SHA = '"+sha(pb)+"'")
    old="""    'checkpoint1745-private': PROGRAM / 'checkpoints/checkpoint_20261003_1745_preparation/actual_run_20261003_181833/PRIVATE_CHECKPOINT_INDEX',
    'checkpoint1530-private': PROGRAM / 'checkpoints/checkpoint_20261003_1530_preparation/actual_run_20261003_1631/PRIVATE_CHECKPOINT_INDEX',"""
    new="""    'checkpoint1915-private': PROGRAM / 'checkpoints/checkpoint_20261003_1915_preparation/actual_run_root1915/PRIVATE_CHECKPOINT_INDEX',
    'checkpoint1915-reconciled': PROGRAM / 'checkpoints/checkpoint_20261003_1915_preparation/actual_run_root1915/RECONCILED_REAL_INDEX',"""
    s=replace(s,old,new)
    s=replace(s,"BASE / 'v4_preparation/compress_completed_v4.py'","BASE / 'checkpoint1915_preparation/compress_checkpoint1915.py'")
    s=replace(s,'BASE / "v4_preparation/V4_INPUT_PINS.json"','BASE / "checkpoint1915_preparation/INPUT_PINS.json"')
    body=s.encode();ast.parse(body);put(N/'compress_checkpoint1915.py',body)
    diff=''.join(difflib.unified_diff(original.decode().splitlines(True),s.splitlines(True),fromfile='reviewedV4/compress_completed_v4.py',tofile='checkpoint1915/compress_checkpoint1915.py'));put(N/'SOURCE.diff',diff.encode())
    record=dict(schema='checkpoint1915-index-compression-SOURCE-derivation/v1',actual_preparer_pid=os.getpid(),utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
      V4_source=dict(path=str(V4),bytes=len(original),sha256=V4_SHA),actual_readonly_inventory=dict(path=str(inv),bytes=len(data),sha256=sha(data),actual_pid=39178),
      proposed_source=dict(path=str(N/'compress_checkpoint1915.py'),bytes=len(body),sha256=sha(body)),input_pins_sha256=sha(pb),
      substantive_preservation_guards_unchanged=True,changes='Docstring, two allowlist entries, canonical helper pathname, input pin pathname and SHA only.',
      helper_imported_or_executed=False,compression_performed=False,ROOT_read_or_approval_of_this_SOURCE=False)
    put(N/'DERIVATION.json',enc(record));put(N/'CUSTODY.json',enc(dict(completed_checkpoint=j['custody'],live_index_distinction=j['live_index_distinction'],
      reconciled_and_live_stage_entry_tables=j['reconciled_and_live_stage_entry_tables'],reconciled_and_live_stage_entries_equal=j['reconciled_and_live_stage_entries_equal'],
      historical_reconciled_body_equals_later_live_snapshot=False,qualification='Current completed saved copy is freshly bound. Entry-table equality does not imply byte equality or justify touching the live index. No cause for byte difference is asserted.')))
    print(json.dumps(record))
if __name__=='__main__':main()
