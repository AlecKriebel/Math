"""Pure final scope custody checker. Standard library only; no project imports,
subprocesses, science execution, network, rendering, bytecode generation or writes.
Scientific derivations/results are held as whole bytes; they are not replayed.
"""
from pathlib import Path
from hashlib import sha256,md5
import json,sys,zipfile,io,zlib
A=Path(__file__).resolve().parent
checks=0
def need(ok,label):
 global checks
 checks+=1
 if not ok:raise ValueError(label)
def read(p):
 need(p.is_file() and not p.is_symlink(),'regular nonsymlink '+str(p));return p.read_bytes()
def binding(b):return {'bytes':len(b),'SHA256':sha256(b).hexdigest()}
def obj(p):return json.loads(read(p))
def same(a,b):
 if type(a) is not type(b):return False
 if isinstance(a,dict):return list(a)==list(b) and all(same(a[k],b[k]) for k in a)
 if isinstance(a,list):return len(a)==len(b) and all(same(x,y) for x,y in zip(a,b))
 return a==b
def namespace(root):
 paths=list(root.rglob('*'));need(not any(p.is_symlink() for p in paths),'no namespace symlinks')
 return sorted(str(p.relative_to(root)) for p in paths if p.is_file())
need(sys.argv[1:] in ([],['--preseal']),'bounded option')
preseal=sys.argv[1:]==['--preseal'];V=obj(A/'VERDICT.json');protocol=obj(A/'SOURCE_PROTOCOL_BINDINGS.json');m=obj(A/'custody/INPUT_MANIFEST.json');S=Path(m['source_root'])
need(read(A/'SOURCE_PROTOCOL_BINDINGS.json')==read(A/'custody/WHOLE_LITERAL_NATIVE.json'),'whole unflattened native protocol byte identity')
need(len(m['files'])==87 and namespace(S)==m['source_namespace'],'complete87original source namespace no basename exceptions')
need(namespace(A/'custody/raw')==m['source_namespace'],'complete87freshraw namespace')
by_original={r['original']:r for r in m['files']}
for r in m['files']:
 expected={'bytes':r['bytes'],'SHA256':r['SHA256']};b=read(A/'custody'/r['copy'])
 need(binding(b)==expected and read(Path(r['original']))==b,'whole literal original and rawsource identity')
def raw(path):return A/'custody'/by_original[str(Path(path))]['copy']
ready=protocol['SOURCE_READY_whole_literal'];source_seal=protocol['SOURCE_READY_SEAL_whole_literal']
need(binding(read(S/'SOURCE_READY.json'))['SHA256']=='28a9736d92beaadb1faa37c9146d56191be83fb217116f24b33162bea922e469','exact incoming READYpin')
need(binding(read(S/'SOURCE_READY_SEAL.json'))['SHA256']=='c523e830e06555037254c26d9d85c82f4324c841cdd268f99d95664bf02e2150','exact actualsourceSEALpin')
for n,k in [('SOURCE_READY.json','SOURCE_READY_whole_literal'),('SOURCE_READY_SEAL.json','SOURCE_READY_SEAL_whole_literal'),('ALL_TRANSPORT_RECEIPTS.json','transport_aggregate_whole_literal'),('NATIVE_SCHEMA_TYPES.json','schema_whole_literal'),('ARCHIVE_CUSTODY.json','archive_custody_whole_literal'),('MANUSCRIPT_CUSTODY.json','manuscript_custody_whole_literal'),('SOURCE_READY_MANIFEST.json','source_manifest_whole_literal'),('SOURCE_READY_CLOSURE.json','source_closure_whole_literal'),('INPUT_MANIFEST.json','source_input_manifest_whole_literal')]:
 need(same(obj(S/n),protocol[k]),'whole types/key/list/header/order/null/history '+n)
need(same(V['whole_original_source_READY'],ready),'own verdict wholeoriginalREADY unchanged')
need(ready['record_id']==23331331 and ready['sheet_row']==133 and ready['version']=='1.0','native exact identity')
need(ready['completion_percent_at_preseal']==100 and source_seal['completion_percent']==100,'actual historical100notgeneric95')
for n in ['printed_title_date_version_inspected','target_PDF_text_extracted','target_PDF_rasters_visually_read','mathematical_PDF_TeX_or_pixels_read','TeX_preamble_or_mathematical_body_read','source_scientific_proofs_code_results_triage_reviews_or_opinions_read']:
 need(ready[n] is False,'actualoriginalunreadflag '+n)
need(ready['target_PDF_pages_rendered'] is True and ready['scientific_verdict'] is None and ready['publication_authority'] is False and ready['source_programmes_executed']==[],'original source rendered/unread/null/false states literal')
need(len(protocol['native_API_whole_literal'])==4,'whole four nativeAPIs')
for descriptor,o in zip(ready['whole_native_API_objects'],protocol['native_API_whole_literal']):need(same(obj(raw(descriptor['path'])),o),'whole rawAPI literal types and order')
record,latest,versions,files=protocol['native_API_whole_literal']
need(type(record['conceptrecid']) is str and record['conceptrecid']=='23331330','native concept string')
need(same(record['swh'],{}) and same(latest['swh'],{}) and versions['hits']['hits'][0]['swh'] is None,'native empty/null/absent distinctions')
need(type(files['entries']) is list and same(files['order'],[]) and files['default_preview']=='outer_pedal_centroid.pdf','actualnative files list/order/previewstring')
trans=protocol['transport_aggregate_whole_literal'];need(type(trans) is list and len(trans)==7,'actualtransports list7 no genericreceiptsadapter')
need(type(protocol['schema_whole_literal']) is list and len(protocol['schema_whole_literal'])==403,'wholeactual403row schema list')
need([t['HTTP_status'] for t in trans]==[200,301,200,200,200,200,200],'nativeHTTP sequence/order')
for t in trans:
 need(same(obj(raw(t['body_path']+'.transport.json')),t),'whole actualtransport types/key/header/list/order')
 need(binding(read(raw(t['body_path'])))=={'bytes':t['bytes'],'SHA256':t['SHA256']},'whole native responsebody')
