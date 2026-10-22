#!/usr/bin/env python3
"""Replay exact artifact integrity, optional source/corpus pins, and finite diagnostics.
No computational check certifies a contact-topology theorem or the general conjecture.
The external audit manifest SHA-256 must be supplied from a trusted acceptance receipt.
"""
import argparse
import hashlib
import io
import json
import pathlib
import stat
import subprocess
import sys
import tempfile

AUTHOR_ZIP = (11598, 'c19623ac22f119bf828875af3cb961e04c2d5679ddd7aa8dcdfdd135416e446a')
AUTHOR_MANIFEST = (1322, 'be3be60e6fe3d89f6642a36f479160e783a5a0d062e450e47e2a3b8072ec8213')
AUTHOR_NAMES = {'APPROACHES.md','REPORT.md','STATUS.json','VALIDATION_RESULTS.json','VERIFICATION_METADATA.json','verify_bundle.py'}
AUDIT_NAMES = {'AUTHOR_SAFE_FREEZE.zip','AUTHOR_EXTERNAL_MANIFEST.json','AUDIT_REPORT.md','INPUT_CHECKS.json','SOURCE_CHECKS.json','REPLAY_RESULTS.json','ACCEPTANCE.json','README.md','verify_acceptance.py'}

def require(condition, message):
    if not condition:
        raise ValueError(message)

def sha(blob):
    return hashlib.sha256(blob).hexdigest()

def read_regular(path):
    require(not path.is_symlink() and path.is_file(), 'not a regular nonsymlink file: '+path.name)
    return path.read_bytes()

def load(blob):
    def pairs(items):
        obj = {}
        for key, value in items:
            require(key not in obj, 'duplicate JSON key')
            obj[key] = value
        return obj
    def invalid(value):
        raise ValueError('nonfinite JSON value: '+value)
    return json.loads(blob.decode('utf-8'), object_pairs_hook=pairs, parse_constant=invalid)

def pin(path, expected):
    blob = read_regular(path)
    require((len(blob),sha(blob)) == expected, 'pin mismatch: '+path.name)
    return blob

def manifest_members(manifest, names):
    require(type(manifest) is dict and type(manifest.get('schema')) is int and manifest['schema']==1 and type(manifest.get('problem_id')) is int and manifest['problem_id']==2839, 'manifest identity')
    entries=manifest.get('members')
    require(type(entries) is list and len(entries)==len(names), 'member count')
    require(all(type(e) is dict and set(e)=={'path','bytes','sha256'} for e in entries), 'member fields')
    require(all(type(e['path']) is str and type(e['bytes']) is int and e['bytes']>=0 and type(e['sha256']) is str and len(e['sha256'])==64 and all(c in '0123456789abcdef' for c in e['sha256']) for e in entries), 'member types')
    require({e['path'] for e in entries}==names and len({e['path'] for e in entries})==len(entries), 'member names')
    return {e['path']:e for e in entries}

