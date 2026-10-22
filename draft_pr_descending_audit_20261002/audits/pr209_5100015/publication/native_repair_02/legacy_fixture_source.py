"""Exact native-source workflow probes. All provider calls are in-memory.

The copied binding fixture creates synthetic sealed review/publication/tracker
ancestry using the exact current other four helper sources. Native sources are
compiled unchanged. No live gh/gws/publication calls or local Git actions occur.
"""
from pathlib import Path, PurePosixPath
from datetime import datetime, timezone
import base64, builtins, copy, hashlib, json, sys, types, zipfile, traceback
import binding_fixture_source as b
from archive_completed_group import archive_completed_group

HERE = Path(__file__).resolve().parent
b.HERE = HERE
b.PUB = HERE.parent
b.SOURCE = {n: (b.PUB / n).read_bytes() for n in b.NAMES}
b.RUNS = HERE / 'probe_runs_06'
b.SNAP = HERE / 'source_snapshot_06'
OLD = 'fd09a95b479f376234835a4494693bb1316c85ec'
PREFIX = 'unsolved_math_prioritization/attempts/5100015/'
QUEUE = 'unsolved_math_prioritization/QUEUE.md'
ROW = '| 222 | 5100015 / AMR-050-0015 | Elliptic-billiard invariant k_{303,b} | 0.1905 | 5.0 | 3 | 2021 | claimed_solved | 1/5 |  |  |  |'
RESULTS = []
def blob(raw): return hashlib.sha1(b'blob ' + str(len(raw)).encode() + b'\0' + raw).hexdigest()


