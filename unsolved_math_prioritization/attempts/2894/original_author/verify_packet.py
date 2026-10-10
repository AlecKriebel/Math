#!/usr/bin/env python3
"""Fail-closed authored packet integrity checks, not a mathematical proof checker."""
import hashlib,json,stat,sys,zipfile
from pathlib import Path
EXPECTED={'README.md','REPORT.md','PROOF.md','status.json','sources.json','verification_metadata.json','research_log.json','verify_packet.py'}
def fail(message): raise ValueError(message)
def require(ok,message):
    if not ok: fail(message)
def pairs(xs):
    d={}
    for k,v in xs:
        require(k not in d,'Duplicate JSON key: '+k); d[k]=v
    return d
def read_json(p):
    require(p.is_file() and not p.is_symlink(),'Missing or symlink JSON: '+str(p))
    return json.loads(p.read_text(encoding='utf-8'),object_pairs_hook=pairs)
def sha(b): return hashlib.sha256(b).hexdigest()
def main():
    require(len(sys.argv) in (3,4),'Usage: verify_packet.py PACKET_DIR EXTERNAL_MANIFEST [ZIP]')
    root=Path(sys.argv[1]); require(root.is_dir() and not root.is_symlink(),'Invalid packet root')
    manifest=read_json(Path(sys.argv[2])); require(manifest['schema']=='authored-packet-v1','Invalid manifest schema')
    require(manifest['problem_id']==2894,'Manifest problem mismatch')
    members=manifest['files']; require(isinstance(members,list),'Invalid manifest inventory')
    names=[x['path'] for x in members]
    require(len(names)==len(set(names)) and set(names)==EXPECTED,'Manifest inventory mismatch')
    actual=set()
    for f in root.rglob('*'):
        require(not f.is_symlink(),'Symlink rejected: '+str(f))
        require(f.is_file(),'Unexpected non-file entry: '+str(f))
        actual.add(f.relative_to(root).as_posix())
    require(actual==EXPECTED,'Packet inventory mismatch')
    for item in members:
        b=(root/item['path']).read_bytes()
        require(type(item['bytes']) is int and item['bytes']==len(b),'Byte count mismatch: '+item['path'])
        require(item['sha256']==sha(b),'Digest mismatch: '+item['path'])
    s=read_json(root/'status.json')
    require(s['problem_id']==2894 and s['problem_number']=='KP-4.18','Problem identity mismatch')
    require(s['disposition']=='partially_solved','Combined disposition must preserve partial status')
    require(s['part_a']=='prior_affirmative_result_public_preprint_plus_published_reduction','Part (a) scope mismatch')
    require(s['part_b']=='unresolved_in_checked_current_primary_literature','Part (b) must remain unresolved')
    require(s['full_problem_solved'] is False and s['new_solution_claimed'] is False,'Unsupported solution claim')
    require(type(s['turns_used']) is int and s['turns_used']==1 and s['turn_limit']==5,'Turn count mismatch')
    m=read_json(root/'verification_metadata.json')
    require(m['primary_statement_match'] is True and m['exact_report_empty'] is True,'Gate/statement mismatch')
    require(m['prior_work_gate']=='passed_literature_triage_only','Gate classification mismatch')
    require(m['statement_sha256']=='8dd529ab545c33caebd35c7c2464b2991c0db6def26843951499b47a1c9a82dc','Statement digest mismatch')
    require(m['complete_record_report_pair_sha256']=='d3eff8f9d1374e5a0c43ee943e6db924980158282869ebd7c874bd0a243cc429','Pair digest mismatch')
    require(m['primary_statement_normalized_sha256']=='5b6dc6cf3470bbf99fe2f0e0ca9f7510460d53cd91d10498f91dbee99c6bf0df','Primary identity mismatch')
    expected_inputs={'catalog.json':(21735099,'891938878f1e395de77f6829d5d5d13cb5d5393f85efaa7941fb14bd3e3d7566'),'problems.json':(68931837,'04128381e42a5e312326d74adb0947ee02062ade70229e02d3060ac4ef9942cf'),'research_results.json':(80334822,'8da848d31c20eb4eecaa07702eced4724aa4a89f877c2a0774d9f3138389aa6b')}
    require(len(m['input_files'])==3,'Input inventory mismatch')
    require({x['logical_name'] for x in m['input_files']}==set(expected_inputs),'Input names mismatch')
    for x in m['input_files']:
        require((x['bytes'],x['sha256'])==expected_inputs[x['logical_name']] and x['match'] is True,'Input binding mismatch')
    source_list=read_json(root/'sources.json')['sources']
    require(len(source_list)==5 and {x['key'] for x in source_list}=={'K3','KNV','HU','KP','NNP'},'Source inventory mismatch')
    by_key={x['key']:x for x in source_list}
    for key,url,digest in [('HU','https://arxiv.org/pdf/2602.05003v1','83e2b04b9ef499601b72ddfd4efca6841b469bce262452e8ec85aff77a84b800'),('KNV','https://arxiv.org/pdf/2405.06637v2','afd0a973619a871ca6043984891f82f0185ebefb4e4cae0002c03b1a4c654e83'),('KP','https://arxiv.org/pdf/2604.27635v2','7847135916536ec12d52d1490ffa0d7394d72bd7c0d3264bba1cf974789a276f')]:
        require(by_key[key]['url']==url and by_key[key]['sha256']==digest,'Source identity mismatch: '+key)
    require('preprint' in by_key['HU']['manuscript_status'].lower(),'HU publication status mismatch')
    require('Published:' in by_key['KNV']['manuscript_status'],'KNV publication status mismatch')
    log=read_json(root/'research_log.json'); require(len(log['approaches'])==1 and log['approaches'][0]['new_math_attempt'] is False,'Approach scope mismatch')
    zip_checked=False
    if len(sys.argv)==4:
        zp=Path(sys.argv[3]); require(zp.is_file() and not zp.is_symlink(),'Invalid ZIP')
        zb=zp.read_bytes(); require(len(zb)==manifest['zip']['bytes'] and sha(zb)==manifest['zip']['sha256'],'ZIP binding mismatch')
        with zipfile.ZipFile(zp) as z:
            entries=z.infolist(); zn=[i.filename for i in entries]
            require(len(zn)==len(set(zn)) and set(zn)==EXPECTED,'ZIP inventory mismatch')
            for i in entries:
                require(not i.is_dir() and not stat.S_ISLNK(i.external_attr>>16),'ZIP link/directory rejected')
                require(z.read(i.filename)==(root/i.filename).read_bytes(),'ZIP payload mismatch')
        zip_checked=True
    print(json.dumps({'result':'pass','problem_id':2894,'files_verified':len(EXPECTED),'zip_verified':zip_checked,'optimized':not __debug__,'mathematical_theorems_verified_by_code':False},sort_keys=True))
if __name__=='__main__':
    try: main()
    except Exception as e:
        print(json.dumps({'result':'fail','error':str(e)},sort_keys=True),file=sys.stderr); sys.exit(1)
