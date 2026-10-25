"""Read-only custody verification; --record writes only a new root receipt."""
from pathlib import Path, PurePosixPath
import hashlib, json, sys, zipfile
from datetime import datetime, timezone

O=Path(__file__).resolve().parent
B=O.parents[1]
P=B.parents[1]
seen={}
def need(ok,msg):
    if not ok: raise RuntimeError(msg)
def load(p): return json.loads(Path(p).read_text())
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def check(p,r):
    p=Path(p)
    need(p.is_file() and not p.is_symlink(),str(p))
    need(p.stat().st_size==r['bytes'] and sha(p)==r['sha256'],'binding '+str(p))
    seen[str(p)]={'bytes':r['bytes'],'sha256':r['sha256']}
def row(p):
    p=Path(p); return {'path':str(p),'bytes':p.stat().st_size,'sha256':sha(p)}
def mapped(base,d):
    for n,r in d.items():check(Path(base)/n,r)
def listed(base,rows):
    for r in rows:check(Path(base)/r['path'],r)

source=B/'sources'; scope=B/'reviews/scope'; analytic=B/'reviews/analytic'; adv=B/'reviews/adversarial'
sm=load(source/'SOURCE_FINAL_MANIFEST.json')
mapped(source,sm['files'])
check(source/'SOURCE_FINAL_MANIFEST.json',load(source/'SOURCE_FINAL_SEAL.json')['manifest'])
fm=load(scope/'FINAL_MANIFEST.json')
mapped(scope,fm['files']);mapped(source,fm['source_files'])
for r in fm['existing_primary_bindings']:check(r['path'],r)
check(scope/'FINAL_MANIFEST.json',load(scope/'FINAL_SEAL.json')['manifest'])
mapped(Path('/'),load(scope/'PRESERVATION_BEFORE.json')['owned_prior_bindings_only'])
am=load(analytic/'MANIFEST.json');listed(analytic,am['portable_files'])
need(sha(analytic/'MANIFEST.json')==load(analytic/'SEAL.json')['manifest_sha256'],'analytic seal')
listed(analytic,load(analytic/'cache-manifest.json')['files'])
for r in load(analytic/'external-bindings.json')['bindings']:check(r['path'],r)
listed(adv,load(adv/'FINAL_MANIFEST.json')['files'])
need(sha(adv/'FINAL_MANIFEST.json')==load(adv/'FINAL_SEAL.json')['manifest_sha256'],'adversarial seal')
ob=load(adv/'ORIGINAL_BINDINGS.json')
for r in ob['originals']:check(r['path'],r)
for k in ['source_manifest','source_seal','archive']:check(ob[k]['path'],ob[k])
pb=load(adv/'PRESERVATION_BINDINGS.json')
for r in pb['actual_primary_pdf_objects']+pb['raw_primary_receipts']:check(r['path'],r)
for packet in pb['prior_packets']:
    for k in ['manifest','seal']:check(packet[k]['path'],packet[k])
    for r in packet['owned_files']:check(r['path'],r)
ready=load(source/'SOURCE_READY.json');raw=load(source/'record.raw.json')
need('version' not in raw['metadata'] and ready['version_field_present'] is False and ready['version'] is None,'absent version')
need([a['original_api_file_object'] for a in ready['all_assets']]==raw['files'],'whole native file objects/order')
for a in ready['all_assets']:
    check(a['path'],a)
    need(hashlib.md5(Path(a['path']).read_bytes()).hexdigest()==a['md5']==a['original_api_file_object']['checksum'].split(':')[1],'asset md5')
archive=source/'source-and-verification.zip'; members=load(source/'archive-members.json')['members']
need(len(members)==41 and len({m['member'] for m in members})==41,'unique member map')
byname={m['member']:m for m in members}
with zipfile.ZipFile(archive) as z:
    files=[i for i in z.infolist() if not i.is_dir()]
    need(len(files)==41 and len({i.filename for i in files})==41 and {i.filename for i in files}==set(byname),'complete archive set')
    for info in files:
        name=PurePosixPath(info.filename)
        need(not name.is_absolute() and '..' not in name.parts and '\\' not in info.filename and info.external_attr>>16&0o170000!=0o120000,'safe member')
        data=z.read(info);m=byname[info.filename]
        need(len(data)==m['bytes'] and hashlib.sha256(data).hexdigest()==m['sha256'] and f'{info.CRC:08x}'==m['CRC32'],'archive CRC/body')
        need(Path(m['extracted_path']).read_bytes()==data,'existing extraction exact')
initial=load(O/'INITIAL_SEAL.json');check(P/initial['path'],initial)
reports={}
for family,vname in [('scope','VERDICT.json'),('analytic','verdict.json'),('adversarial','verdict.json')]:
    folder=B/'reviews'/family
    reports[family]={'report':row(folder/'REPORT.md'),'verdict_file':row(folder/vname),'whole_original_custom_verdict':load(folder/vname)}
renders=[row(P/'tmp/pdfs/root23217863-primary-20261025'/n) for n in ['roydor12.png','openai24.png','jkr22.png']]
result={'utc':datetime.now(timezone.utc).isoformat(),'status':'ROOT_FULL_SOURCE_AND_REVIEW_CUSTODY_VERIFIED',
        'record_id':'23217863','unique_existing_bindings_verified':len(seen),'source_files_including_final_manifest_seal':54,
        'prior_scope_bindings_verified':3686,'complete_safe_ZIP_members_CRC_body_compared':41,'asset_order':'PDF then ZIP',
        'whole_original_API_objects_preserved':True,'version_absent_not_synthesized':True,'reports':reports,
        'root_actual_primary_render_views':renders,'root_review':row(O/'ROOT_REVIEW.md'),
        'binding_maps':[row(p) for p in [source/'SOURCE_FINAL_MANIFEST.json',scope/'FINAL_MANIFEST.json',scope/'PRESERVATION_BEFORE.json',analytic/'MANIFEST.json',analytic/'cache-manifest.json',analytic/'external-bindings.json',adv/'FINAL_MANIFEST.json',adv/'ORIGINAL_BINDINGS.json',adv/'PRESERVATION_BINDINGS.json']],
        'source_or_prior_packet_writes':0,'source_program_or_checker_or_HTTP_reexecution':False,
        'overall_203_goal_complete':False}
if '--record' in sys.argv:
    out=O/'custody-recheck-20261025.json'
    with out.open('x') as f:json.dump(result,f,indent=2,ensure_ascii=False);f.write('\n')
print(json.dumps({k:v for k,v in result.items() if k not in ['reports','binding_maps','root_actual_primary_render_views']},indent=2))
