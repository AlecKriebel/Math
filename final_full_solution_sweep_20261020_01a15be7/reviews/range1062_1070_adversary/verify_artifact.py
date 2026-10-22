#!/usr/bin/env python3
"""Read-only offline custody/scope verifier; pass an externally held manifest SHA256.
This verifies captured bytes and bounded identities, not mathematical truth or remote authenticity.
No evidence code is imported or run. No files are created or rewritten.
"""
import argparse,hashlib,json,pathlib,re,stat,sys,zipfile
PUBLIC={'.gitignore','CHECK_RESULTS.json','RESEARCH_LOG.md','REVIEW.md','verify_artifact.py'}
PRS=list(range(1062,1071));COUNTS=[6,8,9,9,9,8,11,9,11]
CHECKPOINT='f48de23c60fbbe7890019a35bfec64dccf9dd666'
CLASS=['existing_external_publication','credited_prior_application','existing_credited_corollary_publication','credited_prior_application','partial','partial','credited_prior_application','partial','partial']
def require(v,m):
 if not v:raise ValueError(m)
def sha(b):return hashlib.sha256(b).hexdigest()
def integer(v):return type(v) is int and v>=0
def hexsha(v,n=64):return type(v) is str and re.fullmatch('[0-9a-f]{'+str(n)+'}',v) is not None
def pairs(ps):
 d={}
 for k,v in ps:
  require(k not in d,'duplicate JSON key '+k);d[k]=v
 return d
def reject(v):raise ValueError('nonfinite JSON '+v)
def loads(b):return json.loads(b.decode('utf-8'),object_pairs_hook=pairs,parse_constant=reject)
def readj(p):return loads(p.read_bytes())
def safe(s):
 require(type(s) is str and s!='' and not any(ord(c)<32 for c in s),'path type/control')
 p=pathlib.PurePosixPath(s);require(not p.is_absolute() and '\\' not in s and str(p)==s and '..' not in p.parts and '.' not in p.parts,'unsafe path '+s)
 return s
def inventory(root):
 fs=set();ds=set()
 def walk(p):
  for x in p.iterdir():
   st=x.lstat();rel=x.relative_to(root).as_posix();safe(rel)
   require(not stat.S_ISLNK(st.st_mode),'symlink '+rel)
   if stat.S_ISDIR(st.st_mode):ds.add(rel);walk(x)
   else:require(stat.S_ISREG(st.st_mode),'nonregular '+rel);fs.add(rel)
 walk(root);return fs,ds
def entries(root,rows):
 require(type(rows) is list,'manifest entries list');names=[]
 for e in rows:
  require(type(e) is dict and set(e)=={'path','bytes','sha256'},'entry schema');p=safe(e['path']);require(integer(e['bytes']) and hexsha(e['sha256']),'entry types');names.append(p)
  q=root/p;require(q.is_file() and not q.is_symlink(),'missing/nonregular '+p);b=q.read_bytes();require(len(b)==e['bytes'] and sha(b)==e['sha256'],'payload pin '+p)
 require(names==sorted(names) and len(names)==len(set(names))==len({x.casefold() for x in names}),'entry order/duplicate/case alias')
 return set(names)
def check_zip(path,expected):
 with zipfile.ZipFile(path) as z:
  require(z.testzip() is None,'ZIP CRC');items=z.infolist();ns=[i.filename for i in items];require(len(ns)==len(set(ns))==len({x.casefold() for x in ns}),'ZIP aliases')
  for i in items:
   safe(i.filename.rstrip('/'));require(not i.flag_bits&1 and not stat.S_ISLNK(i.external_attr>>16),'unsafe ZIP member')
  require(len(items)==expected,'ZIP member count');return {i.filename:z.read(i) for i in items if not i.is_dir()}
