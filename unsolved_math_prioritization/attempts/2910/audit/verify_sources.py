#!/usr/bin/env python3
"""Read-only full-byte and exact-record verification. Prints metadata only."""
import argparse,hashlib,json,sys
from pathlib import Path
PINS={
'catalog.json':(21735099,'891938878f1e395de77f6829d5d5d13cb5d5393f85efaa7941fb14bd3e3d7566'),
'problems.json':(68931837,'04128381e42a5e312326d74adb0947ee02062ade70229e02d3060ac4ef9942cf'),
'research_results.json':(80334822,'8da848d31c20eb4eecaa07702eced4724aa4a89f877c2a0774d9f3138389aa6b'),
'k3.pdf':(6578041,'ae56518166fe38aaaf555c58614329228afe734e743b111badec4060877fa12f'),
'larson_v2.pdf':(605334,'5fb0bc92edf2729070f25276e1ed8d32a4bdf84716afe32f6cea8d2032521d62'),
'larson_meier_v2.pdf':(451614,'b20627fd97de37a1231bec40230bb4c81d34f2f5e757092a69eb5b0a11b8f5b4'),
'baykur_sunukjian_v3.pdf':(250737,'6de2ef88203a17bb1a175569e26583163ce7233349dfffa70caccd49c7cc14a5')}
PAIR='56eb2b6965848c89fd7f16e3433f3dafb39fb9bf861d801378dfed904b6dcbbd'
STATEMENT='fd75cc9ba9ad9e919960a0d2e05a139e751ebc24cb1f9e0cc599ce8094eb5dd4'
def require(x,m):
    if not x:raise ValueError(m)
def sha(x):return hashlib.sha256(x).hexdigest()
def main():
    p=argparse.ArgumentParser();p.add_argument('catalog');p.add_argument('problems');p.add_argument('reports');p.add_argument('pdf_directory');a=p.parse_args()
    paths={'catalog.json':Path(a.catalog),'problems.json':Path(a.problems),'research_results.json':Path(a.reports)}
    paths.update({n:Path(a.pdf_directory)/n for n in PINS if n.endswith('.pdf')})
    out=[];data={}
    for n,f in paths.items():
        require(f.is_file() and not f.is_symlink(),'missing or unsafe source '+n);b=f.read_bytes();pin=(len(b),sha(b));require(pin==PINS[n],'source mismatch '+n)
        out.append({'logical_name':n,'bytes':pin[0],'sha256':pin[1],'match':True})
        if n.endswith('.json'):data[n]=json.loads(b)
    cat=[x for x in data['catalog.json'] if str(x.get('id'))=='2910'];rows=[x for x in data['problems.json'] if str(x.get('id'))=='2910']
    require(len(cat)==len(rows)==1,'exact-ID uniqueness');cat=cat[0];record=rows[0]
    require(cat['rank']==918 and cat['problem_number']==record['problem_number']=='KP-4.34','identity/rank')
    report=data['research_results.json'].get(record['problem_number'],{})
    pair=sha(json.dumps([record,report],sort_keys=True).encode());statement=sha(record['statement'].encode())
    require(pair==PAIR==cat['review_hash'] and statement==STATEMENT==cat['statement_hash'],'exact complete pair')
    require(report=={},'nonempty inherited report')
    return {'result':'pass','problem_id':2910,'rank':918,'pins':out,'complete_record_report_pair_sha256':pair,'statement_sha256':statement,'pair_serialization':'json.dumps([complete_problem_record, report_or_empty_object], sort_keys=True), Python defaults, UTF-8','inherited_report_key_present':record['problem_number'] in data['research_results.json'],'inherited_report_empty':True,'catalog_records':len(data['catalog.json']),'problem_records':len(data['problems.json']),'copied_source_content_emitted':False}
if __name__=='__main__':
    try:print(json.dumps(main(),sort_keys=True))
    except Exception as e:print(json.dumps({'result':'fail','error':str(e)}),file=sys.stderr);sys.exit(1)
