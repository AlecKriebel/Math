"""ROOT-only proposed absent-manifest custody closer. No scientific acceptance is inferred."""
import datetime as dt,json,os,sys
import source_common as c
if __name__=='__main__':
 c.need(sys.argv==[__file__,'--root-reviewed-source'],'explicit ROOT reviewed-source invocation required')
 c.need(not (c.P/'SOURCE_MANIFEST.json').exists() and not (c.P/'SOURCE_MANIFEST.json').is_symlink(),'manifest must be absent')
 idx,ready,rows=c.verify('prepared')
 for z in rows:os.chmod(c.P/z['path'],0o444)
 os.chmod(c.P/'INDEX.json',0o444);os.chmod(c.P/'SOURCE_READY.json',0o444)
 for z in sorted(idx['directories'],key=lambda z:len(z['path']),reverse=True):os.chmod(c.P/z['path'],0o555)
 idx,ready,rows=c.verify('closed')
 body=(json.dumps(dict(schema='pr18-priority-revisit-public-source-custody/v1',actual_pid=os.getpid(),actual_argv=sys.argv,actual_utc=dt.datetime.now(dt.timezone.utc).isoformat(),index_sha256=c.sha((c.P/'INDEX.json').read_bytes()),ready_sha256=c.sha((c.P/'SOURCE_READY.json').read_bytes()),payload_count=len(rows),payloads=rows,scientific_acceptance=False,new_mathematical_review_credit=0,private_cache_excluded=True),indent=2)+'\n').encode()
 # Temporarily permit the single absent manifest creation; no other file is written.
 os.chmod(c.P,0o755)
 try:
  fd=os.open(c.P/'SOURCE_MANIFEST.json',os.O_CREAT|os.O_EXCL|os.O_WRONLY,0o444)
  with os.fdopen(fd,'wb') as f:f.write(body);f.flush();os.fsync(f.fileno())
  os.chmod(c.P/'SOURCE_MANIFEST.json',0o444)
 finally:os.chmod(c.P,0o555)
 c.verify('closed');print(json.dumps(dict(status='PASS_PUBLIC_SOURCE_CUSTODY_ONLY',actual_pid=os.getpid(),manifest_sha256=c.sha(body),payload_count=len(rows))))
