"""Assemble a current, explicit-scope publication packet; no publication action."""
from pathlib import Path
import datetime,hashlib,json,shutil,stat,subprocess,sys,zipfile
A=Path(__file__).resolve().parent;P=A/'publication_package_v1';V=P/'verification';t=datetime.datetime.now(datetime.UTC).isoformat()
def require(ok,msg):
 if not ok:raise ValueError(msg)
def pin(p):
 b=p.read_bytes();return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def write(p,s):
 p.parent.mkdir(parents=True,exist_ok=True);p.write_text(s)
def copy(src,rel):
 require(src.is_file() and not src.is_symlink(),'Unsafe copy source '+str(src));dst=V/rel;dst.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(src,dst)
priority=json.loads((A/'ROOT_PRIORITY_GATE_01.json').read_text());require(priority['bounded_priority_audit_complete'] and priority['qualified_note_route_authorized_by_human'] and not priority['historical_priority_clearance'],'Wrong claim level')
require(not V.exists(),'Existing verification generation');V.mkdir()
metadata={
 'title':'A parity-selected endpoint theorem for the regular dodecahedron','upload_type':'publication','publication_type':'preprint',
 'description':'<p>This note gives two precise answers associated with Fuchs Conjecture 3.2. The imported bare endpoint-angle condition is false: exactly the two proper face diagonals per initial face and vertex are additional paths and have graph distance two. An explicitly adopted parity-selected convention has a complete unbounded endpoint-exclusion proof through double-pentagon germ symmetry, a physical edge-midpoint half-turn, and a unique-common-neighbor argument. The convention is a supported disambiguation, not an authenticated author correction or uniquely compelled printed reading.</p><p>The midpoint and refolding mechanisms are credited to Athreya–Aulicino–Hooper and Troubetzkoy. Alper Ferudun’s current contemporaneous preprint, DOI 10.5281/zenodo.23267641, contains both the formulation distinction and endpoint theorem, and the public face-word type correction. GitHub records our draft PR creation on 1 October 2026 and DataCite records that related DOI registration on 9 October 2026. These dates do not establish historical exact-byte visibility, firstness, author awareness or independence. Current website files could not be compared to its DOI-deposited files, and journal/body-version gaps remain disclosed. No current openness or guaranteed novelty is claimed.</p><p>The deposit includes a four-page research note, standalone LaTeX source and an exact verification package with current optimization-safe guards, meaningful wrong-science controls, distinct independent scientific audits and bounded priority ledgers. It independently validates the public face word while separating its terminal-angle error and additional displayed-coordinate norm inconsistency. Finite checks corroborate the data; they do not replace the universal proof. AI tools were used extensively in development, drafting, source checking, reproduction and adversarial verification. This preprint is unrefereed and has not undergone conventional human peer review.</p>',
 'creators':[{'name':'Kriebel, Alec','affiliation':'Independent researcher','orcid':'0009-0001-9320-500X'}],
 'publication_date':'2026-10-14','version':'1.0','access_right':'open','license':'cc-by-4.0','language':'eng',
 'keywords':['regular dodecahedron','short geodesics','Fuchs Conjecture 3.2','double pentagon','midpoint symmetry','exact verification','source formulation'],
 'related_identifiers':[{'identifier':'https://github.com/AlecKriebel/Math/pull/190','relation':'isDerivedFrom','scheme':'url'},{'identifier':'10.1007/s40598-020-00170-8','relation':'references','scheme':'doi'},{'identifier':'10.1080/10586458.2020.1712564','relation':'references','scheme':'doi'},{'identifier':'10.1080/00029890.2023.2172298','relation':'references','scheme':'doi'},{'identifier':'10.5281/zenodo.23267641','relation':'references','scheme':'doi'},{'identifier':'https://arxiv.org/abs/1811.04131v2','relation':'references','scheme':'url'},{'identifier':'https://arxiv.org/abs/2202.04892v3','relation':'references','scheme':'url'}],
 'notes':'Two-part, explicitly qualified mathematical note: bare-angle target false, adopted parity-selected endpoint theorem true. Classical symmetry mechanisms and exact current contemporaneous overlap credited. No authenticated author erratum, firstness, guaranteed novelty, current openness or independence-of-discovery certification. Extensive AI; unrefereed; no conventional human peer review.'}
