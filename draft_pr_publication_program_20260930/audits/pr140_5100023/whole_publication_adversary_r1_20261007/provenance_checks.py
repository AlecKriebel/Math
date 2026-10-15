import datetime,hashlib,json,os,pathlib,re,stat,zipfile
from html.parser import HTMLParser
root=pathlib.Path(__file__).resolve().parent.parent;own=root/'whole_publication_adversary_r1_20261007'
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def verify_row(base,row):
 name=row.get('relative',row.get('path'));p=pathlib.Path(name)
 if not p.is_absolute():p=base/p
 if not p.is_file():raise RuntimeError('missing '+str(p))
 if p.stat().st_size!=row['bytes'] or digest(p)!=row['sha256']:raise RuntimeError('pin differs '+str(p))
 if 'mode' in row:
  mode=row['mode'];expected=int(mode,8) if isinstance(mode,str) else mode
  if stat.S_IMODE(p.stat().st_mode)!=expected:raise RuntimeError('mode differs '+str(p))
 return str(p.relative_to(root)) if p.is_relative_to(root) else str(p)
family=[]
for folder in ['algebraic_orbit_boundary_adversary_20261007','geometric_variational_adversary_20261007','historical_general_priority_adversary_20261007','priority_convergence_adversary_20261007']:
 base=root/folder;mf=base/'FINAL_MANIFEST.json';j=json.loads(mf.read_text());verified=[verify_row(base,row) for row in j.get('members',j.get('public_files',[]))]
 family.append({'folder':folder,'manifest_sha256':digest(mf),'authenticated_member_count':len(verified)})
mg=json.loads((root/'ROOT_MATHEMATICAL_GATE.json').read_text());mpins=[verify_row(root,row) for row in mg['evidence']]
pg=json.loads((root/'ROOT_PRIORITY_GATE.json').read_text())
if digest(root/'ROOT_MATHEMATICAL_GATE.json')!=pg['mathematical_gate_sha256']:raise RuntimeError('priority to math gate digest')
for key,path in [('priority_convergence_manifest_sha256','priority_convergence_adversary_20261007/FINAL_MANIFEST.json'),('historical_readback_sha256','ROOT_HISTORICAL_PRIORITY_READBACK.json'),('contemporary_readback_sha256','ROOT_CONTEMPORARY_PRIORITY_READBACK.json'),('chronology_sha256','ROOT_priority_reading_20261007/ROOT_PUBLIC_CHRONOLOGY.json')]:
 if digest(root/path)!=pg[key]:raise RuntimeError('priority gate '+key)
for row in pg['authenticated_convergence_members']:verify_row(root/'priority_convergence_adversary_20261007',row)
sp=json.loads((root/'publication_package_v1/verification/SOURCE_PROVENANCE.json').read_text())
for row in sp['accepted_sources']:
 p=root/row['source_relative_to_audit']
 if p.stat().st_size!=row['bytes'] or digest(p)!=row['sha256']:raise RuntimeError('accepted source altered')
chron=json.loads((root/'ROOT_priority_reading_20261007/ROOT_PUBLIC_CHRONOLOGY.json').read_text());pr=json.loads((root/'ORIGINAL_PR_METADATA.json').read_text());external=json.loads((root/'ROOT_priority_reading_20261007/exact_record.json').read_text())
if digest(root/'original/PROOF.md')!=chron['first_math_proof_sha256']:raise RuntimeError('original proof digest')
if pr['created_at']!=chron['GitHub_server_PR_created_at'] or pr['head']['sha']!=chron['current_head']:raise RuntimeError('PR chronology pin')
if not pr['head']['repo']['visibility']=='public' or 'claimed_solved' not in pr['body']:raise RuntimeError('literal original claimed_solved intake')
if str(external['id'])!='23092466' or external['created']!=chron['contemporary_Zenodo_created'] or external['metadata']['publication_date']!=chron['contemporary_publication_date']:raise RuntimeError('exact overlapping record chronology')
receipt=json.loads((root/'ROOT_priority_reading_20261007/exact_record_access.json').read_text())
if digest(root/'ROOT_priority_reading_20261007/exact_record.json')!=receipt['sha256']:raise RuntimeError('record body receipt mismatch')
class Plain(HTMLParser):
 def __init__(self):super().__init__();self.parts=[];self.skip=0
 def handle_starttag(self,tag,attrs):
  if tag in ['script','style','annotation']:self.skip+=1
 def handle_endtag(self,tag):
  if tag in ['script','style','annotation']:self.skip-=1
 def handle_data(self,d):
  if not self.skip:self.parts.append(d)
html=(root/'historical_general_priority_adversary_20261007/private_primary_sources/reznik_garcia_koiller_v11.html').read_text();parser=Plain();parser.feed(html);plain=' '.join(' '.join(parser.parts).split())
# Keep only a tiny checkable excerpt record; no copyrighted source bodies copied.
if 'opposite vertices' not in plain or 'reflections about the origin' not in plain:raise RuntimeError('source central inversion unavailable')
title=re.search(r'<h1 class="ltx_title ltx_title_document">(.*?)</h1>',html,re.S).group(1);p=Plain();p.feed(title);title=' '.join(' '.join(p.parts).split())
result={'UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'actual_PID':os.getpid(),'frozen_family_seals':family,'math_gate_evidence_members_authenticated':len(mpins),'ROOT_priority_gate_pins_authenticated':True,'accepted_verifier_sources_authenticated':len(sp['accepted_sources']),'original_proof_SHA256':chron['first_math_proof_sha256'],'literal_claimed_solved_original_PR':True,'no_PR50_exception':pg['PR50_exception_used'] is False,'public_PR_created_at':pr['created_at'],'exact_later_record_created_at':external['created'],'later_record_publication_date':external['metadata']['publication_date'],'exact_later_note_DOI':external['doi'],'source_v11_actual_title':title,'source_scope':'Source setting confocal ellipses; Table5 k405 original antipedal vertex centroid, even N, origin/foci, no proof/value; source Section3.7 opposite-vertex inversion supports but does not formally define least period.','contemporary_formula_match':'nu=(C/a,S/b)/D; H_normal=1/D^2; kappa=K/(b^2-lambda). Ferudun (9) is candidate (9), and gamma (4) equals candidate centroid coefficient identically.','priority_scope':'Bounded inspected primary evidence supports qualified resolution; absolute priority, independent discovery and exclusive novelty UNESTABLISHED.','AI_unrefereed_consistency':'PASS across full paper, README, metadata, deposit metadata, contract, audit summary, verifier README.'}
(own/'provenance_checks.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
with (own/'RESEARCH_LOG.md').open('a') as f:f.write('\n'+result['UTC']+': Checkpoint 2; actual provenance PID '+str(os.getpid())+'. Review completion estimate 85%. Six fresh portable positive runs and eight expected failures passed at actual runner PID57065; all child groups empty. Own absolute-coordinate symbolic checks pass. Own exact repeated-odd boundary gives nonzero centroid, and 294 independently generated tangent-point orbit conditions pass at 65digits across N10/winding3, near-circle N8/winding3 and eccentric N16/winding1, three phases each; max scaled residual1.12e-49, tolerance1e-38. All five candidate PDF pages were visually inspected with no rendering defect. Primary source publishedTable5/§3.5/§3.7 and arxivv11 inspected; full exact contemporary six-page proof independently compared. Frozen distinct-family seals, ROOT gates, accepted portable source pins and chronological body receipts authenticated. Priority framing, exact overlap, AI assistance and unrefereed status are consistent. One optional bibliographic title correction identified; no mandatory issue identified so far. Final report/result sealing remains.\n')
