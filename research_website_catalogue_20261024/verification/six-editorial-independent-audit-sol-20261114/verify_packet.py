"""Read-only closure of this editorial audit; no campaign or existing verifier execution."""
from pathlib import Path
import hashlib
import json

A=Path(__file__).resolve().parent
def require(x,m):
    if not x:raise RuntimeError(m)
def read(p):return json.loads(p.read_bytes())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def check(e,base=None):
    p=Path(e['path']);p=base/p if base and not p.is_absolute() else p
    require(p.is_file() and not p.is_symlink(),'missing/nonregular '+str(p))
    require(p.stat().st_size==e['bytes'] and sha(p)==e['sha256'],'file changed '+str(p))
def main():
    seal=read(A/'SEAL.json');manifest=read(A/'MANIFEST.json')
    require(sha(A/'MANIFEST.json')==seal['manifest_sha256'],'audit manifest seal')
    for e in manifest['files']:check(e,A)
    require({str(p.relative_to(A)) for p in A.rglob('*') if p.is_file()}==
            {e['path'] for e in manifest['files']}|{'MANIFEST.json','SEAL.json'},'owned inventory')
    for e in read(A/'PROTECTED_INPUTS.json')['files']:check(e)
    for e in read(A/'AUTHORITY_EXTRA_INPUTS.json')['files']:check(e)
    require((A/'CHECKS.json').read_bytes()==(A/'CHECKS_OPTIMIZED.json').read_bytes(),'normal/optimized outputs')
    results=read(A/'CHECKS.json');verdicts=read(A/'VERDICTS.json')
    require(len(results['records'])==len(verdicts['results'])==6,'all six accounted')
    require(results['whole_literal_custom_verdicts_verified']==18,'all literal family verdicts')
    require(results['scope_omission_falsifiers_rejected']==18
            and results['native_authority_fidelity_falsifiers_rejected']==24,'bounded falsifier counts')
    require(seal['completion_percent']==verdicts['completion_percent']==100,'audit incomplete')
    require(not verdicts['publication_authority'] and verdicts['root_full_copy_and_unique_prose_adoption_required'],
            'publication/root-adoption boundary')
    require('self-audit' in next(x for x in verdicts['results'] if x['record_id']=='23539734')['qualification'],
            '110 independence disclosure')
    print(json.dumps({'status':'PASS_READ_ONLY_SIX_EDITORIAL_AUDIT_CLOSURE','audited_records':6,
                      'protected_original_files':len(read(A/'PROTECTED_INPUTS.json')['files']),
                      'literal_verdict_inputs':18,'owned_manifested_files':len(manifest['files']),
                      'seal_sha256':sha(A/'SEAL.json'),'file_writes':False,'existing_programs_executed':False,
                      'publication_authority':False,'root_full_reading_pending':True},sort_keys=True))
if __name__=='__main__':main()
