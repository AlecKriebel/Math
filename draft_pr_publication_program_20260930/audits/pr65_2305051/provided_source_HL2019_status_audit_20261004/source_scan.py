import hashlib, json, pathlib, shutil
BASE = pathlib.Path('/Users/alec/.cache/codex-pr65-priority-20261004/provided_primary_sources_20261004')
DEST = pathlib.Path('/Users/alec/.cache/codex-pr65-priority-20261004/status_family_20261004')
for name in ['hayman2019.pdf', 'hayman2019.pdf.txt']:
    shutil.copyfile(BASE/name, DEST/name)
pages = (DEST/'hayman2019.pdf.txt').read_text().split('\f')
print('TEXT FORMFEED SEGMENTS', len(pages))
for i, page in enumerate(pages):
    if i < 8 or any(term in page for term in ['5.51', 'Functions in the Unit Disc', 'Holland', 'Blaschke']):
        print('\n=== PDF PAGE', i+1, '===\n'+page)
author = pathlib.Path('/Users/alec/Documents/Math/draft_pr_publication_program_20260930/audits/pr65_2305051/publication_package_v1/verification/author')
print('\nAUTHOR FILENAMES', [x.name for x in author.iterdir() if x.is_file()])
print('\n=== CANDIDATE ===\n'+(author/'CANDIDATE.md').read_text())
