#!/usr/bin/env python3
"""Read-only exact-object and private replay audit, written after math seal."""
from pathlib import Path
import hashlib,json,subprocess,sys,shutil,datetime
H=Path(__file__).resolve().parent
ROOT=H.parents[3]
SNAP=H.parent/'snapshot'
PREFIX='unsolved_math_prioritization/attempts/30004293'
HEAD='36c29bb039471f132889d577c9322d78925b62dd'
BASE='efd29c05204703acca9a0860812f54b94fae54b1'
PRIVATE=H/'tmp'/'replay'
def sha(b):return hashlib.sha256(b).hexdigest()
def git(*a):return subprocess.check_output(['git',*a],cwd=ROOT)
def main():
    manifest=json.loads((H.parent/'snapshot_manifest.json').read_text())
    objects=[]
    for e in manifest['files']:
        b=(SNAP/e['path']).read_bytes();raw=git('show',f'{HEAD}:{e["path"]}')
        assert raw==b and len(b)==e['bytes'] and sha(b)==e['sha256']
        blob=hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
        assert blob==e['git_blob_sha']
        mode=git('ls-tree',HEAD,'--',e['path']).decode().split()[0]
        assert mode=='100644'
        objects.append({'path':e['path'],'bytes':len(b),'sha256':sha(b),'git_blob':blob,'mode':mode})
    actual=set(git('ls-tree','-r','--name-only',HEAD,'--',PREFIX).decode().splitlines())
    assert actual=={x['path'] for x in objects if x['path'].startswith(PREFIX+'/')}
    target=SNAP/PREFIX
    nested=[]
    for mf in sorted(target.rglob('*MANIFEST.json')):
        d=json.loads(mf.read_text())
        for e in d.get('files',[]):
            p=mf.parent/e['path'];b=p.read_bytes()
            assert len(b)==e['bytes'] and sha(b)==e['sha256']
            nested.append({'manifest':str(mf.relative_to(target)),'path':e['path'],'sha256':sha(b)})
    author=json.loads((target/'FINAL_AUTHOR_MANIFEST.json').read_text())['files']
    authorpaths=[e['path'] for e in author]+['FINAL_AUTHOR_MANIFEST.json']
    for name in authorpaths:assert git('show',f'cd4f8dc65cd68c002e2cf85c9df60ce962f33c0d:{PREFIX}/{name}')==(target/name).read_bytes()
    historical=[]
    for commit,turn in [('624b3d15f77ea192eb69f8a0b6d79c484c1237b8',1),('3c8244f53f230138df4393c79c0f6fe86799f137',2),('62b7d113b4bfbf7faf1d0333c8a8a99b3b7d304c',3),('a5377aba029e573d577653330e63619de625fd39',4),('cd4f8dc65cd68c002e2cf85c9df60ce962f33c0d',5)]:
        mf=f'TURN_{turn}_MANIFEST.json';d=json.loads((target/mf).read_text())
        for e in d['files']:assert git('show',f'{commit}:{PREFIX}/{e["path"]}')==(target/e['path']).read_bytes()
        assert git('show',f'{commit}:{PREFIX}/{mf}')==(target/mf).read_bytes()
        state=json.loads((target/f'CURRENT_STATE_T{turn}.json').read_text())
        assert state['author_turns']==turn and state['complete_quantitative_resolution'] is False
        historical.append({'turn':turn,'commit':commit,'immutable_entries_including_manifest':len(d['files'])+1})
    remote=json.loads((target/'review/REMOTE_BINDING.json').read_text())
    for e in remote['files']:
        b=(target/e['path']).read_bytes()
        assert len(b)==e['size'] and hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==e['sha']
    oldq=git('show',f'{BASE}:unsolved_math_prioritization/QUEUE.md').decode()
    newq=git('show',f'{HEAD}:unsolved_math_prioritization/QUEUE.md').decode()
    def rows(q):return [x for x in q.splitlines(keepends=True) if '| 30004293 /' in x]
    oq,nq=rows(oldq),rows(newq);assert len(oq)==len(nq)==1
    assert oldq.replace(oq[0],'')==newq.replace(nq[0],'')
    assert nq[0]==oq[0].replace('| queued | 0/5 |','| unsolved | 5/5 |')
    fields=[x.strip() for x in nq[0].strip().split('|')]
    assert fields[-4:-1]==['','','']
    PRIVATE.mkdir(parents=True,exist_ok=True)
    private=PRIVATE/'30004293'
    if private.exists():shutil.rmtree(private)
    shutil.copytree(target,private)
    source=PRIVATE/'source';source.mkdir(exist_ok=True)
    names={'OWR_2019_50.pdf':'OWR','FGK_2022_arxiv.pdf':'FGKv3','FGK_2023_published.pdf':'FGKpublished','Mao_Song_2026.pdf':'MaoSongv2','de_la_Breteche_Tenenbaum_2026.pdf':'divisorPower'}
    sources=[]
    for e in json.loads((target/'SOURCE_MANIFEST.json').read_text())['sources']:
        b=(H/'tmp'/f'{names[e["file"]]}.pdf').read_bytes()
        assert len(b)==e['bytes'] and sha(b)==e['sha256']
        (source/e['file']).write_bytes(b);sources.append({'name':e['file'],'sha256':sha(b),'fresh_download_byte_exact':True})
    commands=[([sys.executable,str(private/f'verify_turn{i}.py')],f'turn{i}') for i in range(1,6)]
    commands += [([sys.executable,str(private/'replay_author.py')],'author_source_bound'),([sys.executable,str(private/'review/independent_checks.py')],'historical_review'),([sys.executable,str(private/'review/verify_review.py'),'--author',str(private)],'review_wrapper'),([sys.executable,str(private/'verify_publication.py')],'publication_wrapper')]
    replays=[]
    for command,name in commands:
        p=subprocess.run(command,cwd=private,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        (PRIVATE/f'{name}.stdout').write_bytes(p.stdout);(PRIVATE/f'{name}.stderr').write_bytes(p.stderr)
        d={'name':name,'returncode':p.returncode,'stdout_sha256':sha(p.stdout),'stderr_sha256':sha(p.stderr),'stderr_bytes':len(p.stderr)}
        if name.startswith('turn'):
            want=(private/f'TURN_{name[4:]}_CHECKS.json').read_bytes();d['receipt_byte_exact']=want==p.stdout
            assert d['receipt_byte_exact']
        if name=='author_source_bound':d['receipt_byte_exact']=(private/'AUTHOR_REPLAY.json').read_bytes()==p.stdout;assert d['receipt_byte_exact']
        if name=='historical_review':d['receipt_byte_exact']=(private/'review/INDEPENDENT_CHECKS.json').read_bytes()==p.stdout;assert d['receipt_byte_exact']
        assert p.returncode==0,(name,p.stderr.decode())
        replays.append(d)
    return {'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'head':HEAD,'base':BASE,'all_original_objects':objects,'original_target_file_count':len(actual),'nested_manifest_entries':len(nested),'nested':nested,'author_checkpoint_files':len(authorpaths),'historical_original_author_plus_review_files':len(authorpaths)+len(list((target/'review').iterdir())),'chronological_history':historical,'sources':sources,'replays':replays,'original_queue_row_only_delta':True,'original_queue_row':nq[0].strip(),'current_integration_gate':'pending refined head/base and actual queue after PR376 merge; original queue result is not current integration validation'}
if __name__=='__main__':print(json.dumps(main(),indent=2))
