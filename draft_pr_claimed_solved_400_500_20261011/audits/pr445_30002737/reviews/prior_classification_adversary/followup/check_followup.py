#!/usr/bin/env python3
"""Own follow-up receipts: immutable bindings, rational bridge, one direct replay."""
from pathlib import Path
from fractions import Fraction
import datetime
import hashlib
import json
import subprocess
import sys

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
REVIEW = HERE.parent
CASE = REVIEW.parents[1]
ROOT = CASE.parents[2]
EXPECTED = '027dc38ea76f1a4e69d8976a4845caefc4429e48b551afa7c327dc243b3dac20'
def need(test, msg):
    if not test:
        raise RuntimeError(msg)
def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()
def timestamp():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()
def main():
    old = json.loads((REVIEW/'PUBLIC_FILES.json').read_text())
    old_checks = []
    for rec in old['files']:
        path = REVIEW/rec['path']
        need(path.stat().st_size == rec['bytes'] and sha(path) == rec['sha256'],
             'old sealed review changed: '+rec['path'])
        old_checks.append(rec['path'])
    old_result = json.loads((REVIEW/'RESULT.json').read_text())
    need(old_result['unresolved_independently_certified_numerical_reproduction_gaps'] == 1,
         'original gap record changed')
    custody = json.loads((CASE/'SPIN_CERTIFICATE_ADVERSARY_CUSTODY.json').read_text())
    custody_checks = []
    for rec in custody['positive_files']:
        path = ROOT/rec['path']
        need(path.stat().st_size == rec['bytes'] and sha(path) == rec['sha256'],
             'adversary custody changed: '+rec['path'])
        custody_checks.append(rec['path'])
    producer = CASE/'reviews/spin_numerical_validation/certify_integral.py'
    need(sha(producer) == EXPECTED, 'controlling code hash mismatch')
    seal = json.loads((producer.parent/'SEAL.json').read_text())
    for name,digest in seal['immutable_files_sha256'].items():
        need(sha(producer.parent/name)==digest, 'producer pre-peer sealed file changed: '+name)
    adversary = json.loads((CASE/'reviews/spin_certificate_adversary/RESULT.json').read_text())
    need(adversary['controlling_code_sha256'] == EXPECTED, 'adversary code hash mismatch')
    need(adversary['disposition']=='ACCEPT_N13_FINITE_STRICT_UPPER_CERTIFICATE', 'adversary scope mismatch')
    certificate = json.loads((producer.parent/'certificate_N13_M65536.json').read_text())
    M,N,R = certificate['cells'],certificate['N'],int(certificate['scale'])
    U = int(certificate['sum_cell_log_upper_scaled'])
    L = int(certificate['log2_lower_scaled'])
    margin = M*N*L-U
    need((M,N,R)==(65536,13,2**100), 'wrong claimed finite certificate')
    need(margin>0 and margin==int(certificate['strict_integer_margin']), 'strict threshold mismatch')
    need(margin==int(adversary['strict_integer_margin']), 'adversary strict margin mismatch')
    need(margin==11969853181466710380769305597695012, 'root strict margin mismatch')
    # Exact bridge: lambda <= I13/2 < (log 2)/2 = log sqrt(2).
    upper_I = Fraction(U,M*N*R)
    lower_log2 = Fraction(L,R)
    need(upper_I<lower_log2, 'missing strict rational inequality')
    started = timestamp()
    argv = [sys.executable, str(producer), '--N','13','--cells','65536','--bits','100']
    cp = subprocess.run(argv,cwd='/tmp',capture_output=True,text=True)
    finished = timestamp()
    need(cp.returncode==0, 'direct replay failed')
    actual = json.loads(cp.stdout)
    excluded = {'elapsed_seconds','utc_completed','python'}
    need({k:v for k,v in actual.items() if k not in excluded} ==
         {k:v for k,v in certificate.items() if k not in excluded}, 'stable replay fields differ')
    inputs = [
        CASE/'FINAL_PRIORITY_DISPOSITION.md', CASE/'SPIN_CERTIFICATE_ADVERSARY_CUSTODY.json',
        producer, producer.parent/'REPORT.md',producer.parent/'RESULT.json',
        producer.parent/'PUBLIC_FILES.json',producer.parent/'SEAL.json',
        producer.parent/'certificate_N13_M65536.json',
        CASE/'reviews/spin_certificate_adversary/REPORT.md',
        CASE/'reviews/spin_certificate_adversary/RESULT.json',
        CASE/'reviews/spin_certificate_adversary/gram_crosscheck.py',
        CASE/'reviews/spin_certificate_adversary/gram_crosscheck_raw.json',
        CASE/'reviews/spin_certificate_adversary/ANALYTIC_OBLIGATIONS.md',
        CASE/'reviews/spin_certificate_adversary/EXECUTION_SUMMARY.json',
        CASE/'ROOT_SPIN_CERTIFICATE_REPLAY.json', REVIEW/'REPORT.md', REVIEW/'RESULT.json']
    records=[{'path':str(p.relative_to(ROOT)), 'bytes':p.stat().st_size,
              'sha256':sha(p)} for p in inputs]
    output = {
        'at_utc':finished, 'completion_percent':95,
        'old_positive_manifest_files_unchanged':old_checks,
        'old_numerical_gap_preserved':1,
        'custody_is_parent_produced_not_reviewer_seal':True,
        'custody_positive_file_hashes_matched':custody_checks,
        'input_bindings':records,
        'strict_rational_bridge':{'N':N,'M':M,'R':str(R),'U':str(U),'L':str(L),
            'margin':str(margin),'upper_I13':str(upper_I),
            'lower_log2':str(lower_log2),
            'upper_lyapunov_bound':str(upper_I/2),
            'source_threshold':'log(sqrt(2)) = (log(2))/2',
            'N12_certificate_used':False,
            'printed_table_decimal_error_claim_used':False},
        'direct_replay':{'argv':argv,'cwd':'/tmp','started_at_utc':started,
            'completed_at_utc':finished,'exit_code':cp.returncode,
            'stdout':cp.stdout,'stderr':cp.stderr,
            'code_sha256':EXPECTED,'stable_fields_match':True,
            'old_runner_executed':False},
        'classification_blockers':0, 'required_repairs':0,
        'remaining_target_numeric_gaps_for_classification':0,
        'transaction_operational_review_done':False}
    (HERE/'FOLLOWUP_CHECKS.json').write_text(json.dumps(output,indent=2)+'\n')
    print(json.dumps({'strict_margin':str(margin),'old_manifest_files_unchanged':len(old_checks),
         'custody_hashes_matched':len(custody_checks),'direct_replay_stable_fields_match':True,
         'classification_blockers':0,'at_utc':finished},indent=2))
if __name__=='__main__':
    main()
