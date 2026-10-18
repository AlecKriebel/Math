#!/usr/bin/env python3
"""Authenticate the complete reviewed publication before one ready/merge attempt.

Existing intents reconcile read-only; they never authorize a blind retry. Git
reads and the operative updater main are guarded against any mutation fallback.
"""
from pathlib import Path
import contextlib,datetime,hashlib,importlib.util,io,json,re,stat,subprocess

A=Path(__file__).resolve().parents[1]
P=A/'publication'
PR='1283';URL='https://github.com/AlecKriebel/Math/pull/1283'
BRANCH='dot/semibrace-30005434-complete-existence-20261011'
ORIGINAL='4624244af725a80a2b7faf111f6b1ca62aaefe37'
WORKFLOW={'prepare_package.py','build_package.py','compile_note.py','verification/verify.py','append_tracker.py','update_pr_publication.py','check_public_downloads.py','workflow_regression.py'}
PINNED_KIT='a91f961bcabadb15f92bb738c3194f0277cd47f1f87167ac8db8eb7c4fd3b9ca'
PDF='Semibrace_Existence_Classification_Note_v1.0.pdf'
ZIP='Semibrace_Existence_Classification_Verification_v1.0.zip'
EDITION={'ACCEPTANCE.md','AGGREGATE_CHECKS.json','BYTE_PRESERVATION.json','INDEPENDENT_AUDIT.md','MANIFEST.json','PROOF_CLASSIFICATION.md','README.md','SOURCE_METADATA.json'}

def need(value,message):
    if not value:raise RuntimeError(message)
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def regular(path):
    path=Path(path)
    need(not path.is_symlink() and path.is_file(),'Missing/nonregular control '+str(path))
    for parent in path.parents:need(not parent.is_symlink(),'Symlink control parent '+str(parent))
    return path

def read(path):return json.loads(regular(path).read_text())
def stamp(path):
    path=regular(path);before=path.stat();data=path.read_bytes();after=path.stat()
    need((before.st_dev,before.st_ino,before.st_size,before.st_mtime_ns,before.st_mode)==(after.st_dev,after.st_ino,after.st_size,after.st_mtime_ns,after.st_mode),'Control changed while reading '+str(path))
    return {'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest(),'device':after.st_dev,'inode':after.st_ino,'mtime_ns':after.st_mtime_ns,'mode':stat.S_IMODE(after.st_mode)}

def authenticate_preimport():
    """Authenticate reviewed bytes without executing any project source."""
    gate=read(P/'FINAL_REVIEW_GATE.json')
    need(gate.get('schema')=='math-preprint-final-review-gate-v1' and gate.get('pr')==1283 and gate.get('problem_id')==30005434 and gate.get('original_head')==ORIGINAL and gate.get('status')=='pass','Exact reviewed gate required before importing updater')
    need(isinstance(gate.get('workflow'),dict) and set(gate['workflow'])==WORKFLOW,'Exact eight workflow bindings required before importing updater')
    program=A.parents[1];repo=Path('/Users/alec/Documents/Math')
    code={P/name:gate['workflow'][name] for name in WORKFLOW}
    code.update({program/'publication_coordinators/pr1283.py':gate.get('deposit_coordinator_sha256'),program/'publication_coordinators/verify_pr1283_merge.py':gate.get('postmerge_coordinator_sha256'),repo/'zenodo_deposit_tool/zenodo.py':gate.get('shared_kit_sha256')})
    need(gate.get('shared_kit_sha256')==PINNED_KIT,'Pinned kit differs before importing updater')
    for path,expected in code.items():
        need(isinstance(expected,str) and re.fullmatch('[0-9a-f]{64}',expected) is not None and stamp(path)['sha256']==expected,'Reviewed code differs before importing updater '+str(path))
    latest=gate.get('latest_review',{})
    need(latest.get('status')=='CLEAN' and latest.get('actual_review') is True and latest.get('fresh_reviewer') is True,'Latest actual clean review required before importing updater')
    raw=latest.get('input_freeze');need(isinstance(raw,str) and bool(raw),'Latest reviewed input freeze required')
    freeze=regular(P/raw).resolve()
    try:freeze.relative_to((A/'reviews').resolve())
    except ValueError:raise RuntimeError('Pre-import freeze outside own audit reviews')
    need(stamp(freeze)['sha256']==latest.get('input_freeze_sha256'),'Latest reviewed input freeze anchor differs before import')
    inventory=read(freeze);local=inventory.get('files',[]);external=inventory.get('external_readonly_inputs',[]);need(isinstance(local,list) and isinstance(external,list),'Explicit latest input arrays required before import');entries=local+external;bound={}
    need(isinstance(entries,list) and bool(entries),'Nonempty latest frozen inputs required before import')
    for entry in entries:
        need(isinstance(entry,dict) and isinstance(entry.get('path'),str) and type(entry.get('bytes')) is int and entry['bytes']>=0 and isinstance(entry.get('sha256'),str) and re.fullmatch('[0-9a-f]{64}',entry['sha256']) is not None,'Invalid latest frozen input before import')
        raw=entry['path'];need('..' not in Path(raw).parts,'Unsafe latest input path before import')
        path=Path(raw);path=path if path.is_absolute() else A/path;identity=str(path.resolve())
        need(identity not in bound,'Duplicate latest frozen input before import');bound[identity]=entry
        actual=stamp(path);need(actual['bytes']==entry['bytes'] and actual['sha256']==entry['sha256'],'Latest frozen input differs before import '+str(path))
    # The private entrypoint is an explicit external control, never a portable
    # member inferred from a receipt. Its reviewed bytes must also match.
    required={str(path.resolve()) for path in code}|{str(Path(__file__).resolve())}
    need(required<=set(bound),'Latest review freeze omits code/private ready control before import')
    return gate

def load_updater():
    authenticate_preimport()
    path=regular(P/'update_pr_publication.py');spec=importlib.util.spec_from_file_location('pr1283_ready_operative_updater',path);module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module);return module.__dict__

