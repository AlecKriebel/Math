#!/usr/bin/python3
"""Bounded independently authored source and coefficient-specialization controls."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, itertools, json, subprocess, sys, urllib.request
from fractions import Fraction
import sympy as s

ROOT = Path(__file__).resolve().parent
INPUT = json.loads((ROOT / 'priority_input.json').read_text())
def stamp(): return datetime.now(timezone.utc).isoformat()
def digest(b): return hashlib.sha256(b).hexdigest()
checks = []
def require(label, condition):
    checks.append({'label': label, 'pass': bool(condition)})
    if not condition: raise AssertionError(label)

sources = []
for key in ['primary_pdf_url', 'primary_abs_url', 'publisher_url']:
    url = INPUT[key]
    started = stamp()
    request = urllib.request.Request(url, headers={'User-Agent': 'Independent-mathematical-priority-audit/1.0'})
    with urllib.request.urlopen(request, timeout=45) as response:
        body = response.read()
        metadata = {'url': url, 'resolved_url': response.geturl(), 'started_at_utc': started,
                    'ended_at_utc': stamp(), 'status': response.status,
                    'content_type': response.headers.get('Content-Type'),
                    'bytes': len(body), 'sha256': digest(body)}
    if key == 'primary_pdf_url':
        extractor = '/opt/homebrew/bin/pdftotext'
        extraction = subprocess.run([extractor, '-layout', '-', '-'], input=body, capture_output=True, check=True)
        pages = extraction.stdout.decode('utf-8').split('\f')
        if not pages[-1].strip(): pages.pop()
        require('Versioned primary has 59 physical pages', len(pages) == 59)
        required_markers = {7: ['Definition 1.8', 'dim S'], 8: ['Lemma 1.12'],
                            14: ['Proposition 1.27', 'Euler'], 21: ['Definition 2.22'],
                            23: ['Theorem 2.31', 'codim'], 43: ['Definition 5.5'],
                            44: ['Theorem 5.10', 'analogous'],
                            45: ['Definition 5.12'], 46: ['Theorem 5.13']}
        for page, markers in required_markers.items():
            for marker in markers:
                require('Primary page %d marker %s' % (page, marker), marker in pages[page-1])
        definition_plain = ''.join(pages[44].split()).replace('⩾', '≥')
        require('Definition 5.12 includes l >= 0, not strictly positive l', 'l≥0' in definition_plain)
        require('Introduction explains global Laurent version', 'Laurent' in pages[1] and 'global' in pages[1])
        metadata['extractor'] = extractor
        metadata['extractor_sha256'] = digest(Path(extractor).read_bytes())
        metadata['extractor_stderr_sha256'] = digest(extraction.stderr)
        metadata['physical_pages'] = len(pages)
        metadata['selected_page_text_sha256'] = {str(p): digest(pages[p-1].encode())
            for p in INPUT['primary_pages_personally_read_before_controls']}
        # Pages and full primary binary are deliberately kept in memory only.
    else:
        decoded = body.decode('utf-8', errors='replace')
        if key == 'primary_abs_url':
            require('arXiv metadata identifies 31 July 2010 v3', '31 Jul 2010' in decoded and 'v3' in decoded)
            require('arXiv metadata identifies 2008 first submission', '28 Oct 2008' in decoded)
        else:
            require('Publisher DOI is the exact cited article', 's00454-010-9242-7' in decoded)
            require('Publisher records 6 February 2010 publication', '2010-02-06' in decoded or '06 February 2010' in decoded)
    sources.append(metadata)

def positive_compositions(total, count):
    if count == 0:
        return [()] if total == 0 else []
    if total < count: return []
    if count == 1: return [(total,)] if total > 0 else []
    return [(a,) + tail for a in range(1, total-count+2)
            for tail in positive_compositions(total-a, count-1)]
composition_rows = []
for d in INPUT['positive_composition_dimensions']:
    counts = {j: len(positive_compositions(j+1, d)) for j in range(d+1)}
    require('dimension %d full-face coefficient d' % d, counts[d] == d)
    require('dimension %d facet coefficient 1' % d, counts[d-1] == 1)
    require('dimension %d lower faces absent' % d, all(counts[j] == 0 for j in range(d-1)))
    composition_rows.append({'dimension': d, 'counts_by_face_dimension': counts})

univariate_rows = []
for degree in INPUT['univariate_degrees']:
    coeffs = s.symbols('c0:%d' % (degree+1))
    y = s.symbols('y')
    discriminant = s.Poly(s.discriminant(sum(coeffs[a]*y**a for a in range(degree+1)), y), *coeffs)
    support = [exponent for exponent, coefficient in discriminant.terms()]
    labels = 0
    for bits in itertools.product([False, True], repeat=degree-1):
        selected = [0] + [a+1 for a, present in enumerate(bits) if present] + [degree]
        w = [a*a if a in selected else 10*degree*degree for a in range(degree+1)]
        secondary = [0]*(degree+1)
        for left, right in zip(selected[:-1], selected[1:]):
            secondary[left] += right-left
            secondary[right] += right-left
        secondary[0] -= 1
        secondary[-1] -= 1
        predicted = tuple(secondary)
        values = [(sum(wi*zi for wi, zi in zip(w, exponent)), exponent) for exponent in support]
        minimum = min(value for value, exponent in values)
        minimizers = [exponent for value, exponent in values if value == minimum]
        require('degree %d selected %s exact discriminant vertex' % (degree, selected), minimizers == [predicted])
        labels += 1
    univariate_rows.append({'degree': degree, 'ordinary_discriminant_terms': len(support),
                            'all_regular_triangulation_labels_checked': labels})

# The 2x2x2 Cayley discriminant is derived from det(M0+t M1), with all eight
# coefficients algebraically independent. It is not read from an old checker.
c = s.symbols('c0:8')
t = s.symbols('t')
matrix0 = s.Matrix([[c[0], c[1]], [c[2], c[3]]])
matrix1 = s.Matrix([[c[4], c[5]], [c[6], c[7]]])
cube_discriminant = s.Poly(s.discriminant((matrix0+t*matrix1).det(), t), *c)
x = s.symbols('x0:4')
constants = [[s.Rational(v) for v in row] for row in INPUT['cube_column_constants']]
for row in constants:
    for value in row: require('generic constants have nonzero entries', value != 0)
for i, j in itertools.combinations(range(4), 2):
    require('all 2x2 column minors nonzero at %d,%d' % (i,j),
            constants[0][i]*constants[1][j]-constants[0][j]*constants[1][i] != 0)
substituted = s.Poly(cube_discriminant.as_expr().subs({c[4*i+a]: constants[i][a]*x[a]
               for i in range(2) for a in range(4)}), *x)
projected_support = {tuple(exponent[a]+exponent[a+4] for a in range(4))
                     for exponent, coefficient in cube_discriminant.terms()}
actual_support = {exponent for exponent, coefficient in substituted.terms()}
require('generic column specialization preserves every projected exponent', actual_support == projected_support)
bad = s.expand(cube_discriminant.as_expr().subs({c[4*i+a]: x[a]
               for i in range(2) for a in range(4)}))
require('negative control: nongeneric equal equations annihilate discriminant', bad == 0)
cube_row = {'universal_terms': len(cube_discriminant.terms()),
            'projected_exponents': sorted(projected_support),
            'specialized_terms': [[list(exponent), str(coefficient)] for exponent, coefficient in substituted.terms()],
            'nongeneric_all_ones_result': str(bad)}

result = {'schema': 'independent-Esterov-priority-controls-v1', 'completed_at_utc': stamp(),
          'python': sys.version, 'sympy': s.__version__, 'sources': sources,
          'checks': checks, 'all_checks_passed': all(row['pass'] for row in checks),
          'positive_compositions': composition_rows, 'univariate_boundary': univariate_rows,
          'generic_and_nongeneric_column_specialization': cube_row,
          'universal_proof': False, 'ROOT_acceptance_authority': False}
(ROOT/'CONTROL_RESULTS.json').write_text(json.dumps(result, indent=2)+'\n')
print(json.dumps({'all_checks_passed': result['all_checks_passed'], 'check_count': len(checks),
                  'univariate_labels': sum(row['all_regular_triangulation_labels_checked'] for row in univariate_rows),
                  'cube_generic_projection_equal': actual_support == projected_support,
                  'cube_nongeneric_discriminant': str(bad),
                  'pdf_sha256': sources[0]['sha256'], 'pdf_bytes': sources[0]['bytes']}))
