#!/usr/bin/env python3
"""Strict explicit-guard verifier usable in a clean support archive extraction."""
from pathlib import Path,PurePosixPath
import argparse,hashlib,json,re,stat,zipfile
ROOT=Path(__file__).resolve().parent
FIXED_TIME=(2026,10,14,0,0,0)
def require(c,m):
 if not c:raise ValueError(m)
def sha(data):return hashlib.sha256(data).hexdigest()
def load(name):return json.loads((ROOT/name).read_text(encoding='utf-8'))
def safe(name):
 require(isinstance(name,str) and name and '\\' not in name and '\x00' not in name,'unsafe member name')
 p=PurePosixPath(name)
 require(not p.is_absolute() and '..' not in p.parts and '.' not in p.parts and str(p)==name,'unsafe relative path '+name)
 return name

def local_regular(name):
 name=safe(name);p=ROOT/name
 require(p.is_file() and not p.is_symlink(),'missing/symlink member '+name)
 require(all(not (ROOT/Path(*Path(name).parts[:i])).is_symlink() for i in range(1,len(Path(name).parts)+1)),'symlink in member ancestry '+name)
 require(stat.S_ISREG(p.lstat().st_mode),'nonregular member '+name)
 return p

def check():
 # Bootstrap the allowlist only after guarding the allowlist file itself.
 local_regular('SUPPORT_ALLOWLIST.json')
 allow=load('SUPPORT_ALLOWLIST.json')['members'];require(allow==sorted(set(allow)),'allowlist must be sorted and unique')
 for name in allow:safe(name)
 require('SUPPORT_MANIFEST.json' in allow,'manifest missing from allowlist')
 # Guard every local member before reading any remaining allowlisted bytes.
 # The manifest is excluded only from self-hashing, never from path safety.
 for name in allow:local_regular(name)
 manifest=load('SUPPORT_MANIFEST.json');records=manifest['entries']
 require([r['path'] for r in records]==[x for x in allow if x!='SUPPORT_MANIFEST.json'],'manifest exact coverage failed')
 for record in records:
  name=safe(record['path']);p=ROOT/name
  data=p.read_bytes();require(len(data)==record['bytes'] and sha(data)==record['sha256'],'hash mismatch '+name)
  if name!='paper.pdf':data.decode('utf-8')
 require((ROOT/'paper.pdf').read_bytes().startswith(b'%PDF-'),'paper PDF signature missing')
 excluded=set(load('EXCLUSION_LEDGER.json')['local_package_files'])
 for p in ROOT.rglob('*'):
  if not p.is_file():continue
  name=p.relative_to(ROOT).as_posix()
  if name.startswith('tmp/'):continue
  require(name in allow or name in excluded,'unmanifested file '+name)
 copies=load('COPY_MAP.json')['copies']
 for c in copies:
  require(c['package_path'] in allow,'copy not distributed')
  data=(ROOT/c['package_path']).read_bytes()
  require(sha(data)==c['sha256'] and len(data)==c['bytes'],'copy map mismatch')
 require(sum(c['source_path'].startswith('submitted/') for c in copies)==9,'original nine-copy coverage failed')
 require(load('SAFE_INPUT_PINS.json')['records']==copies,'selected input pins mismatch')
 meta=load('metadata.json');require(load('publication/release_metadata.json')['metadata']==meta and load('publication/zenodo.json')['metadata']==meta,'normalized metadata differ')
 status=load('STATUS.json')
 require(status['publication_ready'] is False and status['issues_updated'] is False,'pending preparation gate altered')
 require(status['whole_package_reviews_completed']==0 and status['whole_package_reviews_required']>=2,'new review gate altered')
 require(status['novelty']=='UNKNOWN' and status['historical_priority']=='UNKNOWN','novelty boundary altered')
 current=load('CURRENT_STATUS.json')
 require(current['stage']=='PENDING_NEW_WHOLE_02' and current['snapshot_date']=='2026-10-14','current stage altered')
 require(current['publication_ready'] is False and current['issues_updated'] is False,'current pending gate altered')
 require(current['whole_package_reviews_completed']==1 and current['whole_package_reviews_required']>=2,'current new review gate altered')
 require(current['ascending_publication_hold_after_pr']==1032,'ascending publication hold altered')
 latest=load('CURRENT_STATUS_WHOLE03.json')
 require(latest['stage']=='PENDING_NEW_WHOLE_03' and latest['snapshot_date']=='2026-10-14','latest stage altered')
 require(latest['publication_ready'] is False and latest['issues_updated'] is False,'latest pending gate altered')
 require(latest['whole_package_reviews_completed']==2 and latest['whole_package_reviews_required']>=2,'latest new review gate altered')
 require(latest['ascending_publication_hold_after_pr']==1032,'latest ascending hold altered')
 terminal=load('TERMINAL_STATUS.json')
 require(terminal['stage']=='READY_FOR_SUBMISSION_UNPUBLISHED_HELD_AFTER_1032' and terminal['snapshot_date']=='2026-10-14','terminal stage altered')
 require(terminal['whole_package_reviews_completed']==3 and terminal['whole_package_reviews_required']>=2,'terminal complete-review count altered')
 require(terminal['actionable_P0_P1_P2_P3']==0 and terminal['ready_for_submission_after_root_adoption'] is True,'terminal clean-review readiness altered')
 require(terminal['root_terminal_adoption_required'] is True and terminal['publication_ready'] is False and terminal['published'] is False and terminal['issues_updated'] is False,'terminal adoption/publication gate altered')
 require(terminal['ascending_publication_hold_after_pr']==1032,'terminal ascending hold altered')
 require(terminal['novelty']=='UNKNOWN' and terminal['historical_priority']=='UNKNOWN','terminal novelty boundary altered')
 review=load('support/history/reviews/package_03/VERDICT.json')
 require(review['verdict']=='ZERO_ACTIONABLE_FINDINGS' and all(review['severity_counts'][s]==0 for s in ['P0','P1','P2','P3']),'terminal complete-review verdict altered')
 adoption=load('support/history/ROOT_WHOLE_PACKAGE_REVIEW_03.json')
 require(adoption['whole_reviews_completed']==3 and adoption['minimum_whole_reviews']>=2 and adoption['actionable_P0_P1_P2_P3']==0,'terminal ROOT review adoption altered')
 repaired=load('REPAIR_STATUS_CASE_ALIAS01.json')
 require(repaired['stage']=='PENDING_ROOT_CASE_ALIAS_REPAIR_ADOPTION_AND_NEW_COMPLETE_WHOLE04' and repaired['snapshot_date']=='2026-10-16','case-alias repair stage altered')
 require(repaired['whole_package_reviews_completed']==3 and repaired['whole_package_reviews_required']>=2 and repaired['latest_prior_complete_review_actionable_P0_P1_P2_P3']==0,'prior review count or verdict altered')
 require(repaired['bounded_repair_applied'] is True and repaired['new_complete_whole04_required'] is True and repaired['root_repair_adoption_required'] is True and repaired['focused_validation_is_complete_whole_review'] is False,'required fresh review/adoption altered')
 require(all(repaired[k] is False for k in ['ready_for_submission','publication_ready','published','issues_updated']),'current repair gate altered')
 require(repaired['ascending_publication_hold_after_pr']==1032 and repaired['novelty']=='UNKNOWN' and repaired['historical_priority']=='UNKNOWN','repair hold or novelty boundary altered')
 # Earlier status checks above preserve their dated historical states.
 dated=load('TERMINAL_STATUS_20261016.json')
 require(dated['stage']=='TERMINAL_ADMIN_COMPLETE_PENDING_ROOT_EXTERNAL_FINAL_INTEGRITY' and dated['snapshot_date']=='2026-10-16','dated terminal stage altered')
 require(dated['whole_package_reviews_completed']==4 and dated['whole_package_reviews_required']==2,'dated terminal complete-review count altered')
 require(dated['latest_complete_review']=='support/history/reviews/package_04/VERDICT.json' and dated['root_complete_review_adoption']=='support/history/ROOT_WHOLE_PACKAGE_REVIEW_04.json','dated terminal review pointers altered')
 require(dated['actionable_P0_P1_P2_P3']==0 and dated['latest_complete_review_root_adopted'] is True and dated['new_complete_whole_review_currently_required'] is False,'dated terminal whole-review adoption altered')
 require(dated['root_terminal_administration_adoption_required'] is True and dated['root_external_final_integrity_required'] is True,'dated terminal ROOT integrity gate altered')
 require(all(dated[k] is False for k in ['ready_for_submission','publication_ready','published','issues_updated','issues_resolved']),'dated terminal readiness/publication gate altered')
 require(dated['ascending_publication_hold_after_pr']==1032 and dated['novelty']=='UNKNOWN' and dated['historical_priority']=='UNKNOWN','dated terminal hold or novelty boundary altered')
 require(dated['individual_unsupported_historical_reference_occurrences']==5 and dated['universal_historical_pointer_authentication_claim'] is False,'dated historical qualification altered')
 latest_review=load(dated['latest_complete_review'])
 require(latest_review['verdict']=='ZERO_ACTIONABLE_FINDINGS' and latest_review['this_complete_whole_review_ordinal']==4 and latest_review['minimum_whole_reviews']==2 and all(latest_review['severity_counts'][s]==0 for s in ['P0','P1','P2','P3']),'dated latest complete-review verdict altered')
 latest_adoption=load(dated['root_complete_review_adoption'])
 require(latest_adoption['status']=='ADOPT_COMPLETE_WHOLE04_ZERO_ACTIONABLE_PENDING_TERMINAL_ADMIN' and latest_adoption['whole_reviews_completed']==4 and latest_adoption['minimum_whole_reviews']==2 and latest_adoption['actionable_P0_P1_P2_P3']==0,'dated ROOT whole04 adoption altered')
 require(latest_adoption['terminal_administration_and_NEW_external_final_integrity_required'] is True and latest_adoption['publication_ready'] is False and latest_adoption['published'] is False and latest_adoption['services_held_after_pr']==1032,'dated ROOT whole04 terminal gate altered')
 require(load('support/CHECKS.json')['pass'] is True,'authored diagnostic record not passed')
 return allow

