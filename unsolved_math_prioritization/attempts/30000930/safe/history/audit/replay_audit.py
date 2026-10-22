#!/usr/bin/env python3
"""Replay this audit against the exact frozen author archive.
Usage: python3 replay_audit.py /path/to/author-packet.zip
"""
import hashlib
import importlib.util
import json
from pathlib import Path
from fractions import Fraction as F
import subprocess
import sys
import tempfile
import zipfile


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main():
    root = Path(__file__).resolve().parent
    binding = json.loads((root/'BINDING.json').read_text())
    archive = Path(sys.argv[1])
    data = archive.read_bytes()
    assert len(data) == binding['author_archive']['bytes']
    assert hashlib.sha256(data).hexdigest() == binding['author_archive']['sha256']
    for entry in binding['audit_files']:
        data = (root/entry['path']).read_bytes()
        assert len(data) == entry['bytes'], entry['path']
        assert hashlib.sha256(data).hexdigest() == entry['sha256'], entry['path']
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        with zipfile.ZipFile(archive) as zf:
            assert sorted(zf.namelist()) == sorted(binding['author_archive']['members'])
            for entry in zf.infolist():
                assert entry.filename.startswith('safe/')
                assert not Path(entry.filename).is_absolute()
                assert '..' not in Path(entry.filename).parts
            zf.extractall(tmp)
        author = tmp/'safe'
        subprocess.run([sys.executable, 'verify_manifest.py'], cwd=author, check=True, capture_output=True)
        generated = tmp/'author_replayed_results.json'
        subprocess.run([sys.executable, str(author/'verify.py'), '--output', str(generated)],
                       check=True, capture_output=True)
        assert generated.read_bytes() == (author/'CONTROL_RESULTS.json').read_bytes()
        independent = subprocess.check_output([sys.executable, str(root/'independent_check.py')])
        assert independent == (root/'INDEPENDENT_RESULTS.json').read_bytes()
        a = load_module('author_check', author/'verify.py')
        b = load_module('independent_check', root/'independent_check.py')
        comparisons = 0
        for wa, wb in [(F(1),F(1)),(F(1),F(-1)),(F(0),F(0)),(F(2,3),F(-7,5))]:
            for i in range(12):
                for j in range(12):
                    result = {}
                    for (out, e, f), c in b.TENSOR[i][j].items():
                        result[out] = result.get(out, 0) + c*wa**e*wb**f
                    result = {k:v for k,v in result.items() if v}
                    assert result == a.basis_product(i,j,wa,wb)
                    comparisons += 1
    print(json.dumps({'status':'PASS', 'author_archive_bound':True,
                      'author_manifest_verified':True, 'author_replay_byte_match':True,
                      'independent_replay_byte_match':True,
                      'independent_symbolic_basis_triples':1728,
                      'exact_product_comparisons':comparisons}, sort_keys=True))


if __name__ == '__main__':
    main()