class Fixture(b.Fixture):
    def __init__(self, label, extras=0, omit_original=False, compiler_log=False):
        super().__init__(label)
        self.root = self.base
        self.nodes, self.commits, self.filetrees = {}, {}, {}
        self.native_calls, self.mutations = [], []
        self.ignore_metadata = self.unknown_metadata = self.unknown_object = False
        self.unknown_ref = False
        self.unknown_ready = self.unknown_merge_object = False
        self.races_before_request = 0
        self.raced_attempts = []
        self.unknown_main = self.race_on_main = self.corrupt_merge = self.delay_event = False
        self.protected = False
        u = self.r / 'pr_update/5100015'
        u.mkdir(parents=True)
        for name in ['PROOF.md', 'STATUS.md', 'README.md', 'RESEARCH_LOG.md']:
            (u / name).write_text('SYNTHETIC reviewed science ' + name + '\n')
        b.dump(u / 'readiness.json', {'synthetic': True})
        original = []
        original_files = {}
        for k in range(23):
            name = '.gitignore' if k == 0 else f'original_{k:02d}.txt'
            raw = ('SYNTHETIC original ' + str(k) + '\n').encode()
            original_files[PREFIX + name] = raw
            original.append(dict(native_path=PREFIX + name, native_blob=blob(raw), native_mode='100644', bytes=len(raw), sha256=b.sha(raw)))
            if not (omit_original and k == 22):
                p = u / 'history/original_submission_20261016' / name
                p.parent.mkdir(parents=True, exist_ok=True)
                p.write_bytes(raw)
        for k in range(extras):
            (self.r / f'bulk_{k:04d}.txt').write_text('SYNTHETIC explicitly frozen/exported large delta\n' + str(k))
        queue = (ROW + '\n| foreign | exact preserved row |\n').encode()
        self.intake = dict(head=OLD, branch='dot/math-5100015', native_source_prefix=PREFIX,
            Queue_blob=blob(queue), Queue_sha256=b.sha(queue), queue_row=ROW, original_source_files=original)
        b.dump(self.c / 'initial_review_20261016/INTAKE.json', self.intake)
        source_files = [p for p in sorted(self.r.rglob('*')) if p.is_file() and p.name not in
            {'SOURCE_MANIFEST.json', 'PACKAGE_MANIFEST.json', 'deposit.json', 'FINAL_CLEARANCE.json', 'k303b-source-verification.zip'}]
        b.dump(self.r / 'SOURCE_MANIFEST.json', {'files': [b.pin(p, self.r) for p in source_files]})
        with zipfile.ZipFile(self.r / 'k303b-source-verification.zip', 'w') as archive:
            for p in [*source_files, self.r / 'SOURCE_MANIFEST.json']:
                archive.write(p, 'k303b_outer_center_pedal_product/' + p.relative_to(self.r).as_posix())
        package = dict(submission_files=[b.pin(self.r / x['path'], self.r) for x in self.maps],
            source_manifest=b.pin(self.r / 'SOURCE_MANIFEST.json', self.r),
            manuscript_source=b.pin(self.r / 'manuscript.tex', self.r), metadata=b.pin(self.r / 'metadata.json', self.r))
        b.dump(self.r / 'PACKAGE_MANIFEST.json', package)
        # Preserve the preliminary generic setup seals; rebuild reviews against
        # the actual synthetic native ZIP after those fixture-only changes.
        for name in ['whole1', 'whole2']:
            (self.c / name).rename(self.base / ('preliminary_' + name))
        self.core = self.rb.current_core(self.r)
        whole = self.reviews('whole', self.core)
        prior_raw = json.dumps(dict(PR=210, case_completion_percent=100, counts=[44,21,21,0],
            actual_publication_tracker_native_merge_complete=True,
            actual_both_public_size_SHA256_verified=True, single_append_all_four_cells_verified=True)).encode()
        prior = self.pub / 'progress_baseline_01/ACCEPTANCE.json'
        prior.parent.mkdir()
        prior.write_bytes(prior_raw)
        prior_path = 'prior_case/ROOT_FINAL_CASE_ACCEPTANCE.json'
        self.commits['prior-checkpoint'] = dict(tree={'sha': self.tree({prior_path: prior_raw})}, parents=[])
        checkpoint = self.pub / 'progress_baseline_01/CHECKPOINT.json'
        b.dump(checkpoint, dict(commit='prior-checkpoint', main_readback='prior-checkpoint',
            owned_files=[dict(path=prior_path, bytes=len(prior_raw), sha256=b.sha(prior_raw), git_blob_sha1=blob(prior_raw))]))
        b.dump(self.pub / 'PROGRESS_BASELINE.json', dict(schema='pr209-descending-progress-baseline-v1',
            scope='own_descending_shard', counts=[44,21,21,0], previous_completed_PR=210, current_PR=209,
            previous_case_acceptance=b.pin(prior,self.c), previous_native_checkpoint_receipt=b.pin(checkpoint,self.c),
            authenticated_native_checkpoint='prior-checkpoint', authenticated_acceptance_git_blob_sha1=blob(prior_raw),
            actual_native_acceptance_body_byte_identical=True))
        if compiler_log:
            (self.r/'manuscript.log').write_text('SYNTHETIC explicitly sealed frozen compiler log\n')
        public = [p for p in self.c.rglob('*') if p.is_file() and p.name not in
            {'PUBLIC_EXPORT_MANIFEST.json', 'FINAL_CLEARANCE.json'}]
        b.dump(self.pub / 'PUBLIC_EXPORT_MANIFEST.json', dict(schema='pr209-public-export-manifest-v1',
            files=[b.pin(p,self.c) for p in sorted(public)]))
        self.clear.update(whole_package_reviews=whole, submission_files=package['submission_files'],
            source_manifest=package['source_manifest'], manuscript_source=package['manuscript_source'],
            package_manifest_sha256=b.sha((self.r/'PACKAGE_MANIFEST.json').read_bytes()),
            public_export_manifest=b.pin(self.pub/'PUBLIC_EXPORT_MANIFEST.json',self.c),
            progress_baseline=b.pin(self.pub/'PROGRESS_BASELINE.json',self.c))
        self.save_clear()
        self.ctx = self.rb.context(self.r)
        self.pr = dict(number=209, state='open', draft=True, merged=False, mergeable=True,
            node_id='PR209', html_url='https://github.com/AlecKriebel/Math/pull/209',
            title='SYNTHETIC stale title', body='SYNTHETIC stale focal theorem; first proof claim',
            head=dict(sha=OLD, ref='dot/math-5100015', repo={'full_name':'AlecKriebel/Math'}),
            base=dict(ref='main', repo={'full_name':'AlecKriebel/Math'}))
        self.commits[OLD] = dict(tree={'sha': self.tree({QUEUE:queue, **original_files})}, parents=[])
        self.main_head = 'main-initial'
        self.mainfiles = {QUEUE:queue, 'foreign-preserved.txt': b'SYNTHETIC foreign main file\n'}
        self.commits[self.main_head] = dict(tree={'sha':self.tree(self.mainfiles)}, parents=[])
        self.publish()
        self.append()

    def imp(self, name, globals=None, locals=None, fromlist=(), level=0):
        if name in {'integrate_reviewed_pr', 'append_verified_tracker'}:
            return self.module(name + '.py')
        if name == 'pathlib':
            return types.SimpleNamespace(Path=lambda *a: self.root if a == ('/Users/alec/Documents/Math',) else Path(*a), PurePosixPath=PurePosixPath)
        return super().imp(name,globals,locals,fromlist,level)

    def urlopen(self,url,**kw):
        response=super().urlopen(url,**kw)
        phase=getattr(self,'mutate_during_public',None)
        prepared=(self.pub/'PR_PREPARED.json').exists()
        ready=(self.pub/'NATIVE_READY_ATTEMPT.json').exists()
        objects=bool(list((self.pub/'private_transport/native_merge_attempts').glob('*/OBJECTS_BUILT.json')))
        trigger=(phase=='prepare' and not prepared and (self.pub/'NATIVE_METADATA_ATTEMPT.json').exists()) or (phase=='ready' and prepared and not ready) or (phase=='merge' and objects)
        if trigger:
            self.pr['body']='SYNTHETIC stale first-proof claim changed during public readback'
            self.mutate_during_public=None
        return response

    def tree(self, files):
        nested = {}
        for path, value in files.items():
            cur = nested
            parts = path.split('/')
            for part in parts[:-1]: cur = cur.setdefault(part,{})
            cur[parts[-1]] = value
        def rec(d):
            rows=[]
            for name,value in sorted(d.items()):
                if isinstance(value,dict):
                    rows.append(dict(path=name, mode='040000', type='tree', sha=rec(value)))
                else:
                    raw, mode = value if isinstance(value,tuple) else (value,'100644')
                    key=blob(raw); self.nodes[key]=raw
                    rows.append(dict(path=name,mode=mode,type='blob',sha=key))
            key='tree-'+b.sha(json.dumps(rows,sort_keys=True).encode())
            self.nodes[key]=dict(truncated=False,tree=rows)
            return key
        key=rec(nested); self.filetrees[key]=dict(files)
        return key

    def ancestor(self, ancestor, child):
        if ancestor == child: return True
        return any(self.ancestor(ancestor,p['sha']) for p in self.commits[child]['parents'])

    def advance(self, additions):
        old=self.main_head
        files=dict(self.filetrees[self.commits[old]['tree']['sha']]); files.update(additions)
        self.main_head='main-advance-'+str(len(self.commits))
        self.commits[self.main_head]=dict(tree={'sha':self.tree(files)},parents=[{'sha':old}])

    def native(self, method, path, payload):
        self.native_calls.append(dict(method=method,path=path,payload=payload))
        if method != 'GET':
            event=dict(method=method,path=path,
                object_intent=(self.pub/'NATIVE_OBJECT_BUILD_INTENT.json').exists(),
                merge_object_intent=bool(list((self.pub/'private_transport/native_merge_attempts').glob('*/OBJECT_INTENT.json'))),
                ref_intent=(self.pub/'NATIVE_PREPARE_ATTEMPT.json').exists(),
                metadata_intent=(self.pub/'NATIVE_METADATA_ATTEMPT.json').exists(),
                main_intent=(self.pub/'NATIVE_MERGE_REQUEST.json').exists())
            self.mutations.append(event)
        if method=='GET':
            if path=='pulls/209': return copy.deepcopy(self.pr)
            if path=='git/ref/heads/main':
                folders=sorted((self.pub/'private_transport/native_merge_attempts').glob('[0-9][0-9][0-9][0-9]'))
                if folders and self.races_before_request and not (self.pub/'NATIVE_MERGE_REQUEST.json').exists():
                    folder=folders[-1]
                    if (folder/'OBJECTS_BUILT.json').exists() and not (folder/'ABANDONED_BEFORE_MAIN.json').exists() and folder.name not in self.raced_attempts:
                        self.raced_attempts.append(folder.name);self.races_before_request-=1
                        queue=self.filetrees[self.commits[self.main_head]['tree']['sha']][QUEUE]
                        self.advance({'foreign-before-ref-'+folder.name+'.txt':b'SYNTHETIC safe foreign main advance',
                            QUEUE:queue+('| foreign | safe row '+folder.name+' |\n').encode()})
                return {'object':{'sha':self.main_head}}
            if path=='git/ref/heads/dot/math-5100015': return {'object':{'sha':self.pr['head']['sha']}}
            if path.startswith('git/commits/'): return copy.deepcopy(self.commits[path[len('git/commits/'):]])
            if path.startswith('git/trees/'): return copy.deepcopy(self.nodes[path[len('git/trees/'):]])
            if path.startswith('git/blobs/'):
                key=path[len('git/blobs/'):];raw=self.nodes[key]
                return dict(sha=key,size=len(raw),encoding='base64',content=base64.b64encode(raw).decode())
            if path.startswith('branches/'): return {'protected':self.protected}
            if path.startswith('rules/branches/') or path=='rulesets': return []
            if path.startswith('compare/'):
                a,c=path[len('compare/'):].split('...')
                return dict(status='ahead',merge_base_commit={'sha':a}) if self.ancestor(a,c) else dict(status='diverged')
        if method=='POST' and path=='git/blobs':
            raw=base64.b64decode(payload['content']);key=blob(raw);self.nodes[key]=raw
            if self.unknown_object:
                error=TimeoutError('SYNTHETIC unknown first object creation')
                error.stdout=b'SYNTHETIC partial stdout\xff\x00';error.stderr=b'SYNTHETIC partial stderr\xfe\x00'
                raise error
            if self.unknown_merge_object and list((self.pub/'private_transport/native_merge_attempts').glob('*/OBJECT_INTENT.json')):
                raise TimeoutError('SYNTHETIC unknown merge blob creation')
            return {'sha':key}
        if method=='POST' and path=='git/trees':
            files=dict(self.filetrees[payload['base_tree']])
            for row in payload['tree']:
                raw=row['content'].encode() if 'content' in row else self.nodes[row['sha']]
                files[row['path']]=(raw,row['mode']) if row['mode']!='100644' else raw
            key=self.tree(files)
            if self.unknown_object: raise TimeoutError('SYNTHETIC unknown first tree creation')
            return {'sha':key}
        if method=='POST' and path=='git/commits':
            key='commit-'+str(len(self.commits))
            self.commits[key]=dict(tree={'sha':payload['tree']},parents=[{'sha':p} for p in payload['parents']])
            return {'sha':key}
        if method=='PATCH' and path=='git/refs/heads/dot/math-5100015':
            assert payload['force'] is False and self.ancestor(self.pr['head']['sha'],payload['sha'])
            self.pr['head']['sha']=payload['sha']
            if self.unknown_ref: raise TimeoutError('SYNTHETIC unknown branch ref PATCH after accepted update')
            return {'object':{'sha':payload['sha']}}
        if method=='PATCH' and path=='pulls/209':
            if not self.ignore_metadata: self.pr.update(payload)
            if self.unknown_metadata: raise TimeoutError('SYNTHETIC unknown metadata PATCH outcome')
            return copy.deepcopy(self.pr)
        if method=='POST' and path=='graphql':
            self.pr['draft']=False
            if self.unknown_ready: raise TimeoutError('SYNTHETIC unknown ready outcome')
            return {'data':{'markPullRequestReadyForReview':{'pullRequest':{'id':'PR209','isDraft':False}}}}
        if method=='PATCH' and path=='git/refs/heads/main':
            assert payload['force'] is False
            if self.race_on_main: self.advance({'foreign-concurrent.txt':b'SYNTHETIC concurrent main race'})
            if not self.ancestor(self.main_head,payload['sha']): raise RuntimeError('SYNTHETIC nonforce main update rejected concurrent advance')
            self.main_head=payload['sha']
            if not self.delay_event: self.mark_merged()
            if self.corrupt_merge:
                files=dict(self.filetrees[self.commits[self.main_head]['tree']['sha']])
                files[PREFIX+'UNREVIEWED_AFTER_MERGE.txt']=b'SYNTHETIC corrupt resulting tree'
                self.commits[self.main_head]['tree']['sha']=self.tree(files)
            if self.unknown_main: raise TimeoutError('SYNTHETIC unknown main PATCH after accepted update')
            return {'object':{'sha':payload['sha']}}
        raise RuntimeError('Unimplemented synthetic native call '+repr((method,path,payload)))

    def mark_merged(self):
        self.pr.update(merged=True,state='closed',merge_commit_sha=self.main_head)

    def run(self,args,**kw):
        if Path(args[0]).name=='gh' and '--method' in args:
            method=args[args.index('--method')+1]
            path=args[args.index('--method')+2].removeprefix('repos/AlecKriebel/Math/')
            payload=json.loads(Path(args[args.index('--input')+1]).read_text()) if '--input' in args else None
            result=self.native(method,path,payload)
            return types.SimpleNamespace(returncode=0,stdout=json.dumps(result).encode(),stderr=b'')
        return super().run(args,**kw)

    def prepare(self,reconcile=False):
        return self.module('integrate_reviewed_pr.py').main(['--reconcile'] if reconcile else [])
    def merge(self,reconcile=False):
        return self.module('verify_and_merge.py').main(['--reconcile'] if reconcile else [])
    def resume(self):
        return self.module('verify_and_merge.py').main(['--resume-before-main'])
    def trace(self):
        b.dump(self.base/'PROVIDER_TRACE.json',dict(native_calls=self.native_calls,mutations=self.mutations,
            pr=self.pr,main=self.main_head,sheet=self.sheet,other_calls=self.calls))


