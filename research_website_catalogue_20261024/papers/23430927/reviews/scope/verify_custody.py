"""Pure offline read-only custody, not mathematical verification.

Use python -I -B. No project/scientific imports, network, subprocess or writes.
Default requires exact sealed files/directories. --preseal is partial bindings only.
"""
from pathlib import Path
import hashlib
import json
import stat
import sys

E=Path(__file__).resolve().parent
INITIAL='022d8e7753acaef7b4d81e291217816a5f9c4758e806a38be5954df7384ca259'
RESULTS='085c42ec87ce99732cdb69b6926ecedb2f7a0e7c83558a068d1af9a3d02c17be'
CORE='0f285e35daa206f53aa931946c4bcc6c5b01ae6b4b59a231a861b0a6fe11d104'
GO='6e0d5e3049549f7b85f70c5d290d882948ce13f8e56bf382ef0eba903c372502'
HANDOFF='d611b86b851385d9f05523b0acb126b335f935ae6fdce0fb0dd001c4bd674236'
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
    b=p.read_bytes();need(type(row['bytes']) is int and len(b)==row['bytes'],'whole length '+str(p))
    need(sha(b)==row['SHA256'],'whole SHA256 '+str(p));return b

def literal(v):
    if isinstance(v,dict):return ('dict',tuple((k,literal(x)) for k,x in v.items()))
    if isinstance(v,list):return ('list',tuple(literal(x) for x in v))
    return (type(v).__name__,v)

def same(a,b,why):need(literal(a)==literal(b),why)

def inventory(root):
    files=set();dirs=set()
    for p in root.rglob('*'):
        mode=p.lstat().st_mode;r=p.relative_to(root).as_posix()
        need(stat.S_ISDIR(mode) or stat.S_ISREG(mode),'symlink/special entry '+r)
        (dirs if stat.S_ISDIR(mode) else files).add(r)
    return files,dirs

def namespace(af,ad,ef,ed):
    need(af==set(ef),'exact ordinary file namespace');need(ad==set(ed),'exact directory namespace')

def reject(fn,why):
    try:fn()
    except ValueError:need(True,why)
    else:need(False,'negative accepted '+why)

def controls():
    reject(lambda:same(1,True,'type'),'integer/bool')
    reject(lambda:same({'a':None,'b':[]},{'b':[],'a':None},'order'),'key order')
    reject(lambda:same({'a':None},{},'absence'),'null/absent')
    reject(lambda:namespace({'x','nested/MANIFEST.json'},{'nested'},{'x'},set()),'nested terminal-name file')
    reject(lambda:namespace({'x'},{'empty'},{'x'},set()),'empty directory')
    reject(lambda:need(sha(b'raw')==sha(b'raW'),'buffer'),'one-byte body mutation')

