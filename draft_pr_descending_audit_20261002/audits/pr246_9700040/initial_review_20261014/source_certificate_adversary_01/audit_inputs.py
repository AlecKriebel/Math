#!/usr/bin/env python3
"""Read-only original/native and historical-manifest audit; output authored receipts."""
from pathlib import Path
import base64, datetime, hashlib, json

HERE=Path(__file__).resolve().parent
CASE=HERE.parent
ATTEMPT=CASE/'submitted/unsolved_math_prioritization/attempts/9700040'

def stamp(): return datetime.datetime.now(datetime.timezone.utc).isoformat()
def pin(p):
    b=p.read_bytes()
    return {'bytes':len(b),'sha1':hashlib.sha1(b).hexdigest(),
            'git_blob_sha1':hashlib.sha1(f'blob {len(b)}\0'.encode()+b).hexdigest(),
            'sha256':hashlib.sha256(b).hexdigest()}

def main():
    intake=json.loads((CASE/'INTAKE.json').read_text())
    rows=[]
    for item in intake['original_source_files']:
        p=CASE/'submitted'/item['native_path']; h=pin(p)
        transport=[]
        for rp in sorted((CASE/'transport_receipts/intake_01').glob('*stdout.json')):
            d=json.loads(rp.read_text())
            if d.get('sha')!=item['native_blob'] or d.get('encoding')!='base64': continue
            body=base64.b64decode(d['content']);transport.append({
                'receipt_path':str(rp.relative_to(CASE)),
                'receipt_sha256':pin(rp)['sha256'],
                'declared_size_matches':d['size']==len(body),
                'decoded_matches_submitted':body==p.read_bytes(),
                'decoded_git_blob_matches':hashlib.sha1(f'blob {len(body)}\0'.encode()+body).hexdigest()==d['sha']})
        checks={'size_matches_intake':h['bytes']==item['bytes'],
                'sha256_matches_intake':h['sha256']==item['sha256'],
                'native_git_blob_matches_intake':h['git_blob_sha1']==item['native_blob'],
                'has_exactly_one_transport_body':len(transport)==1,
                'all_transport_checks':all(all(v for k,v in t.items() if k not in ('receipt_path','receipt_sha256')) for t in transport)}
        rows.append({'native_path':item['native_path'],**h,'checks':checks,'transport':transport})
    manifests=[]
    for name,base in [('FROZEN_MANIFEST.json',ATTEMPT),('PUBLICATION_MANIFEST.json',ATTEMPT),
                      ('independent_review/REVIEW_MANIFEST.json',ATTEMPT/'independent_review')]:
        path=ATTEMPT/name;d=json.loads(path.read_text()); entries=[]
        for item in d['files']:
            target=base/item['path'];h=pin(target)
            entries.append({'path':str(target.relative_to(ATTEMPT)),**h,
                            'size_matches':h['bytes']==item['bytes'],
                            'sha256_matches':h['sha256']==item['sha256']})
        manifests.append({'path':name,**pin(path),'declared_entry_count':len(d['files']),
                          'all_entries_match':all(x['size_matches'] and x['sha256_matches'] for x in entries),'entries':entries})
    original=set(x['native_path'].split('attempts/9700040/',1)[1] for x in rows)
    actual=set(str(p.relative_to(ATTEMPT)) for p in ATTEMPT.rglob('*') if p.is_file())
    extra=sorted(actual-original)
    transport_pins=[{'path':str(p.relative_to(CASE)),**pin(p)} for p in sorted((CASE/'transport_receipts').rglob('*')) if p.is_file()]
    old_verify=json.loads((ATTEMPT/'independent_review/FROZEN_VERIFICATION.json').read_text())
    old_review=json.loads((ATTEMPT/'independent_review/REVIEW_MANIFEST.json').read_text())
    old_compare=json.loads((ATTEMPT/'independent_review/AUTHOR_COMPARISON.json').read_text())
    sources=json.loads((ATTEMPT/'source_manifest.json').read_text())['sources']
    old_input_checks={
        'frozen_verification_author_manifest_matches':old_verify['author_manifest_sha256']==pin(ATTEMPT/'FROZEN_MANIFEST.json')['sha256'],
        'frozen_verification_all_author_hashes_match':all(pin(ATTEMPT/x['file'])['sha256']==x['sha256'] for x in old_verify['author']),
        'frozen_verification_all_source_hashes_match_pins':all(any(x['file']==s['reading_filename'] and x['sha256']==s['sha256'] for s in sources) for x in old_verify['sources']),
        'review_manifest_author_proof_matches':old_review['author_proof_sha256']==pin(ATTEMPT/'PROOF.md')['sha256'],
        'review_manifest_author_manifest_matches':old_review['author_manifest_sha256']==pin(ATTEMPT/'FROZEN_MANIFEST.json')['sha256'],
        'author_comparison_evaluator_matches':old_compare['author_evaluator_sha256']==pin(ATTEMPT/'stationary_law.py')['sha256']}
    receipt={'utc':stamp(),'method':'Python hashlib over all bytes; Git blob SHA1 includes blob header; base64 provider bodies independently decoded',
             'native_head':intake['head'],'intake_pin':pin(CASE/'INTAKE.json'),
             'original_count':len(rows),'all_original_checks_pass':all(all(r['checks'].values()) for r in rows),
             'originals':rows,'historical_manifests':manifests,
             'extra_files_in_submitted':extra,'all_historical_manifest_entries_pass':all(m['all_entries_match'] for m in manifests),
             'inherited_review_input_crosslinks':old_input_checks,
             'transport_receipt_pins':transport_pins,
             'limits':'Verifies saved native transport bodies and submitted bytes, not a new live remote content fetch; parent provided live head revalidation.'}
    (HERE/'INPUT_VERIFICATION.json').write_text(json.dumps(receipt,indent=2)+'\n')
    assert receipt['all_original_checks_pass'] and receipt['all_historical_manifest_entries_pass'] and all(old_input_checks.values())
    print(json.dumps({'status':'PASS','original_files':len(rows),'historical_manifest_entries':sum(m['declared_entry_count'] for m in manifests),'extra_files':extra,'receipt':'INPUT_VERIFICATION.json'}))

if __name__=='__main__':main()
