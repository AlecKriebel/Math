"""Separate ROOT-only proposed closed-source readback; no source mutation."""
import datetime as dt,json,os,stat,sys
import source_common as c
if __name__=='__main__':
 c.need(sys.argv==[__file__,'--root-readback'],'explicit separate ROOT invocation required');idx,ready,rows=c.verify('closed');f=c.P/'SOURCE_MANIFEST.json';r=c.row(f);c.need(r['full_mode']==292,'manifest mode444');m=json.loads(f.read_bytes());c.need(m['index_sha256']==c.sha((c.P/'INDEX.json').read_bytes()) and m['ready_sha256']==c.sha((c.P/'SOURCE_READY.json').read_bytes()) and m['payloads']==rows and m['actual_pid']!=os.getpid(),'exact independent closed readback');print(json.dumps(dict(status='PASS_SEPARATE_CLOSED_PUBLIC_SOURCE_READBACK_ONLY',actual_pid=os.getpid(),actual_utc=dt.datetime.now(dt.timezone.utc).isoformat(),manifest_sha256=r['sha256'],payload_count=len(rows),scientific_acceptance=False)))