def test(label,fn):
    try: detail=fn(); item=dict(label=label,status='PASS',detail=detail)
    except Exception as e: item=dict(label=label,status='FAIL',error=repr(e),traceback=traceback.format_exc())
    RESULTS.append(item);b.dump(HERE/'PROBE_RESULTS_06.json',RESULTS);print(json.dumps(item),flush=True)


def baseline():
    f=Fixture('baseline');f.prepare();f.advance({'foreign-added.txt':b'SYNTHETIC foreign concurrent work',
        QUEUE:f.mainfiles[QUEUE]+b'| other | new foreign queue row |\n'})
    f.merge();f.trace();r=json.loads((f.pub/'PR_MERGED.json').read_text())
    merged=f.filetrees[f.commits[f.main_head]['tree']['sha']]
    assert r['program_counts']==[45,22,22,0] and r['program_count_scope']=='own_descending_shard'
    assert merged['foreign-added.txt']==b'SYNTHETIC foreign concurrent work' and b'new foreign queue row' in merged[QUEUE]
    assert not (f.pub/'native_current_source').exists()
    for e in f.mutations:
        if e['path'].startswith('git/') and e['method']=='POST': assert e['object_intent']
        if e['path']=='git/refs/heads/dot/math-5100015': assert e['ref_intent']
        if e['path']=='pulls/209': assert e['metadata_intent']
        if e['path']=='git/refs/heads/main': assert e['main_intent'] and e['merge_object_intent']
    return dict(complete=True,pins=len(r['exact_native_body_readbacks']),foreign_paths_rows_preserved=True,all_intents_precede_writes=True)


