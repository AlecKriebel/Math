from pathlib import Path
import datetime, hashlib, json, subprocess, urllib.request

F = Path(__file__).resolve().parent
URL = 'https://publications.mfo.de/bitstream/handle/mfo/2988/OWR_2007_02.pdf?isAllowed=y&sequence=1'
req = urllib.request.Request(URL, headers={'User-Agent': 'Independent mathematics source audit'})
with urllib.request.urlopen(req, timeout=45) as response:
    b = response.read(10_000_001)
    resolved = response.url
    content_type = response.headers.get('Content-Type')
assert b.startswith(b'%PDF-') and len(b) <= 10_000_000
assert len(b) == 472577
assert hashlib.sha256(b).hexdigest() == 'b1001aadcbbf3a8c35707b4b58cddbce46132e7ecb7601869e676d5f702f805d'
p = subprocess.run(['/opt/homebrew/bin/pdftotext', '-f', '24', '-l', '24', '-', '-'],
                   input=b, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
txt = p.stdout.decode('utf-8')
start = txt.index('Isomorphism of Complete Local Noetherian Rings and Strong')
end = txt.index('Recovering Fields from Galois Groups', start)
contribution = ' '.join(txt[start:end].split())
checks = {
    'exact_local_noetherian_scope': 'complete local noetherian rings' in contribution,
    'all_natural_orders': 'isomorphic for every natural number' in contribution,
    'unrestricted_negative_answer': 'negative answer to Macintyre' in contribution and 'general case' in contribution,
    'gabber_credit': 'Ofer Gabber' in contribution,
    'positive_algebraic_residue_field': 'residue field is algebraic over its prime' in contribution,
    'zero_equicharacteristic': 'equicharacteristic 0' in contribution,
    'positive_equicharacteristic': 'equicharacteristic p > 0' in contribution,
    'zero_residue_transcendence_degree_one': 'transcendence degree 1' in contribution,
    'positive_residue_infinite_transcendence_degree': 'infinite transcendence degree' in contribution,
    'non_domain_examples': 'These examples are not integral domains' in contribution,
    'historical_domain_question': 'problem remains open in that case' in contribution,
    'contribution_includes_references': 'References' in contribution and 'Die strenge Approximationseigenschaft' in contribution
}
assert all(checks.values()), checks
result = {'schema': 'pr53-independent-fresh-primary-scope/v1',
          'checked_at': datetime.datetime.now(datetime.timezone.utc).isoformat(),
          'url': URL, 'resolved_url': resolved, 'content_type': content_type,
          'pdf_bytes': len(b), 'pdf_sha256': hashlib.sha256(b).hexdigest(),
          'selected_pdf_page': 24, 'printed_page': 106, 'scope_checks': checks,
          'page_text_sha256': hashlib.sha256(p.stdout).hexdigest(),
          'pdftotext_argv': p.args, 'pdftotext_exit_code': p.returncode,
          'full_pdf_saved': False, 'copyrighted_page_text_saved': False,
          'nested_child_pid_or_interval_claimed': False,
          'counterexample_construction_reproduced': False,
          'mathematical_counterexample_test_count': 0}
(F / 'FRESH_PRIMARY_SCOPE.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps(result, indent=2))
