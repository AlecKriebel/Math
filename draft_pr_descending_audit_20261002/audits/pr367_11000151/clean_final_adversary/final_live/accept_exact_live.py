"""Additive read-only live acceptance gate. Requires explicit refreshed execution pins.
No candidate writes, Git object/ref writes, remote mutations, installs or outreach.
Run only after completed review02 clearance and root's literal pins are supplied.
"""
from pathlib import Path
from datetime import datetime,timezone
import argparse,base64,copy,gzip,hashlib,json,os,runpy,shutil,subprocess,sys,tempfile,traceback,zipfile

HERE=Path(__file__).resolve().parent
AUDIT=HERE.parent.parent
REPO=Path('/Users/alec/Documents/Math')
PREFIX='problems/11000151_artin_a5_quotient'
QUEUE='unsolved_math_prioritization/QUEUE.md'
PYTHON=REPO/'draft_pr_descending_audit_20261002/audits/pr378_30004322/sources_effective_review/private_runtime/bin/python'
CAPTURES=[];CHECKS=[]
def utc():return datetime.now(timezone.utc).isoformat()
def sha(data):return hashlib.sha256(data).hexdigest()
def load(path):return json.loads(path.read_bytes())
def bind(data):return {'bytes':len(data),'sha256':sha(data)}
def require(condition,label):
 CHECKS.append({'check':label,'pass':bool(condition)})
 if not condition:raise AssertionError(label)
def save(name,value):
 (HERE/'receipts'/name).write_text(json.dumps(value,indent=2,ensure_ascii=False)+'\n')
def save_compressed(name,value):
 (HERE/'receipts'/name).write_bytes(gzip.compress((json.dumps(value,indent=2,ensure_ascii=False)+'\n').encode(),mtime=0))
def checkpoint(percent,text):
 with (HERE/'RESEARCH_LOG.md').open('a') as log:log.write('- '+utc()+': '+text+' Completion'+str(percent)+'%.\n')
def run(label,args,cwd=REPO,private=False):
 start=utc();env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',TMPDIR=str(HERE/'private_runtime'))
 result=subprocess.run(list(map(str,args)),cwd=cwd,capture_output=True,env=env)
 folder=HERE/'private_runtime/api_git_sources' if private else HERE/'fullstreams'
 folder.mkdir(exist_ok=True)
 streams={}
 for name,data in [('stdout',result.stdout),('stderr',result.stderr)]:
  path=folder/(label+'.'+name+'.gz');compressed=gzip.compress(data,mtime=0);path.write_bytes(compressed)
  streams[name]={'path':str(path.relative_to(HERE)),**bind(data),'stored_bytes':len(compressed),'stored_sha256':sha(compressed),'compression':'gzip'}
 CAPTURES.append({'label':label,'command':list(map(str,args)),'cwd':str(cwd),'started_utc':start,'finished_utc':utc(),'exit_code':result.returncode,**streams})
 save('EXECUTIONS.json',CAPTURES)
 require(result.returncode==0,label+' successful execution')
 require(result.stderr==b'',label+' complete empty stderr')
 return result.stdout
def git(label,*args):return run('git_'+label,['git',*args],private=True)
def api(label,path):return json.loads(run('api_'+label,['gh','api','--method','GET','-H','Cache-Control: no-cache','repos/AlecKriebel/Math/'+path],private=True))
def binding(path,row,label):
 data=path.read_bytes();require(not path.is_symlink(),label+' regular file')
 require(len(data)==row['bytes'] and sha(data)==row['sha256'],label+' complete bytes')
 return {'path':str(path.relative_to(AUDIT)),**bind(data)}
def manifest(path,expected_sha=None):
 data=path.read_bytes()
 if expected_sha:require(sha(data)==expected_sha,str(path.relative_to(AUDIT))+' literal manifest pin')
 obj=json.loads(data);records=[];names=[]
 for row in obj['files']:
  name=row['path'];names.append(name);target=path.parent/name
  require(target.resolve().is_relative_to(path.parent.resolve()),name+' confined manifest path')
  records.append(binding(target,row,str(path.relative_to(AUDIT))+':'+name))
 require(len(names)==len(set(names)),str(path.relative_to(AUDIT))+' unique complete bindings')
 return {'path':str(path.relative_to(AUDIT)),**bind(data),'all_bindings':records}
