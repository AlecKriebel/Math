from pathlib import Path
import json,hashlib,datetime
R=Path(__file__).resolve().parent;C=R.parent;P=C/'publication_package_v3'
h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
checks=[];errors=[]
for family in ['whole_package_r1','whole_package_r2']:
 M=json.loads((C/family/'MANIFEST.json').read_text())
 for direction in ['inputs','outputs']:
  for name,pin in M[direction].items():
   p=Path(name)
   if not p.is_absolute():p=C/family/p
   ok=p.is_file() and p.stat().st_size==pin['bytes'] and h(p)==pin['sha256']
   checks.append({'review':family,'scope':direction,'path':str(p),'match':ok})
   if not ok:errors.append(str(p))
for version,record in [('publication_package_v1','PACKAGE_REVIEW_INPUT.json'),('publication_package_v2','PACKAGE_REVIEW_INPUT_V2.json'),('publication_package_v3','PACKAGE_REVIEW_INPUT_V3.json')]:
 x=json.loads((C/record).read_text())
 for name,pin in x['package_files'].items():
  p=C/version/name;ok=p.stat().st_size==pin['bytes'] and h(p)==pin['sha256']
  checks.append({'review':version,'scope':'frozen_package','path':str(p),'match':ok})
  if not ok:errors.append(str(p))
a=json.loads((C/'ROOT_R1_REPAIR_ACCEPTANCE.json').read_text());b=json.loads((C/'ROOT_R2_REPAIR_ACCEPTANCE.json').read_text());root=json.loads((C/'ROOT_PRIORITY_SYNTHESIS.json').read_text())
for family,a0,fields in [('whole_package_r1',a,{'REVIEW.md':'R1_report_sha256','MANIFEST.json':'R1_manifest_sha256'}),('whole_package_r2',b,{'REVIEW.md':'R2_report_sha256','RESULT.json':'R2_result_sha256','MANIFEST.json':'R2_manifest_sha256'})]:
 for file,key in fields.items():
  if h(C/family/file)!=a0[key]:errors.append('acceptance hash '+file)
for family,pins in root['family_report_sha256'].items():
 for file,digest in pins.items():
  if h(C/family/file)!=digest:errors.append('priority report hash '+family+'/'+file)
text=(P/'labelled_length_ratio.tex').read_text();note=(P/'SOURCES_AND_PRIORITY.md').read_text();code=(P/'verification/exact_reversal_counterexample.py').read_text()
repairs={'R1_L1_quotient_cover':all(s in text for s in ['smaller opposite-side quotient','Hubert--Schmidt','Lemma J']),
'R1_L2_actual_reflections':all(s in code for s in ['first_side1_reflection_collinear_with_AB','first_side1_reflection_positive_scale','final_side1_reflection_downwards']),
'R1_optional_unfolding':all(s in text for s in ['midpoint half-turn','perpendicular bisector']),
'R2_L1_global_locator':all(s in text for s in ['Immediately after Remark 3.4 on p.7','her p.20']) and all(s in note for s in ['after Remark3.4 on printedp7','Remark3.5 on printedp8']),
'R2_L2_genus_scope':'For \\(n\\ge5\\), every orientation-preserving affine automorphism' in text,
'physical_chart_weight_global':all(s in text for s in ['k\\equiv\\sigma K','(-1)^N k','w_n(k)=w_n(K)'])}
if not all(repairs.values()):errors.append('repair propagation')
# Inspect actual primary chronology records, not only audit conclusions.
zen=json.loads((C/'priority_exact_history/private_source_cache/zenodo_record.json').read_text())
pr=json.loads((C/'original_submission/PR.response.json').read_text())
original=C/'priority_exact_history/private_source_cache/github_pr152_original_candidate.md'
for s in ['hyperelliptic','sine','cusp']:
 if s not in original.read_text().lower():errors.append('original mechanism '+s)
chronology={'Zenodo_created':zen.get('created'),'Zenodo_doi':zen.get('doi'),'Zenodo_state':zen.get('state'),'Zenodo_submitted':zen.get('submitted'),'PR_created':pr.get('created_at'),'PR_head':pr.get('head',{}).get('sha'),'original_candidate_sha256':h(original),'competing_PDF_sha256':h(C/'priority_exact_history/private_source_cache/ferudun2026.pdf'),'files':[]}
for z in zen['files']:
 basename=z['key'];matchfiles={'paper.pdf':'ferudun2026.pdf','source.zip':'ferudun2026_source.zip','verification-report.md':'ferudun2026_verification.md'}
 # Resolve actual file names flexibly from the cached record.
 kind='ferudun2026.pdf' if basename.endswith('.pdf') else 'ferudun2026_source.zip' if basename.endswith('.zip') else 'ferudun2026_verification.md'
 p=C/'priority_exact_history/private_source_cache'/kind
 digest=hashlib.md5(p.read_bytes()).hexdigest();expected=z['checksum'].split(':')[-1];size=z.get('size',z.get('filesize'))
 ok=digest==expected and p.stat().st_size==size
 chronology['files'].append({'deposited_name':basename,'cache_name':kind,'size':size,'md5':digest,'match':ok})
 if not ok:errors.append('cached deposit '+basename)
if errors:raise RuntimeError(errors)
o={'UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS','checked_pins':checks,'counts':{fam:{d:sum(x['review']==fam and x['scope']==d for x in checks) for d in ['inputs','outputs']} for fam in ['whole_package_r1','whole_package_r2']},'all_old_current_package_pins_match':True,'repair_propagation':repairs,'historical_checkpoints_not_treated_as_current':True,'chronology':chronology,'errors':errors}
(R/'PRIOR_CONSISTENCY.json').write_text(json.dumps(o,indent=2)+'\n');print(json.dumps({'status':o['status'],'counts':o['counts'],'repairs':repairs,'chronology':chronology},indent=2))
