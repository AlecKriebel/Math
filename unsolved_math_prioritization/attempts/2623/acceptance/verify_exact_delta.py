#!/usr/bin/env python3
"""Check the exact KOU-21.114 v1-to-v2 correction without modifying inputs.

Inputs are the two author ZIPs, supplied delta/patch/receipt/replay, and the
original independent audit directory. Mathematical replay is a separate step.
Uses only the Python standard library. Do not run with Python -O.
"""
import argparse
import ast
import copy
import difflib
import hashlib
import json
from pathlib import Path
import zipfile


def digest(b):
    return hashlib.sha256(b).hexdigest()


def read_zip(path, expected_hash, expected_bytes):
    data=path.read_bytes()
    assert len(data)==expected_bytes and digest(data)==expected_hash,path.name
    with zipfile.ZipFile(path) as z:
        names=z.namelist()
        assert len(names)==9 and len(set(names))==9
        assert all(Path(n).name==n for n in names)
        assert z.testzip() is None
        payload={n:z.read(n) for n in names}
    manifest=json.loads(payload['AUTHOR_MANIFEST.json'])
    assert set(payload)=={x['path'] for x in manifest['files']}|{'AUTHOR_MANIFEST.json'}
    for item in manifest['files']:
        b=payload[item['path']]
        assert len(b)==item['bytes'] and digest(b)==item['sha256']
    return payload,manifest


class RemoveDocstrings(ast.NodeTransformer):
    def visit_Module(self,node):
        self.generic_visit(node)
        if node.body and isinstance(node.body[0],ast.Expr) and isinstance(node.body[0].value,ast.Constant) and isinstance(node.body[0].value.value,str):
            node.body=node.body[1:]
        return node
    visit_ClassDef=visit_Module
    visit_FunctionDef=visit_Module
    visit_AsyncFunctionDef=visit_Module


def functional_ast(data):
    return ast.dump(RemoveDocstrings().visit(ast.parse(data.decode())),include_attributes=False)