def verify(root,expected):
 require(hexsha(expected),'external SHA format');require(not root.is_symlink(),'root symlink');root=root.resolve()
 fs,ds=inventory(root);require({p for p in fs if '/' not in p}==PUBLIC|{'OUTPUT_MANIFEST.json'},'public inventory');require({p for p in ds if '/' not in p}=={'private'},'public directories');require(all(p.startswith('private/') or '/' not in p for p in fs),'nested public file')
 raw=(root/'OUTPUT_MANIFEST.json').read_bytes();require(sha(raw)==expected,'external public manifest SHA');m=loads(raw);require(set(m)=={'schema','files','private_manifest'},'public manifest schema');require(m['schema']=='closed-range-review/v1','public manifest version');require(entries(root,m['files'])==PUBLIC,'public allowlist')
 pm=m['private_manifest'];require(set(pm)=={'path','bytes','sha256'} and pm['path']=='private/PRIVATE_MANIFEST.json' and integer(pm['bytes']) and hexsha(pm['sha256']),'private link schema');b=(root/pm['path']).read_bytes();require(len(b)==pm['bytes'] and sha(b)==pm['sha256'],'private manifest link');q=loads(b);require(set(q)=={'schema','files','directories'} and q['schema']=='closed-private/v1','private manifest schema');d=root/'private';pfs,pds=inventory(d);listed=entries(d,q['files']);require(pfs==listed|{'PRIVATE_MANIFEST.json'},'private inventory closure');dirs=q['directories'];require(type(dirs) is list and all(type(x) is str for x in dirs) and dirs==sorted(set(dirs)) and len(dirs)==len({x.casefold() for x in dirs}),'private directory schema');require(all(safe(x)==x for x in dirs) and set(dirs)==pds,'private directory closure')
 c=readj(root/'CHECK_RESULTS.json');require(c['schema']=='range1062_1070_adversary/v1' and c['range']=={'first':1062,'last':1070,'count':9} and c['immutable_checkpoint']==CHECKPOINT,'bounded result identity')
 expected_counts={'actual_nonnull_paths':80,'missing_QUEUE_status':9,'partial':4,'credited_prior_application':3,'existing_publication':2,'new_publications':0,'provider_writes':0,'sheet_writes':0,'PR_writes':0,'git_mutations':0,'unresolved_actionable_findings':0};require(c['counts']==expected_counts and all(type(v) is int for v in c['counts'].values()),'bounded counts')
 s=readj(d/'structural_checks.json');require(s['immutable_remote_checkpoint']==CHECKPOINT and s['actual_paths']==80 and s['root_files']==47,'structural scope');require(s['remote_dispositions_equal'] is True and s['remote_journal_prefix'] is True,'remote receipt flags');require([x['pr'] for x in s['cases']]==PRS and [x['paths'] for x in s['cases']]==COUNTS,'case sequence/counts')
 require(c['cases']==[{**x,'classification':k} for x,k in zip(s['cases'],CLASS)],'case disposition binding')
 pins=readj(d/'capture_pins.json')['files'];require(len(pins)==47,'capture count')
 for e in pins:
  b=(d/'capture'/safe(e['path'])).read_bytes();require(integer(e['bytes']) and len(b)==e['bytes'] and sha(b)==e['sha256'],'capture pin')
 require(len({e['path'] for e in pins})==47,'capture duplicate')
 journal=[loads(b) for b in (d/'capture/dispositions.jsonl').read_bytes().splitlines()];remote=(d/'remote/dispositions.jsonl').read_bytes();require((d/'capture/dispositions.jsonl').read_bytes().startswith(remote),'remote journal prefix');require(readj(d/'remote/STATE.json')['next_pr']==1071,'remote cursor');require(readj(d/'remote_commit.json')['sha']==CHECKPOINT,'remote commit identity')
 for row in s['cases']:
  n=row['pr'];require(type(n) is int and row['no_QUEUE_edit'] is True and row['journal_exactly_once'] is True,'case types/flags');require(hexsha(row['head'],40) and hexsha(row['base'],40) and hexsha(row['body_sha256']),'case hashes');disp=readj(d/'capture'/('PR%d_DISPOSITION.json'%n));require([x for x in journal if x['pr']==n]==[disp],'unique exact journal');require((d/'remote'/('PR%d_DISPOSITION.json'%n)).read_bytes()==(d/'capture'/('PR%d_DISPOSITION.json'%n)).read_bytes(),'remote disposition')
  blobs=readj(d/'original'/str(n)/'BLOBS.json');elig=readj(d/'capture/eligibility'/('pr%04d.json'%n));paths=[x['path'] for x in blobs];require(len(blobs)==row['paths'] and len(paths)==len(set(paths)) and set(paths)==set(elig['changed_paths']),'actual paths');require(not any(pathlib.PurePosixPath(p).name=='QUEUE.md' for p in paths),'unexpected QUEUE');cached={x['filename']:x for x in elig['files']};require(set(cached)==set(paths),'cached complete paths')
  for x in blobs:
   b=(d/'original'/str(n)/safe(x['path'])).read_bytes();require(integer(x['bytes']) and len(b)==x['bytes'] and sha(b)==x['sha256'] and hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==x['oid'] and cached[x['path']]['sha']==x['oid'],'original Git/payload pin')
  for folder in ['live','final_live']:
   live=readj(d/folder/('pr%d.json'%n));require(live['number']==n and live['head']['sha']==row['head'] and live['base']['sha']==row['base'] and sha((live['body'] or '').encode())==row['body_sha256'],'fresh live identity')
 p=readj(d/'publication_checks.json');require(c['publications']==p['publications'] and p['sheet_rows']==180 and p['broad_leads']==33,'publication receipt identity');require([x['pr'] for x in p['publications']]==[1062,1064],'publication scope')
 rows=readj(d/'final_sheet.json')['values'];oldrows=readj(d/'sheet.json')['values'];require(rows[0]==['Original Problem','Solution Chat URL','DOI','Notes'],'sheet schema')
 for pub,rec,rownum,num in zip(p['publications'],[23071924,23430776],[180,142],[77,212]):
  n=pub['pr'];folder=d/('pub%d'%n);record=readj(folder/'record.json');require(pub['record']==rec and pub['ledger_row']==rownum and pub['doi']=='10.5281/zenodo.'+str(rec) and record['doi']==pub['doi'] and record['submitted'] is True and record['state']=='done','published record');require(pub['doi_resolution']['status']==200 and pub['doi_resolution']['final_url']=='https://zenodo.org/records/'+str(rec),'DOI receipt')
  rawfiles={x['key']:x for x in record['files']};require(set(rawfiles)=={x['name'] for x in pub['files']},'all provider files');require(len(rawfiles)==(3 if n==1062 else 2),'provider file count');captured=readj(d/'capture'/('PR%d_PUBLICATION_VERIFICATION.json'%n));require({x['name']:x['sha256'] for x in captured['files']}=={x['name']:x['sha256'] for x in pub['files']},'parent provider hashes')
  for x in pub['files']:
   b=(folder/safe(x['name'])).read_bytes();api=rawfiles[x['name']];require(len(b)==x['bytes']==api['size'] and sha(b)==x['sha256'] and 'md5:'+hashlib.md5(b).hexdigest()==x['md5']==api['checksum'],'downloaded file checksums')
  for term,want in pub['ledger_identity_checks'].items():require([i for i,v in enumerate(rows,1) if re.search(term,' '.join(map(str,v)),re.I)]==want==[rownum],'unique ledger identity')
  require(rows[rownum-1]==oldrows[rownum-1],'final row unchanged');zp=next(folder/x['name'] for x in pub['files'] if x['name'].endswith('.zip'));members=check_zip(zp,num)
  if n==1062:
   require(len(members)==70 and members['verification_report.md']==(folder/'OWR-782-001-verification-report.md').read_bytes(),'1062 archive report/count');require(rows[179]==readj(d/'capture/audits/pr1062_30000160/LEDGER_PUBLICATION_VERIFICATION.json')['values'],'repaired root readback')
  else:
   es=loads(members['SUPPORT_MANIFEST.json'])['entries'];require(len(es)==211 and set(members)=={e['path'] for e in es}|{'SUPPORT_MANIFEST.json'},'1064 ZIP closed');require(len({e['path'] for e in es})==211,'ZIP manifest duplicate')
   for e in es:require(safe(e['path']) in members and integer(e['bytes']) and len(members[e['path']])==e['bytes'] and sha(members[e['path']])==e['sha256'],'1064 member pin')
   require(members['paper.pdf']==(folder/'paper.pdf').read_bytes(),'embedded PDF');originals=loads(members['support/history/SUBMITTED_PINS.json']);bs=readj(d/'original/1064/BLOBS.json');require(originals['head_oid']==s['cases'][2]['head'] and {x['repository_path'] for x in originals['files']}=={x['path'] for x in bs},'nine original identities')
   for x in originals['files']:require(members['support/history/'+x['snapshot_path']]==(d/'original/1064'/safe(x['repository_path'])).read_bytes(),'nine original bytes')
 rep=readj(d/'reproduction1064.json');require(rep['all212copied_inputs_unchanged'] is True and rep['complete_guard_JSON_equal_after_declared_runtime_projection'] is True and rep['complete_original_JSON_equal_after_declared_runtime_projection'] is True and rep['normal_only_original_assertions'] is True,'copied replay flags');require([x['returncode'] for x in rep['runs']]==[0,0,0,1] and [x['name'] for x in rep['runs']]==['verify_normal','verify_optimized','run_checks','require_external_absent'],'replay returncodes');require(len(rep['negative_faults'])==7 and (rep['matrix_cases'],rep['arbitrary_laws'],rep['positive_histories'],rep['scalar_pairs'])==(11,2,1573,201),'finite replay scope');require(all(x['exact_path_normalized_byte_count_equal'] is True for x in rep['traceback_path_normalizations']) and len(rep['traceback_path_normalizations'])==17,'exact receipt path normalization')
 return {'verified':True,'scope':'bounded captured custody and receipt identities only','prs':9,'actual_paths':80,'publications':2,'private_files':len(listed),'public_manifest_sha256':expected,'private_manifest_sha256':pm['sha256']}
def main():
 a=argparse.ArgumentParser(description=__doc__);a.add_argument('--root',type=pathlib.Path,default=pathlib.Path(__file__).parent);a.add_argument('--expect-manifest-sha256',required=True);v=a.parse_args()
 try:r=verify(v.root,v.expect_manifest_sha256)
 except Exception as e:print('REJECTED: '+str(e),file=sys.stderr);return 1
 print(json.dumps(r,sort_keys=True));return 0
if __name__=='__main__':sys.exit(main())
