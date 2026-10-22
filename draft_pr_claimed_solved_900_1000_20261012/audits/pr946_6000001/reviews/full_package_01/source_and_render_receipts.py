import sys
if not sys.flags.safe_path:raise SystemExit('safe startup')
import pathlib,json,hashlib,datetime,subprocess
R=pathlib.Path('/Users/alec/Documents/Math');A=R/'draft_pr_claimed_solved_900_1000_20261012/audits/pr946_6000001';W=A/'reviews/full_package_01'
def fp(p):
 b=p.read_bytes();return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
# Authenticate the exact earlier family reports and every curated payload, as
# pinned by the already independently checked frozen candidate package.
f=json.loads((A/'preprint/FREEZE.json').read_text());family=[]
for name in ['jet_calculus','global_hessian','global_adversary','source_model','reproducibility','classical_priority','recent_priority','priority_falsifier']:
 folder=A/'reviews'/name;m=json.loads((folder/'MANIFEST.json').read_text());key=next(k for k in ['files','curated_files','public_files','payloads'] if k in m);v=m[key];rows=v if type(v) is list else [{'path':k,**r} for k,r in v.items()]
 for record in rows:
  p=folder/record['path'];want={k:record[k] for k in ['bytes','sha256']}
  if fp(p)!=want:raise ValueError('family payload '+str(p))
  frozen_name='package/reviews/'+name+'/'+record['path']
  if frozen_name in f['files'] and f['files'][frozen_name]!=want:raise ValueError('frozen family mismatch')
 family.append({'family':name,'manifest':fp(folder/'MANIFEST.json'),'curated_payloads':len(rows),'status':'PASS'})
