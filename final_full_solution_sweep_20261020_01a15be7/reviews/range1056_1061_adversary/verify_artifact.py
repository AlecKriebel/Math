#!/usr/bin/env python3
"""Read-only offline custody check. No evidence import, execution, writes or network."""
import argparse,hashlib,json,os,re,stat,sys
from pathlib import Path,PurePosixPath
PUBLIC={'.gitignore','CHECK_RESULTS.json','RESEARCH_LOG.md','REVIEW.md','verify_artifact.py'}
HEXS=re.compile('[0-9a-f]{64}')
def require(ok,msg):
 if not ok:raise ValueError(msg)
def digest(b):return hashlib.sha256(b).hexdigest()
def strict(b):
 def unique(items):
  d={}
  for k,v in items:
   require(k not in d,'duplicate JSON key');d[k]=v
  return d
 def invalid(v):raise ValueError('nonfinite JSON')
 return json.loads(b.decode('utf-8'),object_pairs_hook=unique,parse_constant=invalid)
def read(p):
 require(stat.S_ISREG(p.lstat().st_mode),'not regular '+str(p));return p.read_bytes()
def safe(s):
 require(type(s) is str and s and '\\' not in s and '\x00' not in s,'bad path')
 p=PurePosixPath(s);require(not p.is_absolute() and all(x not in ('.','..','') for x in p.parts) and p.as_posix()==s,'unsafe path');return p
def listing(root,skip_private=False):
 require(stat.S_ISDIR(root.lstat().st_mode),'root not real directory');out=set()
 def walk(d):
  for p in d.iterdir():
   rel=p.relative_to(root).as_posix();m=p.lstat().st_mode;require(not stat.S_ISLNK(m),'symlink')
   if stat.S_ISDIR(m):
    if skip_private and rel=='private':continue
    walk(p)
   else:require(stat.S_ISREG(m),'nonregular file');out.add(rel)
 walk(root);return out

def entries(root,rows):
 require(type(rows) is list,'files array');seen=set();folded=set()
 for e in rows:
  require(type(e) is dict and set(e)=={'path','bytes','sha256'},'entry keys');name=e['path'];pp=safe(name);require(name not in seen and name.casefold() not in folded,'duplicate path');seen.add(name);folded.add(name.casefold());require(type(e['bytes']) is int and e['bytes']>=0,'byte count');require(type(e['sha256']) is str and HEXS.fullmatch(e['sha256']) is not None,'digest syntax');p=root
  for x in pp.parts:p=p/x;require(not stat.S_ISLNK(p.lstat().st_mode),'symlink in path')
  b=read(p);require(len(b)==e['bytes'] and digest(b)==e['sha256'],'payload mismatch '+name)
 return seen

def manifest(root,name,external=None):
 b=read(root/(name+'.json'));seal=read(root/(name+'.sha256')).decode('ascii');require(seal==digest(b)+'\n','seal mismatch')
 if external is not None:require(HEXS.fullmatch(external) is not None and external==digest(b),'external anchor mismatch')
 m=strict(b);return m,digest(b)

def results(j):
 require(type(j) is dict and j['schema_version']==1 and type(j['schema_version']) is int,'result schema');require(j['outcome']=='no_actionable_findings' and j['substantive_findings']==[],'verdict')
 s=j['scope'];require(s['first_pr']==1056 and s['last_pr']==1061 and s['pr_count']==6 and s['new_proof_priority_or_global_acceptance'] is False,'scope')
 expected={'cases':6,'missing_QUEUE_cases':6,'actual_nonnull_changed_blobs':47,'partial_unsolved':3,'credited_prior_applications':2,'existing_external_publications':1,'new_publications_by_reviewer':0,'provider_writes_by_reviewer':0,'sheet_writes_by_reviewer':0}
 require(type(j['counts']) is dict and set(j['counts'])==set(expected),'count keys')
 for k,v in expected.items():require(type(j['counts'][k]) is int and j['counts'][k]==v,'count '+k)
 require([x['pr'] for x in j['cases']]==list(range(1056,1062)) and sum(x['paths'] for x in j['cases'])==47,'case identities')
 for c in j['cases']:
  require(c['no_QUEUE_edit'] is True and c['journal_exactly_once'] is True,'case binding');require(re.fullmatch('[0-9a-f]{40}',c['head']) is not None and re.fullmatch('[0-9a-f]{40}',c['base']) is not None,'nonnull object');require(HEXS.fullmatch(c['body_sha256']) is not None,'body hash')
 p=j['publication'];require(p['pr']==1060 and p['doi']=='10.5281/zenodo.23006720' and p['ledger_row']==179 and p['archive_members']==20 and p['archive_regular_files']==15 and p['archive_directories']==5 and p['exact_unique_row_readback'] is True,'publication identity')
 require(j['immutable_remote_checkpoint']=='805833bbd7874a39459cd3cda60c2e9acfc6bc54','checkpoint')

def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--root',type=Path,default=Path(__file__).resolve().parent);p.add_argument('--with-private',action='store_true');p.add_argument('--expected-public-sha256');a=p.parse_args();root=a.root.absolute();m,md=manifest(root,'OUTPUT_MANIFEST',a.expected_public_sha256);require(type(m) is dict and set(m)=={'schema_version','scope','files','private_manifest_sha256'},'manifest keys');require(type(m['schema_version']) is int and m['schema_version']==1 and m['scope']=='PR1056–1061 bounded review custody only','manifest schema/scope');require(HEXS.fullmatch(m['private_manifest_sha256']) is not None,'private anchor');names=entries(root,m['files']);require(names==PUBLIC,'public payload allowlist');require(listing(root,True)==PUBLIC|{'OUTPUT_MANIFEST.json','OUTPUT_MANIFEST.sha256'},'closed public inventory');require(read(root/'.gitignore')==b'private/\n','ignore rule');results(strict(read(root/'CHECK_RESULTS.json')));private_n=None
 if a.with_private:
  pr=root/'private';pm,pd=manifest(pr,'PRIVATE_MANIFEST',m['private_manifest_sha256']);require(type(pm) is dict and set(pm)=={'schema_version','files'} and type(pm['schema_version']) is int and pm['schema_version']==1,'private manifest schema');pn=entries(pr,pm['files']);require(listing(pr)==pn|{'PRIVATE_MANIFEST.json','PRIVATE_MANIFEST.sha256'},'closed private inventory');private_n=len(pn)
 print(json.dumps({'status':'PASS','public_payloads':len(names),'private_payloads':private_n,'scope':'Offline byte custody only; no mathematical, priority, provider or global completion certification'},sort_keys=True))
if __name__=='__main__':
 try:main()
 except Exception as e:print(json.dumps({'status':'FAIL','error':str(e)},sort_keys=True),file=sys.stderr);sys.exit(1)
