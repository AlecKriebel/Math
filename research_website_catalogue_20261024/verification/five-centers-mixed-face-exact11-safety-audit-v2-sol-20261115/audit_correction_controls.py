"""Fresh independent selected-function namespace/runtime controls; all fixtures in this own folder."""
from pathlib import Path,PurePosixPath
import ast,copy,hashlib,json,os,re,stat,tempfile
D=Path(__file__).resolve().parent
O=D.parent/'five-centers-mixed-face-production-integration-preparation-v2-sol-20261115'

def need(ok,label):
 if not ok:raise RuntimeError(label)
def sha(b):return hashlib.sha256(b).hexdigest()
def denied(call,label,records):
 try:call()
 except (RuntimeError,ValueError,FileNotFoundError) as e:records.append({'case':label,'rejected':True,'diagnostic':str(e)})
 else:raise RuntimeError('missed rejection: '+label)
def selected(name,base):
 tree=ast.parse((O/name).read_bytes());names={'need','sha','read','obj','pin','safe_rel','extent','live_path','closed_namespace','runtime_custody','verify_preparation'}
 nodes=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in names]
 e=dict(Path=Path,PurePosixPath=PurePosixPath,json=json,hashlib=hashlib,os=os,re=re,stat=stat,O=base,W=base/'never-live',LIVE_AUTHORIZED=False,CHECKS=0)
 exec(compile(ast.Module(body=nodes,type_ignores=[]),'<independent exact current selected definitions>','exec'),e)
 return e

