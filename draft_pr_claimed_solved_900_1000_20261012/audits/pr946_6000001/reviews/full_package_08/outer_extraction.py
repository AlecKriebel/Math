import pathlib,zipfile,hashlib,json,stat,datetime
W=pathlib.Path(__file__).resolve().parent;A=W.parent.parent;D=A/'preprint';T=W/'private/complete_outer';T.mkdir()
def sha(b):return hashlib.sha256(b).hexdigest()
raw=(D/'global_hessian_verification.zip').read_bytes();assert sha(raw)=='e687f7c9a3643a796a5fe813ec10e5c2c74a28adb081a7ebeefb6910823c6863'
f=json.loads((D/'FREEZE.json').read_bytes());records=[]
with zipfile.ZipFile(D/'global_hessian_verification.zip') as z:
 manifest=z.read(f['archive_layout']['manifest']);assert sha(manifest)=='0833606acbf062d90872dd562e27423e51e2efc91369059436ca2fb83d55e33b';m=json.loads(manifest);assert len(z.infolist())==220 and set(z.namelist())==set(m['files'])|{f['archive_layout']['manifest']}
 for info in z.infolist():
  name=info.filename;assert not name.startswith('/') and all(p not in ('','.','..') for p in name.split('/')) and stat.S_ISREG(info.external_attr>>16);b=z.read(info)
  if name in m['files']:assert {'bytes':len(b),'sha256':sha(b)}==m['files'][name]
  q=T/name;q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes(b);q.chmod(0o644);assert q.read_bytes()==b;records.append({'member':name,'bytes':len(b),'sha256':sha(b),'archive_mode':oct(info.external_attr>>16)})
out={'status':'PASS','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'complete_outer_members_extracted':len(records),'all_members_authenticated_before_this_extraction':True,'outer_manifest_sha256':sha(manifest),'private_destination':str(T),'records':records};(W/'OUTER_EXTRACTION.json').write_text(json.dumps(out,indent=2)+'\n');print('Entire220member outer ZIP authenticated and extracted')
