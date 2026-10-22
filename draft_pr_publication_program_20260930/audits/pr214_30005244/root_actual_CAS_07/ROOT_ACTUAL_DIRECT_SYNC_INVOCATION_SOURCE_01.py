from pathlib import Path
import types,hashlib,json,os,datetime
A=Path("/Users/alec/Documents/Math/draft_pr_publication_program_20260930/audits/pr85_30001203/isolated_main_integration_20261005/checkout/draft_pr_publication_program_20260930/audits/pr214_30005244");B=A/'native_completion_preparation_02';D=A/'root_actual_CAS_07'
assert A.resolve()==A;D.mkdir(exist_ok=True);assert D.resolve()==D and not D.is_symlink()
def pin(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
p=B/'completion_checkpoint.py';code=p.read_bytes();assert pin(code)=={'bytes':44492,'sha256':'30bdc4dd56c176da4176be136a34ba2424d73c8653e50a501dd624210957a945'}
q=types.ModuleType('Root214_true_CAS_evidence');q.__file__=str(p);exec(compile(code,str(p),'exec'),q.__dict__)
seed=q.Seed({"path":"/Users/alec/Documents/Math/draft_pr_publication_program_20260930/audits/pr85_30001203/isolated_main_integration_20261005/checkout/draft_pr_publication_program_20260930/audits/pr214_30005244/root_logical_capture_01/LOGICAL_MANIFEST_01.json","bytes":286492,"sha256":"f344079c1613a768da24b6f2ac3fc66ca5729579f6761be191ddb903bd7b5b9b"},{"path":"/Users/alec/Documents/Math/draft_pr_publication_program_20260930/audits/pr85_30001203/isolated_main_integration_20261005/checkout/draft_pr_publication_program_20260930/audits/pr214_30005244/root_completion_acceptance_01/ROOT_LOGICAL_PACKET_ACCEPTANCE_02.json","bytes":6585,"sha256":"eb29018250f708fe85d668b77974599416f97f03161712c8451fbb1a4821d21e"});h=seed.h;e=seed.e
def ref(p):return {'path':str(p),**pin(q.read_regular(p)[0])}
def put(n,j):
 assert Path(n).name==n
 data=q.enc(j)
 with e.ParentHandle(D/n) as parent:
  parent.check();fd=os.open(n,os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW,0o444,dir_fd=parent.fd)
  with os.fdopen(fd,'wb') as f:f.write(data);f.flush();os.fchmod(f.fileno(),0o444);os.fsync(f.fileno())
  parent.check();os.fsync(parent.fd)
 return ref(D/n)

ar={"path":"/Users/alec/Documents/Math/draft_pr_publication_program_20260930/audits/pr85_30001203/isolated_main_integration_20261005/checkout/draft_pr_publication_program_20260930/audits/pr214_30005244/native_completion_preparation_02/ROOT_COMPLETE214_READ_ADMISSION_07/ADMISSION.json","bytes":2507,"sha256":"cc0cf10d11567fffebb19c5eae6e59ef3c6a10b212a9410eae0a3b53dc469ac8"};gr={"path":"/Users/alec/Documents/Math/draft_pr_publication_program_20260930/audits/pr85_30001203/isolated_main_integration_20261005/checkout/draft_pr_publication_program_20260930/audits/pr214_30005244/root_completion_acceptance_01/ROOT_ADMISSION_ACCEPTANCE_07.json","bytes":3325,"sha256":"e86a8e8e358fd2442047cf766b234971bff7cba0852b22709a8ddfaffa66a2c7"};xr={"path":"/Users/alec/Documents/Math/draft_pr_publication_program_20260930/audits/pr85_30001203/isolated_main_integration_20261005/checkout/draft_pr_publication_program_20260930/audits/pr214_30005244/root_completion_acceptance_01/ROOT_BOUNDED_GET_OPERATION_ACCEPTANCE_08.json","bytes":3442,"sha256":"82d694e2288399c84feed31830f93227436acd01ddd118133558d85e1e3c395b"};cas={"path":"/Users/alec/Documents/Math/draft_pr_publication_program_20260930/audits/pr85_30001203/isolated_main_integration_20261005/checkout/draft_pr_publication_program_20260930/audits/pr214_30005244/root_actual_CAS_07/ROOT_ACTUAL_CAS_ACCEPTANCE_07.json","bytes":5583,"sha256":"6f84deeeeef178ae5b2e73025a13c7b5afe0f06d86f436207f4e33dbe8a74896"}
xp=A/'bounded_get_transport_preparation_02/bounded_get_extension.py';raw=q.read_regular(xp)[0]
assert pin(raw)=={'bytes':24365,'sha256':'53bc5c3ffd9495aa06b03739b1ea362c9660a2ebb7075cf955f06045b7fbb05c'}
x=types.ModuleType('Root_accepted_bounded_sync_direct');x.__file__=str(xp);exec(compile(raw,str(xp),'exec'),x.__dict__)
base=q.Runtime(seed,ar,gr);rt=x.bind_runtime(q,base,xr,'sync')
transport=e.journal_new('ROOT_COMPLETE214_RETRY_READ_SYNC_TRANSPORT_01')
api=x.make_readonly_api(q,rt,transport)
journal=q.read_journal(e,'ROOT_COMPLETE214_SYNC_BOUNDED_01','ROOT_COMPLETE214_SYNC_')
e.put(journal,'ROOT_TWO_JOURNAL_SYNC_ASSOCIATION.json',{'schema':'pr214-root-direct-sync-two-journal-association-v1',
'UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'extension_source':ref(xp),'operation_gate':xr,'actual_CAS':cas,
'transport_journal':str(transport),'effect_journal':str(journal),'extension_CLI_sync_used':False,
'same_wrapped_runtime_observer_actual_CAS_passed_to_unchanged_original_sync':True,'transport_provenance_before_sync':api.provenance()})
result=q.sync(rt,api,journal,cas)
rt.refresh();e.put(journal,'ROOT_TRANSPORT_PROVENANCE_AFTER_SYNC.json',api.provenance())
pointer=ref(B/'ROOT_ACTUAL_COMPLETION_POINTER.json');sync=ref(journal/'ACTUAL_FIVE_SYNC.json');q.checked_pointer(rt,cas)
print(json.dumps({'sync':sync,'pointer':pointer,'native_observation':result,'actual_external_Root_terminal_inferred':False}))
