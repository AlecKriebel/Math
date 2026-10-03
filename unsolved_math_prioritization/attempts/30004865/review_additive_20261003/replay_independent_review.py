#!/usr/bin/env python3
"""Stage the frozen independent checker in its original layout without editing it.
Sources are required for this source-bound audit. Missing sources yield exit 2,
not a successful or partially successful audit. The five author scripts do not
need these sources and remain runnable directly from --attempt.
"""
import argparse
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--attempt',required=True,type=Path,help='Published attempt directory containing TURN_5_MANIFEST.json and the copied frozen review')
parser.add_argument('--sources',type=Path,help='Directory containing the nine separately obtained, manifest-bound source files')
args=parser.parse_args()
attempt=args.attempt.resolve()
review=attempt/'review_independent_20261003'
needed=[]
try:
    author=json.loads((attempt/'TURN_5_MANIFEST.json').read_text())
    reviewed=json.loads((review/'REVIEW_MANIFEST.json').read_text())
    for name in ['SOURCE_MANIFEST.json','SOURCE_ADDITION_T2.json','SOURCE_ADDITION_T3.json','SOURCE_ADDITION_T5.json']:
        needed.extend(x['file'] for x in json.loads((attempt/name).read_text())['sources'])
except (OSError,ValueError,KeyError) as error:
    parser.exit(2,f'Preflight failed: published attempt/review metadata unavailable: {error}\n')
missing=[name for name in needed if args.sources is None or not (args.sources/name).is_file()]
if missing:
    print(json.dumps({'status':'NOT_RUN_MISSING_SOURCES','independent_audit_run':False,
        'missing_source_files':missing,'required_source_location':'--sources DIRECTORY',
        'obtain_urls_and_expected_hashes_from':['SOURCE_MANIFEST.json','SOURCE_ADDITION_T2.json','SOURCE_ADDITION_T3.json','SOURCE_ADDITION_T5.json'],
        'author_scripts':'The five verify_turnN.py scripts remain runnable directly from the attempt directory without these source files.'},indent=2))
    sys.exit(2)
with tempfile.TemporaryDirectory(prefix='entanglement_review_replay_') as tmp:
    root=Path(tmp)
    for base,dst,manifest,name in [(attempt,root/'attempt',author,'TURN_5_MANIFEST.json'),(review,root/'review_independent_20261003',reviewed,'REVIEW_MANIFEST.json')]:
        dst.mkdir()
        for rel in [x['path'] for x in manifest['files']]+[name]:
            source=base/rel
            target=dst/rel
            target.parent.mkdir(parents=True,exist_ok=True)
            shutil.copyfile(source,target)
    (root/'sources').mkdir()
    for name in needed:shutil.copyfile(args.sources/name,root/'sources'/name)
    result=subprocess.run([sys.executable,str(root/'review_independent_20261003'/'independent_checks.py')],check=False)
    sys.exit(result.returncode)
