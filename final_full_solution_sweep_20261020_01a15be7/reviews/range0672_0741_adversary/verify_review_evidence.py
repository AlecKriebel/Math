#!/usr/bin/env python3
"""Offline, read-only replay of bounded scope/status/custody checks.

Only checker execution occurs in a NEW temporary private directory. No network,
Git updates, provider writes, canonical certificate execution, or assertions.
"""
from pathlib import Path, PurePosixPath
import collections, copy, hashlib, json, os, re, shutil, stat, subprocess, sys, tempfile, zipfile
sys.dont_write_bytecode=True
os.environ.update(PYTHONDONTWRITEBYTECODE='1',GIT_OPTIONAL_LOCKS='0')
Q=Path(__file__).resolve().parent;R=Q.parent.parent;REPO=R.parent
def require(ok,msg):
 if not ok:raise RuntimeError(msg)
def sha(b):return hashlib.sha256(b).hexdigest()
def read(rel):return json.loads((Q/rel).read_text())
def run(args,**kw):return subprocess.run(args,cwd=REPO,capture_output=True,check=True,**kw).stdout
def validate_row(actual,expected):
 require(actual==expected,'Own QUEUE row differs')
 require(actual['status'] in {'unsolved','already_solved','claimed_solved'},'No usable own status: full-claim inference required')
def parse_row(line,path):
 c=[s.strip() for s in re.split(r'(?<!\\)\|',line.strip().strip('|'))]
 if len(c)>=9 and c[0].isdigit():return dict(queue_path=path,problem_id=c[1].split('/')[0].strip(),status=c[7],source_line=line)
def rowkey(row):return {k:row[k] for k in ['queue_path','problem_id','status','source_line']}
def validate_live(record,expected):require(all(record[k]==expected.get(k) for k in record),'Live metadata differs')
def validate_paths(paths,eligibility,scope):
 require(len(paths)==len(set(paths))==eligibility['file_count']==scope['path_count'],'Scope count')
 require(paths==scope['complete_paths'] and set(paths)==set(eligibility['changed_paths'])=={x['filename'] for x in eligibility['files']},'Scope completeness')
def validate_satoh(scope):require(scope['degree5_rank_min']==4 and scope['degree6_rank_min']==3 and scope['component_algebra']=='rational_SL2_matrix_entry_functions' and scope['A_uses_integral_free_group_LCS'] is True and scope['D_acts_on_whole_J_quotient'] is True and scope['ordinary_IA_LCS_conjecture_claim'] is False and scope['character_algebra_claim'] is False,'Wrong Satoh scope')
def validate_718_names(names):require('paper.pdf' not in names and 'paper.tex' in names,'Source archive/standalone PDF identity')
inputs=read('INPUT_MANIFEST.json')['files'];require(len({v['path'] for v in inputs})==len(inputs),'Duplicate captured input')
for v in inputs:
 b=(Q/v['path']).read_bytes();require(len(b)==v['bytes'] and sha(b)==v['sha256'],'Input digest '+v['path'])
