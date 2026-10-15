#!/usr/bin/env python3
"""Read-only validation of current operations sources and the genuine candidate."""
import hashlib,json,os,stat,sys,zipfile
from pathlib import Path,PurePosixPath
from unittest.mock import patch
HERE=Path(__file__).resolve().parent
AUDIT=HERE.parent.parent
REPO=AUDIT.parents[2]
sys.path.insert(0,str(AUDIT/'operations'))
import common as c
import zenodo_pr464 as z
import register_pr464_tracker as t
import integrate_pr464_publication as integ
COUNT=0

def require(ok,message):
    global COUNT
    COUNT+=1
    if not ok:raise RuntimeError(message)
def sha(b):return hashlib.sha256(b).hexdigest()
def read(p):return json.loads(p.read_text(),object_pairs_hook=unique)
def unique(pairs):
    out={}
    for k,v in pairs:
        require(k not in out,'Duplicate JSON key');out[k]=v
    return out

def bound(p,spec):
    require(not p.is_symlink() and p.is_file(),'Bound input missing/symlink')
    data=p.read_bytes();require(type(spec['bytes']) is int and len(data)==spec['bytes'] and sha(data)==spec['sha256'],'Bound bytes drift');return data

def main():
    original=read(HERE/'REVIEWED_INPUTS.json')
    for name,spec in original['files'].items():bound(REPO/name.removeprefix('repo:') if name.startswith('repo:') else AUDIT/name,spec)
    freeze=read(AUDIT/'PACKAGE_REVIEW_INPUT_2.json')
    require(freeze['pr']==464 and freeze['problem']=='30004807' and freeze['original_head']==c.ORIGINAL,'Freeze identity drift')
    for name,field in [('SOURCE_RECEIPT.json','source_receipt_sha256'),('MATHEMATICAL_ACCEPTANCE_GATE.json','mathematical_acceptance_gate_sha256'),('BRANCH_INSTALL_PLAN.json','branch_install_plan_sha256')]:require(freeze[field]==sha((AUDIT/name).read_bytes()),'Freeze crossbinding drift')
    package=AUDIT/'package'
    for name,spec in freeze['files'].items():bound(package/name,spec)
    require(len(freeze['files'])==8,'Wrong top-file count')
    manifest=read(package/'SHA256SUMS.json')['files'];plan=read(AUDIT/'BRANCH_INSTALL_PLAN.json')
    installs={}
    for item in plan['entries']:
        c.relative(item['local_program_path']);c.relative(item['repository_destination'])
        p=c.safe_file(REPO,item['local_program_path']);require(p.is_relative_to(package),'Install escaped package')
        name=p.relative_to(package).as_posix();require(item['repository_destination']==c.PREPRINT+name and name not in installs,'Install duplicate/mapping drift')
        installs[name]=bound(p,item)
    require(len(installs)==185,'Wrong exact install count')
    archive_names=set()
    with zipfile.ZipFile(package/c.ZIP_NAME) as archive:
        entries=archive.infolist();require(len(entries)==181 and len({e.filename for e in entries})==181 and archive.testzip() is None,'ZIP size/uniqueness/CRC drift')
        for item in entries:
            c.relative(item.filename);require(not item.is_dir() and ((item.external_attr>>16)&0o170000)!=0o120000,'ZIP directory/symlink')
            data=archive.read(item);require(data==(package/item.filename).read_bytes(),'ZIP/local mismatch');require(data==installs[item.filename],'ZIP/install mismatch')
            require(item.filename not in {'manuscript.pdf',c.ZIP_NAME,'deposit.json','ARCHIVE_RECEIPT.json'},'Circular external ZIP entry')
            archive_names.add(item.filename)
        require(archive_names==set(manifest)|{'SHA256SUMS.json'} and len(manifest)==180,'Manifest entry union drift')
        for name,spec in manifest.items():require(bound(package/name,spec)==archive.read(name),'Manifest bound payload drift')
    require(set(installs)==archive_names|set(freeze['files']),'Exact install union drift')
    source=read(AUDIT/'SOURCE_RECEIPT.json');sources={}
    for item in source['files']:
        data=bound(AUDIT/'source_snapshot'/item['path'],item);sources[item['path']]=data
        historical='verification/frozen_history/'+item['path'].removeprefix(c.PREFIX);require(installs[historical]==data,'Historical copy differs')
    require(len(sources)==13 and source['scope_gate']=='exact claimed_solved' and source['head_sha']==c.ORIGINAL,'Source receipt identity drift')
    base=AUDIT/'source_snapshot'/c.PREFIX
    refs=read(base/'audit/FROZEN_INPUTS.json');count=0
    for item in refs['files']:bound(base/'release'/item['path'],item);count+=1
    for name,spec in read(base/'audit/AUDIT_MANIFEST.json')['portable_files'].items():bound(base/'audit'/name,spec);count+=1
    require(count==11 and refs['author_manifest_sha256'] not in {sha(d) for d in sources.values()},'Historical available/unattested reference distinction drift')
    evidence=read(package/'REVIEW_EVIDENCE_SELECTION.json')
    for item in evidence['entries']:require(bound(package/item['path'],item)==bound(REPO/item['origin'],item),'Evidence origin drift')
    require(len(evidence['entries'])==138 and evidence['positive_explicit_selection'] is True,'Evidence inventory drift')
    metadata=read(package/'metadata.json');deposit=read(package/'deposit.json');require(metadata==deposit['metadata'],'Canonical metadata drift')
    require({x.get('name',Path(x['path']).name):x['path'] for x in deposit['files']}==c.UPLOADS,'Public effective upload mapping drift')
    reviews=[]
    for number in [1,2]:
        root=AUDIT/'reviews'/('package_round'+str(number));result=read(root/'RESULT.json')
        require(result['verdict']=='PASS' and type(result['blocking_issue_count']) is int and result['blocking_issue_count']==0 and type(result['required_correction_count']) is int and result['required_correction_count']==0,'Clean full review absent')
        require(result['input_manifest_sha256']==sha((AUDIT/'PACKAGE_REVIEW_INPUT_2.json').read_bytes()) and result['final_candidate_files']==freeze['files'],'Clean full review binding drift')
        require(result['report_sha256']==sha((root/'FULL_PACKAGE_REVIEW.md').read_bytes()),'Report hash drift')
        reviews.append({'round':number,'identity':result['reviewer'],'report_sha256':result['report_sha256'],'blocking_issue_count':0,'required_correction_count':0})
    require(reviews[0]['identity']!=reviews[1]['identity'],'Reviewers not fresh')
    require(not (AUDIT/'FINAL_ACCEPTANCE_GATE.json').exists(),'Genuine final gate unexpectedly exists')
    dispatch=[]
    def no_dispatch(*a,**k):dispatch.append('called');raise RuntimeError('Forbidden genuine service dispatch')
    missing=[]
    with patch.object(c,'github',no_dispatch),patch.object(c,'gws',no_dispatch),patch.object(t,'gws',no_dispatch),patch.object(c.subprocess,'run',side_effect=no_dispatch):
        for name,fn in [('validate',c.validate_gate),('check',lambda:z.run()),('stage',lambda:z.run('stage',True)),('publish',lambda:z.run('publish',True,123456)),('tracker',lambda:t.run(True)),('integration',lambda:integ.run(True)),('reconcile',integ.reconcile)]:
            try:fn()
            except RuntimeError as exc:require('FINAL_ACCEPTANCE_GATE.json' in str(exc),'Wrong missing-gate rejection');missing.append(name)
            else:raise RuntimeError('Missing gate allowed entry '+name)
    require(not dispatch,'Actual absent-gate probe dispatched a service')
    # Inspect only path type; do not read account draft state or credentials.
    state_dir=REPO/'.zenodo-state';require(state_dir.is_dir() and not state_dir.is_symlink() and state_dir.resolve()==state_dir,'Actual private kit state root is aliased')
    result={'verdict':'PASS','explicit_conditions':COUNT,'original_source_files':13,'extant_internal_references':11,'standalone_author_manifest_digest':'UNATTESTED','frozen_top_files':8,'archive_entries':181,'archive_payloads':180,'install_targets':185,'review_evidence_origins':138,'full_package_reviews':reviews,'genuine_missing_gate_probes':missing,'real_external_calls':0,'reviewed_inputs_unchanged':True,'actual_private_kit_state_root_path_type':'ordinary canonical directory; contents not read','genuine_final_gate_absent':True,'review_input_manifest_sha256':sha((AUDIT/'PACKAGE_REVIEW_INPUT_2.json').read_bytes())}
    (HERE/'CURRENT_INPUT_VALIDATION.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
if __name__=='__main__':main()
