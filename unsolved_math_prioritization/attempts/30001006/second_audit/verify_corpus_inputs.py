#!/usr/bin/env python3
"""Optional exact replay using separately supplied complete corpora. Prints metadata only."""
import argparse,hashlib,json,pathlib


def need(ok,message):
    if not ok: raise RuntimeError(message)


def main():
    p=argparse.ArgumentParser()
    for key in ['catalog','problems','reports']:p.add_argument('--'+key,required=True)
    a=p.parse_args();root=pathlib.Path(__file__).resolve().parent
    expected=json.loads((root/'FRESH_CORPUS_VERIFICATION.json').read_text())
    objects=[]
    for path,meta in zip([a.catalog,a.problems,a.reports],expected['full_corpora']):
        raw=pathlib.Path(path).read_bytes()
        need(len(raw)==meta['bytes'],'corpus size mismatch: '+meta['filename'])
        need(hashlib.sha256(raw).hexdigest()==meta['sha256'],'corpus hash mismatch: '+meta['filename'])
        obj=json.loads(raw);need(len(obj)==meta['parsed_records'],'corpus count mismatch');objects.append(obj)
    catalog,problems,reports=objects
    rows=[x for x in catalog if str(x['id'])=='30001006'];records=[x for x in problems if str(x['id'])=='30001006']
    need(len(rows)==len(records)==1,'target ID count mismatch')
    row,record=rows[0],records[0]
    need(row['rank']==817 and row['problem_number']==record['problem_number']=='OWR-2045-003','target identity mismatch')
    need(isinstance(row['id'],str) and isinstance(record['id'],int),'ID type mismatch')
    need(record['problem_number'] not in reports,'expected report absence changed')
    raw=json.dumps([record,reports.get(record['problem_number'],{})],sort_keys=True).encode()
    review=expected['record_review'];digest=hashlib.sha256(raw).hexdigest()
    need(len(raw)==review['bytes'] and digest==review['sha256']==row['review_hash'],'review serialization mismatch')
    print(json.dumps({'status':'PASS','full_corpus_hashes_and_counts':'MATCH','target_record_serialization':'MATCH','record_review_sha256':digest,'record_review_bytes':len(raw),'dataset_contents_printed':False},sort_keys=True))

if __name__=='__main__':main()
