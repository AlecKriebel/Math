"""Inactive PR211 protocol: immutable candidate proof and descendant-safe sync.

Imports are inert. Old m6/g6 authorize logical bytes only. New protocol review,
each exact admission acceptance, two candidate proofs and actual external Root
CAS evidence are separate requirements. No reference/PR/provider writer exists.
"""
import argparse
import datetime
import hashlib
import json
import os
from pathlib import Path
import re
import selectors
import signal
import stat
import sys
import time
import types

BASE=Path(__file__).absolute().parent
CASE=BASE.parent
NATIVE=CASE/'native_adoption_preparation_01'
PROGRAM=CASE.parents[1]
CHECKOUT=PROGRAM.parent
SNAPSHOT=CASE/'native_input_snapshot_preparation_01/snapshot_preimages.py'
SP={'bytes':15984,'sha256':'ed58585543f86c6bd0fe44617fb29e2ceee6db34d667b1f2a75955ea4e6258e5'}
MP={'bytes':107835,'sha256':'b5a34d2ec2720ec968dce694a694389381b1a473fadc7f7a9e0622f73b09d3e2'}
GP={'bytes':6438,'sha256':'c659f743dfbd7357e5d6b396d9a73184524937bdb8545352c30624a50e1f7f71'}
MN='_private_ROOT_INPUTS_ADOPTION100_06/INPUT_MANIFEST.json'
GN='ROOT_ADOPTION100_MODEL_ACCEPTANCE_06.json'
CACHE=CASE/'concurrent_native_body_cache_01/ROOT_ACTUAL_GET_CACHE_01'
CM={'bytes':241696,'sha256':'dda719f8d9a3380645dabbcdf485b8aa05bdc8336dd9690a817e99be6622ba55'}
CS={'bytes':588,'sha256':'6f74101c849f594d274d1aa3134e6d3357fc93122ca291a4d42a2cfbf463281c'}
CA={'bytes':2665,'sha256':'bfca150c7ccbf03c2a1176020acc2f7c32938a1b8b0ffb915ae6c1fff8e1366e'}
COLLECTOR={'bytes':7482,'sha256':'846ebd2a90d3d84e03439047452bf13093260ed8279c3a1f7eb2fab364497105'}
RETIRED={'2748e804f0ede21a8c91443430931f23bba80bff','c43d6346bd92cd6abd8753439819c12fddea4726'}
IMMUTABLE_SCOPE='IMMUTABLE_CANDIDATE_ONLY_NOT_MAIN_LEASE_CAS_OR_COMPLETION'


def need(ok,message):
    if type(ok) is not bool or not ok:raise RuntimeError(message)