def main():
    need(sys.argv[1:] in ([],['--preseal']),'arguments');partial=bool(sys.argv[1:])
    b=(E/'INITIAL_SEAL.json').read_bytes();need(sha(b)==INITIAL,'immutable INITIAL');i=json.loads(b)
    need(len(i['payloads'])==15,'all initial payloads')
    for n,r in i['payloads'].items():check(dict(r,path=n),E)
    b=(E/'OWN_PROOF_CONTROL_SEAL.json').read_bytes();need(sha(b)==RESULTS,'immutable actual own RESULTS');r=json.loads(b)
    m=json.loads(check(r['manifest'],E))
    for n,pin in m['files'].items():check(dict(pin,path=n),E)
    p=readj('PROTECTED_INPUTS.json');need(p['protected_paths']==719,'complete source plus qualified core')
    s=p['source'];need(len(s['files'])==701 and len(s['directories'])==119,'source full counts')
    for row in s['files']:check(row)
    af,ad=inventory(Path(s['path']));namespace(af,ad,[r['relative_path'] for r in s['files']],s['directories'])
    core=check(p['qualified_core_contract']);need(sha(core)==CORE,'actual qualified core authority')
    c=json.loads(core);same(c,p['whole_literal_core_contract'],'whole literal core authority')
    need(len(c['files'])==18 and c['original17_plus_sole_authorized405b_checkpoint'] is True and c['all18_original_unchanged_claim'] is False,'17 original plus sole405b, not18 original')
    same(c['files'],p['core_files'],'whole actual core path bindings')
    for row in c['files']:check(row)
    protocol=readj('SOURCE_PROTOCOL_BINDINGS.json')
    for name,row in protocol.items():
        if name.endswith('.json'):check(row['original_by_reference'])
    apis=protocol['whole_native_API_objects_in_original_role_order']
    need([a['role'] for a in apis]==['record','latest','versions-page001','files'],'original API role/list order')
    for a in apis:same(json.loads(check(a['original_by_reference'])),a['whole_literal_object'],'whole raw API ordered/types/values')
    ready=json.loads(check(protocol['SOURCE_READY.json']['original_by_reference']))
    need(ready['recursive_archive_container_count']==5 and ready['whole_regular_payload_occurrences']==636,'unchanged recorded archive counts, not a replay')
    tex=Path(ready['controlling_TeX']['extracted_path']).read_bytes()
    need(len(tex)==26569 and len(tex.splitlines())==160 and sha(tex)=='43115a1b12108340e4e3b28eb315e6d7d79ff3a8a208286abf3528c537ea6587','current outer controlling body')
    need(len(ready['all_TeX_candidates'])==5,'five historical/current occurrences')
    for t in ready['all_TeX_candidates']:need(Path(t['extracted_path']).read_bytes()==tex,'all five actual TeX byte identities')
    hb=(E/'RAW_PRIMARY_HANDOFF_01.json').read_bytes();need(sha(hb)==HANDOFF,'immutable raw-only handoff');h=json.loads(hb)
    go=check(h['root_authority']);need(sha(go)==GO,'actual root acquisition GO');same(json.loads(go),h['whole_literal_root_authority'],'whole literal GO')
    need(h['new_GETs']==0 and h['old_raw_corpora_copied'] is False and len(h['records'])==9,'cache-only raw references')
    for row in h['records']:
        b=check(row['whole_original_raw_body']);entries=json.loads(check(row['available_legacy_transport_container']));actual=row['whole_selected_legacy_transport_object']
        need(any(literal(x)==literal(actual) for x in entries),'whole selected available legacy transport object')
        need(len(b)==actual['bytes'] and sha(b)==actual['sha256'] and row['fresh_GET'] is False,'raw body against literal legacy record, no fresh GET')
    for row in h['legacy_access_limits']:
        entries=json.loads(check(row['available_legacy_transport_container']))
        need(any(literal(x)==literal(row['whole_original_recorded_failure_object']) for x in entries),'whole legacy failure object')
        need(row['whole_failed_response_body'] is None and row['current_access_claim'] is None and row['fresh_GET'] is False,'no fabricated failure body or current access claim')
    ledger=readj('PRIMARY_READ_LEDGER.json');need(ledger['initial_SHA256']==INITIAL and ledger['own_results_SHA256']==RESULTS,'reading after actual evidence freezes')
    for row in ledger['items']:check(row['original_by_reference']);check(row['own_reading_text'])
    controls();v=readj('CUSTOM_VERDICT.json')
    need(v['root_gate']=='CLOSED' and v['followup'] is None and v['canonical_AA_authority'] is False and v['publication_authority'] is None and v['root_adoption'] is None,'no publication or adoption authority')
    need(v['independent_evidence']['native_or_own_scientific_programmes_executed']==[],'no scientific execution in scope')
    if partial:need(not any((E/n).exists() for n in TERMS),'partial preseal only; no outer terminals yet')
    else:
        seal=readj('FINAL_SEAL.json');m=json.loads(check(seal['manifest'],E))
        need(m['exact_outer_terminal_names']==sorted(TERMS),'exact outer terminals, no basename/future exclusions')
        need(seal['initial_SHA256']==INITIAL and seal['own_results_SHA256']==RESULTS,'final exact evidence freezes')
        for n,pin in m['payloads'].items():check(dict(pin,path=n),E)
        af,ad=inventory(E);namespace(af,ad,set(m['payloads'])|TERMS,m['directories'])
        check(seal['whole_custom_verdict'],E);need(seal['root_gate']=='CLOSED' and seal['followup'] is None,'final closed gate/null followup')
    print(json.dumps({'mode':'partial-preseal-bindings' if partial else 'sealed-exact-namespace','custody_checks':COUNT,'scientific_or_native_execution':False,'network_subprocess_project_imports_or_writes':False,'root_gate':'CLOSED'},sort_keys=True))

if __name__=='__main__':main()