def controls(u):
    paths=[P/name for name in ['PR_BRANCH_RECEIPT.json','PR_BRANCH_INTENT.json','PR_BODY_FINAL.md','FINAL_REVIEW_GATE.json','BUILD_RECEIPT.json','COMPILE_RECEIPT.json','LAYOUT_VERIFICATION.json','PUBLICATION_RECEIPT.json','PUBLIC_DOWNLOAD_VERIFICATION.json','zenodo-deposit.json','tracker/TRACKER_RECEIPT.json','manuscript/main.tex','output/pdf/main.pdf',PDF,ZIP]]
    paths += [A/name for name in ['CURRENT_PR1283_CONTEXT.json','MATH_GATE.json','PRIORITY_ADJUDICATION.json','SUBMITTED_SNAPSHOT.json']]
    if read(A/'CURRENT_PR1283_CONTEXT.json')['edition_mode']=='documented_correction':paths.append(A/'CURRENT_EDITION_CORRECTION.json')
    paths += [A/folder/name for folder in ['submitted','current_edition'] for name in sorted(EDITION)]
    paths += [P/name for name in sorted(u['REQUIRED_WORKFLOW'])]
    paths += [u['COORDINATOR'],u['POSTMERGE'],u['SHARED_KIT'],Path(__file__).resolve()]
    if (P/'PR_BODY_UPDATE_INTENT.json').exists():paths.append(P/'PR_BODY_UPDATE_INTENT.json')
    # These are explicitly registered reviewer controls, not arbitrary nested paths.
    gate=read(P/'FINAL_REVIEW_GATE.json')
    for review in gate.get('reviews',[]):
        paths.extend(P/review[key] for key in ['report','verdict','manifest','input_freeze'])
    latest=gate.get('latest_review',{})
    inventory=read(P/latest['input_freeze'])
    for entry in inventory.get('files',[])+inventory.get('external_readonly_inputs',[]):
        target=Path(entry['path']);paths.append(target if target.is_absolute() else A/target)
    return {str(Path(path).absolute()):stamp(path) for path in paths}

def unchanged(saved):
    need({raw:stamp(Path(raw)) for raw in saved}==saved,'Publication control files changed during authentication/action boundary')

def read_git_command(args):
    need(bool(args),'Empty Git command')
    if args[0]=='branch':need(tuple(args)==('branch','--show-current'),'Forbidden Git branch mutation')
    else:need(args[0] in {'rev-list','diff-tree','show','ls-remote','rev-parse'},'Forbidden Git mutation during completed receipt authentication')

class ReadOnlySubprocess:
    def __init__(self,original):self.original=original
    def _check(self,args):
        need(isinstance(args,(list,tuple)) and bool(args),'Explicit readonly subprocess arguments required')
        if args[0]=='git':
            tail=list(args[1:])
            while tail and tail[0]=='-c':need(len(tail)>=2,'Malformed Git option');tail=tail[2:]
            read_git_command(tail)
        else:need(list(args[:3])==['gh','pr','view'],'Forbidden service mutation during completed receipt authentication')
    def run(self,args,**kwargs):self._check(args);return self.original.run(args,**kwargs)
    def check_output(self,args,**kwargs):self._check(args);return self.original.check_output(args,**kwargs)

