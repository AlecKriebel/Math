#!/usr/bin/env python3
"""Read-only independent replay. No network, source checkers, bytecode writes or certificate generation.
Use --unsealed before sealing; otherwise verify SEALED_MANIFEST.json and SEAL.json first.
The externally reported SEAL.json digest is the trust anchor against a rewritten local seal.
"""
from pathlib import Path,PurePosixPath
import argparse,json,hashlib,zipfile,io,stat,re,subprocess,base64
W=Path(__file__).resolve().parent
REPO=W.parents[2]
PUBS=[742,764,765,778,781,786,788,789]
count=0
def need(ok,msg):
 global count
 count+=1
 if not ok:raise ValueError(msg)
def digest(b):return hashlib.sha256(b).hexdigest()
def readj(p):return json.loads((W/p).read_bytes())
def git(*a):
 c=subprocess.run(['git',*a],cwd=REPO,capture_output=True)
 need(c.returncode==0,'git replay failed '+str(a[:3]))
 return c.stdout
def parse_row(s,path):
 c=[x.strip() for x in s.strip().strip('|').split('|')]
 if len(c)<9 or not c[0].isdigit():return None
 m=re.match(r'(\d+)\b',c[1])
 if not m:return None
 return (path,s,m[1],c[7])
def exact_doi_rows(ledger,doi):
 return [i for i,row in enumerate(ledger,1) if len(row)>2 and re.fullmatch(r'(?:https?://(?:dx\.)?doi\.org/)?'+re.escape(doi)+r'/?',str(row[2]).strip(),re.I)]
def archive_check(data,originals,source,pdf):
 with zipfile.ZipFile(io.BytesIO(data)) as z:
  names=z.namelist();need(len(names)==len(set(names)),'duplicate ZIP member');need(z.testzip() is None,'bad CRC')
  for x in z.infolist():
   n=x.filename;p=PurePosixPath(n)
   need(bool(n) and not n.startswith('/') and '\\' not in n and '..' not in p.parts and '.' not in p.parts and str(p)==n and not x.is_dir() and not stat.S_ISLNK(x.external_attr>>16),'unsafe ZIP path')
  m=json.loads(z.read('MANIFEST.json'))['files'];paths=[x['path'] for x in m]
  need(len(paths)==len(set(paths)),'duplicate manifested path');need(set(names)==set(paths)|{'MANIFEST.json'},'manifest not exact inventory')
  for f in m:
   b=z.read(f['path']);need(type(f['bytes']) is int and f['bytes']>=0 and len(b)==f['bytes'] and digest(b)==f['sha256'],'manifest length/hash mismatch')
  for f in originals:
   b=z.read(f['archive_member']);need(len(b)==f['bytes'] and digest(b)==f['sha256'],'original candidate changed')
   # Git object-ID framing authenticates captured original bytes independently of archive manifest.
   need(hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==f['git_blob'],'original Git blob mismatch')
  need('paper.pdf' not in names,'standalone PDF unexpectedly in archive')
  if 'PREPRINT_BINDINGS.json' in names:
   binding=json.loads(z.read('PREPRINT_BINDINGS.json'))
   for name,b in [(source,z.read(source)),('paper.pdf',pdf)]:need(binding[name]['bytes']==len(b) and binding[name]['sha256']==digest(b),'preprint binding mismatch')
  need(source in names and any(x.endswith('.py') for x in names),'source/verification absent')
  return {'members':len(names),'payloads':len(m),'originals':len(originals),'zero_bytes':sum(x['bytes']==0 for x in m)}
def expect_bad(fn,label):
 try:fn()
 except (ValueError,KeyError,zipfile.BadZipFile):return label
 raise ValueError('negative control accepted: '+label)
def rebuild(data,mutate):
 with zipfile.ZipFile(io.BytesIO(data)) as z:d={n:z.read(n) for n in z.namelist()}
 mutate(d)
 out=io.BytesIO()
 with zipfile.ZipFile(out,'w',compression=zipfile.ZIP_DEFLATED) as z:
  for n,b in d.items():z.writestr(n,b)
 return out.getvalue()
