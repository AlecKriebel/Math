#!/usr/bin/env python3
"""Recheck the pinned downloaded publication bytes without executing its code."""
import datetime as dt
import hashlib
import json
from pathlib import Path, PurePosixPath
import stat
import zipfile

D = Path(__file__).resolve().parent
A = D.parent
R = A.parents[1]


def require(value, reason):
    if not value: raise RuntimeError(reason)


def main():
    plan = json.loads((A / 'LEDGER_RECONCILIATION_PLAN.json').read_text())
    baseline = R / 'raw/pr1156/zenodo_23350364.json'
    require(hashlib.sha256(baseline.read_bytes()).hexdigest() == plan['baseline_provider_sha256'], 'Provider baseline changed')
    record = json.loads(baseline.read_text())
    require(record['id'] == 23350364 and record['conceptrecid'] == '23350363'
            and record['doi'] == '10.5281/zenodo.23350364'
            and record['conceptdoi'] == '10.5281/zenodo.23350363'
            and record['state'] == 'done' and record['submitted'] is True, 'Publication identity/state changed')
    require(record['metadata']['creators'] == [{'name': 'Ferudun, Alper', 'affiliation': 'Mercury Software GmbH'}], 'External authorship changed')
    checked = []
    for item in plan['existing_publication']['files']:
        body = (R / 'raw/pr1156' / ('payload_' + item['sha256'] + '.bin')).read_bytes()
        require(len(body) == item['size'] and hashlib.sha256(body).hexdigest() == item['sha256']
                and 'md5:' + hashlib.md5(body).hexdigest() == item['checksum'], 'Published payload changed')
        checked.append({k: item[k] for k in ['name', 'size', 'checksum', 'sha256']})
        if item['name'] != 'source.zip': continue
        with zipfile.ZipFile(R / 'raw/pr1156' / ('payload_' + item['sha256'] + '.bin')) as archive:
            names = archive.namelist()
            require(len(names) == len(set(names)) == 18 and archive.testzip() is None, 'Archive inventory or CRC failed')
            for info in archive.infolist():
                path = PurePosixPath(info.filename)
                require(not path.is_absolute() and '..' not in path.parts and '\\' not in info.filename
                        and not info.is_dir() and not stat.S_ISLNK(info.external_attr >> 16), 'Unsafe ZIP member')
            entries = json.loads(archive.read('source-archive-manifest.json'))['files']
            require(set(entries) == set(names) - {'source-archive-manifest.json'}, 'Manifest is not closed')
            for name, binding in entries.items():
                payload = archive.read(name)
                require(len(payload) == binding['bytes'] and hashlib.sha256(payload).hexdigest() == binding['sha256'], 'Archive manifest mismatch')
    primary = A / 'inverse_congruence_adversary/private/original_OWR_2017.pdf'
    primary_image = A / 'inverse_congruence_adversary/private/original_OWR_2017_page_13.png'
    result = {'checked_utc': dt.datetime.now(dt.timezone.utc).isoformat(),
              'public_record': 23350364, 'concept_record': 23350363, 'external_author': 'Alper Ferudun',
              'cached_provider_baseline_sha256': plan['baseline_provider_sha256'],
              'checked_payloads': checked, 'safe_unique_zip_members': 18, 'closed_manifest_payloads': 17,
              'primary_report_url': 'https://ems.press/content/serial-article-files/46715',
              'primary_pdf_sha256': hashlib.sha256(primary.read_bytes()).hexdigest(),
              'primary_page_13_image_sha256': hashlib.sha256(primary_image.read_bytes()).hexdigest(),
              'primary_visual_inspection': 'Printed page3083 / PDF page13, both distinct questions and the bound read directly. Fresh EMS web text independently agreed.',
              'full_public_math_text_read': ['main.tex', 'reproducibility/canonical_statement.md', 'reproducibility/complete_proof.md', 'source-provenance.json'],
              'scope_verdict': 'The row accurately credits the existing external result for separate Question2 in all orders, including singular cases and attained extrema. Exact ordinary-rank maxima equality is a direct corollary of the two rank-preserving constructions. Question1 maximum pointwise gap and a numeric formula for all p_n remain unresolved.',
              'priority_limit': 'This is content identity and attribution checking. Publication date and candidate metadata do not establish worldwide priority, chronology of public visibility, causal dependence or authorship transfer.',
              'freshness_limit': 'This script verifies downloaded evidence and its pins. It makes no new authenticated account, spreadsheet, PR, DOI-resolution or public-record live request.',
              'external_mutations': 0, 'public_code_executed': False}
    (D / 'PUBLICATION_BINDING_RECEIPT.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({k: result[k] for k in ['public_record', 'external_author', 'safe_unique_zip_members', 'closed_manifest_payloads', 'external_mutations']}))


if __name__ == '__main__': main()