def validate_pr(pr,pins,main,testmerge,head_tree):
 assert pr['head']['sha']==pins['head'],'head pin'
 assert pr['base']['sha']==pins['base']==main['object']['sha'],'base/current-main pin'
 body=pr['body'].encode('utf-8');assert body==pins['_body'],'exact body bytes'
 assert not pr['draft'] and not pr['merged'] and pr['state']=='open','non-draft open PR'
 assert pr['mergeable'] is True and pr['mergeable_state']=='clean','clean merge metadata'
 assert pr['base']['ref']=='main' and pr['base']['repo']['full_name']=='AlecKriebel/Math','main repository'
 assert pr['head']['repo']['full_name']=='AlecKriebel/Math','head repository'
 assert [p['sha'] for p in testmerge['parents']]==[pins['base'],pins['head']],'test-merge actual parents'
 assert testmerge['tree']['sha']==head_tree,'Git/API actual merge tree'
 assert pr['merge_commit_sha']==testmerge['sha'],'PR test-merge identity'
def validate_queue(before,after):
 old=before.splitlines(keepends=True);new=after.splitlines(keepends=True)
 assert len(old)==len(new),'queue physical line count'
 differences=[i for i,(a,b) in enumerate(zip(old,new),1) if a!=b]
 assert differences==[400],'only own physical queue line400'
 cells=old[399].split(b'|');assert b'11000151 / AMR-109-0151' in cells[2],'own row identity'
 assert cells[8]==b' queued ' and cells[9]==b' 0/5 ','original own status/turns'
 cells[8]=b' claimed_solved ';cells[9]=b' 4/5 ';expected=list(old);expected[399]=b'|'.join(cells)
 assert after==b''.join(expected),'exact only cells8/9 and all other bytes'
def reject(label,call):
 try:call()
 except BaseException:
  failure=traceback.format_exc();(HERE/'fullstreams'/('negative_'+label+'.txt')).write_text(failure)
  CHECKS.append({'check':'negative '+label+' rejected','pass':True,'complete_failure':'fullstreams/negative_'+label+'.txt'})
 else:raise AssertionError('negative control unexpectedly accepted: '+label)
def equal_run_local_utc(out,expected,start,finish,label):
 actual= json.loads(out);reference=json.loads(expected)
 require(actual.keys()==reference.keys(),label+' all output keys')
 stamp=actual['utc'];require(datetime.fromisoformat(start)<=datetime.fromisoformat(stamp)<=datetime.fromisoformat(finish),label+' run-local UTC')
 require(out.count(stamp.encode())==1,label+' unique UTC bytes')
 require(out.replace(stamp.encode(),reference['utc'].encode(),1)==expected,label+' entire output bytes after declared UTC substitution')

