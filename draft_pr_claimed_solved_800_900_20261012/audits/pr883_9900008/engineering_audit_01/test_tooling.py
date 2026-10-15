#!/usr/bin/env python3
"""Falsify current tooling guards; no archival harness is imported as a module."""
import copy
import hashlib
import importlib.util
import io
import json
import os
from pathlib import Path
import shutil
import stat
import struct
import subprocess
import sys
import tempfile
import zipfile

BASE = Path(__file__).resolve().parent.parent
TOOLS = BASE / 'tooling_candidate'
MODES = ['-I', '-S', '-B'] + (['-O'] if sys.flags.optimize else [])


def need(ok, message):
    if not ok:
        raise ValueError(message)


def load(name):
    spec = importlib.util.spec_from_file_location(name, TOOLS / (name + '.py'))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def js(value):
    return (json.dumps(value, sort_keys=True, indent=2) + '\n').encode()


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def seal(root, outer=False):
    index_name = 'CURRENT_PUBLICATION_MANIFEST.json' if outer else 'package_index.json'
    rows = []
    # Fixtures are small and deliberately constructed in this temporary tree.
    for path in sorted(root.rglob('*')):
        if path.is_file() and path.name != index_name:
            raw = path.read_bytes()
            rows.append({'path': path.relative_to(root).as_posix(), 'bytes': len(raw), 'sha256': digest(raw)})
    raw = js({'schema': 'diffuse-9900008-current-publication-v1' if outer else 'diffuse-9900008-verification-v1', 'problem_id': '9900008', 'files': rows})
    (root / index_name).write_bytes(raw)
    return digest(raw)


def invoke(script, args, expected=True):
    proc = subprocess.run([sys.executable, *MODES, str(TOOLS / script), *map(str, args)], capture_output=True, timeout=1800, cwd=BASE / 'engineering_audit_01')
    need(not proc.stderr, 'unexpected stderr: ' + proc.stderr.decode(errors='replace'))
    result = json.loads(proc.stdout)
    need((proc.returncode == 0 and result['status'] == 'PASS') if expected else (proc.returncode != 0 and result['status'] == 'REJECTED'), 'wrong CLI outcome: ' + script + ': ' + proc.stdout.decode())
    if 'archive' in result:
        result['archive'] = Path(result['archive']).name
        result['archive_path_redacted'] = True
    return {'script': script, 'flags': MODES, 'returncode': proc.returncode, 'stdout_bytes': len(proc.stdout), 'stdout_sha256': digest(proc.stdout), 'result': result}


def zip_bytes(mapping):
    out = io.BytesIO()
    with zipfile.ZipFile(out, 'w') as archive:
        for name, data in sorted(mapping.items()):
            info = zipfile.ZipInfo(name, (2026, 10, 15, 0, 0, 0))
            info.create_system = 3
            info.external_attr = (stat.S_IFREG | 0o644) << 16
            info.compress_type = zipfile.ZIP_DEFLATED
            archive.writestr(info, data)
    return out.getvalue()


