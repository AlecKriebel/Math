#!/usr/bin/env python3
"""Optional metadata-only replay with complete locally obtained source inputs."""
from pathlib import Path
import argparse,hashlib,json
ROOT=Path(__file__).resolve().parent

def info(p):
    b=p.read_bytes();return b,{'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def require(value,label):
    if not value:raise ValueError(label)
def main():
    a=argparse.ArgumentParser()
    a.add_argument('--catalog',type=Path,required=True)
    a.add_argument('--problems',type=Path,required=True)
    a.add_argument('--research',type=Path,required=True)
    a.add_argument('--source-dir',type=Path)
    args=a.parse_args()
    expected=json.loads((ROOT/'DATA_AUDIT.json').read_text())
    source=json.loads((ROOT/'SOURCE_AUDIT.json').read_text())
    parsed={}; raw={}
    for name,p in [('catalog.json',args.catalog),('problems.json',args.problems),('research_results.json',args.research)]:
        b,m=info(p);require(m=={k:expected['files'][name][k] for k in m},'Corpus mismatch: '+name)
        raw[name]=b;parsed[name]=json.loads(b)
        require(len(parsed[name])==expected['files'][name]['entries'],'Entry count mismatch')
    p=next(x for x in parsed['problems.json'] if x['id']==30005026)
    c=next(x for x in parsed['catalog.json'] if x['id']=='30005026')
    require(sum(x['problem_number']==p['problem_number'] for x in parsed['problems.json'])==1,'Ambiguous report join')
    r=parsed['research_results.json'].get(p['problem_number'],{})
    statement=hashlib.sha256(p['statement'].encode()).hexdigest()
    review=hashlib.sha256(json.dumps([p,r],sort_keys=True).encode()).hexdigest()
    require(statement==expected['statement_sha256']==c['statement_hash'],'Statement mismatch')
    require(review==expected['review_sha256']==c['review_hash'],'Review mismatch')
    require(r=={} and p['problem_number'] not in parsed['research_results.json'],'Prior report changed')
    b=raw['catalog.json'];blob=hashlib.sha1(f'blob {len(b)}\0'.encode()+b).hexdigest()
    require(blob==expected['catalog_git_blob_sha1'],'Catalog blob mismatch')
    pdf_count=0
    if args.source_dir:
        for s in source['sources']:
            b,m=info(args.source_dir/s['local_filename_for_optional_replay'])
            require(m=={k:s[k] for k in m} and b.startswith(b'%PDF-'),'PDF mismatch: '+s['title'])
            pdf_count+=1
    print(json.dumps({'status':'PASS','full_corpora_verified':3,'source_pdfs_verified':pdf_count,
                     'statement_and_review_hashes_match':True,'joined_prior_report_empty':True,
                     'raw_source_content_emitted':False},indent=2,sort_keys=True))
if __name__=='__main__':main()