def pin(raw):return {'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()}


def enc(obj):return (json.dumps(obj,sort_keys=True,indent=2,allow_nan=False)+'\n').encode()


def bootstrap():
    """Nofollow every ancestor before executing the one pinned existing reader."""
    need(SNAPSHOT.resolve()==SNAPSHOT,'Canonical pinned snapshot reader')
    handles=[];fd=None
    try:
        path=Path('/');parent=os.open(path,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW)
        handles.append((path,parent,os.fstat(parent)))
        for part in SNAPSHOT.parent.parts[1:]:
            path=path/part;parent=os.open(part,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW,dir_fd=parent)
            handles.append((path,parent,os.fstat(parent)))
        fd=os.open(SNAPSHOT.name,os.O_RDONLY|os.O_NOFOLLOW|os.O_NONBLOCK,dir_fd=parent)
        before=os.fstat(fd)
        need(stat.S_ISREG(before.st_mode) and stat.S_IMODE(before.st_mode)==0o444 and before.st_size==SP['bytes'],
             'Exact readonly snapshot source')
        with os.fdopen(fd,'rb',closefd=False) as stream:raw=stream.read(before.st_size+1)
        fields=lambda s:(s.st_dev,s.st_ino,s.st_size,s.st_mtime_ns,s.st_ctime_ns)
        need(fields(before)==fields(os.fstat(fd))==fields(SNAPSHOT.lstat()) and pin(raw)==SP,'Pinned source changed')
        for path,descriptor,initial in handles:
            a,b=os.fstat(descriptor),path.lstat()
            need(stat.S_ISDIR(b.st_mode) and (a.st_dev,a.st_ino)==(b.st_dev,b.st_ino)==(initial.st_dev,initial.st_ino),
                 'Pinned source ancestor changed')
    finally:
        if fd is not None:os.close(fd)
        for path,descriptor,initial in reversed(handles):os.close(descriptor)
    s=types.ModuleType('pr211_concurrent_pinned_snapshot');s.__file__=str(SNAPSHOT)
    exec(compile(raw,str(SNAPSHOT),'exec'),s.__dict__)
    return s


def ref(h,s,row):
    need(type(row) is dict and set(row)=={'path','bytes','sha256'} and type(row['path']) is str,'Exact file reference')
    path=Path(row['path']);need(path.is_absolute() and path.is_relative_to(CASE),'Case-owned canonical input required')
    raw,unused=s.read_regular(path)
    need(h.exact(pin(raw),h.bytepin({k:row[k] for k in ('bytes','sha256')})),'Referenced body differs')
    return h.decode(raw)


def fixed(h,s,path,wanted):
    raw,unused=s.read_regular(path)
    need(h.exact(pin(raw),h.bytepin(wanted)),'Fixed input differs: '+path.name)
    return raw,h.decode(raw)


def validate_object(h,obj,response_raw,receipt_raw,stderr):
    need(type(obj) is dict and set(obj)=={'oid','body_pin','raw_response','receipt','stderr'}
         and h.hexid(obj['oid']),'Exact cache object fields')
    oid=obj['oid'];wanted=h.bytepin(obj['body_pin'])
    need(h.exact(pin(response_raw),{k:obj['raw_response'][k] for k in ('bytes','sha256')})
         and h.exact(pin(receipt_raw),{k:obj['receipt'][k] for k in ('bytes','sha256')})
         and h.exact(pin(stderr),{k:obj['stderr'][k] for k in ('bytes','sha256')}) and stderr==b'',
         'Exact raw response/receipt/empty stderr pins')
    receipt=h.decode(receipt_raw)
    h.matches(receipt,{'schema':'pr211-actual-native-blob-GET-receipt-v1','method':'GET','path':'git/blobs/'+oid,
        'exit':0,'no_retry':True,'expected_body_pin':wanted,'stdout':obj['raw_response'],'stderr':obj['stderr']},
        'Actual exact GET receipt required')
    value=h.decode(response_raw)
    def completed_get(method,path):
        need(method=='GET' and path=='git/blobs/'+oid,'Only this actual immutable raw GET envelope')
        return h.decode(response_raw)
    body=h.read_blob(completed_get,oid)
    need(h.exact(pin(body),wanted),'Native body length/SHA256 differs')
    return body


def load_cache(seed):
    h,s=seed.h,seed.s
    raw,j=fixed(h,s,CACHE/'BODY_CACHE_MANIFEST.json',CM)
    unused,seal=fixed(h,s,CACHE/'BODY_CACHE_EXTERNAL_SEAL.json',CS)
    unused,a=fixed(h,s,CACHE.parent/'ROOT_NATIVE_BODY_CACHE_ACCEPTANCE_01.json',CA)
    collector,unused=s.read_regular(CACHE.parent/'collect_native_body_cache.py')
    need(h.exact(pin(collector),COLLECTOR),'Pinned explicit-host collector changed')
    h.matches(a,{'schema':'pr211-root-native-body-cache-acceptance-v1','evidence_scope':'ACTUAL_ROOT_RECEIPT',
        'accepted':True,'PR':211,'hostname':'github.com','repository_full_name':'AlecKriebel/Math',
        'logical_manifest_pin':MP,'logical_gate_pin':GP,'cache_manifest_pin':CM,'cache_external_seal_pin':CS,
        'collector_source_pin':COLLECTOR,'selected_paths':192,'protected_paths':10,'unique_objects':202,
        'decoded_native_body_bytes':2756787,
        'all202_native_SHA1_SHA256_lengths_and_exact_expected_associations_verified':True,
        'all202_successful_GET_routes_raw_response_receipt_stderr_links_verified':True},'Separate actual Root cache acceptance')
    h.matches(seal,{'schema':'pr211-native-body-cache-external-seal-v1',
        'manifest':{'path':'BODY_CACHE_MANIFEST.json',**CM},'logical_manifest_pin':MP,'collector_source_pin':COLLECTOR},
        'Cache external seal differs')
    h.matches(j,{'schema':'pr211-sealed-actual-native-body-cache-v1',
        'evidence_scope':'FACTUAL_NATIVE_BODY_GETS_REQUIRE_ROOT_ACCEPTANCE','logical_manifest_pin':MP,'logical_gate_pin':GP,
        'snapshot_source_pin':SP,'collector_source_pin':COLLECTOR,'selected_paths':192,'protected_paths':10,
        'unique_object_count':202,'all_native_oid_SHA1_and_body_SHA256_lengths_verified':True,
        'source_gate_rechecked_after_collection':True,'Root_acceptance_inferred':False,
        'native_mutations_or_refs_PRs_providers_currentfive_or_gates_changed':False},'Exact factual cache manifest')
    associations=[{'role':'selected','path':r['path'],'oid':r['git_blob'],
                   'body_pin':{k:r[k] for k in ('bytes','sha256')}} for r in seed.logical['files']]
    associations += [{'role':'protected','path':r['path'],'oid':r['sha'],
                      'body_pin':{k:r[k] for k in ('bytes','sha256')}} for r in seed.logical['reused_blobs']]
    need(h.exact(j.get('associations'),associations) and len({r['path'] for r in associations})==202,
         'Exact202 path/role/native/body associations')
    objects=j.get('objects')
    need(type(objects) is list and len(objects)==202 and all(type(r) is dict for r in objects)
         and [r.get('oid') for r in objects]==sorted({r['oid'] for r in associations}),
         'Complete exact unique immutable object set')
    wanted_by_oid={r['oid']:r['body_pin'] for r in associations}
    expected_files={'BODY_CACHE_MANIFEST.json','BODY_CACHE_EXTERNAL_SEAL.json','FROZEN_COLLECTION_INPUT.json'}
    bodies={};raw_total=receipt_total=decoded_total=0
    for obj in objects:
        oid=obj['oid'];need(h.exact(obj.get('body_pin'),wanted_by_oid[oid]),'Object association differs')
        payload=[]
        for key,suffix in (('raw_response','.stdout.json'),('receipt','.RECEIPT.json'),('stderr','.stderr.txt')):
            row=obj[key]
            need(type(row) is dict and set(row)=={'path','bytes','sha256'} and row['path']==oid+suffix,
                 'Exact positive cache basename; no escape or extras')
            raw,unused=s.read_regular(CACHE/row['path'])
            need(h.exact(pin(raw),h.bytepin({k:row[k] for k in ('bytes','sha256')})),'Cache file changed')
            payload.append(raw);expected_files.add(row['path'])
        body=validate_object(h,obj,*payload)
        bodies[oid]=body;raw_total+=len(payload[0]);receipt_total+=len(payload[1]);decoded_total+=len(body)
        need(raw_total<=4_000_000 and receipt_total<=200_000 and decoded_total<=2_756_787,'Aggregate cache bounds')
    need(decoded_total==2756787 and set(p.name for p in CACHE.iterdir())==expected_files,'Cache complete; unlisted entries refused')
    collection,unused=s.read_regular(CACHE/'FROZEN_COLLECTION_INPUT.json')
    h.matches(h.decode(collection),{'schema':'pr211-native-body-cache-input-v1','logical_manifest_pin':MP,
        'logical_gate_pin':GP,'snapshot_source_pin':SP,'collector_source_pin':COLLECTOR,
        'associations':associations,'unique_objects':202,'Root_acceptance_or_Main_lease_inferred':False},
        'Collection origin differs')
    return bodies


class Seed:
    """Pinned logical bytes/source/cache only; not mutation authority."""
    def __init__(self):
        self.s=bootstrap();self.e,self.h,self.c,self.original_refresh=self.s.load_helpers()
        self.source,self.source_identity=self.s.read_regular(Path(__file__).absolute())
        self.source_pin=pin(self.source)
        self.manifest_raw,self.source_manifest=fixed(self.h,self.s,BASE/'SOURCE_MANIFEST.json',
                                                    pin(self.s.read_regular(BASE/'SOURCE_MANIFEST.json')[0]))
        self.source_manifest_pin=pin(self.manifest_raw)
        self.refresh()

    def refresh(self):
        self.original_refresh()
        current,unused=self.s.read_regular(Path(__file__).absolute())
        need(current==self.source,'New protocol source changed')
        raw,unused=self.s.read_regular(BASE/'SOURCE_MANIFEST.json')
        need(raw==self.manifest_raw,'New protocol source manifest changed')
        self.h.matches(self.source_manifest,{'schema':'pr211-concurrent-native-source-manifest-v1',
            'source_only':True,'self_excluded':True},'Exact positive new protocol source manifest')
        rows=self.source_manifest.get('files')
        need(type(rows) is list and 1<=len(rows)<=20 and all(type(r) is dict and set(r)=={'path','bytes','sha256'} for r in rows)
             and len({r['path'] for r in rows})==len(rows),'Finite exact new source files')
        need({'path':'concurrent_checkpoint.py',**self.source_pin} in rows,'Own source absent or wrong in source manifest')
        for row in rows:
            name=self.h.rel(row['path']);need(Path(name).name==name,'New source manifest has no operational/nested files')
            body,unused=self.s.read_regular(BASE/name)
            need(self.h.exact(pin(body),self.h.bytepin({k:row[k] for k in ('bytes','sha256')})),'New source file changed')
        self.c,self.logical,self.overlay,self.pre,self.reused=self.h.load_inputs(MN,MP,GN,GP)
        need(len(self.overlay)==192 and sum(map(len,self.overlay.values()))==2219715 and len(self.reused)==10,
             'Frozen192/2219715 plus10 only')
        for body in self.overlay.values():need('\0' not in body.decode('utf-8'),'Only original inline UTF8 bodies; no blob POST')
        self.bodies=load_cache(self)
        for path,body in self.overlay.items():need(self.bodies[self.h.native('blob',body)]==body,'Selected body/cache differs')


def checked_admission(seed,a):
    h=seed.h
    need(type(a) is dict and set(a)=={'schema','PR','evidence_scope','protocol_pin','source_manifest_pin',
        'logical_manifest_pin','logical_gate_pin','cache_manifest_pin','cache_acceptance_pin','facts','parent','parent_tree',
        'created_UTC','commit_author','commit_committer','commit_message','parents','tree','candidate','candidate_journal'},
        'Exact typed admission fields')
    h.matches(a,{'schema':'pr211-concurrent-parent-admission-v1','PR':211,
        'evidence_scope':'FACTUAL_PARENT_ADMISSION_REQUIRES_ROOT_ACCEPTANCE','protocol_pin':seed.source_pin,
        'source_manifest_pin':seed.source_manifest_pin,'logical_manifest_pin':MP,'logical_gate_pin':GP,
        'cache_manifest_pin':CM,'cache_acceptance_pin':CA,'facts':seed.logical['facts'],
        'commit_message':seed.logical['commit_message']},'Admission fixed authority differs')
    need(all(h.hexid(a[k]) for k in ('parent','parent_tree','tree','candidate'))
         and h.exact(a['parents'],[a['parent']]) and a['candidate'] not in RETIRED,'Exact fresh one-parent admission')
    need(type(a['candidate_journal']) is str and len(a['candidate_journal'])<=80
         and re.fullmatch('ROOT_CONCURRENT_CANDIDATE_[A-Za-z0-9_-]{1,50}',a['candidate_journal']) is not None,
         'New exact one-use concurrent candidate journal;04/06 retired')
    for key in ('commit_author','commit_committer'):
        need(type(a[key]) is dict and set(a[key])=={'name','email','date'},'Fixed identity/date fields')
        for field in ('name','email'):need(h.exact(a[key][field],seed.logical[key][field]),'Identity substitution refused')
        need(h.exact(a[key]['date'],a['created_UTC']),'Only one explicit UTC seconds parameter')
    m=dict(seed.logical)
    m.update(expected_parent=a['parent'],expected_parent_tree=a['parent_tree'],commit_author=a['commit_author'],
             commit_committer=a['commit_committer'],candidate_journal=a['candidate_journal'])
    request,oid=h.commit_request(m,a['tree'],[a['parent']])
    need(oid==a['candidate'],'Deterministic admission candidate differs')
    return m


class Runtime:
    def __init__(self,seed,admission_ref,gate_ref):
        self.seed,self.e,self.h,self.c=seed,seed.e,seed.h,seed.c
        self.admission_ref,self.gate_ref=admission_ref,gate_ref
        self.refresh()

    def refresh(self):
        self.seed.refresh();h=self.h
        self.admission=ref(h,self.seed.s,self.admission_ref)
        self.m=checked_admission(self.seed,self.admission)
        self.admission_pin={k:self.admission_ref[k] for k in ('bytes','sha256')}
        self.gate=ref(h,self.seed.s,self.gate_ref)
        self.gate_pin={k:self.gate_ref[k] for k in ('bytes','sha256')}
        h.matches(self.gate,{'schema':'pr211-root-concurrent-admission-acceptance-v1','evidence_scope':'ACTUAL_ROOT_RECEIPT',
            'PR':211,'accepted':True,'protocol_pin':self.seed.source_pin,'source_manifest_pin':self.seed.source_manifest_pin,
            'admission_pin':self.admission_pin,'logical_manifest_pin':MP,'logical_gate_pin':GP,
            'cache_manifest_pin':CM,'cache_acceptance_pin':CA,'facts':self.seed.logical['facts'],
            'parent_only_parameterization_reviewed':True,'one_use_two_immutable_POSTs_authorized':True,
            'supersedes_legacy_exactMain_bridge_for_this_admission':True,'no_ref_writer_authority':True,
            'prior04_and06_retired_no_redispatch':True},'Separate actual Root admission authorization required')
        review=ref(h,self.seed.s,self.gate.get('protocol_review'))
        h.matches(review,{'schema':'pr211-root-concurrent-protocol-review-acceptance-v1','evidence_scope':'ACTUAL_ROOT_RECEIPT',
            'PR':211,'accepted':True,'protocol_pin':self.seed.source_pin,'source_manifest_pin':self.seed.source_manifest_pin,
            'logical_manifest_pin':MP,'logical_gate_pin':GP,'cache_manifest_pin':CM,'cache_acceptance_pin':CA,
            'Root_full_source_read':True,'independent_adversarial_review_accepted':True,
            'all_original_verifications_retained':True,'parent_only_admissions_without_new_peer_review_approved':True},
            'New general protocol review; old g6 alone grants no authority')
        self.overlay,self.pre,self.reused,self.bodies=self.seed.overlay,self.seed.pre,self.seed.reused,self.seed.bodies
        return self


def local_states(rt,resume=False,all_post=False):
    for row in rt.m['local_views']:
        raw,identity=rt.seed.s.read_regular(CHECKOUT/row['path'],absent=True)
        now=pin(raw) if raw is not None else None;post=pin(rt.overlay[row['path']])
        need(rt.h.exact(now,post) if all_post else
             rt.h.exact(now,row['preimage']) or (resume and rt.h.exact(now,post)),
             'Local five third state refused: '+row['path'])


def protected(rt,trees,root,post):
    h=rt.h
    need(trees.lookup(root,h.ATTEMPT[:-1])==('040000','tree',h.ATTEMPT_TREE)
         and trees.lookup(root,h.SHARED)==('040000','tree',h.SHARED_TREE),'Whole opaque protected trees differ')
    need(trees.lookup(root,h.QUEUE)==h.tuple_pin(rt.m['protected_queue']),'WholeQUEUE differs')
    for path,row in rt.reused.items():
        need(trees.lookup(root,path)==(row['mode'],row['type'],row['sha']),'Critical scientific path association differs')
    for path,body in rt.overlay.items():
        expected=('100644','blob',h.native('blob',body)) if post else rt.pre[path]
        need(trees.lookup(root,path)==expected,'Selected native path/preimage/postimage differs: '+path)


def parent_state(rt,observer):
    """Authenticates a fixed immutable parent without observing mutable Main."""
    h,c,m=rt.h,rt.c,rt.m;api=h.GetOnly(observer);parent=m['expected_parent'];root=m['expected_parent_tree']
    commit=api('GET','git/commits/'+parent)
    need(commit.get('sha')==parent and commit['tree']['sha']==root,'Admission parent/root differs')
    if parent!=h.ANCHOR:
        comp=api('GET','compare/'+h.ANCHOR+'...'+parent)
        need(comp.get('status')=='ahead' and comp['merge_base_commit']['sha']==h.ANCHOR,'Actual210 anchor ancestry differs')
    h.pr_identity(api,m)
    trees=c.NativeTrees(api);protected(rt,trees,root,False)
    wanted,leaves,dirs=h.expected(c,trees,root,rt.overlay,rt.pre)
    need(leaves==set(rt.overlay) and len(leaves)==192 and len(dirs)==25,'Exact192-leaf25-directory scope required')
    progress=h.decode(h.read_blob(api,rt.pre[h.VIEWS[2]][2]))
    h.matches(progress,h.baseline_facts(),'Intervening ascending checkpoint refused')
    baseline=h.decode(h.sealed('BASELINE_MEMBERSHIP.json',h.BASELINE_PIN))
    for key in ('fully_completed_eligible_PRs','published_PRs'):
        need(h.exact(progress.get(key),baseline[key]),'Exact52/36 baseline membership differs')
    need(type(progress.get('dated_eligible_total')) is int and progress['dated_eligible_total']==99,'Dated99 baseline differs')
    for alias,key in (('current_PR','active_PR'),('current_case_percent','case_workflow_estimate_percent')):
        if alias in progress:h.matches(progress,{alias:h.baseline_facts()[key]},'Baseline alias')
    for path in (h.VIEWS[1],h.VIEWS[4]):
        if rt.pre[path] is not None:need(rt.overlay[path].startswith(h.read_blob(api,rt.pre[path][2])),'Native log prefix differs')
    return wanted,leaves,dirs


def body_associations(rt,trees,root):
    """Explicit immutable proof reuse; no GET is fabricated or substituted."""
    selected={};critical={};h=rt.h
    protected(rt,trees,root,True)
    for path,expected in rt.overlay.items():
        oid=h.native('blob',expected);body=rt.bodies[oid]
        need(body==expected,'Cached actual native selected body differs')
        selected[path]={**pin(body),'mode':'100644','type':'blob','git_blob':oid}
    for path,row in rt.reused.items():
        need(h.exact(pin(rt.bodies[row['sha']]),{k:row[k] for k in ('bytes','sha256')}),'Critical full native body differs')
        critical[path]=dict(row)
    return selected,critical


def verify_immutable(rt,observer):
    """No mutable-ref read/equality assumption. A moved Main is immaterial here."""
    h,c,a=rt.h,rt.c,rt.admission;api=h.GetOnly(observer)
    wanted,expected_leaves,expected_dirs=parent_state(rt,api)
    need(wanted==a['tree'],'Reconstructed tree differs from admission')
    request,oid=h.commit_request(rt.m,wanted,[a['parent']])
    need(oid==a['candidate'] and oid not in RETIRED,'Canonical candidate identity differs/retired')
    commit=api('GET','git/commits/'+oid)
    need(commit.get('sha')==oid and commit['tree']['sha']==wanted
         and [r['sha'] for r in commit['parents']]==[a['parent']],'Candidate actual metadata/tree/ordered parent differs')
    h.matches(commit.get('author'),rt.m['commit_author'],'Canonical author')
    h.matches(commit.get('committer'),rt.m['commit_committer'],'Canonical committer')
    message=h.commit_message_readback(rt.m['commit_message'],commit.get('message'))
    trees=c.NativeTrees(api)
    leaves,dirs,deleted=trees.changes(a['parent_tree'],wanted)
    need(leaves==expected_leaves and dirs==expected_dirs and not deleted,'Full192/25/no-deletion foreign scope differs')
    selected,critical=body_associations(rt,trees,wanted)
    return {'schema':'pr211-concurrent-immutable-candidate-verification-v1','evidence_scope':IMMUTABLE_SCOPE,
        'PR':211,'protocol_pin':rt.seed.source_pin,'source_manifest_pin':rt.seed.source_manifest_pin,
        'logical_manifest_pin':MP,'logical_gate_pin':GP,'admission_pin':rt.admission_pin,
        'parent':a['parent'],'parent_tree':a['parent_tree'],'candidate':oid,'tree':wanted,'parents':[a['parent']],
        'selected_files':selected,'protected_existing_bodies':critical,'selected_count':192,'protected_count':10,
        'cache_manifest_pin':CM,'cache_acceptance_pin':CA,'all202_native_bodies_reauthenticated_from_actual_GET_cache':True,
        'full_scope_verified':True,'all_selected_native_bodies_verified':True,'foreign_native_tuples_preserved':True,
        'changed_leaves':sorted(leaves),'new_directories':sorted(dirs),'deleted_directories':[],
        'deterministic_canonical_commit_oid_verified':True,'fixed_author_and_committer_metadata_verified':True,
        'commit_message_readback':message,'mutable_Main_observed_or_spoofed':False,
        'this_action_native_POSTs':0,'earlier_attempt_effects_not_characterized':True,'actual_CAS_or_completion_inferred':False}


def lease_guard(rt,api,lock):
    lock.check();rt.refresh();local_states(rt)
    need(api('GET','git/ref/heads/main')['object']['sha']==rt.admission['parent'],'Stale admission before immutable effect/CAS')
    wanted,unused,unused_dirs=parent_state(rt,api)
    need(wanted==rt.admission['tree'],'Fresh native preimages/root differ')
    local_states(rt);rt.refresh();lock.check()
    need(api('GET','git/ref/heads/main')['object']['sha']==rt.admission['parent'],'Lease lost immediately before effect/CAS')
    lock.check()


def reserve_candidate_oid(rt):
    """Exclusive canonical-OID reservation survives admission/journal renaming."""
    oid=rt.admission['candidate']
    need(rt.h.hexid(oid) and oid not in RETIRED,'Retired/invalid candidate cannot be reserved')
    ledger=CASE/'concurrent_native_integration_01/_private_candidate_oid_ledger'
    with rt.e.ParentHandle(ledger) as parent:
        parent.check()
        try:os.mkdir(ledger.name,0o700,dir_fd=parent.fd)
        except FileExistsError:pass
        parent.check();os.fsync(parent.fd)
    name=oid+'.json'
    with rt.e.ParentHandle(ledger/name) as parent:
        parent.check()
        fd=os.open(name,os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW,0o444,dir_fd=parent.fd)
        try:
            raw=enc({'schema':'pr211-one-use-canonical-candidate-reservation-v1','candidate':oid,
                'admission_pin':rt.admission_pin,'protocol_pin':rt.seed.source_pin,
                'candidate_journal':rt.admission['candidate_journal'],
                'semantics':'Permanent attempt reservation before immutable POST. Never remove/reuse after failure or uncertainty.'})
            with os.fdopen(fd,'wb',closefd=False) as stream:
                need(stream.write(raw)==len(raw),'Short OID reservation write')
                stream.flush();os.fchmod(fd,0o444);os.fsync(fd)
        finally:os.close(fd)
        parent.check();os.fsync(parent.fd)


def candidate(rt):
    """Exactly two original audited API immutable POSTs; no resume/retry/ref writer."""
    e,h=rt.e,rt.h
    with e.WriterLock(rt.m['writer_lock']) as lock:
        rt.refresh()
        # Fixed journal from accepted admission prevents a fresh-journal retry of that admission.
        journal=e.journal_new(rt.admission['candidate_journal'])
        api=e.API(h,journal,mutate=True)
        lease_guard(rt,api,lock)
        reserve_candidate_oid(rt)
        entries=[{'path':path,'mode':'100644','type':'blob','content':body.decode('utf-8')}
                 for path,body in sorted(rt.overlay.items())]
        tree_request={'base_tree':rt.admission['parent_tree'],'tree':entries}
        commit_request,oid=h.commit_request(rt.m,rt.admission['tree'],[rt.admission['parent']])
        e.put(journal,'ONE_USE_ADMISSION_RESERVATION.json',{'admission_pin':rt.admission_pin,
            'protocol_pin':rt.seed.source_pin,'logical_manifest_pin':MP,'gate_pin':rt.gate_pin,
            'expected_tree':rt.admission['tree'],'expected_candidate':oid,
            'semantics':'One tree POST and one commit POST only. No redispatch after uncertainty or stale stop.'})
        lease_guard(rt,api,lock)
        api('POST','git/trees',tree_request,expected_oid=rt.admission['tree'])
        lease_guard(rt,api,lock)
        api('POST','git/commits',commit_request,expected_oid=oid)
        # New GET API instance, independent of construction API/cache. Main may now advance.
        reader=e.API(h,journal,mutate=False);reader.number=api.number
        rt.refresh();result=verify_immutable(rt,reader)
        rt.refresh();local_states(rt);lock.check()
        e.put(journal,'IMMUTABLE_CANDIDATE_VERIFIED.json',result)
        return {'candidate':oid,'tree':rt.admission['tree'],'journal':str(journal),
                'this_action_immutable_POST_dispatches':2,'actual_CAS_or_completion_inferred':False}


def accepted_verifications(rt,row):
    root=ref(rt.h,rt.seed.s,row)
    rt.h.matches(root,{'schema':'pr211-root-concurrent-preCAS-acceptance-v1','evidence_scope':'ACTUAL_ROOT_RECEIPT',
        'PR':211,'accepted':True,'protocol_pin':rt.seed.source_pin,'admission_pin':rt.admission_pin,
        'logical_manifest_pin':MP,'logical_gate_pin':GP,'candidate':rt.admission['candidate'],'tree':rt.admission['tree'],
        'immutable_candidate_verification_accepted':True,'independent_GET_candidate_verification_accepted':True,
        'cache_manifest_pin':CM,'cache_acceptance_pin':CA},'Actual Root acceptance of two candidate proofs')
    reports=root.get('verification_reports')
    need(type(reports) is list and len(reports)==2 and len({r.get('path') for r in reports})==2,'Two distinct candidate proof records')
    for report in reports:
        proof=ref(rt.h,rt.seed.s,report)
        rt.h.matches(proof,{'schema':'pr211-concurrent-immutable-candidate-verification-v1','evidence_scope':IMMUTABLE_SCOPE,
            'protocol_pin':rt.seed.source_pin,'admission_pin':rt.admission_pin,'candidate':rt.admission['candidate'],
            'tree':rt.admission['tree'],'parent':rt.admission['parent'],'parent_tree':rt.admission['parent_tree'],
            'full_scope_verified':True,'all_selected_native_bodies_verified':True,'foreign_native_tuples_preserved':True,
            'selected_count':192,'protected_count':10,'cache_manifest_pin':CM,'cache_acceptance_pin':CA,
            'all202_native_bodies_reauthenticated_from_actual_GET_cache':True,
            'mutable_Main_observed_or_spoofed':False,'actual_CAS_or_completion_inferred':False},'Candidate proof binding differs')
    return root


def actual_cas(rt,row,api):
    """Actual request/result/readback, never ancestry alone or a planned receipt."""
    h=rt.h;a=ref(h,rt.seed.s,row)
    h.matches(a,{'schema':'pr211-root-concurrent-actual-CAS-acceptance-v1','evidence_scope':'ACTUAL_ROOT_RECEIPT',
        'PR':211,'accepted':True,'hostname':'github.com','repository_full_name':'AlecKriebel/Math',
        'protocol_pin':rt.seed.source_pin,'source_manifest_pin':rt.seed.source_manifest_pin,
        'admission_pin':rt.admission_pin,'logical_manifest_pin':MP,'logical_gate_pin':GP,
        'cache_manifest_pin':CM,'cache_acceptance_pin':CA,'facts':rt.m['facts'],
        'parent':rt.admission['parent'],'candidate':rt.admission['candidate'],'tree':rt.admission['tree'],
        'actual_Root_MCP_CAS_performed':True,'actual_tool_success_and_readback_accepted':True,
        'original_lock_held_across_actual_Root_CAS':True,'unknown_outcome':False},
        'Separate actual external Root CAS acceptance required')
    accepted_verifications(rt,a.get('preCAS_acceptance'))
    ready=ref(h,rt.seed.s,a.get('actual_lock_guard_ready'))
    h.matches(ready,{'schema':'pr211-concurrent-locked-CAS-ready-v1',
        'evidence_scope':'HELD_LOCK_AND_DATED_FRESH_LEASE_NOT_CAS_SUCCESS',
        'protocol_pin':rt.seed.source_pin,'admission_pin':rt.admission_pin,
        'parent':rt.admission['parent'],'candidate':rt.admission['candidate'],
        'original_stable_lock_held':True},'Actual held-lock ready record required')
    request=ref(h,rt.seed.s,a.get('actual_tool_request'))
    h.matches(request,{'tool':'NativeMCP.github_update_ref','owner':'AlecKriebel','repo':'Math','ref':'heads/main',
        'expected_sha':rt.admission['parent'],'sha':rt.admission['candidate'],'force':False},'True Root expectedSHA forcefalse request')
    result=ref(h,rt.seed.s,a.get('actual_tool_response'))
    h.matches(result,{'isError':False,'structuredContent':{'success':True}},'Actual successful MCP tool response required')
    response_row=a.get('actual_readback_response');response=ref(h,rt.seed.s,response_row)
    receipt=ref(h,rt.seed.s,a.get('actual_readback_receipt'))
    h.matches(receipt,{'method':'GET','path':'git/ref/heads/main','exit':0,
        'stdout_pin':{k:response_row[k] for k in ('bytes','sha256')}},'Actual native ref readback receipt differs')
    need(response.get('ref')=='refs/heads/main' and response['object'].get('type')=='commit'
         and h.hexid(response['object'].get('sha')),'Actual native Main readback required')
    # A ready file alone says nothing about process lifetime after Root's CAS.
    # Root separately confirms a same-session live poll after actual CAS/readback
    # and before acceptance/ack, binding its raw poll, PID and exact evidence.
    confirmation=ref(h,rt.seed.s,a.get('post_CAS_same_live_guard_confirmation'))
    h.matches(confirmation,{'schema':'pr211-root-postCAS-same-live-guard-confirmation-v1',
        'evidence_scope':'ACTUAL_ROOT_RECEIPT','accepted':True,'protocol_pin':rt.seed.source_pin,
        'admission_pin':rt.admission_pin,
        'actual_lock_guard_ready_pin':{k:a['actual_lock_guard_ready'][k] for k in ('bytes','sha256')},
        'actual_tool_response_pin':{k:a['actual_tool_response'][k] for k in ('bytes','sha256')},
        'actual_readback_response_pin':{k:response_row[k] for k in ('bytes','sha256')},
        'same_session_live_poll_after_actual_MCP_and_readback_before_acceptance_and_ack':True,
        'original_lock_continuity_from_linear_held_source_and_same_live_session':True},
        'Separate actual Root post-CAS same-live-session confirmation required')
    need(type(ready.get('guard_pid')) is int and ready['guard_pid']>0
         and h.exact(confirmation.get('guard_pid'),ready['guard_pid']),'Same live guard PID required')
    poll=ref(h,rt.seed.s,confirmation.get('actual_same_session_poll_response'))
    need(type(poll.get('session_id')) is int and poll['session_id']>0
         and h.exact(confirmation.get('session_id'),poll['session_id'])
         and poll.get('exit_code') is None and type(poll.get('output')) is str,
         'Actual still-running session poll response required; exited guard is not continuity')
    observed=response['object']['sha']
    need(h.exact(a.get('actual_MAIN_after_CAS'),observed),'Actual readback observation differs')
    if observed!=rt.admission['candidate']:
        comp=api('GET','compare/'+rt.admission['candidate']+'...'+observed)
        need(comp.get('status')=='ahead' and comp['merge_base_commit']['sha']==rt.admission['candidate'],
             'Actual readback must equal/descend from true CAS target')
    return a


def wait_actual_CAS_reference(fd,check,timeout=180):
    """Bounded one-line Root acknowledgment; reject immediately queued excess.

    Only this descriptor's nonblocking flag is changed and restored. The bound
    is an observation of already queued bytes, not a promise about future input.
    """
    need(type(timeout) in (int,float) and 0<timeout<=180,'Finite CAS hold deadline')
    selector=selectors.DefaultSelector();prior=os.get_blocking(fd)
    data=bytearray();deadline=time.monotonic()+timeout
    try:
        os.set_blocking(fd,False);selector.register(fd,selectors.EVENT_READ)
        while True:
            check()
            remaining=deadline-time.monotonic()
            need(remaining>0,'Root CAS hold timed out; reconcile actual outcome read-only')
            if not selector.select(min(1,remaining)):continue
            try:chunk=os.read(fd,4097-len(data))
            except BlockingIOError:continue
            need(bool(chunk),'Root CAS input closed before a complete reference; no success inferred')
            data.extend(chunk)
            need(len(data)<=4096 and time.monotonic()<deadline,'Root CAS input oversized/late; no success inferred')
            if b'\n' not in data:continue
            need(data.count(b'\n')==1 and data.endswith(b'\n'),'One exact Root CAS reference line required')
            try:extra=os.read(fd,1)
            except BlockingIOError:extra=b''
            need(extra==b'','Queued excess after Root CAS reference refused')
            check()
            return bytes(data[:-1])
    finally:
        selector.close();os.set_blocking(fd,prior)


def hold_CAS(rt,api,journal,preCAS_ref):
    """Keep the original lock held while external Root alone uses true MCP CAS."""
    accepted_verifications(rt,preCAS_ref)
    old_handlers={}
    def interrupted(signum,frame):raise RuntimeError('Root hold interrupted; no CAS outcome inferred')
    for signum in (signal.SIGINT,signal.SIGTERM):
        old_handlers[signum]=signal.signal(signum,interrupted)
    try:
        with rt.e.WriterLock(rt.m['writer_lock']) as lock:
            lease_guard(rt,api,lock)
            ready={'schema':'pr211-concurrent-locked-CAS-ready-v1',
                'evidence_scope':'HELD_LOCK_AND_DATED_FRESH_LEASE_NOT_CAS_SUCCESS',
                'UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'guard_pid':os.getpid(),
                'protocol_pin':rt.seed.source_pin,'admission_pin':rt.admission_pin,
                'parent':rt.admission['parent'],'candidate':rt.admission['candidate'],
                'original_stable_lock_held':True,'actual_CAS_success_inferred':False}
            rt.e.put(journal,'LOCKED_CAS_READY.json',ready)
            print(json.dumps({'status':'READY_ORIGINAL_LOCK_HELD','ready_path':str(journal/'LOCKED_CAS_READY.json'),
                              'ready_pin':pin(enc(ready)),'expected_sha':rt.admission['parent'],
                              'sha':rt.admission['candidate'],'force':False}),flush=True)
            cas_ref=rt.h.decode(wait_actual_CAS_reference(sys.stdin.fileno(),lock.check))
            rt.refresh();local_states(rt,resume=True);lock.check()
            actual_cas(rt,cas_ref,api)
            observation=main_closure(rt,api)
            local_states(rt,resume=True);lock.check()
            rt.e.put(journal,'LOCKED_ACTUAL_CAS_READBACK.json',{'actual_CAS_pin':{k:cas_ref[k] for k in ('bytes','sha256')},
                **observation,'original_stable_lock_held':True,'terminal_acceptance_inferred':False})
            return observation
    finally:
        for signum,handler in old_handlers.items():signal.signal(signum,handler)


def main_closure(rt,observer):
    """Coherent exact R/root; later foreign motion is not silently accepted."""
    h,c=rt.h,rt.c;api=h.GetOnly(observer)
    observed=api('GET','git/ref/heads/main')['object']['sha']
    need(h.hexid(observed),'Fresh native Main identity')
    commit=api('GET','git/commits/'+observed)
    need(commit.get('sha')==observed and h.hexid(commit['tree']['sha']),'Fresh R/root differs')
    if observed!=rt.admission['candidate']:
        comp=api('GET','compare/'+rt.admission['candidate']+'...'+observed)
        need(comp.get('status')=='ahead' and comp['merge_base_commit']['sha']==rt.admission['candidate'],
             'Main must equal or actually descend from accepted CAS target')
    root=commit['tree']['sha'];trees=c.NativeTrees(api)
    selected,critical=body_associations(rt,trees,root)
    h.pr_identity(api,{**rt.m,'expected_parent':observed},after_ref=True)
    need(api('GET','git/ref/heads/main')['object']['sha']==observed,'Main moved across closure check; read-only reconcile again explicitly')
    return {'actual_MAIN_observed':observed,'actual_MAIN_tree':root,'CAS_target':rt.admission['candidate'],
            'CAS_target_tree':rt.admission['tree'],'selected_postimage_paths_verified':len(selected),
            'protected_body_paths_verified':len(critical),'whole_two_science_trees_and_QUEUE_verified':True,
            'native_final_ref_UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),
            'coherent_before_after_ref':True,'CAS_or_completion_inferred_from_ancestry':False,
            'perpetual_or_write_time_Main_equality_claimed':False}


def sync(rt,api,journal,cas_ref):
    e,h=rt.e,rt.h;rt.refresh()
    actual=actual_cas(rt,cas_ref,api)
    verify_immutable(rt,api)
    pointer=NATIVE/'ROOT_ACTUAL_CONCURRENT_ADOPTION100_POINTER.json'
    need(not pointer.exists() and not pointer.is_symlink(),'Actual pointer already exists')
    with e.WriterLock(rt.m['writer_lock']) as lock:
        def guard():
            lock.check();rt.refresh()
            now=actual_cas(rt,cas_ref,api)
            need(h.exact(now,actual),'Actual Root CAS envelope changed')
            local_states(rt,resume=True)
            observation=main_closure(rt,api)
            local_states(rt,resume=True);lock.check()
            need(api('GET','git/ref/heads/main')['object']['sha']==observation['actual_MAIN_observed'],
                 'Main moved after owned closure/local guard; no local effect permitted')
            observation['native_final_ref_UTC']=datetime.datetime.now(datetime.timezone.utc).isoformat()
            return observation
        guard()
        e.put(journal,'SYNC_INTENT.json',{'admission_pin':rt.admission_pin,'actual_CAS_pin':{k:cas_ref[k] for k in ('bytes','sha256')},
            'semantics':'Five per-file atomic installs under original lock; mixed exact pre/post resumable, never a five-file transaction.'})
        for index,row in enumerate(rt.m['local_views']):
            guard();path=CHECKOUT/row['path'];body=rt.overlay[row['path']];post=pin(body)
            if e.local_pin(h,path)!=post:
                with e.ParentHandle(path) as parent:
                    temp='.pr211-concurrent-'+journal.name+'-'+str(index)+'.tmp'
                    guard();parent.check()
                    fd=os.open(temp,os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW,0o444,dir_fd=parent.fd)
                    try:
                        with os.fdopen(fd,'wb',closefd=False) as stream:
                            need(stream.write(body)==len(body),'Short current-view temporary write')
                            stream.flush();os.fchmod(fd,0o444);os.fsync(fd)
                    finally:os.close(fd)
                    guard();parent.check()
                    need(h.exact(e.local_pin(h,path),row['preimage']),'Local preimage changed before atomic install')
                    if row['preimage'] is None:
                        os.link(temp,path.name,src_dir_fd=parent.fd,dst_dir_fd=parent.fd,follow_symlinks=False)
                        os.unlink(temp,dir_fd=parent.fd)
                    else:os.replace(temp,path.name,src_dir_fd=parent.fd,dst_dir_fd=parent.fd)
                    parent.check();os.fsync(parent.fd)
            need(h.exact(e.local_pin(h,path),post),'Installed current-view postimage differs')
            observation=guard()
            e.put(journal,'VIEW_'+str(index)+'.json',{'path':row['path'],'postimage':post,'native_observation':observation})
        local_states(rt,all_post=True);observation=guard();local_states(rt,all_post=True)
        receipt={'schema':'pr211-concurrent-actual-five-sync-v1','evidence_scope':'ACTUAL_SYNC_REQUIRES_EXTERNAL_ROOT_TERMINAL_ACCEPTANCE',
            'PR':211,'protocol_pin':rt.seed.source_pin,'source_manifest_pin':rt.seed.source_manifest_pin,
            'admission_pin':rt.admission_pin,'actual_CAS_pin':{k:cas_ref[k] for k in ('bytes','sha256')},
            'CAS_target':rt.admission['candidate'],'CAS_target_tree':rt.admission['tree'],**observation,
            'all_five_local_postimages_verified':True,'facts':rt.m['facts'],'external_Root_terminal_acceptance_inferred':False}
        e.put(journal,'ACTUAL_FIVE_SYNC.json',receipt)
        observation=guard();local_states(rt,all_post=True)
        e.put(NATIVE,pointer.name,{'schema':'pr211-concurrent-actual-five-pointer-v1','evidence_scope':'ACTUAL_SYNC_NOT_EXTERNAL_ROOT_TERMINAL_ACCEPTANCE',
            'protocol_pin':rt.seed.source_pin,'admission_pin':rt.admission_pin,
            'actual_CAS_pin':{k:cas_ref[k] for k in ('bytes','sha256')},'sync_path':str(journal/'ACTUAL_FIVE_SYNC.json'),
            'sync_pin':pin(enc(receipt)),**observation,'all_five_local_postimages_verified':True,
            'recorded_under_original_stable_lock':True,'external_Root_terminal_acceptance_inferred':False})
        return receipt


def read_journal(e,name,prefix):
    need(type(name) is str and name.startswith(prefix) and len(name)<=80,'Exact new read/sync journal prefix')
    return e.journal_new(name)


def checked_pointer(rt,cas_ref):
    raw,unused=rt.seed.s.read_regular(NATIVE/'ROOT_ACTUAL_CONCURRENT_ADOPTION100_POINTER.json')
    pointer=rt.h.decode(raw)
    rt.h.matches(pointer,{'schema':'pr211-concurrent-actual-five-pointer-v1',
        'evidence_scope':'ACTUAL_SYNC_NOT_EXTERNAL_ROOT_TERMINAL_ACCEPTANCE','protocol_pin':rt.seed.source_pin,
        'admission_pin':rt.admission_pin,'actual_CAS_pin':{k:cas_ref[k] for k in ('bytes','sha256')},
        'CAS_target':rt.admission['candidate'],'CAS_target_tree':rt.admission['tree'],
        'all_five_local_postimages_verified':True,'recorded_under_original_stable_lock':True,
        'external_Root_terminal_acceptance_inferred':False},'Exact actual-sync pointer required before terminal readout')
    path=Path(pointer['sync_path'])
    need(path.parent.parent==NATIVE and path.parent.name.startswith('ROOT_CONCURRENT_SYNC_')
         and path.name=='ACTUAL_FIVE_SYNC.json','Exact actual sync journal pointer')
    proof=ref(rt.h,rt.seed.s,{'path':str(path),**pointer['sync_pin']})
    rt.h.matches(proof,{'schema':'pr211-concurrent-actual-five-sync-v1',
        'evidence_scope':'ACTUAL_SYNC_REQUIRES_EXTERNAL_ROOT_TERMINAL_ACCEPTANCE',
        'protocol_pin':rt.seed.source_pin,'admission_pin':rt.admission_pin,
        'actual_CAS_pin':{k:cas_ref[k] for k in ('bytes','sha256')},'CAS_target':rt.admission['candidate'],
        'CAS_target_tree':rt.admission['tree'],'all_five_local_postimages_verified':True,
        'facts':rt.m['facts'],'external_Root_terminal_acceptance_inferred':False},'Actual sync receipt association differs')
    return pin(raw)


def propose(seed,api,date,journal_name):
    """Read-only admission proposal; never a Root gate or native object."""
    h=seed.h;seed.refresh()
    parent=api('GET','git/ref/heads/main')['object']['sha']
    need(h.hexid(parent),'Actual proposed parent')
    commit=api('GET','git/commits/'+parent)
    need(commit.get('sha')==parent and h.hexid(commit['tree']['sha']),'Actual proposed root')
    a={'schema':'pr211-concurrent-parent-admission-v1','PR':211,
       'evidence_scope':'FACTUAL_PARENT_ADMISSION_REQUIRES_ROOT_ACCEPTANCE','protocol_pin':seed.source_pin,
       'source_manifest_pin':seed.source_manifest_pin,'logical_manifest_pin':MP,'logical_gate_pin':GP,
       'cache_manifest_pin':CM,'cache_acceptance_pin':CA,'facts':seed.logical['facts'],
       'parent':parent,'parent_tree':commit['tree']['sha'],'parents':[parent],'created_UTC':date,
       'commit_author':{**seed.logical['commit_author'],'date':date},
       'commit_committer':{**seed.logical['commit_committer'],'date':date},'commit_message':seed.logical['commit_message'],
       'tree':'0'*40,'candidate':'0'*40,'candidate_journal':journal_name}
    # Temporary pure context has no mutation method and creates no synthetic ref observation.
    q=types.SimpleNamespace(seed=seed,h=h,e=seed.e,c=seed.c,m={**seed.logical,'expected_parent':parent,
        'expected_parent_tree':commit['tree']['sha']},overlay=seed.overlay,pre=seed.pre,reused=seed.reused,bodies=seed.bodies)
    with seed.e.WriterLock(seed.logical['writer_lock']) as lock:
        local_states(q);tree,unused,unused_dirs=parent_state(q,api)
        a['tree']=tree
        m={**q.m,'commit_author':a['commit_author'],'commit_committer':a['commit_committer']}
        unused,a['candidate']=h.commit_request(m,tree,[parent])
        checked_admission(seed,a);seed.refresh();local_states(q);lock.check()
        need(api('GET','git/ref/heads/main')['object']['sha']==parent,'Admission observation became stale; no silent rebind')
    return a


def main():
    need(sys.flags.ignore_environment and sys.flags.no_site and sys.dont_write_bytecode and sys.flags.safe_path
         and not sys.flags.optimize,'Use Python -E -S -B -P without optimization')
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action',choices=('admit','candidate','verify','preCAS','hold-CAS','postcheck','sync','terminal'))
    parser.add_argument('--admission');parser.add_argument('--admission-bytes',type=int);parser.add_argument('--admission-sha256')
    parser.add_argument('--Root-gate');parser.add_argument('--Root-gate-bytes',type=int);parser.add_argument('--Root-gate-sha256')
    parser.add_argument('--preCAS-acceptance');parser.add_argument('--preCAS-acceptance-bytes',type=int);parser.add_argument('--preCAS-acceptance-sha256')
    parser.add_argument('--actual-CAS');parser.add_argument('--actual-CAS-bytes',type=int);parser.add_argument('--actual-CAS-sha256')
    parser.add_argument('--journal');parser.add_argument('--commit-date');parser.add_argument('--candidate-journal')
    args=parser.parse_args();seed=Seed();h,e=seed.h,seed.e
    def supplied(prefix):
        name=prefix.replace('-','_')
        return {'path':getattr(args,name),'bytes':getattr(args,name+'_bytes'),'sha256':getattr(args,name+'_sha256')}
    if args.action=='admit':
        journal=read_journal(e,args.journal,'ROOT_CONCURRENT_READ_');api=e.API(h,journal,mutate=False)
        result=propose(seed,api,args.commit_date,args.candidate_journal)
        e.put(journal,'ADMISSION.json',result)
    else:
        rt=Runtime(seed,supplied('admission'),supplied('Root-gate'))
        if args.action=='candidate':
            need(args.journal is None,'Mutation journal only from accepted admission')
            result=candidate(rt)
        else:
            prefix='ROOT_CONCURRENT_SYNC_' if args.action=='sync' else 'ROOT_CONCURRENT_READ_'
            journal=read_journal(e,args.journal,prefix);api=e.API(h,journal,mutate=False)
            if args.action=='verify':
                rt.refresh();result=verify_immutable(rt,api);rt.refresh();e.put(journal,'VERIFIED.json',result)
            elif args.action=='preCAS':
                accepted_verifications(rt,supplied('preCAS-acceptance'))
                with e.WriterLock(rt.m['writer_lock']) as lock:lease_guard(rt,api,lock)
                result={'schema':'pr211-concurrent-preCAS-fresh-lease-observation-v1','parent':rt.admission['parent'],
                        'candidate':rt.admission['candidate'],'expected_sha':rt.admission['parent'],'force':False,
                        'ref_writer_exists':False,'observation_is_not_atomic_CAS_or_future_lease':True}
                e.put(journal,'PRECAS_FRESH_OBSERVATION.json',result)
            elif args.action=='hold-CAS':result=hold_CAS(rt,api,journal,supplied('preCAS-acceptance'))
            elif args.action=='sync':result=sync(rt,api,journal,supplied('actual-CAS'))
            else:
                rt.refresh();actual_cas(rt,supplied('actual-CAS'),api);verify_immutable(rt,api)
                with e.WriterLock(rt.m['writer_lock']) as lock:
                    local_states(rt,resume=True,all_post=args.action=='terminal')
                    if args.action=='terminal':checked_pointer(rt,supplied('actual-CAS'))
                    result=main_closure(rt,api);lock.check()
                    rt.refresh();actual_cas(rt,supplied('actual-CAS'),api)
                    local_states(rt,resume=True,all_post=args.action=='terminal')
                    need(api('GET','git/ref/heads/main')['object']['sha']==result['actual_MAIN_observed'],
                         'Main moved after dated reconciliation; no terminal/readout receipt')
                    result['native_final_ref_UTC']=datetime.datetime.now(datetime.timezone.utc).isoformat()
                    result['external_Root_terminal_acceptance_inferred']=False
                    e.put(journal,args.action.upper()+'.json',result)
    print(json.dumps(result,sort_keys=True,indent=2))


if __name__=='__main__':main()