def payloads():
    out={}
    for name in ['preprint/UNREVIEWED.txt','publication/.env']:
        f=Fixture('payload_'+Path(name).name.replace('.','_'));(f.c/name).write_text('SYNTHETIC forbidden payload')
        out[name]=b.reject(f.prepare);assert not f.mutations;f.trace()
    return out


def forged_prepared():
    f=Fixture('forged_prepared');b.dump(f.pub/'PR_PREPARED.json',dict(prepared_head=OLD,included_owned_pins=[]))
    error=b.reject(f.merge);assert not f.mutations;f.trace();return error


def metadata():
    out={}
    f=Fixture('stale_metadata');f.ignore_metadata=True
    out['ignored']=b.reject(f.prepare);assert not (f.pub/'PR_PREPARED.json').exists()
    out['merge_blocked']=b.reject(f.merge);f.trace()
    f=Fixture('unknown_metadata');f.unknown_metadata=True
    out['unknown']=b.reject(f.prepare);assert not (f.pub/'PR_PREPARED.json').exists()
    before=len(f.mutations);out['retry']=b.reject(f.prepare);assert len(f.mutations)==before
    f.unknown_metadata=False;f.prepare(True);assert len(f.mutations)==before
    f.pr['body']='SYNTHETIC later stale first-proof body';out['later_body']=b.reject(f.merge)
    assert len(f.mutations)==before;f.trace()
    return out


