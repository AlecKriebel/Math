"""Seal this new analytic lane; never mutates original inputs or earlier packages."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,zipfile
P=Path('/Users/alec/Documents/Math/research_website_catalogue_20261024');paper=P/'papers/23442760';A=paper/'reviews/analytic'
now=lambda:datetime.now(timezone.utc).isoformat()
sha=lambda f:hashlib.sha256(Path(f).read_bytes()).hexdigest()
def dump(name,o):(A/name).write_text(json.dumps(o,indent=2,ensure_ascii=False)+'\n')
def binding(f):return {'bytes':f.stat().st_size,'sha256':sha(f)}
before=json.loads((A/'inputs-before.json').read_text())['bindings'];sourcechecks=[]
for b in before:
 f=Path(b['path']);assert f.stat().st_size==b['bytes'] and sha(f)==b['sha256'],f
 sourcechecks.append({**b,'unchanged':True})
sm=json.loads((paper/'sources/SOURCE_READY_MANIFEST.json').read_text())
for b in sm['files']:
 f=paper/'sources'/b['path'];assert f.stat().st_size==b['bytes'] and sha(f)==b['sha256']
assert sha(paper/'sources/SOURCE_READY.json')=='b3b01936d1b1ce7ce7ab88b0082b92399ebf663d2dcddc81fc50aa72250db8b2'
assert sha(paper/'sources/SOURCE_READY_MANIFEST.json')=='445d0532cc31dfca48ade7cf207d5439d83a0da13dc66f4c0451a12db3912c79'
assert sha(paper/'sources/SOURCE_READY_SEAL.json')=='002b8324c97eb11428fa6b747f7b749ea4a1301c953acdb425f19dc168b87da5'
zipchecks=[]
with zipfile.ZipFile(paper/'sources/Convex_Body_SOS_Density_Verification_v1.0.zip') as z:
 for i in z.infolist():
  if i.is_dir():continue
  f=paper/'sources/published-source'/i.filename;data=z.read(i)
  assert f.is_file() and f.read_bytes()==data,(i.filename,'member')
  zipchecks.append({'member':i.filename,'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest(),'matches_frozen_extraction':True})
assert len(zipchecks)==152
initial=json.loads((A/'INITIAL_SEAL.json').read_text())
assert sha(A/'INITIAL_SEAL.json')=='9c10db79da7084354663bcad68d5831a1b760e1457c43b4de997a84c98d8a994'
for b in initial['bindings']:assert sha(b['path'])==b['sha256']
# Preserve only former owned outputs and their manifests/seals. Do not follow stale source/site/core input maps.
protected={};packages=[]
for label in ['quadratic','bosonic','slit-gaussian','surreal-cone-brownian','dipole-langlands','cubic-fps-hessian']:
 d=P/f'verification/local-{label}-stage-sol-20261025';m=d/'stage-readiness-manifest.json';o=json.loads(m.read_text());owned=o.get('owned_output_bindings',o.get('artifacts'))
 assert isinstance(owned,dict)
 count=0
 for name,b in owned.items():
  f=Path(name) if Path(name).is_absolute() else d/name
  assert f.is_file() and sha(f)==(b['sha256'] if isinstance(b,dict) else b),(label,name)
  protected[str(f)]=binding(f);count+=1
 for f in d.glob('*'):
  if f.is_file() and ('seal' in f.name.lower() or f==m):protected[str(f)]=binding(f)
 packages.append({'package':str(d),'owned_output_count_verified':count,'manifest_sha256':sha(m),'stale_input_bindings_followed':False})
d=P/'redirects/cubic-hessian-preflight-sol-20261025';m=d/'MANIFEST.json';o=json.loads(m.read_text())
for name,b in o['owned_output_bindings'].items():
 f=d/name;assert sha(f)==b['sha256'];protected[str(f)]=binding(f)
for f in [m,d/'SEAL.json',d/'SEAL.sha256']:protected[str(f)]=binding(f)
for rid in ['23444606','23440119','23224103','23204952','22983138','23409904']:
 d=P/f'papers/{rid}/reviews/editorial'
 for f in d.glob('*'):
  if f.is_file() and (f.name in ['MANIFEST.json','SEAL.json','SEAL.sha256']):protected[str(f)]=binding(f)
for f in [P/'papers/23129302/reviews/analytic/SEAL.json',P/'papers/22983138/reviews/analytic/SEAL.json',P/'redirects/fps-legacy-identity-preflight-root-20261025.json']:
 if f.exists():protected[str(f)]=binding(f)
primary=json.loads((A/'PRIMARY_ACCESS.json').read_text())
for b in primary['bodies']:assert sha(b['path'])==b['sha256']
reads=[
 {'path':str(paper/'sources/Convex_Body_SOS_Density_Note_v1.0.pdf'),'extent':'entire actual 5 pages, extracted text plus controlling TeX cross-check','before_independence_seal':True},
 {'path':str(paper/'sources/published-source/manuscript/main.tex'),'extent':'entire 15887 bytes including abstract/theorem/proofs/limits/references','before_independence_seal':True},
 {'path':str(paper/'sources/SOURCE_READY.json'),'extent':'entire technical custody object; SOURCE_READY_SEAL entire; SOURCE_READY_MANIFEST machine-authenticated all entries','before_independence_seal':True},
 {'path':str(paper/'sources/published-source/current_edition/PROOF.md'),'extent':'entire, including historical attribution/status paragraphs; read only after independent derivation and actual primary reading began; opinions not adopted','before_independence_seal':False},
 {'path':str(paper/'sources/published-source/current_edition/MOMENT_FORMULATION.md'),'extent':'entire; monomial/moment-pencil/witness derivation independently checked analytically','before_independence_seal':False}]
for b in reads:b['sha256']=sha(b['path'])
primary_extents={
 'owr2018-50':{'extent':'complete Laurent contribution printed2991–2993/PDF23–25 (not full 56-page multi-author report); actualPDF23 rendered for normalization; adjacent next-title text incidental','extracted_lines_read':[[858,1055],[1054,1070]]},
 'slot-laurent-v2':{'extent':'Eq3/degree convention; parameter definitions; Lemmas1,3,4 and proofs; Thm11/assumption context; complete Section4.3 proof including Lemmas15–20/Cor5; conclusions C2 extension/acceleration/openquestions. Not entire30pages. A combined output truncated its tail; missing relevant Thm11/conclusion passages re-read in smaller commands.','extracted_lines_read':[[40,145],[253,380],[1155,1235],[1612,1940],[2113,2185],[2190,2245]]},
 'deklerk-laurent-annealing-v1':{'extent':'Cor4.3 statement and complete quadratic-proxy proof, PDF7–8; not full12pages','extracted_lines_read':[[415,478]]},
 'deklerk-laurent-worst-v1':{'extent':'Section3.1 target setup/Thm3.1/Cors3.2–3.3 and complete proofs, PDF8–9; not full17pages','extracted_lines_read':[[495,645]]},
 'totik-varga-published':{'extent':'Thm2.1 all hypotheses/full proof, PDF2–4; Section3 definitions/Thms3.1/3.2 and relevant upper-proof core/shell passage throughEq3.13, PDF5–8; actualPDF2 rendered. Not entire13pages; remaining Thm3.1 lower/other tail argument not represented as read.','extracted_lines_read':[[87,358],[420,775]]},
 'laurent-slot-overview-final':{'extent':'normalized hierarchy/Table1 plus nearby context, PDF9–11; proxy/eigenvalue/univariate/needle strategy discussion PDF13–17; not full28pages','extracted_lines_read':[[420,522],[580,735]]}}
for b in primary['bodies']:b.update(primary_extents[b['name']])
dump('READ_LEDGER.json',{'utc':now(),'actual_and_support':reads,'primary_bodies':primary['bodies'],'not_read':['all current sibling/root scientific review reports','historical audit/review reports except incidental status paragraphs within the explicitly listed current-edition PROOF.md','all submitted code bodies; no submitted programs executed'],'reading_is_not_equated_to_hashing':True,'early_seal_sha256':sha(A/'INITIAL_SEAL.json')})
dump('DERIVATION_LEDGER.json',{'utc':now(),'universal_derivations':[{'claim':'literal universal main theorem','artifact':'REPORT.md','mechanism':'constrained Taylor + homothetic relative mass + finite endpoint kernel + same-core cancellation + all-r degree normalization','status':'complete analytic reconstruction'},{'claim':'interval/product lower proposition','artifact':'REPORT.md and DERIVATIONS.md','mechanism':'all-degree Rodrigues/Legendre evaluation bound + mass cap + fiberwise marginal','status':'complete analytic reconstruction'},{'claim':'stated deduction from Totik–Varga older ingredients','artifact':'DERIVATIONS.md','mechanism':'actual a=0/psi=sqrt hypotheses + Markov core + dyadic relative-volume summation + degree','status':'complete contextual deduction; not claim of earlier printed full theorem'}],'finite_diagnostics':'EXACT_DIAGNOSTICS.json','finite_checks_replace_universal_proof':False,'submitted_code_inspected_or_run':False,'reason':'not needed for the complete manuscript analytic proof; independent code only'})
checks=json.loads((A/'EXACT_DIAGNOSTICS.json').read_text());assert len(checks['checks'])==150 and all(x['passed'] for x in checks['checks']);assert len(checks['negative_controls'])==7 and all(x['detected'] for x in checks['negative_controls'])
dump('VERDICT.json',{'record_id':23442760,'lane':'independent analytic proof reconstruction','status':'COMPLETE_ANALYTIC_SUPPORTED_WITH_EXPLICIT_SCOPE_LIMITS','mathematical_disposition':'literal main theorem and interval/product lower proposition supported; no central defect located','strongest_verified_result':{'universal_upper':'For each n>=1, every fixed full-dimensional compact convex K and real polynomial f, every integer r>=1 has unit-Lebesgue-mass single-global-square SOS witness of root total degree<=r and error<=4(n+2)^2(pi/2)^(2n+4)(1+2^(n+2))G/r^2.','lower':'H_r(t,[0,1]x[-1,1]^(n-1))>=1/[4(r+1)^2] for every fixed n>=1 and integer r>=1.','extension':'C2 objectives on an open neighborhood of K by the same quadratic proxy'},'central_gap':None,'priority_status':'not established by this analytic lane; classical proxy/localization/relative-mass/lower-rate mechanisms credited; no firstness or current worldwide openness certified','boundaries':['Lebesgue measure; no arbitrary-reference-measure transfer','compact convex full-dimensional K','fixed n,K,f; no uniform geometry/dimension/objective-independent constant','full SOS hierarchy; not general original-objective-polynomial restriction','existence uses global minimizer a; no efficient location/integration method','worst-case lower exponent only, not positive lower rate for every objective','finite checks are not a universal/formal proof certificate'],'independence':{'initial_seal_sha256':sha(A/'INITIAL_SEAL.json'),'before_historical_or_sibling_root_opinions_and_external_primary_bodies':True,'current_sibling_root_reports_read':False},'checks':{'exact_passed':150,'changed_assumption_controls_detected':7,'original_programs_executed':False,'formal_certificate':False},'followup':None,'AA':None,'all_publication_native_browser_live_gates':False,'programme_goal_complete':False,'completion_estimate_percent':100})
with (A/'RESEARCH_LOG.md').open('a') as f:
 f.write(now()+' — Actual primary hypotheses/proofs and normalization interface checked; complete universal main/lower reconstructions remain supported. Exact tests150 plus seven changed-assumption controls pass. First-run JSON serialization error corrected; no mathematical assertion changed. Completion estimate85%.\n')
 f.write(now()+' — Final report/derivations/custom verdict/read/access ledgers complete; source/member/early-seal and prior owned-package preservation rechecked. No central defect, no follow-up, no publication decision. Completion estimate100% for analytic lane; programme203 ongoing.\n')
dump('custody.json',{'utc':now(),'original_sources_before_after':sourcechecks,'source_ready_manifest_all_entries_verified':len(sm['files']),'archive_member_comparisons':zipchecks,'primary_body_bindings':primary['bodies'],'early_seal_preserved':True,'protected_prior_packages':packages,'protected_prior_owned_bindings':protected,'stale_site_core_baselines_followed':False,'original_writes':False,'source_config_shared_site_native_browser_git_deploy_redirect_release_outreach_actions':False,'only_new_analytic_namespace_written':True})
# Report and internal consistency controls.
r=(A/'REPORT.md').read_text();assert all(t in r for t in ['same F(h)','No central mathematical gap','every integer r>=1','1/[4(r+1)^2]','no new environment','firstness'])
assert len(zipchecks)==152 and all(x['unchanged'] for x in sourcechecks)
exclude={'MANIFEST.json','SEAL.json','SEAL.sha256'}
owned={str(f.relative_to(A)):binding(f) for f in sorted(A.rglob('*')) if f.is_file() and f.name not in exclude}
manifest={'utc':now(),'status':'COMPLETE_INDEPENDENT_ANALYTIC_HANDOFF','record_id':23442760,'completion_estimate_percent':100,'original_source_bindings_unchanged':True,'owned_output_bindings':owned,'private_primary_cache_complete_directory_ignored':True,'excluded_self_and_seals':sorted(exclude),'root_and_publication_adjudication_separate':True}
dump('MANIFEST.json',manifest)
seal={'utc':now(),'status':'IMMUTABLE_COMPLETE_ANALYTIC_REVIEW','manifest':'MANIFEST.json','manifest_sha256':sha(A/'MANIFEST.json'),'report_sha256':sha(A/'REPORT.md'),'verdict_sha256':sha(A/'VERDICT.json'),'early_seal_sha256':sha(A/'INITIAL_SEAL.json'),'owned_output_count':len(owned),'source_original_count':len(sourcechecks),'archive_regular_members_compared':len(zipchecks),'protected_prior_owned_and_seal_count':len(protected),'publication_or_native_pass':False}
dump('SEAL.json',seal);(A/'SEAL.sha256').write_text(sha(A/'SEAL.json')+'  SEAL.json\n')
print(json.dumps({**seal,'seal_sha256':sha(A/'SEAL.json')}))
