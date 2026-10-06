"""Physically seal the prepared namespace; report actual observed modes."""
import datetime, hashlib, json, os, pathlib, stat, sys
root=pathlib.Path(__file__).resolve().parent
def utc(): return datetime.datetime.now(datetime.timezone.utc).isoformat()
start=utc()
if sys.flags.optimize:
    raise RuntimeError('optimization is not allowed')
paths=list(root.rglob('*'))
if any(p.is_symlink() for p in paths):
    raise RuntimeError('unexpected symlink in namespace')
files=sorted(p for p in paths if p.is_file())
dirs=sorted((p for p in paths if p.is_dir()),key=lambda p:len(p.parts),reverse=True)
receipt=root/'PHYSICAL_SEAL_RESULT.json'
if receipt not in files:
    raise RuntimeError('wrapper did not prepare seal receipt')
# The descriptor is intentionally acquired before chmod and is closed below.
with receipt.open('wb') as out:
    for p in files:
        os.chmod(p,0o444)
    for p in dirs:
        os.chmod(p,0o555)
    os.chmod(root,0o555)
    file_modes={str(p.relative_to(root)):format(stat.S_IMODE(p.stat().st_mode),'04o') for p in files}
    dir_modes={str(p.relative_to(root)):format(stat.S_IMODE(p.stat().st_mode),'04o') for p in dirs}
    dir_modes['.']=format(stat.S_IMODE(root.stat().st_mode),'04o')
    if set(file_modes.values())!={'0444'} or set(dir_modes.values())!={'0555'}:
        raise RuntimeError('physical mode verification failed')
    result=dict(actual_pid=os.getpid(),argv=sys.argv,cwd=os.getcwd(),started_utc=start,
                verified_utc=utc(),files=len(files),directories_including_root=len(dir_modes),
                file_mode='0444',directory_mode='0555',all_actual_modes_verified=True,
                receipt_descriptor_note='opened before chmod and closed after writing this observed result')
    out.write((json.dumps(result,indent=2)+'\n').encode())
    out.flush(); os.fsync(out.fileno())
print(json.dumps(result))
