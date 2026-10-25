#!/usr/bin/env python3
"""Read-only exact custody and Git-tree checks; --write-receipt writes this bundle's audit receipt."""
from pathlib import Path
from html.parser import HTMLParser
import argparse, datetime, hashlib, json, os, subprocess
E=Path(__file__).resolve().parent
P=E.parents[1]
R=P.parent
S=Path('/Users/alec/Desktop/alec-dev/aleckriebel.com')

def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  while b:=f.read(1048576):h.update(b)
 return h.hexdigest()

def same(p,b):return p.is_file() and p.stat().st_size==b['bytes'] and sha(p)==b['sha256']

def git(*a):
 env=os.environ.copy();env['GIT_OPTIONAL_LOCKS']='0'
 return subprocess.check_output(['git',*a],cwd=R,env=env)

def main():
 parser=argparse.ArgumentParser();parser.add_argument('--write-receipt',action='store_true');args=parser.parse_args();issues=[]
 before=json.loads((E/'preservation-before.json').read_text());after=json.loads((E/'preservation-after.json').read_text());root_changes={r['path']:r for r in after['root_authorized_changed_existing_files']}
 for b in before['files']:
  expected=root_changes.get(b['path'],b)
  if not same(Path(b['path']),expected):issues.append({'kind':'original_binding','path':b['path']})
 for b in after['root_authorized_added_files']:
  if not same(Path(b['path']),b):issues.append({'kind':'root_added_binding','path':b['path']})
 expected_public={r['path'] for r in before['files'] if r['path'].startswith(str(S/'public')+'/')}|{r['path'] for r in after['root_authorized_added_files']}
 actual_public={str(p) for p in (S/'public').rglob('*') if p.is_file()}
 if actual_public!=expected_public:issues.append({'kind':'public_path_set','added':sorted(actual_public-expected_public),'missing':sorted(expected_public-actual_public)})
 if sha(Path(after['root_authorization_receipt']))!=after['root_authorization_receipt_sha256']:issues.append({'kind':'root_concurrent_authority_changed'})
 c=json.loads((E/'commit-receipt.json').read_text());changed=git('diff-tree','--no-commit-id','--name-only','-r',c['parent'],c['commit']).decode().splitlines()
 if sorted(changed)!=sorted(c['changed_paths']):issues.append({'kind':'commit_scope','actual':changed})
 for path in changed:
  if git('show',c['commit']+':'+path)!=(E/'proposed'/path).read_bytes():issues.append({'kind':'committed_proposal_mismatch','path':path})
 def tree_map(raw):return {r.split(b'\t',1)[1]:r.split(b'\t',1)[0] for r in raw.split(b'\0') if r}
 old=tree_map((E/'before/docs-tree.raw').read_bytes());new=tree_map(git('ls-tree','-r','-z',c['commit'],'--','docs'))
 untouched=[p for p in old if p.decode() not in changed]
 if set(old)!=set(new) or any(old[p]!=new[p] for p in untouched):issues.append({'kind':'other_docs_tree_changed'})
 local=json.loads((E/'git-local-before.json').read_text())
 if sha(Path(local['shared_index']['path']))!=local['shared_index']['sha256']:issues.append({'kind':'shared_index_changed'})
 if git('rev-parse','HEAD').decode().strip()!=local['commands'][2]['stdout'].strip():issues.append({'kind':'shared_HEAD_changed'})
 for b in json.loads((E/'screenshot-manifest.json').read_text())['screenshots']:
  if not same(E/b['file'],b):issues.append({'kind':'raw_screenshot','path':b['file']})
 for d in (E/'live').iterdir():
  receipt=json.loads((d/'receipt.json').read_text())
  for b in receipt['responses']:
   suffix='.pdf' if b['key']=='historical_pdf' else '.xml' if b['key']=='legacy_sitemap' else '.html';p=d/(b['key']+suffix)
   if not same(p,b):issues.append({'kind':'raw_HTTP_body','path':str(p)})
 result={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'STATIC_CUSTODY_AND_EXACT_COMMIT_CHECKS_PASS' if not issues else 'FAIL','all_pass':not issues,'original_bindings':len(before['files']),'unchanged_original_bindings':len(before['files'])-len(root_changes),'root_authorized_existing_deltas':len(root_changes),'root_authorized_added_files':len(after['root_authorized_added_files']),'current_site_files':len(actual_public),'committed_changed_paths':changed,'other_docs_blobs_preserved':len(untouched),'raw_screenshots':2,'live_redirect_PASS_claimed':False,'remaining_gap':'GitHub Pages build and ordinary live redirect/browser verification','issues':issues}
 if args.write_receipt:(E/'audit-receipt.json').write_text(json.dumps(result,indent=2)+'\n')
 print(json.dumps(result,indent=2));return bool(issues)
if __name__=='__main__':raise SystemExit(main())
