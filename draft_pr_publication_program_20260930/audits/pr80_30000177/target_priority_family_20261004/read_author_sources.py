import datetime, hashlib, json, pathlib
root=pathlib.Path(__file__).resolve().parent
source=root.parent/'original_source_authentication_20261004'/'original_head'/'unsolved_math_prioritization'/'attempts'/'30000177'/'SOURCES.md'
b=source.read_bytes()
record={'first_read_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(), 'path':str(source), 'bytes':len(b), 'sha256':hashlib.sha256(b).hexdigest(), 'git_blob_sha1':hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest(), 'first_priority_pin_preexists':(root/'FIRST_PRIORITY_PIN.json').exists(), 'sibling_conclusions_read':False}
(root/'AUTHOR_SOURCES_AUTH.json').write_text(json.dumps(record,indent=2)+'\n')
(root/'private'/'AUTHOR_SOURCES.md').write_bytes(b)
print(json.dumps(record))
