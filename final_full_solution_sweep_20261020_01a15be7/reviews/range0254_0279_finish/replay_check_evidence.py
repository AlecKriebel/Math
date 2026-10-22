#!/usr/bin/env python3
"""Offline identity/coverage checker. Never performs Git/provider/ledger mutations."""
from pathlib import Path
import json,hashlib,subprocess,os,re,zipfile,io,datetime,collections,unicodedata
Q=Path(__file__).resolve().parent.parent/"range0254_0279_adversary"
OUT=Path(__file__).resolve().parent
P=Q.parents[1]
WORK=P.parent
checks=[]
def check(name,value,detail=None):
 checks.append({'name':name,'pass':bool(value),**({'detail':detail} if detail is not None else {})})
def read(path):return json.loads(path.read_text())
def sha(b):return hashlib.sha256(b).hexdigest()
def git(*args):
 r=subprocess.run(['git',*args],cwd=WORK,capture_output=True,env=dict(os.environ,GIT_OPTIONAL_LOCKS='0'),timeout=25)
 r.check_returncode();return r.stdout
normdoi=lambda x:re.sub(r'^https?://(?:dx[.])?doi[.]org/','',str(x).strip()).lower().rstrip('/')
def parse(line):
 c=[v.strip() for v in re.split(r'(?<!\\)\|',line.strip('|'))]
 return c[1].split(' / ')[0],c[7]
bindings=read(Q/'bindings.json')['bindings']
live={a['number']:a for a in read(Q/'live_prs.json')['prs']}
canon=read(Q/'canonical_queue_fresh.json')
check('scope',sorted(live)==list(range(254,280))==[b['pr'] for b in bindings])
counts=collections.Counter(b['own_row']['status'] for b in bindings)
check('status counts',counts=={'already_solved':16,'unsolved':6,'claimed_solved':4})
for b in bindings:
 n=b['pr'];tag=str(n);e=read(P/b['eligibility_path']);l=live[n];row=b['own_row'];status=row['status'];d=b['disposition']
 check(tag+' eligibility receipt',sha((P/b['eligibility_path']).read_bytes())==b['eligibility_sha256'])
 check(tag+' recorded checks',all(b['checks'].values()),b['checks'])
 check(tag+' live head/base',l['head_sha']==e['inventory_head_sha'] and l['base_sha']==e['inventory_base_sha'])
 check(tag+' live body',sha(l['body'].encode())==d['inventory_body_sha256']==b['live_body_sha256'])
 paths=git('diff','--no-ext-diff','--no-renames','--name-only','-z',b['comparison']).decode().strip('\0').split('\0')
 check(tag+' exact paths',set(paths)==set(e['changed_paths']) and len(paths)==e['file_count'])
 for qb in b['queue_bindings']:
  pin=git('rev-parse',b['queue_end']+':'+qb['path']).decode().strip()
  diff=git('diff','--no-ext-diff','--no-renames','--unified=0',b['comparison'],'--',qb['path'])
  added=[x[1:] for x in diff.decode().splitlines() if x.startswith('+|')]
  check(tag+' queue blob',pin==qb['actual_blob']==qb['cached_blob'])
  check(tag+' queue diff',sha(diff)==qb['diff_sha256'] and added==qb['actual_rows'])
  check(tag+' own row',sum(x==row['source_line'] for x in added)==1 and parse(row['source_line'])==(row['problem_id'],status) and row['problem_id'] in e['path_problem_ids'])
 if e.get('pinned_comparison'):
  parents=git('rev-list','--parents','-n','1',b['queue_end']).decode().split()
  check(tag+' true merge binding',b['queue_end']==l['merge_commit_sha'] and l['head_sha'] in parents[1:])
 if status!='claimed_solved':
  check(tag+' explicit exclusion',d['disposition']=='skip_explicit_non_claimed_solved' and d['current_classification']==status and d['explicit_pr_queue_statuses']==[status])
 else:
  check(tag+' published coverage disposition',d['disposition'] in ['skip_entirely_already_published','reconcile_existing_publication_record'] and bool(d['doi']))
