"""Accept PR95's qualified result only after actual publication, tracker, and merge.

This program acts exclusively in the independent main checkout.  It preserves
the primary checkout/index and the immutable incoming source archive.
"""
from pathlib import Path
import ast, datetime, hashlib, json, os, subprocess

A=Path(__file__).resolve().parent;C=A.parents[2];P=A.parents[1]
HEAD='6534ad01e519c719628a18984b108e73cf2e8ead'
D=A/'native_acceptance_20261005';D.mkdir(exist_ok=False);records=[]
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def require(ok,message):
    if not ok:raise RuntimeError(message)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def load(p):return json.loads(p.read_text())
def dump(p,x):p.write_text(json.dumps(x,indent=2,sort_keys=True)+'\n')
def run(argv,cwd=C):
    started=now();child=subprocess.Popen(argv,cwd=cwd,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    out,err=child.communicate();i=len(records)
    for name,b in [('stdout',out),('stderr',err)]:(D/(str(i)+'.'+name+'.bin')).write_bytes(b)
    records.append({'argv':argv,'cwd':str(cwd),'PID':child.pid,'UTC_start':started,'UTC_end':now(),
       'exit_code':child.returncode,'stdout_file':str(i)+'.stdout.bin','stderr_file':str(i)+'.stderr.bin',
       'stdout_sha256':hashlib.sha256(out).hexdigest(),'stderr_sha256':hashlib.sha256(err).hexdigest()})
    dump(D/'PROCESS_JOURNAL.json',{'operator_PID':os.getpid(),'records':records})
    require(child.returncode==0,err.decode('utf-8','replace')[:1000]);return out
def git(*args):return run(['/usr/bin/git',*args])

ready=load(A/'ROOT_READY_FOR_PUBLICATION.json')
require(ready['publication_clearance'] is True and ready['whole_package_rounds']>=2,'fresh whole-package gate')
require(ready['source_head']==HEAD and ready['priority_clearance'] is False
        and ready['qualified_publication_user_authorized'] is True,'qualified scope')
Q=A/ready['package_relative_path']
for e in ready['upload_pins']:
    f=Q/'publicfiles'/e['file'];require(f.stat().st_size==e['bytes'] and sha(f)==e['sha256'],'reviewed payload changed')
pub=load(A/'actual_operations/zenodo_publish/stdout.bin')
require(pub['state']=='published' and pub['environment']=='production' and pub['doi'],'published receipt')
doi=pub['doi'];url=pub['doi_url']
public=load(A/'ROOT_PUBLIC_DEPOSIT_VERIFICATION.json')
require(public['verified'] is True and str(public['record_id'])==str(pub['id']),'public download gate')
tracker=load(A/'ROOT_TRACKER_RECORD.json')
require(tracker['unique_verified'] is True and tracker['DOI']==doi,'tracker gate')
pr=load(A/'actual_operations/pr95_merged_readback/stdout.bin')
require(pr['state']=='MERGED' and pr['headRefOid']==HEAD and pr['mergeCommit']['oid'],'merge gate')
merge=pr['mergeCommit']['oid']
require(git('symbolic-ref','--short','HEAD').strip()==b'main','branch')
old=git('rev-parse','HEAD').strip().decode();require(not git('diff','--cached','--name-only','-z'),'foreign staged')
queue=C/'unsolved_math_prioritization/QUEUE.md'
old_queue=git('show',old+':unsolved_math_prioritization/QUEUE.md')
require(not queue.exists() or queue.read_bytes()==old_queue,'unknown queue worktree edits')
git('fetch','--no-tags','https://github.com/AlecKriebel/Math.git','main')
base=git('rev-parse','FETCH_HEAD').strip().decode()
git('merge-base','--is-ancestor',old,base);git('merge-base','--is-ancestor',merge,base)
orig=load(A/'original_source_authentication_20261005/ORIGINAL_BLOB_MANIFEST.json')
require(len(orig['files'])==17,'incoming inventory')
incoming=[]
native_prefix='unsolved_math_prioritization/attempts/10400120/'
native_dir=C/native_prefix
if native_dir.exists():
    require(not native_dir.is_symlink(),'linked native directory')
    present={str(f.relative_to(C)) for f in native_dir.rglob('*') if f.is_file() or f.is_symlink()}
    require(present<={e['path'] for e in orig['files']},'foreign native files')
for e in orig['files']:
    require(e['path']==native_prefix+e['relative_path'] and '..' not in Path(e['relative_path']).parts,'native path scope')
    require(Path(e['preserved_path']).is_relative_to(A/'original_source_authentication_20261005/original_attempt'),'original archive scope')
    require(sha(Path(e['preserved_path']))==e['sha256'],'incoming archive changed')
    b=git('show',base+':'+e['path']);require(hashlib.sha256(b).hexdigest()==e['sha256'],'merged native body changed')
    f=C/e['path'];require(not f.is_symlink() and (not f.exists() or f.read_bytes()==b),'foreign native worktree edits')
    incoming.append((e,f,b))
qb=git('show',base+':unsolved_math_prioritization/QUEUE.md').decode()
lines=qb.splitlines();indices=[i for i,s in enumerate(lines) if '| 10400120 / AMR-103-0120 |' in s]
require(len(indices)==1,'unique queue row');i=indices[0];cells=lines[i].split('|')
require(cells[8].strip()=='claimed_solved' and cells[9].strip()=='2/5','literal status/budget')
# The private index is empty; mixed reset preserves worktree files and never acts in R.
git('reset','--mixed','--quiet',base)
for e,f,b in incoming:f.parent.mkdir(parents=True,exist_ok=True);f.write_bytes(b)
N=C/'unsolved_math_prioritization/attempts/10400120'
for rel in ['verify.py','independent_review/author_replay/verify.py']:
    source=A/'repaired_certificate_sources_20261005/verify.py'
    require(sha(source)=='1294068a5202c9f05ededf864887b7ce7bcb979319bd8f32827df5c88191a6e8','repaired author pin')
    (N/rel).write_bytes(source.read_bytes())
source=A/'repaired_certificate_sources_20261005/independent_checks.py'
require(sha(source)=='401a42f6295c482ba2b745d764558c08507ea1eed1dc0df38ef780d2e6966487','repaired independent pin')
(N/'independent_review/independent_checks.py').write_bytes(source.read_bytes())
for rel in ['verify.py','independent_review/author_replay/verify.py','independent_review/independent_checks.py']:
    require(not any(isinstance(n,ast.Assert) for n in ast.walk(ast.parse((N/rel).read_text()))),'removable guard')
proof=N/'COUNTEREXAMPLE.md';s=proof.read_text()
old_header='**Status:** complete counterexample candidate, independent review pending.'
require(s.count(old_header)==1,'incoming status header')
s=s.replace(old_header,'**Status:** verified full counterexample to the printed claim; accepted as a qualified research note with historical priority unresolved.')
old_pending='Independent review must verify source normalization, root/level admissibility, lens surgery words and the cyclotomic computation before a resolution status is adopted.'
require(s.count(old_pending)==1,'incoming review boundary')
s=s.replace(old_pending,'The source normalization, root/level admissibility, lens surgery words and cyclotomic computation have been independently verified; historical priority remains unresolved as detailed below.')
s+='\n## 5. Qualified publication acceptance (2026-10-05)\n\nThe checkable research note, [An explicit SU(5) lens-space counterexample to the printed Guadagnini-Pilo conjecture]('+url+'), contains a short analytic A4 root-lattice reduction and portable exact certificates. The target is the claim printed as Ohtsuki Conjecture7.5, p474, not an assertion about the problem\'s current global status. Ohtsuki\'s volume is nominally2002 and was published1June2004; Guadagnini-Pilo appeared in CMP192(1998),47–65, DOI10.1007/s002200050290. The actual general-formula input is Hansen-Takata arXiv:math/0209403v2; its final journal full text was not compared. Established full ordinary modular-category and RT surgery foundations are imported mathematical inputs.\n\nHistorical priority remains unresolved. Takahito Kuriya\'s directly relevant preprint, The LMO invariant and the Guadagnini-Pilo conjecture for lens spaces, is credited in the note and priority supplement. Its full text and complete hypotheses/conclusions could not be obtained; we cannot establish that it does not already contain or circumscribe this result. No first counterexample, exhaustive novelty clearance, continuing global openness, or new historical resolution is claimed. Other source and edition gaps are disclosed in the public supplement. No claim that Kuriya\'s language is Japanese or that it has a DOI is made.\n\nAt least two sequential fresh whole-package adversarial AI reviews checked the final package; any required corrections were propagated before publication. Active native guards use explicit exceptions that remain enabled under Python -O. All seventeen incoming bodies, original review reports, original execution receipts and author effort2/5 remain in the immutable program archive. The author-replay proof stays a historical incoming proof and its refreshed receipt binds those historical bytes; it is distinguished from this current acceptance proof. AI tools were used extensively; this is an unrefereed preprint without conventional human peer review.\n'
proof.write_text(s);proof_hash=sha(proof)
author_out=run(['/usr/bin/python3','-E','-B','-O',str(N/'verify.py')],N)
author=load(N/'verification.json')
require(author['all_pass'] is True and author['artifact_sha256']==proof_hash and author['weight_count']==126
        and author['final_polynomial_identities']==7,'current author receipt')
replay=N/'independent_review/author_replay'
replay_out=run(['/usr/bin/python3','-E','-B','-O',str(replay/'verify.py')],replay)
replay_result=load(replay/'verification.json')
require(replay_result['all_pass'] is True and replay_result['artifact_sha256']==sha(replay/'COUNTEREXAMPLE.md'), 'historical replay binding')
ind_out=run(['/usr/bin/python3','-E','-B','-O',str(N/'independent_review/independent_checks.py')],N/'independent_review')
ind=json.loads(ind_out);require(ind['status']=='PASS' and ind['exact_assertions']==2005,'independent native receipt')
(N/'independent_review/independent_results.json').write_bytes(ind_out)
package_rel='../../../draft_pr_publication_program_20260930/audits/pr95_10400120/'+ready['package_relative_path']+'/publicfiles'
(N/'README.md').write_text('# 10400120: verified SU(5) lens-space counterexample, priority unresolved\n\nThe exact full ordinary SU(5) WZW level5 (shifted10) result in COUNTEREXAMPLE.md contradicts the nonzero-magnitude statement printed as Ohtsuki Conjecture7.5. Both fundamental groups are Z/5; the positive S3-normalized squares are3475+1550sqrt5 and4025+1800sqrt5. Imported RT/modular-category and Hansen-Takata formula inputs are identified in the [research note]('+url+').\n\nHistorical priority remains unresolved because Kuriya\'s directly relevant preprint could not be obtained. It is credited and the inability to rule out its containing or circumscribing this result is explicit in the note, public priority supplement and Zenodo metadata. No firstness, exhaustive novelty, current global openness or new historical resolution is claimed. The human specifically authorized this qualified publication.\n\nThe [portable package]('+package_rel+'/README.md) contains analytic proof, exact source, provenance, recorded runs and optimization-safe guards. At least two sequential fresh whole-package adversarial AI reviews completed; all required repairs were propagated. Current native optimized author/replay checks reproduce126 labels and7 final polynomial identities, and the independent lattice route passes2005 explicit finite checks. Counts are algorithmic counts, not quality scores; replay proof and old review texts are historical and the immutable originals remain archived.\n\nAI tools were used extensively; the preprint is unrefereed without conventional human peer review. Original author effort2/5 is preserved; zero new central proof-search turns. DOI: '+doi+'; tracker: '+tracker['range']+'. See ACCEPTANCE.json for current provenance.\n')
summary=N/'independent_review/review_summary.json';x=load(summary)
x.update({'historical_review_about_original_submission':True,'current_candidate_sha256':proof_hash,
   'current_author_replay_byte_identical_to_original_receipt':False,
   'current_receipt_note':'Minimal guards repaired and actual optimized receipts refreshed. Immutable original proof/review/receipts remain archived; candidate_sha256 still identifies that original proof.',
   'qualified_publication_DOI':doi,'historical_priority_established':False,
   'whole_package_review_rounds':ready['whole_package_rounds']});dump(summary,x)
with (N/'RESEARCH_LOG.md').open('a') as f:f.write('\n### '+now()+' — qualified publication acceptance, workflow95%\nVerified complete printed-claim counterexample published as '+doi+'; tracker '+tracker['range']+'. Priority unresolved with Kuriya credited and inaccessible full text disclosed. Fresh sequential full-package reviews completed, current native optimized explicit guards reproduce exactly. Incoming17 bodies and original effort2/5 preserved. Final scoped main checkpoint remains pending.\n')
accept={'schema':'pr95-native-qualified-acceptance/v1','UTC':now(),'actual_operator_PID':os.getpid(),
 'PR':95,'source_head':HEAD,'merge_commit':merge,'base_commit':base,'premerge_private_main':old,
 'DOI':doi,'record_url':pub['record_url'],'tracker_range':tracker['range'],'literal_status':'claimed_solved',
 'full_printed_claim_counterexample_verified':True,'qualified_publication_user_authorized':True,
 'priority_clearance':False,'historical_priority_established':False,'human_peer_review':False,
 'whole_package_review_rounds':ready['whole_package_rounds'],'original_budget':'2/5','new_central_proof_search_turns':0,
 'current_proof_sha256':proof_hash,'incoming_bodies_authenticated':17,'native_optimized_runs_passed':True,
 'native_author_polynomial_identities':7,'native_independent_finite_checks':2005,
 'main_checkpoint_pending':True,'primary_checkout_mutated':False,'primary_synchronization_pending':True}
dump(N/'ACCEPTANCE.json',accept)
all_native=sorted(f for f in N.rglob('*') if f.is_file() and f.name!='SHA256SUMS')
(N/'SHA256SUMS').write_text(''.join(sha(f)+'  '+str(f.relative_to(N))+'\n' for f in all_native))
cells[11]=' 2026-10-05: Verified full ordinary SU(5) counterexample to printed Conjecture7.5; qualified research note published after fresh sequential package reviews. Historical priority unresolved: Kuriya preprint unavailable and credited; no firstness/new historical resolution claim. Exact optimization-safe certificates, extensive AI, unrefereed. PR95 accepted. '
cells[12]=' '+url+' ';lines[i]='|'.join(cells)
queue.parent.mkdir(parents=True,exist_ok=True);queue.write_text('\n'.join(lines)+'\n')
require([s for j,s in enumerate(lines) if j!=i]==[s for j,s in enumerate(qb.splitlines()) if j!=i],'other queue rows changed')
accept['native_paths']=[str(f.relative_to(C)) for f in N.rglob('*') if f.is_file()]+[str(queue.relative_to(C))]
accept['native_pins']=[{'file':str(f.relative_to(C)),'bytes':f.stat().st_size,'sha256':sha(f)} for f in N.rglob('*') if f.is_file()]
dump(D/'PREPARED_RECEIPT.json',accept)
print(json.dumps({k:v for k,v in accept.items() if k not in ['native_paths','native_pins']}))
