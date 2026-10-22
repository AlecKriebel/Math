#!/usr/bin/env python3
"""Direct old/new operative predicates; no service or Git operation is made."""
from pathlib import Path
import hashlib,json,runpy
F=Path(__file__).resolve().parent
A=F.parents[1]
OLD=A/'reviews/workflow_tooling'
def need(value,message):
    if not value:raise RuntimeError(message)
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def main():
    manifest=OLD/'MANIFEST.json'
    need(sha(manifest)=='f516d2ca9a3a5830c99d201694edeab9fdfac6b2f5e6787607805b593b5b26b4','Initial workflow seal drift')
    obj=json.loads(manifest.read_text())
    for item in obj['authored_files']:
        path=OLD/item['path']
        need(not path.is_symlink() and path.stat().st_size==item['bytes'] and sha(path)==item['sha256'],'Initial sealed member drift '+item['path'])
    old_path=OLD/'deployed/publication/append_tracker.py';new_path=A/'publication/append_tracker.py'
    old=runpy.run_path(str(old_path))['row_has_problem_identity']
    new=runpy.run_path(str(new_path))['row_has_problem_identity']
    regression=runpy.run_path(str(A/'publication/workflow_regression.py'))
    accepted=regression['ALIAS_VARIANTS'];rejected=regression['ALIAS_NEAR_COLLISIONS']
    pub={'doi':'10.5281/zenodo.123','doi_url':'https://doi.org/10.5281/zenodo.123'}
    cases=[]
    for label,identity in {**accepted,**rejected,'prose':'Hayman-Lingham (AMR-022-7072), target problem'}.items():
        for column in range(4):
            row=['','','',''];row[column]=identity;before=old(row,pub);after=new(row,pub)
            need(after==(label not in rejected),'New direct alias control failed '+label)
            cases.append({'identity':label,'cell':column,'text':identity,'old_recognized':before,'new_recognized':after})
    for identity in ['2307072','https://github.com/AlecKriebel/Math/pull/1274',' 10.5281/zenodo.123 ',' HTTPS://DOI.ORG/10.5281/ZENODO.123 ']:
        for column in range(4):
            row=['','','',''];row[column]=identity;need(old(row,pub) and new(row,pub),'Previously supported numeric/PR/known DOI behavior changed')
            cases.append({'identity':'existing_supported','cell':column,'text':identity,'old_recognized':True,'new_recognized':True})
    sample=['','','','AMR-022-7072']
    need(old(sample,pub) is False and new(sample,pub) is True,'Canonical motivating case not reproduced')
    trailing=['AMR02270729','','','']
    need(old(trailing,pub) is True and new(trailing,pub) is False,'Longer compact alias false positive not reproduced/fixed')
    print(json.dumps({'status':'PASS','initial_workflow_manifest_sha256':sha(manifest),'initial_sealed_members_unchanged':len(obj['authored_files']),'old_append_sha256':sha(old_path),'new_append_sha256':sha(new_path),'motivating_case':{'row':sample,'before':False,'after':True},'longer_alias_case':{'row':trailing,'before':True,'after':False},'accepted_alias_spellings':accepted,'rejected_near_collisions':rejected,'cases':cases,'limits':'Direct string identity recognition only. Actual action-time service/Git paths are exercised separately with mocked services; no real external action or mathematical/full-package clearance.'},sort_keys=True))
if __name__=='__main__':main()
