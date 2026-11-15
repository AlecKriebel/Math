#!/usr/bin/env python3
"""Baseline artifact closure; optional live file comparison. No network/Git/writes/science."""
from pathlib import Path
import hashlib,json,re,sys
import xml.etree.ElementTree as ET
A=Path(__file__).resolve().parent
checks=0
def need(c,m):
 global checks
 checks+=1
 if not c:raise ValueError(m)
def load(p):return json.loads(p.read_bytes())
def sha(b):return hashlib.sha256(b).hexdigest()
def check(e):
 p=Path(e['path']);b=p.read_bytes();need(not p.is_symlink(),'symlink '+str(p));need(len(b)==e['bytes'] and sha(b)==e.get('SHA256',e.get('sha256')),'bytes '+str(p));return b
def main():
 args=set(sys.argv[1:]);need(args<=set(['--preseal','--live-baseline']),'recognized options only');pre='--preseal' in args;live='--live-baseline' in args
 need(pre or (A/'BASELINE_SEAL.json').is_file(),'default requires baseline seal')
 if not pre:
  seal=load(A/'BASELINE_SEAL.json')
  need(seal['status']=='FRESH614_BASELINE_SEALED_BEFORE_WRITER_EXPOSURE','literal baseline seal')
  for e in seal['bindings'].values():check(e)
 for e in load(A/'BASELINE_MANIFEST.json')['files']:check(e)
 # All initial artifacts remain exact, including the restored initial log.
 for e in load(A/'INITIAL_MANIFEST.json')['files']:check(e)
 base=load(A/'FRESH_WEBSITE_BASELINE.json');need(base['HEAD']=='46773fd3d0e7289f5ab79bfc9f8ddf382fa508fc' and base['branch']=='master','actual observed website identity')
 need(base['writer_stage_code_copy_or_opinion_reads']==0,'baseline predates writer exposure')
 rows=base['public_files'];by={e['public_relative_path']:e for e in rows};need(len(rows)==len(by)==614,'entire614 baseline paths')
 for e in rows:
  b=check(e['snapshot']);need(len(b)==e['bytes'] and sha(b)==e['SHA256'],'whole baseline public body')
 for e in base['configs']:need(sha(check(e['snapshot']))==e['SHA256'],'whole site config')
 index=check(by['research/index.html']['snapshot']).decode()
 graphs=[json.loads(x) for x in re.findall(r'<script[^>]*type=["\']application/ld\+json["\'][^>]*>(.*?)</script>',index,re.S)]
 need(graphs==base['whole_index_JSONLD_original_typed_objects'],'complete original index schema')
 item=graphs[0]['mainEntity'];need(type(item['numberOfItems']) is int and item['numberOfItems']==92 and len(item['itemListElement'])==92,'typed92')
 need([x['position'] for x in item['itemListElement']]==list(range(1,93)),'ordered typed positions')
 cards=re.findall(r'<li>(.*?)</li>',index,re.S);need(len(cards)==92,'visible92')
 urls=[re.search(r'<a href="([^"]+)"',x).group(1) for x in cards]
 need(['https://aleckriebel.com'+x for x in urls]==[x['url'] for x in item['itemListElement']],'whole visible/typed URL order')
 sitemap=ET.fromstring(check(by['research/sitemap.xml']['snapshot']));locs=[e.text for e in sitemap.findall('{*}url/{*}loc')]
 need(locs==base['whole_sitemap_locations'] and len(locs)==len(set(locs))==93,'whole93 sitemap')
 paths=load(A/'ACTUAL_EXPECTED_OUTPUT_PATHS.json')['paths'];need(len(paths)==len({e['website_relative_path'] for e in paths})==11,'actual11 contract')
 need([e['website_relative_path'] for e in paths if e['kind'].startswith('aggregate_')]==['research/index.html','research/sitemap.xml'],'actual two aggregates')
 need(sum(e['website_relative_path'] not in by for e in paths)==9,'nine absent leaves')
 git=load(A/'FRESH_GIT_OBSERVATIONS.json');raw=check(git['raw_index_records']);records=raw.rstrip(b'\0').split(b'\0')
 need(len(records)==git['all_index_record_count']==58554,'fresh raw index record count')
 excluded={('public/'+e['website_relative_path']).encode() for e in paths}
 protected=[r for r in records if r.split(b'\t',1)[1] not in excluded];bound=check(git['fresh_protected_raw_records'])
 need(bound==b'\0'.join(protected)+b'\0' and len(protected)==git['fresh_protected_index_record_count']==58552,'fresh exact protected record set')
 need(git['excluded_future11_gitpaths']==sorted(x.decode() for x in excluded),'scope corrected to actual aggregate')
 check(git['raw_index_flags'])
 for e in git['actual_read_only_command_receipts']:need(e['exit_code']==0 and e['GIT_OPTIONAL_LOCKS']=='0','read-only actual Git observation');check(e['stdout']);check(e['stderr'])
 core=load(A/'CORE17_AND_AUTHORIZED_CHECKPOINT.json');need(core['original17_files_unchanged']==17 and core['claim_all18_match_original_baseline'] is False,'qualified core claim')
 original={e['path']:e for e in core['prior_whole_qualification']['original_core_file_bindings']}
 changed=[]
 for e in core['current_actual_file_snapshots']:
  b=check(e['snapshot']);need(sha(b)==e['source']['SHA256'],'core actual snapshot')
  if sha(b)!=original[e['source']['path']]['SHA256']:changed.append(e)
 need(len(changed)==1 and changed[0]['source']['path'].endswith('/checkpoint_subtree.py') and changed[0]['source']['SHA256']=='405b0357fd20a2e14893ce6c3c1a0f81910894ccd8ffaddac4e25014138fb9c0','sole authorized checkpoint difference')
 for e in base['prior_publication_receipts']:check(e)
 if live:
  root=Path(base['website_root'])/'public';actual={q.relative_to(root).as_posix() for q in root.rglob('*') if q.is_file()}
  need(actual==set(by) and not any(q.is_symlink() for q in root.rglob('*')),'live complete namespace614')
  for e in rows:
   b=Path(e['source_path']).read_bytes();need(len(b)==e['bytes'] and sha(b)==e['SHA256'],'live unchanged public')
  for e in base['configs']:
   b=Path(e['source_path']).read_bytes();need(len(b)==e['bytes'] and sha(b)==e['SHA256'],'live unchanged config')
 print(json.dumps({'status':'PASS_INDEPENDENT_FRESH614_BASELINE','checks':checks,'counts':[614,92,93],'fresh_protected_index_records':58552,'initial_files_exact':True,'writer_stage_exposed_at_capture':False,'live_file_comparison':live,'network':0,'subprocesses':0,'writes':0,'science_execution':0},indent=2))
if __name__=='__main__':main()
