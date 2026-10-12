"""Derive only a two-case readonly reader from the reviewed readback mechanism."""
from pathlib import Path
import difflib,hashlib,json,os,datetime
N=Path(__file__).absolute().parent;S=N.parent
old=S/'metadata_readback_v4_v3_final_20261003/readback_only.py'
source=old.read_bytes();assert hashlib.sha256(source).hexdigest()=='fe0a820d986969cbb044e3304ca72d62ade151689139a6be07597d850a80f876'
s=source.decode();start=s.index('CASES=[');end=s.index('\n]\n',start)+3
cases="""CASES=[
 ('checkpoint1915-private','checkpoint1915-private_4307x_rt',43975,'root_checkpoint1915_private_compression_actual_capture','checkpoint1915_preparation/compress_checkpoint1915.py','5333c9b78f4221c3e41b0360e5101269bee0f25bcd8320c209015b8bbc717990','9a1e6a5986329c96933f5b439489d09053d63037f4dae15dd65f7ffad8ae7c38'),
 ('checkpoint1915-reconciled','checkpoint1915-reconciled_a2exeqna',44225,'root_checkpoint1915_reconciled_compression_actual_capture','checkpoint1915_preparation/compress_checkpoint1915.py','5333c9b78f4221c3e41b0360e5101269bee0f25bcd8320c209015b8bbc717990','b614e4b1c3f594c10852fb52e1fa05cade94a1e462ab6c2dfc231a4a3a41185c'),
]
"""
s=s[:start]+cases+s[end:]
s=s.replace('storageV4-and-finalV3-preparer-readonly-readback/v1','checkpoint1915-compression-preparer-readonly-readback/v1')
s=s.replace('PASS_ALL_FIVE_PREPARER_READBACKS','PASS_BOTH_CHECKPOINT1915_READBACKS')
s=s.replace('production_main_compression_Git_native_remote_executed=False','production_main_compression_Git_native_campaign_remote_executed=False')
with (N/'readback_only.py').open('xb') as f:f.write(s.encode());f.flush();os.fsync(f.fileno())
diff=''.join(difflib.unified_diff(source.decode().splitlines(True),s.splitlines(True),fromfile='reviewed-readback/readback_only.py',tofile='checkpoint1915/readback_only.py'))
with (N/'READER_DERIVATION.diff').open('xb') as f:f.write(diff.encode());f.flush();os.fsync(f.fileno())
record=dict(actual_source_preparer_pid=os.getpid(),utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
 source=str(old),source_sha256=hashlib.sha256(source).hexdigest(),reader_sha256=hashlib.sha256(s.encode()).hexdigest(),
 changes='Exact two cases and result naming only; bounded non-main snapshot/identity/authentication/error-custody mechanism unchanged.',
 compression_executed=False,ROOT_approval=False)
with (N/'DERIVATION.json').open('xb') as f:f.write((json.dumps(record,indent=2,sort_keys=True)+'\n').encode());f.flush();os.fsync(f.fileno())
print(json.dumps(record))