deposit={'metadata':metadata,'files':[{'path':'dodecahedron_endpoint.pdf'},{'path':'dodecahedron_endpoint.tex'},{'path':'verification-package.zip'}]}
write(P/'zenodo-deposit.json',json.dumps(deposit,indent=2)+'\n')
write(P/'PACKAGE_README.md',"""# A parity-selected endpoint theorem for the regular dodecahedron

The research note distinguishes the false imported bare-angle exclusion from the proved explicitly parity-selected endpoint theorem. It credits classical midpoint symmetry and Ferudun's current contemporaneous overlapping work. The source convention is not an authenticated author correction; chronology does not certify firstness or independence.

The PDF and standalone LaTeX source are the reading copies. The verification archive includes exact current scripts, independent implementations and derived data, the authenticated original draft as historical provenance, scientific and priority audits, and an exact payload manifest. Primary article bodies and downloaded third-party programs are excluded.

The metadata file is the exact intended input to the repository's Zenodo uploader. Author: Alec Kriebel, ORCID0009-0001-9320-500X. Version1.0, CC BY4.0, AI-assisted, unrefereed and without conventional human peer review. Mathematical details and historical limits are in the note and supplement.
""")
copy(A/'CURRENT_PROOF.md','CURRENT_PROOF.md')
for n in ['dodecahedron_endpoint.pdf','dodecahedron_endpoint.tex']:copy(P/n,'manuscript/'+n)
write(V/'provenance/intended_zenodo_metadata.json',json.dumps(metadata,indent=2)+'\n')
for p in (A/'current_verification').iterdir():
 if p.is_file():copy(p,'current/'+p.name)
for d,n,rename in [('exact_reproduction_adversary','independent_exact.py','independent_exact.py'),('global_geometry_adversary','EXACT_WITNESS_REPLAY.py','independent_face_word.py'),('literal_source_adversary','independent_double_pentagon_check.py','independent_double_pentagon.py')]:copy(A/d/n,'independent/'+rename)
# Preserve complete own-authored family manifests in historical locations.
d='literal_source_adversary';j=json.loads((A/d/'PUBLICATION_ALLOWLIST.json').read_text());names=[x['path'] for x in j['allowlist']]+j['also_authored']
for n in sorted(set(names)):copy(A/d/n,'audit_history/'+d+'/'+n)
d='global_geometry_adversary';names=json.loads((A/d/'SAFE_PUBLICATION_ALLOWLIST.json').read_text())['allowed_relative_paths']
for n in names:copy(A/d/n,'audit_history/'+d+'/'+n)
d='exact_reproduction_adversary';names=json.loads((A/d/'PUBLIC_SAFE_ALLOWLIST.json').read_text())['files']
for n in names:copy(A/d/n,'audit_history/'+d+'/'+n)
d='primary_priority_adversary';j=json.loads((A/d/'FINAL_SEAL.json').read_text());names=[x['path'] for x in j['manifest']]+['FINAL_SEAL.json']
for n in names:copy(A/d/n,'priority/'+d+'/'+n)
d='current_literature_priority_adversary';names=json.loads((A/d/'SAFE_AUTHORED_ALLOWLIST.json').read_text())['authored_only_allowlist']
for n in names:copy(A/d/n,'priority/'+d+'/'+n)
for folder in ['root_verification_runs','root_independent_replays_02']:
 for p in (A/folder).iterdir():
  if p.is_file():copy(p,'results/'+folder+'/'+p.name)
for n in ['ORIGINAL_FILE_MANIFEST.json','ROOT_UPSTREAM_TARGET_AND_PRIOR_01.json','ROOT_UPSTREAM_PRIOR_LOOKUP_CORRECTION_02.json','ROOT_GITHUB_CHRONOLOGY_01.json','ROOT_PRIMARY_SOURCE_ACQUISITION_01.json','ROOT_SCIENTIFIC_ASSESSMENT_01.md','ROOT_GUARD_REPAIR_ADOPTION_01.json','ROOT_FAMILY_PROMOTION_MODES_01.json','ROOT_MATHEMATICAL_GATE_01.json','ROOT_PRIORITY_GATE_01.json','ROOT_REPLAY_INTERRUPTION_01.json','ROOT_OWN_REGENERABLE_RENDER_CLEANUP_01.json']:copy(A/n,'provenance/'+n)
original=json.loads((A/'ORIGINAL_FILE_MANIFEST.json').read_text())
for x in original['files']:
 p=A/'original_submission/files'/x['path'];require(pin(p)=={'bytes':x['bytes'],'sha256':x['sha256']},'Original pin drift');copy(p,'historical_original/'+x['path'])
