#!/usr/bin/env python3
"""Optional offline hash replay for separately supplied private reading inputs."""
import argparse
import hashlib
import json
from pathlib import Path
import sys

def need(ok,msg):
    if not ok:raise ValueError(msg)
def pairs(items):
    d={}
    for k,v in items:
        need(k not in d,'duplicate JSON key');d[k]=v
    return d
def no_constant(c):raise ValueError('nonfinite JSON constant')
def read(p):
    need(p.is_file() and not p.is_symlink(),'nonregular input: '+p.name);return p.read_bytes()
def load(b):return json.loads(b.decode('utf-8'),object_pairs_hook=pairs,parse_constant=no_constant)
def sha(b):return hashlib.sha256(b).hexdigest()
def canon(x):return json.dumps(x,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()
def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--sources',type=Path,required=True);ap.add_argument('--corpora',type=Path,required=True);args=ap.parse_args();root=Path(__file__).resolve().parent
    pins=load(read(root/'SOURCE_PINS.json'));binding=load(read(root/'CORPUS_BINDINGS.json'));matched=0
    for pin in pins['sources']:
        b=read(args.sources/pin['filename']);need(len(b)==pin['bytes'] and sha(b)==pin['sha256'],'source hash mismatch: '+pin['filename']);matched+=1
    loaded={}
    for pin in binding['corpora']:
        b=read(args.corpora/pin['filename']);need(len(b)==pin['bytes'] and sha(b)==pin['sha256'],'corpus hash mismatch: '+pin['filename']);obj=load(b);need(len(obj)==pin['record_count'],'record count mismatch');loaded[pin['filename']]=obj
    found=[r for r in loaded['problems.json'] if type(r.get('id')) is int and r['id']==10300043];need(len(found)==1,'target multiplicity');p=found[0];r=loaded['research_results.json']['AMR-102-0043'];need(p['problem_number']=='AMR-102-0043','code mismatch')
    for value,key in [(p,'selected_problem_sha256'),(r,'selected_research_sha256'),({'problem':p,'research':r},'selected_pair_sha256')]:need(sha(canon(value))==binding[key],'record binding mismatch')
    print(json.dumps({'status':'PASS_OFFLINE_INPUT_PINS','sources_matched':matched,'corpora_matched':2,'unique_record_report_pair':True,'source_text_distributed':False,'mathematical_source_proofs_certified':False},sort_keys=True))
if __name__=='__main__':
    try:main()
    except (ValueError,TypeError,KeyError,UnicodeError,OSError) as e:print('FAIL: '+str(e),file=sys.stderr);sys.exit(2)
