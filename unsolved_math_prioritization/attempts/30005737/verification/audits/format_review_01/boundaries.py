#!/usr/bin/env python3
"""Additional independent boundary probes after the first completed run."""
import contextlib, copy, importlib.util, io, json, os
from pathlib import Path
import struct, sys, types
sys.path.insert(0,str(Path(__file__).resolve().parent))
import review as r
r.SEQ=max(int(p.name.split('-')[1].split('.')[0]) for p in r.TMP.glob('invocation-*.json'))
spec=importlib.util.spec_from_file_location('subject_boundaries',r.SUPPLIED/'portable.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
baseline=r.TMP/'portable';subject=baseline/'portable.py'
portable={str(p.relative_to(baseline)):p.read_bytes() for p in baseline.rglob('*') if p.is_file()}
current=r.fixture_current(portable)
curroot=r.TMP/'boundary_current';r.tree(curroot,current)
def actual_rejection(name, args, contains=None):return r.cli(name,args,tool=subject,accepted=False,contains=contains)
def current_zip_case(name,raw):
    outer=dict(current);outer['post-lie-verification.zip']=raw;r.reindex_current(outer,regenerate_zip=False)
    for n,b in outer.items():(curroot/n).write_bytes(b)
    actual_rejection(name,['current',r.sha(outer['CURRENT_PUBLICATION_MANIFEST.json']),'--root',curroot,'--verify-only'])

# Strict CLI identity, startup copy and parser contract boundaries.
actual_rejection('wrong_external_index_pin',['verify','0'*64,'--root',baseline,'--verify-only'])
actual_rejection('uppercase_external_index_pin',['verify',r.PIN.upper(),'--root',baseline,'--verify-only'])
actual_rejection('source_only_requires_three_paths',['source-only','--catalog',baseline/'metadata.json'])
for name,options in [('missing_isolation',[]),('optimize_two',['-I','-S','-B','-OO']),('missing_no_site',['-I','-B']),('missing_no_bytecode',['-I','-S'])]:
    meta,out,err=r.process(name,[r.PY,*options,str(subject),'verify',r.PIN,'--root',str(baseline),'--verify-only'])
    r.result(name,meta['returncode']==1 and err==b'' and json.loads(out).get('status')=='REJECTED')
meta,out,err=r.process('build_has_no_verify_only_option',[r.PY,'-I','-S','-B',str(subject),'build',r.PIN,str(r.TMP/'bad.zip'),'--root',str(baseline),'--verify-only'])
r.result('build_has_no_verify_only_option',meta['returncode']==2 and b'unrecognized arguments: --verify-only' in err)
meta,out,err=r.process('rejects_abbreviated_options',[r.PY,'-I','-S','-B',str(subject),'verify',r.PIN,'--roo',str(baseline),'--verify-only'])
r.result('rejects_abbreviated_options',meta['returncode']==2)
mut=r.TMP/'boundary_portable';r.tree(mut,portable)
def index_case(name,obj=None,raw=None):
    raw=raw if raw is not None else r.dump(obj)
    (mut/'package_index.json').write_bytes(raw)
    actual_rejection(name,['verify',r.sha(raw),'--root',mut,'--verify-only'])
    (mut/'package_index.json').write_bytes(portable['package_index.json'])
idx=json.loads(portable['package_index.json'])
for key,raw in [('nan',b'NaN'),('infinity',b'Infinity'),('negative_infinity',b'-Infinity'),('exponent_overflow',b'1e400')]:
    changed=portable['package_index.json'].replace(b'"bytes": 5228',b'"bytes": '+raw,1)
    index_case('actual_index_json_'+key,raw=changed)
for name,row in [('alias',dict(path='readme.md',bytes=0,sha256='0'*64)),('file_directory_collision',dict(path='README.md/leaf',bytes=0,sha256='0'*64)),('directory_case_alias',dict(path='SOURCE/leaf',bytes=0,sha256='0'*64))]:
    obj=copy.deepcopy(idx);obj['files'].append(row);index_case('actual_index_'+name,obj)
original=(mut/'portable.py').read_bytes();(mut/'portable.py').write_bytes(original+b'\n# Untrusted startup copy change\n')
changed=dict(portable);changed['portable.py']=(mut/'portable.py').read_bytes();(mut/'package_index.json').write_bytes(r.indexed({n:b for n,b in changed.items() if n!='package_index.json'}))
actual_rejection('startup_copy_mismatch_reindexed',['verify',r.sha((mut/'package_index.json').read_bytes()),'--root',mut,'--verify-only'],contains='authenticated startup copy mismatch')
(mut/'portable.py').write_bytes(original);(mut/'package_index.json').write_bytes(portable['package_index.json'])
original=(mut/'source/authored/PROOF.md').read_bytes();(mut/'source/authored/PROOF.md').write_bytes(original+b'\nchanged\n')
changed=dict(portable);changed['source/authored/PROOF.md']=(mut/'source/authored/PROOF.md').read_bytes();raw=r.indexed({n:b for n,b in changed.items() if n!='package_index.json'});(mut/'package_index.json').write_bytes(raw)
actual_rejection('immutable_original_even_with_new_index',['verify',r.sha(raw),'--root',mut,'--verify-only'],contains='pin mismatch: source/authored/PROOF.md')
(mut/'source/authored/PROOF.md').write_bytes(original);(mut/'package_index.json').write_bytes(portable['package_index.json'])
fifo=mut/'unlisted-fifo';os.mkfifo(fifo)
actual_rejection('special_fifo_rejected_without_open',['verify',r.PIN,'--root',mut,'--verify-only']);fifo.unlink()
output_link=r.TMP/'output-link';output_link.symlink_to(r.TMP/'build/post-lie-verification.zip')
actual_rejection('receipt_existing_symlink_leaf',['verify',r.PIN,'--root',baseline,'--receipt-dir',output_link])
buildlink=r.TMP/'build-symlink';buildlink.mkdir();(buildlink/'post-lie-verification.zip').symlink_to(r.TMP/'build/post-lie-verification.zip')
actual_rejection('build_existing_symlink_leaf',['build',r.PIN,buildlink/'post-lie-verification.zip','--root',baseline])
# Verify-only is independently checked with a process trap and replay trap.
oldp=m.subprocess.Popen;oldr=m.replay;calls=[]
def forbidden(*args,**kw):calls.append(True);raise RuntimeError('ARCHIVAL_PROCESS_TRAP')
m.subprocess.Popen=forbidden;m.replay=forbidden
args=types.SimpleNamespace(catalog=None,problems=None,reports=None,primary_dir=None,verify_only=True,receipt_dir=None)
try:
    value=m.verify_result(baseline,portable,r.PIN,args)
    r.result('verify_only_independent_zero_process_traps',not calls and value['replay']['label']=='VERIFY_ONLY_BYTE_AUTHENTICATION_NO_ARCHIVAL_EXECUTION')
finally:m.subprocess.Popen=oldp;m.replay=oldr
# Raw record fields must be honored, independently pinned current manifests.
raw=r.independent_zip(portable);central=struct.unpack_from('<I',raw,len(raw)-6)[0]
for name,offset,replacement in [('local_name_disagreement',30,b'X'),('local_time_disagreement',10,b'\x01\x00'),('central_create_system',central+4,b'\x14\x00'),('central_crc',central+16,b'\x00\x00\x00\x00'),('local_extract_version',4,b'\x0a\x00')]:
    damaged=raw[:offset]+replacement+raw[offset+len(replacement):]
    current_zip_case('actual_zip_'+name,damaged)
# Verify primary exact-name/type/byte contract without modifying source hardlinks.
prim=r.TMP/'boundary_primary';prim.mkdir()
for name in m.PRIMARY_PINS:os.link(r.BASE/'private_sources'/name,prim/name)
workspace=r.BASE.parents[2]
native=[workspace/'unsolved_math_prioritization/catalog.json',workspace/'unsolved_math_prioritization/cache/problems.json',workspace/'unsolved_math_prioritization/cache/research_results.json']
args=['--catalog',native[0],'--problems',native[1],'--reports',native[2]]
leaf=prim/'owr2023.pdf';leaf.unlink();leaf.write_bytes(b'%PDF-bad')
actual_rejection('primary_corrupt_size_hash_actual',['source-only',*args,'--primary-dir',prim])
leaf.unlink();leaf.symlink_to(r.BASE/'private_sources/owr2023.pdf')
actual_rejection('primary_symlink_actual',['source-only',*args,'--primary-dir',prim]);leaf.unlink();os.link(r.BASE/'private_sources/owr2023.pdf',leaf)
(prim/'empty').mkdir();actual_rejection('primary_unlisted_empty_directory_actual',['source-only',*args,'--primary-dir',prim]);(prim/'empty').rmdir()
# Independently derive full target pair and statement only after hashing ALL corpora.
hashes=[]
for name,path in zip(m.INPUT_PINS,native):
    h=r.hashlib.sha256();count=0
    with path.open('rb') as stream:
        for chunk in iter(lambda:stream.read(1048576),b''):h.update(chunk);count+=len(chunk)
    hashes.append(dict(name=name,bytes=count,sha256=h.hexdigest()))
r.result('independent_complete_native_authentication',all((row['bytes'],row['sha256'])==m.INPUT_PINS[row['name']] for row in hashes),hashes)
cat=json.loads(native[0].read_bytes());record=json.loads(native[1].read_bytes());reports=json.loads(native[2].read_bytes())
selected=[x for x in record if str(x.get('id'))=='30005737'];catalog=[x for x in cat if str(x.get('id'))=='30005737']
pair=json.dumps([selected[0],{}],sort_keys=True).encode();statement=selected[0]['statement'].encode()
r.result('independent_native_pair_statement_absent_report',len(selected)==len(catalog)==1 and (len(pair),r.sha(pair))==m.PAIR_PIN and (len(statement),r.sha(statement))==m.STATEMENT_PIN and 'OWR-14298013-001' not in reports,dict(pair=r.pin(pair),statement=r.pin(statement),target_report='ABSENT'))
del cat,record,reports,selected,catalog,pair,statement
original_src=json.loads((r.BASE/'SOURCE_MANIFEST.json').read_bytes())
allrows=[]
for label,root in [('original',r.BASE/'source'),('portable',r.SUPPLIED/'verification/source')]:
    for row in original_src['files']:
        b=(root/row['path']).read_bytes();allrows.append(dict(path=label+'/'+row['path'],passed=len(b)==row['bytes'] and r.sha(b)==row['sha256']))
r.result('final_all18_both_copies_unchanged',all(x['passed'] for x in allrows),allrows)
r.result('final_handoff_tool_and_manifest_unchanged',r.sha((r.SUPPLIED/'portable.py').read_bytes())==r.TOOL_PIN and r.sha((r.SUPPLIED/'SAFE_MANIFEST.json').read_bytes())==r.MAN_PIN)
r.save('BOUNDARY_SUMMARY.json',dict(timestamp_utc=r.stamp(),tests=len(r.RESULTS),passed=sum(x['passed'] for x in r.RESULTS),failed=sum(not x['passed'] for x in r.RESULTS),processes_total=r.SEQ))
print(json.dumps(dict(additional_tests=len(r.RESULTS),passed=sum(x['passed'] for x in r.RESULTS),failed=sum(not x['passed'] for x in r.RESULTS),processes_total=r.SEQ)))
