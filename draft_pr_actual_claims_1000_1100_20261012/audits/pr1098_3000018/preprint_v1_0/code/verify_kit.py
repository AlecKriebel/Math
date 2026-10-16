"""Strict payload, metadata and present-required external binding verifier."""
import sys
sys.dont_write_bytecode = True
import json
from common import ROOT, archive_bytes, digest, load, member, regular, require
from metadata_constants import EXPECTED_METADATA

def verify():
    for path in ('metadata.json', 'zenodo-api.json', 'publication/zenodo-deposit.json'):
        j = load(ROOT/path)
        obj = j if path == 'metadata.json' else j['metadata']
        require(obj == EXPECTED_METADATA, 'native metadata mismatch: '+path)
    native = load(ROOT/'publication/zenodo-deposit.json')
    require(set(native) == {'metadata','files'}, 'native upload root fields')
    require(native['files'] == [
        {'path':'../paper.pdf','name':'paper.pdf'},
        {'path':'../pr1098_support_v1_0.zip','name':'pr1098_support_v1_0.zip'}],
        'native exact file selections')
    require(set(load(ROOT/'zenodo-api.json')) == {'metadata'}, 'API metadata wrapper')
    manifest = load(ROOT/'MANIFEST.json')
    require(manifest['schema_version'] == 1, 'manifest schema')
    archive = archive_bytes()
    bindings = load(ROOT/'ARTIFACT_BINDINGS.json')  # Required, even in an extraction.
    require(set(bindings) == {'paper.pdf'}, 'external PDF binding names')
    for name, expected in bindings.items():
        raw = regular(ROOT/name).read_bytes()
        require(expected == {'bytes':len(raw),'sha256':digest(raw)}, 'artifact binding: '+name)
    require(archive == regular(ROOT/'pr1098_support_v1_0.zip').read_bytes(),
            'current archive does not equal closed deterministic reconstruction')
    require(regular(ROOT/'paper.pdf').read_bytes().startswith(b'%PDF-'), 'PDF header')
    return {'status':'PASS','payload_members':len(manifest['entries']),
            'strict_present_required_bindings':True,'metadata_objects_exact':True,
            'archive_bytes':len(archive),'archive_sha256':digest(archive)}

if __name__ == '__main__':
    require(not sys.argv[1:], 'stdout verifier accepts no output argument')
    print(json.dumps(verify(), sort_keys=True, indent=2))