# No need to resolve the remote checkpoint commit locally: use its immutable QUEUE blob.
cq=git('cat-file','blob',canon['blob_sha'])
check('canonical QUEUE hash',sha(cq)==canon['sha256'] and len(cq)==canon['bytes'])
check('canonical scoped rows',all(b['canonical_row'] in cq.decode().splitlines() for b in bindings))
ledger_receipt=read(Q/'ledger_fresh.json');ledger=ledger_receipt['data']['values']
check('full open-ended GWS CLI range',ledger_receipt['returncode']==0 and ledger_receipt['command'][-1]=="'Math Puzzles'!A:AQ")
check('ledger schema',ledger[0]==['Original Problem','Solution Chat URL','DOI','Notes'])
pubs=read(Q/'publications_fresh.json')['publications']
check('four published PRs',[a['pr'] for a in pubs]==[254,256,263,278])
payload_count=payload_bytes=zip_members=manifest_entries=0
package_results=[]
for a in pubs:
 n=a['pr'];tag=str(n);d=next(b['disposition'] for b in bindings if b['pr']==n);prrow=next(b['own_row'] for b in bindings if b['pr']==n)
 v=a['record'];m=v['metadata']
 check(tag+' publication recorded checks',all(a['checks'].values()),a['checks'])
 check(tag+' public published state',v['state']=='done' and v['submitted'] is True and v['doi']==d['doi'])
 check(tag+' DOI resolves',a['doi_resolution']['status']==200 and a['doi_resolution']['final_url'].rstrip('/').endswith('/'+str(v['id'])))
 matches=[i+1 for i,r in enumerate(ledger) if len(r)>2 and normdoi(r[2])==normdoi(v['doi'])]
 check(tag+' primary DOI unique row',matches==[d['ledger_row']])
 row=ledger[d['ledger_row']-1];joined=' '.join(row)
 check(tag+' catalogue/alias/PR reference',prrow['problem_id'] in joined and prrow['problem_alias'].split(' / ')[1] in joined and '/pull/'+str(n)+'.' in joined+'.')
 api={x['key']:x for x in v['files']}
 check(tag+' expected file set',set(api)=={f['name'] for f in a['payloads']})
 for f in a['payloads']:
  data=(P/f['path']).read_bytes();payload_count+=1;payload_bytes+=len(data)
  check(tag+' file '+f['name'],sha(data)==f['sha256']==f['expected_sha256'] and 'md5:'+hashlib.md5(data).hexdigest()==api[f['name']]['checksum'] and len(data)==api[f['name']]['size']==f['size'])
  if zipfile.is_zipfile(io.BytesIO(data)):
   with zipfile.ZipFile(io.BytesIO(data)) as z:
    names=z.namelist();zip_members+=len(names)
    check(tag+' ZIP integrity',z.testzip() is None and names==f['members'])
    check(tag+' package source/code/instructions',any(x.endswith('.tex') for x in names) and any(x.endswith('.py') for x in names) and any(x.lower().endswith('readme.md') for x in names))
    manifests=[x for x in names if x.split('/')[-1].lower() in ['manifest.json','hashes.json']]
    manifest=sorted(manifests,key=lambda x:x.count('/'))[0];root=manifest.rsplit('/',1)[0]+'/' if '/' in manifest else ''
    entries=json.loads(z.read(manifest))['files']
    for ent in entries:
     raw=z.read(root+ent['path']);manifest_entries+=1
     check(tag+' manifest '+ent['path'],sha(raw)==ent['sha256'] and len(raw)==ent['bytes'])
    covered={root+e['path'] for e in entries}|{manifest}
    check(tag+' full manifest membership',covered==set(names))
    meta_names=[x for x in names if x in [root+'metadata.json',root+'publication_metadata.json',root+'record_metadata.json']]
    dep=json.loads(z.read(meta_names[0]));dep=dep.get('metadata',dep)
    for key in ['title','description','creators','publication_date','version','keywords']:
     if key=='keywords' and n==278:
      expected_extra=['SOS certificates','Scheiderer quartic','rational sums of squares','quadratic modules','Archimedean quadratic modules','Putinar Positivstellensatz','real algebraic geometry','polynomial optimization','Galois obstruction','representing measures','moment matrices','Gram spectrahedra']
      check(tag+' original keyword prefix retained; explicit live enrichment',m[key]==dep[key]+expected_extra)
     else:
      check(tag+' deposited/public metadata '+key,dep[key]==m[key])
    check(tag+' preprint/license metadata',dep['publication_type']==m['resource_type']['subtype']=='preprint' and dep['upload_type']==m['resource_type']['type']=='publication' and dep['license']==m['license']['id'])
    package_results.append({'pr':n,'manifest':manifest,'members':len(names),'declared_entries':len(entries),'source':f['source_members'],'code_count':len(f['code_members'])})
  else:
   text=subprocess.check_output(['pdftotext','-f','1','-l','1',str(P/f['path']),'-'],text=True)
   plain=' '.join(unicodedata.normalize('NFKC',text).split())
   check(tag+' PDF title/author/ORCID',m['title'] in plain and 'Alec Kriebel' in plain and '0009-0001-9320-500X' in plain)