@contextlib.contextmanager
def readonly_updater(u):
    original_git=u['git'];original_subprocess=u['subprocess']
    def git(*args,**kwargs):read_git_command(args);return original_git(*args,**kwargs)
    u['git']=git;u['subprocess']=ReadOnlySubprocess(original_subprocess)
    try:yield
    finally:u['git']=original_git;u['subprocess']=original_subprocess

def authenticate_completed(u=None):
    u=load_updater() if u is None else u
    need(u['BRANCH']==BRANCH and u['NUMBER']==PR,'Operative updater target differs')
    before=controls(u);receipt=read(P/'PR_BRANCH_RECEIPT.json');intent=read(P/'PR_BRANCH_INTENT.json');body=regular(P/'PR_BODY_FINAL.md').read_text()
    need(receipt.get('body_readback_verified') is True and receipt.get('remote_readback_verified') is True and receipt.get('operation_stage')=='reviewed_branch_and_final_body_verified','Regular completed branch/body receipt required')
    with readonly_updater(u):
        # This is the actual complete main, not a gate-only replacement. The
        # pre-existing receipt plus readonly facade forbids its mutation routes.
        output=io.StringIO()
        with contextlib.redirect_stdout(output):u['main']()
        need(json.loads(output.getvalue())==receipt,'Operative completed receipt readback differs')
        build=read(P/'BUILD_RECEIPT.json');pub=read(P/'PUBLICATION_RECEIPT.json');tracker=read(P/'tracker/TRACKER_RECEIPT.json');snapshot=read(A/'SUBMITTED_SNAPSHOT.json')
        files,_,_=u['desired_files'](build,pub,tracker,snapshot);need(len(files)==13,'Exactly thirteen authenticated intended blobs required')
        wanted=u['expected_identity'](pub,tracker,files,body)
        head=u['validate_saved'](receipt,wanted,files);need(u['validate_saved'](intent,wanted,files)==head,'Completed branch intent/receipt commit differs')
    unchanged(before)
    return {'head':head,'branch':BRANCH,'body':body,'paths':sorted(files),'release_identity':wanted,'controls':before}

class Services:
    def live(self):
        return json.loads(subprocess.check_output(['gh','pr','view',PR,'--repo','AlecKriebel/Math','--json','state,isDraft,headRefOid,headRefName,baseRefName,body,files,url'],text=True,timeout=60))
    def ready(self):return subprocess.run(['gh','pr','ready',PR,'--repo','AlecKriebel/Math'],capture_output=True,text=True,timeout=60)
    def merge(self,head):return subprocess.run(['gh','pr','merge',PR,'--repo','AlecKriebel/Math','--merge','--match-head-commit',head],capture_output=True,text=True,timeout=60)

def remote_head(u):
    with readonly_updater(u):parts=u['git']('ls-remote','origin','refs/heads/'+BRANCH).decode().split()
    need(len(parts)==2 and parts[1]=='refs/heads/'+BRANCH,'Missing/different remote branch')
    return parts[0]

def check_live(j,auth,u,states=('OPEN',)):
    need(j.get('url')==URL and j.get('state') in states and j.get('baseRefName')=='main' and j.get('headRefOid')==auth['head'] and j.get('headRefName')==BRANCH and j.get('body')==auth['body'],'Fresh live PR target/head/base/body differs')
    need(type(j.get('isDraft')) is bool,'Fresh actual draft state required')
    paths=[entry.get('path') for entry in j.get('files',[]) if isinstance(entry,dict)]
    need(len(paths)==13 and len(set(paths))==13 and set(paths)==set(auth['paths']),'Fresh live thirteen-path scope differs')
    if j['state']=='OPEN':need(remote_head(u)==auth['head'],'Fresh remote head differs')
    return j

def exclusive(path,data):
    need(not path.is_symlink(),'Unsafe intent path')
    try:
        with path.open('x') as stream:stream.write(json.dumps(data,indent=2)+'\n')
    except FileExistsError:raise RuntimeError('Prior/concurrent intent exists; reconcile read-only, never retry blindly')

def make_intent(kind,auth):
    return {'schema':'math-pr1283-'+kind+'-intent-v1','at_utc':now(),'pr':1283,'expected_head':auth['head'],'branch':BRANCH,'base_ref':'main','body_sha256':hashlib.sha256(auth['body'].encode()).hexdigest(),'exact13_paths':auth['paths'],'release_identity':auth['release_identity'],'control_files':auth['controls'],'policy':'One attempt; uncertain outcomes reconcile read-only against this exact known head and release, never by blind ready/merge retry.'}

