"""Explicit terminal stage checks; ordinary and optimized Python use exceptions."""
import hashlib
import json
from pathlib import Path, PurePosixPath

def require(ok,message):
    if not ok:raise RuntimeError(message)
def verify_terminal(root):
    def get(name):
        parts=PurePosixPath(name)
        require(name.isascii() and not parts.is_absolute() and '..' not in parts.parts and '\\' not in name,'unsafe terminal path')
        p=root/name
        require(p.is_file() and not p.is_symlink(),'missing regular terminal input: '+name)
        return p.read_bytes()
    def check(row):
        data=get(row['path'])
        require(len(data)==row['bytes'] and hashlib.sha256(data).hexdigest()==row['sha256'],'protected reviewed input changed: '+row['path'])
    state=json.loads(get('CURRENT_REVIEW_STATE.json'))
    require(state['publication_ready'] is True and state['all_issues_resolved'] is True and
            state['published'] is False and state['fresh_whole_package_reviews']==2 and
            state['status']=='TERMINAL_TWO_CLEAN_WHOLE_REVIEWS_ADMINISTRATION', 'terminal ready stage required')
    acceptance=json.loads(get('evidence/FINAL_ACCEPTANCE.json'))
    require(acceptance['fresh_whole_package_reviews']==2 and acceptance['publication_ready'] is True and
            acceptance['published'] is False and acceptance['actionable_issues']==[], 'terminal acceptance differs')
    for row in acceptance['root_adoption_pins']:check(row)
    for family,num,report,counts,status in [('package_01',1,'REPORT.md','finding_counts','PASS_NEW_WHOLE_PACKAGE_REVIEW_01_NO_P0_P3_FINDINGS'),('package_whole_02',2,'REVIEW.md','severity_counts','PASS_NO_ACTIONABLE_FINDINGS_SECOND_FULL_REVIEW')]:
        prefix='evidence/reviews/'+family+'/'
        verdict=json.loads(get(prefix+'VERDICT.json'))
        require(verdict['status']==status and verdict['findings']==[] and
                verdict[counts]=={'P0':0,'P1':0,'P2':0,'P3':0},'terminal review must have zero actionable P0-P3: '+family)
        adoption=json.loads(get('evidence/ROOT_WHOLE_PACKAGE_REVIEW_0'+str(num)+'.json'))
        require(adoption.get('root_entire_report_and_verdict_read',adoption.get('root_complete_report_and_verdict_read')) is True,'root complete review acceptance missing')
        for name,field in [(report,'report_sha256'),('VERDICT.json','verdict_sha256'),('OUTPUT_PINS.json','output_pins_sha256')]:
            require(hashlib.sha256(get(prefix+name)).hexdigest()==adoption[field],'root-adopted review hash differs: '+family+'/'+name)
        if num==2:
            require(adoption['status']=='ADOPT_ZERO_ACTIONABLE_FINDINGS_PENDING_TERMINAL_ADMIN_SEAL' and adoption['mathematics_accepted_unchanged'] is True and adoption['fresh_whole_package_reviews']==2,'root accepted terminal stage missing')
            seal=json.loads(get(prefix+'SEAL.json'))
            for row in seal['pinned_records']:
                check({'path':prefix+row['path'],'bytes':row['bytes'],'sha256':row['sha256']})
    for row in acceptance['protected_package_inputs']:
        if row['path'] in acceptance['external_nonarchive_inputs'] and not (root/row['path']).exists():continue
        check(row)
    originals=json.loads(get('evidence/ROOT_MATH_ACCEPTANCE.json'))['original_files']
    require(len(originals)==9,'original nine-file edition required')
    for row in originals:check({'path':'evidence/'+row['snapshot_path'],'bytes':row['bytes'],'sha256':row['sha256']})
    copies=json.loads(get('EVIDENCE_COPY_MAP.json'))['copies']
    require(len(copies)==acceptance['evidence_copy_count'] and len({r['package_path'] for r in copies})==len(copies),'terminal copy coverage differs')
    for row in copies:check({'path':row['package_path'],'bytes':row['bytes'],'sha256':row['sha256']})
    wrapper=json.loads(get('zenodo_metadata.json'));metadata=json.loads(get('.zenodo.json'))
    require(wrapper=={'metadata':metadata},'exact bare/wrapped metadata differs')
    if (root/'zenodo-deposit.json').exists():
        require(json.loads(get('zenodo-deposit.json'))=={'metadata':metadata,'files':[{'path':'paper/matroid_rank_obstruction.pdf'},{'path':'pr1047_supportkit_v1.0.zip'}]},'exact external deposit metadata/selection differs')
    require(metadata['creators'][0]['orcid']=='0009-0001-9320-500X','ORCID differs')
    return {'fresh_whole_package_reviews':2,'zero_actionable_issues':True,'ready':True,'published':False,'services_hold':'preceding PR1032 priority cursor'}
