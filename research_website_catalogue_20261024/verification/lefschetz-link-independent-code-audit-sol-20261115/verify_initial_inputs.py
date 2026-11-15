"""Pure independent prewriter custody checker. No project imports, network,
subprocess, source/science/owner-program execution, rendering or writes.
No writer or website access: the future605baseline still requires explicit GO.
After INITIAL_SEAL exists, verify all initial payloads; later phase additions
are allowed outside this fixed initial manifest, while raw membership stays exact.
"""
from pathlib import Path
from hashlib import sha256,md5
import json,re,sys,zipfile,io,zlib
A=Path(__file__).resolve().parent;checks=0
def need(ok,label):
 global checks
 checks+=1
 if not ok:raise ValueError(label)
def read(p):
 need(p.is_file() and not p.is_symlink(),'regular nonsymlink '+str(p));return p.read_bytes()
def obj(p):return json.loads(read(p))
def binding(b):return {'bytes':len(b),'SHA256':sha256(b).hexdigest()}
def same(a,b):
 if type(a) is not type(b):return False
 if isinstance(a,dict):return list(a)==list(b) and all(same(a[k],b[k]) for k in a)
 if isinstance(a,list):return len(a)==len(b) and all(same(x,y) for x,y in zip(a,b))
 return a==b
def names(p):
 allp=list(p.rglob('*'));need(not any(q.is_symlink() for q in allp),'namespace symlink forbidden');return sorted(str(q.relative_to(p)) for q in allp if q.is_file())
need(sys.argv[1:] in ([],['--preseal']),'boundedinitialcustodyoption');preseal=sys.argv[1:]==['--preseal']
m=obj(A/'INPUT_MANIFEST.json');c=obj(A/'WHOLE_NATIVE_AND_EDITORIAL_CONTRACT.json');e=obj(A/'EXPECTED_OUTPUTS.json');receipts=obj(A/'COMPARISON_RECEIPTS.json')
need(m['raw_ignored_before_creation'] is True and read(A/'.gitignore').decode().splitlines()==['raw/'],'raw ignoredentirelybeforecreation')
need(len(m['files'])==245,'whole245originalinputs')
need(names(A/'raw')==sorted(Path(v['copy']).relative_to('raw').as_posix() for v in m['files'].values()),'entire rawnamespace no exclusions')
for row in m['files'].values():
 b=read(A/row['copy']);need(binding(b)=={'bytes':row['bytes'],'SHA256':row['SHA256']} and read(Path(row['original']))==b,'wholefreshoriginal/rawbyteidentity')
