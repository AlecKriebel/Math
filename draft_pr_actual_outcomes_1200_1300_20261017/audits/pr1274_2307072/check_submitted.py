"""Authenticate current original packet and check only observable editorial ranges."""
import datetime, hashlib, json, pathlib

A=pathlib.Path(__file__).resolve().parent
def sha(b): return hashlib.sha256(b).hexdigest()
def need(ok,label):
    if not ok: raise ValueError(label)
s=json.loads((A/'SUBMITTED_SNAPSHOT.json').read_text())
rows=[]
for r in s['files']:
    b=(A/r['local_path']).read_bytes()
    need(len(b)==r['bytes'] and sha(b)==r['sha256'],r['path'])
    need(hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==r['git_blob_sha1'],'git blob')
    need((A/'current_edition'/pathlib.PurePosixPath(r['path']).name).read_bytes()==b,'edition mismatch')
    rows.append(r['path'])
m=json.loads((A/'submitted/PUBLIC_MANIFEST.json').read_text())
need(m['file_count']==len(s['files'])==6,'packet count')
need({r['path'] for r in m['files']}|{'PUBLIC_MANIFEST.json'}=={pathlib.PurePosixPath(p).name for p in rows},'membership')
for r in m['files']:
    b=(A/'submitted'/r['path']).read_bytes()
    need(len(b)==r['bytes'] and sha(b)==r['sha256'],'public manifest pin')
e=json.loads((A/'submitted/EDITORIAL_MAP.json').read_text())
counts=dict(output_pins=0,replacements=0,unchanged_ranges=0,protected_ranges=0)
for art in e['artifacts']:
    b=(A/'submitted'/art['output']['path']).read_bytes()
    need(len(b)==art['output']['bytes'] and sha(b)==art['output']['sha256'],'editorial output')
    counts['output_pins']+=1
    for r in art['operations']:
        v=b[r['output_start']:r['output_end']]
        need(v==r['replacement_utf8'].encode() and sha(v)==r['replacement_sha256'],'replacement output')
        need(r['input_end']-r['input_start']==r['removed_bytes'],'removed length metadata')
        counts['replacements']+=1
    for key,label in [('unchanged_ranges','unchanged_ranges'),('protected_mathematical_regions','protected_ranges')]:
        for r in art.get(key,[]):
            v=b[r['output_start']:r['output_end']]
            need(len(v)==r['bytes'] and sha(v)==r['sha256'],label)
            need(r['input_end']-r['input_start']==r['bytes'],'input range metadata')
            counts[label]+=1
print(json.dumps(dict(at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),status='PASS',
    original_files=len(rows),public_manifest_nonself_files=len(m['files']),editorial_observable_checks=counts,
    historical_input_scope='Historical AUDIT input body absent from captured original packet: removed bytes/whole transformation not independently replayed. Output substrings and original Git pins were checked, not inferred input history.'),indent=2))
