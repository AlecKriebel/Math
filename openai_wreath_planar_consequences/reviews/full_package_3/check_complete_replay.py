import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from flint import arb, ctx

ctx.prec = 192
review = Path(__file__).resolve().parent
program = review.parents[1]
package = review / 'extracted'
output = program / 'receipts' / 'clean_reproduction_revised'
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
receipt_path = output / 'REPRODUCTION_RECEIPT.json'
receipt = json.loads(receipt_path.read_text())
assert receipt['status'] == 'PASS_ALL_AUTHORED_COMPUTATIONS'
assert not receipt['quick'] and receipt['pdf_requested'] and receipt['pdf_build_and_text_verified']
assert receipt['package_identity_sha256'] == '45e264fe2ae99c093f2b8a02082e8b9af14cd3602fb176d39f73be474005d0c7'
assert receipt['manifest_verified'] and receipt['python'] == '3.12.14' and receipt['python_flint'] == '0.9.0'
labels = ['fixed_constants', 'wreath_orientation', 'exact_lattice', 'scalar_bounds',
          'validated_integrals', 'secondary_bernstein', 'publication_pdf']
assert [r['label'] for r in receipt['checks']] == labels
records = []
for check in receipt['checks']:
    label = check['label']
    assert check['returncode'] == 0
    for kind in ['stdout', 'stderr']:
        assert sha(output / f'{label}.{kind}.txt') == check[f'{kind}_sha256']
    if label != 'publication_pdf':
        assert sha(output / f'{label}.receipt.json') == check['receipt_sha256']
    records.append({'label': label, 'returncode': 0, 'all_saved_output_hashes_match': True,
                    'receipt_sha256': check.get('receipt_sha256')})

integral = json.loads((output / 'validated_integrals.receipt.json').read_text())
assert integral['status'] == integral['full_finite_gates'] == 'pass'
assert integral['precision_bits'] == 160
assert integral['script_sha256'] == sha(package / 'target_b/independent_validated_integrals.py') == '3c6546b00a821621b87c024d69280ae4075629d32b2b7fb0e021408613698379'
assert integral['coverage'] == {'finite_nodes': 51, 'matrix_signs': 2, 'residual_pairs': 102,
                                'half_gap_intervals': 84, 'Bernstein_inequalities': 2436}
facts = json.loads((package / 'publication/support/data/planar_certificate_tables.json').read_text())
nodes = [r[0] for r in facts['tables']['coefficients']['rows']]
assert len(nodes) == 51
assert {(r['i'], r['m']) for r in integral['residuals']} == {(i, n) for i in (1,2) for n in nodes}
assert len(integral['residuals']) == 102
for row in integral['residuals']:
    for kind in ['c','d']:
        val = arb(row[kind])
        assert val.is_finite() and val < arb('1e-9')
assert len(integral['Bernstein_intervals']) == 84
for row in integral['Bernstein_intervals']:
    assert arb(row['minimum']).is_finite() and arb(row['minimum']) > arb(row['threshold'])
assert len(integral['cross_certificates']) == 2
for row in integral['cross_certificates']:
    assert arb(row['defect']) < arb('.001')
    assert arb(row['WU']) < arb('3.54')
    assert arb(row['inverse_upper']) < 32
    assert arb(row['cross_upper']) < arb('3.7')
assert arb(integral['low_exterior_norm']) < arb('.09')

secondary = json.loads((output / 'secondary_bernstein.receipt.json').read_text())
assert secondary['status'] == 'pass_all_finite_bernstein_grouped_claims'
assert secondary['implementation_sha256'] == sha(package / 'reproducibility/checks/standalone_arb_bernstein.py')
assert secondary['authored_data_json_sha256'] == sha(package / 'publication/support/data/planar_certificate_tables.json')
assert len(secondary['checks']) == 84
count = 0
for row in secondary['checks']:
    assert len(row['all_29_bernstein_enclosures']) == 29
    for val in row['all_29_bernstein_enclosures']:
        enclosure = arb(val)
        assert enclosure.is_finite() and enclosure > arb(row['claimed_group_lower'])
        count += 1
assert count == 2436

scalar = json.loads((output / 'scalar_bounds.receipt.json').read_text())
assert scalar['status'] == 'pass' and scalar['source_sha256'] == sha(package / 'target_b/independent_scalar_checks.py')
assert arb(scalar['exact_list_error']) < arb('.00003')
assert arb(scalar['tail_second_derivative_bound']) < arb('.006')
assert min(arb(v) for v in scalar['midpoint_barriers']) > arb('.68')
assert arb(scalar['quadrature_error_bound']) < arb('1e-22')

pdf = receipt['checks'][-1]
assert pdf['compiler'] == 'Tectonic 0.16.9' and pdf['normalized_all_page_text_matches']
assert pdf['packaged_pdf_sha256'] == sha(package / 'publication/preprint.pdf') == 'e4ffb02321fd0a826395aadb038a10e28995db2fefde21c57a54c8ff9ae7083c'
assert pdf['rebuilt_pdf_sha256'] == sha(output / 'pdf/preprint.pdf')
old = (output / 'publication_original_text.txt').read_text()
new = (output / 'publication_rebuilt_text.txt').read_text()
assert len(old.split('\f')) == len(new.split('\f')) == 9
for a,b in zip(old.split('\f')[:-1], new.split('\f')[:-1]):
    assert re.sub(r'\s+', ' ', a).strip() == re.sub(r'\s+', ' ', b).strip()

result = {'utc': datetime.now(timezone.utc).isoformat(), 'status': 'PASS_ACTUAL_COMPLETE_REVISED_RECEIPTS',
          'source_receipt_sha256': sha(receipt_path), 'source_finished_utc': receipt['finished_utc'],
          'package_identity_sha256': receipt['package_identity_sha256'], 'all_seven_saved_output_hash_sets_match': True,
          'checks': records, 'integral_script_sha256': integral['script_sha256'],
          'integral_coverage': integral['coverage'], 'all_102_residual_balls_strictly_below_claim': True,
          'all_84_interval_minimum_balls_strictly_above_claim': True,
          'secondary_all_2436_enclosure_balls_strictly_above_group_claim': True,
          'secondary_script_sha256': secondary['implementation_sha256'],
          'all_eight_pages_normalized_text_match_individually': True,
          'packaged_pdf_sha256': pdf['packaged_pdf_sha256'], 'rebuilt_pdf_sha256': pdf['rebuilt_pdf_sha256'],
          'coverage_limits': receipt['limitations']}
(review / 'COMPLETE_REPLAY_INSPECTION.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps({k:v for k,v in result.items() if k not in ['checks','coverage_limits']},indent=2))
