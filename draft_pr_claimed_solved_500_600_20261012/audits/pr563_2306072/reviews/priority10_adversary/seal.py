"""Seal authored review files. Raw source evidence stays outside this seal."""
from pathlib import Path
import hashlib
import json
import argparse

ROOT=Path(__file__).resolve().parent
MANIFEST=ROOT/'MANIFEST.json'

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def inventory():
    files={}
    for path in sorted(ROOT.rglob('*')):
        if not path.is_file():
            continue
        rel=path.relative_to(ROOT)
        if '.cache' in rel.parts or '__pycache__' in rel.parts or path==MANIFEST:
            continue
        files[str(rel)]={'sha256':digest(path),'bytes':path.stat().st_size}
    return files

parser=argparse.ArgumentParser()
parser.add_argument('--verify',action='store_true')
parser.add_argument('--sources',action='store_true')
args=parser.parse_args()
if args.verify:
    record=json.loads(MANIFEST.read_text())
    actual=inventory()
    assert actual==record['files'],'Authored file set or bytes differ'
    result={'authored_files':len(actual),'authored_seal_pass':True}
    if args.sources:
        inputs=json.loads((ROOT/'SOURCE_INPUTS.json').read_text())['inputs']
        for row in inputs:
            path=Path(row['path'])
            assert path.is_file() and digest(path)==row['sha256'],row['name']
        result.update({'external_inputs':len(inputs),'external_hashes_pass':True})
    print(json.dumps(result,sort_keys=True))
else:
    record={'scope':'All present authored review files; excludes this manifest itself and ignored cache/raw PDFs/OCR/images. No external source bytes are republished.',
            'files':inventory()}
    MANIFEST.write_text(json.dumps(record,indent=2)+'\n')
    print(json.dumps({'sealed_authored_files':len(record['files'])}))
