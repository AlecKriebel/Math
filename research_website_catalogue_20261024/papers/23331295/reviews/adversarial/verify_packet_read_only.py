#!/usr/bin/env python3
"""Pure offline custody closure: never imports or runs scientific/native code."""
from pathlib import Path
import hashlib,json,zipfile
E=Path(__file__).resolve().parent;P=E.parent.parent;S=P/'sources';checks=0
def need(v,m):
 global checks
 checks+=1
 if not v:raise RuntimeError(m)
def h(f):return hashlib.sha256(f.read_bytes()).hexdigest()
def obj(f):return json.loads(f.read_bytes())
def match(f,z):
 need(f.is_file()and not f.is_symlink(),'regularfile '+str(f));need(f.stat().st_size==z['bytes'],'size '+str(f));need(h(f)==z['SHA256'],'SHA256 '+str(f))
def main():
 m=obj(E/'MANIFEST.json');actual={f.relative_to(E).as_posix()for f in E.rglob('*')if f.is_file()}-{'MANIFEST.json','SEAL.json'}
 need(actual=={z['path']for z in m['owned_files']},'closed owned file set')
 for z in m['owned_files']:match(E/z['path'],z)
 if(E/'SEAL.json').exists():
  seal=obj(E/'SEAL.json');need(h(E/'MANIFEST.json')==seal['MANIFEST_SHA256'],'manifestseal')
  for k,n in [('REPORT_SHA256','REPORT.md'),('VERDICT_SHA256','VERDICT.json'),('READ_ONLY_VERIFIER_SHA256','verify_packet_read_only.py')]:need(h(E/n)==seal[k],k)
 inputs=obj(E/'INPUT_MANIFEST.json')['whole_source_directory'];need({str(f)for f in S.rglob('*')if f.is_file()}=={z['path']for z in inputs},'whole source set')
 for z in inputs:match(Path(z['path']),z)
 for name,want in [('SOURCE_READY.json','1380f9b64a17e237a38020778bc84b38984bfc6d1c05ae6acf5dd5516b665092'),('SOURCE_READY_SEAL.json','e683dda6b1cf61c87807214fe3602605f0fa9eed1118835141f39044f1e85b2b')]:need(h(S/name)==want,'source authority '+name)
 for name,want in [('INITIAL_SEAL.json','0fd1fa5ac0764e7cc256fdac95bc39436bfe34ac68103d2b49572957583be4eb'),('OWN_PROOF_RESULTS_SEAL.json','9c32b71bc83f5b9c8437c8b21d12e344d2ef9a88099a2c45198269de7752314c')]:
  need(h(E/name)==want,'earlyseal '+name)
  for z in obj(E/name)['files']:match(Path(z['path']),z)
 for f in(E/'native-objects').iterdir():need(f.read_bytes()==(S/f.name).read_bytes(),'whole literalnative '+f.name)
 ready=obj(S/'SOURCE_READY.json');dist=ready['native_schema_distinctions']
 need(type(dist['record_swh']['original_value'])is dict and not dist['record_swh']['original_value'],'native emptyobject')
 need(dist['versions_swh_fields'][0]['original_value']is None and dist['files_default_preview']['original_value']is None,'native explicitnull')
 need(type(dist['files_order']['original_value'])is list and not dist['files_order']['original_value'],'native emptyorder')
 need(ready['selected_actual_PDF']['pages_visually_or_scientifically_read']is False and ready['controlling_TeX']['preamble_or_mathematical_body_read']is False,'nativehistoricalflags unchanged')
 need([a['original_api_file_object']['key']for a in ready['all_native_assets_in_original_order']]==['nullstellensatz.tex','verification-package.zip','nullstellensatz.pdf'],'native assetorder')
 for a in ready['all_native_assets_in_original_order']:
  b=Path(a['path']).read_bytes();need(hashlib.md5(b).hexdigest()==a['original_api_file_object']['checksum'].split(':')[1],'nativeMD5');need(hashlib.sha256(b).hexdigest()==a['SHA256'],'nativeSHA256')
 custody=obj(E/'CUSTODY.json');members=custody['all_15_ZIP_payload_occurrences']
 with zipfile.ZipFile(S/'assets/verification-package.zip')as z:
  need(z.testzip()is None,'ZIP wholeCRC');need(len(z.infolist())==len(members)==15,'ZIPwholepayloadcount')
  for i,(f,a)in enumerate(zip(z.infolist(),members)):
   need(not f.is_dir()and i==a['ordinal_zero_based']and f.filename==a['native_filename'],'ZIPordernames')
   need(f.file_size==a['native_uncompressed_bytes']and f.compress_size==a['native_compressed_bytes'],'ZIPsizes')
   need(f'{f.CRC:08x}'==a['native_CRC32']and f.flag_bits==a['native_flags']and f.external_attr==a['native_external_attr']and f.create_system==a['native_create_system']and list(f.date_time)==a['native_date_time']and f.compress_type==a['native_compression_method'],'ZIPwholemetadata')
   b=z.read(f);need(hashlib.sha256(b).hexdigest()==a['SHA256']and b==Path(a['extracted_path']).read_bytes(),'ZIPpayloadbyteequivalence')
 native=S/'published-source/asset-002';copy=E/'native-isolated'
 names={f.relative_to(native).as_posix()for f in native.rglob('*')if f.is_file()};need(names=={f.relative_to(copy).as_posix()for f in copy.rglob('*')if f.is_file()},'isolatedcompletefilelist')
 for n in names:need((native/n).read_bytes()==(copy/n).read_bytes(),'isolatedunchanged '+n)
 native_m=obj(native/'MANIFEST.json')['files'];need(names==set(native_m)|{'MANIFEST.json'},'nativeclosedmanifest')
 for n,z in native_m.items():match(native/n,z)
 need((native/'nullstellensatz.tex').read_bytes()==(S/'assets/nullstellensatz.tex').read_bytes(),'standalonearchivedTeX')
 need(not any(n.endswith('.pdf')for n in names),'nativearchivePDFabsence')
 runs=obj(E/'NATIVE_REPLAY.json')['runs'];need(len(runs)==2,'selectedtwoonlyreplays')
 original_records=obj(native/'FRESH_CONTROL_RUNS.json')['runs']
 for run in runs:
  mode=run['mode'];base=next(r for r in original_records if r['kind']=='primary'and r['variant']=='baseline'and r['mode']==mode)
  need(run['whole_native_baseline_record']==base,'wholenativeexpectedobject')
  out=(E/f'NATIVE_{mode}.stdout').read_bytes();err=(E/f'NATIVE_{mode}.stderr').read_bytes();o=json.loads(out)
  need(run['exit_code']==0 and not err,'selectedexit/stderr')
  need(hashlib.sha256(out).hexdigest()==base['stdout_SHA256']==run['stdout_SHA256'],'wholeexpectedstdoutSHA')
  need(hashlib.sha256(err).hexdigest()==base['stderr_SHA256']==run['stderr_SHA256'],'wholeexpectedstderrSHA')
  need(o['categories']==base['categories']and o['assertions']==base['check_count'],'everycategory/total')
  need(o['artifact_sha256']==base['proof_companion_SHA256']and o['verifier_sha256']==base['code_SHA256'],'wholeoutputidentity')
 receipts=obj(E/'cache/primary/GET_RECEIPTS.json');need(len(receipts)==4,'boundedfourprimaryPDFs')
 for r in receipts:need(r['status']==200,'primaryactual200');match(E/'cache/primary'/r['filename'],r)
 denied=obj(E/'cache/primary/STOIMENOW_ACCESS.json');need(denied['published_body_authenticated']is False,'exacteditionnotinvented')
 need([r['status']for r in denied['hops']]==[302,403],'actualpublisherfailurechain')
 for r in denied['hops']:match(E/'cache/primary'/r['body_file'],r)
 verdict=obj(E/'VERDICT.json');need(verdict['record_id']==23331295 and verdict['followup']is None and verdict['publication_authority']is False,'verdictidentitygates')
 need(verdict['mathematical_remaining_gap']is None and verdict['full_original_mathematical_scope_validated']is True,'recordedclaimscope')
 print(json.dumps({'status':'PASS_PURE_CUSTODY_ONLY','checks':checks,'owned_payloads':len(m['owned_files']),'original_source_files_unchanged':len(inputs),'native_ZIP_payloads':len(members),'scientific_code_rerun':False,'network_used':False,'writes_performed':False},indent=2))
if __name__=='__main__':main()