for n in [254,256]:
 r=read(P/f'PR{n:04}_LEDGER_REPAIR.json');raw=P/'raw'/f'pr{n:04}'
 before=read(raw/'ledger_repair_before.json')['values'];after=read(raw/'ledger_repair_after.json')['values'];rr=r['row']
 changed=[]
 for i in range(max(len(before),len(after))):
  a=before[i] if i<len(before) else [];b=after[i] if i<len(after) else []
  for j in range(max(len(a),len(b))):
   if (a[j] if j<len(a) else '')!=(b[j] if j<len(b) else ''):changed.append([i+1,j+1])
 check(str(n)+' one repaired Notes cell',changed==[[rr,4]] and len(before)==len(after)==173)
 check(str(n)+' notes prefix preserved',after[rr-1][3].startswith(before[rr-1][3]) and before[rr-1][3]==r['old_notes'] and after[rr-1][3]==r['new_notes'])
 check(str(n)+' final live row equals repair',ledger[rr-1]==after[rr-1]==r['final_row'])
 req=read(raw/'ledger_repair_request.json')['requests'][0]['findReplace']
 expected={'sheetId':1254632077,'startRowIndex':rr-1,'endRowIndex':rr,'startColumnIndex':3,'endColumnIndex':4}
 check(str(n)+' exact cell CAS',req['range']==expected and req['find']==r['old_notes'] and req['replacement']==r['new_notes'] and req['matchEntireCell'] and req['matchCase'] and not req['searchByRegex'])
 reply=read(raw/'ledger_repair_response.json')['replies'][0]['findReplace']
 check(str(n)+' exactly one reported write',all(reply[k]==1 for k in ['occurrencesChanged','rowsChanged','sheetsChanged','valuesChanged']) and r['new_row'] is False and r['new_publication'] is False)
for docs in read(Q/'source_identity.json').values():
 for doc in docs:
  if doc['kind']=='repository_source_scope':
   raw=git('cat-file','blob',doc['blob_sha'])
   check('source scope '+doc['path'],sha(raw)==doc['sha256'] and len(raw)==doc['bytes'] and git('rev-parse',doc['commit']+':'+doc['path']).decode().strip()==doc['blob_sha'])
  else:
   with zipfile.ZipFile(io.BytesIO((P/doc['payload_path']).read_bytes())) as z:raw=z.read(doc['member'])
   check('deposited theorem source '+doc['member'],sha(raw)==doc['sha256'] and len(raw)==doc['bytes'])
for doc in read(Q/'withdrawal_bindings.json'):
 raw=git('cat-file','blob',doc['blob_sha'])
 check('withdrawal '+str(doc['pr'])+' '+doc['path'],sha(raw)==doc['sha256'] and len(raw)==doc['bytes'] and git('rev-parse',doc['commit']+':'+doc['path']).decode().strip()==doc['blob_sha'])
for doc in read(Q/'primary_source_identity.json')['sources']:
 check('original primary PDF '+doc['key'],sha((WORK/doc['path']).read_bytes())==doc['sha256']==doc['expected_sha256'])
warnings=[{'pr':n,'issue':'Rebuilt pinned-first-parent eligibility retains unannotated old live-REST page/time/preliminary fields; operative paths/QUEUE bindings independently pass.','recommended_repair':'Annotate retained intake provenance and add reconstruction timestamp, as with prior PR248; no scientific/disposition change.'} for n in [254,256,263]]
out={'at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'scope':[254,279],'passed':all(x['pass'] for x in checks),'checks':len(checks),'failures':[x for x in checks if not x['pass']],'counts':dict(counts),'payloads':payload_count,'payload_bytes':payload_bytes,'archive_members':zip_members,'manifest_entries':manifest_entries,'packages':package_results,'nonblocking_provenance_annotations':warnings,'metadata_differences':[{'pr':278,'field':'keywords','deposited_count':6,'public_count':18,'interpretation':'Live record enriches the six unchanged original terms with twelve relevant terms; no scientific identity/DOI/file mismatch and no new upload indicated.'}],'scope_limit':'Identity, eligibility and existing-publication coverage only; no new correctness/priority certification.','inputs':[{'path':f.name,'sha256':sha(f.read_bytes())} for f in sorted(Q.glob('*.json')) if f.name not in ['CHECK_RECEIPT.json']]}
(OUT/'REPLAY_CHECK_RECEIPT.json').write_text(json.dumps(out,separators=(',',':')))
print(json.dumps(out,indent=2))
raise SystemExit(0 if out['passed'] else 1)
