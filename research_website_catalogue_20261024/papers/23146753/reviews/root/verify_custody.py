"""Root read/hash verification; --record creates only a new own receipt."""
from pathlib import Path, PurePosixPath
import json, hashlib, zipfile, sys, datetime
O=Path(__file__).resolve().parent;B=O.parents[1];P=B.parents[1];S=B/'sources';seen={}
def need(x,m):
    if not x:raise RuntimeError(m)
def load(p):return json.loads(Path(p).read_text())
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def row(p):
    p=Path(p);return {'path':str(p),'bytes':p.stat().st_size,'sha256':sha(p)}
def check(p,r,capital=False):
    p=Path(p);digest=r['SHA256'] if capital else r['sha256']
    need(p.is_file() and not p.is_symlink() and p.stat().st_size==r['bytes'] and sha(p)==digest,'binding '+str(p))
    seen[str(p)]=True
def listed(base,rows,capital=False):
    for r in rows:check(Path(base)/r['path'],r,capital)
def mapped(base,m):
    for n,r in m.items():check(Path(base)/n,r)
listed(S,load(S/'SOURCE_MANIFEST.json')['files'])
need(sha(S/'SOURCE_MANIFEST.json')==load(S/'SOURCE_SEAL.json')['manifest_sha256'],'final source seal')
sc=B/'reviews/scope';an=B/'reviews/analytic';ad=B/'reviews/adversarial'
listed(sc,load(sc/'MANIFEST.json')['files'])
need(sha(sc/'MANIFEST.json')==load(sc/'SEAL.json')['manifest_sha256'],'scope seal')
listed(Path('/'),load(sc/'ORIGINAL_BINDINGS.json')['files'])
listed(sc,load(sc/'CACHE_MANIFEST.json')['files'])
listed(an,load(an/'FINAL_MANIFEST.json')['files'],True)
check(an/'FINAL_MANIFEST.json',load(an/'FINAL_SEAL.json')['manifest'],True)
ib=load(an/'INPUT_BINDINGS.json')
for key in ['source_files','original_primary_bodies','original_primary_receipts_and_publisher_metadata','additive_source_final_controls']:listed(Path('/'),ib[key],True)
listed(an,load(an/'CACHE_BINDINGS.json')['files'],True)
am=load(ad/'FINAL_MANIFEST.json');mapped(ad,am['owned_bindings']);mapped(Path('/'),am['original_bindings'])
check(ad/'FINAL_MANIFEST.json',load(ad/'FINAL_SEAL.json')['manifest_binding'])
ready=load(S/'SOURCE_READY.json');raw=load(S/'record.raw.json')
need([a['original_api_file_object'] for a in ready['all_assets']]==raw['files'],'whole native object/order')
need([a['original_api_file_object']['key'] for a in ready['all_assets']]==['mtp2-edge-closure-verification.zip','mtp2-edge-closure-note.pdf'],'actual ZIP then PDF')
for a in ready['all_assets']:
    check(a['path'],a)
    need(hashlib.md5(Path(a['path']).read_bytes()).hexdigest()==a['md5']==a['original_api_file_object']['checksum'].split(':')[1],'actual asset MD5')
members=load(S/'archive-members.json')['members'];table={m['member']:m for m in members}
need(len(table)==len(members)==13,'complete unique13')
with zipfile.ZipFile(S/'mtp2-edge-closure-verification.zip') as z:
    infos=[i for i in z.infolist() if not i.is_dir()]
    need(len(infos)==13 and len({i.filename for i in infos})==13 and {i.filename for i in infos}==set(table),'exact ZIP set')
    for i in infos:
        n=PurePosixPath(i.filename);need(not n.is_absolute() and '..' not in n.parts and '\\' not in i.filename and (i.external_attr>>16&0o170000) in [0,0o100000],'safe regular body')
        data=z.read(i);m=table[i.filename]
        need(len(data)==m['bytes'] and hashlib.sha256(data).hexdigest()==m['sha256'] and f'{i.CRC:08x}'==m['CRC32'] and data==Path(m['extracted_path']).read_bytes(),'CRC/hash/extraction exact')
    need(z.read('output/pdf/mtp2_edge_closure.pdf')==(S/'mtp2-edge-closure-note.pdf').read_bytes(),'one byte-identical reader')
primary=load(ad/'PRIMARY_LEDGER.json')['entries']
for r in primary:check(r['path'],r)
need(len(primary)==9,'nine actual primary bodies')
initial=load(O/'INITIAL_SEAL.json');check(P/initial['path'],initial)
reports={}
for family,vname in [('scope','verdict.json'),('analytic','VERDICT.json'),('adversarial','VERDICT.json')]:
    folder=B/'reviews'/family
    reports[family]={'report':row(folder/'REPORT.md'),'verdict_file':row(folder/vname),'whole_original_custom_verdict':load(folder/vname)}
receipt={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'ROOT_ORIGINAL_SOURCE_AND_THREE_REVIEW_PACKETS_CUSTODY_VERIFIED','record_id':'23146753','unique_bindings_verified':len(seen),'original_source_files_with_additive_final_controls':27,'archive_safe_regular_CRC_body_comparisons':13,'embedded_reader_byteidentical':True,'actual_native_asset_order':'ZIP then PDF','all_original_custom_verdicts_retained':reports,'nine_actual_primary_bodies_rehashed':primary,'root_viewed_renders':[row(P/'tmp/pdfs/root23146753-primary-20261025'/n) for n in ['target1.png','pq9.png']],'source_program_HTTP_or_prior_math_controls_rerun':False,'source_or_prior_packet_writes':0,'overall203_goal_complete':False}
if '--record' in sys.argv:
    with (O/'custody-recheck-20261025.json').open('x') as f:json.dump(receipt,f,indent=2,ensure_ascii=False);f.write('\n')
print(json.dumps({k:v for k,v in receipt.items() if k not in ['all_original_custom_verdicts_retained','nine_actual_primary_bodies_rehashed','root_viewed_renders']},indent=2))
