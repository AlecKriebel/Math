#!/usr/bin/env python3
"""Fail-closed, flat-inventory verification of this source-free audit packet."""
import argparse
import ast
import hashlib
import json
from pathlib import Path
import re

EXPECTED_FILES={
    'README.md','REPORT.md','CLAIMS.json','GATE.json','LEDGER.json','SOURCES.json',
    'verify_math.py','verify_packet.py','test_negative_controls.py'
}


def require(condition,message):
    if not condition:
        raise ValueError(message)


def unique_object(pairs):
    out={}
    for k,v in pairs:
        require(k not in out,'duplicate JSON key: '+k)
        out[k]=v
    return out


def read_json(p):
    return json.loads(p.read_text(),object_pairs_hook=unique_object)


def verify(root):
    require(root.is_dir() and not root.is_symlink(),'packet root must be a real directory')
    entries=list(root.iterdir())
    require({p.name for p in entries}==EXPECTED_FILES|{'MANIFEST.json'},'closed file inventory mismatch')
    for p in entries:
        require(not p.is_symlink() and p.is_file(),'only ordinary flat files are allowed: '+p.name)
    manifest=read_json(root/'MANIFEST.json')
    require(set(manifest)=={'schema','problem_id','files'},'manifest key mismatch')
    require(manifest['schema']=='rational-voa-frozen-manifest-v1','manifest schema mismatch')
    require(manifest['problem_id']==30002842,'manifest problem mismatch')
    require(type(manifest['files']) is list,'manifest files must be a list')
    names=[x.get('name') for x in manifest['files']]
    require(len(names)==len(set(names)) and set(names)==EXPECTED_FILES,'manifest file inventory mismatch')
    for x in manifest['files']:
        require(set(x)=={'name','bytes','sha256'},'manifest entry keys mismatch')
        require(type(x['bytes']) is int and x['bytes']>=0,'bad byte count')
        require(type(x['sha256']) is str and re.fullmatch('[0-9a-f]{64}',x['sha256']) is not None,'bad hash format')
        data=(root/x['name']).read_bytes()
        require(len(data)==x['bytes'],'byte count mismatch: '+x['name'])
        require(hashlib.sha256(data).hexdigest()==x['sha256'],'SHA-256 mismatch: '+x['name'])
    for name in ['verify_math.py','verify_packet.py','test_negative_controls.py']:
        tree=ast.parse((root/name).read_text())
        require(not any(isinstance(node,ast.Assert) for node in ast.walk(tree)),'optimization-removable assertion found: '+name)
    claims=read_json(root/'CLAIMS.json')
    scope={'__name__':'packet_math','__file__':str(root/'verify_math.py')}
    exec(compile((root/'verify_math.py').read_bytes(),str(root/'verify_math.py'),'exec'),scope)
    math_results=scope['verify'](claims)
    ledger=read_json(root/'LEDGER.json')
    require(ledger['problem_id']==30002842 and ledger['author_approaches_completed']==5,'ledger identity/count mismatch')
    require(ledger['final_disposition']=='unsolved_partial' and ledger['prior_resolution_accepted'] is False,'ledger overclaim')
    seq=ledger['chronology']
    require([x['sequence'] for x in seq]==list(range(7)),'chronological ledger order mismatch')
    require([x.get('report_section') for x in seq[1:6]]==list('12345'),'approach mapping mismatch')
    require(all(x['full_resolution'] is False for x in seq[1:6]),'approach falsely claims resolution')
    gate=read_json(root/'GATE.json')
    require(gate['result']=='no_substantive_inherited_attempt_found','gate result mismatch')
    require(gate['problem_id']==30002842 and gate['remote_mutations']==0 and gate['queue_mutations']==0,'gate scope mismatch')
    sources=read_json(root/'SOURCES.json')
    pdfs=sources['pdf_sources']
    require({x['id'] for x in pdfs}=={'L','DG','H1','H5','R','Rad','DZ'} and len(pdfs)==7,'source inventory mismatch')
    for x in pdfs:
        require(x['redistributed'] is False,'source redistribution prohibited')
        require(type(x['bytes']) is int and x['bytes']>0,'bad source size')
        require(type(x['pages']) is int and x['pages']>0,'bad PDF page count')
        require(re.fullmatch('[0-9a-f]{64}',x['sha256']) is not None,'bad source fingerprint')
        require(x['url'].startswith('https://'),'non-public source URL')
    require(all(x['contents_included'] is False for x in sources['corpus_fingerprints']),'dataset contents prohibited')
    report=(root/'REPORT.md').read_text()
    for required in ['Approach I:', 'Approach II:', 'Approach III:', 'Approach IV:', 'Approach V:',
                     'No counterexample to the target is claimed.', 'uniform tail', 'quasi-primary', 'Theorem 4.']:
        require(required in report,'report structural/scope marker missing: '+required)
    return {'files_authenticated':len(EXPECTED_FILES),'math':math_results,
            'status':'unsolved_partial','external_sources_retrieved_by_replay':False}


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--root',type=Path,default=Path(__file__).parent)
    args=parser.parse_args()
    print(json.dumps({'ok':True,'result':verify(args.root)},sort_keys=True))


if __name__=='__main__':
    main()
