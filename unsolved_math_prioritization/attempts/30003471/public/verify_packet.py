#!/usr/bin/env python3
"""Read-only verifier with explicit exceptions in normal/-O/-OO modes."""
import argparse
import hashlib
import json
import math
import pathlib
import runpy
import shutil
import tempfile

class VerificationError(Exception):
    pass

def require(condition,message):
    if not condition:raise VerificationError(message)

def unique_object(pairs):
    out={}
    for k,v in pairs:
        if k in out:raise VerificationError('duplicate JSON key: '+k)
        out[k]=v
    return out

def reject_constant(value):
    raise VerificationError('nonfinite JSON constant: '+value)

def load_json_bytes(data):
    try:
        return json.loads(data.decode('utf-8'),object_pairs_hook=unique_object,parse_constant=reject_constant)
    except (UnicodeDecodeError,json.JSONDecodeError) as e:
        raise VerificationError('malformed JSON') from e

def sha(data):return hashlib.sha256(data).hexdigest()

EXPECTED_STATUS={"target_id":30003471,"problem_number":"OWR-15427-013","queue_rank":999,"date":"2026-10-08","dimension":3,"convex":True,"full_dimensional":True,"fixed_correspondence":True,"original_target":"one_corresponding_weak_inequality","candidate_strengthening":"weak_dominance_implies_full_normal_gram_equality","status":"complete_author_candidate_pending_independent_audit","substantive_approaches":1,"maximum_approaches":5,"independent_audit_passed":False,"accepted_solution":False,"formal_verification":False,"novelty_claim":False,"candidate_journal_accepted":False,"uses_wxy_singular_index":False,"smooth_corner_diffeomorphism_assumed":False,"source_free":True,"source_pdfs_included":False,"remote_writes":False,"numeric_controls_prove_analytic_theorem":False}
FILES={'README.md','PROOF.md','SOURCE_STATUS.md','RESEARCH_LEDGER.md','STATUS.json','SOURCE_METADATA.json','controls.py','CONTROL_RESULTS.json','verify_packet.py'}

def validate_status(status):
    require(type(status) is dict,'status must be object')
    require(status.keys()==EXPECTED_STATUS.keys(),'status schema')
    for k,v in EXPECTED_STATUS.items():
        require(type(status[k]) is type(v) and status[k]==v,'false/unsupported status claim: '+k)

def verify(root,pin):
    require(type(pin) is str and len(pin)==64 and all(c in '0123456789abcdef' for c in pin),'external manifest SHA-256 required')
    entries=list(root.iterdir())
    require({x.name for x in entries}==FILES|{'MANIFEST.json'},'inventory differs')
    for x in entries:require(x.is_file() and not x.is_symlink(),'nonregular or symlink packet entry')
    manifest_bytes=(root/'MANIFEST.json').read_bytes()
    require(sha(manifest_bytes)==pin,'external manifest pin mismatch')
    m=load_json_bytes(manifest_bytes)
    require(type(m) is dict and set(m)=={'schema','files'} and m['schema']==1,'manifest schema')
    require(type(m['files']) is dict and set(m['files'])==FILES,'manifest file schema')
    for name,expected in m['files'].items():
        require(type(expected) is dict and set(expected)=={'bytes','sha256'},'entry schema')
        b=(root/name).read_bytes()
        require(type(expected['bytes']) is int and len(b)==expected['bytes'],'byte count mismatch '+name)
        require(sha(b)==expected['sha256'],'hash mismatch '+name)
    validate_status(load_json_bytes((root/'STATUS.json').read_bytes()))
    sm=load_json_bytes((root/'SOURCE_METADATA.json').read_bytes())
    require(type(sm) is dict and set(sm)=={'sources','corpora','retrieval_not_peer_review'},'source metadata schema')
    require(sm['retrieval_not_peer_review'] is True,'source-status inflation')
    require(len(sm['sources'])==9 and len(sm['corpora'])==2,'source counts')
    for s in sm['sources']:
        require(s.get('included_in_packet') is False,'source inclusion forbidden')
        require(type(s.get('bytes')) is int and s['bytes']>0,'source byte count')
        require(type(s.get('sha256')) is str and len(s['sha256'])==64,'source hash')
        require(s.get('url','').startswith('https://'),'public URL required')
    for s in sm['corpora']:require(s.get('contents_included') is False,'dataset contents forbidden')
    result=runpy.run_path(str(root/'controls.py'))['run']()
    expected=load_json_bytes((root/'CONTROL_RESULTS.json').read_bytes())
    require(result==expected,'finite diagnostic replay differs')
    return {'packet':'pass','files':len(FILES),'manifest_sha256':pin,'finite_controls':result['total'],'mathematical_acceptance':False}