for p,ns in m['complete_namespaces'].items():need(names(Path(p))==ns['relative_files'] and len(ns['relative_files'])==ns['count'],'complete originalnamespace no basename exceptions')
need([n['count'] for n in m['complete_namespaces'].values()]==[65,41,65,60],'exact65/41/65/60')
need(receipts['count']==len(receipts['whole_typed_ordered_comparisons'])==206 and receipts['all_equal'] is True,'recordedwholetyped206events')
need(all(r['same_types_keyorder_listorder_values'] is True for r in receipts['whole_typed_ordered_comparisons']),'typed/ordercomparisonevents retained')
for i,rec in enumerate(c['records']):
 rid=rec['record_id'];ed=Path(next(p for p in m['complete_namespaces'] if '/'+rid+'/reviews/editorial' in p));s=ed.parents[1]/'sources';ready=rec['source_ready_whole_literal'];pub=rec['publication_config_whole_literal'];promotion=rec['promotion_config_whole_literal'];adoption=rec['root_editorial_authority_whole_literal']
 files={'protocol':rec['source_protocol_whole_literal'],'publication':pub,'promotion':promotion,'adapter':rec['adapter_whole_literal'],'rootclearance':rec['root_scientific_clearance_whole_literal']}
 config='config/' if i==0 else ''
 for q,v in [(s/'SOURCE_READY.json',ready),(ed/(config+'publication.json'),pub),(ed/(config+'promotion.json'),promotion),(ed/'SCHEMA_ADAPTER.json',rec['adapter_whole_literal']),(ed/'SOURCE_PROTOCOL_BINDINGS.json',rec['source_protocol_whole_literal'])]:need(same(obj(q),v),'wholeoriginal config/protocol/native object exacttypeskeysorder')
 for spec in receipts['whole_descriptor_originals']:
  if spec['record_id']!=rid:continue
  node=files[spec['container']]
  for token in spec['pointer']:node=node[token]
  need(same(node['whole_literal_object'],obj(Path(spec['original']))),'whole originalembedded descriptor typed/order exact')
 need(pub['canonical_url'] is None and pub['AA'] is None and pub['follow_up'] is None and promotion['canonical_url'] is None and promotion['AA'] is None,'literal private config nulls unchanged')
 need(ready['completion_percent_at_preseal']==100 and ready['scientific_verdict'] is None and ready['publication_authority'] is False,'actualsourcehistorical100/null/false unchanged')
 need(ready['printed_title_date_version_inspected'] is False,'historical unread flag preserved')
 need(same(obj(Path(ready['actual_transport_receipts']['path'])),rec['transport_aggregate_whole_literal']),'whole actualtransport list/key/headerorder')
 need(type(rec['transport_aggregate_whole_literal']) is list and len(rec['transport_aggregate_whole_literal'])==7+i,'actual heterogeneous transport list count')
 need(type(rec['native_schema_whole_literal']) is list and same(obj(Path(ready['native_schema_types']['path'])),rec['native_schema_whole_literal']),'whole original nativeschemalist')
 for d,o in zip(ready['whole_native_API_objects'],rec['native_API_whole_literal']):need(same(obj(Path(d['path'])),o),'whole actualnativeAPI field/order/null values')
 native_order=rec['native_order'];expected_order=['periodic-lefschetz-source-and-verification.zip','periodic-lefschetz.pdf'] if i==0 else ['nullstellensatz.tex','verification-package.zip','nullstellensatz.pdf']
 need(native_order==expected_order,'exactnativeZIPPDF/TeXZIPPDF order')
 for asset in rec['native_assets_in_literal_order']:
  q=asset['native_original_object'];b=read(Path(q['path']));need(binding(b)==asset['binding'] and 'md5:'+md5(b).hexdigest()==q['original_api_file_object']['checksum'],'whole actual native asset checksum')
  need(b==read(ed/'candidate'/asset['candidate_relative']),'full nativecandidate assetbytes')
 need(binding(read(ed/'candidate/assets/citation.bib'))==rec['BibTeX']['binding'],'whole originalBib')
 text=read(ed/'candidate/index.html').decode();main=re.search(r'<main\b[^>]*>.*?</main>',text,re.S)[0]
 need(main==rec['original_main'] and main+'\n'==read(ed/'PUBLIC_MAIN.html').decode(),'whole main and exactone-publicmain trailingnewline')
 expected=main.replace('<main>','<main id="main">',1) if main.startswith('<main>') else main
 need(expected==rec['expected_main_with_only_missing_id'] and binding(expected.encode())==rec['main_expected_binding'],'exact full main onlypermitted missing id')
 need(adoption['root_editorial_adopted'] is True and adoption['future_native_encoding_order_preserved'] is True and adoption['website_baseline_freeze_requires_separate_explicit_GO'] is True and adoption['production_installation_authorized'] is False,'fullrooteditorialadoption separateGO/installgates')
 if i==0:
  need(pub['code_license']=='MIT' and adoption['future_127_ZIP_MediaObject_omit_blanket_encoding_license_preserve_visible_split_CCBY_MIT_rights'] is True,'127exactmixedrights outputrefinement')
  need(type(pub['collaboration']) is list,'127actualarraycollaboration')
 else:
  need(pub['code_license'] is None and pub['printed_version'] is None and pub['printed_version_field_present'] is False and pub['version']=='1.0','128broadCCBYandnativevsprintededition')
  need(type(pub['collaboration']) is str,'128actualscalarcollaboration')
 # Pure opaque complete archive body/CRC checks, never execute a payload.
 archive=rec['archive_custody_whole_literal'];occ=archive['regular_payload_occurrences'];zipasset=next(a for a in ready['all_native_assets_in_original_order'] if a['path'].endswith('.zip'))
 need(len(archive['containers'])==1 and len(occ)==[18,15][i],'whole18/15 payloads onecontainer each')
 with zipfile.ZipFile(io.BytesIO(read(Path(zipasset['path'])))) as z:
  items=[p for p in z.infolist() if not p.is_dir()];need([p.filename for p in items]==[o['original_member_name'] for o in occ],'whole native archive regular memberorder')
  for info,o in zip(items,occ):
   b=z.read(info);need(binding(b)=={'bytes':o['bytes'],'SHA256':o['SHA256']} and b==read(Path(o['extracted_path'])),'wholeopaque nativeZIP/extractedbyteidentity')
   need(info.CRC==(zlib.crc32(b)&0xffffffff) and f'{info.CRC:08x}'==o['CRC32'],'nativepayloadCRC unchanged')
need(e['derivation']=={'record127_leaves':4,'record128_leaves_including_nativeTeX':5,'new_leaves':9,'aggregate_replacements':2,'overlay_paths':11},'derived11paths includingnativeTeX')
need(len(set(e['exact_overlay_paths']))==11 and e['conditional_virtual_counts_if_futurebaseline_confirmed']==[614,92,93],'conditional614/92/93 counts')
need(e['website_baseline_captured'] is False and e['website_GO_received'] is False and e['root_editorial_adoptions_received'] is True,'initialnoGO/nobaseline/rooteditorialreceived statesliteral')
need(e['publication_authority'] is False and e['canonical_url'] is None and e['AA'] is None and e['follow_up'] is None,'no publication/canonical authority')
if not preseal:
 seal=obj(A/'INITIAL_SEAL.json');manifest=obj(A/'INITIAL_MANIFEST.json');need(binding(read(A/'INITIAL_MANIFEST.json'))==seal['manifest'],'whole independentinitialmanifestseal')
 for p,b in manifest['payloads'].items():need(binding(read(A/p))==b,'unchanged wholeinitialpayload')
print(json.dumps({'scope':'pureindependent prewriter custody','mode':'preseal' if preseal else 'sealedinitial','positive_custody_checks':checks,'whole_original_files':245,'source_editorial_counts':[65,41,65,60],'whole_typed_comparison_events':206,'derived_overlay_paths':11,'new_leaves':9,'future_GO_and_actual_baseline_pending':True,'writer_or_website_read':False,'projectimports_network_subprocess_science_owner_execution_or_writes':False,'publication_authority':False,'canonical_url':None,'AA':None,'follow_up':None},ensure_ascii=False,indent=2))
