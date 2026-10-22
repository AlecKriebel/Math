#!/usr/bin/env python3
"""Verify curated public receipt; optional private source integrity. No network/writes."""
import argparse, hashlib, json, pathlib
HERE=pathlib.Path(__file__).resolve().parent
EXPECTED={
 'AUDIT.md','INITIAL_RECONSTRUCTION.md','PRIOR_IMPLICATION.md','QUERY_LOG.md',
 'SOURCE_INSPECTION.md','RESEARCH_LOG.md','RESULT.json','SOURCE_PINS.json',
 'ORIGINAL_AUTH_START.json','ORIGINAL_AUTH_END.json','authenticate_originals.py',
 'fetch_primary.py','render_primary.py','verify_review.py','VERIFY.md',
 'PUBLIC_ALLOWLIST_MAP.json',
}
def require(condition,message):
 if not condition:raise ValueError(message)
def sha(b):return hashlib.sha256(b).hexdigest()
def run(private=False):
 raw=(HERE/'MANIFEST.json').read_bytes();manifest=json.loads(raw)
 pin=(HERE/'MANIFEST.sha256').read_text().split()
 require(pin==[sha(raw),'MANIFEST.json'],'external manifest pin mismatch')
 rows=manifest['files'];names=[r['path'] for r in rows]
 require(len(names)==len(set(names))==len(EXPECTED),'duplicate or wrong public file count')
 require(set(names)==EXPECTED,'curated set differs from fixed expected files')
 for row in rows:
  name=row['path'];path=pathlib.PurePosixPath(name)
  require(not path.is_absolute() and len(path.parts)==1 and '..' not in path.parts,'unsafe path')
  body=(HERE/name).read_bytes()
  require(len(body)==row['bytes'] and sha(body)==row['sha256'],'public file mismatch: '+name)
 amap=json.loads((HERE/'PUBLIC_ALLOWLIST_MAP.json').read_text())
 require(set(amap['allowlist'])==EXPECTED,'map differs from curated set')
 for name in ['ORIGINAL_AUTH_START.json','ORIGINAL_AUTH_END.json']:
  auth=json.loads((HERE/name).read_text())
  require(auth['original_count']==29 and auth['all_originals_match'],'original auth failure')
  require(all(r['git_sha256']==r['disk_sha256'] and r['matches'] for r in auth['files']),'original per-file mismatch')
 result=json.loads((HERE/'RESULT.json').read_text())
 require(result['author_proof_search_turns_added']==0,'proof accounting changed')
 require(result['prior_disposition']['exact_target_subsumed'] and result['prior_disposition']['full_candidate_strengthening_subsumed'],'priority disposition mismatch')
 sources=json.loads((HERE/'SOURCE_PINS.json').read_text())['sources']
 require(len(sources)==28 and sum(r['ok'] for r in sources)==26,'source count mismatch')
 bykey={r['key']:r for r in sources}
 require(bykey['winter_stoker_author']['sha256']==bykey['winter_stoker_git_766c313']['sha256'],'historical note differs')
 if private:
  for row in sources:
   if row['ok']:
    body=(HERE/row['private_path']).read_bytes()
    require(sha(body)==row['sha256'] and len(body)==row['bytes'],'private source mismatch: '+row['key'])
 return {'ok':True,'public_allowlist_count':len(rows),'source_records':len(sources),
         'successful_source_pins':26,'original_files_authenticated_start_and_end':29,
         'private_sources_checked':private,'manifest_sha256':sha(raw)}
if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--private',action='store_true')
 args=parser.parse_args();print(json.dumps(run(args.private),indent=2))
