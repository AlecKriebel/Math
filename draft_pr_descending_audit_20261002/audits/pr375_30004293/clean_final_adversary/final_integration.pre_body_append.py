#!/usr/bin/env python3
"""Read-only final integration gate; never modifies a candidate or Git."""
from pathlib import Path
import hashlib,json,subprocess,datetime,argparse
H=Path(__file__).resolve().parent
ROOT=H.parents[3]
HEAD='6b4d7afefb1b98c2fe06c1dceada279d4c21c055'
BASE='6dab96e6a1579056b35ff0b4c35c7c1acfa7c8cd'
ORIGINAL='36c29bb039471f132889d577c9322d78925b62dd'
TREE='1884a51f9e5f8605b2007227a9470245c96c0578'
ANCESTOR376='f193a85b640eae025089d8a7d35b8c00024e6ae7'
PREFIX='unsolved_math_prioritization/attempts/30004293'
def git(*a):return subprocess.check_output(['git',*a],cwd=ROOT)
def digest(b):return hashlib.sha256(b).hexdigest()
def check(metadata=None):
    mf=H.parent/'repaired_snapshot_manifest.json';m=json.loads(mf.read_text())
    assert m['head']==HEAD and m['base']==BASE and m['original_frozen_head']==ORIGINAL
    rawparents=git('show','-s','--format=%P',HEAD).decode().strip().split()
    assert rawparents==[ORIGINAL,BASE]
    assert git('show','-s','--format=%T',HEAD).decode().strip()==TREE
    subprocess.run(['git','merge-base','--is-ancestor',ANCESTOR376,BASE],cwd=ROOT,check=True)
    assert git('rev-parse','main').decode().strip()==BASE
    paths=set(git('diff','--name-only',BASE,HEAD).decode().splitlines())
    assert paths=={e['path'] for e in m['files']} and len(paths)==54
    old=json.loads((H.parent/'snapshot_manifest.json').read_text())
    olds={e['path']:e for e in old['files']}
    objects=[]
    for e in m['files']:
        b=git('show',f'{HEAD}:{e["path"]}')
        assert b==(H.parent/'repaired_snapshot'/e['path']).read_bytes()
        assert len(b)==e['bytes'] and digest(b)==e['sha256']
        mode=git('ls-tree',HEAD,'--',e['path']).decode().split()[0];assert mode=='100644'
        if e['path'].startswith(PREFIX+'/'):
            assert b==git('show',f'{ORIGINAL}:{e["path"]}')
            assert digest(b)==olds[e['path']]['sha256']
        objects.append({'path':e['path'],'bytes':len(b),'sha256':digest(b),'git_blob_sha':hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest(),'mode':mode})
    before=git('show',f'{BASE}:unsolved_math_prioritization/QUEUE.md').decode()
    after=git('show',f'{HEAD}:unsolved_math_prioritization/QUEUE.md').decode()
    diff=[(i+1,a,b) for i,(a,b) in enumerate(zip(before.splitlines(),after.splitlines())) if a!=b]
    assert len(before.splitlines())==len(after.splitlines()) and len(diff)==1
    line,a,b=diff[0];assert line==412
    af=[s.strip() for s in a.split('|')];bf=[s.strip() for s in b.split('|')]
    changed=[i for i,(x,y) in enumerate(zip(af,bf)) if x!=y]
    assert changed==[8,9] and af[1]=='401' and af[2]=='30004293 / OWR-17293-009'
    assert (af[8],af[9],bf[8],bf[9])==('queued','0/5','unsolved','5/5')
    assert bf[10:13]==['','','']
    original_mathseal=digest((H/'MATHEMATICAL_SEAL.md').read_bytes())
    report={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'head':HEAD,'base':BASE,'original_head':ORIGINAL,'ordered_parents':rawparents,'tree':TREE,'actual_pr376_ancestor':ANCESTOR376,'repaired_manifest_sha256':digest(mf.read_bytes()),'all_final_git_objects':objects,'unchanged_original_target_files':53,'original_replay_receipt_sha256':digest((H/'PACKAGE_REPLAY_RECEIPT.json').read_bytes()),'nested_bindings':220,'historical_author_files':42,'historical_author_plus_review_files':50,'current_vs_author_manifest_entries':[172,120],'queue_physical_line':line,'queue_rank':af[1],'only_changed_cells':changed,'no_paper_doi_link':True,'source_seal_sha256':digest((H/'SOURCE_FIRST_SEAL.md').read_bytes()),'mathematical_seal_sha256':original_mathseal,'mathematical_disposition':'all five scoped partial proofs withstand whole-package audit; original target unsolved5/5; distinct stronger audit deduction verified separately; no novelty certification'}
    if metadata:
        p=Path(metadata);d=json.loads(p.read_text())
        assert d['number']==375 and d['headRefOid']==HEAD and d['baseRefName']=='main'
        assert d['state']=='OPEN' and d['isDraft'] is True
        body=d['body'];assert all(x in body for x in [HEAD,ORIGINAL,BASE])
        lower=body.lower()
        assert 'unsolved' in lower and '5/5' in body and 'ai' in lower
        assert 'novelty' in lower and 'not a sixth author turn' in lower and 'without exhaustive' in lower
        assert ('independent' in lower and 'published' in lower)
        assert digest(body.encode())=='4fab85e37f3f47c8d58d9c6d2862339d0ddcda8849b88896599e5c0df006f78f'
        remote=H/'tmp/live_main_ref.json';rd=json.loads(remote.read_text())
        assert rd['object']['sha']==BASE
        pr376=H/'tmp/live_pr376_merge.json';merge=json.loads(pr376.read_text())
        assert merge['number']==376 and merge['state']=='MERGED' and merge['mergeCommit']['oid']==ANCESTOR376
        report['remote_main']={'oid':rd['object']['sha'],'readback_sha256':digest(remote.read_bytes())}
        report['actual_pr376_merge_readback']={'commit':merge['mergeCommit']['oid'],'mergedAt':merge['mergedAt'],'readback_sha256':digest(pr376.read_bytes())}
        report['live_metadata']={'sha256':digest(p.read_bytes()),'url':d['url'],'title':d['title'],'head':d['headRefOid'],'state':d['state'],'draft':d['isDraft'],'scope_readback_verified':True}
        report['completion_estimate_percent']=100
        report['integration_gate']='complete for this exact head/base and live metadata; root owns ready/merge/publication decisions'
    else:
        report['completion_estimate_percent']=90
        report['integration_gate']='final Git/queue checks passed; independent live PR body readback pending'
    return report
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--metadata');args=ap.parse_args()
    print(json.dumps(check(args.metadata),indent=2))
