"""Separate read-only closed-source reader; prepared but not executed by agent."""
import datetime, json, os, sys
from verify_source import BASE, MANIFEST, verify, sha
assert len(sys.argv)==2
result = verify(sys.argv[1],closed=True)
body=(BASE/MANIFEST).read_bytes()
closed=json.loads(body)
for key in result:
    assert closed[key] == result[key]
assert closed["source_bytes_closed"] is True
assert closed["mathematical_or_publication_approval"] is False
result.update(actual_reader_pid=os.getpid(), recorded_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
    argv=sys.argv, closure_sha256=sha(body), closure_bytes=len(body),
    status="PASS_READ_ONLY_SOURCE_READBACK", native_acceptance=False)
print(json.dumps(result,indent=2))
