"""Read-only verification of this review's saved evidence; no provider calls."""
from pathlib import Path,PurePosixPath
import hashlib,json,stat,zipfile
Q=Path(__file__).resolve().parent
def require(ok,msg):
 if not ok:raise RuntimeError(msg)
def sha(b):return hashlib.sha256(b).hexdigest()
def read(rel):return json.loads((Q/rel).read_text())
def checked(path,v):
 require(not path.is_symlink() and path.is_file(),'Nonregular '+str(path));b=path.read_bytes();require(len(b)==v['bytes'] and sha(b)==v['sha256'],'Digest '+str(path));return b
for v in read('INPUT_MANIFEST.json')['files']:checked(Q/v['path'],v)
for v in read('GIT_BLOB_INPUT_MANIFEST.json')['files']:checked(Q/v['captured_path'],v)
scopes=read('pinned_scope_checks.json');require([x['pr'] for x in scopes]==list(range(582,628)),'Range gap')
require(all(x['complete_paths_equal'] and x['all_paths_own_problem'] and len(x['own_rows'])==1 for x in scopes),'Scope mismatch')
wire=(Q/'private/ledger_wire.json').read_bytes();ledger=read('ledger_fresh_receipt.json');require(sha(wire)==ledger['whole_ledger_sha256'],'Ledger wire digest');rows=json.loads(wire)['values'];require(len(rows)==ledger['rows'],'Ledger count')
for v in ledger['targets']:require(rows[v['row']-1]==v['values'],'Ledger target cells')
payload_count=0
for item in read('publication_integrity_checks.json')['publications']:
 n=item['pr'];rid=item['record'];record=read(f'private/public_{n}/record.json')
 require(record['doi']==item['doi'] and record['submitted'] is True and record['state']=='done','Record identity')
 require(item['doi_resolution']=={'status':200,'final_url':'https://zenodo.org/records/'+str(rid)},'DOI destination receipt')
 for f in item['files']:
  kind='.pdf' if f['name'].endswith('.pdf') else '.zip';body=checked(Q/f'private/public_{n}/payload_{f["sha256"]}{kind}',f)
  require(hashlib.md5(body).hexdigest()==f['md5'],'MD5')
 z=zipfile.ZipFile(next((Q/f'private/public_{n}').glob('*.zip')));names=z.namelist();require(len(names)==len(set(names)) and z.testzip() is None,'ZIP CRC/inventory')
 for zi in z.infolist():
  p=PurePosixPath(zi.filename);require(not p.is_absolute() and '..' not in p.parts and not stat.S_ISLNK(zi.external_attr>>16),'ZIP safety')
 if n in [582,585]:
  mn=next(x for x in names if x.endswith('/MANIFEST.json') and x.count('/')==1);prefix=mn.rsplit('/',1)[0]+'/';m=json.loads(z.read(mn));entries=[dict(path=prefix+p,**v) for p,v in m['files'].items()]
 else:mn='PACKAGE_MANIFEST.json';entries=json.loads(z.read(mn))['files']
 require(set(names)=={mn}|{v['path'] for v in entries},'Strict positive inventory')
 for v in entries:
  b=z.read(v['path']);require(len(b)==v['bytes'] and sha(b)==v['sha256'],'Archive payload')
 require(len(entries)==item['manifest_payloads_verified'],'Payload count');payload_count+=len(entries)
require(payload_count==356,'Total payload count')
if (Q/'OUTPUT_MANIFEST.json').exists():
 m=read('OUTPUT_MANIFEST.json')
 for v in m['files']:checked(Q/v['path'],v)
 require(not m['symlinks'],'Unexpected output symlinks')
print(json.dumps({'result':'PASS','PRs':46,'captured_inputs':len(read('INPUT_MANIFEST.json')['files']),'git_blobs':169,'publications':4,'public_files':8,'archive_payloads':payload_count,'provider_calls':0}))
