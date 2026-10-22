"""Bounded read-only final input/source inventory; no provider or Git operations."""
from pathlib import Path
import datetime,hashlib,json,stat
ROOT=Path(__file__).resolve().parent;A=ROOT.parent;O=A/'operations';S=ROOT/'source'
def need(x,m):
    if not x:raise RuntimeError(m)
def sha(b):return hashlib.sha256(b).hexdigest()
need(not(ROOT/'MANIFEST.json').exists(),'Closed packet: copy this preparation verifier to an owned unsealed folder before producing a new output')
inventory={}
def read(path,pin=None):
    need(path.is_file() and not path.is_symlink(),'Nonregular input '+str(path))
    b=path.read_bytes();st=path.stat();current={'bytes':len(b),'sha256':sha(b)}
    if pin is not None:need(current==pin,'Input pin changed '+str(path))
    inventory[str(path)]={**current,'mode':stat.S_IMODE(st.st_mode),'mtime_ns':st.st_mtime_ns}
    return b
MS='623a85eca963527260367dd192bb0373f6a81972179633fa6f219c72a6237803';BS='5a60e8743ab5dd72e113a75f9af370974a0895bdabd8e68321d58701c947ae94'
b=read(S/'SOURCE_MANIFEST.json');need(sha(b)==MS,'Final17 source anchor')
pins=json.loads(b);need(set(p.name for p in S.iterdir())==set(pins)|{'SOURCE_MANIFEST.json'},'Final17 source closure')
for n,p in pins.items():read(S/n,p)
need(sha(read(S/'bootstrap17.py'))==BS,'Final17 bootstrap anchor')
f=json.loads(read(S/'SOURCE_FREEZE.json'))
manifest=json.loads(read(O/'OPERATIONS_MANIFEST.json'))
need(sha((O/'OPERATIONS_MANIFEST.json').read_bytes())==f['prior_operations_manifest_sha256'],'Immutable05 seal')
for n,p in manifest['files'].items():read(O/n,p)
need(set(p.name for p in(O/'runtime').iterdir())==set(f['prior_runtime_files']),'13 old runtime closure')
for n,p in f['prior_runtime_files'].items():read(O/'runtime'/n,p)
for n,p in f['prior_wrapper_files'].items():read(A/'stage_known_unattempted_resumption01'/n,p)
for group in ['held06_context','held07_context','held08_context','held09_context','held10_context','held11_context','held12_context','held13_context','held14_context','held15_context','held16_context']:
    for n,p in f[group].items():read(A/n,p)
for n,p in f['actual_phase_reference_inputs'].items():read(A.parent/n,p)
for phase in ['06','07','08','09','10','11','12','13','14','15','16','17']:need(not(A/('operations'+phase)/'runtime').exists(),'Unauthorized production runtime appeared')
need(not(O/'runtime/ROOT_OPERATIONAL_CLEARANCE.json').exists(),'Revoked05 authority revived')
for phase in ['06','07','08','09','10','11','12','13','14','15','16']:
    s=A/('operations'+phase)/'source';declared=json.loads(read(s/'SOURCE_MANIFEST.json'))
    need(set(p.name for p in s.iterdir())==set(declared)|{'SOURCE_MANIFEST.json'},'Prior source closure')
    for n,p in declared.items():read(s/n,p)
# The immediate prior whole preparation seal is read back completely, including
# its nested manifests/private custody, with exact file and directory metadata.
prior=A/'operations16';seal=json.loads(read(prior/'MANIFEST.json'))
entries=seal['entries'];actual={'.'}|{p.relative_to(prior).as_posix() for p in prior.rglob('*') if p!=prior/'MANIFEST.json'}
need(actual==set(entries),'Closed16 recursive inventory changed')
for n,p in entries.items():
    q=prior if n=='.' else prior/n;st=q.lstat()
    need(not q.is_symlink() and stat.S_IMODE(st.st_mode)==p['mode'] and st.st_mtime_ns==p['mtime_ns'],'Closed16 metadata changed '+n)
    if p['kind']=='file':read(q,{'bytes':p['bytes'],'sha256':p['sha256']})
    else:need(q.is_dir(),'Closed16 directory changed')
# Read the entire root-adopted independent whole13 closure without expanding
# its historical private ZIP recipes or changing any source metadata.
whole=A/'publication_operations13_whole_review01';whole_seal=json.loads(read(whole/'MANIFEST.json'))
need({'.'}|{q.relative_to(whole).as_posix()for q in whole.rglob('*')if q!=whole/'MANIFEST.json'}==set(whole_seal['entries']),'Whole13 recursive membership changed')
for n,pin in whole_seal['entries'].items():
 q=whole if n=='.'else whole/n;st=q.lstat()
 need(not q.is_symlink()and stat.S_IMODE(st.st_mode)==pin['mode']and st.st_mtime_ns==pin['mtime_ns'],'Whole13 metadata changed')
 if 'nlink'in pin:need(st.st_nlink==pin['nlink'],'Whole13 pinned nlink changed')
 if pin['kind']=='file':read(q,{'bytes':pin['bytes'],'sha256':pin['sha256']})
 else:need(q.is_dir(),'Whole13 directory changed')