write(V/'README.md',"""# Exact verification and provenance

The current manuscript and CURRENT_PROOF.md are authoritative. There are two separate results: the imported bare-angle exclusion is false by two proper face diagonals; the expressly adopted parity-selected class has an unbounded graph-distance-two exclusion proof. No author-authenticated erratum, unique printed intent, firstness, guaranteed novelty, current openness or independence of discovery is certified.

## Reproduce current checks

Use Python3.11 or newer with its standard library. Run from this archive's root:

    python3 -B check_manifest.py
    python3 -B current/run_verification.py
    python3 -B independent/independent_exact.py
    python3 -B independent/independent_face_word.py
    python3 -B independent/independent_double_pentagon.py

The -B flag avoids adding bytecode files to the sealed manifest. The current runner executes8 baseline commands and10 meaningful wrong-science controls, in both ordinary and optimized Python. It rejects a wrong length, wrong cyclotomic coefficient, wrong terminal ray, empty edge geometry and wrong displayed-coordinate coefficient. The two canonical original scripts have all28 assert guards replaced by explicit conditional raises. The scientific expressions and valid baseline output are unchanged. Original small float-comparison tests are corroboration only; independent exact field/near-cancellation checks are recorded separately.

The independent programs use distinct exact constructions: rational cyclotomic four-vectors/Gaussian elimination with supporting-plane faces, a separate reflected face-word replay, and an independent double-pentagon corner/gluing check. Display angles and lengths are numerical conveniences; the scientific decisions use exact arithmetic. Finite checks corroborate identities and data; the universal geometric theorem is proved in the manuscript.

## Current and historical records

current/ and independent/ are the portable verification entry points. results/ contains actual Root replays and receipts. The interrupted first Root capture is identified in provenance and is not promoted as a complete run; generation02 completed.

audit_history/ preserves full authored scientific-family seals, reports and exploratory scripts. Those historical runners may require their original repository layout and private acquisition records; they are research provenance, not the portable interface above. They must not be mistaken for current publication claims. The hash seals identify their original scope, including expressly excluded private receipts; they do not certify priority or peer review.

historical_original/ preserves all22 immutable original PR files, including superseded scope phrasing, optimization-unsafe guards, draft-only publication receipt and past AI reviews. Current corrections are in CURRENT_PROOF.md, the manuscript, current/ and the gate/provenance records. The historical documents are not present-day validity/priority/publication certificates.

priority/ contains two completed independent bounded primary-body/version/current-literature audits. Ferudun's current primary manuscript materially overlaps both formulations and the face-word type correction. DataCite registration on9October and our GitHub PR creation on1October are recorded with exact visibility/version limits. DOI-deposited files could not be compared with the current site bytes; journal-version/body gaps remain. No novelty is inferred from failed searches or from the displayed-coordinate defect's absence in inspected competing material.

## Scope and rights

The pinned public face word reconstructs a valid path. Its terminal transported source relation is144degrees(A1), and its displayed A+B eta expression has norm(425+189sqrt5)/2, separate from the reconstructed path norm(307+137sqrt5)/2. These claims concern specified mathematical artifacts.

Downloaded primary PDFs, article text, external source archives/programs, browser cache inventories and credentials are excluded. The source ledgers provide locators, hashes, exact read depth and access limits. AI tools were used extensively; this is unrefereed and has not undergone conventional human peer review. Authored publication material is released CC BY4.0; citations and third-party materials retain their own terms.
""")
checker=r'''"""Validate exact package membership and byte hashes; no mathematical proof claim."""
from pathlib import Path
import hashlib,json
ROOT=Path(__file__).resolve().parent
def require(ok,msg):
    if not ok:raise ValueError(msg)
def main():
    m=json.loads((ROOT/'MANIFEST.json').read_text());files=m['files']
    require(isinstance(files,dict) and files,'Empty manifest')
    observed=set()
    for p in ROOT.rglob('*'):
        require(not p.is_symlink(),'Symlink in package')
        if p.is_file():observed.add(p.relative_to(ROOT).as_posix())
    require(observed==set(files)|{'MANIFEST.json'},'Missing or unexpected package file')
    for name,x in files.items():
        q=Path(name);require(not q.is_absolute() and '..' not in q.parts,'Unsafe manifest path')
        b=(ROOT/q).read_bytes();require(len(b)==x['bytes'] and hashlib.sha256(b).hexdigest()==x['sha256'],'Package bytes changed: '+name)
    return {'status':'PASS','verified_payloads':len(files),'limits':'Exact artifact identity is not proof of mathematical truth, priority or peer review.'}
if __name__=='__main__':print(json.dumps(main(),indent=2))
'''
write(V/'check_manifest.py',checker)
files={p.relative_to(V).as_posix():pin(p) for p in sorted(V.rglob('*')) if p.is_file()}
write(V/'MANIFEST.json',json.dumps({'schema':'pr190-qualified-verification/v1','UTC':t,'files':files,'self_excluded':'MANIFEST.json','claim_level':'Bare-angle exclusion false; adopted parity-selected exclusion proved. Nofirstness/author-intent correction certified.'},indent=2)+'\n')
# Actual portable packet execution, with receipts outside the sealed payload.
runs=[]
for argv in [[sys.executable,'-E','-S','-B','-P',str(V/'check_manifest.py')],[sys.executable,'-E','-S','-B','-P',str(V/'current/run_verification.py')]]:
 start=datetime.datetime.now(datetime.UTC).isoformat();r=subprocess.run(argv,capture_output=True);end=datetime.datetime.now(datetime.UTC).isoformat();require(r.returncode==0,r.stderr.decode(errors='replace'))
 runs.append({'argv':argv,'start_UTC':start,'end_UTC':end,'exit_code':r.returncode,'stdout_SHA256':hashlib.sha256(r.stdout).hexdigest(),'stderr_SHA256':hashlib.sha256(r.stderr).hexdigest(),'result':json.loads(r.stdout)})
