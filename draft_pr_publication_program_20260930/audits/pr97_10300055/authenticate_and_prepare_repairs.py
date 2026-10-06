from pathlib import Path
import json,hashlib,datetime,os,ast
A=Path(__file__).resolve().parent
def require(ok,message):
    if not ok:raise RuntimeError(message)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
families=[('source_scope_tightness_adversary_20261005','CLOSED_MANIFEST.json','a0005bef960a6e4e13ab340ac52dd84008226097be15abb7c8569f2999f8520a'),('low_regularity_disk_adversary_20261005','CLOSED_SHA256_MANIFEST.json','d6260f53cdcb7455a2cfd2a9473af0040d9ea0cd93feb51c7a9917d4984cc891'),('pencil_certificate_adversary_20261005','CLOSED_MANIFEST.json','384946b08db8fcc698aade1850637c64cad6cb28b3fadb9dbf8ae5741d235345')]
checked=[]
def verify(e,D):
    p=Path(e.get('path',e.get('file','')))
    if not p.is_absolute():p=D/p
    require(p.resolve().is_relative_to(A) and p.is_file() and not p.is_symlink(),'unsafe evidence')
    require(p.stat().st_size==e['bytes'] and sha(p)==e['sha256'],'evidence changed '+str(p))
for folder,name,digest in families:
    D=A/folder;p=D/name;require(sha(p)==digest,'closed manifest pin');m=json.loads(p.read_text())
    for e in m['files']:verify(e,D)
    borrowed=m.get('transitive_evidence',m.get('borrowed_read_only_inputs',[]))
    require(isinstance(borrowed,list),'borrowed input shape')
    for e in borrowed:verify(e,D)
    require(sha(D/'REPORT.md')==m['report_sha256'] and sha(D/'VERDICT.json')==m['verdict_sha256'],'report pins')
    checked.append({'family':folder,'manifest_sha256':digest,'own_files':len(m['files']),'borrowed_files':len(borrowed),'report_sha256':m['report_sha256'],'ROOT_full_report_read':True})
O=A/'original_source_authentication_20261005/original_attempt';orig=O/'CANDIDATE.md';require(sha(orig)=='4ff15e7cbf742bb7fcaf329d1d31b99b1bc9d33c5e45b9ba7ca5bb3365964c33','original candidate')
D=A/'repaired_verification_candidate_v1';D.mkdir(exist_ok=False)
s=orig.read_text();s=s.replace('Complete affirmative proof candidate; separate adversarial review pending.','Verified conditional argument with mathematical-audit repairs incorporated; priority and publication-package reviews pending.')
old='For smooth contact structures, tightness has its usual meaning. The proof also treats $C^1$ contact forms using the equivalent overtwisted-disk criterion: an overtwisted disk is an embedded disk whose boundary is Legendrian and whose tangent planes are distinct from the contact planes along that boundary. The disk may be taken smooth; the approximation argument below also allows a $C^2$ disk. This criterion is recalled in [DR, p. 5] and [V11, pp. 42–43].'
new='For smooth contact structures, tightness has its usual meaning and is equivalent to the absence of an embedded smooth disk with Legendrian boundary whose tangent planes are distinct from the contact planes along that boundary. For $C^1$ forms, tightness in this note means precisely the absence of such an embedded $C^2$ disk. The proof also shows that every sufficiently $C^1$-close smooth contact form is tight. No equivalence with other low-regularity definitions, or existence of a smooth Legendrian-boundary disk for the original $C^1$ field, is asserted. The smooth criterion is recalled in [DR, p. 5] and [V11, pp. 42–43].'
require(s.count(old)==1,'regularity paragraph');s=s.replace(old,new)
old='Then $\\ker\\omega$ is tight. In particular the answer to Calegari\'s Question 13.2 is affirmative.'
new='Then $\\ker\\omega$ is tight with the explicit $C^2$-disk meaning stated below, and every sufficiently $C^1$-close smooth contact form is tight in the usual sense. In particular, if $\\omega$ is smooth then $\\ker\\omega$ is tight in the usual smooth sense, answering Calegari\'s Question 13.2 under its standard smooth contact-form interpretation.'
require(s.count(old)==1,'theorem scope');s=s.replace(old,new)
old='Let $\\theta$ be a $C^1$ contact form on a smooth three-manifold.';new='Let $\\theta$ be a $C^1$ contact form on a closed smooth three-manifold.';require(s.count(old)==1,'closed lemma scope');s=s.replace(old,new)
(D/'CANDIDATE.md').write_text(s)
prepared=A/'pencil_certificate_adversary_20261005/prepared_minimal_guard_corrections'
for rel,digest in [('verify.py','009845e507b2dcfed4c681b6514e9be22aa56e979168b3c1834dbc5b44f70af0'),('independent_checks.py','b3a08e300c19e3aabf2782716825463feedb40d9e82b946729cdbc3975fb4652')]:
    f=prepared/rel;require(sha(f)==digest,'prepared guard source');require(not any(isinstance(x,ast.Assert) for x in ast.walk(ast.parse(f.read_text()))),'removable guard')
    target=D/(rel if rel=='verify.py' else 'review/'+rel);target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(f.read_bytes())
replay=D/'review/author_replay';replay.mkdir();(replay/'CANDIDATE.md').write_bytes((D/'CANDIDATE.md').read_bytes());(replay/'verify.py').write_bytes((D/'verify.py').read_bytes())
x={'schema':'pr97-root-authenticated-minimal-repairs/v1','UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'actual_operator_PID':os.getpid(),'families':checked,'repairs':['Explicit exception diagnostic guards active under Python-O','C1 statement explicitly excludes embedded C2 boundary-criterion disks; standard smooth tightness and nearby smooth tightness distinguished','Auxiliary smoothing lemma restricted to closed M'],'original_candidate_sha256':sha(orig),'current_candidate_sha256':sha(D/'CANDIDATE.md'),'source_head':'fb50facb2a7389bb272bbf0b5cbd80c24c79b992','original_author_effort':'2/5','new_central_proof_search_turns':0,'priority_clearance':False,'publication_clearance':False,'current_receipt_refresh_pending':True,'original_native_archive_unchanged':True}
(A/'ROOT_REPAIR_PREPARATION_20261005.json').write_text(json.dumps(x,indent=2)+'\n');print(json.dumps(x))