def main_boundaries():
    out={}
    for label,change in [('science',{PREFIX+'foreign.txt':b'SYNTHETIC unreviewed science'}),
        ('owned',{'case/preprint/manuscript.tex':b'SYNTHETIC foreign overwrite'}),
        ('row',{QUEUE:(ROW.replace('| 2021 |','| 2020 |')+'\n').encode()})]:
        f=Fixture('main_'+label);f.prepare();f.advance(change);before=len(f.mutations)
        out[label]=b.reject(f.merge);assert len(f.mutations)==before and not (f.pub/'PR_MERGED.json').exists();f.trace()
    return out


def large_scope():
    f=Fixture('large_scope',extras=310);f.prepare();f.merge();f.trace()
    assert not any(x['path'].startswith('compare/') for x in f.native_calls)
    p=json.loads((f.pub/'PR_PREPARED.json').read_text())
    assert len(p['included_owned_pins'])>300
    return dict(complete=True,pins=len(p['included_owned_pins']),compare_file_limit_unused=True)


def unknown_objects():
    f=Fixture('unknown_object');f.unknown_object=True;error=b.reject(f.prepare)
    assert (f.pub/'NATIVE_OBJECT_BUILD_INTENT.json').exists() and not (f.pub/'NATIVE_OBJECTS_BUILT.json').exists()
    before=len(f.mutations);retry=b.reject(f.prepare);assert len(f.mutations)==before
    recovery=b.reject(lambda:f.prepare(True));assert len(f.mutations)==before;f.trace()
    stdout=list((f.pub/'private_transport').rglob('*-partial-stdout.bin'))
    stderr=list((f.pub/'private_transport').rglob('*-partial-stderr.bin'))
    assert len(stdout)==len(stderr)==1 and stdout[0].read_bytes()==b'SYNTHETIC partial stdout\xff\x00' and stderr[0].read_bytes()==b'SYNTHETIC partial stderr\xfe\x00'
    return dict(first=error,retry=retry,readonly_recovery_pending=recovery,no_second_write=True)