inventory=read('private/inputs/rest_inventory.json');prs={p['number']:p for p in inventory['pull_requests']}
state=read('private/inputs/STATE.json');journal=[json.loads(s) for s in (Q/'private/inputs/dispositions.jsonl').read_text().splitlines() if s];ds={d['pr']:d for d in journal}
require([d['pr'] for d in journal]==list(range(9,state['next_pr'])) and state['next_pr']>=742,'Captured contiguous completed range')
scopes=read('pinned_scope_checks.json');assessments=read('per_pr_assessments.json');values=read('pinned_blob_values.json')
require([v['pr'] for v in scopes]==[v['pr'] for v in assessments]==list(range(672,742)),'Exact range accounting')
require(len(values)==2106,'Changed-path entry count')
all_rows={};path_total=0
for scope in scopes:
 n=scope['pr'];p=prs[n];e=read(f'private/inputs/eligibility/pr{n:04d}.json');d=read(f'private/inputs/PR{n:04d}_DISPOSITION.json')
 require(d==ds[n] and e['inventory_head_sha']==p['headRefOid'] and e['inventory_base_sha']==p['baseRefOid'],'Pinned commit/journal mismatch')
 comp=(p['mergeCommit']['oid']+'^1..'+p['mergeCommit']['oid']) if n==681 else p['baseRefOid']+'...'+p['headRefOid']
 require(scope['comparison']==comp,'Wrong comparison')
 raw=run(['git','diff','--no-ext-diff','--no-renames','--name-only','-z',comp]);paths=raw.decode().rstrip('\0').split('\0') if raw else []
 validate_paths(paths,e,scope)
 rows=[];qp=set(paths)&{'QUEUE.md','unsolved_math_prioritization/QUEUE.md'}
 for path in qp:
  patch=run(['git','diff','--no-ext-diff','--no-renames','--unified=0',comp,'--',path]);require(patch==(Q/f'private/git_inputs/pr{n:04d}/QUEUE.patch').read_bytes(),'Captured queue patch')
  for line in patch.decode().splitlines():
   if line.startswith('+') and not line.startswith('+++'):
    row=parse_row(line[1:],path)
    if row:rows.append(row)
 require(len(rows)==len(e['added_queue_rows'])==1,'One own changed row required');row=rows[0];validate_row(row,rowkey(e['added_queue_rows'][0]));pid=row['problem_id'];all_rows[n]=row
 require(d['problem_ids']==[pid],'Own identifier differs');require(all(path in qp or path.startswith('unsolved_math_prioritization/attempts/'+pid+'/') or n==681 and path.startswith('unsolved_math_prioritization/publications/'+pid+'/') or n==729 and path.startswith('problems/20002559_rbm43_prior_obstruction/') for path in paths),'Non-own path')
 if n==672:require(row['status']=='claimed_solved' and d['disposition']=='skip_priority_gate_not_met','Hold classification')
 elif n in [681,718]:require(row['status']=='claimed_solved' and d['disposition']=='skip_entirely_already_published','Published classification')
 elif n==734:require(row['status']=='claimed_solved' and d['current_classification']=='already_solved' and d['disposition']=='skip_explicit_non_claimed_solved','Withdrawal precedence')
 else:require(row['status'] in {'unsolved','already_solved'} and d['current_classification']==row['status'] and d['disposition']=='skip_explicit_non_claimed_solved','Explicit-negative exclusion')
 require(assessments[n-672]['problem_id']==pid and assessments[n-672]['explicit_status']==row['status'] and assessments[n-672]['missing_status_inference_required'] is False,'Assessment correspondence')
 path_total+=len(paths)
require(path_total==2106,'Path sum')
expressions=[v['head']+':'+v['path'] for v in values]
out=run(['git','cat-file','--batch-check=%(objectname) %(objecttype)'],input=('\n'.join(expressions)+'\n').encode()).decode().splitlines();require(len(out)==len(values),'Git batch length')
def validate_cached(entry):
 if entry['cached_blob'] is None:require(entry['cached_blob_equal'] is None,'Unknown cached blob cannot equal known object')
 else:require(entry['git_blob']==entry['cached_blob'] and entry['cached_blob_equal'] is True,'Cached known blob differs')
for v,line in zip(values,out):
 require(line==v['git_blob']+' blob','Immutable path/body object differs');validate_cached(v)
 if v['pr']==681:require(v['actual_merge_blob']==v['git_blob'],'Actual merge object differs')
nulls=[v for v in values if v['pr']==681 and v['cached_blob'] is None];require(len(nulls)==45,'Special fallback nulls')
merge=prs[681]['mergeCommit']['oid'];parents=run(['git','show','--no-patch','--format=%P',merge]).decode().split();require(len(parents)==2 and parents[1]==prs[681]['headRefOid'],'Actual merge parent')
merged_entries=[v for v in values if v['pr']==681];merged_out=run(['git','cat-file','--batch-check=%(objectname) %(objecttype)'],input=('\n'.join(merge+':'+v['path'] for v in merged_entries)+'\n').encode()).decode().splitlines();require(merged_out==[v['git_blob']+' blob' for v in merged_entries],'Independent actual-merge head blob equality')
old=run(['git','diff','--no-ext-diff','--no-renames','--name-only','-z',prs[681]['baseRefOid']+'...'+prs[681]['headRefOid']]);require(len(old.rstrip(b'\0').split(b'\0'))==62109,'Unrelated integrated-history context')
blobs=read('GIT_BLOB_INPUT_MANIFEST.json')['files'];require(len(blobs)==188,'Captured Git bodies')
for v in blobs:
 b=(Q/v['captured_path']).read_bytes();require(len(b)==v['bytes'] and sha(b)==v['sha256'],'Git captured digest');require(hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==v['git_blob'],'Git blob content hash')