def main():
 global W,REPO
 a=argparse.ArgumentParser();a.add_argument('--unsealed',action='store_true');a.add_argument('--skip-git',action='store_true');a.add_argument('--review-dir',type=Path,default=W);args=a.parse_args();W=args.review_dir.resolve();REPO=W.parents[2]
 if not args.unsealed:
  mb=(W/'SEALED_MANIFEST.json').read_bytes();seal=readj('SEAL.json');need(seal['manifest_bytes']==len(mb) and seal['manifest_sha256']==digest(mb),'seal manifest binding')
  files=json.loads(mb)['files'];actual={p.relative_to(W).as_posix() for p in W.rglob('*') if p.is_file() and p.name not in ['SEALED_MANIFEST.json','SEAL.json']}
  need(actual=={x['path'] for x in files},'sealed exact file inventory')
  for f in files:
   p=W/f['path'];need(not p.is_symlink() and p.is_file(),'nonregular sealed input');b=p.read_bytes();need(len(b)==f['bytes'] and digest(b)==f['sha256'],'sealed input changed '+f['path'])
 inv=readj('private/root_inputs/rest_inventory.json');items={x['number']:x for x in inv['pull_requests']};scopes=[];synth=[]
 for n in range(742,790):
  s=readj(f'per_pr/PR{n:04}_SCOPE.json');e=readj(f'private/root_inputs/eligibility/pr{n:04}.json');d=readj(f'private/root_inputs/PR{n:04}_DISPOSITION.json');x=readj(f'live/initial/pr{n:04}.json');y=readj(f'live/final/pr{n:04}.json');iv=items[n]
  need(s['pr']==n and not s['failures'],'bad scope result');need(s['head']==x['head']['sha']==y['head']['sha']==iv['headRefOid']==d['inventory_head_sha'],'head drift');need(s['base']==x['base']['sha']==y['base']['sha']==iv['baseRefOid']==d['inventory_base_sha'],'base drift')
  for key in ['state','merged','body','title','draft','closed_at','merged_at']:need(x[key]==y[key],'material live drift '+key)
  need(d['inventory_body_sha256']==digest((x['body'] or '').encode())==digest((iv['body'] or '').encode()),'body snapshot mismatch')
  normalized='MERGED' if x['merged'] else x['state'].upper();need(normalized==iv['state']==d['pr_state'],'state snapshot mismatch')
  if x['merge_commit_sha']!=y['merge_commit_sha']:
   need(x['state']=='open' and y['state']=='open' and not x['merged'] and not y['merged'],'actual merged commit drift');synth.append(n)
  if x['merged']:need(x['merge_commit_sha']==iv['mergeCommit']['oid']==y['merge_commit_sha'],'merge identity mismatch')
  need(set(s['paths'])==set(e['changed_paths']) and len(s['paths'])==len(set(s['paths']))==s['path_count']==e['file_count'],'cached scope incomplete')
  need({b['path']:b['git_blob'] for b in s['head_blob_bindings']}=={b['filename']:b['sha'] for b in e['files']},'cached head blob mismatch')
  ids=set()
  for path in s['paths']:
   m=re.search(r'/attempts/(\d+)(?:/|$)',path) or re.search(r'problems/[^/]*?(\d{7,})(?:/|$)',path)
   if m:ids.add(m[1])
  need(ids==set(s['own_path_ids'])==set(d['problem_ids']),'wrong own IDs')
  parsed=[]
  for q in s['queue_bindings']:
   patch=(W/f'private/scopes/pr{n:04}_{Path(q["path"]).name}.patch').read_bytes();need(digest(patch)==q['patch_sha256'],'patch binding')
   for line in patch.decode().splitlines():
    if line.startswith('+') and not line.startswith('+++'):
     r=parse_row(line[1:],q['path'])
     if r:parsed.append(r)
  expected={(r['queue_path'],r['source_line'],r['problem_id'],r['status']) for r in s['all_added_rows']};need(set(parsed)==expected,'row parser mismatch');own=[r for r in parsed if r[2] in ids];need(bool(own) and {r[3] for r in own}==set(s['own_statuses']),'missing usable own status')
  if not args.skip_git:
   cmp=s['base']+'...'+s['head'];paths=git('diff','--no-ext-diff','--no-renames','--name-only','-z',cmp).decode().strip('\0').split('\0');need(paths==s['paths'],'immutable complete paths changed')
   tree=git('ls-tree','-r','-z',s['head'],'--',*paths);actual={}
   for entry in tree.split(b'\0'):
    if not entry:continue
    meta,path=entry.split(b'\t',1);mode,typ,oid=meta.decode().split();need(typ=='blob','unexpected nonblob');actual[path.decode()]=oid
   need(actual=={b['path']:b['git_blob'] for b in s['head_blob_bindings']},'immutable head tree binding')
   for q in s['queue_bindings']:need(git('diff','--no-ext-diff','--no-renames','--unified=0',cmp,'--',q['path'])==(W/f'private/scopes/pr{n:04}_{Path(q["path"]).name}.patch').read_bytes(),'immutable patch differs')
  for b in s['head_blob_bindings']:
   data=(W/'private/git_objects'/b['git_blob']).read_bytes();need(len(data)==b['bytes'] and digest(data)==b['sha256'],'captured blob SHA256');need(hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()==b['git_blob'],'captured blob Git ID')
  for label,commit in [('head',s['head']),('base',s['base'])]:
   data=(W/f'private/git_bodies/pr{n:04}_{label}.commit').read_bytes();need(hashlib.sha1(b'commit '+str(len(data)).encode()+b'\0'+data).hexdigest()==commit,'commit body Git ID')
  scopes.append(s)
 negative=[s['pr'] for s in scopes if s['own_statuses']!=['claimed_solved']];need(len(negative)==39,'ordinary negative count');need([s['pr'] for s in scopes if s['own_statuses']==['claimed_solved']]==sorted(PUBS+[767]),'unexpected full-claim inference candidate')
 for phase in ['initial','final']:
  qb=(W/f'live/{phase}/main_QUEUE.md').read_bytes();qc=readj(f'live/{phase}/main_QUEUE_contents.json');need(base64.b64decode(qc['content'])==qb and hashlib.sha1(b'blob '+str(len(qb)).encode()+b'\0'+qb).hexdigest()==qc['sha'],'main QUEUE immutable content binding');q=qb.decode();row=[x for x in q.splitlines() if re.match(r'^\|\s*802\s*\|\s*30005902\b',x)];need(len(row)==1 and parse_row(row[0],'QUEUE.md')[3]=='already_solved','767 current withdrawal missing');need('Farinati' in row[0] and '2026-10-16T07:30:12' in row[0],'767 correction missing')
  comment=readj(f'live/{phase}/withdrawal_comment.json');need(comment['id']==6210328294 and 'Farinati' in comment['body'] and 'already_solved' in comment['body'],'767 comment mismatch')
 need(readj('live/initial/pr0767.json')['state']=='closed' and not readj('live/initial/pr0767.json')['merged'],'767 state')
 ledgers=[readj('private/ledger_initial.json')['values'],readj('private/ledger_final.json')['values']];pubres=[]
 for n in PUBS:
  p=W/f'private/public/pr{n:04}';pub=readj(f'per_pr/PR{n:04}_PUBLICATION.json');record=json.loads((p/'record.json').read_text());d=readj(f'private/root_inputs/PR{n:04}_DISPOSITION.json');ownid=readj(f'per_pr/PR{n:04}_SCOPE.json')['own_path_ids'][0]
  need(not pub['failures'] and record['state']=='done' and record['submitted'] is True and record['doi']==d['doi']==pub['doi'],'public record identity/state')
  need({f['key'] for f in record['files']}=={'paper.pdf','source-and-verification.zip'},'public file set')
  for f in record['files']:
   b=(p/f['key']).read_bytes();need(len(b)==f['size'] and f['checksum']=='md5:'+hashlib.md5(b).hexdigest(),'public file checksum');need(any(x['name']==f['key'] and x['sha256']==digest(b) and x['bytes']==len(b) for x in pub['public_files']),'public SHA256 binding')
  for ledger in ledgers:
   matches=exact_doi_rows(ledger,record['doi']);need(matches==[d['ledger_row']],'DOI row not unique');row=ledger[matches[0]-1];need(re.search(r'(?<!\d)'+ownid+r'(?!\d)',' '.join(row)) and re.search(r'pull/'+str(n)+r'(?!\d)',' '.join(row)),'wrong ledger identity');need(row==ledgers[0][matches[0]-1],'own ledger row drift')
  retrieval=readj(f'private/public/pr{n:04}/RETRIEVALS.json');need(any(x['requested_url']=='https://doi.org/'+record['doi'] and x['status']==200 and x['final_url']=='https://zenodo.org/records/'+str(record['id']) for x in retrieval),'DOI resolution')
  r=archive_check((p/'source-and-verification.zip').read_bytes(),pub['originals'],pub['source_file'],(p/'paper.pdf').read_bytes());need(r['members']==pub['archive_members'] and r['payloads']==pub['manifest_payloads'] and r['originals']==pub['originals_count'],'archive result mismatch');pubres.append(dict(pr=n,**r))
  native=readj(f'private/original_problems/pr{n:04}.json');catalog=next(x for x in readj('private/CATALOG_SELECTED.json') if str(x['id'])==ownid);need(digest(native['problem']['statement'].encode())==catalog['statement_hash'],'original statement binding');need(digest(json.dumps([native['problem'],native['report']],sort_keys=True).encode())==catalog['review_hash'],'native problem/report binding')
 need(sum(x['payloads'] for x in pubres)==1199 and sum(x['originals'] for x in pubres)==355,'publication coverage totals')
 # Adversarial parser and inventory controls run only against in-memory new copies.
 controls=[];pub=readj('per_pr/PR0742_PUBLICATION.json');p=W/'private/public/pr0742';zbytes=(p/'source-and-verification.zip').read_bytes();pdf=(p/'paper.pdf').read_bytes()
 def check(b):return archive_check(b,pub['originals'],pub['source_file'],pdf)
 def drop_manifest(d):
  m=json.loads(d['MANIFEST.json']);m['files']=m['files'][1:];d['MANIFEST.json']=json.dumps(m).encode()
 controls.append(expect_bad(lambda:check(rebuild(zbytes,drop_manifest)),'unmanifested payload rejected'))
 controls.append(expect_bad(lambda:check(rebuild(zbytes,lambda d:d.update({'../escape':b'x'}))),'unsafe path rejected'))
 def rehash_original(d):
  name=pub['originals'][0]['archive_member'];d[name]=d[name]+b'\nchanged';m=json.loads(d['MANIFEST.json'])
  for f in m['files']:
   if f['path']==name:f.update(bytes=len(d[name]),sha256=digest(d[name]))
  d['MANIFEST.json']=json.dumps(m).encode()
 controls.append(expect_bad(lambda:check(rebuild(zbytes,rehash_original)),'rehash cannot counterfeit Git-original binding'))
 row='| 1 | 123 / X | title | .1 | 5 | 3 | 2020 | unsolved | 5/5 | claimed_solved partial |'
 need(parse_row(row,'QUEUE.md')[3]=='unsolved','status parser distracted by note');controls.append('explicit status wins over misleading claimed note')
 dup=[['problem','','https://doi.org/10.5281/zenodo.1','']]*2;need(len(exact_doi_rows(dup,'10.5281/zenodo.1'))==2,'duplicate DOI control');controls.append('duplicate DOI detection')
 need(all(x['unchanged'] for x in readj('SOURCE_STABILITY.json')),'captured root source changed; investigate separately')
 semantic=readj('SEMANTIC_REVIEW.json');need(set(map(int,semantic['assessments']))==set(PUBS),'manual semantic review coverage')
 print(json.dumps({'status':'PASS_BOUNDED_COVERAGE','checks':count,'pr_count':48,'pinned_paths':sum(s['path_count'] for s in scopes),'ordinary_explicit_negatives':len(negative),'current_withdrawal':767,'published_cases':PUBS,'source_payload_entries':1199,'archived_originals':355,'open_ephemeral_test_merge_changes':synth,'archive_results':pubres,'negative_controls':controls,'sealed':not args.unsealed,'git_replayed':not args.skip_git,'mathematical_or_priority_certification':False},indent=2))
if __name__=='__main__':main()
