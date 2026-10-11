from pathlib import Path
import datetime, hashlib, json, os, sys
A=Path(__file__).resolve().parent;folder=A/sys.argv[1];expected=sys.argv[2]
def require(ok,msg):
    if not ok:raise RuntimeError(msg)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
manifest=folder/'CLOSED_MANIFEST.json';require(sha(manifest)==expected,'closed manifest pin')
x=json.loads(manifest.read_text());seen=set()
for e in x['files']:
    rel=Path(e['file']);require(not rel.is_absolute() and '..' not in rel.parts,'safe relative entry')
    require(e['file'] not in seen,'duplicate entry');seen.add(e['file'])
    p=folder/rel;require(p.is_file() and p.stat().st_size==e['bytes'] and sha(p)==e['sha256'],'entry byte pin '+str(rel))
r={'schema':'pr95-root-whole-review-byte-authentication/v1','UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'actual_operator_PID':os.getpid(),'folder':folder.name,'closed_manifest_sha256':sha(manifest),
    'files_verified':len(seen),'reported_verdict':x['verdict'],'priority_clearance':False,
    'publication_clearance':False,'reports_read_by_ROOT':True,'report_sha256':sha(folder/'REPORT.md')}
(A/('ROOT_AUTHENTICATED_'+folder.name+'.json')).write_text(json.dumps(r,indent=2)+'\n')
print(json.dumps(r))