def check_archive(path,allow):
 require(path.is_file(),'archive missing')
 with zipfile.ZipFile(path) as z:
  infos=z.infolist();require([i.filename for i in infos]==allow,'archive exact member set/order failed')
  for info in infos:
   safe(info.filename)
   require(info.date_time==FIXED_TIME and info.create_system==3 and info.external_attr==(0o100644<<16),'archive timestamp/mode failed')
   require(info.compress_type==zipfile.ZIP_DEFLATED,'unexpected compression')
   require(not (info.flag_bits&1),'encrypted member rejected')
   require(z.read(info)==(ROOT/info.filename).read_bytes(),'archive bytes mismatch '+info.filename)

def check_binding(path,archive,required):
 if not path.exists():
  require(not required,'required deposit binding absent')
  return 'absent (permitted for clean extraction)'
 binding=json.loads(path.read_text(encoding='utf-8'))
 require(set(binding)=={'schema_version','paper_pdf','support_archive'},'binding fields differ')
 require(binding['schema_version']==1,'binding schema unsupported')
 for key,file in [('paper_pdf',ROOT/'paper.pdf'),('support_archive',archive)]:
  require(file is not None and file.is_file(),'present binding requires both deliverables')
  r=binding[key];require(r['path']==('paper.pdf' if key=='paper_pdf' else 'support.zip'),'binding names differ')
  data=file.read_bytes();require(r['bytes']==len(data) and r['sha256']==sha(data),'deposit binding mismatch '+key)
 return 'present and valid'

def main():
 p=argparse.ArgumentParser();p.add_argument('--archive');p.add_argument('--deposit-binding');p.add_argument('--require-deposit-binding',action='store_true');args=p.parse_args()
 allow=check()
 archive=Path(args.archive).resolve() if args.archive else (ROOT/'support.zip' if (ROOT/'support.zip').exists() else None)
 if archive is not None:check_archive(archive,allow)
 binding=Path(args.deposit_binding).resolve() if args.deposit_binding else ROOT/'publication/DEPOSIT_BINDING.json'
 result=check_binding(binding,archive,args.require_deposit_binding)
 print(json.dumps({'pass':True,'members':len(allow),'archive_checked':archive is not None,'deposit_binding':result},indent=2))
if __name__=='__main__':main()