z=P/'verification-package.zip'
with zipfile.ZipFile(z,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as out:
 for p in sorted(V.rglob('*')):
  if p.is_file():
   n=p.relative_to(V).as_posix();info=zipfile.ZipInfo(n,date_time=(2026,10,14,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED;info.external_attr=0o100444<<16;out.writestr(info,p.read_bytes())
with zipfile.ZipFile(z) as zz:
 require(zz.testzip() is None,'ZIP integrity');require(set(zz.namelist())==set(files)|{'MANIFEST.json'} and len(zz.namelist())==len(files)+1,'ZIP exact membership')
 for n,x in files.items():
  b=zz.read(n);require(len(b)==x['bytes'] and hashlib.sha256(b).hexdigest()==x['sha256'],'ZIP byte mismatch')
payloads={n:pin(P/n) for n in ['dodecahedron_endpoint.pdf','dodecahedron_endpoint.tex','verification-package.zip','zenodo-deposit.json','PACKAGE_README.md']}
write(P/'FINAL_REVIEW_PACKET_MANIFEST.json',json.dumps({'UTC':datetime.datetime.now(datetime.UTC).isoformat(),'PR':190,'original_head':'0c3346c8ebcb3b967a1d8bf9a283f027b44b738c','package_name':P.name,'payloads':payloads,'verification_payload_count':len(files),'ZIP_entries':len(files)+1,'historical_priority_clearance':False,'qualified_note_route_authorized':True,'whole_package_adversarial_reviews_complete':False,'Zenodo_published':False},indent=2)+'\n')
for p in P.rglob('*'):
 if p.is_file():p.chmod(0o444)
write(A/'PACKAGE_V1_ASSEMBLY_01.json',json.dumps({'UTC':datetime.datetime.now(datetime.UTC).isoformat(),'status':'EXACT_QUALIFIED_RESEARCH_NOTE_PACKET_ASSEMBLED_NEW_WHOLE_REVIEWS_PENDING','package':P.name,'PDF_pages':4,'artifact_operation_marker':'PDF create marker succeeded exactly once immediately before first authoring command; receipt records observation, not invented precise call time.','desktop_compiler':'success observed, existing unrelated editor preserved; no new tab opened','all4_PDF_pages_personally_viewed':True,'visual_check':'No clipping/collision/illegible equations/broken references; minor underfull bibliographic paragraph only. Inspected regenerable PNGs later removed under recorded disk cleanup; original final PDF retained.','actual_packet_checks':runs,'payloads':payloads,'ZIP_entries':len(files)+1,'actual_all_payload_modes_0444':True,'publication_ready':False,'published':False},indent=2)+'\n')
print(json.dumps({'status':'EXACT_PACKET_ASSEMBLED_NEW_WHOLE_REVIEWS_PENDING','payloads':payloads,'verification_files':len(files),'ZIP_entries':len(files)+1,'PDF_pages':4}))

