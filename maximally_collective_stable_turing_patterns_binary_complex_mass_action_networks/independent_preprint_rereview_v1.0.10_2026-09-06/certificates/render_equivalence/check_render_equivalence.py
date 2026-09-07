#!/usr/bin/env python3
"""Independently parse shipped coefficient TeX with exact rational arithmetic.

Does not import any manuscript/verifier/generator code. Old ambiguous notation
is parsed with its intended coefficient-times-variable meaning; new notation
has its numerator variable explicitly before the division sign.
"""
import hashlib
import json
import re
import subprocess
from datetime import datetime, timezone
from fractions import Fraction
from pathlib import Path

HERE = Path(__file__).resolve().parent
AUDIT = HERE.parents[1]
SOURCE = AUDIT / 'source_snapshot'
PROJECT = AUDIT.parent
REPO = PROJECT.parent
OLD = '94d5177485b9680be8b77f13448abf1f923963e8'
NEW = '953c836a12b9d9d474521feb4a96e218c1155203'


def historic(commit, relative):
    return subprocess.check_output(
        ['git', 'show', f'{commit}:{PROJECT.name}/{relative}'], cwd=REPO
    ).decode()


def load_certificates(read):
    unit = json.loads(read('independent_verifier/improved_modulus_certificate.json'))
    scaled = json.loads(read('independent_verifier/pareto_all_m_certificate.json'))
    return [unit['homogeneous'], unit['improved_mode'],
            scaled['modulus']['homogeneous'], scaled['modulus']['spatial']]


def parse_polynomial(expr, old, expected_variable):
    """Return {degree: Fraction}; grammar accepts only the shipped exact forms."""
    result = {}
    for term in expr.split('+'):
        # Pure rational constants.
        if re.fullmatch(r'\d+(?:/\d+)?', term):
            degree, coefficient = 0, Fraction(term)
        else:
            # Unambiguous numerator monomial, optionally divided by integer.
            match = re.fullmatch(r'(\d*)([AU])(?:\^\{(\d+)\})?(?:/(\d+))?', term)
            if match:
                numerator, variable, exponent, denominator = match.groups()
                if variable != expected_variable:
                    raise ValueError(f'Unexpected polynomial variable: {variable}')
                degree = int(exponent or '1')
                coefficient = Fraction(int(numerator or '1'), int(denominator or '1'))
            elif old:
                # Explicit intended interpretation of the superseded a/bA form.
                match = re.fullmatch(r'(\d+)/(\d+)([AU])(?:\^\{(\d+)\})?', term)
                if not match:
                    raise ValueError(f'Unrecognized legacy term: {term}')
                numerator, denominator, variable, exponent = match.groups()
                if variable != expected_variable:
                    raise ValueError(f'Unexpected legacy polynomial variable: {variable}')
                degree = int(exponent or '1')
                coefficient = Fraction(int(numerator), int(denominator))
            else:
                raise ValueError(f'Unrecognized or ambiguous current term: {term}')
        if degree in result:
            raise ValueError(f'Duplicate coefficient degree in {expr}')
        result[degree] = coefficient
    return {k: v for k, v in result.items() if v}


def parse_tables(tex, old):
    tables = []
    for index, block in enumerate(tex.split(r'\begin{longtable}')[1:]):
        expected_variable = [None, None, 'U', 'A'][index]
        rows = []
        for line in block.splitlines():
            match = re.fullmatch(r'((?:\d+ & )+)\$(.*?)\$\\\\', line)
            if match:
                powers = tuple(int(x) for x in match.group(1).split(' & ')[:-1])
                expression = match.group(2)
                rows.append((powers, parse_polynomial(expression, old, expected_variable), expression))
        tables.append(rows)
    return tables