def pending_ready_and_merge_objects():
    out={}
    for label,flag in [('unknown_ready','unknown_ready'),('unknown_merge_object','unknown_merge_object')]:
        f=Fixture(label);f.prepare();setattr(f,flag,True);first=b.reject(f.merge)
        assert not (f.pub/'PR_MERGED.json').exists() and not any(e['path']=='git/refs/heads/main' for e in f.mutations)
        before=len(f.mutations);retry=b.reject(f.merge);recovery=b.reject(lambda:f.merge(True))
        resumed=b.reject(f.resume)
        assert len(f.mutations)==before;f.trace();out[label]=dict(first=first,retry=retry,readonly_pending=recovery,no_second_write=True)
    return out


def merge_races():
    out={}
    for label,flag in [('concurrent_main','race_on_main'),('bad_tree','corrupt_merge'),('delayed_event','delay_event')]:
        f=Fixture(label);f.prepare();setattr(f,flag,True);error=b.reject(f.merge)
        assert not (f.pub/'PR_MERGED.json').exists() and (f.pub/'NATIVE_MERGE_REQUEST.json').exists()
        before=len(f.mutations);retry=b.reject(f.merge);assert len(f.mutations)==before
        if label=='delayed_event':
            f.mark_merged();f.merge(True);assert len(f.mutations)==before and (f.pub/'PR_MERGED.json').exists()
        else:
            b.reject(lambda:f.merge(True));assert len(f.mutations)==before
        f.trace();out[label]=dict(first=error,retry=retry,no_second_write=True)
    return out


def unknown_main():
    f=Fixture('unknown_main');f.prepare();f.unknown_main=True;first=b.reject(f.merge)
    assert not (f.pub/'PR_MERGED.json').exists();before=len(f.mutations)
    b.reject(f.merge);f.unknown_main=False;f.merge(True);assert len(f.mutations)==before
    receipt=json.loads((f.pub/'PR_MERGED.json').read_text());assert receipt['program_counts']==[45,22,22,0]
    f.merge(True);assert len(f.mutations)==before;f.trace()
    return dict(first=first,readonly_recovery=True,no_second_main_write=True,counters_increment_once=True)


