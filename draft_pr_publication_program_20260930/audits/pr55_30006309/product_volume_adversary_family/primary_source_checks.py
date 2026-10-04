"""Read selected primary sources transiently; retain hashes and predicates, no PDFs."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import re
import subprocess
import urllib.request

HERE = Path(__file__).resolve().parent

def main():
    specs = [
        ('OWR', 'https://ems.press/content/serial-article-files/51856'),
        ('SANO', 'https://arxiv.org/pdf/2302.09801v1'),
        ('OGUSU_SANO', 'https://arxiv.org/pdf/2302.09792v1'),
        ('GKZ', 'https://webhomes.maths.ed.ac.uk/~v1ranick/papers/gelkapzel.pdf')]
    receipts = []
    texts = {}
    for label, url in specs:
        start = datetime.now(timezone.utc).isoformat()
        with urllib.request.urlopen(url, timeout=30) as r:
            body = r.read()
            resolved = r.url
        p = subprocess.run(['pdftotext', '-layout', '-', '-'], input=body,
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        text = p.stdout.decode('utf-8')
        texts[label] = re.sub(r'\s+', ' ', text)
        receipts.append({'label': label, 'requested_url': url, 'resolved_url': resolved,
                         'started_utc': start, 'finished_utc': datetime.now(timezone.utc).isoformat(),
                         'bytes': len(body), 'sha256': hashlib.sha256(body).hexdigest(),
                         'extraction_argv': ['pdftotext', '-layout', '-', '-'],
                         'extraction_exit_code': p.returncode,
                         'extraction_stdout_bytes': len(p.stdout),
                         'extraction_stdout_sha256': hashlib.sha256(p.stdout).hexdigest(),
                         'extraction_stderr_bytes': len(p.stderr),
                         'extraction_stderr_sha256': hashlib.sha256(p.stderr).hexdigest(),
                         'retention': 'PDF and full extracted text held only in process memory, not copied into this packet.'})
    predicates = {
        'OWR_exact_combinatorial_reproof_question': 'combinatorial way?' in texts['OWR'],
        'OWR_Hurwitz_vectors_model': 'nηT,n' in texts['OWR'].replace(' ', ''),
        'Sano_smooth_very_ample_scope': 'smooth polarized variety with very ample line bundle' in texts['SANO'],
        'Sano_degree_at_least_two': 'greater than or equal to two' in texts['SANO'],
        'Sano_Theorem_1_4': 'Theorem 1.4.' in texts['SANO'],
        'Ogusu_Sano_surface_product_refinement': 'Proposition 3.5.' in texts['OGUSU_SANO'] and 'vertical regular triangulation' in texts['OGUSU_SANO'],
        'Ogusu_Sano_nonregular_remark': 'Proposition 3.5 still holds if' in texts['OGUSU_SANO'],
        'GKZ_massive_vertex_formula_present': 'D-equivalent' in texts['GKZ'] and 'massive' in texts['GKZ'],
        'GKZ_fan_refinement_present': 'normal fan of' in texts['GKZ'] and 'Minkowski summand' in texts['GKZ'],
        'GKZ_normal_cone_union_present': 'Proposition 3.7. The normal cone' in texts['GKZ'],
    }
    assert all(predicates.values()), predicates
    result = {'status': 'PASS_SELECTED_PRIMARY_SOURCE_PREDICATES', 'utc': datetime.now(timezone.utc).isoformat(),
              'receipts': receipts, 'predicates': predicates,
              'limits': 'These extraction predicates identify personally read source locations; they are not a formal verification of the sources\' proofs or a priority audit.'}
    (HERE / 'PRIMARY_SOURCE_RECEIPTS.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({'status': result['status'], 'source_count': len(receipts), 'predicates': len(predicates),
                      'no_primary_PDF_or_full_text_retained': True}, sort_keys=True))

if __name__ == '__main__':
    main()