for phase in ['initial_live_prs','final_live_prs']:
 live=read('private/'+phase+'.json');require('errors' not in live,'Live capture provider error')
 for n in range(672,742):
  p=live['data']['repository'][f'p{n}'];validate_live(p,prs[n])
initial=read('private/initial_live_prs.json');require(initial==read('private/final_live_prs.json'),'Start/end provider metadata differs')
for phase,receipt in [('initial','initial_live_metadata_receipt.json'),('final','final_live_recheck.json')]:
 wire=(Q/f'private/{phase}_live_wire.json').read_bytes();rr=read(receipt);require(sha(wire)==rr.get('raw_sha256',rr.get('wire_sha256')) and json.loads(wire)==read(f'private/{phase}_live_prs.json'),'Exact provider wire custody')
ledger=read('private/ledger_wire.json')['values'];require(len(ledger)==178 and max(map(len,ledger))==4,'Whole ledger shape')
def validate_ledger(rows):
 for n,pid,rownum,record in [(681,'30003703',102,23387442),(718,'30004324',71,23331395)]:
  exact=[i for i,row in enumerate(rows,1) if re.search(r'(?<!\d)'+pid+r'(?!\d)',' '.join(row)) or re.search(r'\bPR\s*#?'+str(n)+r'(?!\d)',' '.join(row)) or re.search(r'/pull/'+str(n)+r'(?!\d)',' '.join(row))]
  require(exact==[rownum],'Duplicate/missing target ledger row')
  doi='10.5281/zenodo.'+str(record);require([i for i,row in enumerate(rows,1) if len(row)>2 and doi in row[2]]==[rownum],'Duplicate/missing DOI')
 for pid in ['6700060','2515']:require(not any(re.search(r'(?<!\d)'+pid+r'(?!\d)',' '.join(row)) for row in rows),'Unexpected excluded target ledger identity')
validate_ledger(ledger)
public=read('publication_integrity_checks.json');require([v['pr'] for v in public]==[681,718],'Public case set')
for v in public:
 n=v['pr'];base=Q/f'private/public_{n}';record=read(f'private/public_{n}/record_wire.json');require(record['state']=='done' and record['submitted'] is True and record['doi']==v['doi'],'Public status')
 for f in v['files']:
  b=(base/f['name']).read_bytes();rf=next(x for x in record['files'] if x['key']==f['name']);require(len(b)==f['bytes']==rf['size'] and sha(b)==f['sha256'] and rf['checksum']=='md5:'+hashlib.md5(b).hexdigest(),'Public file bytes')
 z=zipfile.ZipFile(next(base.glob('*.zip')));names=z.namelist();require(len(names)==len(set(names))==v['archive_members'] and z.testzip() is None,'ZIP CRC/names')
 for item in z.infolist():
  pp=PurePosixPath(item.filename);require(not pp.is_absolute() and '..' not in pp.parts and '\\' not in item.filename and not stat.S_ISLNK(item.external_attr>>16),'ZIP unsafe member')
 mn='PACKAGE_MANIFEST.json' if n==681 else 'MANIFEST.json';m=json.loads(z.read(mn));entries=m['files'];entries=entries if isinstance(entries,list) else [dict(path=k,**val) for k,val in entries.items()]
 require(len(entries)==v['positive_payloads'] and set(names)=={mn}|{x['path'] for x in entries},'ZIP positive membership')
 for f in entries:
  b=z.read(f['path']);require(len(b)==f.get('bytes',f.get('size')) and sha(b)==f['sha256'],'Positive payload digest')
 originals=v['originals'];require(len(originals)=={681:23,718:49}[n],'Public originals count')
 for f in originals:require(z.read(f['archive_member'])==run(['git','show',prs[n]['headRefOid']+':'+f['path']]),'Original Git bytes')
 if n==681:
  scope=json.loads(z.read('CLAIM_SCOPE.json'));validate_satoh(scope)
  for f in originals:require(z.read(f['archive_member'])==run(['git','show',scope['original_head']+':'+f['path']]),'Earlier original head binding')
  require(z.read('satoh_filtration_counterexamples.pdf')==(base/'satoh_filtration_counterexamples.pdf').read_bytes(),'Embedded PDF')
  for name in ['CLAIM_SCOPE.json','CURRENT_PRIORITY_AND_STATUS.md','README.md','satoh_filtration_counterexamples.tex','satoh_filtration_counterexamples.pdf']:require(z.read(name)==run(['git','show',prs[n]['headRefOid']+':unsolved_math_prioritization/publications/30003703/'+name]),'Merged public governing file identity')
 else:
  validate_718_names(names)
  tex=z.read('paper.tex').decode();pdf=(base/'paper.txt').read_text();require('arbitrary characteristic' in tex and 'closed point' in tex and '\\epsilon(T_X;x)>0' in tex and 'projective space' in pdf and 'arbitrary characteristic' in pdf,'Wrong tangent scope')
