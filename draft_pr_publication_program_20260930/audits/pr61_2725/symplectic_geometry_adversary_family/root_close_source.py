"""SOURCE only. Prepared by agent; run only by ROOT after its own full read."""
import datetime, json, os, sys
from verify_source import BASE, MANIFEST, verify
assert len(sys.argv)==3 and sys.argv[1]=="--ROOT-reviewed-source"
assert not (BASE/MANIFEST).exists()
result = verify(sys.argv[2], closed=False)
result.update(schema="pr61-symplectic-family-source-closure/v1",
    actual_executor_pid=os.getpid(), recorded_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
    argv=sys.argv, caller_role="ROOT explicitly asserted by invocation; not independently inferred",
    source_bytes_closed=True, mathematical_or_publication_approval=False,
    native_acceptance=False, helper_preparation_is_not_execution=True)
body=(json.dumps(result,indent=2)+"\n").encode()
fd=os.open(BASE/MANIFEST,os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o444)
os.fchmod(fd,0o444)
try:
    with os.fdopen(fd,"wb") as f:
        f.write(body)
        f.flush()
        os.fsync(f.fileno())
except BaseException:
    raise  # Preserve partial outcome honestly; no replacement or cleanup.
print(body.decode(),end="")
