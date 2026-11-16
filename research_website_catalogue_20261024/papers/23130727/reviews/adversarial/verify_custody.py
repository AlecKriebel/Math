"""Pure offline custody. No scientific/project import, network, subprocess or write.

Default guards the exact final files AND directories. --preseal explicitly checks
only the frozen bindings before the two outer terminal files are created.
"""
from pathlib import Path
import hashlib
import json
import stat
import sys
import zipfile
import zlib

E=Path(__file__).resolve().parent
INITIAL='1dd7868fa5cce7d7b3a880bbfc05d549d64e68a9b79b9b6feb3973b4e36ed4b3'
RESULTS='9eccfae42cf1e262bcab3e926faf75ab893691b9784039ba35543954334370b0'
CORE='0f285e35daa206f53aa931946c4bcc6c5b01ae6b4b59a231a861b0a6fe11d104'
TERMS={'MANIFEST.json','FINAL_SEAL.json'}
COUNT=0

def need(ok,why):
    global COUNT
    COUNT+=1
    if not ok:raise ValueError(why)

def sha(b):return hashlib.sha256(b).hexdigest()

def readj(name):return json.loads((E/name).read_bytes())

def check(row,base=None):
    p=Path(row['path']) if base is None else base/row['path']
    need(stat.S_ISREG(p.lstat().st_mode),'ordinary file '+str(p))
    b=p.read_bytes()
    need(type(row['bytes']) is int and len(b)==row['bytes'],'whole length '+str(p))
    need(sha(b)==row['SHA256'],'whole SHA256 '+str(p))
    return b

def literal(x):
    if isinstance(x,dict):return ('dict',tuple((k,literal(v)) for k,v in x.items()))
    if isinstance(x,list):return ('list',tuple(literal(v) for v in x))
    return (type(x).__name__,x)

def same(a,b,why):need(literal(a)==literal(b),why)

def inventory(root):
    files=set();dirs=set()
    for p in root.rglob('*'):
        mode=p.lstat().st_mode;r=p.relative_to(root).as_posix()
        need(stat.S_ISREG(mode) or stat.S_ISDIR(mode),'no symlink/special entry '+r)
        (dirs if stat.S_ISDIR(mode) else files).add(r)
    return files,dirs

def namespace(af,ad,ef,ed):
    need(af==set(ef),'exact file namespace')
    need(ad==set(ed),'exact directory namespace')

def reject(fn,why):
    try:fn()
    except ValueError:need(True,why)
    else:need(False,'negative accepted '+why)

def controls():
    reject(lambda:same(1,True,'typed'),'integer/bool')
    reject(lambda:same({'a':None,'b':[]},{'b':[],'a':None},'ordered'),'key order')
    reject(lambda:same({'a':None},{},'absent'),'null/absent')
    reject(lambda:namespace({'x','nested/MANIFEST.json'},{'nested'},{'x'},set()),'nested terminal-name file')
    reject(lambda:namespace({'x'},{'empty'},{'x'},set()),'empty directory')
    reject(lambda:need(b'buffer'==b'buffeR','one byte'),'whole stdout mutation')

