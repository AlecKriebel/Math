"""Build the explicit preprint support archive and matching Zenodo upload kit."""
from pathlib import Path
import datetime
import hashlib
import json
import shutil
import zipfile

ROOT = Path(__file__).resolve().parent
AUDIT = ROOT.parent
TITLE = 'Positive tangent-bundle Seshadri constants characterize projective space'
METADATA = {
    'title': TITLE, 'upload_type': 'publication', 'publication_type': 'preprint',
    'publication_date': '2026-10-12',
    'creators': [{'name': 'Kriebel, Alec', 'affiliation': 'Independent researcher',
                  'orcid': '0009-0001-9320-500X'}],
    'description': (
        '<p>Let X be a smooth integral projective variety of dimension n at least one '
        'over an algebraically closed field of arbitrary characteristic. Positivity '
        'of the relative Fulger-Murayama Seshadri constant of the tangent bundle at '
        'one arbitrary closed point implies that X is projective n-space. The '
        'five-page research note proves Fulger-Murayama Conjecture 4.9 without '
        'assuming Fano, global tangent nefness, characteristic zero, or a general point.</p>'
        '<p>An absolute minimum of ample degree through the specified point '
        'eliminates the boundary of the one-marked stable-map family. Very-free '
        'evaluation and the actual contracted marking section give numerical '
        'Picard rank one and ampleness of the anticanonical divisor; the established '
        'Fano clause completes the proof. Standard numerical-generation methods, '
        'Mori/Kollar, Fulger-Murayama, and Chang\'s toric case are credited. The '
        'source and verification archive preserves the frozen original candidate, '
        'independent mathematical reviews, a documented 64-query priority audit, '
        'and portable integrity and finite controls. Those computations do not '
        'formally verify the geometric theorem.</p>'
        '<p>AI tools were used extensively in developing, checking, reviewing, '
        'and preparing the result. This is an unrefereed preprint; internal '
        'AI-assisted review is not external human peer review. A bounded '
        'primary-source audit found no earlier full resolution, but first '
        'historical priority is not certified. The full Kollar monograph and '
        'CMSB text were not independently obtained; the exact imported published '
        'Fulger-Murayama propositions were inspected. The deposit is licensed '
        'CC BY 4.0.</p>'),
    'access_right': 'open', 'license': 'cc-by-4.0', 'version': '1.0', 'language': 'eng',
    'keywords': ['Seshadri constants', 'tangent bundle', 'projective space',
                 'rational curves', 'positive characteristic',
                 'Fulger-Murayama conjecture', 'algebraic geometry', 'OWR-17296-007'],
    'related_identifiers': [
        {'identifier': '10.1016/j.jpaa.2020.106559', 'relation': 'references', 'scheme': 'doi'},
        {'identifier': '10.4171/OWR/2019/53', 'relation': 'references', 'scheme': 'doi'},
        {'identifier': '10.1016/j.jpaa.2025.108046', 'relation': 'references', 'scheme': 'doi'},
        {'identifier': '10.4310/AJM.2005.v9.n4.a5', 'relation': 'references', 'scheme': 'doi'},
        {'identifier': 'https://github.com/AlecKriebel/Math/pull/718',
         'relation': 'isDocumentedBy', 'scheme': 'url'},
        {'identifier': 'https://github.com/AlecKriebel/Math/tree/main/'
         'draft_pr_claimed_solved_700_800_20261012/audits/pr718_30004324',
         'relation': 'isSupplementedBy', 'scheme': 'url'}]}


def json_write(path, value):
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + '\n')


def copy_file(source, dest):
    if source.is_symlink() or not source.is_file():
        raise ValueError(f'Unexpected source object: {source}')
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, dest)