def self_test(root,pin):
    rejected=[]
    def rejection(label,f):
        try:f()
        except VerificationError:rejected.append(label)
        else:raise VerificationError('negative control was accepted: '+label)
    rejection('malformed_json',lambda:load_json_bytes(b'{'))
    rejection('duplicate_json',lambda:load_json_bytes(b'{"a":1,"a":2}'))
    rejection('nonfinite_json',lambda:load_json_bytes(b'{"a":NaN}'))
    for field,value in [('independent_audit_passed',True),('accepted_solution',True),('formal_verification',True),('novelty_claim',True),('candidate_journal_accepted',True),('dimension',4),('substantive_approaches',5),('source_pdfs_included',True),('smooth_corner_diffeomorphism_assumed',True),('target_id',True)]:
        changed=dict(EXPECTED_STATUS);changed[field]=value
        rejection('false_claim_'+field,lambda c=changed:validate_status(c))
    def copy_case(label,mutator):
        with tempfile.TemporaryDirectory(prefix='dihedral_negative_') as temp:
            copy=pathlib.Path(temp)/'packet';shutil.copytree(root,copy)
            mutator(copy)
            rejection(label,lambda:verify(copy,pin))
    copy_case('modified_proof',lambda p:(p/'PROOF.md').write_bytes((p/'PROOF.md').read_bytes()+b'\nchanged\n'))
    copy_case('missing_proof',lambda p:(p/'PROOF.md').unlink())
    copy_case('extra_source_pdf',lambda p:(p/'source.pdf').write_bytes(b'%PDF forbidden'))
    copy_case('corrupt_manifest',lambda p:(p/'MANIFEST.json').write_bytes(b'{'))
    def replace_status(p):
        s=dict(EXPECTED_STATUS);s['accepted_solution']=True
        (p/'STATUS.json').write_text(json.dumps(s))
        m=load_json_bytes((p/'MANIFEST.json').read_bytes())
        b=(p/'STATUS.json').read_bytes();m['files']['STATUS.json']={'bytes':len(b),'sha256':sha(b)}
        (p/'MANIFEST.json').write_text(json.dumps(m))
    copy_case('forged_status_and_manifest',replace_status)
    def link(p):
        (p/'STATUS.json').unlink();(p/'STATUS.json').symlink_to(root/'STATUS.json')
    copy_case('symlink_replacement',link)
    with tempfile.TemporaryDirectory(prefix='dihedral_readonly_') as temp:
        copy=pathlib.Path(temp)/'packet';shutil.copytree(root,copy)
        before={x.name:sha(x.read_bytes()) for x in copy.iterdir()}
        for x in copy.iterdir():x.chmod(0o444)
        copy.chmod(0o555)
        try:
            relocated=verify(copy,pin)
            after={x.name:sha(x.read_bytes()) for x in copy.iterdir()}
            require(before==after,'verifier modified readonly copy')
        finally:
            copy.chmod(0o755)
            for x in copy.iterdir():x.chmod(0o644)
    return {'negative_controls_rejected':len(rejected),'labels':rejected,'readonly_relocation':'pass','packet_writes':False}

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--manifest-sha256',required=True)
    parser.add_argument('--self-test',action='store_true')
    args=parser.parse_args()
    root=pathlib.Path(__file__).resolve().parent
    out=verify(root,args.manifest_sha256)
    if args.self_test:out['self_test']=self_test(root,args.manifest_sha256)
    print(json.dumps(out,sort_keys=True))

if __name__=='__main__':
    main()
