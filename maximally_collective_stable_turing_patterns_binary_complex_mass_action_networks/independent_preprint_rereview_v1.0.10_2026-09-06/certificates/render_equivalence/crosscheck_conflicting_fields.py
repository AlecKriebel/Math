#!/usr/bin/env python3
"""Peer-check the mixed A/U field finding without rerunning the full suite."""
import importlib.util
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import sympy as sp
from check_render_equivalence import SOURCE, load_certificates, parse_tables, check_certificate_tables

HERE = Path(__file__).resolve().parent
CERTIFICATES = HERE.parent
MUTANT = CERTIFICATES / 'conflicting_coefficient_fields.json'
MUTANT_TABLE = CERTIFICATES / 'conflicting_coefficient_fields_table.tex'
sys.path.insert(0, str(SOURCE / 'independent_verifier'))


def load(name, relative):
    spec = importlib.util.spec_from_file_location(name, SOURCE / relative)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main():
    original_certificates = load_certificates(lambda p: (SOURCE / p).read_text())
    mutant = json.loads(MUTANT.read_text())
    spatial = mutant['modulus']['spatial']
    row = spatial['terms'][1]
    if row != {'powers': [6, 1, 0], 'coefficient_in_A_ascending': ['8281/24300'],
               'coefficient_in_U_ascending': ['1']}:
        raise ValueError('Unexpected mutant')

    mode = load('peer_mode', 'independent_verifier/frontier_verify_mode_certificates.py')
    exposition = load('peer_exposition', 'independent_verifier/frontier_verify_exposition_identities.py')
    generator = load('peer_generator', 'computation/generate_tables.py')
    mode.verify(MUTANT)
    exposition.verify_modulus_source_polynomials(pareto_certificate=MUTANT)

    regenerated = generator.cert_table(
        '84-term equilibrium-scaled spatial certificate', spatial['variables'],
        spatial['terms'], spatial['term_count'], ('x', 'z', 's'), True)
    if not MUTANT_TABLE.read_text().endswith(regenerated + '\n'):
        raise ValueError('Saved mutant table does not match the real generator')
    tables = parse_tables(MUTANT_TABLE.read_text(), False)
    try:
        check_certificate_tables(original_certificates, tables)
    except ValueError as error:
        independent_rejection = str(error)
    else:
        raise ValueError('Independent exact coefficient checker accepted wrong table')

    # Reconstruct E84 from real and imaginary parts of the displayed factors.
    # For lambda=x+i*y and z=y^2, the imaginary parts below are divided by y.
    x, z, s, A = sp.symbols('x z s A')
    t = 1 + s
    u = x + 2 + sp.Rational(23, 63) * t
    v = x + 5 + sp.Rational(1, 7) * t
    w = x + 4 + sp.Rational(16, 45) * t
    f_real = u*v*w - (u+v+w)*z - 4*u - 4*v + w
    f_imag_over_y = u*v + u*w + v*w - z - 7
    g_real = w*(4*u+v) - 5*z - 36
    g_imag_over_y = 4*u + v + 5*w
    exact_E84 = sp.expand(
        sp.Rational(91, 90)**2 * (1+A*x+z/3)
        * (f_real**2+z*f_imag_over_y**2)
        - (g_real**2+z*g_imag_over_y**2))
    printed = sum(
        sum(sp.Rational(c.numerator, c.denominator)*A**degree
            for degree, c in coefficients.items())
        * x**powers[0]*z**powers[1]*s**powers[2]
        for powers, coefficients, _ in tables[3])
    difference = sp.factor(printed-exact_E84)
    expected_difference = sp.Rational(16019, 24300)*x**6*z
    if sp.expand(difference-expected_difference) != 0:
        raise ValueError(f'Unexpected exact discrepancy: {difference}')
    original = sum(
        sum(sp.Rational(c)*A**degree for degree, c in enumerate(term['coefficient_in_A_ascending']))
        * x**term['powers'][0]*z**term['powers'][1]*s**term['powers'][2]
        for term in original_certificates[3]['terms'])
    if sp.expand(original-exact_E84) != 0:
        raise ValueError('Shipped coefficient identity is wrong')

    manifest = dict(line.split(maxsplit=1)[::-1] for line in
                    (SOURCE / 'release/sha256_manifest.txt').read_text().splitlines())
    hash_checks = []
    for relative, altered in [
        ('independent_verifier/pareto_all_m_certificate.json', MUTANT),
        ('data/certificate_tables.tex', MUTANT_TABLE),
    ]:
        expected = manifest['./'+relative]
        shipped_hash = hashlib.sha256((SOURCE / relative).read_bytes()).hexdigest()
        mutant_hash = hashlib.sha256(altered.read_bytes()).hexdigest()
        if expected != shipped_hash or expected == mutant_hash:
            raise ValueError('Unexpected manifest integrity result')
        hash_checks.append({'path': relative, 'shipped_matches_manifest': True,
                            'mutant_matches_manifest': False})

    result = {
        'timestamp_utc': datetime.now(timezone.utc).isoformat(),
        'verdict': 'CONFIRMED',
        'direct_mode_reader': 'ACCEPTED (independently rerun)',
        'source_polynomial_reader': 'ACCEPTED (independently rerun)',
        'real_generator_matches_mutant_table': True,
        'independent_parser_rejection': independent_rejection,
        'independently_derived_printed_minus_actual_E84': str(difference),
        'shipped_A_coefficients_equal_actual_E84': True,
        'unchanged_release_manifest_detects_mutants': hash_checks,
        'scope': 'No full suite or PDF rebuild rerun. Their supplied logs inspected separately.'
    }
    (HERE / 'CROSSREVIEW_RESULT.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
