"""Finalize a small own SOURCE manifest only; never import or execute compressor."""
import ast,datetime,hashlib,json,os,sys
from pathlib import Path
N=Path(__file__).absolute().parent
def sha(b):return hashlib.sha256(b).hexdigest()
def ref(p):
    b=p.read_bytes();return dict(path=str(p.relative_to(N)),bytes=len(b),sha256=sha(b),full_mode=p.stat().st_mode&0o7777)
def main():
    assert __debug__
    for p in N.glob('*.py'):ast.parse(p.read_bytes(),filename=p.name)
    d=json.loads((N/'DERIVATION.json').read_bytes())
    assert sha((N/'compress_checkpoint1915.py').read_bytes())==d['proposed_source']['sha256']
    assert sha((N/'INPUT_PINS.json').read_bytes())==d['input_pins_sha256']
    for dirname in ['inventory_actual_capture','inventory_corrected_actual_capture','preparation_actual_capture']:
        q=N/dirname;j=json.loads((q/'CAPTURE.json').read_bytes());assert j['actual_execution'] and j['completed'] and j['exit_code']==0 and j['compression_executed'] is False
        for k in ['prelaunch_operator','prelaunch_controller','stdout','stderr']:
            z=j[k];p=Path(z['path']);a=ref(p);assert all(a[t]==z[t] for t in ['bytes','sha256','full_mode'])
    now=datetime.datetime.now(datetime.timezone.utc).isoformat()
    with (N/'RESEARCH_LOG.md').open('ab') as f:
        f.write(('\n'+now+' — Actual own SOURCE finalizer'+str(os.getpid())+' verified all current source hashes, input pins and retained administrative captures. Preparation100% at SOURCE_READY; compressor unexecuted, compression0%, discovery0%, formal program37/180 (20.56%). ROOT personal read and actual execution remain pending.\n').encode());f.flush();os.fsync(f.fileno())
    rows=[ref(p) for p in sorted(N.rglob('*')) if p.is_file()]
    record=dict(schema='checkpoint1915-index-compression-SOURCE-ready/v1',source_only=True,actual_preparer_pid=os.getpid(),utc=now,argv=sys.argv,
      files=rows,source_ready_literal_self_exclusion='SOURCE_READY.json',directories=[dict(path=str(p.relative_to(N)),full_mode=p.stat().st_mode&0o7777) for p in [N]+sorted(q for q in N.rglob('*') if q.is_dir())],
      helper_sha256=d['proposed_source']['sha256'],input_pins_sha256=d['input_pins_sha256'],source_preparation_percent=100,
      compression_executed=False,ROOT_approval=False,targets=['checkpoint1915-private','checkpoint1915-reconciled'],logical_target_bytes=48078150,allocated_target_bytes=48082944,
      original_checkpoint_and_V4_unchanged=True,live_git_index_ineligible=True,new_discovery=0,formal_completed_acceptance='37/180')
    with (N/'SOURCE_READY.json').open('xb') as f:f.write((json.dumps(record,indent=2,sort_keys=True)+'\n').encode());f.flush();os.fsync(f.fileno())
    print(json.dumps(dict(status='SOURCE_READY_UNEXECUTED_COMPRESSOR',actual_pid=os.getpid(),ready=ref(N/'SOURCE_READY.json'),files_including_ready=len(rows)+1,helper_sha256=record['helper_sha256'],input_pins_sha256=record['input_pins_sha256'])))
if __name__=='__main__':main()
