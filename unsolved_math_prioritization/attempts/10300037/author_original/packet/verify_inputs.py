#!/usr/bin/env python3
"""Optional read-only check of separately held source and corpus bytes."""
from pathlib import Path
import hashlib,json,sys
class VerificationError(Exception):pass
def require(ok,msg):
    if not ok:raise VerificationError(msg)
def pairs(items):
    d={}
    for k,v in items:
        require(k not in d,'duplicate key');d[k]=v
    return d
def readjson(b):
    def bad(v):raise VerificationError('nonfinite JSON constant')
    return json.loads(b,object_pairs_hook=pairs,parse_constant=bad)
def sha(b):return hashlib.sha256(b).hexdigest()
def check(p,pin):
    require(p.is_file() and not p.is_symlink(),'missing or symlink input '+p.name)
    b=p.read_bytes();require(len(b)==pin['bytes'] and sha(b)==pin['sha256'],'input mismatch '+p.name);return b

def run():
    require(len(sys.argv)==3,'usage: verify_inputs.py SOURCE_DIRECTORY CORPUS_DIRECTORY')
    src=Path(sys.argv[1]);corpus=Path(sys.argv[2]);root=Path(__file__).resolve().parent
    source=readjson((root/'SOURCE_PINS.json').read_bytes());inputs=readjson((root/'CORPUS_BINDINGS.json').read_bytes())
    require(source['schema']=='even-sided-source-pins-v1','source schema')
    require(inputs['schema']=='even-sided-corpus-bindings-v1' and inputs['problem_id']==10300037,'corpus schema')
    checked=[]
    for e in source['sources']:
        require(type(e['id']) is str and '/' not in e['id'] and '\\' not in e['id'],'unsafe source id')
        b=check(src/(e['id']+'.pdf'),e['pdf']);require(b.startswith(b'%PDF'),'not a PDF')
        check(src/(e['id']+'.txt'),e['text_extraction']);checked.append(e['id'])
    selected=[]
    for e in inputs['inputs']:
        require(e['name'] in ('problems.json','research_results.json'),'unexpected corpus')
        b=check(corpus/e['name'],e);d=readjson(b);require(len(d)==e['record_count'],'record count')
        if e['name']=='problems.json':
            require(type(d) is list,'problem list schema')
            rs=[r for r in d if type(r) is dict and type(r.get('id')) is int and r['id']==10300037]
            require(len(rs)==1,'nonunique matching problem');r=rs[0]
            require(r['problem_number']=='AMR-102-0037','problem code')
        else:
            require(type(d) is dict and 'AMR-102-0037' in d,'research schema');r=d['AMR-102-0037']
        b=json.dumps(r,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()
        require(len(b)==e['canonical_selected_bytes'] and sha(b)==e['canonical_selected_sha256'],'selected record mismatch')
        selected.append(e['name'])
    require(set(selected)=={'problems.json','research_results.json'},'missing corpus')
    return {'schema':'even-sided-private-input-replay-v1','status':'pass','pdfs_and_extractions':len(checked),'corpora':len(selected),'matched_records':2,'source_free_packet':True,'qualification':'Existing local bytes checked; no new HTTP retrieval or independent source proof audit.'}
if __name__=='__main__':
    try:print(json.dumps(run(),sort_keys=True,separators=(',',':')))
    except (VerificationError,OSError,ValueError,KeyError,TypeError) as e:
        print('REJECT: '+str(e),file=sys.stderr);sys.exit(1)