# Entire newly root-adopted whole15 HOLD closure, including every private carrier.
whole15=A/'operations15_whole_review01';whole15_seal=json.loads(read(whole15/'MANIFEST.json'))
need({'.'}|{q.relative_to(whole15).as_posix()for q in whole15.rglob('*')if q!=whole15/'MANIFEST.json'}==set(whole15_seal['entries']),'Whole15 recursive membership changed')
for n,pin in whole15_seal['entries'].items():
 q=whole15 if n=='.'else whole15/n;st=q.lstat()
 need(not q.is_symlink()and stat.S_IMODE(st.st_mode)==pin['mode']and st.st_mtime_ns==pin['mtime_ns'],'Whole15 metadata changed')
 if 'nlink'in pin:need(st.st_nlink==pin['nlink'],'Whole15 pinned nlink changed')
 if pin['kind']=='file':read(q,{'bytes':pin['bytes'],'sha256':pin['sha256']})
 else:need(q.is_dir(),'Whole15 directory changed')

# Entire newly root-adopted independent whole16 HOLD, without importing it.
whole16=A/'operations16_whole_review01';whole16_seal=json.loads(read(whole16/'MANIFEST.json'))
need({'.'}|{q.relative_to(whole16).as_posix()for q in whole16.rglob('*')if q!=whole16/'MANIFEST.json'}==set(whole16_seal['entries']),'Whole16 recursive membership changed')
for n,pin in whole16_seal['entries'].items():
 q=whole16 if n=='.'else whole16/n;st=q.lstat()
 need(not q.is_symlink()and stat.S_IMODE(st.st_mode)==pin['mode']and st.st_mtime_ns==pin['mtime_ns'],'Whole16 metadata changed')
 if 'nlink'in pin:need(st.st_nlink==pin['nlink'],'Whole16 pinned nlink changed')
 if pin['kind']=='file':read(q,{'bytes':pin['bytes'],'sha256':pin['sha256']})
 else:need(q.is_dir(),'Whole16 directory changed')

# Execute only the immutable filesystem package/proposal validation helpers.
base=read(O/'bootstrap.py');need(sha(base)==f['prior_bootstrap_sha256'],'Immutable05 bootstrap')
ns={'__file__':str(O/'bootstrap.py'),'__name__':'final_input_bootstrap'}
exec(compile(base,str(O/'bootstrap.py'),'exec',dont_inherit=True,optimize=0),ns)
load,_=ns['load_verified'](O,f['prior_operations_manifest_sha256'],f['prior_bootstrap_sha256'])
c=load('ops_common');pkg=c.package();c.proposal()
read(c.AUDIT/'PACKAGE_FREEZE_01.json');read(c.AUDIT/'ROOT_SCIENTIFIC_CLEARANCE.json')
for n,p in pkg['freeze']['frozen_six'].items():read(c.PUBLICATION/n,p)
read(c.PUBLICATION/'SOURCE_MANIFEST.json')
for n,p in json.loads((c.PUBLICATION/'SOURCE_MANIFEST.json').read_bytes()).items():read(c.PUBLICATION/n,p)
for n,p in json.loads((c.AUDIT/'ROOT_SCIENTIFIC_CLEARANCE.json').read_bytes())['root_acceptance_pins'].items():read(c.AUDIT/n,p)
for n,p in json.loads((O/'DEPENDENCY_PINS.json').read_bytes()).items():read(c.REPO/n,p)
references=[]
for p in sorted((O/'private/repair_native_reference').glob('*.json')):
    b=read(p);references.append({'path':str(p.relative_to(A)),'bytes':len(b),'sha256':sha(b)})
result={'at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'final_source_sha256':MS,'bootstrap_sha256':BS,'original_public_payloads':len(manifest['files']),'prior_runtime_leaves':len(f['prior_runtime_files']),'immediate_prior_seal_files':seal['files'],'immediate_prior_seal_directories':seal['directories'],'closed16_recursive_bytes_modes_nsmtimes_readback':True,'prior06_to16_source_closures_readback':True,'science_package_source_zip_release_kit_proposal_helpers_passed':True,'native_reference_inputs':references,'inventory':inventory,'whole13_full_closed_bytes_modes_nsmtimes_nlink_checked':True,'whole13_seal_files':whole_seal['files'],'whole13_seal_directories':whole_seal['directories'],'whole15_complete_closed_readback':True,'whole15_files':sum(v['kind']=='file'for v in whole15_seal['entries'].values()),'whole15_directories':sum(v['kind']=='directory'for v in whole15_seal['entries'].values()),'whole16_complete_closed_readback':True,'whole16_files':sum(v['kind']=='file'for v in whole16_seal['entries'].values()),'whole16_directories':sum(v['kind']=='directory'for v in whole16_seal['entries'].values()),'prior_deeper_private_closures_not_reexpanded_here':True,'actual_provider_or_Git_requests':0,'actual_service_or_Git_mutations':0,'publication_ready':False}
(ROOT/'private/FINAL_INPUT_READBACK.json').write_text(json.dumps(result,sort_keys=True,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items()if k not in {'inventory','native_reference_inputs'}},indent=2))
