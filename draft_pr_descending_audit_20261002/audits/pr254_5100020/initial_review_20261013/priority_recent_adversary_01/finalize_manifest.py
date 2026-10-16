from pathlib import Path
import json,hashlib,datetime
ROOT=Path(__file__).resolve().parent
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
proof=ROOT.parent/'submitted/unsolved_math_prioritization/attempts/5100020/PROOF.md'
assert hashlib.sha256(proof.read_bytes()).hexdigest()=='ff2b1d78a1b94997d366d5173243ea95b949d5ae24574471639740b35cf2c16e'
original=[]
for path in sorted((ROOT/'sources/zenodo').glob('*.json')):
 d=json.loads(path.read_text())
 item={'record_id':d['id'],'doi':d.get('doi'),'title':d['metadata']['title'],'server_created':d['created'],'server_modified':d['modified'],'record_json_sha256':hashlib.sha256(path.read_bytes()).hexdigest()}
 main=ROOT/'sources/zenodo'/('original_'+str(d['id']))/'main.tex'
 if main.exists(): item['original_main_tex_sha256']=hashlib.sha256(main.read_bytes()).hexdigest()
 current={23079799:'amr-050-0021',23085904:'amr-050-0012',23087221:'amr-050-0014',23088516:'amr-050-0014',23077039:'amr-050-0019',23071366:'amr-050-0026',23092466:'amr-050-0023',23089778:'amr-050-0027',23090907:'amr-050-0029'}.get(d['id'])
 if current and main.exists(): item['current_main_tex_same_as_original']=main.read_bytes()==(ROOT/'sources/current_tex'/current/'main.tex').read_bytes()
 original.append(item)
prior204=json.loads((ROOT/'receipts/PR204_SOURCE_AUTHENTICATION.json').read_text())
prior_background=json.loads((ROOT/'receipts/BACKGROUND_SOURCE_AUTHENTICATION.json').read_text())['PRs']
prior_background=[x for x in prior_background if x['PR']!=110]
corrected110=[x for x in json.loads((ROOT/'receipts/SECONDARY_LEAD_RECEIPTS.json').read_text()) if x.get('PR')==110 and '/independent_review/'not in x['native_path']]
assert len(corrected110)==1
prior_background.append(dict(corrected110[0],id=5100032,initial_guessed_id=5100034,initial_path_guess_failed=True,recovered_from_native_changed_file_paths=True))
native=[]
for n in [204,254]:
 d=json.loads((ROOT/f'receipts/pr{n}.json').read_text()); native.append({'PR':n,'url':d['html_url'],'server_created':d['created_at'],'server_updated':d['updated_at'],'head_sha':d['head']['sha'],'commit_chronology':[{'sha':c['sha'],'git_author_date':c['commit']['author']['date'],'git_committer_date':c['commit']['committer']['date']} for c in json.loads((ROOT/f'receipts/pr{n}_commits.json').read_text())]})
checks=json.loads((ROOT/'receipts/ZENODO_ORIGINAL_RECEIPTS.json').read_text())+json.loads((ROOT/'receipts/ZENODO_21907170_RECEIPTS.json').read_text())
assert all(x.get('provider_checksum_matches',True) for x in checks)
zip_checks=[{k:x[k] for k in ['url','relative_path','bytes','sha256','provider_checksum','provider_checksum_matches'] if k in x} for x in checks if 'provider_checksum'in x]
pins={'utc':now,'candidate_input':{'PR':254,'head':'73efd1fb8ba2d3039ed6692b3ad1dfa1e3085755','proof_bytes':len(proof.read_bytes()),'proof_sha256':hashlib.sha256(proof.read_bytes()).hexdigest()},'native_PR_chronology':native,'credited_PR204_proof':prior204,'background_native_sources':prior_background,'original_archives':original,'deposited_file_pins':zip_checks,'all_provider_md5s_match':True,'third_party_source_bytes_excluded_from_public_content':True}
(ROOT/'PUBLIC_SOURCE_PINS.json').write_text(json.dumps(pins,indent=2)+'\n')
log=ROOT/'RESEARCH_LOG.md'
if '100% complete for the assigned bounded priority audit'not in log.read_text():
 log.write_text(log.read_text()+f'\n- {now}; 100% complete for the assigned bounded priority audit. Finished strongest adjacent full-source covering tests. Authenticated ten original Zenodo records/archives (including old21907170),21 current source ZIPs against metadata, and seven earlier repository proof sources. No earlier exact or covering odd-origin antipedal ratio was located; the two strongest transfer routes retain an unsupported construction-specific step and are blocked. Report/query ledger/source pins finalized. No global-firstness certificate, outreach, target mutation or publication performed. Background PR110 wrong-ID path guesses were corrected from native file paths; an expanded Zenodo query400 was followed by a successful plain query200; the target-page403 and PDF-xref recovery warning remain recorded access/extraction limitations, not mathematical failures.\n')
public=[]
for p in sorted(ROOT.iterdir()):
 if p.is_file() and p.name not in ['FINAL_AUDIT_MANIFEST.json']:
  data=p.read_bytes();public.append({'relative_path':p.name,'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()})
manifest={'utc':now,'verdict':'NO_COVERING_PRIOR_RESULT_LOCATED_IN_BOUNDED_PRIMARY_AUDIT','priority_scope_completion_percent':100,'not_absolute_priority_certificate':True,'mathematical_validation_deferred_to_separate_audits':True,'public_files':public,'excluded_reading_only_directories':['sources/','receipts/'],'candidate_proof_sha256':hashlib.sha256(proof.read_bytes()).hexdigest()}
(ROOT/'FINAL_AUDIT_MANIFEST.json').write_text(json.dumps(manifest,indent=2)+'\n')
print(json.dumps({'utc':now,'public_file_count':len(public),'report_sha256':hashlib.sha256((ROOT/'REPORT.md').read_bytes()).hexdigest(),'manifest_sha256':hashlib.sha256((ROOT/'FINAL_AUDIT_MANIFEST.json').read_bytes()).hexdigest(),'provider_checks_all_match':True},indent=2))
