#!/usr/bin/env python3
"""Fresh input integrity and copied certificate reproduction; no input writes."""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys

HERE = Path(__file__).resolve().parent
AUDIT = HERE.parent
TMP = HERE / 'tmp' / 'copied_reproduction'

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def normalized(x):
    if isinstance(x, dict):
        return {k: normalized(v) for k, v in x.items()
                if k not in ('timestamp_UTC', 'timestamp_utc', 'timestamp', 'at')}
    if isinstance(x, list):
        return [normalized(v) for v in x]
    return x

def main():
    TMP.mkdir(parents=True, exist_ok=True)
    frozen = json.loads((AUDIT/'snapshot_manifest.json').read_text())
    originals = []
    for e in frozen['files']:
        p = AUDIT/e['snapshot_path']
        assert sha(p) == e['sha256'], p
        assert p.stat().st_size == e['size'], p
        originals.append({'file':e['snapshot_path'], 'sha256':sha(p)})
    specs = [
        ('reviewed_candidate/check_koszul.py', 'reviewed_candidate/check_results.json', 'stdout'),
        ('reviewed_candidate/independent_review/independent_checks.py',
         'reviewed_candidate/independent_review/independent_results.json', 'independent_results.json'),
        ('priority/equivalent_methods/check_prior_translation.py',
         'priority/equivalent_methods/translation_checks.json', 'translation_checks.json'),
        ('exact_reproduction_family/ideal_certificate/check_certificates.py',
         'exact_reproduction_family/ideal_certificate/CHECK_RESULTS.json', 'CHECK_RESULTS.json'),
        ('exact_reproduction_family/ideal_certificate/gorenstein_falsifier/verify_identities.py',
         'exact_reproduction_family/ideal_certificate/gorenstein_falsifier/verification_result.json',
         'verification_result.json'),
        ('exact_reproduction_family/independent_quotients.py',
         'exact_reproduction_family/independent_quotient_results.json',
         'independent_quotient_results.json'),
    ]
    reproduced=[]
    for i, (script, saved, output) in enumerate(specs):
        source = AUDIT/script
        own = TMP/str(i)/source.name
        own.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, own)
        proc = subprocess.run([sys.executable, str(own)], check=True,
                              text=True, capture_output=True)
        (own.parent/'stdout.txt').write_text(proc.stdout)
        (own.parent/'stderr.txt').write_text(proc.stderr)
        new = json.loads(proc.stdout if output == 'stdout' else
                         (own.parent/output).read_text())
        old = json.loads((AUDIT/saved).read_text())
        assert normalized(new) == normalized(old), script
        assert sha(source) == sha(own), script
        reproduced.append({'script':script, 'sha256':sha(source),
                           'saved':saved, 'exact_mathematical_payload_equal':True,
                           'stderr':proc.stderr})
        print('PASS copied reproduction:', script, flush=True)
    report={'generated_at':datetime.now(timezone.utc).isoformat(),
            'original_manifest_entries_checked':len(originals),
            'immutable_originals':originals, 'reproductions':reproduced,
            'status':'PASS', 'scope':'Exact saved examples and certificates; no proof by finite testing.'}
    (HERE/'reproduction_results.json').write_text(json.dumps(report,indent=2)+'\n')

if __name__ == '__main__':
    main()
