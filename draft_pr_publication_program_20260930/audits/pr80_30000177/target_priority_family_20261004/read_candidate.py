import datetime, hashlib, json, pathlib

root = pathlib.Path(__file__).resolve().parent
candidate = root.parent / 'original_source_authentication_20261004' / 'original_head' / 'unsolved_math_prioritization' / 'attempts' / '30000177' / 'CANDIDATE.md'
b = candidate.read_bytes()
assert len(b) == 11679
assert hashlib.sha256(b).hexdigest() == 'fb8646bbe3cd8512ec7736fc180fa08a76740ac8b0dbb60b539a0320328c6404'
assert hashlib.sha1(b'blob ' + str(len(b)).encode() + b'\0' + b).hexdigest() == '7adfc78adb9561d2fdaaa091559de190cf13f673'
record = {
    'first_read_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'candidate_path': str(candidate), 'bytes': len(b),
    'sha256': hashlib.sha256(b).hexdigest(),
    'git_blob_sha1': hashlib.sha1(b'blob ' + str(len(b)).encode() + b'\0' + b).hexdigest(),
    'original_head': 'dcfeb5d8ad68b397ec509c70e85c6fca46cd01e3',
    'first_source_only_preexists': (root/'FIRST_SOURCE_ONLY_PIN.json').exists(),
    'first_priority_preexists': (root/'FIRST_PRIORITY_PIN.json').exists(),
    'sibling_conclusions_read': False, 'author_sources_read': False,
    'supplemental_pre_candidate_reading': ['Bruss2005 lines440-475', 'Song2009 lines75-310', 'Pradhan2007 lines100-165 and1075-1145', 'LocalSubentropy2006 lines145-255']
}
(root/'CANDIDATE_AUTH.json').write_text(json.dumps(record, indent=2)+'\n')
(root/'private'/'CANDIDATE.md').write_bytes(b)
print(json.dumps(record))