def archive(path, files):
    with zipfile.ZipFile(path, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for name, raw in sorted(files.items()):
            info = zipfile.ZipInfo(name, date_time=(2026, 10, 12, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            z.writestr(info, raw)


def main():
    support = ROOT / 'support'
    if support.exists():
        shutil.rmtree(support)
    support.mkdir()
    copy_file(ROOT / 'paper.tex', support / 'paper.tex')
    copy_file(ROOT / 'verify_bundle.py', support / 'verify_bundle.py')
    copy_file(ROOT / 'README-verification.md', support / 'README.md')
    json_write(support / 'zenodo-metadata.json', {'metadata': METADATA})
    original = AUDIT / 'original/unsolved_math_prioritization/attempts/30004324'
    for path in sorted(original.rglob('*')):
        if path.is_file():
            copy_file(path, support / 'historical_candidate' / path.relative_to(original))
    for name in ['review_pointed_geometry', 'review_picard_fano', 'priority_audit']:
        # Authored reports and metadata only; never source downloads/extracts.
        for path in sorted((AUDIT / name).iterdir()):
            if path.is_file() and path.suffix in {'.md', '.json', '.py'}:
                copy_file(path, support / 'audit' / name / path.name)
    for name in ['ROOT_MATHEMATICAL_REVIEW.md', 'ROOT_PRIORITY_CHECKS.md',
                 'root_reproduction_normal.json', 'root_reproduction_optimized.json',
                 'ROOT_POINTED_CONTROL_REPRODUCTION.json', 'FM21_retrieval_receipt.json']:
        copy_file(AUDIT / name, support / 'audit' / name)
    files = {p.relative_to(support).as_posix(): p.read_bytes()
             for p in support.rglob('*') if p.is_file()}
    json_write(support / 'MANIFEST.json', {
        'schema': 'sha256-exact-file-inventory-v1',
        'scope': 'Source, authored audits, bibliographic provenance, and finite/integrity controls; not a formal geometry proof.',
        'files': [{'path': name, 'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()}
                  for name, raw in sorted(files.items())]})
    files['MANIFEST.json'] = (support / 'MANIFEST.json').read_bytes()
    archive(ROOT / 'source-and-verification.zip', files)
    deposit = {'metadata': METADATA, 'files': [
        {'path': 'output/pdf/paper.pdf', 'name': 'paper.pdf'},
        {'path': 'source-and-verification.zip', 'name': 'source-and-verification.zip'}]}
    json_write(ROOT / 'zenodo-deposit.json', deposit)
    json_write(ROOT / 'zenodo-metadata.json', {'metadata': METADATA})
    flat_deposit = {'metadata': METADATA, 'files': [
        {'path': 'paper.pdf'}, {'path': 'source-and-verification.zip'}]}
    archive(ROOT / 'zenodo-upload-kit.zip', {
        'paper.pdf': (ROOT / 'output/pdf/paper.pdf').read_bytes(),
        'source-and-verification.zip': (ROOT / 'source-and-verification.zip').read_bytes(),
        'zenodo-deposit.json': (json.dumps(flat_deposit, indent=2, ensure_ascii=False) + '\n').encode(),
        'zenodo-metadata.json': (ROOT / 'zenodo-metadata.json').read_bytes(),
        'README.md': b'Upload paper.pdf and source-and-verification.zip separately using the enclosed metadata. The outer ZIP is a convenience kit, not an extra deposit file.\n'})
    outputs = ['paper.tex', 'output/pdf/paper.pdf', 'source-and-verification.zip',
               'zenodo-deposit.json', 'zenodo-metadata.json', 'zenodo-upload-kit.zip']
    json_write(ROOT / 'PACKAGE_INVENTORY.json', {
        'built_at': datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'title': TITLE, 'version': '1.0', 'support_files': len(files),
        'files': [{'path': name, 'bytes': (ROOT / name).stat().st_size,
                   'sha256': hashlib.sha256((ROOT / name).read_bytes()).hexdigest()}
                  for name in outputs]})
    print(json.dumps({'support_files': len(files), 'outputs': outputs}, indent=2))


if __name__ == '__main__':
    main()
