#!/usr/bin/env python3
"""Independent bounded helper controls; never executes archival code.

Synthetic helper inputs test format boundaries only. They are not a paper,
publication wrapper, authenticated source corpus, or mathematical evidence.
"""
from pathlib import Path
import argparse
import datetime
import hashlib
import json
import os
import runpy
import stat
import struct
import tempfile
import types
import zipfile
import zlib

HERE = Path(__file__).resolve().parent
TOOL = HERE.parent / 'publication_tools_02' / 'portable.py'
ASSIGNED = '09e4932f66c15916891245a1fb3d6a7052cb5619710d94e0e2305fb7a7612aa6'


def main():
    parser = argparse.ArgumentParser(allow_abbrev=False)
    parser.add_argument('--output', default='HELPER_V2_RECEIPTS.json')
    args = parser.parse_args()
    raw = TOOL.read_bytes()
    assert hashlib.sha256(raw).hexdigest() == ASSIGNED
    api = runpy.run_path(str(TOOL), run_name='format_review_only')
    receipts = []

    def reject(name, function, *values):
        try:
            function(*values)
        except (ValueError, KeyError, TypeError, OSError, zipfile.BadZipFile, zlib.error, struct.error) as exc:
            receipts.append({'case': name, 'rejected': True, 'exception': type(exc).__name__, 'reason': str(exc)})
        else:
            raise AssertionError('Unexpected helper acceptance: ' + name)

    def accept(name, function, *values):
        result = function(*values)
        receipts.append({'case': name, 'accepted': True})
        return result

    for name, raw_json in [
        ('json_duplicate', b'{"a":0,"a":1}'), ('json_nested_duplicate', b'{"a":{"x":1,"x":2}}'),
        ('json_nan', b'{"a":NaN}'), ('json_infinity', b'{"a":Infinity}'),
        ('json_negative_infinity', b'{"a":-Infinity}'), ('json_float_overflow', b'{"a":1e10000}')]:
        reject(name, api['strict_json'], raw_json)
    accept('json_finite', api['strict_json'], b'{"x":[0,1.5,"a",null]}')
    for name in ['', '/x', '../x', 'a/../x', 'a//x', 'a/', './x', 'a\\x', 'a:x', 'x\n', 'x' * 513]:
        reject('path_' + repr(name), api['safe_name'], name)
    accept('path_safe_nested', api['safe_name'], 'root_evidence/SOURCE_MANIFEST.json')
    row = {'path': 'a/x', 'bytes': 0, 'sha256': '0' * 64}
    accept('row_valid', api['pin_row'], row)
    for label, key, value in [('bool_bytes','bytes',True), ('float_bytes','bytes',0.0), ('negative_bytes','bytes',-1),
                              ('oversize_bytes','bytes',api['MAX_FILE']+1), ('digest_upper','sha256','A'*64),
                              ('digest_nonstring','sha256',0), ('path_nonstring','path',False)]:
        mutation = dict(row); mutation[key] = value
        reject(label, api['pin_row'], mutation)
    reject('row_extra_key', api['pin_row'], {**row, 'extra': 0})
    reject('rows_duplicate', api['rows_map'], [row, dict(row)])
    reject('rows_case_alias', api['rows_map'], [row, {**row, 'path': 'A/X'}])
    reject('directory_alias', api['rows_map'], [row, {**row, 'path': 'A/y'}])
    reject('file_directory_collision', api['rows_map'], [row, {**row, 'path': 'a/x/y'}])
    reject('rows_total_bound', api['rows_map'], [{**row, 'path': 'x'+str(i), 'bytes':api['MAX_FILE']} for i in range(3)])
    for label, value in [('index_bool_identity', {'schema':api['PACKAGE_SCHEMA'],'problem_id':9700042,'files':[row]}),
                         ('index_extra_key', {'schema':api['PACKAGE_SCHEMA'],'problem_id':'9700042','files':[row],'extra':0})]:
        reject(label, api['typed_index'], json.dumps(value).encode(), api['PACKAGE_SCHEMA'])

    with tempfile.TemporaryDirectory(prefix='helper-', dir=HERE) as td:
        root = Path(td)
        (root/'a').mkdir(); (root/'a/x').write_bytes(b'')
        accept('tree_valid', api['closed_tree'], root, {'a/x'})
        (root/'empty').mkdir()
        reject('tree_empty_directory', api['closed_tree'], root, {'a/x'})
        (root/'empty').rmdir()
        (root/'link').symlink_to(root/'a/x')
        reject('tree_symlink', api['closed_tree'], root, {'a/x','link'})
        reject('read_regular_symlink', api['read_regular'], root/'link')
        (root/'link').unlink()
        os.mkfifo(root/'fifo')
        reject('tree_fifo', api['closed_tree'], root, {'a/x','fifo'})
        reject('read_regular_fifo', api['read_regular'], root/'fifo')
        (root/'fifo').unlink()
        reject('read_regular_wrong_size', api['read_regular'], root/'a/x', 1)

    expected = {'bounded.txt': b'Independent raw ZIP control.\n'}
    good = accept('zip_generated_valid', api['deterministic_zip'], expected)
    accept('zip_raw_valid', api['zip_payloads'], good, expected, True)
    assert good == api['deterministic_zip'](expected)
    receipts.append({'case':'zip_same_runtime_bytes','equal':True,'bytes':len(good),'sha256':hashlib.sha256(good).hexdigest()})
    for label, data in [('zip_prefix',b'X'+good),('zip_suffix',good+b'X'),('zip_truncated',good[:-1])]:
        reject(label, api['zip_payloads'], data, expected, True)

    def compressed_suffix(extra):
        data = bytearray(good)
        end = len(data)-22
        central = struct.unpack_from('<I',data,end+16)[0]
        size = struct.unpack_from('<I',data,18)[0]
        data[central:central] = extra
        struct.pack_into('<I',data,18,size+len(extra))
        struct.pack_into('<I',data,central+len(extra)+20,size+len(extra))
        struct.pack_into('<I',data,end+len(extra)+16,central+len(extra))
        return bytes(data)
    compressor = zlib.compressobj(wbits=-15)
    second = compressor.compress(b'another stream') + compressor.flush()
    for label, extra in [('zip_deflate_trailing',b'JUNK'),('zip_deflate_concatenated',second),('zip_deflate_empty_second',b'\x03\x00')]:
        reject(label, api['zip_payloads'], compressed_suffix(extra), expected, True)
    for label, offset in [('zip_local_crc',14),('zip_local_size',22),('zip_local_flags',6)]:
        mutation=bytearray(good);mutation[offset]^=1
        reject(label, api['zip_payloads'], bytes(mutation), expected, True)

    # The boundary defect is reproduced in this helper only. Replay is replaced
    # with a sentinel because this test concerns build_output's path validation;
    # no real package/current wrapper is claimed and no archival code executes.
    build_globals = api['build_output'].__globals__
    original_verify = build_globals['verify_result']
    sentinels = []
    def sentinel_verify(*unused):
        sentinels.append(True)
        return {'status':'HELPER_SENTINEL_NO_ARCHIVAL_CODE'}
    build_globals['verify_result'] = sentinel_verify
    try:
        for label, spelling in [('dotdot_root','dotdot'),('symlink_output_parent','symlink')]:
            with tempfile.TemporaryDirectory(prefix='build-boundary-', dir=HERE) as td:
                base=Path(td); root=base/'input'; root.mkdir(); (base/'spelling').mkdir()
                output=root/'oriented-flow-verification.zip'
                if spelling=='dotdot':
                    input_arg=base/'spelling'/'..'/'input'; output_arg=output
                else:
                    alias=base/'output_alias';alias.symlink_to(root,target_is_directory=True)
                    input_arg=root;output_arg=alias/output.name
                before=len(sentinels)
                reject('build_inside_input_via_'+label,api['build_output'],{'bounded.txt':b'helper only'},'0'*64,
                       types.SimpleNamespace(root=input_arg,output=output_arg,verify_only=False))
                assert not output.exists() and len(sentinels)==before
                receipts[-1].update({'helper_sentinel_not_reached':True,'archival_execution':False,
                                     'archive_created_inside_input':False})
    finally:
        build_globals['verify_result'] = original_verify

    output=HERE/args.output
    assert output.parent == HERE and not output.exists()
    output.write_text(json.dumps({'timestamp_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
                                 'tool_sha256':ASSIGNED,'scope':'Independent bounded helper tests; no archival execution or current-wrapper validation.',
                                 'completion_estimate_percent':45,'receipts':receipts},indent=2,sort_keys=True)+'\n')
    print(json.dumps({'cases':len(receipts),'path_boundary_defects':sum(x.get('unexpected_acceptance',False) for x in receipts),'output':output.name}))


if __name__=='__main__':
    main()
