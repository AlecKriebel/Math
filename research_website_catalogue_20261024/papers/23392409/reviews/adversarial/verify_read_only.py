"""Pure offline custody only: no scientific program imports, controls or network.

Authenticate the sealed local packet, all original source bytes, the two early
freezes, and literal bound native JSON objects. Do not recompute mathematics.
"""
from pathlib import Path
import argparse
import hashlib
import json
import platform
import sys


def literal(value):
    return json.dumps(value,ensure_ascii=False,separators=(',',':'),allow_nan=False)


def verify(root):
    root=Path(root).resolve();checks=0
    def need(ok,why):
        nonlocal checks
        checks+=1
        if not ok:raise ValueError(why)
    def sha(raw):return hashlib.sha256(raw).hexdigest()
    def file(path,size,digest):
        path=Path(path);need(path.is_file() and not path.is_symlink(),'regular file '+str(path));raw=path.read_bytes();need(len(raw)==size,'size '+str(path));need(sha(raw)==digest,'SHA256 '+str(path));return raw
    raw=(root/'OWNED_MANIFEST.json').read_bytes();owned=json.loads(raw);seal=json.loads((root/'FINAL_SEAL.json').read_bytes());need(sha(raw)==seal['OWNED_MANIFEST_SHA256'],'final manifest seal');need(len(raw)==seal['OWNED_MANIFEST_bytes'],'manifest byte length')
    rows=owned['files'];names=[x['path'] for x in rows];need(len(names)==len(set(names)),'unique owned files');need(all(not Path(n).is_absolute() and '..' not in Path(n).parts for n in names),'relative owned paths')
    actual=sorted(str(p.relative_to(root)) for p in root.rglob('*') if p.is_file());need(actual==sorted(names+['OWNED_MANIFEST.json','FINAL_SEAL.json']),'complete owned namespace');need(not any(p.is_symlink() for p in root.rglob('*')),'no owned symlinks')
    for row in rows:file(root/row['path'],row['bytes'],row['SHA256'])
    need(len(rows)==seal['owned_payloads'],'owned count')
    source=json.loads((root/'SOURCE_INPUTS.json').read_bytes());source_root=Path(source['source_root'])
    for row in source['files']:file(row['path'],row['bytes'],row['SHA256'])
    need(sorted(str(p.relative_to(source_root)) for p in source_root.rglob('*') if p.is_file())==source['source_namespace'],'original121 source namespace')
    need(sha((source_root/'SOURCE_READY.json').read_bytes())=='388fbf673c3f14886f9da3628be04a1f7c019b0d6d1c6c936fb084d8a245d972','original READY authority')
    need(sha((source_root/'SOURCE_READY_SEAL.json').read_bytes())=='0b056ecf4a219a11f44b0461de41b1ba80320b950323b17e6f1e52ebd45a64bc','original source seal authority')
    for manifest_name,seal_name,key in [('INITIAL_MANIFEST.json','INITIAL_SEAL.json','INITIAL_MANIFEST_SHA256'),('OWN_PROOF_RESULTS_MANIFEST.json','OWN_PROOF_RESULTS_SEAL.json','manifest_SHA256')]:
        mraw=(root/manifest_name).read_bytes();s=json.loads((root/seal_name).read_bytes());need(sha(mraw)==s[key],'early immutable seal '+seal_name)
        for row in json.loads(mraw)['files']:file(root/row['path'],row['bytes'],row['SHA256'])
    wrapper_count=0
    def wrappers(value):
        nonlocal wrapper_count
        if isinstance(value,dict):
            if {'path','bytes','SHA256','whole_literal_object'}<=set(value):
                raw=file(value['path'],value['bytes'],value['SHA256']);need(literal(json.loads(raw))==literal(value['whole_literal_object']),'whole native types/key/list/header order/nulls');wrapper_count+=1
            for child in value.values():wrappers(child)
        elif isinstance(value,list):
            for child in value:wrappers(child)
    bundle=json.loads((root/'NATIVE_OBJECT_BINDINGS.json').read_bytes());wrappers(bundle)
    verdict=json.loads((root/'VERDICT.json').read_bytes());need(literal(verdict['whole_original_SOURCE_READY_object'])==literal(json.loads((source_root/'SOURCE_READY.json').read_bytes())),'verdict retains whole historical READY')
    for a in bundle['whole_original_native_API_objects']:
        if a['role'] in ['record','latest']:need('version' not in a['whole_literal_object']['metadata'],'native version key genuinely absent')
    need(bundle['whole_original_SOURCE_READY']['whole_literal_object']['version_field_present'] is False,'absent native version not invented')
    native=json.loads((root/'NATIVE_ISOLATION.json').read_bytes());need(len(native['payloads'])==64,'whole64 original ZIP payloads')
    for row in native['payloads']:file(root/'native-isolated'/row['relative_path'],row['bytes'],row['SHA256'])
    rules=(root/'.gitignore').read_text().splitlines();need('/cache/primary/' in rules and '/native-isolated/' in rules,'private raw-body boundary')
    return {'status':'PASS','scope':'Pure offline custody; no mathematical/native replay, controls, network or writes.','python':platform.python_version(),'optimized':not __debug__,'checks':checks,'owned_payloads':len(rows),'original_source_files':len(source['files']),'whole_native_JSON_wrappers':wrapper_count,'unchanged_isolated_native_payloads':64,'both_early_scientific_freezes_authenticated':True,'native_version_field_present':False,'private_ignored_bodies_still_locally_authenticated':True,'scientific_adoption_or_publication_authority_claim':False}


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--packet-root',required=True);args=parser.parse_args()
    try:result=verify(args.packet_root)
    except Exception as error:print(json.dumps({'status':'FAIL','error':str(error)},indent=2));sys.exit(1)
    print(json.dumps(result,indent=2))


if __name__=='__main__':main()