def main():
 results=[];source_contract=json.loads((O/'RUNTIME_CONTRACT.json').read_bytes());held=json.loads((O/'HELD_BASELINE_CONTRACT.json').read_bytes())
 with tempfile.TemporaryDirectory(prefix='fresh-correction-',dir=D) as name:
  parent=Path(name)
  for code in ['exact11_lib.py','verify_preparation.py']:
   base=parent/code.removesuffix('.py');base.mkdir();e=selected(code,base);rejects=[]
   packet=base/'namespace';packet.mkdir();(packet/'inputs').mkdir();(packet/'nested').mkdir();(packet/'payload').write_bytes(b'x');(packet/'nested/kept').write_bytes(b'y');(packet/'PREPARATION_SEAL.json').write_bytes(b'root terminal')
   files=['nested/kept','payload'];dirs=['inputs','nested'];terms=['PREPARATION_SEAL.json'];check=lambda:e['closed_namespace'](packet,files,dirs,terms)
   check()
   (packet/'extra-empty').mkdir();denied(check,'unexpected empty directory',rejects);(packet/'extra-empty').rmdir()
   (packet/'extra-file').write_bytes(b'u');denied(check,'unexpected ordinary file',rejects);(packet/'extra-file').unlink()
   os.mkfifo(packet/'fifo');denied(check,'FIFO rejected before read',rejects);(packet/'fifo').unlink()
   (packet/'symlink-file').symlink_to(packet/'payload');denied(check,'symlink to regular file',rejects);(packet/'symlink-file').unlink()
   (packet/'symlink-directory').symlink_to(packet/'inputs');denied(check,'symlink to declared empty directory',rejects);(packet/'symlink-directory').unlink()
   (packet/'nested/PREPARATION_SEAL.json').write_bytes(b'unlisted nested terminal');denied(check,'no recursive terminal basename exclusion',rejects);(packet/'nested/PREPARATION_SEAL.json').unlink()
   denied(lambda:e['closed_namespace'](packet,files+['payload'],dirs,terms),'duplicate declared file',rejects)
   denied(lambda:e['closed_namespace'](packet,files,list(reversed(dirs)),terms),'noncanonical declared directory list',rejects)
   check()
   # The library preparation check itself must no longer exempt any run-state subtree.
   if code=='exact11_lib.py':
    prep=base/'prep';prep.mkdir();(prep/'payload').write_bytes(b'p');mb=json.dumps({'files':[{'path':'payload','bytes':1,'SHA256':sha(b'p')}],'directories':[]}).encode();(prep/'PREPARATION_MANIFEST.json').write_bytes(mb);cb=b'{}';(prep/'PREPARATION_CLOSURE.json').write_bytes(cb);(prep/'PREPARATION_SEAL.json').write_text(json.dumps({'MANIFEST_SHA256':sha(mb),'CLOSURE_SHA256':sha(cb),'owned_payload_count':1}))
    before=e['O'];e['O']=prep
    try:
     e['verify_preparation']();(prep/'run-state').mkdir();(prep/'run-state/arbitrary').write_bytes(b'unsealed')
     denied(e['verify_preparation'],'library prep rejects former run-state carveout',rejects)
    finally:e['O']=before
   runtime=Path(str(base)+'-runtime');contract=copy.deepcopy(source_contract);contract['runtime_root']=str(runtime);cb=json.dumps(contract).encode();prep_sha='e'*64
   absent=e['runtime_custody'](runtime,prep_sha,cb,held);need(absent['phase']=='ABSENT','absent own runtime')
   denied(lambda:e['runtime_custody'](parent/'wrong-runtime',prep_sha,cb,held),'runtime name must match exact contract',rejects)
   runtime.mkdir();phase_receipts=[]
   def put(name,value):
    b=value if isinstance(value,bytes) else json.dumps(value).encode();(runtime/name).write_bytes(b);return b
   adoption={'fixture_only_not_actual_root_authority':True,'schema':'root_five_centers_mixed_face_exact11_production_adoption_v1','authority':'root','template_not_root_receipt':False,'root_stage_adopted':True,'independent_code_audit_adopted':True,'complete_current_helper_and_rendered_output_adopted':True,'production_install_authorized':True,'preparation_final_seal_SHA256':prep_sha,'root_stage_reading_SHA256':contract['root_stage_reading_SHA256'],'runtime_root':str(runtime),'runtime_contract_SHA256':sha(cb)}
   ab=put('ROOT_ADOPTION.json',adoption);adopt_sha=sha(ab);put('PRE_INSTALL.json',{'fixture_only_not_actual_root_authority':True,'root_adoption_SHA256':adopt_sha,'actual_parent':contract['parent'],'exact11':[{'path':p.removeprefix('public/')} for p in contract['gitpaths']]})
   def write_state(phase,approval=None):
    descriptors={n:{'bytes':len((runtime/n).read_bytes()),'SHA256':sha((runtime/n).read_bytes())} for n in contract['phases'][phase]['files']}
    s={'schema':'exact11-durable-runtime-state-v1','phase':phase,'preparation_final_seal_SHA256':prep_sha,'runtime_contract_SHA256':sha(cb),'root_adoption_SHA256':adopt_sha,'root_commit_approval_SHA256':approval,'files':descriptors,'directories':[]};put('STATE.json',s);return s
   check_runtime=lambda:e['runtime_custody'](runtime,prep_sha,cb,held)
   def observe(phase):
    r=check_runtime();need(r['phase']==phase,'positive phase '+phase);phase_receipts.append({'phase':phase,'result':r,'complete_state':json.loads((runtime/'STATE.json').read_bytes())})
   write_state('INSTALL_STARTED');observe('INSTALL_STARTED')
   put('commit.index',b'OWN TOY INDEX ONLY');denied(check_runtime,'partial next-phase object cannot inherit prior success',rejects)
   pending={'fixture_only_not_actual_root_authority':True,'root_adoption_SHA256':adopt_sha,'parent':contract['parent'],'commit':'a'*40,'tree':'c'*40,'gitpaths':contract['gitpaths'],'public_counts':[623,94,95],'shared_index_SHA256_unchanged':held['Git']['index_SHA256'],'protected_raw_records_SHA256':held['Git']['protected_raw_records_SHA256'],'temporary_index_SHA256':sha((runtime/'commit.index').read_bytes())}
   pb=put('PENDING_COMMIT.json',pending);write_state('INSTALLED');observe('INSTALLED')
   (runtime/'unlisted-empty').mkdir();denied(check_runtime,'installed runtime extra empty directory',rejects);(runtime/'unlisted-empty').rmdir()
   os.mkfifo(runtime/'fifo');denied(check_runtime,'runtime FIFO',rejects);(runtime/'fifo').unlink()
   (runtime/'symlink').symlink_to(runtime/'commit.index');denied(check_runtime,'runtime symlink',rejects);(runtime/'symlink').unlink()
   saved=(runtime/'commit.index').read_bytes();put('commit.index',b'changed');denied(check_runtime,'runtime content changed without descriptor update',rejects);put('commit.index',saved)
   s=write_state('INSTALLED');s['phase']='PUBLISHED';put('STATE.json',s);denied(check_runtime,'phase jump without published extent',rejects);write_state('INSTALLED')
   s=write_state('INSTALLED');s['unexpected']=True;put('STATE.json',s);denied(check_runtime,'extra STATE schema field',rejects);write_state('INSTALLED')
   bad=copy.deepcopy(pending);bad['protected_raw_records_SHA256']='0'*64;put('PENDING_COMMIT.json',bad);write_state('INSTALLED');denied(check_runtime,'rehashed pending protected stream mismatch',rejects);put('PENDING_COMMIT.json',pending);write_state('INSTALLED')
   approval={'fixture_only_not_actual_root_authority':True,'schema':'root_five_centers_mixed_face_exact11_commit_approval_v1','authority':'root','publication_authorized':True,'root_adoption_SHA256':adopt_sha,'pending_commit_receipt_SHA256':sha(pb),**{k:pending[k] for k in ['parent','commit','tree','gitpaths','protected_raw_records_SHA256']}}
   approval_b=put('ROOT_COMMIT_APPROVAL.json',approval);approval_sha=sha(approval_b);approved=put('shared-index.approved',b'OWN TOY APPROVED BUFFER ONLY')
   prepub={'fixture_only_not_actual_root_authority':True,'root_adoption_SHA256':adopt_sha,'root_commit_approval_SHA256':approval_sha,'old_index_SHA256':held['Git']['index_SHA256'],'approved_index_SHA256':sha(approved),'commit':pending['commit']};put('PRE_PUBLICATION.json',prepub);put('PUSH.stdout',b'OWN TOY OUTPUT, NO PUSH')
   publication={'fixture_only_not_actual_root_authority':True,**{k:pending[k] for k in ['parent','commit','tree','gitpaths','protected_raw_records_SHA256']},'counts':[623,94,95]};put('PUBLICATION.json',publication);write_state('PUBLISHED',approval_sha);observe('PUBLISHED')
   bad=copy.deepcopy(approval);bad['commit']='d'*40;bad_sha=sha(put('ROOT_COMMIT_APPROVAL.json',bad));changed_pre=copy.deepcopy(prepub);changed_pre['root_commit_approval_SHA256']=bad_sha;put('PRE_PUBLICATION.json',changed_pre);write_state('PUBLISHED',bad_sha);denied(check_runtime,'rehashed approval and prepub still cannot change pending commit',rejects)
   put('ROOT_COMMIT_APPROVAL.json',approval);put('PRE_PUBLICATION.json',prepub);write_state('PUBLISHED',approval_sha)
   put('shared-index.approved',b'changed buffer');write_state('PUBLISHED',approval_sha);denied(check_runtime,'rehashed approved buffer still bound to PRE_PUBLICATION',rejects);put('shared-index.approved',approved);write_state('PUBLISHED',approval_sha)
   bad=copy.deepcopy(publication);bad['counts']=[623,94,96];put('PUBLICATION.json',bad);write_state('PUBLISHED',approval_sha);denied(check_runtime,'rehashed publication count drift',rejects);put('PUBLICATION.json',publication);write_state('PUBLISHED',approval_sha)
   check_runtime();complete_bodies={n:json.loads((runtime/n).read_bytes()) if n.endswith('.json') else {'hex':(runtime/n).read_bytes().hex()} for n in contract['phases']['PUBLISHED']['files']}
   results.append({'source':code,'synthetic_fixture_only_never_actual_root_authority':True,'positive_namespace_declared_empty_inputs_and_exact_root_terminal':True,'positive_phase_receipts':phase_receipts,'full_toy_contract':contract,'full_published_toy_bodies':complete_bodies,'negative_cases':rejects})
 print(json.dumps({'status':'PASS_FRESH_INDEPENDENT_CORRECTION_NAMESPACE_RUNTIME_CONTROLS','results':results,'reviewed_modules_or_owner_controls_imported_or_executed':False,'actual_installer_Git_website_runtime_or_root_authority_touched':False,'all_fixture_writes_only_own_temporary_child_removed_after_observation':True},indent=2))
if __name__=='__main__':main()