def check(inputs,audit):
    v1_hash='d1f66407e8a7ff1c7aceaf7531b959085877de50c4198558d5d69dc33983f0f4'
    v2_hash='897360dd152d57c8d3ac10043fdb28b889e7206509eec56f6cb9a1dadbd71823'
    old,om=read_zip(inputs/'KOUROVKA_2623_AUTHOR_SAFE_FREEZE.zip',v1_hash,21815)
    new,nm=read_zip(inputs/'KOUROVKA_2623_AUTHOR_V2_SAFE_FREEZE.zip',v2_hash,22379)
    assert digest(old['AUTHOR_MANIFEST.json'])=='5a59d7d8e527873107d7fa2ccb0338648efeedfb875eb0e109f39396dcad3a73'
    assert digest(new['AUTHOR_MANIFEST.json'])=='d63ba4c1c9e4183b612ea57580f453421f69d1b86ededbf40b0b5ac79cff63c3'
    correction_bytes=(audit/'CORRECTIONS.json').read_bytes()
    assert digest(correction_bytes)=='9d52bb17e3d9a630e4bbeb95a348369f01bbc12da617a33857f2ac0cc2159576'
    corrections=json.loads(correction_bytes)
    expected=dict(old)
    expected_source=json.loads(old['SOURCE_VERIFICATION.json'])
    operations=[]
    for issue in corrections['required']+corrections['recommended_editorial']:
        for change in issue['changes']:
            operations.append(dict(correction_id=issue['id'],**change))
            if change['operation']=='replace_exact_string':
                before=expected[change['path']].decode()
                assert before.count(change['old'])==1
                expected[change['path']]=before.replace(change['old'],change['new']).encode()
            elif change['operation']=='replace_json_value':
                assert change['path']=='SOURCE_VERIFICATION.json'
                assert expected_source['identity']['earliest_identified_appearance']==change['old']
                expected_source['identity']['earliest_identified_appearance']=change['new']
            elif change['operation']=='append_source_metadata_object':
                assert not any(s['url']==change['new']['url'] for s in expected_source['sources'])
                expected_source['sources'].append(change['new'])
            else:
                raise AssertionError('Unknown correction operation')
    expected['SOURCE_VERIFICATION.json']=(json.dumps(expected_source,indent=2,ensure_ascii=False)+'\n').encode()
    for name in old:
        if name!='AUTHOR_MANIFEST.json':
            assert expected[name]==new[name],name
    expected_manifest=copy.deepcopy(om)
    expected_manifest.update(created_at_utc=nm['created_at_utc'],release_version=2,
        previous_author_archive_sha256=v1_hash,
        previous_author_manifest_sha256=digest(old['AUTHOR_MANIFEST.json']),
        corrections_source_sha256=digest(correction_bytes),applied_corrections=['C1','C2'])
    assert nm['created_at_utc']=='2026-10-05T19:08:32.983173+00:00'
    for item in expected_manifest['files']:
        b=new[item['path']]
        item.update(bytes=len(b),sha256=digest(b))
    assert nm==expected_manifest
    assert new['AUTHOR_MANIFEST.json']==(json.dumps(expected_manifest,indent=2,ensure_ascii=False)+'\n').encode()
    changed=sorted(n for n in old if old[n]!=new[n])
    unchanged=sorted(n for n in old if old[n]==new[n])
    assert changed==['AUTHOR_MANIFEST.json','PROOFS.md','README.md','SOURCE_VERIFICATION.json','verify_math.py']
    assert new['CHECK_RESULTS.json']==old['CHECK_RESULTS.json']
    for name in ('verify_math.py','verify_manifest.py'):
        assert functional_ast(new[name])==functional_ast(old[name])
    delta_bytes=(inputs/'KOUROVKA_2623_V2_DELTA.json').read_bytes()
    assert digest(delta_bytes)=='9450d06903dac34b3be242534f0f3db83573167938a243a6301c2c68adf1ad89'
    delta=json.loads(delta_bytes)
    assert delta['added_files']==delta['removed_files']==[]
    assert delta['changed_files']==changed and delta['unchanged_files']==unchanged
    assert delta['exact_correction_operations']==operations
    assert delta['old_archive_sha256']==v1_hash and delta['new_archive_sha256']==v2_hash
    assert delta['corrections_sha256']==digest(correction_bytes)
    assert len(delta['file_delta'])==9
    ids={'AUTHOR_MANIFEST.json':['manifest_refresh'],'PROOFS.md':['C2'],
         'README.md':['C1'],'SOURCE_VERIFICATION.json':['C1'],'verify_math.py':['C2']}
    for d in delta['file_delta']:
        name=d['path']
        assert d['status']==('changed' if name in changed else 'unchanged')
        assert d['old_bytes']==len(old[name]) and d['new_bytes']==len(new[name])
        assert d['old_sha256']==digest(old[name]) and d['new_sha256']==digest(new[name])
        assert d['correction_ids']==ids.get(name,[])
    patch=''.join(''.join(difflib.unified_diff(old[n].decode().splitlines(True),new[n].decode().splitlines(True),fromfile='v1/'+n,tofile='v2/'+n)) for n in changed).encode()
    assert patch==(inputs/'KOUROVKA_2623_V2_FROM_V1.patch').read_bytes()
    receipt=json.loads((inputs/'KOUROVKA_2623_AUTHOR_V2_FREEZE_RECEIPT.json').read_text())
    for key in ['archive','delta','patch','replay']:
        b=(inputs/receipt[key]).read_bytes()
        assert digest(b)==receipt[key+'_sha256'],key
    assert receipt['archive_bytes']==22379 and receipt['files']==9
    assert receipt['author_manifest_sha256']==digest(new['AUTHOR_MANIFEST.json'])
    assert digest((inputs/'KOUROVKA_2623_AUDIT_SAFE_FREEZE.zip').read_bytes())=='3e2bd48f1686e61f73831c5ddfd95fb7bb87aefad879a18ca1219018d2f6fce0'
    return dict(problem_id=2623,exact_delta='passed',corrections_applied=['C1','C2'],
        original_author_archive_sha256=v1_hash,accepted_v2_archive_sha256=v2_hash,
        accepted_v2_archive_bytes=22379,accepted_v2_manifest_sha256=digest(new['AUTHOR_MANIFEST.json']),
        delta_sha256=digest(delta_bytes),patch_sha256=digest(patch),
        changed_files=changed,unchanged_files=unchanged,added_files=[],removed_files=[],
        only_exact_corrections_and_manifest_refresh=True,
        functional_python_ast_unchanged_after_removing_docstrings=True,
        check_results_byte_identical=True,check_results_sha256=digest(new['CHECK_RESULTS.json']),
        original_author_and_audit_archives_preserved=True,
        problem_result=nm['result'],substantive_approaches=nm['substantive_approaches'],
        historical_pending_strings_preserved=True,remote_writes=False)


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--inputs',type=Path,required=True)
    parser.add_argument('--audit-dir',type=Path,required=True)
    parser.add_argument('--output',type=Path)
    args=parser.parse_args()
    result=check(args.inputs,args.audit_dir)
    payload=json.dumps(result,indent=2)+'\n'
    if args.output:args.output.write_text(payload)
    print(payload)

if __name__=='__main__':main()
