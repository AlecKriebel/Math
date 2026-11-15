"""Approved-source-only integration controls; stdout only, no writer access."""
from pathlib import Path
import importlib.util
import json


def run(root):
    spec = importlib.util.spec_from_file_location('own_frozen_contract', root / 'independent_contract.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    contract = module.load_contract(root)
    baseline = json.loads((root / 'INDEPENDENT_BASELINE.json').read_bytes())
    site = Path(baseline['public_root'])
    available = {Path(r['path']).relative_to(site).as_posix() for r in baseline['public_files']}
    for record in contract['records']:
        pub = record['whole_original_publication']; prefix = 'research/' + pub['slug'] + '/'
        available |= {prefix + 'index.html', prefix + 'assets/' + pub['pdf_filename'],
                      prefix + 'assets/' + pub['supplement_filename'], prefix + 'assets/citation.bib'}
    results = []
    for record in contract['records']:
        pub = record['whole_original_publication']
        text = module.read_blob(root, record['source_paths']['approved_HTML']).decode()
        text = text.replace('<main>', '<a href="#main">Skip to main content</a><nav><a href="/">Home</a><a href="/research/">Research</a></nav><main id="main">')
        if record['record_id'] == '23439582':
            text = text.replace(contract['allowed_main_change_121']['old'], contract['allowed_main_change_121']['new'])
        positive = module.check_page(root, record, text.encode(), available)
        inner = module.main_inner(text)
        altered = inner.replace(pub['abstract'][:80], '[truncated abstract]', 1)
        module.need(inner != altered, 'source body control must be nonvacuous')
        faults = [
            ('truncated_actual_main_body', text.replace(inner, altered, 1)),
            ('hidden_main', text.replace('<main id="main">', '<main id="main" hidden>')),
            ('outer_template', text.replace('<body>', '<body><template>').replace('</body>', '</template></body>')),
            ('wrong_scholarly_DOI', text.replace('name="citation_doi" content="' + pub['doi'] + '"', 'name="citation_doi" content="10.5281/zenodo.0"')),
            ('created_date_substitution', text.replace('name="citation_publication_date" content="2026/10/17"', 'name="citation_publication_date" content="2026/11/15"')),
        ]
        if record['record_id'] == '23439582':
            faults.append(('lost_literal_underscores', text.replace('C_*', 'C*').replace('H_*', 'H*')))
        rejected = []
        for label, data in faults:
            try:
                module.check_page(root, record, data.encode(), available)
            except ValueError as error:
                rejected.append({'fault': label, 'literal_rejection': str(error)})
            else:
                raise ValueError('integration fault accepted: ' + label)
        results.append({'record_id': record['record_id'], 'authentic_source_derived_positive': positive,
                        'independent_faults_rejected': rejected})
    return {'literal_custom_status': 'APPROVED_SOURCE_DERIVED_POSITIVES_AND_DISTINCT_INTEGRATION_FAULTS_CONFIRMED_BEFORE_WRITER_EXPOSURE',
            'rows': results, 'writer_implementation_or_outputs_read': False,
            'science_replayed': False, 'fixtures_created_on_disk': False}


if __name__ == '__main__':
    print(json.dumps(run(Path(__file__).resolve().parent), indent=2))