def remaining_guards():
    out={}
    f=Fixture('original_missing',omit_original=True);out['original_missing']=b.reject(f.prepare);assert not f.mutations;f.trace()
    f=Fixture('rules');f.prepare();f.protected=True;out['active_rules']=b.reject(f.merge)
    assert not any(x['path']=='git/refs/heads/main' for x in f.mutations);f.trace()
    f=Fixture('mode');f.prepare();head=f.pr['head']['sha'];files=dict(f.filetrees[f.commits[head]['tree']['sha']]);files[PREFIX+'PROOF.md']=(files[PREFIX+'PROOF.md'],'100755')
    f.commits[head]['tree']['sha']=f.tree(files)
    # Make the mutable native object/ref/metadata chain internally consistent;
    # the independent expected byte/mode derivation must still reject it.
    built=json.loads((f.pub/'NATIVE_OBJECTS_BUILT.json').read_text());built['tree']=f.commits[head]['tree']['sha']
    b.dump(f.pub/'NATIVE_OBJECTS_BUILT.json',built)
    ref=json.loads((f.pub/'NATIVE_PREPARE_ATTEMPT.json').read_text());ref['tree']=built['tree'];ref['object_build_receipt_sha256']=b.sha((f.pub/'NATIVE_OBJECTS_BUILT.json').read_bytes())
    b.dump(f.pub/'NATIVE_PREPARE_ATTEMPT.json',ref)
    meta=json.loads((f.pub/'NATIVE_METADATA_ATTEMPT.json').read_text());meta['ref_intent_sha256']=b.sha((f.pub/'NATIVE_PREPARE_ATTEMPT.json').read_bytes());b.dump(f.pub/'NATIVE_METADATA_ATTEMPT.json',meta)
    before=len(f.mutations)
    out['wrong_mode']=b.reject(f.merge);assert len(f.mutations)==before;f.trace()
    return out


def branch_unknown_and_placeholder():
    f=Fixture('unknown_ref');f.unknown_ref=True;first=b.reject(f.prepare)
    assert (f.pub/'NATIVE_PREPARE_ATTEMPT.json').exists() and not (f.pub/'PR_PREPARED.json').exists()
    before=len(f.mutations);retry=b.reject(f.prepare);recovery=b.reject(lambda:f.prepare(True))
    assert len(f.mutations)==before;f.trace()
    g=Fixture('queued_placeholder');fields=ROW.split('|');fields[8]=' queued ';fields[9]=' 0/5 '
    for n in [10,11,12]: fields[n]='  '
    g.advance({QUEUE:('|'.join(fields)+'\n| foreign | preserved placeholder row |\n').encode()})
    g.prepare();g.merge();g.trace()
    r=json.loads((g.pub/'PR_MERGED.json').read_text())
    assert '| 2021 | claimed_solved | 1/5 |' in r['exact_queue_row']
    return dict(unknown_ref=first,retry=retry,readonly_pending=recovery,placeholder_completed=True,no_second_ref_write=True)


def safe_advance_recovery():
    f=Fixture('safe_advance_recovery',compiler_log=True);f.prepare();f.races_before_request=2
    first=b.reject(f.merge);assert not (f.pub/'NATIVE_MERGE_REQUEST.json').exists()
    folder=f.pub/'private_transport/native_merge_attempts/0001'
    old={p.name:p.read_bytes() for p in folder.iterdir()}
    second=b.reject(f.resume);assert not (f.pub/'NATIVE_MERGE_REQUEST.json').exists()
    assert old=={p.name:p.read_bytes() for p in folder.iterdir()}
    f.resume();f.trace()
    assert old=={p.name:p.read_bytes() for p in folder.iterdir()}
    r=json.loads((f.pub/'PR_MERGED.json').read_text())
    assert r['merge_attempt_number']==3 and len(r['prior_abandoned_attempts'])==2 and r['program_counts']==[45,22,22,0]
    assert sum(e['path']=='git/refs/heads/main' for e in f.mutations)==1 and f.publishes==f.appends==1
    files=f.filetrees[f.commits[f.main_head]['tree']['sha']]
    assert files['case/preprint/manuscript.log']==(f.r/'manuscript.log').read_bytes()
    assert b'safe row 0001' in files[QUEUE] and b'safe row 0002' in files[QUEUE]
    assert files['foreign-before-ref-0001.txt']==files['foreign-before-ref-0002.txt']
    return dict(first=first,second=second,successful_attempt=3,all_old_records_byte_unchanged=True,main_ref_calls=1,
        foreign_paths_and_rows_preserved=True,explicit_compiler_log_included=True)


