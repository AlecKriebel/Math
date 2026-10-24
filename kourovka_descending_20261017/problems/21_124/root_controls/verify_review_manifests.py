#!/usr/bin/env python3
"""Check exact current input/output bytes of restricted, independently reviewed claims."""
from pathlib import Path
import hashlib,json,datetime
BASE=Path(__file__).resolve().parent.parent

def main():
    results=[]; receipts=[]
    correction=json.loads((BASE/'COMMENT_CORRECTION_RECEIPT.json').read_text())
    def check(path,wanted,origin):
        p=BASE/path;actual=hashlib.sha256(p.read_bytes()).hexdigest()
        editorial=(str(path)=='tubular/check_abelian_holonomy.py' and wanted==correction['old_sha256'] and actual==correction['new_sha256'] and correction['python_AST_unchanged'])
        assert actual==wanted or editorial, (origin,str(path),wanted,actual)
        results.append({'path':str(path),'sha256':actual,'review_receipt':origin,'matches_frozen_hash':actual==wanted,'accepted_AST_identical_comment_delta':editorial})
    def mapping(d,prefix,origin):
        for name,value in d.items():
            h=value.get('sha256') if isinstance(value,dict) else value
            if isinstance(h,str) and len(h)==64:check(prefix/name,h,origin)
    configurations=[
      ('root_controls_review',[('input_sha256',''),('artifacts_sha256','root_controls_review')]),
      ('theta_review',[('input_sha256','tubular')]),
      ('abelian_holonomy_review',[('author_sha256','tubular'),('review_sha256','abelian_holonomy_review')]),
      ('negative_review',[('inputs',''),('outputs','negative_review')]),
      ('one_twist_review',[('reviewed_files','positive_hierarchy'),('review_artifact_sha256','one_twist_review')]),
      ('flats_review',[('input_sha256',''),('output_sha256','flats_review')]),
      ('dihedral_review',[('input_sha256',''),('review_files_sha256','dihedral_review')]),
      ('height_envelope_review',[('input_sha256',''),('review_output_sha256','height_envelope_review')]),
      ('pell_positive_review',[('input_sha256',''),('output_sha256','pell_positive_review')]),
      ('height_positive_review',[('input_sha256',''),('review_files_sha256','height_positive_review')]),
      ('smoothing_review',[('input_sha256',''),('review_output_sha256','smoothing_review')]),
    ]
    for folder,fields in configurations:
        origin=folder+'/RECEIPT.json';p=BASE/origin;d=json.loads(p.read_text());receipts.append({'path':origin,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
        for field,prefix in fields:mapping(d[field],Path(prefix),origin)
        if folder=='theta_review':
            check(Path(folder)/'independent_check.py',d['independent_check_sha256'],origin);check(Path(folder)/'independent_results.json',d['independent_results_sha256'],origin)
    for folder in ['retraction_review','regular_reduction_review']:
        origin=folder+'/RECEIPT.json';p=BASE/origin;d=json.loads(p.read_text());receipts.append({'path':origin,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
        for field in ['inputs','outputs']:
            for item in d[field]:check(Path(item['path']),item['sha256'],origin)
    out={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'all_current_hash_checks_passed':True,'checks':results,'receipts':receipts,'scope':'Exact byte verification of frozen restricted reviews, not independent proof or originality certification. Complete21.124 remains unproved.'}
    (BASE/'ROOT_MANIFEST_VERIFICATION.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'status':'PASS','checks':len(results),'receipts':len(receipts)}))
if __name__=='__main__':main()