withdrawal=read('withdrawal_current_binding.json');queue=(Q/'private/withdrawal_current_QUEUE.md').read_bytes();require(sha(queue)==withdrawal['queue_sha256'],'Current withdrawal bytes');target=[s for s in queue.decode().splitlines() if s.startswith('| 766 | 2515 / KOU-21.6 |')]
def validate_withdrawal(rows):require(len(rows)==1 and '| already_solved |' in rows[0] and 'PR#734 closed without merge' in rows[0] and '21538908' in rows[0],'Explicit current withdrawal required')
validate_withdrawal(target);snapshot=read('private/inputs/CURRENT_CANONICAL_QUEUE_SNAPSHOT.json');require(snapshot['main']=='f0f09658b2696e0d23d0fce88fe5964bcd25626c','Canonical snapshot commit');require(withdrawal['source_line']==target[0],'Withdrawal same row')
require(snapshot['rows']['2515']['source_line']==target[0] and snapshot['rows']['2515']['status']=='already_solved','Canonical exact target row');prior=read('private/inputs/canonical_queue_history/snapshot_20261021T1842.json');require(prior['main']=='d6ca2e4dbb7355aec650ca17d3cb32575d8c64cf' and prior['rows']['2515']['source_line']==target[0],'Preserved earlier canonical snapshot')
require(target==[s for s in (Q/'private/final_main_QUEUE.md').read_text().splitlines() if s.startswith('| 766 | 2515 / KOU-21.6 |')],'Final current withdrawal');require(read('private/final_withdrawal_comment_wire.json')['body']==read('private/withdrawal_comment_wire.json')['body'],'Final correction body')
comment=read('private/withdrawal_comment_wire.json');require(comment['issue_url'].endswith('/issues/734') and '21538908' in comment['body'],'Source-bound closing correction')
H='private/inputs/audits/pr0672_6700060/';A=H+'reviews/prior_application_recheck01/';seal=read(A+'SEAL.json');manifest=read(A+'SEALED_MANIFEST.json');accept=read(H+'ROOT_FINAL_RECHECK_ACCEPTANCE.json')
require(sha((Q/(A+'SEAL.json')).read_bytes())==accept['seal_sha256']=='e2266da1306431f045c8b6ee692d6d25f917b26641c11c0d0cbf69c6ea9a6b29','Hold seal identity');require(sha((Q/(A+'SEALED_MANIFEST.json')).read_bytes())==seal['manifest_sha256']==accept['manifest_sha256'],'Hold manifest seal');require(len(manifest['files'])==50,'Hold payload count')
for v in manifest['files']:
 b=(Q/A/v['path']).read_bytes();require(len(b)==v['bytes'] and sha(b)==v['sha256'],'Hold sealed payload')
