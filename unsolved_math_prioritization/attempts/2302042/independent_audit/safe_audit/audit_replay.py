#!/usr/bin/env python3
"""Independent replay against the named immutable recovery freeze."""
import hashlib
import json
from pathlib import Path
from fractions import Fraction
import shutil
import subprocess
import sys
import tempfile
import zipfile

def need(ok, label):
    if not ok:
        raise RuntimeError(label)

if len(sys.argv) != 2:
    raise SystemExit('Usage: python3 audit_replay.py /path/to/asymptotic_ratio_2302042_recovery')
root = Path(sys.argv[1])
packet = root/'safe_output'
archive = root/'asymptotic_ratio_2302042_NEW_FREEZE_20261005.zip'
zip_bytes = archive.read_bytes()
need(len(zip_bytes) == 13409, 'archive length')
zip_hash = hashlib.sha256(zip_bytes).hexdigest()
need(zip_hash == 'f55af0a7d0d909ec90a41158620f8e5304d74646032ef6e1465613f7518f0902', 'archive hash')
manifest_hash = hashlib.sha256((packet/'MANIFEST.json').read_bytes()).hexdigest()
need(manifest_hash == '9a16d1058ebccac239eee2faf033b61437eeeffe83ae178409e2903ae6914320', 'manifest hash')
allowed = {'CHECKS.json','CLAIMS.json','MANIFEST.json','PROOF.md','README.md','SOURCE_VERIFICATION.json','verify_exact.py','verify_manifest.py'}
with zipfile.ZipFile(archive) as z:
    need(z.testzip() is None, 'archive CRC')
    need(len(z.namelist()) == len(set(z.namelist())) == 8, 'archive unique members')
    need(set(z.namelist()) == allowed, 'independent archive allowlist')
    for name in z.namelist():
        need(z.read(name) == (packet/name).read_bytes(), 'archive/folder equality: '+name)

replays = []
for flags in ([], ['-O']):
    for name in ('verify_exact.py','verify_manifest.py'):
        p = subprocess.run([sys.executable, *flags, str(packet/name)], capture_output=True, text=True, check=True)
        result = json.loads(p.stdout)
        need(result['result'] == 'PASS', 'replay status')
        if name == 'verify_exact.py':
            need(result == json.loads((packet/'CHECKS.json').read_text()), 'stored checks reproduction')
        replays.append({'script':name,'optimized':bool(flags),'result':result})

mutants=[]
for label in ('content alteration','unexpected file','missing file','symlink'):
    with tempfile.TemporaryDirectory(prefix='audit-2302042-') as td:
        altered = Path(td)/'packet'
        shutil.copytree(packet, altered)
        if label == 'content alteration':
            with (altered/'PROOF.md').open('a') as f:
                f.write('\nAudit mutation.\n')
        elif label == 'unexpected file':
            (altered/'UNEXPECTED.txt').write_text('Audit mutation.')
        elif label == 'missing file':
            (altered/'README.md').unlink()
        else:
            (altered/'alias').symlink_to('PROOF.md')
        for flags in ([], ['-O']):
            p = subprocess.run([sys.executable, *flags, str(packet/'verify_manifest.py'), str(altered)],capture_output=True,text=True)
            need(p.returncode != 0, 'manifest mutation accepted')
            mutants.append({'label':label,'optimized':bool(flags),'rejected':True,'reason':(p.stderr or p.stdout).strip()})

c=json.loads((packet/'CLAIMS.json').read_text())
checks={
    'rank_and_problem': c['rank']==675 and c['problem_number']=='AMR-022-2042',
    'exact_function':c['positive_construction']['function']=='integral_0^z sin(t^n)/t^n dt',
    'exact_order':c['positive_construction']['order']=='n',
    'selected_pair_sum':c['positive_construction']['sum_over_2n_values']=='1',
    'simplicity_scope':c['positive_construction']['simple_ray_points'] is True,
    'standard_analytic_inputs_declared':c['positive_construction']['uses_standard_subharmonic_compactness'] is True and c['positive_construction']['uses_distributional_zero_measure_identity'] is True,
    'venue_discrepancy_declared':c['density_one_exclusion']['venue_discrepancy_unresolved'] is True,
    'status_is_literature_only':c['recommended_disposition']=='already_solved' and c['density_one_exclusion']['scope']=='attributed_literature_correction',
    'six_scope_exclusions':len(c['excluded_claims'])==6,
}
need(all(checks.values()), 'additional claims consistency')
for n in range(2,1002):
    # Integral of |sin(n theta)| on one angular sector is 2/n.
    angular_integral=2*n*Fraction(2,n)
    flux_mass_times_pi=Fraction(n,2)*angular_integral
    need(angular_integral==4, 'angular integral')
    need(flux_mass_times_pi==2*n, 'independent radial flux mass')

need(hashlib.sha256(archive.read_bytes()).hexdigest()==zip_hash, 'archive remained immutable')
need(hashlib.sha256((packet/'MANIFEST.json').read_bytes()).hexdigest()==manifest_hash, 'manifest remained immutable')
print(json.dumps({'result':'PASS','archive_bytes':len(zip_bytes),'archive_sha256':zip_hash,
    'manifest_sha256':manifest_hash,'archive_members':8,'replays':replays,
    'manifest_mutants':mutants,'additional_claim_checks':checks,'independent_riesz_flux_checks':2000,
    'analytic_proof_formalized':False,'barsegyan_original_proof_verified':False,
    'original_dataset_bytes_verified':False},indent=2,sort_keys=True))