def main():
 parser=argparse.ArgumentParser();parser.add_argument('--pins',type=Path,required=True);args=parser.parse_args()
 for row in load(HERE/'CODE_READY_SEAL.json')['prepared_programs']:
  require(bind((HERE/row['path']).read_bytes())=={'bytes':row['bytes'],'sha256':row['sha256']},'fully read prepared program unchanged '+row['path'])
 (HERE/'receipts/EXECUTION_PINS.json').write_bytes(args.pins.read_bytes())
 pins=load(args.pins);required={'head','base','body_file','body_bytes','body_sha256','clearance_file','clearance_sha256','clearance_complete_object','review02_manifest_file','review02_manifest_sha256'}
 require(required<=pins.keys(),'all explicit execution pins supplied')
 require(pins['head']!='d977c9564f079cde975a7b4261776eb9061c5f5f','refreshed head distinct from old draft')
 for key in ('head','base'):require(len(pins[key])==40 and all(c in '0123456789abcdef' for c in pins[key]),key+' literal SHA')
 body=Path(pins['body_file']).read_bytes();require(bind(body)=={'bytes':pins['body_bytes'],'sha256':pins['body_sha256']},'exact approved body file')
 pins['_body']=body;(HERE/'receipts/EXACT_ACCEPTED_BODY.txt').write_bytes(body)
 private=HERE/'private_runtime';private.mkdir(exist_ok=True)
 baseline=load(HERE/'PREPARATION_BASELINE.json');prior=[]
 for row in baseline['immutable_prior_files']:prior.append(binding(AUDIT/row['path'],row,'prepared immutable '+row['path']))
 manifest_records=[manifest(AUDIT/name) for name in baseline['immutable_prior_manifests']]
 require(len(manifest_records[0]['all_bindings'])==127,'immutable original127 public files')
 require(run('start_original_closed_audit',[PYTHON,'-B',HERE.parent/'verify_audit.py'])==b'PASS: complete self-excluded public audit, earlier/final seals and44 raw execution-output streams\n','entire start original closed-audit verifier stdout')
 clearance=Path(pins['clearance_file']);require(sha(clearance.read_bytes())==pins['clearance_sha256'],'literal completed publishing clearance')
 clearance_object=load(clearance)
 require(pins.get('clearance_complete_object')==clearance_object,'entire final clearance object explicitly supplied and accepted by root')
 review02=Path(pins['review02_manifest_file']);manifest_records.append(manifest(review02,pins['review02_manifest_sha256']))
 review_status=load(review02.parent/'REVIEW_STATUS.json');review_seal=load(review02.parent/'FINAL_SEAL.json')
 require(review_status['verdict']==review_seal['verdict']=='PASS_EXACT_REPAIRED_BYTES_CLEARED_FOR_PUBLICATION','completed second review exact clearance verdict')
 require(review_status['assigned_review_completion_percent']==review_seal['assigned_review_completion_percent']==100 and review_status['mandatory_remaining_changes']==[],'completed second review has no mandatory remaining changes')
 require(review_seal['manifest_sha256']==pins['review02_manifest_sha256'],'completed second review final seal literal manifest')
 save('PRIOR_IMMUTABLE_BINDINGS.json',{'files':prior,'all_manifest_records':manifest_records,'clearance':bind(clearance.read_bytes()),'clearance_full_object':load(clearance)})
 # Exact root/family output receipts and all retained complete captures are bound, not just PASS labels.
 for name,count in [('root_original_reproduction_receipt.json',857),('root_family_reproduction_receipt.json',652)]:
  report=load(AUDIT/name);require(report['status']=='PASS' and report['check_count']==count and len(report['checks'])==count and all(r['pass'] is True for r in report['checks']),name+' every original check')
  commands=report.get('commands',report.get('all_complete_captures',[]))
  for command in commands:
   for channel in ('stdout','stderr'):
    row=command[channel];path=AUDIT/row['path'];stored=path.read_bytes();data=gzip.decompress(stored) if path.suffix=='.gz' else stored
    stored_bytes=row.get('stored_bytes',row.get('gzip_bytes'));stored_sha=row.get('stored_sha256',row.get('gzip_sha256'))
    if stored_bytes is not None:require(len(stored)==stored_bytes and sha(stored)==stored_sha,name+' complete retained compressed '+command['label']+' '+channel)
    require(len(data)==row.get('raw_bytes',row.get('bytes')) and sha(data)==row.get('raw_sha256',row.get('sha256')),name+' complete retained '+command['label']+' '+channel)
 save('ROOT_PRIOR_RECEIPTS.json',{'original':load(AUDIT/'root_original_reproduction_receipt.json'),'families':load(AUDIT/'root_family_reproduction_receipt.json')})
 checkpoint(20,'Immutable earlier audit/family/priority/review seals and full original receipts verified; clearance literal-bound.')
 pr=api('start_pr','pulls/367');mainref=api('start_main','git/ref/heads/main');mergeref=api('start_merge_ref','git/ref/pull/367/merge');testmerge=api('start_merge_commit','git/commits/'+mergeref['object']['sha'])
 head_tree=git('head_tree','rev-parse',pins['head']+'^{tree}').decode().strip()
 require(git('branch','branch','--show-current')==b'main\n','work stayed on main')
 git('base_ancestor','merge-base','--is-ancestor',pins['base'],pins['head'])
 validate_pr(pr,pins,mainref,testmerge,head_tree)
 public_pr={'checked_utc':utc(),'head':pr['head'],'base':pr['base'],'body':pr['body'],'draft':pr['draft'],'state':pr['state'],'merged':pr['merged'],'mergeable':pr['mergeable'],'mergeable_state':pr['mergeable_state'],'merge_commit_sha':pr['merge_commit_sha'],'testmerge':testmerge,'main_ref':mainref}
 save('EXACT_LIVE_METADATA.json',public_pr)
 original=load(AUDIT/'root_original_reproduction_receipt.json');target_rows=[r for r in original['all44_actual_files'] if r['path'].startswith(PREFIX+'/')]
 expected_paths=sorted([r['path'] for r in target_rows]+[QUEUE]);require(len(target_rows)==43,'complete original43 target paths')
 delta=git('full_delta','diff','--name-only',pins['base'],pins['head']).decode().splitlines();require(delta==expected_paths,'exact full Git delta44')
 apifiles=api('all_files','pulls/367/files?per_page=100&page=1');require(api('files_end','pulls/367/files?per_page=100&page=2')==[],'actual API pagination exhausted')
 require(sorted(r['filename'] for r in apifiles)==expected_paths,'exact full44 API file scope')
 bypath={r['filename']:r for r in apifiles};bytes_by_path={};live=[]
 for row in target_rows+[{'path':QUEUE}]:
  path=row['path'];data=git('blob_'+str(len(live)),'show',pins['head']+':'+path);mode,kind,blob,_=git('mode_'+str(len(live)),'ls-tree',pins['head'],'--',path).decode().split(None,3)
  require(mode=='100644' and kind=='blob',path+' exact mode')
  require(bypath[path]['sha']==blob and bypath[path]['status']==('modified' if path==QUEUE else 'added'),path+' API mode/status/blob')
  raw=api('blob_'+str(len(live)),'git/blobs/'+blob);require(base64.b64decode(raw['content'])==data and raw['size']==len(data),path+' entire API/Git bytes')
  if path!=QUEUE:require(bind(data)=={'bytes':row['bytes'],'sha256':row['sha256']},path+' original immutable bytes')
  bytes_by_path[path]=data;live.append({'path':path,'mode':mode,'blob':blob,**bind(data),'status':bypath[path]['status']})
 before=git('base_queue','show',pins['base']+':'+QUEUE);validate_queue(before,bytes_by_path[QUEUE])
 save('ALL44_BINDINGS_AND_QUEUE.json',{'all_files':live,'queue_line':400,'queue_only_changed_cells':[8,9],'all_other_queue_bytes_identical':True})
 # The106 historical manifest records exclude the separate three primary-source records.
 for row in original['nested_bindings']:
  resolved=(Path(PREFIX)/Path(row['manifest']).parent/row['path']).as_posix();require(resolved in bytes_by_path,'original106 actual manifest-relative path '+resolved)
  data=bytes_by_path[resolved];require(bind(data)=={'bytes':row['bytes'],'sha256':row['sha256']},'original106 binding '+row['manifest']+':'+row['path'])
 require(len(original['nested_bindings'])==106,'all106 original nested bindings')
 historical=[]
 for then in original['all4_actual_author_checkpoint_API_records']:
  commit=then['sha'];actual=api('author_'+str(len(historical)),'git/commits/'+commit)
  require(actual==then,'entire actual historical API commit '+commit)
  require(git('author_tree_'+str(len(historical)),'rev-parse',commit+'^{tree}').decode().strip()==actual['tree']['sha'],'entire actual Git/API historical tree '+commit)
  require(git('author_parents_'+str(len(historical)),'rev-list','--parents','-n','1',commit).decode().split()==[commit]+[p['sha'] for p in actual['parents']],'actual Git/API historical parents '+commit)
  paths=git('author_paths_'+str(len(historical)),'ls-tree','-r','--name-only',commit,'--',PREFIX).decode().splitlines();entries=[]
  require(len(paths)==[7,14,21,34][len(historical)],'entire actual author checkpoint path count '+commit)
  for path in paths:
   data=git('author_blob_'+str(len(historical))+'_'+str(len(entries)),'show',commit+':'+path);require(data==bytes_by_path[path],'entire actual author checkpoint '+path)
   mode,kind,blob,_=git('author_mode_'+str(len(historical))+'_'+str(len(entries)),'ls-tree',commit,'--',path).decode().split(None,3)
   require(mode=='100644' and kind=='blob','actual historical mode '+path);entries.append({'path':path,'mode':mode,'blob':blob,**bind(data)})
  historical.append({'actual_commit':actual,'all_actual_files':entries})
 save('ORIGINAL106_BINDINGS_FOUR_CHECKPOINTS.json',{'all106_bindings':original['nested_bindings'],'actual_checkpoints':historical})
 checkpoint(45,'Refreshed live metadata, actual test-merge parents/tree, full44 Git/API scope, exact queue and historical checkpoints verified.')
 repair=load(AUDIT/'preprint/REPAIRED_REVIEW_PACKAGE_02.json');sealed=[]
 require(review_status['candidate_bindings']==repair['sealed_files'],'entire completed review exact four submission bindings')
 require(review_status['repaired_candidate_manifest_sha256']==sha((AUDIT/'preprint/REPAIRED_REVIEW_PACKAGE_02.json').read_bytes()),'completed second review exact repair record binding')
 for row in repair['sealed_files']:sealed.append(binding(AUDIT/'preprint'/row['path'],row,'exact submission '+row['path']))
 archive=AUDIT/'preprint/wajnryb-artin-a5-verification.zip';member_bytes={};zip_rows=[]
 with zipfile.ZipFile(archive) as zipped:
  infos=zipped.infolist();require(len(infos)==60 and len({i.filename for i in infos})==60,'closed60 ZIP members')
  expected_members={'fixed_generator_classification.tex','verification/MANIFEST.json'}|{'verification/'+r['path'] for r in load(AUDIT/'preprint/verification/MANIFEST.json')['files']}
  require({i.filename for i in infos}==expected_members,'exact closed ZIP member scope')
  for info in infos:
   require(not info.is_dir() and not Path(info.filename).is_absolute() and '..' not in Path(info.filename).parts,'safe ZIP member '+info.filename)
   data=zipped.read(info);require(data==(AUDIT/'preprint'/info.filename).read_bytes(),'complete ZIP/directory bytes '+info.filename);member_bytes[info.filename]=data;zip_rows.append({'path':info.filename,'CRC32':info.CRC,**bind(data)})
 save('EXACT_SUBMISSION_ALL60_MEMBERS.json',{'sealed_submission_files':sealed,'archive':bind(archive.read_bytes()),'all_members':zip_rows})
 source_rows=load(AUDIT/'preprint/verification/SOURCE_RECEIPTS.json')['receipts'];source_rows+=original['sources'];seen=set();fresh=[];source_bytes={}
 numdam_old='https://www.numdam.org/item/AMBP_2011__18_1_15_0.pdf';numdam_current='https://www.numdam.org/article/AMBP_2011__18_1_15_0.pdf'
 for row in source_rows:
  if row['url']==numdam_old:
   require(numdam_current in source_bytes,'canonical Numdam source already freshly retrieved')
   data=source_bytes[numdam_current];require(bind(data)=={'bytes':row['bytes'],'sha256':row['sha256']},'canonical Numdam bytes equal exact historical source binding')
   source_bytes[numdam_old]=data;fresh.append({'historical_url':numdam_old,'fresh_current_url':numdam_current,**bind(data),'historically_hash_bound':True,'chronology':'Historical obsolete /item/ route is preserved in original receipts; current primary /article/ PDF freshly fetched once above and full bytes bind identically.'});continue
  if row['url'] in seen:continue
  seen.add(row['url']);start=utc();data=run('fresh_source_'+str(len(fresh)),['curl','-L','--fail','--silent','--show-error','--connect-timeout','15','--max-time','60',row['url']],private=True)
  bound='bytes' in row and 'sha256' in row
  if bound:require(bind(data)=={'bytes':row['bytes'],'sha256':row['sha256']},'fresh exact source '+row['url'])
  source_bytes[row['url']]=data
  fresh.append({'url':row['url'],'started_utc':start,'finished_utc':utc(),**bind(data),'historically_hash_bound':bound,'chronology':'Fresh retrieval after earlier independent source/math/code seals; byte refresh does not reopen or retroactively establish source independence.'})
 save('FRESH_SOURCES_POSTGATES.json',fresh)
 checkpoint(60,'Closed reviewed submission/ZIP and fresh source bytes bound; mathematical replay begins in isolated private temporary copies.')
 with tempfile.TemporaryDirectory(dir=private,prefix='live_replay_') as temp:
  work=Path(temp);package=work/'package';package.mkdir()
  for name,data in member_bytes.items():
   path=package/name;path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(data)
  candidate=package/'verification/reference'
  for number in range(1,5):require(run('original_turn'+str(number),[PYTHON,'-B',candidate/f'check_turn_{number}.py'],work)==(candidate/f'TURN_{number}_CHECKS.json').read_bytes(),'complete original turn'+str(number)+' stdout')
  for label,script,expected in [('cpp_wrapper','verify_turn_4_cpp.py','TURN_4_CPP_CHECKS.json'),('review_control','review/independent_check.py','review/INDEPENDENT_CHECKS.json'),('author_replay','review/replay_author.py','review/AUTHOR_REPLAY.json')]:
   argv=[PYTHON,'-B',candidate/script]
   if label=='author_replay':argv.append(candidate)
   require(run(label,argv,work)==(candidate/expected).read_bytes(),'complete '+label+' stdout')
  require(run('original_publication',[PYTHON,'-B',candidate/'verify_publication.py'],work)==b'PASS: all frozen public bytes, four Python receipts, C++ full stream, and independent review controls\n','complete publication stdout')
  records=gzip.decompress(member_bytes['verification/certificates/30_action_records.txt.gz']);twenty=gzip.decompress(member_bytes['verification/certificates/20_full_actions.jsonl.gz'])
  exe=work/'cpp';require(run('compile_cpp',['g++','-O3','-std=c++17',candidate/'check_turn_4.cpp','-o',exe],work)==b'','complete compiler stdout')
  plain=run('cpp_plain',[exe],work);full=run('cpp_full',[exe,'--stream'],work);lines=full.splitlines(keepends=True)
  require(plain==b'{"status":"PASS","reachable_states":234368,"outgoing_edges":711342,"coaccessible_states":90921,"coaccessible_edges":261810}\n','entire literal C++ plain stdout')
  require(b''.join(line for line in lines if line.startswith(b'S|'))==records,'all90921 complete C++ record bytes')
  require(lines[-1]==plain,'entire C++ terminal stdout')
  require(full==records+plain,'entire literal C++ full stdout including terminal and no extra lines')
  # Reproduce the entire original packet again with the freshly retrieved primary files present.
  # The first original execution above had no source/ directory.
  sources=candidate/'source';sources.mkdir()
  for row in original['sources']:(sources/row['name']).write_bytes(source_bytes[row['url']])
  for number in range(1,5):require(run('with_sources_original_turn'+str(number),[PYTHON,'-B',candidate/f'check_turn_{number}.py'],work)==(candidate/f'TURN_{number}_CHECKS.json').read_bytes(),'complete with-sources original turn'+str(number)+' stdout')
  for label,script,expected in [('cpp_wrapper','verify_turn_4_cpp.py','TURN_4_CPP_CHECKS.json'),('review_control','review/independent_check.py','review/INDEPENDENT_CHECKS.json'),('author_replay','review/replay_author.py','review/AUTHOR_REPLAY.json')]:
   argv=[PYTHON,'-B',candidate/script]
   if label=='author_replay':argv.append(candidate)
   require(run('with_sources_'+label,argv,work)==(candidate/expected).read_bytes(),'complete with-sources '+label+' stdout')
  require(run('with_sources_original_publication',[PYTHON,'-B',candidate/'verify_publication.py'],work)==b'PASS: all frozen public bytes, four Python receipts, C++ full stream, and independent review controls\n','complete with-sources publication stdout')
  require(run('with_sources_cpp_plain',[exe],work)==plain,'entire with-sources C++ plain stdout')
  require(run('with_sources_cpp_full',[exe,'--stream'],work)==full,'entire with-sources C++ full stdout')
  shutil.rmtree(sources)
  del source_bytes,full,lines
  first=work/'independent';first.mkdir();(first/'fullstreams').mkdir();(first/'receipts').mkdir();shutil.copyfile(package/'verification/independent_20_30.py',first/'independent_20_30.py')
  start=utc();out=run('packaged_independent20_30',[PYTHON,'-B',first/'independent_20_30.py'],work);finish=utc();equal_run_local_utc(out,member_bytes['verification/independent_expected.json'],start,finish,'independent20/30')
  generated=gzip.decompress((first/'fullstreams/independent_backward_records.txt.gz').read_bytes());require(generated==records,'independent20/30 all literal records')
  (HERE/'fullstreams/independent20_30_records.txt.gz').write_bytes(gzip.compress(generated,mtime=0))
  del generated
  snapshot=work/'snapshot/problems/11000151_artin_a5_quotient';snapshot.mkdir(parents=True);shutil.copyfile(candidate/'check_turn_4.cpp',snapshot/'check_turn_4.cpp')
  second=work/'ranks';second.mkdir();(second/'receipts').mkdir();shutil.copyfile(package/'verification/independent_ranks1_6.py',second/'independent_ranks1_6.py')
  start=utc();out=run('packaged_independent_ranks',[PYTHON,'-B',second/'independent_ranks1_6.py'],work);finish=utc();expected_ranks=json.loads(member_bytes['verification/independent_ranks_expected.json']);rank_receipt=(second/'receipts/INDEPENDENT_FINITE_CONTROLS.json').read_bytes()
  equal_run_local_utc(rank_receipt,member_bytes['verification/independent_ranks_expected.json'],start,finish,'independent ranks receipt')
  actual_utc=json.loads(rank_receipt)['utc'];reference_utc=expected_ranks['utc'];expected_out=b''.join((json.dumps(r)+'\n').encode() for r in expected_ranks['ranks'])+member_bytes['verification/independent_ranks_expected.json']
  require(out.replace(actual_utc.encode(),reference_utc.encode(),1)==expected_out,'entire seven-value independent ranks stdout')
  for rank in range(1,7):
   data=(second/f'private_streams/rank{rank}_all_coaccessible_actions.txt').read_bytes();expected=records if rank==6 else gzip.decompress(member_bytes[f'verification/certificates/rank{rank}_action_records.txt.gz']);require(data==expected,'rank'+str(rank)+' all literal records');(HERE/'fullstreams'/f'rank{rank}_records.txt.gz').write_bytes(gzip.compress(data,mtime=0))
  require((second/'private_streams/all_810_F4_actions.jsonl').read_bytes()==twenty,'all810 complete packaged rank-control actions');(HERE/'fullstreams/all810_actions.jsonl.gz').write_bytes(gzip.compress(twenty,mtime=0))
  # Delete only own generated temporary large raw streams after their full comparisons.
  shutil.rmtree(first);shutil.rmtree(second);shutil.rmtree(work/'snapshot');exe.unlink()
  del data,out,rank_receipt
  # Retain every complete nested package-verifier subprocess output in the wrapper.
  wrapper=HERE/'retain_package_children.py';require(wrapper.exists(),'prepared package capture wrapper present')
  package_out=run('full_closed_package',[PYTHON,'-B',wrapper,package/'verification/verify_package.py',HERE/'fullstreams/package_child_outputs.jsonl.gz'],work)
  require(package_out==repair['package_verification_stdout'].encode(),'entire closed package verifier stdout')
  child_rows=[json.loads(line) for line in gzip.decompress((HERE/'fullstreams/package_child_outputs.jsonl.gz').read_bytes()).splitlines()]
  require(bool(child_rows),'complete package child log populated')
  for row in child_rows:
   require(row['returncode']==0 and base64.b64decode(row['stderr_b64'])==b'','complete nested package child successful/no stderr '+str(row['args']))
  save_compressed('PACKAGE_ALL_CHILD_OUTPUTS.json.gz',{'complete_children':child_rows,'all_outputs_retained':'fullstreams/package_child_outputs.jsonl.gz'})
 checkpoint(85,'Full original and both packaged independent replays, all810 actions and all90921 records compared; no selected-field acceptance.')
 # Falsify acceptance conditions by local fixture mutations only.
 for field,value in [('body',pr['body']+' altered'),('head',None),('base',None),('draft',True)]:
  mutant=copy.deepcopy(pr)
  if field in ('head','base'):mutant[field]['sha']='0'*40
  else:mutant[field]=value
  reject(field,lambda m=mutant:validate_pr(m,pins,mainref,testmerge,head_tree))
 changed_queue=bytes_by_path[QUEUE].splitlines(keepends=True);changed_queue[400]=changed_queue[400]+b'altered\n';reject('queue',lambda:validate_queue(before,b''.join(changed_queue)))
 firstrow=target_rows[0];bad=bytes_by_path[firstrow['path']]+b'altered';reject('target_bytes',lambda:assert_binding_bytes(bad,firstrow))
 packaged=load(package_manifest_path())['files'][0];bad_member=member_bytes['verification/'+packaged['path']]+b'altered';reject('package_binding',lambda:assert_binding_bytes(bad_member,packaged))
 merge_mutant=copy.deepcopy(testmerge);merge_mutant['tree']['sha']='0'*40;reject('merge_tree',lambda:validate_pr(pr,pins,mainref,merge_mutant,head_tree))
 endpr=api('end_pr','pulls/367');endmain=api('end_main','git/ref/heads/main');endmergeref=api('end_merge_ref','git/ref/pull/367/merge');endmerge=api('end_merge_commit','git/commits/'+endmergeref['object']['sha']);validate_pr(endpr,pins,endmain,endmerge,head_tree)
 require(endmerge==testmerge,'entire start/end test-merge commit unchanged')
 for row in baseline['immutable_prior_files']:binding(AUDIT/row['path'],row,'end immutable '+row['path'])
 for name in baseline['immutable_prior_manifests']:manifest(AUDIT/name)
 require(run('end_original_closed_audit',[PYTHON,'-B',HERE.parent/'verify_audit.py'])==b'PASS: complete self-excluded public audit, earlier/final seals and44 raw execution-output streams\n','entire end original closed-audit verifier stdout')
 for row in repair['sealed_files']:binding(AUDIT/'preprint'/row['path'],row,'end exact submission '+row['path'])
 with zipfile.ZipFile(archive) as zipped:
  require([i.filename for i in zipped.infolist()]==[r['path'] for r in zip_rows],'end ordered ZIP scope unchanged')
  for name,data in member_bytes.items():require(zipped.read(name)==data==(AUDIT/'preprint'/name).read_bytes(),'end entire ZIP/directory member unchanged '+name)
 require(sha(clearance.read_bytes())==pins['clearance_sha256'],'end completed clearance unchanged')
 manifest(review02,pins['review02_manifest_sha256'])
 save('CHECKS.json',CHECKS);checkpoint(100,'Qualified exact-live acceptance checks pass at literal refreshed pins; no mutation or external-human peer-review claim.')
 result={'status':'QUALIFIED_EXACT_LIVE_ACCEPTANCE_PASS','finished_utc':utc(),'head':pins['head'],'base':pins['base'],'body':bind(body),'testmerge_sha':testmerge['sha'],'testmerge_tree':head_tree,'checks':len(CHECKS),'complete_executions':len(CAPTURES),'candidate_git_service_mutations':False,'original127_manifest_untouched':True,'publication_clearance_literal_sha256':pins['clearance_sha256'],'scope':'Fixed standard generator theorem under both conventions; no new discovery, human peer-review or current-open certificate.'}
 save('FINAL_LIVE_RECEIPT.json',result)
 runpy.run_path(str(HERE/'seal_live_audit.py'),run_name='__main__')
 print(json.dumps(result,indent=2))

def assert_binding_bytes(data,row):assert bind(data)=={'bytes':row['bytes'],'sha256':row['sha256']},'complete binding bytes'
def package_manifest_path():return AUDIT/'preprint/verification/MANIFEST.json'

if __name__=='__main__':
 try:main()
 except BaseException:
  (HERE/'receipts').mkdir(exist_ok=True)
  save('FAILURE.json',{'utc':utc(),'status':'FAIL_NO_ACCEPTANCE','complete_traceback':traceback.format_exc(),'checks':CHECKS,'captures':CAPTURES})
  traceback.print_exc();raise
