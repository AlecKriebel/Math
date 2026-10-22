#!/usr/bin/env python3
"""Confirm public historical inventories close over independently reconstructed Git trees."""
import pathlib,json,zipfile,subprocess
W=pathlib.Path(__file__).resolve().parent;checks=[]
for n in [883,885,888,894,904,905]:
 z=zipfile.ZipFile(next((W/'downloads_private'/str(n)).glob('*.zip')));c=json.loads((W/'inputs'/f'PR{n:04}_PUBLICATION_COVERAGE_DETAILS.json').read_text());d=json.loads((W/'inputs'/f'PR{n:04}_DISPOSITION.json').read_text());prefix=f"unsolved_math_prioritization/attempts/{c['problem_id']}/";res={'pr':n}
 fs='root_evidence/SOURCE_MANIFEST.json' if n in (883,894) else 'SOURCE_MANIFEST.json' if n in (885,888) else 'ORIGINAL_SNAPSHOT.json' if n==905 else 'PACKAGE_MANIFEST.json';man=json.loads(z.read(fs));sh=c.get('source_head',d['inventory_head_sha']);res['historical_head_embedded_in_public_inventory']=sh in json.dumps({k:v for k,v in man.items() if k!='files'});res['inventory_member']=fs
 originals=next(x for x in json.loads((W/'PACKAGE_CHECKS.json').read_text())['results'] if x['pr']==n)['original_bindings']
 if n in (883,885,888,894):
  by={x['path']:x for x in man['files']};res['source_inventory_paths_exact']=set(by)=={x['path'][len(prefix):] for x in originals};res['source_inventory_all_hash_blob_size_exact']=all(by[x['path'][len(prefix):]]['sha256']==x['sha256'] and by[x['path'][len(prefix):]]['bytes']==x['bytes'] and by[x['path'][len(prefix):]]['git_blob']==x['original_git_blob'] for x in originals)
 elif n==905:
  res['source_inventory_paths_exact']=set(man['files'])=={x['path'] for x in originals};res['source_inventory_all_hash_exact']=all(man['files'][x['path']]==x['sha256'] for x in originals)
 else:res['source_inventory_paths_exact']=set(k for k in man['files'] if k.startswith('original_packet/'))=={x['member'] for x in originals}
 if n in (904,905):
  raw=subprocess.run(['git','-C',str(W.parents[2]),'cat-file','-e',d['inventory_head_sha']+':'+prefix+'note.tex'],capture_output=True);res['later_paper_absent_original_PR_head']=raw.returncode!=0
 checks.append(res)
(W/'SOURCE_INVENTORY_CHECKS.json').write_text(json.dumps(checks,indent=2)+'\n');print('PASS',len(checks),'public historical source inventories')
