"""Read-only current metadata evidence using authenticated non-main helpers."""
import datetime
import hashlib
import json
import os
from pathlib import Path
import runpy
import stat
import sys

N=Path(__file__).absolute().parent
S=N.parent
P=S.parent
A45=P/'audits/pr45_9900007'
CASES=[
 ('checkpoint1915-private','checkpoint1915-private_4307x_rt',43975,'root_checkpoint1915_private_compression_actual_capture','checkpoint1915_preparation/compress_checkpoint1915.py','5333c9b78f4221c3e41b0360e5101269bee0f25bcd8320c209015b8bbc717990','9a1e6a5986329c96933f5b439489d09053d63037f4dae15dd65f7ffad8ae7c38'),
 ('checkpoint1915-reconciled','checkpoint1915-reconciled_a2exeqna',44225,'root_checkpoint1915_reconciled_compression_actual_capture','checkpoint1915_preparation/compress_checkpoint1915.py','5333c9b78f4221c3e41b0360e5101269bee0f25bcd8320c209015b8bbc717990','b614e4b1c3f594c10852fb52e1fa05cade94a1e462ab6c2dfc231a4a3a41185c'),
]
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def sha(b):return hashlib.sha256(b).hexdigest()
def need(v,m):
 if not v:raise RuntimeError(m)
def ref(q):
 need(q.is_file()and not q.is_symlink()and not any(v.is_symlink()for v in q.parents),'Regular exact source')
 s=q.stat();b=q.read_bytes();t=q.stat()
 need((s.st_ino,s.st_size,s.st_mode,s.st_mtime_ns,s.st_ctime_ns)==(t.st_ino,t.st_size,t.st_mode,t.st_mtime_ns,t.st_ctime_ns),'Source changed while reading')
 return dict(path=str(q),bytes=len(b),sha256=sha(b),full_mode_07777=oct(stat.S_IMODE(s.st_mode)))
def save(name,value):
 b=(json.dumps(value,sort_keys=True,indent=2)+'\n').encode()
 with(N/name).open('xb')as f:f.write(b);f.flush();os.fsync(f.fileno())
 return b

def main():
 need(__debug__,'No optimized preparer readback')
 started=now();rows=[];failed=False
 for key,directory,pid,capname,helpername,helpersha,receiptsha in CASES:
  ns=None;row=dict(target_name=key,actual_original_compressor_pid=pid,readback_started_utc=now())
  try:
   helper=S/helpername;receiptfile=S/directory/'receipt.json';receipt=json.loads(receiptfile.read_bytes())
   receipt_before=ref(receiptfile);helper_before=ref(helper);prelaunch=ref(S/directory/'helper.prelaunch.py')
   need(receipt_before['sha256']==receiptsha and helper_before['sha256']==prelaunch['sha256']==helpersha==receipt['helper_sha256'],'Exact actual receipt and reviewed executed helper')
   need(receipt['status']=='COMPRESSED'and receipt['source_replaced']is True and receipt['operator_pid']==pid,'Genuine completed compression')
   capfile=A45/capname/'CAPTURE.json';cap=json.loads(capfile.read_bytes());caprefs=[ref(v)for v in sorted(capfile.parent.iterdir())if v.is_file()]
   need({Path(v['path']).name for v in caprefs}=={'CAPTURE.json','prelaunch_operator.py','stdout.bin','stderr.bin'},'Exact genuine ROOT CAP4')
   need(cap['pid']==pid and cap['actual_execution']and cap['completed']and cap['exit_code']==0 and cap['operator_unchanged'],'Actual ROOT compression CAP')
   need(str(helper)in cap['argv']and key in cap['argv'],'Exact operator and target argv')
   need(ref(capfile.parent/'prelaunch_operator.py')['sha256']==cap['operator_sha256'],'Actual ROOT capture operator source')
   for kind in ['stdout','stderr']:
    z=ref(capfile.parent/(kind+'.bin'));need(z['sha256']==cap[kind]['sha256']and z['bytes']==cap[kind]['bytes'],'Complete genuine ROOT stream')
   # The custom run name prevents the guarded production main from executing.
   # Only the fully reviewed helper's bounded readonly snapshot functions run.
   ns=runpy.run_path(str(helper),run_name='PREPARER_READONLY_STORAGE_SNAPSHOT_NOT_MAIN')
   need(ns['__name__']!='__main__'and ns['commands']==[],'No production main invoked during import')
   target=Path(receipt['target']);need(ns['ALLOW'][key]==target and target.is_relative_to(P),'Exact already-completed own allowed target')
   need('.git'not in target.parts,'No live Git index')
   current=ns['snapshot'](target,receipt['before']['xattrs'])
   observed=ns['identity'](current);expected=ns['identity'](receipt['after'])
   row.update(current_snapshot=current,complete_native_readonly_commands=ns['commands'],receipt_after_identity=expected,
              identity_excludes_only_st_atime_ns=True,readback_matches=observed==expected)
   need(observed==expected,'Current logical body/full metadata differs from receipt.after')
   need(current['sha256']==receipt['before']['sha256'],'Original logical body preserved')
   need(ref(receiptfile)==receipt_before and ref(helper)==helper_before and ref(S/directory/'helper.prelaunch.py')==prelaunch,'Receipt/helper exact bytes and modes unchanged')
   need([ref(Path(v['path']))for v in caprefs]==caprefs,'Whole original ROOT CAP4 unchanged')
   row.update(status='PASS_PREPARER_READONLY_CURRENT_RECEIPT_IDENTITY',receipt=receipt_before,executed_prelaunch_helper=prelaunch,
              reviewed_current_helper=helper_before,original_ROOT_CAP4=caprefs,actual_original_saved_allocated_bytes=receipt['saved_allocated_bytes'],
              original_receipt_bytes_and_mode_unchanged=True,original_target_logical_bytes_full07777_uidgid_mtime_flags_xattrs_ACL_bound=True,
              compression_bookkeeping_compact_hashes_only=True,readback_finished_utc=now())
  except BaseException as exc:
   failed=True;row.update(status='FAIL_PREPARER_READBACK_NO_APPROVAL',error=repr(exc),readback_finished_utc=now(),
                         complete_native_readonly_commands=[]if ns is None else ns['commands'])
  rows.append(row)
 result=dict(schema='checkpoint1915-compression-preparer-readonly-readback/v1',actual_preparer_pid=os.getpid(),argv=sys.argv,
             started_utc=started,finished_utc=now(),status='FAIL'if failed else'PASS_BOTH_CHECKPOINT1915_READBACKS',cases=rows,
             substantive_current_checks=sum(z['status'].startswith('PASS_')for z in rows),ROOT_personal_readback_or_approval=False,
             production_main_compression_Git_native_campaign_remote_executed=False,no_original_receipt_or_target_rewrite=True,
             only_atime_excluded_from_receipt_after_identity=True,no_huge_xattrs_or_target_bodies_copied=True)
 body=save('RESULT.json',result);print(body.decode(),end='')
 need(not failed,'Readback failure preserved; no ROOT approval inferred')

if __name__=='__main__':main()
