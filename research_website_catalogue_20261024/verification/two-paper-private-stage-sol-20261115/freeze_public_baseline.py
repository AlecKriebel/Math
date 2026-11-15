"""One exact post-five baseline freeze, after explicit root release."""
from two_common import *
from datetime import datetime,timezone
import re,xml.etree.ElementTree as ET
AUTH=[('root-five-stage-adoption-20261115.json','9311a588af93b9297dad692828a055fc68cdd98dd9fd7038389fe828aa478d0b'),('root-five-install-20261115/LOCAL_INSTALL.json','3cf4894f8d31cfaf5a7543276789ecb7199d7c58e5fd70e4581d1976751580b1')]
def freeze():
 need(not (OWN/'BASELINE_SEAL.json').exists(),'one_released_baseline_freeze_only');auth=[]
 for rel,wanted in AUTH:
  p=PROGRAMME/'verification'/rel;need(bind(p)['sha256']==wanted,'exact_root_post_five_authority');auth.append({'path':str(p),**bind(p),'whole_original_authority':load(p)})
 old=load(PROGRAMME/'verification/five-paper-private-stage-sol-20261115/FRESH_BASELINE.json');files=[p for p in PUBLIC.rglob('*') if p.is_file()];need(len(files)==576 and not any(p.is_symlink() for p in PUBLIC.rglob('*')),'released576_current_public')
 index=(PUBLIC/'research/index.html').read_bytes();sitemap=(PUBLIC/'research/sitemap.xml').read_bytes();need(len(re.findall(rb'<li>.*?</li>',index,re.S))==83,'released83_index');need(len(ET.fromstring(sitemap).findall('{*}url/{*}loc'))==84,'released84_sitemap')
 for r in old['installed_core_files']:need(bind(r['path'])=={k:r[k] for k in ['bytes','sha256']},'root_promised18_current_core_unchanged')
 now=datetime.now(timezone.utc).isoformat();baseline={'UTC':now,'public_root':str(PUBLIC),'public_files':[{'path':str(p.relative_to(PUBLIC)),**bind(p)} for p in sorted(files)],'installed_core_files':[{'path':r['path'],**bind(r['path'])} for r in old['installed_core_files']],'public_files_count':576,'index_entries':83,'sitemap_locations':84,'root_release_received':True,'Git_or_private_mail_inspected':False,'unrelated_staging_modified':False}
 (OWN/'baseline/research').mkdir(parents=True);(OWN/'baseline/research/index.html').write_bytes(index);(OWN/'baseline/research/sitemap.xml').write_bytes(sitemap)
 (OWN/'FRESH_BASELINE.json').write_text(json.dumps(baseline,indent=2)+'\n');(OWN/'BASELINE_AUTHORITY.json').write_text(json.dumps({'UTC':now,'root_released_exact_post_five_baseline':True,'whole_original_authorities':auth,'source_policy_historical_pending_flags_unchanged':True,'AA':None,'canonical_assignment':None,'two_stage_install_authorized':False},indent=2)+'\n')
 seal={'UTC':now,'baseline_sha256':bind(OWN/'FRESH_BASELINE.json')['sha256'],'authority_sha256':bind(OWN/'BASELINE_AUTHORITY.json')['sha256'],'native_public_namespace':576,'eventual_two_overlay_paths':11,'eventual_union_namespace':585,'eventual_index':85,'eventual_sitemap':86,'production_install_authorized':False,'AA':None,'canonical_assignment':None};(OWN/'BASELINE_SEAL.json').write_text(json.dumps(seal,indent=2)+'\n');print(json.dumps(seal,indent=2))
if __name__=='__main__':freeze()
