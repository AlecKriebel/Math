#!/usr/bin/env python3
"""Optional exact-byte and full-corpus checks. Never fetches or distributes source contents."""
import argparse
import hashlib
import json
from pathlib import Path
import stat
import sys

class SourceError(Exception):
    pass

def require(condition, message):
    if not condition:
        raise SourceError(message)

def pairs(values):
    out={}
    for key,value in values:
        require(key not in out,'duplicate JSON key')
        out[key]=value
    return out

def check(path, entry):
    require(path.exists() and stat.S_ISREG(path.lstat().st_mode),'missing or nonregular source: '+path.name)
    raw=path.read_bytes()
    require(len(raw)==entry['bytes'],'source size mismatch: '+path.name)
    require(hashlib.sha256(raw).hexdigest()==entry['sha256'],'source hash mismatch: '+path.name)
    return raw

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--pdf-dir',type=Path)
    parser.add_argument('--corpus-dir',type=Path)
    args=parser.parse_args()
    try:
        data=json.loads((Path(__file__).resolve().parent/'SOURCE_METADATA.json').read_text(),object_pairs_hook=pairs)
        outputs=[]
        for kind,root in [('pdfs',args.pdf_dir),('corpora',args.corpus_dir)]:
            if root is None:
                outputs.append({'kind':kind,'status':'NOT_RUN: no source directory supplied'})
                continue
            checks=[]
            for entry in data[kind]:
                raw=check(root/entry['filename'],entry)
                extra={}
                if kind=='corpora':
                    parsed=json.loads(raw,object_pairs_hook=pairs)
                    if entry['filename']=='problems.json':
                        require(isinstance(parsed,list),'problem corpus shape')
                        targets=[r for r in parsed if isinstance(r,dict) and r.get('id')==30003081]
                        require(len(targets)==1 and targets[0].get('problem_number')=='OWR-14222-009','exact target identity')
                        extra={'records':len(parsed),'exact_target_matches':len(targets)}
                    else:
                        require(isinstance(parsed,dict),'research corpus shape')
                        require('OWR-14222-009' not in parsed,'new exact-target research record')
                        extra={'top_level_records':len(parsed),'exact_target_key_present':False}
                checks.append({'filename':entry['filename'],'bytes':len(raw),'sha256':entry['sha256'],'match':True,**extra})
            outputs.append({'kind':kind,'status':'PASS','checks':checks})
        print(json.dumps({'status':'PASS_REQUESTED_CHECKS' if args.pdf_dir or args.corpus_dir else 'NOT_RUN',
                          'checks':outputs,'scope':'Byte authentication and exact corpus identity only; reading mathematical content is a separate manual audit.'},indent=2,sort_keys=True))
    except (SourceError,OSError,ValueError,TypeError,KeyError) as error:
        print('REJECT: '+str(error),file=sys.stderr)
        return 1
    return 0

if __name__=='__main__':
    sys.exit(main())
