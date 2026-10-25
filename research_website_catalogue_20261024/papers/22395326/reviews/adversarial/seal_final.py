"""Final read-only evidence seal. Run once after scientific report completion."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json
D=Path(__file__).resolve().parent
def sha(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        for b in iter(lambda:f.read(1<<20),b''):h.update(b)
    return h.hexdigest()
def req(c,m):
    if not c:raise RuntimeError(m)
def bind(p):return {'path':str(p.relative_to(D)),'bytes':p.stat().st_size,'sha256':sha(p)}
req(not (D/'FINAL_SEAL.json').exists(),'final seal already exists')
early=D/'EARLY_SEAL.json';req(sha(early)=='69aec360d173c342dba7caa95aaa2ea9e502c9853095cd4b9892ee04bfcb0374','early seal unchanged')
e=json.loads(early.read_text());req(sha(Path(e['ledger']['path']))==e['ledger']['sha256'],'early substantive ledger unchanged')
for p in e['read_objects']:
    req(sha(Path(p['path']))==p['sha256'],'early read object unchanged')
o=json.loads((D/'ORIGINAL_BINDINGS.json').read_text())
for row in o['source_objects']:
    p=Path(row['path']);req(p.stat().st_size==row['bytes'] and sha(p)==row['sha256'],'original final drift')
old=json.loads((D/'PREVIOUS_PACKET_PRESERVATION.json').read_text())
for packet in old['packets']:
    for row in packet['owned_bindings']+[packet['manifest'],packet['seal']]:
        p=Path(row['path']);req(sha(p)==row['sha256'],'previous packet final drift')
primary=json.loads((D/'PRIMARY_BINDINGS.json').read_text())
for name in ['transport_custody_receipts','actual_PDF_and_extraction_bindings','selected_interface_bindings','original_archive_bindings']:
    for row in primary[name]:req(sha(Path(row['path']))==row['sha256'],'primary final drift')
execution=json.loads((D/'EXECUTION_RECEIPT.json').read_text())
req(len(execution['runs'])==8,'eight preserved execution records')
req(sum(r['exit_code']==0 for r in execution['runs'])==4,'four positive runs and four rejections')
interval=json.loads((D/'INTERVAL_ARITHMETIC_RESULTS.json').read_text())
req(interval['strict_krawczyk_inclusion_recomputed'] and interval['direct_box_strict_physics_recomputed'],'own interval result present')
verdict=json.loads((D/'verdict.json').read_text());req(verdict['publication_authorization'] is False,'root authority')
work=[]
for p in sorted((D/'replay-work').rglob('*')):
    req(not p.is_symlink(),'no symlink disposable output')
    if p.is_file():work.append(bind(p))
(D/'REPLAY_WORK_MANIFEST.json').write_text(json.dumps({'scope':'Bounded exact replays, mutation fixtures, generated results and read-only target renderings; all ignored before writing.','files':work},indent=2)+'\n')
required=['REPORT.md','verdict.json','DERIVATIONS.md','ATTACK_LEDGER.md','READ_LEDGER.md','ORIGINAL_BINDINGS.json','PRIMARY_BINDINGS.json','PREVIOUS_PACKET_PRESERVATION.json','EXECUTION_RECEIPT.json','INDEPENDENT_EXACT_RESULTS.json','INTERVAL_ARITHMETIC_RESULTS.json','VISUAL_RENDER_RECEIPT.json','RESEARCH_LOG.md']
req(all((D/n).is_file() for n in required),'complete final packet')
files=[bind(p) for p in sorted(D.iterdir()) if p.is_file() and p.name not in {'FINAL_MANIFEST.json','FINAL_SEAL.json'}]
now=datetime.now(timezone.utc).isoformat()
m={'utc':now,'record_id':'22395326','status':'COMPLETE_BOUNDED_INDEPENDENT_ADVERSARIAL_REVIEW','completion_percent':100,'scope':'Full original target and explicit imported mathematical interfaces, with bounded exact execution and declared unexecuted upstream regeneration.','files':files,'original_source_bindings':133,'original_archive_members':118,'prior_packets':10,'prior_owned_files':147,'disposable_files_bound':len(work),'root_publication_authority_retained':True,'all_203_goal_ongoing':True}
manifest=D/'FINAL_MANIFEST.json';manifest.write_text(json.dumps(m,indent=2)+'\n')
seal=D/'FINAL_SEAL.json';seal.write_text(json.dumps({'utc':now,'manifest':'FINAL_MANIFEST.json','manifest_sha256':sha(manifest),'owned_file_count':len(files),'disposable_file_count':len(work),'status':'IMMUTABLE_FINAL_EVIDENCE_SEALED'},indent=2)+'\n')
for p in D.rglob('*'):
    if p.is_file():p.chmod(0o444)
for row in files:req(sha(D/row['path'])==row['sha256'],'owned file seal validation')
print(json.dumps({'REPORT':sha(D/'REPORT.md'),'verdict':sha(D/'verdict.json'),'FINAL_MANIFEST':sha(manifest),'FINAL_SEAL':sha(seal),'owned_files':len(files),'disposable_files':len(work)},indent=2))