(W/'FAMILY_AUTHENTICATION.json').write_text(json.dumps({'status':'PASS','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'families':family},indent=2)+'\n')
# Metadata/fingerprints only. No third-party body, text extraction, or image is
# copied into this public receipt.
readings=[
('FMU1998','reviews/classical_priority/private/fmu1998.pdf','https://www.jstage.jst.go.jp/article/iis/4/2/4_2_125/_pdf/-char/en','p125 item1(a), footnote1; actual page image inspected; source question matches.'),
('Amari1997','reviews/classical_priority/private/amari1997.pdf','https://bsi-ni.brain.riken.jp/database/file/166/169.pdf','Actual page images82,84,87 inspected: torsion-free duality, torsion+curvature flatness, local dual coordinates, embedding question1.'),
('LauritzenIMS1987','reviews/classical_priority/private/lauritzen1987_body.pdf','https://doi.org/10.1214/lnms/1215467061','Statistical/cubic/dual framework and pp175-176 orthogonal induced connection inspected; this is not the separate Lancaster note.'),
('Matumoto1993','reviews/classical_priority/private/matumoto1993_body.pdf','https://doi.org/10.32917/hmj/1206128255','Full6page text read, Theorem1p328 and proof329-331; compatible3jets/global contrast and explicit separate1flat embedding question.'),
('Whitney1936','reviews/global_hessian/private/sources/whitney1936.pdf','https://doi.org/10.2307/1968482','Actualp665/Lemma19/footnote32 image read:2n+1 embedding and reciprocal-radius proper version.'),
('Gualtieri2017','reviews/global_hessian/private/sources/gualtieri2017part11.pdf','https://math.toronto.edu/mgualt/courses/17-1300/docs/17-1300-notes-11.pdf','Actualpp43-44 images read: Def3.53 variable positive radius, normaladdition, Theorem3.54 and proof.'),
('Le2003long','reviews/classical_priority/private/le2003_43.pdf','https://files-www.mis.mpg.de/mpi-typo3/preprints/2003/preprint2003_43.pdf','pp33-39 free-map/jet/right-inverse mechanism read, especially Proposition5.13 minimum-norm choicep36; old noncompact globalization comparison read separately.'),
('Le2003short','reviews/classical_priority/private/le2003_77.pdf','https://files-www.mis.mpg.de/mpi-typo3/preprints/2003/preprint2003_77.pdf','pp3-6 exact noncompact compactification/product map argument read; common exterior values/derivatives not supplied by the displayed independent placements.'),
('Le2016v6','reviews/classical_priority/private/le_v6.pdf','https://arxiv.org/abs/math/0506163v6','Actualpp14-15,22-23 read: compact MainTheorem, compactTheorem5.1 uniform scale and compactTheorem5.6. Fresh official arXiv revision comment independently confirms compactness added.'),
('Marugame2021accepted','reviews/recent_priority/private/marugame_uec.pdf','https://uec.repo.nii.ac.jp/record/10333/files/Bonnet_thm_statistical_mfd.pdf','pp2-6 full definitions and completeTheorem2.2 proof read. Local-only pair equivalence; positive transversequadratic antecedent. Accepted body distinguished from finalVOR.'),
('LoiMatta2023accepted','reviews/recent_priority/private/loi_matta_accepted.pdf','https://doi.org/10.1016/j.topol.2023.108438','Actualacceptedcover, Theorem1 plus Proposition5 minimum-norm inverse read. StartsalreadyNinduced; no universal prescribed-data existence. FinalVOR gap retained.'),
('Osipov2112v2','reviews/recent_priority/private/osipov2021_v2.pdf','https://arxiv.org/abs/2112.06686v2','Theorem2.12 and orthogonal positivecone decomposition read: genuine global predecessor under its constantcurvature hypothesis.'),
('Osipov2209v3','reviews/recent_priority/private/osipov2022_v3.pdf','https://arxiv.org/abs/2209.02357v3','Theorem3.16p14 actualtext read, globalradiantHessiancone; curvatureconstraint is the relevant restriction.'),
('AJLS2017p222','reviews/priority_falsifier/private/ajls2017_authorized_preview_p222.png','https://books.google.com/books?id=pLsyDwAAQBAJ&pg=PA222','Actualauthorizedpageimage personallyread: Theorem4.10 finitecompact/countablenoncompact. Statement-accessgap resolved.'),
('AJLS2017p237','reviews/priority_falsifier/private/ajls2017_authorized_preview_p237.png','https://books.google.com/books?id=pLsyDwAAQBAJ&pg=PA237','Actualauthorizedpageimage personallyread: countablymany blocks with squaredradiisumming4, no finiteambient reduction claimed.'),
('AJLS2017p238','reviews/priority_falsifier/private/ajls2017_authorized_preview_p238.png','https://books.google.com/books?id=pLsyDwAAQBAJ&pg=PA238','Actualauthorizedpageimage personallyread: Theorem4.11 finitecompact/countablenoncompact embedding, proofstart. p239unavailable; no fullproof certification.')]
items=[]
for key,name,url,what in readings:items.append({'id':key,'url':url,'private_repository_path':str((A/name).relative_to(R)),**fp(A/name),'actual_reading':what})
# Current source-map anchors for the exact primary identities.
sm=json.loads((A/'reviews/source_model/SOURCE_MAP.json').read_text())['sources']
for key,rel in [('fmu1998','reviews/classical_priority/private/fmu1998.pdf'),('amari1997','reviews/classical_priority/private/amari1997.pdf'),('le_v6','reviews/classical_priority/private/le_v6.pdf')]:
 if fp(A/rel)!={k:sm[key][k] for k in ['bytes','sha256']}:raise ValueError('primary prior anchor '+key)
ghsources=json.loads((A/'reviews/global_hessian/SOURCE_AUTHENTICATION.json').read_text())['sources']
for source in ghsources:
 if fp(A/'reviews/global_hessian'/source['private_pdf'])!={k:source[k] for k in ['bytes','sha256']}:raise ValueError('global primary anchor')
(W/'PRIMARY_SOURCE_REVIEW.json').write_text(json.dumps({'status':'PASS','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'sources':items,'source_body_copies':'none; previously retrieved private primary objects inspected in place','material_access_gaps':['Le2006finalbody','Le2007finalbody','LauritzenLancaster1987separatebody','Abe1994body','AJLSfullchapter/p239','Marugame/LoiMattafinalVOR','Amari2021reviewbody'],'priority_claim':'Bounded review; neither historical firstness nor current openness certified; no new full unrestricted predecessor established.'},indent=2)+'\n')
pages=[]
for i in range(1,7):pages.append({'page':i,'render':fp(W/f'private/page-{i}.png'),'visually_inspected':True,'layout':'legible, no clipping/overlap/unresolvedcitation observed'})
metadata=json.loads((A/'preprint/zenodo-deposit.json').read_text())['metadata']
(W/'PDF_RENDER_REVIEW.json').write_text(json.dumps({'status':'PASS_WITH_OPTIONAL_METADATA_PORTABILITY_IMPROVEMENT','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'pdf':fp(W/'private/cold/research_note.pdf'),'TeX':fp(A/'preprint/research_note.tex'),'fresh_render_command':'pdftoppm -r110 -png [cold_extracted_actual_pdf] [own_private_page_prefix]','all_pages':pages,'author':'Alec Kriebel','ORCID':'0009-0001-9320-500X','date':'October15,2026','descriptor_version':metadata['version'],'descriptor_license':metadata['license'],'disclosure':'ExtensiveAI research/writing/verification, unrefereed, no independenthuman peerreview or formalproofcertification are explicit.','optional_issue':'FP01-DOC-001: standalone PDF has author/ORCID/date and disclosure, but no visible version1.0 or CC-BY4.0 license notice; descriptor carries both.'},indent=2)+'\n')
print('PASS family, primary metadata, and6page render receipts')