def check(args):
    import zipfile
    root=args.root.resolve()
    require(not args.root.is_symlink() and root.is_dir(), 'root directory')
    require(len(args.manifest_sha256)==64 and all(c in '0123456789abcdef' for c in args.manifest_sha256), 'trusted manifest digest required')
    mb=read_regular(args.manifest)
    require(sha(mb)==args.manifest_sha256, 'audit manifest hash mismatch')
    audit=load(mb); entries=manifest_members(audit,AUDIT_NAMES)
    require({p.name for p in root.iterdir()}==AUDIT_NAMES, 'audit root membership')
    for name,e in entries.items():pin(root/name,(e['bytes'],e['sha256']))
    az=pin(root/'AUTHOR_SAFE_FREEZE.zip',AUTHOR_ZIP)
    am=load(pin(root/'AUTHOR_EXTERNAL_MANIFEST.json',AUTHOR_MANIFEST))
    members=manifest_members(am,AUTHOR_NAMES)
    require(am.get('archive')=={'path':'LARGE_SLOPE_CONTACT_SURGERY_2839_AUTHOR_SAFE_FREEZE.zip','bytes':AUTHOR_ZIP[0],'sha256':AUTHOR_ZIP[1]},'author archive metadata')
    author={}
    with zipfile.ZipFile(io.BytesIO(az)) as z:
        infos=z.infolist()
        require(len(infos)==len(AUTHOR_NAMES) and {i.filename for i in infos}==AUTHOR_NAMES,'ZIP membership')
        require(z.testzip() is None,'ZIP CRC failure')
        for i in infos:
            require(not i.is_dir() and not stat.S_ISLNK(i.external_attr>>16) and not i.flag_bits&1,'ZIP member type')
            require(i.file_size==members[i.filename]['bytes'],'ZIP expanded size')
            b=z.read(i.filename);e=members[i.filename]
            require((len(b),sha(b))==(e['bytes'],e['sha256']),'ZIP member pin')
            author[i.filename]=b
    if args.author_root:
        require(not args.author_root.is_symlink() and args.author_root.is_dir(),'author root')
        require({p.name for p in args.author_root.iterdir()}==AUTHOR_NAMES,'author root membership')
        for name,e in members.items():pin(args.author_root/name,(e['bytes'],e['sha256']))
    result={'ok':True,'problem_id':2839,'author_members':6,'audit_members':9,'optimization':sys.flags.optimize,'scope':'exact-byte artifact acceptance and finite arithmetic only; no geometry theorem certification','corpora':'not rechecked in this invocation','source_pdfs':'not rechecked in this invocation','author_checker':[]}
    corpus=[args.catalog,args.problems,args.reports]
    require(all(corpus) or not any(corpus),'supply all three corpus inputs or none')
    if all(corpus):
        expected=load(read_regular(root/'INPUT_CHECKS.json'))
        data=[]
        for p,e in zip(corpus,expected['full_corpora']):data.append(load(pin(p,(e['bytes'],e['sha256']))))
        cats,probs,reports=data
        require(type(cats) is list and type(probs) is list and type(reports) is dict,'corpus types')
        c=[x for x in cats if x.get('id')=='2839'];p=[x for x in probs if x.get('id')==2839]
        require(len(c)==len(p)==1,'unique corpus match')
        c,p=c[0],p[0]
        require(c['rank']==913 and p['problem_number']==c['problem_number']=='KP-3.41','corpus identity')
        sr=sha(p['statement'].encode());rr=reports.get(p['problem_number'],{})
        pair=sha(json.dumps([p,rr],sort_keys=True).encode())
        require(sr==expected['statement_sha256']==c['statement_hash'],'statement pin')
        require(pair==expected['complete_record_report_pair_sha256']==c['review_hash'],'complete pair pin')
        require(rr=={},'inherited report not empty')
        result['corpora']='all three entire files and complete target pair verified'
    if args.source_dir:
        sources=load(read_regular(root/'SOURCE_CHECKS.json'))['sources']
        for e in sources:pin(args.source_dir/e['file_label'],(e['bytes'],e['sha256']))
        result['source_pdfs']='all seven entire PDF files verified; this does not prove provenance or mathematical correctness'
    with tempfile.TemporaryDirectory(prefix='contact-2839-') as td:
        base=pathlib.Path(td);target=base/'author';target.mkdir(); manifest=base/'author-manifest.json';manifest.write_bytes(read_regular(root/'AUTHOR_EXTERNAL_MANIFEST.json'))
        for name,b in author.items():(target/name).write_bytes(b)
        for opt in ([],['-O'],['-OO']):
            run=subprocess.run([sys.executable,*opt,str(target/'verify_bundle.py'),'--root',str(target),'--manifest',str(manifest)],cwd=base,capture_output=True,text=True,timeout=30)
            require(run.returncode==0,'author checker failed: '+run.stderr)
            out=load(run.stdout.encode())
            require(out['ok'] is True and out['stabilization_examples']==4356,'author diagnostics result')
            result['author_checker'].append({'optimization':len(opt[0])-1 if opt else 0,'ok':True,'stabilization_examples':4356})
    return result

if __name__=='__main__':
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--root',type=pathlib.Path,required=True)
    ap.add_argument('--manifest',type=pathlib.Path,required=True)
    ap.add_argument('--manifest-sha256',required=True)
    ap.add_argument('--author-root',type=pathlib.Path)
    ap.add_argument('--catalog',type=pathlib.Path)
    ap.add_argument('--problems',type=pathlib.Path)
    ap.add_argument('--reports',type=pathlib.Path)
    ap.add_argument('--source-dir',type=pathlib.Path)
    args=ap.parse_args()
    try:print(json.dumps(check(args),sort_keys=True))
    except Exception as exc:
        print(json.dumps({'ok':False,'error':str(exc)},sort_keys=True),file=sys.stderr)
        sys.exit(1)
