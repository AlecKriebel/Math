"""One authorized, guarded repository-kit publication; unknown outcomes recover read-only."""
import sys
if not __debug__ or sys.flags.optimize:
    raise RuntimeError('Release helpers refuse optimized Python before any action')
from pathlib import Path
from datetime import datetime, timezone
import base64
import json
import subprocess
from release_binding import (context,binding,unchanged,acquire,exclusive_json,pr_identity,
    require,digest,durable_mkdir,tool_publication,ORIGINAL_HEAD,SHEET,FULL_RANGE)

PY='/Users/alec/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3'


def now():return datetime.now(timezone.utc).isoformat()


def publish_once(R,PUB,ROOT=None):
    R=Path(R);PUB=Path(PUB);ROOT=Path('/Users/alec/Documents/Math') if ROOT is None else Path(ROOT)
    lock=acquire(PUB)
    try:
        CTX=context(R)
        require(not (PUB/'ZENODO_VERIFIED_PUBLICATION.json').exists(),'Already verified: read-only reconciliation')
        require(not (PUB/'STAGE_ATTEMPT.json').exists(),'Prior stage attempt: no second stage permitted')
        require(not (PUB/'PUBLISH_ATTEMPT.json').exists(),'Prior publish intent requires read-only reconciliation')
        stamp=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
        T=PUB/'private_transport/zenodo_stage'/stamp;durable_mkdir(T,exist_ok=False)
        def run(label,command,timeout=60):
            try:result=subprocess.run(command,cwd=ROOT,capture_output=True,text=True,timeout=timeout)
            except Exception as e:
                for suffix,value in [('stdout.json',getattr(e,'stdout',None)),('stderr.txt',getattr(e,'stderr',None))]:
                    (T/(label+'-'+suffix)).write_bytes(value if isinstance(value,bytes) else (value or '').encode())
                exclusive_json(T/(label+'-exception.json'),{'utc':now(),'type':type(e).__name__,'error':str(e)})
                raise
            (T/(label+'-stdout.json')).write_text(result.stdout);(T/(label+'-stderr.txt')).write_text(result.stderr)
            require(result.returncode==0,label+' failed: retain outcome; no mutation retry')
            return json.loads(result.stdout)
        pr=run('PR-head-preflight',['/opt/homebrew/Cellar/gh/2.85.0/bin/gh','api','repos/AlecKriebel/Math/pulls/209'])
        pr_identity(pr,ORIGINAL_HEAD,True)
        q=run('PR-status-preflight',['/opt/homebrew/Cellar/gh/2.85.0/bin/gh','api',
            'repos/AlecKriebel/Math/contents/unsolved_math_prioritization/QUEUE.md?ref='+pr['head']['sha']])
        qrows=[x for x in base64.b64decode(q['content']).decode().splitlines() if '5100015 / AMR-050-0015' in x]
        require(len(qrows)==1 and qrows[0].split('|')[8].strip()=='claimed_solved','Wrong native queued case status')
        sheet=run('tracker-duplicate-preflight',['/Users/alec/.nvm/versions/node/v22.16.0/bin/gws',
            'sheets','spreadsheets','values','get','--params',json.dumps({'spreadsheetId':SHEET,'range':FULL_RANGE})])
        matches=[i for i,row in enumerate(sheet.get('values',[]),1) if any('AMR-050-0015' in str(v) or '5100015' in str(v) for v in row)]
        require(not matches,'Problem already appears in tracker: reconcile before deposit')
        exclusive_json(T/'PUBLICATION_PREFLIGHT.json',{'utc':now(),'PR':209,'head':pr['head']['sha'],
            'QUEUE_status':'claimed_solved','existing_problem_tracker_rows':matches,'release_binding':binding(CTX)})
        def call(label,operation,extra=()):
            return run(label,[PY,'-B',str(ROOT/'zenodo_deposit_tool/zenodo.py'),operation,str(R/'deposit.json'),*extra],600)
        local=call('01-local-check','check')
        require(local.get('environment')=='production' and local.get('files')==CTX['expected_files'] and local.get('title')==CTX['metadata']['title'],'Local toolkit/cleared manifest mismatch')
        unchanged(R,CTX)
        shared={'release_binding':binding(CTX),'metadata':CTX['metadata'],'files':CTX['expected_files']}
        exclusive_json(PUB/'STAGE_ATTEMPT.json',dict(shared,utc=now(),operation='single stage about to be attempted'))
        stage=call('02-stage','stage')
        record_id=stage.get('id');tool_publication(stage,CTX,record_id,'ready_to_publish')
        exclusive_json(PUB/'ZENODO_STAGED_VERIFIED.json',dict(shared,utc=now(),id=record_id,state='ready_to_publish',
            stage_attempt_sha256=digest(PUB/'STAGE_ATTEMPT.json'),tool_readback=stage))
        inspect=call('03-inspect-before-publication','inspect')
        tool_publication(inspect,CTX,record_id,'ready_to_publish');unchanged(R,CTX)
        exclusive_json(PUB/'ZENODO_PREPUBLICATION_INSPECT.json',dict(shared,utc=now(),id=record_id,
            staged_receipt_sha256=digest(PUB/'ZENODO_STAGED_VERIFIED.json'),tool_readback=inspect))
        exclusive_json(PUB/'PUBLISH_ATTEMPT.json',dict(shared,utc=now(),id=record_id,operation='single publish about to be attempted',
            staged_receipt_sha256=digest(PUB/'ZENODO_STAGED_VERIFIED.json'),
            prepublication_inspect_sha256=digest(PUB/'ZENODO_PREPUBLICATION_INSPECT.json')))
        published=call('04-publish','publish',['--confirm-id',str(record_id)])
        tool_publication(published,CTX,record_id)
        exclusive_json(PUB/'ZENODO_TOOL_PUBLICATION_RECEIPT.json',dict(shared,utc=now(),id=record_id,source='publish-tool',
            publish_attempt_sha256=digest(PUB/'PUBLISH_ATTEMPT.json'),tool_readback=published))
        from verify_published_readonly import verify_existing
        return verify_existing(R,PUB,CTX)
    except Exception as e:
        if 'T' in locals():exclusive_json(T/'PENDING.json',{'utc':now(),'error':str(e),'recovery':'Retain every outcome; existing stage/publish intent forbids another mutation'})
        raise
    finally:lock.close()


if __name__=='__main__':
    PUB=Path(__file__).resolve().parent
    receipt=publish_once(PUB.parent/'preprint',PUB)
    print(json.dumps({k:v for k,v in receipt.items() if k not in ['metadata','tool_postpublication_readback']},indent=2))