def check_certificate_tables(certificates, tables):
    if len(certificates) != len(tables):
        raise ValueError('Unexpected table count')
    for cert, table in zip(certificates, tables):
        if cert['term_count'] != len(table) or len(cert['terms']) != len(table):
            raise ValueError('Unexpected row count')
        for term, (powers, coefficients, expression) in zip(cert['terms'], table):
            if tuple(term['powers']) != powers:
                raise ValueError('Mismatched exponent order')
            if 'coefficient' in term:
                expected = {0: Fraction(term['coefficient'])}
            else:
                key = ('coefficient_in_U_ascending' if 'coefficient_in_U_ascending' in term
                       else 'coefficient_in_A_ascending')
                expected = {k: Fraction(c) for k, c in enumerate(term[key]) if Fraction(c)}
            if coefficients != expected:
                raise ValueError(f'Coefficient mismatch at {powers}: {expression}')


def main():
    old_certs = load_certificates(lambda p: historic(OLD, p))
    new_certs = load_certificates(lambda p: (SOURCE / p).read_text())
    old_tex = historic(OLD, 'data/certificate_tables.tex')
    new_tex = (SOURCE / 'data/certificate_tables.tex').read_text()
    old_tables = parse_tables(old_tex, True)
    new_tables = parse_tables(new_tex, False)
    check_certificate_tables(old_certs, old_tables)
    check_certificate_tables(new_certs, new_tables)
    if old_certs != new_certs:
        raise ValueError('Exact certificate data changed between releases')
    changes = []
    for index, (old_table, new_table) in enumerate(zip(old_tables, new_tables)):
        for previous, current in zip(old_table, new_table):
            if previous[:2] != current[:2]:
                raise ValueError('Rendered coefficient semantics changed')
            if previous[2] != current[2]:
                changes.append({'table': index + 1, 'powers': list(current[0]),
                                'old': previous[2], 'new': current[2]})
    if len(changes) != 50:
        raise ValueError(f'Expected 50 rendering repairs, observed {len(changes)}')
    if re.search(r'\d+/\d+[AU]', new_tex):
        raise ValueError('Ambiguous fractional coefficient remains')
    controls = []
    for label, mutation in [
        ('old ambiguous notation', new_tex.replace('8281A/8100', '8281/8100A', 1)),
        ('wrong coefficient', new_tex.replace('8281A/8100', '8282A/8100', 1)),
        ('wrong polynomial variable', new_tex.replace('8281A/8100', '8281U/8100', 1)),
    ]:
        try:
            check_certificate_tables(new_certs, parse_tables(mutation, False))
        except ValueError as error:
            controls.append({'mutation': label, 'rejected': True, 'reason': str(error)})
        else:
            raise ValueError(f'Independent checker failed its negative control: {label}')
    copies = []
    for relative in ['data/certificate_tables.tex',
                     'public/repository/data/certificate_tables.tex',
                     'submission/arxiv/source/data/certificate_tables.tex',
                     'submission/biorxiv/source/data/certificate_tables.tex',
                     'submission/journal/source/data/certificate_tables.tex']:
        data = (SOURCE / relative).read_bytes()
        if data != new_tex.encode():
            raise ValueError(f'Export differs: {relative}')
        copies.append({'path': relative, 'sha256': hashlib.sha256(data).hexdigest()})
    result = {'utc': datetime.now(timezone.utc).isoformat(), 'old_commit': OLD,
              'new_commit': NEW, 'status': 'PASS',
              'mechanism': 'Independent restricted-grammar TeX parser and Fraction arithmetic; no project code imported',
              'table_row_counts': [len(t) for t in new_tables],
              'rows_checked_per_release': sum(len(t) for t in new_tables),
              'unchanged_exact_json_certificates': True,
              'independent_checker_negative_controls': controls,
              'semantics_preserving_rendering_changes': changes,
              'identical_current_export_copies': copies}
    (HERE / 'RESULTS.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({k: v for k, v in result.items()
                      if k not in ('semantics_preserving_rendering_changes',
                                   'identical_current_export_copies')}, indent=2))


if __name__ == '__main__':
    main()