def command(path,call,head,kind):
    try:result=call()
    except Exception as error:
        exclusive(path,{'at_utc':now(),'expected_head':head,'outcome':'unknown','exception':type(error).__name__,'message':str(error)})
        raise RuntimeError(kind+' outcome requires read-only reconciliation; no blind retry') from error
    exclusive(path,{'at_utc':now(),'expected_head':head,'returncode':result.returncode,'stdout':result.stdout,'stderr':result.stderr})
    need(result.returncode==0,kind+' outcome requires read-only reconciliation; no blind retry')
    return result

def reconcile_existing(u,services):
    # A prior intent never authorizes another mutation. MERGED cannot pass the
    # updater's OPEN-only main; only immutable saved controls/live identity are
    # observed here, leaving full postmerge verification to its own coordinator.
    receipt=read(P/'PR_BRANCH_RECEIPT.json');body=regular(P/'PR_BODY_FINAL.md').read_text();head=receipt.get('commit')
    need(isinstance(head,str) and re.fullmatch('[0-9a-f]{40}',head) is not None,'Invalid known completed head')
    auth={'head':head,'body':body,'paths':receipt.get('paths',[])}
    for kind in ['ready','merge']:
        path=P/('READY_REQUEST_INTENT.json' if kind=='ready' else 'MERGE_REQUEST_INTENT.json')
        if path.exists():
            saved=read(path)
            need(saved.get('schema')=='math-pr1283-'+kind+'-intent-v1' and saved.get('pr')==1283 and saved.get('expected_head')==head and saved.get('branch')==BRANCH and saved.get('base_ref')=='main' and saved.get('body_sha256')==hashlib.sha256(body.encode()).hexdigest() and saved.get('exact13_paths')==auth['paths'],'Saved attempt identity differs; remain read-only')
            unchanged(saved['control_files'])
    j=check_live(services.live(),auth,u,states=('OPEN','MERGED'))
    if j['state']=='OPEN':authenticate_completed(u)
    return {'at_utc':now(),'expected_head':head,'state':j['state'],'status':'existing_attempt_read_only_reconciliation','new_ready_requests':0,'new_merge_requests':0,'independent_postmerge_verification_required':True}

def guarded_main(u=None,services=None):
    u=load_updater() if u is None else u;services=Services() if services is None else services
    if (P/'READY_REQUEST_INTENT.json').exists() or (P/'MERGE_REQUEST_INTENT.json').exists():return reconcile_existing(u,services)
    auth=authenticate_completed(u);j=check_live(services.live(),auth,u)
    if j['isDraft']:
        fresh=authenticate_completed(u);need(fresh==auth,'Reviewed release changed before first ready request');j=check_live(services.live(),fresh,u);unchanged(fresh['controls'])
        need(j['isDraft'] is True,'Draft state changed before first ready request; reconcile read-only')
        exclusive(P/'READY_REQUEST_INTENT.json',make_intent('ready',fresh));unchanged(fresh['controls'])
        command(P/'READY_COMMAND_RECEIPT.json',services.ready,auth['head'],'Ready')
        j=check_live(services.live(),auth,u);unchanged(auth['controls']);need(j['isDraft'] is False,'Ready transition not confirmed; reconcile read-only')
    fresh=authenticate_completed(u);need(fresh==auth,'Reviewed release changed before merge request');j=check_live(services.live(),fresh,u);unchanged(fresh['controls']);need(j['isDraft'] is False,'PR remains a draft; no merge request')
    exclusive(P/'MERGE_REQUEST_INTENT.json',make_intent('merge',fresh));unchanged(fresh['controls'])
    result=command(P/'MERGE_COMMAND_RECEIPT.json',lambda:services.merge(auth['head']),auth['head'],'Merge')
    observed=check_live(services.live(),auth,u,states=('OPEN','MERGED'));unchanged(auth['controls'])
    return {'at_utc':now(),'expected_head':auth['head'],'state':observed['state'],'status':'one_expected_head_merge_request_completed','new_ready_requests':1 if (P/'READY_REQUEST_INTENT.json').exists() else 0,'new_merge_requests':1,'merge_command_returncode':result.returncode,'independent_postmerge_verification_required':True}

def main():print(json.dumps(guarded_main(),indent=2))
if __name__=='__main__':main()