assets=ready['all_native_assets_in_original_order'];need([Path(t['path']).suffix for t in assets]==['.zip','.pdf'],'nativeZIPthenPDF assetorder')
for t in assets:
 b=read(raw(t['path']));need(binding(b)=={'bytes':t['bytes'],'SHA256':t['SHA256']} and 'md5:'+md5(b).hexdigest()==t['original_api_file_object']['checksum'],'whole native asset checksums')
need(read(A/'manuscript/actual-published.pdf')==read(raw(ready['selected_actual_PDF']['path'])),'actual manuscriptPDF nativebyteidentity')
need(read(A/'manuscript/controlling.tex')==read(raw(ready['controlling_TeX']['extracted_path'])),'all controllingTeX nativebyteidentity')
need(len(read(A/'manuscript/controlling.tex').splitlines())==342,'actual342controllinglines')
need(ready['selected_actual_PDF']['pages']==5,'complete5page nativePDFcustody')
archive=protocol['archive_custody_whole_literal'];occ=archive['regular_payload_occurrences']
need(len(occ)==38 and len(archive['containers'])==1,'complete38payloads1container')
with zipfile.ZipFile(io.BytesIO(read(raw(assets[0]['path'])))) as z:
 entries=[q for q in z.infolist() if not q.is_dir()]
 need([q.filename for q in entries]==[q['original_member_name'] for q in occ],'whole native regular memberorder')
 for q,r in zip(entries,occ):
  b=z.read(q);need(b==read(raw(r['extracted_path'])) and binding(b)=={'bytes':r['bytes'],'SHA256':r['SHA256']},'opaqueZIPmember completebytes')
  need(q.CRC==(zlib.crc32(b)&0xffffffff) and f'{q.CRC:08x}'==r['CRC32'],'whole opaque nativeCRC')
initial=obj(A/'INITIAL_SEAL.json')
for r in initial['files']:need(binding(read(Path(r['path'])))=={'bytes':r['bytes'],'SHA256':r['SHA256']},'unchangedpreforeignscientific initial payload')
need(initial['foreign_scientific_material_unread'] is True and initial['distinct_claim_proof_scope_families']==14,'owninitial scope/independence boundary')
need(V['native_scientific_programmes_executed']==[] and V['current_or_archived_scientific_peer_or_root_opinions_read'] is False,'native noexecution and peerindependence')
need(V['publication_authority'] is False and V['root_only_scientific_adoption_authority'] is True and V['canonical_url'] is None and V['AA'] is None and V['follow_up'] is None,'closedroot and nullpublication gates')
need(V['root_scientific_gate']=='CLOSED' and V['findings_released_to_root'] is False,'literal gate atfinalization')
need('raw/' in read(A/'custody/.gitignore').decode().splitlines() and 'raw/' in read(A/'primary/.gitignore').decode().splitlines(),'whole raw custody/primary directories ignored')
for r in obj(A/'PRIMARY_FETCH_RECEIPTS.json')['sources']:
 b=read(A/r['local']);need(binding(b)=={'bytes':r['bytes'],'SHA256':r['SHA256']},'actualprimarybytes retained')
 need(b.startswith(b'%PDF')==r['actual_is_PDF'],'actualPDFvsHTML accesslimit notcoerced')
code=obj(A/'CODE_MANIFEST.json')
for r in code['files']:need(binding(read(A/r['path']))=={'bytes':r['bytes'],'SHA256':r['SHA256']},'whole own helper body')
if not preseal:
 manifest=obj(A/'MANIFEST.json');seal=obj(A/'FINAL_SEAL.json')
 need(binding(read(A/'MANIFEST.json'))==seal['manifest'],'whole finalmanifest seal')
 expected=sorted(manifest['payloads']);actual=sorted(set(namespace(A))-{'MANIFEST.json','FINAL_SEAL.json'})
 need(actual==expected,'entire own namespace exact rootterminal exclusions only')
 for p,e in manifest['payloads'].items():need(binding(read(A/p))==e,'whole ownedpayload identity')
 need(binding(read(A/'REPORT.md'))==seal['report'] and binding(read(A/'VERDICT.json'))==seal['whole_literal_verdict'],'full report and unique literalverdict bound')
print(json.dumps({'scope':'row133 pure final custody; no scientific replay','mode':'preseal' if preseal else 'sealeddefault','positive_custody_checks':checks,'complete_source_files':87,'whole_native_APIs':4,'actual_transports':7,'whole_nativeZIPpayloads':38,'complete_native_manuscript_pages':5,'controlling_TeX_lines':342,'initial_independence_history_intact':True,'projectimports_network_subprocess_scienceexecution_rendering_or_writes':False,'root_gate_atseal':'CLOSED','canonical_url':None,'AA':None,'follow_up':None},ensure_ascii=False,indent=2))