def main():
    need(sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode, 'run -I -S -B')
    current, original, outer = load('verify_package'), load('check_originals'), load('verify_current_publication')
    rejected, positives, receipts = [], [], []
    exceptions = (ValueError, OSError, KeyError, TypeError, OverflowError, RecursionError, zipfile.BadZipFile, UnicodeError, struct.error)
    def reject(name, action):
        try:
            action()
        except exceptions as exc:
            rejected.append({'name': name, 'rejected': True, 'reason': str(exc)})
        else:
            raise ValueError('negative control accepted: ' + name)
    def accept(name, action):
        action()
        positives.append({'name': name, 'passed': True})
    row = {'path': 'a/b', 'bytes': 1, 'sha256': '0' * 64}
    for raw in (b'{"x":1,"x":2}', b'{"x":NaN}', b'{"x":Infinity}', b'{"x":-Infinity}', b'{"x":1e999}', b'{"a":{"x":1,"x":2}}'):
        reject('strict-json:' + raw.decode(), lambda raw=raw: current.strict_json(raw))
    accept('strict-json-positive', lambda: need(current.strict_json(b'{"x":1.5,"b":false}') == {'x': 1.5, 'b': False}, 'JSON positive'))
    for bad in (True, 1.0, -1, 2**40, '1'):
        reject('typed-inventory-bytes:' + repr(bad), lambda bad=bad: current.pin_row({**row, 'bytes': bad}))
    for name in ('../x', '/x', 'a//b', 'a/./b', 'a/../b', 'a\\b', 'C:x', 'a\x00b', 'a\nb', 'é', ''):
        reject('unsafe-path:' + repr(name), lambda name=name: current.safe_name(name))
    for names in (('a','a'), ('a','A'), ('a','a/b'), ('A','a/b'), ('dir/a','DIR/b')):
        reject('inventory-alias:' + repr(names), lambda names=names: current.rows_map([{**row, 'path': n} for n in names]))
    cert = json.loads((BASE / 'source/author/certificate.json').read_bytes())
    accept('certificate-positive', lambda: original.certificate_typed(cert))
    for key, value in [('dimension', True), ('dimension', 2.0), ('source_coset_count', 2.0), ('expected_preserving_target_labels', [[False, True]]), ('expected_preserving_target_labels', [[0.0, 1.0]]), ('line_weights', [1, '2']), ('period', 'NaN'), ('period', '1/0')]:
        bad = copy.deepcopy(cert); bad[key] = value
        reject('certificate-type:' + key + ':' + repr(value), lambda bad=bad: original.certificate_typed(bad))
    payload = {'a.json': b'{"typed":1}', 'b.txt': b'test'}
    rawzip = zip_bytes(payload)
    accept('ZIP-positive', lambda: current.zip_payloads(rawzip, payload, generated=True))
    mutations = {'prefix': b'x' + rawzip, 'trailer': rawzip + b'x', 'truncated': rawzip[:-1]}
    bad = bytearray(rawzip); bad[10] ^= 1; mutations['local-time-disagreement'] = bytes(bad)
    bad = bytearray(rawzip); bad[30] ^= 1; mutations['local-name-disagreement'] = bytes(bad)
    bad = bytearray(rawzip); central = struct.unpack_from('<4s4H2IH', bad, len(bad)-22)[6]; bad[central+12] ^= 1; mutations['central-time-disagreement'] = bytes(bad)
    for name, raw in mutations.items():
        reject('ZIP-' + name, lambda raw=raw: current.zip_payloads(raw, payload, generated=True))
    reject('ZIP-member-deletion', lambda: current.zip_payloads(zip_bytes({'a.json': payload['a.json']}), payload, generated=True))
    reject('ZIP-expanded-byte-mismatch', lambda: current.zip_payloads(rawzip, {**payload, 'b.txt': b'fail'}, generated=True))
    with tempfile.TemporaryDirectory(prefix='pr883 small engineering fixtures ') as td:
        work = Path(td)
        tree = work / 'closed'; tree.mkdir(); (tree / 'a').write_bytes(b'x')
        accept('closed-tree-positive', lambda: current.closed_tree(tree, {'a'}))
        (tree / 'empty').mkdir(); reject('extra-empty-directory', lambda: current.closed_tree(tree, {'a'})); (tree/'empty').rmdir()
        (tree / 'alias').symlink_to(tree, target_is_directory=True); reject('extra-symlink-directory', lambda: current.closed_tree(tree, {'a'})); (tree/'alias').unlink()
        (tree / 'alias').symlink_to(tree/'a'); reject('same-byte-symlink-file', lambda: current.read_regular(tree/'alias')); (tree/'alias').unlink()
        fifo=tree/'fifo'; os.mkfifo(fifo); reject('FIFO-bounded-leaf', lambda: current.read_regular(fifo)); reject('FIFO-closed-tree', lambda: current.closed_tree(tree, {'a'})); fifo.unlink()
        (tree/'dir').mkdir(); (tree/'dir'/'a').write_bytes(b'x'); saved=tree/'dir'; saved.rename(tree/'saved'); saved.symlink_to(tree/'saved',target_is_directory=True)
        reject('listed-symlink-parent', lambda: current.within(tree, 'dir/a')); saved.unlink(); shutil.rmtree(tree/'saved')
        reject('bounded-read-size', lambda: current.read_regular(tree/'a', limit=0))
        alias=work/'root-alias'; alias.symlink_to(tree,target_is_directory=True); reject('selected-root-leaf-alias', lambda: current.selected_root(alias))
        corpus = BASE.parents[2] / 'unsolved_math_prioritization/catalog.json'
        reject('complete-corpus-streaming-digest-mismatch', lambda: current.stream_pin(corpus, 21735099, '0' * 64))
        # A read-only private hardlink is never written, chmod'ed or truncated.
        # Unlink it before a destructive negative fixture is constructed.
        linked = work / 'catalog.json'
        os.link(corpus, linked, follow_symlinks=False)
        accept('source-readonly-hardlink-pin', lambda: current.stream_pin(linked, *original.INPUT_PINS['catalog.json']))
        linked.unlink()
        linked.write_bytes(b'corrupted private fixture')
        reject('source-private-replacement-size', lambda: current.stream_pin(linked, *original.INPUT_PINS['catalog.json']))
        linked.unlink()
        linked.symlink_to(corpus)
        reject('source-leaf-symlink', lambda: current.stream_pin(linked, *original.INPUT_PINS['catalog.json']))
        linked.unlink()
        assembly=work/'assembly'; assembly.mkdir()
        for name in ('check_originals.py','verify_package.py','build_verification.py','verify_current_publication.py'):
            shutil.copyfile(TOOLS/name,assembly/name)
        (assembly/'root_evidence').mkdir(); shutil.copyfile(BASE/'SOURCE_MANIFEST.json',assembly/'root_evidence/SOURCE_MANIFEST.json')
        shutil.copytree(BASE/'source',assembly/'source',copy_function=shutil.copyfile)
        (assembly/'README.md').write_text('Synthetic verification tooling fixture. No paper or publication approval.\n')
        index=seal(assembly)
        pins, blobs=current.package_inputs(assembly,index,'verify_package.py')
        accept('all26-frozen-original-structure', lambda: original.original_inputs(blobs))
        accept('portable-positive', lambda: current.package_inputs(assembly,index,'verify_package.py'))
        (assembly/'empty').mkdir(); reject('portable-extra-empty-directory', lambda: current.package_inputs(assembly,index)); (assembly/'empty').rmdir()
        path=assembly/'source/author/PROOF.md'; raw=path.read_bytes(); path.unlink(); path.symlink_to(BASE/'source/author/PROOF.md')
        reject('portable-same-byte-symlink', lambda: current.package_inputs(assembly,index)); path.unlink(); path.write_bytes(raw)
        # Reanchor the outer inventory: the separate immutable source manifest
        # still rejects coordinated source deletion before archived execution.
        badblobs=dict(blobs); del badblobs['source/review1/AUDIT.md']
        reject('coordinated-source-deletion-vs-frozen-anchor', lambda: original.original_inputs(badblobs))
        manifestpath=assembly/'package_index.json'; baseline=manifestpath.read_bytes()
        for label, malformed in [('duplicate-key',baseline.replace(b'"schema":',b'"schema":"forged","schema":',1)), ('overflow-number',baseline.replace(b'"bytes": 1702',b'"bytes": 1e999',1)), ('bool-byte-count',baseline.replace(b'"bytes": 1702',b'"bytes": true',1))]:
            manifestpath.write_bytes(malformed)
            reject('reanchored-index-'+label, lambda malformed=malformed: current.package_inputs(assembly,digest(malformed)))
        manifestpath.write_bytes(baseline)
        # A reanchored non-source JSON payload exercises strict parsing before
        # any executable is called, independent of the immutable source pin.
        extra=assembly/'adversarial.json'
        for label, raw in [('duplicate',b'{"x":1,"x":2}'),('nonfinite',b'{"x":NaN}'),('overflow',b'{"x":1e999}')]:
            extra.write_bytes(raw); pin=seal(assembly)
            reject('reanchored-payload-'+label, lambda pin=pin: current.package_inputs(assembly,pin))
        extra.unlink(); manifestpath.write_bytes(baseline)
        startup=assembly/'verify_package.py'; startup.write_bytes(startup.read_bytes()+b'\n# altered copy\n'); altered=seal(assembly)
        reject('reanchored-startup-mismatch-before-replay', lambda: current.package_inputs(assembly,altered,'verify_package.py'))
        receipts.append(invoke('verify_package.py',[altered,'--root',assembly],False))
        shutil.copyfile(TOOLS/'verify_package.py',startup); index=seal(assembly)
        receipts.append(invoke('verify_package.py',[index,'--root',assembly]))
        need(receipts[-1]['result']['originals']['direct_subprocess_count']==6 and receipts[-1]['result']['originals']['nested_author_subprocess_count']==16,'actual full replay counts')
        receipts.append(invoke('verify_package.py',[index,'--root',assembly,'--verify-only','--catalog',BASE.parents[2]/'unsolved_math_prioritization/catalog.json','--problems',BASE.parents[2]/'unsolved_math_prioritization/cache/problems.json','--reports',BASE.parents[2]/'unsolved_math_prioritization/cache/research_results.json','--pdf-dir',BASE/'private_sources']))
        need(len(receipts[-1]['result']['originals']['source_authentication']['inputs'])==8,'source input receipt count')
        # Each suite mode performs two full builds in its own interpreter mode.
        verifier_pin=digest((TOOLS/'verify_package.py').read_bytes())
        for name in ('build1','build2'):
            receipts.append(invoke('build_verification.py',[assembly,index,verifier_pin,work/name]))
        zip1=(work/'build1/verification.zip').read_bytes(); zip2=(work/'build2/verification.zip').read_bytes()
        need(zip1==zip2,'repeated same-runtime build differs')
        positives.append({'name':'repeated-byte-identical-build','passed':True,'bytes':len(zip1),'sha256':digest(zip1)})
        # Build failure does not create the output directory.
        failed=work/'failed-output'
        receipts.append(invoke('build_verification.py',[assembly,index,'0'*64,failed],False)); need(not failed.exists(),'failed build wrote output')
        rejected.append({'name':'builder-bad-external-verifier-pin-no-output','rejected':True})
        outerroot=work/'outer'; outerroot.mkdir()
        shutil.copyfile(TOOLS/'verify_current_publication.py',outerroot/'verify_current_publication.py')
        preserved=set(json.loads((BASE/'SOURCE_MANIFEST.json').read_bytes())['files'][i]['path'] for i in range(26))-{'README.md','RESEARCH_LOG.md'}
        for name in preserved:
            target=outerroot/name; target.parent.mkdir(parents=True,exist_ok=True); shutil.copyfile(BASE/'source'/name,target)
        (outerroot/'README.md').write_text('Synthetic outer fixture.\n'); (outerroot/'RESEARCH_LOG.md').write_text('Synthetic outer log.\n')
        shutil.copytree(assembly,outerroot/'preprint/verification_package')
        shutil.copyfile(work/'build1/verification.zip',outerroot/'preprint/verification.zip')
        shutil.copyfile(assembly/'README.md', outerroot/'preprint/README.md')
        for name in ('metaA.json', 'metaB.json'):
            (outerroot/name).write_bytes(js({'typed': 1}))
        config={'portable_prefix':'preprint/verification_package','zip_path':'preprint/verification.zip','copy_pairs':[{'outer_path':'preprint/README.md','portable_path':'README.md'}], 'preserved_source_paths':sorted(preserved),'json_equal_groups':[['metaA.json','metaB.json']]}
        (outerroot/'CURRENT_PUBLICATION.json').write_bytes(js({'tooling_layout':config}))
        outerpin=seal(outerroot,True)
        receipts.append(invoke('verify_current_publication.py',[outerpin,'--root',outerroot]))
        _,outerblobs=outer.outer_inputs(outerroot,outerpin)
        accept('current-root-positive',lambda:outer.portable_inputs(outerblobs))
        bad=dict(outerblobs); bad['preprint/README.md']+=b'changed'
        reject('outer-portable-explicit-copy-mismatch',lambda:outer.portable_inputs(bad))
        bad=dict(outerblobs); bad['metaB.json']=js({'typed':True})
        reject('outer-typed-JSON-metadata-mismatch',lambda:outer.portable_inputs(bad))
        bad=dict(outerblobs); bad['preprint/verification.zip']=b'x'+zip1
        reject('outer-ZIP-prefix-with-reanchored-bytes',lambda:outer.portable_inputs(bad))
        # Explicit metadata-preserving source change must fail even when the
        # outer and portable container inventories are reanchored by an attacker.
        bad=dict(outerblobs); bad['author/PROOF.md']+=b'changed'
        reject('outer-preserved-original-mismatch',lambda:outer.portable_inputs(bad))
        # Confirm the immutable input tree still authenticates after all tests.
        original.original_inputs(blobs)
    result={'status':'PASS','scope':'Tools-only guard falsification and finite diagnostic replay; independent package adversary still required.', 'optimized':bool(sys.flags.optimize), 'negative_control_count':len(rejected),'positive_control_count':len(positives),'negative_controls':rejected,'positive_controls':positives,'cli_receipts':receipts,'no_corpus_copy_or_write':True,'historical_executable_audit_replayed':False}
    output=BASE/'engineering_audit_01'/('TEST_OPTIMIZED.json' if sys.flags.optimize else 'TEST_NORMAL.json')
    output.write_bytes(js(result))
    print(json.dumps({'status':'PASS','negative_controls':len(rejected),'positive_controls':len(positives),'cli_receipts':len(receipts),'receipt_file':str(output)},sort_keys=True))


if __name__=='__main__':
    main()
