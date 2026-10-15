#!/usr/bin/env python3
"""Create/verify a nonrecursive public manifest; does not touch original inputs."""
from pathlib import Path
import datetime,hashlib,json,sys
HERE=Path(__file__).resolve().parent
CASE=HERE.parent
MANIFEST=HERE/'FINAL_AUDIT_MANIFEST.json'
def pin(p):
    b=p.read_bytes()
    return {'bytes':len(b),'sha1':hashlib.sha1(b).hexdigest(),
            'git_blob_sha1':hashlib.sha1(f'blob {len(b)}\0'.encode()+b).hexdigest(),
            'sha256':hashlib.sha256(b).hexdigest()}
def validate(path,expected):
    actual=pin(path)
    assert all(actual[k]==expected[k] for k in ('bytes','sha1','git_blob_sha1','sha256')),str(path)
def main():
    if '--verify' in sys.argv:
        m=json.loads(MANIFEST.read_text())
        for x in m['public_authored_artifacts']:validate(HERE/x['path'],x)
        for x in m['original_inputs']:validate(CASE/'submitted'/x['native_path'],x)
        for x in m['context_inputs']:validate(CASE/x['path'],x)
        assert set(x['path'] for x in m['public_authored_artifacts'])==set(str(p.relative_to(HERE)) for p in HERE.rglob('*') if p.is_file() and p!=MANIFEST)
        print(json.dumps({'status':'PASS','manifest_sha256':pin(MANIFEST)['sha256'],
                          'public_authored_count':len(m['public_authored_artifacts']),
                          'original_input_count':len(m['original_inputs'])}))
        return
    inputs=json.loads((HERE/'INPUT_VERIFICATION.json').read_text())
    controls=json.loads((HERE/'CONTROL_RECEIPTS.json').read_text())
    replays=json.loads((HERE/'ORIGINAL_REPLAY_RECEIPTS.json').read_text())
    sources=json.loads((HERE/'SOURCE_ACCESS_RECEIPTS.json').read_text())
    assert inputs['all_original_checks_pass'] and inputs['all_historical_manifest_entries_pass'] and all(inputs['inherited_review_input_crosslinks'].values())
    assert controls['status']=='PASS' and controls['exact_assertions']==99955
    assert all(r['matches_historical_stdout_byte_for_byte'] and r['returncode']==0 for r in replays['rows'])
    assert replays['historical_direct_coefficient_match_count']==42
    assert sum(x.get('matches_original_size_sha256',False) for x in sources['sources'])==6
    originals=[{'native_path':x['native_path'],**{k:x[k] for k in ('bytes','sha1','git_blob_sha1','sha256')}} for x in inputs['originals']]
    authored=[{'path':str(p.relative_to(HERE)),**pin(p)} for p in sorted(HERE.rglob('*')) if p.is_file() and p!=MANIFEST]
    context=[]
    for name in ('INTAKE.json','LIVE_REVALIDATION_20261015.json','CURRENT_AUDIT_STATE.json','root_source_reading/PRIMARY_RETRIEVAL.json'):
        p=CASE/name;context.append({'path':name,**pin(p)})
    m={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'problem_id':9700040,'source_code':'AMR-096-0040','PR':246,
       'native_head':'0b4db59eb5515f2d90d8b8df33b6b729b78b48f1',
       'audit_family':'independent exact primary-source scope and finite rational certificate adversary',
       'completion_percent_this_audit':100,
       'disposition':'PASS_SOURCE_SCOPE_AND_RATIONAL_CERTIFICATE_WITH_EXECUTABLE_LIMITS',
       'mandatory_mathematical_corrections':[],
       'qualifications':['Qualitative explicitness judgment is reasoned, not proposer acceptance.',
                         'Historical novelty and already-solved classification require a later distinct priority phase.',
                         'Exact fractions certify; display_only floats do not round outward.',
                         'Unchanged CLI has default integer-string limits; recursive enumeration and unbounded caches have runtime limits.'],
       'fresh_exact_assertions':controls['exact_assertions'],
       'historical_replay_assertions':[r['complete_json_stdout'].get('assertions',r['complete_json_stdout'].get('exact_assertions')) for r in replays['rows']],
       'historical_coefficient_matches':42,
       'all_original_native_bodies_and_historical_manifest_checks_pass':True,
       'all_six_primary_original_source_pins_match':True,
       'original_inputs':originals,'context_inputs':context,
       'public_authored_artifacts':authored,
       'source_objects':[{'key':x['key'],'url':x['requested_url'],'bytes':x['bytes'],'sha1':x['sha1'],'sha256':x['sha256'],'matches_original_source_pin':x.get('matches_original_size_sha256')} for x in sources['sources']],
       'exclusions':['This manifest cannot recursively include its own hash; verify its externally reported SHA256.',
                     'All whole third-party PDFs/HTML/text/provider responses and the entire root_source_reading/private_reading directory.',
                     'Unmodified original/native inputs are bound by hashes rather than duplicated in this authored folder.'],
       'mutation_scope':'Only this assigned source_certificate_adversary_01 directory was written; no Git/index/ref/checkouts/source/QUEUE/PR/publication/tracker mutations or outreach.'}
    MANIFEST.write_text(json.dumps(m,indent=2)+'\n')
    print(json.dumps({'status':'CREATED','manifest_sha256':pin(MANIFEST)['sha256'],'public_authored_count':len(authored),'original_input_count':len(originals)}))
if __name__=='__main__':main()