def recovery_rejections():
    out={}
    for label,change in [('case',{'case/preprint/manuscript.tex':b'SYNTHETIC case edit'}),
        ('queue',{QUEUE:(ROW.replace('| 2021 |','| 2020 |')+'\n').encode()})]:
        f=Fixture('resume_'+label);f.prepare();f.races_before_request=1;b.reject(f.merge)
        f.advance(change);before=len(f.mutations);out[label]=b.reject(f.resume);assert len(f.mutations)==before;f.trace()
    f=Fixture('resume_unknown_main');f.prepare();f.unknown_main=True;b.reject(f.merge);before=len(f.mutations)
    out['unknown_main']=b.reject(f.resume);assert len(f.mutations)==before;f.unknown_main=False;f.merge(True);assert len(f.mutations)==before;f.trace()
    f=Fixture('resume_rules');f.prepare();f.races_before_request=1;b.reject(f.merge);f.protected=True;before=len(f.mutations)
    out['active_rules_before_rebuild']=b.reject(f.resume);assert len(f.mutations)==before;f.trace()
    for label in ['readback','abandonment','intent']:
        f=Fixture('mutated_'+label);f.prepare();f.races_before_request=1;b.reject(f.merge)
        folder=f.pub/'private_transport/native_merge_attempts/0001'
        record=json.loads((folder/'ABANDONED_BEFORE_MAIN.json').read_text())
        if label=='readback':
            p=f.c/record['actual_main_ref_readback']['path'];p.write_bytes(p.read_bytes()+b' ')
        elif label=='abandonment':
            record['observed_queue_sha256']='0'*64;b.dump(folder/'ABANDONED_BEFORE_MAIN.json',record)
        else:
            p=folder/'OBJECT_INTENT.json';value=json.loads(p.read_text());value['prior_abandoned_attempts']=[{'forged':True}];b.dump(p,value)
        before=len(f.mutations);out[label]=b.reject(f.resume);assert len(f.mutations)==before;f.trace()
    f=Fixture('unsealed_compiler_log');(f.r/'manuscript.log').write_text('SYNTHETIC unsealed log')
    out['unsealed_compiler_log']=b.reject(f.prepare);assert not f.mutations;f.trace()
    return out


def metadata_after_public():
    out={}
    for phase in ['prepare','ready','merge']:
        f=Fixture('metadata_during_'+phase)
        if phase!='prepare':f.prepare()
        f.mutate_during_public=phase
        out[phase]=b.reject(f.prepare if phase=='prepare' else f.merge)
        assert not (f.pub/'NATIVE_MERGE_REQUEST.json').exists()
        if phase=='prepare':assert not (f.pub/'PR_PREPARED.json').exists()
        if phase=='ready':assert not any(e['path']=='graphql' for e in f.mutations)
        assert not any(e['path']=='git/refs/heads/main' for e in f.mutations)
        f.trace()
    return out


if __name__=='__main__':
    b.SNAP.mkdir(exist_ok=False)
    for name,raw in b.SOURCE.items():(b.SNAP/name).write_bytes(raw)
    b.dump(HERE/'EXACT_SOURCE_INPUTS_06.json',dict(utc=datetime.now(timezone.utc).isoformat(),case_completion_percent=55,
        files=[b.pin(b.SNAP/n,HERE) for n in b.NAMES]))
    # Suppress normal source receipts while retaining every result/provider trace.
    real=sys.stdout
    for label,fn in [('baseline',baseline),('payloads',payloads),('forged_prepared',forged_prepared),
        ('metadata',metadata),('main_boundaries',main_boundaries),('large_scope',large_scope),
        ('unknown_objects',unknown_objects),('merge_races',merge_races),('unknown_main',unknown_main),('remaining_guards',remaining_guards),
        ('branch_unknown_and_placeholder',branch_unknown_and_placeholder),('pending_ready_and_merge_objects',pending_ready_and_merge_objects),
        ('safe_advance_recovery',safe_advance_recovery),('recovery_rejections',recovery_rejections),
        ('metadata_after_public',metadata_after_public)]:
        sys.stdout=types.SimpleNamespace(write=lambda s:None,flush=lambda:None)
        try:
            test(label,fn)
        finally:sys.stdout=real
        print(json.dumps(RESULTS[-1]),flush=True)
        receipt=archive_completed_group(HERE,b.RUNS,'06_'+label)
        if receipt:print(json.dumps({'fixture_archive':receipt}),flush=True)
    raise SystemExit(0 if all(r['status']=='PASS' for r in RESULTS) else 1)