orig=read(H+'private/ORIGINAL_INPUTS.json')['files'];require(len(orig)==24,'Hold originals count');lookup={x['path']:x for x in blobs if x['pr']==672}
for f in orig:require(sha((Q/lookup[f['path']]['captured_path']).read_bytes())==f['sha256'],'Hold original body')
with tempfile.TemporaryDirectory(prefix='verify672_',dir=Q/'private') as td:
 t=Path(td);shutil.copyfile(Q/(A+'exact_application_controls.py'),t/'controls.py')
 for flags in [[],['-O']]:
  result=subprocess.run([sys.executable,'-I','-B',*flags,str(t/'controls.py')],cwd=t,capture_output=True);require(result.returncode==0 and not result.stderr and sha(result.stdout)==accept['independent_private_replay']['byteidentical_output_sha256'],'Private controls replay')
hold=read('hold_custody_checks.json');require(hold['conditional_stated_Bi_theorem'] is True and hold['ambient_smooth_category'] is True and hold['broader_corner_singular_category_certified'] is False and hold['fresh_full_analytic_PDE_certification'] is False and hold['new_discovery_mechanism'] is False,'Hold scope inflation')
for f in read('fresh_primary_source_receipts.json'):
 b=(Q/'private/fresh_primary'/f['name']).read_bytes();require(sha(b)==f['sha256'],'Fresh primary custody')
 if f['name'] in ['gromov2017.pdf','bi2608.06320v1.pdf','gromov2013.pdf']:require(b==(Q/A/'private'/f['name']).read_bytes(),'Fresh versus sealed exact source')
# Targeted fault controls: same validators, deliberately hostile copies only.
negative=[]
def rejects(label,fn):
 try:fn()
 except RuntimeError:negative.append(label)
 else:raise RuntimeError('Fault accepted: '+label)
bad=copy.deepcopy(all_rows[673]);bad['problem_id']='unrelated';rejects('unrelated_negative_row',lambda:validate_row(bad,all_rows[673]))
bad=copy.deepcopy(all_rows[672]);bad['status']='unsolved';rejects('claim_replaced_by_negative',lambda:validate_row(bad,all_rows[672]))
bad=copy.deepcopy(nulls[0]);bad['cached_blob_equal']=True;rejects('null_cached_SHA_false_equality',lambda:validate_cached(bad))
bad=copy.deepcopy(ledger);bad.append(copy.deepcopy(ledger[101]));rejects('duplicate_publication_row',lambda:validate_ledger(bad))
rejects('withdrawal_without_explicit_current_status',lambda:validate_withdrawal([target[0].replace('| already_solved |','| claimed_solved |')]))
bad=copy.deepcopy(initial['data']['repository']['p672']);bad['headRefOid']='0'*40;rejects('stale_live_head',lambda:validate_live(bad,prs[672]))
rejects('truncated_fullscope',lambda:validate_paths(scopes[0]['complete_paths'][:-1],read('private/inputs/eligibility/pr0672.json'),scopes[0]))
bad=copy.deepcopy(all_rows[673]);bad['status']='queued';rejects('unusable_status_without_inference',lambda:validate_row(bad,bad))
bad=json.loads(zipfile.ZipFile(Q/'private/public_681/satoh_filtration_verification.zip').read('CLAIM_SCOPE.json'));bad['ordinary_IA_LCS_conjecture_claim']=True;rejects('wrong_ordinary_IA_scope',lambda:validate_satoh(bad))
bad=zipfile.ZipFile(Q/'private/public_718/source-and-verification.zip').namelist()+['paper.pdf'];rejects('false_PDF_inside_718_sourceZIP',lambda:validate_718_names(bad))
final=read('final_live_recheck.json');require(final['differences_from_initial']==[] and final['changed_canonical_dispositions']==[],'Final changed metadata or decisions')
print(json.dumps(dict(status='PASS',range_count=70,path_entries=2106,Git_bodies=188,explicit_negative_exclusions=67,ordinary_explicit_negatives=66,withdrawn=734,priority_holds=[672],publications=[681,718],public_positive_payloads=183,publication_originals=72,hold_sealed_payloads=50,hold_originals=24,hold_exact_controls_per_mode=358,fresh_primary_sources=5,negative_controls_rejected=negative),sort_keys=True))