def main():
    need(sys.argv[1:] in ([],['--preseal']),'arguments')
    partial=bool(sys.argv[1:])
    b=(E/'INITIAL_SEAL.json').read_bytes();need(sha(b)==INITIAL,'initial immutable')
    initial=json.loads(b);need(len(initial['payloads'])==147,'initial all payloads')
    for n,r in initial['payloads'].items():check(dict(r,path=n),E)
    b=(E/'OWN_PROOF_CONTROL_SEAL.json').read_bytes();need(sha(b)==RESULTS,'own actual result immutable')
    result=json.loads(b);em=json.loads(check(result['manifest'],E))
    for n,r in em['files'].items():check(dict(r,path=n),E)
    protected=readj('PROTECTED_INPUTS.json');need(len(protected['files'])==146,'source plus qualified core')
    for r in protected['files']:
        a=check(r);b=check(dict(r,path=r['copy']),E);need(a==b,'whole opaque copy identity')
    s=protected['source_namespace'];af,ad=inventory(Path(s['path']))
    namespace(af,ad,s['files'],s['directories']);need(len(af)==128 and len(ad)==18,'whole source cardinality')
    core=readj('QUALIFIED_CORE_AUTHORITY_BINDING.json');b=check(core['original_by_reference']);need(sha(b)==CORE,'actual neutral qualified core authority')
    c=json.loads(b);same(c,core['whole_literal_contract'],'whole core object')
    need(len(c['files'])==18 and c['original17_plus_sole_authorized405b_checkpoint'] is True and c['all18_original_unchanged_claim'] is False,'17 originals plus sole separately authorized405b')
    for r in c['files']:check(r)
    protocol=readj('SOURCE_PROTOCOL_BINDINGS.json')
    wrappers=[protocol['whole_SOURCE_READY']]+protocol['whole_native_API_objects_in_original_role_order']+[v for k,v in protocol.items() if k.endswith('.json')]
    need([r['role'] for r in protocol['whole_native_API_objects_in_original_role_order']]==['record','latest','versions-page001','files'],'original native API role order')
    for r in wrappers:
        b=check(r['original']);need(b==(E/r['copy']).read_bytes(),'whole wrapper copy');same(json.loads(b),r['whole_literal_object'],'whole original ordered typed object')
    ar=readj('NATIVE_ARCHIVE_LITERAL_BINDINGS.json');need(len(ar['archives'])==1 and ar['regular_payloads']==69,'native ZIP and all69 payloads')
    for a in ar['archives']:
        check(a['original'])
        with zipfile.ZipFile(a['original']['path']) as z:
            need(z.comment.hex()==a['archive_comment_hex'],'archive comment')
            need(len(z.infolist())==len(a['members_in_original_order']),'archive member order/count')
            for i,r in zip(z.infolist(),a['members_in_original_order']):
                for k in ('filename','compress_type','create_system','create_version','extract_version','reserved','flag_bits','volume','internal_attr','external_attr','header_offset','CRC','compress_size','file_size'):need(getattr(i,k)==r[k],'ZIP '+k)
                need(list(i.date_time)==r['date_time'] and i.comment.hex()==r['comment_hex'] and i.extra.hex()==r['extra_hex'] and i.is_dir()==r['is_dir'],'ZIP remaining metadata')
                b=z.read(i);need(sha(b)==r['payload_SHA256'] and zlib.crc32(b)&0xffffffff==r['CRC'],'all payload SHA/CRC')
                need(b==Path(r['extracted']).read_bytes(),'all original extracted payload bytes including nested manifests')
    native=readj('NATIVE_ACTUAL_EXECUTION_COMPARISON.json')
    a=check(native['whole_stdout'],E);b=check(native['whole_original_expected'],E);err=check(native['whole_stderr'],E)
    need(a==b and err==b'','complete actual/expected output bytes and empty stderr')
    same(json.loads(a),native['whole_actual_literal_object'],'whole actual native object')
    same(json.loads(b),native['whole_original_expected_literal_object'],'whole expected native object')
    need(native['actual_process_exit_code']==0 and native['optimization_flag']==0 and native['asserts_enabled'] is True,'actual process exit versus optimization/asserts')
    need(native['normal_execution_count']==1 and native['optimized_execution_count']==0,'sole native normal route, no optimized duplicate')
    safety=readj('NATIVE_SAFETY_ROUTE.json')
    for r in safety['unchanged_copies']:need(check(r['original'])==check(r['copy']),'whole unchanged selected route/interfaces')
    raw=readj('RAW_PRIMARY_REFERENCE_BINDINGS.json')
    original=check(raw['handoff_original_by_reference']);same(json.loads(original),raw['whole_literal_raw_handoff'],'whole raw-only handoff')
    need(sha(original)=='e3b46063528a9c35332c72ba061b12c20801b632cb8a408da3b98d4597817c3d','exact raw-only handoff pin')
    for r in raw['referenced_original_raw_files']:check(r)
    need(raw['primary_GETs_by_this_lane']==0 and raw['raw_bodies_copied_into_this_packet'] is False,'raw-only reference custody')
    h=raw['whole_literal_raw_handoff'];same(json.loads(check(h['root_authority'])),h['whole_root_authority'],'whole actual root acquisition authority')
    need(h['new_GETs']==0 and h['old_raw_corpora_copied'] is False,'actual cache-only acquisition; no new GET assertion')
    for r in h['records']:
        if 'legacy_transport_metadata_container' in r:
            entries=[json.loads(line) for line in check(r['legacy_transport_metadata_container']).splitlines() if line.strip()]
            for selected in r['whole_original_selected_legacy_transport_objects_in_recorded_order']:
                need(any(literal(selected)==literal(v) for v in entries),'whole literal selected legacy transport object')
        if 'legacy_metadata_container' in r:
            same(json.loads(check(r['legacy_metadata_container'])),r['whole_original_legacy_metadata_object'],'whole original identity metadata; not fresh transport')
    ledger=readj('PRIMARY_READ_LEDGER.json')
    need(ledger['preexposure_initial_SHA256']==INITIAL and ledger['preexposure_own_results_SHA256']==RESULTS,'primary read after both own freezes')
    for r in ledger['items']:
        check(r['original_by_reference'])
        if r.get('own_reading_text'):check(r['own_reading_text'])
    controls()
    verdict=readj('CUSTOM_VERDICT.json')
    need(verdict['root_gate']=='CLOSED' and verdict['followup'] is None and verdict['canonical_AA_authority'] is False and verdict['publication_authority'] is None and verdict['root_adoption'] is None,'no promotion authority')
    if partial:
        need(not any((E/n).exists() for n in TERMS),'preseal partial only, no outer terminal yet')
    else:
        seal=readj('FINAL_SEAL.json');manifest=json.loads(check(seal['manifest'],E))
        need(manifest['exact_outer_terminal_names']==sorted(TERMS),'exact root terminal set only')
        need(seal['initial_SHA256']==INITIAL and seal['own_results_SHA256']==RESULTS,'final retains both exact evidence freezes')
        for n,r in manifest['payloads'].items():check(dict(r,path=n),E)
        af,ad=inventory(E);namespace(af,ad,set(manifest['payloads'])|TERMS,manifest['directories'])
        check(seal['whole_custom_verdict'],E);need(seal['root_gate']=='CLOSED' and seal['followup'] is None,'final closed gate and null followup')
    print(json.dumps({'mode':'partial-preseal-bindings' if partial else 'sealed-exact-namespace','custody_checks':COUNT,'native_scientific_executions_in_helper':0,'network_subprocess_project_imports_or_writes':False,'root_gate':'CLOSED'},sort_keys=True))

if __name__=='__main__':main()
