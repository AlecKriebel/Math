"""Fresh finite private-editorial custody; one root disposition output."""
from pathlib import Path
import hashlib,json,stat
from datetime import datetime,timezone
P=Path('/Users/alec/Documents/Math/research_website_catalogue_20261024/verification')
sha=lambda b:hashlib.sha256(b).hexdigest()
packets=[
 ('binary-gram-locus-editorial-sol-20261117','d422a994ca62dd9c9ee35ba1067841065afd42e99b6763c4c93674be2a3e942c','FINAL_SEAL.json','542fb861f6f2dee95737007d5c5ccd0c597a591081eea04ec3599cfb465f6b73',21,1),
 ('binary-gram-locus-editorial-fact-sol-20261117','d5d1e97687ae02c9508779bea3daaabfde3fc4967e2e0fe5d92cfaf02ac8b4fa','FINAL_SEAL.json','2c807ef87eef2aee6a2d8c9fee0ab1c763d6520f899c5139d3e149eab33a5604',13,0),
 ('binary-gram-locus-legacy-sol-20261117','3dfdcb870464db84e0430da01309eb8294729e01bf33c50b4a00f3227c530eb0','FINAL.json','146b7e007248bdfb98e3b169457d98cefe0f36cfc39a0092504f89d545a709b9',135,1),
]
accepted=[]
for name,mh,terminal,th,nf,nd in packets:
 b=P/name;mn='FINAL_MANIFEST.json'
 assert sha((b/mn).read_bytes())==mh
 assert sha((b/terminal).read_bytes())==th
 m=json.loads((b/mn).read_bytes())
 if 'entries' in m:rows=m['entries']
 else:
  rows=[dict(v,path=k,kind='file') for k,v in m['payload_files'].items()]
  rows += [{'path':k,'kind':'directory','mode':v} for k,v in m['directories'].items()]
  rows += [dict(r,kind='file') for r in m['terminal_pair']]
  rows += [{'path':'.','kind':'directory','mode':m['root_mode']}]
 declared={r['path']:r for r in rows};actual={'.':b}
 actual.update({f.relative_to(b).as_posix():f for f in b.rglob('*')})
 assert set(declared)==set(actual)
 assert sum(x.is_file() for x in actual.values())==nf
 assert sum(x.is_dir() for x in actual.values())==nd+1
 for rel,f in actual.items():
  r=declared[rel];assert not f.is_symlink()
  assert f.is_dir()==(r['kind']=='directory')
  assert stat.S_IMODE(f.stat().st_mode)==int(r['mode'],8)
  if f.is_file():
   raw=f.read_bytes();assert len(raw)==r['bytes']
   h=r.get('SHA256')
   if rel in {mn,terminal}:assert h in {None,'EXCLUDED_TERMINAL_RECURSIVE_HASH'}
   else:assert sha(raw)==h
  if 'empty' in r:assert (not any(f.iterdir()) if f.is_dir() else f.stat().st_size==0)==r['empty']
 accepted.append({'path':name,'files':nf,'child_directories':nd,'manifest_SHA256':mh,'terminal_SHA256':th})
result={'UTC':datetime.now(timezone.utc).isoformat(),'status':'ACCEPTED_PRIVATE_EDITORIAL_ONLY',
 'record':'23318851','packets':accepted,'authenticated_files':169,'child_directories':2,
 'root_personally_read':['whole actual HTML HEAD/BODY/MAIN','MODEL.json','citation.bib','EDITORIAL_REPORT.md','fact FINAL.json and FACT_REPORT.md','legacy FINAL.json and complete REPORT.md'],
 'fact_result':'PASS_NO_CORRECTION','legacy_result':'No genuine same-work article in three bounded docs collections; no redirect recommended',
 'follow_up':None,'canonical':None,'AA':None,'publication_certificate':False,'future_action_authority':False,
 'activation_caution':'Remove only the exact Private editorial draft entry-meta paragraph during later explicit activation, with a closed body edit in addition to HEAD metadata. Preserve native PDF/ZIP filenames and all substantive article bytes.',
 'retained_first_reader_failure':'root-gram-editorial-adoption-reader-first-failure-20261117.json',
 'private_copy_percent':100,'goal_active_incomplete':True}
out=P/'root-binary-gram-locus-editorial-adoption-20261117.json'
with out.open('x') as f:json.dump(result,f,indent=2);f.write('\n')
print(json.dumps(result))
