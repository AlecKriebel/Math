--- native239_primitives.py TOP OLD
+++ native239_primitives.py TOP CURRENT
@@ -1,4 +1,4 @@
-"""Reviewed generic bounded native/descriptor primitives for inactive PR218 protocol."""
+"""Reviewed generic bounded native/descriptor primitives for inactive PR239 protocol."""
 import fcntl,hashlib,json,os,re,selectors,stat,subprocess,sys,time,types
 from pathlib import Path
 BASE=Path(__file__).absolute().parent

--- completion_checkpoint.py OLD Runtime
+++ completion_checkpoint.py CURRENT Runtime
@@ -11,12 +11,12 @@
         self.admission_pin={k:self.admission_ref[k] for k in ('bytes','sha256')}
         self.gate=ref(h,self.seed.s,self.gate_ref)
         self.gate_pin={k:self.gate_ref[k] for k in ('bytes','sha256')}
-        h.matches(self.gate,{'schema':'pr218-root-completion-admission-acceptance-v1','evidence_scope':'ACTUAL_ROOT_RECEIPT',
-            'PR':218,'accepted':True,'protocol_pin':self.seed.source_pin,'source_manifest_pin':self.seed.source_manifest_pin,
+        h.matches(self.gate,{'schema':'pr239-root-completion-admission-acceptance-v1','evidence_scope':'ACTUAL_ROOT_RECEIPT',
+            'PR':239,'accepted':True,'protocol_pin':self.seed.source_pin,'source_manifest_pin':self.seed.source_manifest_pin,
             'admission_pin':self.admission_pin,'logical_manifest_pin':self.seed.manifest_pin,'logical_gate_pin':self.seed.logical_gate_pin,
-            'facts':h.phase_facts(),'body_proof_policy':h.BODY_POLICY,'QUEUE_policy':h.QUEUE_POLICY,
+            'facts':h.phase_facts(self.m['phase']),'body_proof_policy':h.BODY_POLICY,'QUEUE_policy':h.QUEUE_POLICY,
             'parent_only_parameterization_reviewed':True,'one_use_two_immutable_POSTs_authorized':True,
-            'no_ref_writer_or_PR_action_authority':True,'exact_baseline_plus218_memberships':True,
+            'no_ref_writer_or_PR_action_authority':True,'phase95_baseline55_39_held_phase100_only239_added':True,
             'Root_full_source_read':True,'independent_source_review_accepted':True,
             'parent_only_admissions_without_new_peer_review_approved':True},'Separate exact Root completion admission acceptance')
         self.overlay,self.pre=self.seed.overlay,self.seed.pre

--- completion_checkpoint.py OLD accepted_verifications
+++ completion_checkpoint.py CURRENT accepted_verifications
@@ -1,7 +1,7 @@
 def accepted_verifications(rt,row):
     root=ref(rt.h,rt.seed.s,row);h=rt.h
-    h.matches(root,{'schema':'pr218-root-completion-preCAS-acceptance-v1','evidence_scope':'ACTUAL_ROOT_RECEIPT',
-        'PR':218,'accepted':True,'protocol_pin':rt.seed.source_pin,'admission_pin':rt.admission_pin,
+    h.matches(root,{'schema':'pr239-root-completion-preCAS-acceptance-v1','evidence_scope':'ACTUAL_ROOT_RECEIPT',
+        'PR':239,'phase':rt.m['phase'],'accepted':True,'protocol_pin':rt.seed.source_pin,'admission_pin':rt.admission_pin,
         'logical_manifest_pin':rt.seed.manifest_pin,'logical_gate_pin':rt.seed.logical_gate_pin,'candidate':rt.admission['candidate'],
         'tree':rt.admission['tree'],'immutable_candidate_verification_accepted':True,
         'independent_GET_candidate_verification_accepted':True,'body_proof_policy':h.BODY_POLICY,'QUEUE_policy':h.QUEUE_POLICY},
@@ -10,8 +10,8 @@
     need(type(reports) is list and len(reports)==2 and len({r.get('path') for r in reports})==2,'Two distinct native GET proof records')
     for row in reports:
         proof=ref(h,rt.seed.s,row)
-        h.matches(proof,{'schema':'pr218-completion-immutable-candidate-verification-v1','evidence_scope':IMMUTABLE_SCOPE,
-            'protocol_pin':rt.seed.source_pin,'source_manifest_pin':rt.seed.source_manifest_pin,'admission_pin':rt.admission_pin,
+        h.matches(proof,{'schema':'pr239-completion-immutable-candidate-verification-v1','evidence_scope':IMMUTABLE_SCOPE,
+            'phase':rt.m['phase'],'protocol_pin':rt.seed.source_pin,'source_manifest_pin':rt.seed.source_manifest_pin,'admission_pin':rt.admission_pin,
             'logical_manifest_pin':rt.seed.manifest_pin,'logical_gate_pin':rt.seed.logical_gate_pin,
             'candidate':rt.admission['candidate'],'tree':rt.admission['tree'],'parent':rt.admission['parent'],
             'parent_tree':rt.admission['parent_tree'],'full_scope_verified':True,'all_selected_native_bodies_verified':True,

--- completion_checkpoint.py OLD body_associations
+++ completion_checkpoint.py CURRENT body_associations
@@ -1,6 +1,6 @@
 def body_associations(rt,observer,trees,root,allow_foreign_rows=False):
     h=rt.h;protected(rt,trees,root,True)
-    queue=h.queue_observation(observer,trees,root,rt.m,rt.pool,allow_foreign_rows)
+    queue=h.queue_observation(observer,trees,root,rt.m,rt.pool,allow_foreign_rows,post=True)
     for row in rt.m['protected_bodies']:
         rt.pool.get(observer,row['sha'],{k:row[k] for k in ('bytes','sha256')})
     selected={}

--- completion_checkpoint.py OLD candidate
+++ completion_checkpoint.py CURRENT candidate
@@ -11,7 +11,7 @@
         entries=[{'path':path,'mode':'100644','type':'blob','content':body.decode('utf-8')}
                  for path,body in sorted(rt.overlay.items())]
         tree_request={'base_tree':rt.admission['parent_tree'],'tree':entries}
-        commit_request,oid=h.commit_request(rt.m,rt.admission['tree'],[rt.admission['parent']])
+        commit_request,oid=h.commit_request(rt.m,rt.admission['tree'],rt.admission['parents'])
         e.put(journal,'ONE_USE_ADMISSION_RESERVATION.json',{'admission_pin':rt.admission_pin,
             'protocol_pin':rt.seed.source_pin,'logical_manifest_pin':rt.seed.manifest_pin,'gate_pin':rt.gate_pin,
             'expected_tree':rt.admission['tree'],'expected_candidate':oid,

--- completion_checkpoint.py OLD checked_admission
+++ completion_checkpoint.py CURRENT checked_admission
@@ -4,22 +4,22 @@
         'logical_manifest_pin','logical_gate_pin','facts','body_proof_policy','QUEUE_policy','parent','parent_tree',
         'created_UTC','commit_author','commit_committer','commit_message','parents','tree','candidate','candidate_journal'},
         'Exact typed completion admission')
-    h.matches(a,{'schema':'pr218-completion-parent-admission-v1','PR':218,
+    h.matches(a,{'schema':'pr239-completion-parent-admission-v1','PR':239,
         'evidence_scope':'FACTUAL_PARENT_ADMISSION_REQUIRES_ROOT_ACCEPTANCE','protocol_pin':seed.source_pin,
         'source_manifest_pin':seed.source_manifest_pin,'logical_manifest_pin':seed.manifest_pin,
-        'logical_gate_pin':seed.logical_gate_pin,'facts':h.phase_facts(),'body_proof_policy':h.BODY_POLICY,
+        'logical_gate_pin':seed.logical_gate_pin,'facts':h.phase_facts(seed.logical['phase']),'body_proof_policy':h.BODY_POLICY,
         'QUEUE_policy':h.QUEUE_POLICY,'commit_message':seed.logical['commit_message']},'Admission fixed semantics')
     need(all(h.hexid(a[k]) for k in ('parent','parent_tree','tree','candidate'))
-         and h.exact(a['parents'],[a['parent']]) and a['parent'] not in (h.ORIGINAL,h.CURRENT,h.MERGED) and a['candidate'] not in RETIRED
+         and h.exact(a['parents'],h.commit_parents(seed.logical,a['parent'])) and a['parent'] not in (h.ORIGINAL,h.CURRENT) and a['candidate'] not in RETIRED
          and a['candidate'] not in seed.logical['retired_candidates'],'Only canonical one-parent archive; retired candidates forbidden')
     need(type(a['candidate_journal']) is str and len(a['candidate_journal'])<=80
-         and re.fullmatch('ROOT_COMPLETE218_CANDIDATE_[A-Za-z0-9_-]{1,50}',a['candidate_journal']) is not None,'Fresh exact one-use candidate journal')
+         and re.fullmatch('ROOT_COMPLETE239_CANDIDATE_[A-Za-z0-9_-]{1,50}',a['candidate_journal']) is not None,'Fresh exact one-use candidate journal')
     for key in ('commit_author','commit_committer'):
         need(type(a[key]) is dict and set(a[key])=={'name','email','date'},'Fixed commit identity fields')
         for k in ('name','email'):need(h.exact(a[key][k],seed.logical[key][k]),'Identity substitution refused')
         need(h.exact(a[key]['date'],a['created_UTC']),'Single explicit UTC-seconds date')
     m={**seed.logical,'expected_parent':a['parent'],'expected_parent_tree':a['parent_tree'],
-       'commit_author':a['commit_author'],'commit_committer':a['commit_committer'],'candidate_journal':a['candidate_journal']}
-    request,oid=h.commit_request(m,a['tree'],[a['parent']])
+       'commit_author':a['commit_author'],'commit_committer':a['commit_committer'],'candidate_journal':a['candidate_journal'],'expected_candidate':a['candidate'],'expected_tree':a['tree']}
+    request,oid=h.commit_request(m,a['tree'],a['parents'])
     need(oid==a['candidate'],'Canonical candidate identity differs')
     return m
--- completion_checkpoint.py OLD checked_pointer
+++ completion_checkpoint.py CURRENT checked_pointer
@@ -1,17 +1,17 @@
 def checked_pointer(rt,cas_ref):
-    raw,unused=rt.seed.s.read_regular(NATIVE/'ROOT_ACTUAL_COMPLETION_POINTER.json')
+    raw,unused=rt.seed.s.read_regular(NATIVE/pointer_name(rt.m))
     pointer=rt.h.decode(raw)
-    rt.h.matches(pointer,{'schema':'pr218-completion-actual-five-pointer-v1',
+    rt.h.matches(pointer,{'schema':'pr239-completion-actual-five-pointer-v1',
         'evidence_scope':'ACTUAL_SYNC_NOT_EXTERNAL_ROOT_TERMINAL_ACCEPTANCE','protocol_pin':rt.seed.source_pin,
         'admission_pin':rt.admission_pin,'actual_CAS_pin':{k:cas_ref[k] for k in ('bytes','sha256')},
         'CAS_target':rt.admission['candidate'],'CAS_target_tree':rt.admission['tree'],
         'all_five_local_postimages_verified':True,'recorded_under_original_stable_lock':True,
         'external_Root_terminal_acceptance_inferred':False},'Exact actual-sync pointer required before terminal readout')
     path=Path(pointer['sync_path'])
-    need(path.parent.parent==NATIVE and path.parent.name.startswith('ROOT_COMPLETE218_SYNC_')
+    need(path.parent.parent==NATIVE and path.parent.name.startswith('ROOT_COMPLETE239_SYNC_')
          and path.name=='ACTUAL_FIVE_SYNC.json','Exact actual sync journal pointer')
     proof=ref(rt.h,rt.seed.s,{'path':str(path),**pointer['sync_pin']})
-    rt.h.matches(proof,{'schema':'pr218-completion-actual-five-sync-v1',
+    rt.h.matches(proof,{'schema':'pr239-completion-actual-five-sync-v1',
         'evidence_scope':'ACTUAL_SYNC_REQUIRES_EXTERNAL_ROOT_TERMINAL_ACCEPTANCE',
         'protocol_pin':rt.seed.source_pin,'admission_pin':rt.admission_pin,
         'actual_CAS_pin':{k:cas_ref[k] for k in ('bytes','sha256')},'CAS_target':rt.admission['candidate'],

--- completion_checkpoint.py OLD main_closure
+++ completion_checkpoint.py CURRENT main_closure
@@ -8,7 +8,7 @@
         need(comp.get('status')=='ahead' and comp['merge_base_commit']['sha']==rt.admission['candidate'],'R must equal or actually descend from C')
     root=commit['tree']['sha'];trees=c.NativeTrees(api)
     selected,queue=body_associations(rt,observer,trees,root,True)
-    pr=h.pr_identity(observer,rt.m,rt.pool)
+    pr=h.pr_identity(observer,rt.m,rt.pool,post=True)
     need(api('GET','git/ref/heads/main')['object']['sha']==observed,'R changed during coherent owned-state proof; explicit readonly reconciliation needed')
     return {'actual_MAIN_observed':observed,'actual_MAIN_tree':root,'CAS_target':rt.admission['candidate'],
         'CAS_target_tree':rt.admission['tree'],'selected_postimage_paths_verified':len(selected),

--- completion_checkpoint.py OLD parent_state
+++ completion_checkpoint.py CURRENT parent_state
@@ -1,25 +1,28 @@
-def parent_state(rt,observer):
-    """Immutable fixed-parent truth, never a mutable Main observation."""
+def parent_state(rt,observer,immutable=False):
+    '''Immutable fixed-parent truth; open95 creation and closed100 ancestry differ.'''
     h,c,m=rt.h,rt.c,rt.m;api=h.GetOnly(observer);parent=m['expected_parent'];root=m['expected_parent_tree']
-    need(parent not in (h.ORIGINAL,h.CURRENT,h.MERGED),'A PR218 snapshot can never be the archival commit parent')
+    need(parent not in (h.ORIGINAL,h.CURRENT),'Submitted HEAD can never be fresh Main first parent')
     value=api('GET','git/commits/'+parent)
     need(value.get('sha')==parent and value['tree']['sha']==root,'Admission parent/root differs')
     if parent!=h.ANCHOR:
         comp=api('GET','compare/'+h.ANCHOR+'...'+parent)
-        need(comp.get('status')=='ahead' and comp['merge_base_commit']['sha']==h.ANCHOR,'Fresh Main must preserve actual212 administrative terminal ancestry')
-    comp=api('GET','compare/'+h.MERGED+'...'+parent)
-    need((parent==h.MERGED and comp.get('status')=='identical') or
-         (comp.get('status')=='ahead' and comp['merge_base_commit']['sha']==h.MERGED),
-         'Fresh parent must preserve actual already-merged PR218 ancestry')
-    h.pr_identity(observer,m,rt.pool)
+        need(comp.get('status')=='ahead' and comp['merge_base_commit']['sha']==h.ANCHOR,'Fresh Main must preserve actual218 completion ancestry')
+    if m['phase']=='completion100':
+        merged=h.merge_identity(m)['merge_candidate']
+        comp=api('GET','compare/'+merged+'...'+parent)
+        need((parent==merged and comp.get('status')=='identical') or
+             (comp.get('status')=='ahead' and comp['merge_base_commit']['sha']==merged),'Final archive must descend from actual Root merge95 CAS')
+    h.pr_identity(observer,m,rt.pool,allow_post=immutable)
     trees=c.NativeTrees(api);protected(rt,trees,root,False)
-    queue=h.queue_observation(observer,trees,root,m,rt.pool,False)
+    queue=h.queue_observation(observer,trees,root,m,rt.pool,False,post=False)
+    queue_before=rt.pool.get(observer,m['protected_queue']['sha'])
+    h.queue_transition(queue_before,rt.overlay.get(h.QUEUE,queue_before),m)
     wanted,changed,dirs=h.expected(c,trees,root,rt.overlay,rt.pre)
     need(changed==set(m['expected_changed_paths']) and dirs==set(m['expected_new_directories']),'Full exact bound selected scope')
     need(rt.pre[h.VIEWS[2]] is not None,'Native progress baseline required')
     progress=h.decode(rt.pool.get(observer,rt.pre[h.VIEWS[2]][2]))
-    h.matches(progress,h.baseline_facts(),'Intervening ascending checkpoint refused')
-    for key,value in h.source_baseline().items():need(h.exact(progress.get(key),value),'Exact54/38 memberships changed')
+    h.matches(progress,h.baseline_facts(m['phase']),'Intervening ascending checkpoint refused')
+    for key,value in h.source_baseline().items():need(h.exact(progress.get(key),value),'Exact55/39 memberships changed')
     need(type(progress.get('dated_eligible_total')) is int and progress['dated_eligible_total']==99,'Dated99 baseline changed')
     for path in (h.VIEWS[1],h.VIEWS[4]):
         if rt.pre[path] is not None:need(rt.overlay[path].startswith(rt.pool.get(observer,rt.pre[path][2])),'Native log prefix changed')

--- completion_checkpoint.py OLD pointer_name
+++ completion_checkpoint.py CURRENT pointer_name
@@ -0,0 +1,3 @@
+def pointer_name(m):
+    need(m['phase'] in ('merge95','completion100'),'Exact phase pointer')
+    return 'ROOT_ACTUAL_'+m['phase'].upper()+'_POINTER.json'
--- completion_checkpoint.py OLD propose
+++ completion_checkpoint.py CURRENT propose
@@ -2,10 +2,10 @@
     h=seed.h;seed.refresh()
     parent=api('GET','git/ref/heads/main')['object']['sha'];need(h.hexid(parent),'Actual proposed parent')
     commit=api('GET','git/commits/'+parent);need(commit.get('sha')==parent and h.hexid(commit['tree']['sha']),'Actual proposed root')
-    a={'schema':'pr218-completion-parent-admission-v1','PR':218,'evidence_scope':'FACTUAL_PARENT_ADMISSION_REQUIRES_ROOT_ACCEPTANCE',
+    a={'schema':'pr239-completion-parent-admission-v1','PR':239,'evidence_scope':'FACTUAL_PARENT_ADMISSION_REQUIRES_ROOT_ACCEPTANCE',
        'protocol_pin':seed.source_pin,'source_manifest_pin':seed.source_manifest_pin,'logical_manifest_pin':seed.manifest_pin,
-       'logical_gate_pin':seed.logical_gate_pin,'facts':h.phase_facts(),'body_proof_policy':h.BODY_POLICY,'QUEUE_policy':h.QUEUE_POLICY,
-       'parent':parent,'parent_tree':commit['tree']['sha'],'parents':[parent],'created_UTC':date,
+       'logical_gate_pin':seed.logical_gate_pin,'facts':h.phase_facts(seed.logical['phase']),'body_proof_policy':h.BODY_POLICY,'QUEUE_policy':h.QUEUE_POLICY,
+       'parent':parent,'parent_tree':commit['tree']['sha'],'parents':h.commit_parents(seed.logical,parent),'created_UTC':date,
        'commit_author':{**seed.logical['commit_author'],'date':date},'commit_committer':{**seed.logical['commit_committer'],'date':date},
        'commit_message':seed.logical['commit_message'],'tree':'0'*40,'candidate':'0'*40,'candidate_journal':journal_name}
     q=types.SimpleNamespace(seed=seed,h=h,e=seed.e,c=seed.c,m={**seed.logical,'expected_parent':parent,
@@ -13,7 +13,7 @@
     with seed.e.WriterLock(seed.logical['writer_lock']) as lock:
         local_states(q);tree,unused,unused_dirs=parent_state(q,api);a['tree']=tree
         m={**q.m,'commit_author':a['commit_author'],'commit_committer':a['commit_committer']}
-        unused,a['candidate']=h.commit_request(m,tree,[parent])
+        unused,a['candidate']=h.commit_request(m,tree,a['parents'])
         checked_admission(seed,a);seed.refresh();local_states(q);lock.check()
         need(api('GET','git/ref/heads/main')['object']['sha']==parent,'Admission became stale; no silent rebind')
     return a
--- completion_checkpoint.py OLD protected
+++ completion_checkpoint.py CURRENT protected
@@ -1,6 +1,7 @@
 def protected(rt,trees,root,post):
     h=rt.h
     for path,expected in rt.m['protected_nodes'].items():
+        if post and path==h.ATTEMPT:expected=rt.m['post_attempt_tree']
         need(trees.lookup(root,path)==h.preserved_tuple(expected,tree_only=True),'Fresh opaque attempt/audit state changed')
     for row in rt.m['protected_bodies']:
         need(trees.lookup(root,row['path'])==(row['mode'],row['type'],row['sha']),

--- completion_checkpoint.py OLD sync
+++ completion_checkpoint.py CURRENT sync
@@ -2,7 +2,7 @@
     e,h=rt.e,rt.h;rt.refresh()
     actual=actual_cas(rt,cas_ref,api)
     verify_immutable(rt,api)
-    pointer=NATIVE/'ROOT_ACTUAL_COMPLETION_POINTER.json'
+    pointer=NATIVE/pointer_name(rt.m)
     need(not pointer.exists() and not pointer.is_symlink(),'Actual pointer already exists')
     with e.WriterLock(rt.m['writer_lock']) as lock:
         def guard():
@@ -23,7 +23,7 @@
             guard();path=CHECKOUT/row['path'];body=rt.overlay[row['path']];post=pin(body)
             if e.local_pin(h,path)!=post:
                 with e.ParentHandle(path) as parent:
-                    temp='.pr218-completion-'+journal.name+'-'+str(index)+'.tmp'
+                    temp='.pr239-completion-'+journal.name+'-'+str(index)+'.tmp'
                     guard();parent.check()
                     fd=os.open(temp,os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW,0o444,dir_fd=parent.fd)
                     try:
@@ -42,14 +42,14 @@
             observation=guard()
             e.put(journal,'VIEW_'+str(index)+'.json',{'path':row['path'],'postimage':post,'native_observation':observation})
         local_states(rt,all_post=True);observation=guard();local_states(rt,all_post=True)
-        receipt={'schema':'pr218-completion-actual-five-sync-v1','evidence_scope':'ACTUAL_SYNC_REQUIRES_EXTERNAL_ROOT_TERMINAL_ACCEPTANCE',
-            'PR':218,'protocol_pin':rt.seed.source_pin,'source_manifest_pin':rt.seed.source_manifest_pin,
+        receipt={'schema':'pr239-completion-actual-five-sync-v1','evidence_scope':'ACTUAL_SYNC_REQUIRES_EXTERNAL_ROOT_TERMINAL_ACCEPTANCE',
+            'PR':239,'phase':rt.m['phase'],'protocol_pin':rt.seed.source_pin,'source_manifest_pin':rt.seed.source_manifest_pin,
             'admission_pin':rt.admission_pin,'actual_CAS_pin':{k:cas_ref[k] for k in ('bytes','sha256')},
             'CAS_target':rt.admission['candidate'],'CAS_target_tree':rt.admission['tree'],**observation,
             'all_five_local_postimages_verified':True,'facts':rt.m['facts'],'external_Root_terminal_acceptance_inferred':False}
         e.put(journal,'ACTUAL_FIVE_SYNC.json',receipt)
         observation=guard();local_states(rt,all_post=True)
-        e.put(NATIVE,pointer.name,{'schema':'pr218-completion-actual-five-pointer-v1','evidence_scope':'ACTUAL_SYNC_NOT_EXTERNAL_ROOT_TERMINAL_ACCEPTANCE',
+        e.put(NATIVE,pointer.name,{'schema':'pr239-completion-actual-five-pointer-v1','evidence_scope':'ACTUAL_SYNC_NOT_EXTERNAL_ROOT_TERMINAL_ACCEPTANCE',
             'protocol_pin':rt.seed.source_pin,'admission_pin':rt.admission_pin,
             'actual_CAS_pin':{k:cas_ref[k] for k in ('bytes','sha256')},'sync_path':str(journal/'ACTUAL_FIVE_SYNC.json'),
             'sync_pin':pin(enc(receipt)),**observation,'all_five_local_postimages_verified':True,

--- completion_checkpoint.py OLD verify_immutable
+++ completion_checkpoint.py CURRENT verify_immutable
@@ -1,22 +1,22 @@
 def verify_immutable(rt,observer):
     h,c,a=rt.h,rt.c,rt.admission;api=h.GetOnly(observer)
-    wanted,expected_leaves,expected_dirs=parent_state(rt,observer)
+    wanted,expected_leaves,expected_dirs=parent_state(rt,observer,immutable=True)
     need(wanted==a['tree'],'Reconstructed archive tree differs')
-    request,oid=h.commit_request(rt.m,wanted,[a['parent']])
+    request,oid=h.commit_request(rt.m,wanted,a['parents'])
     need(oid==a['candidate'] and oid not in RETIRED and oid not in rt.m['retired_candidates'],'Canonical candidate differs/retired')
     commit=api('GET','git/commits/'+oid)
     need(commit.get('sha')==oid and commit['tree']['sha']==wanted
-         and [r['sha'] for r in commit['parents']]==[a['parent']],'Exact one-parent archive metadata')
+         and [r['sha'] for r in commit['parents']]==a['parents'],'Exact phase-specific ordered commit parents')
     h.matches(commit.get('author'),rt.m['commit_author'],'Canonical author')
     h.matches(commit.get('committer'),rt.m['commit_committer'],'Canonical committer')
     message=h.commit_message_readback(rt.m['commit_message'],commit.get('message'))
     trees=c.NativeTrees(api);leaves,dirs,deleted=trees.changes(a['parent_tree'],wanted)
     need(leaves==expected_leaves and dirs==expected_dirs and not deleted,'Full native scope/foreign preservation differs')
     selected,queue=body_associations(rt,observer,trees,wanted)
-    return {'schema':'pr218-completion-immutable-candidate-verification-v1','evidence_scope':IMMUTABLE_SCOPE,
-        'PR':218,'protocol_pin':rt.seed.source_pin,'source_manifest_pin':rt.seed.source_manifest_pin,
+    return {'schema':'pr239-completion-immutable-candidate-verification-v1','evidence_scope':IMMUTABLE_SCOPE,
+        'PR':239,'phase':rt.m['phase'],'protocol_pin':rt.seed.source_pin,'source_manifest_pin':rt.seed.source_manifest_pin,
         'logical_manifest_pin':rt.seed.manifest_pin,'logical_gate_pin':rt.seed.logical_gate_pin,'admission_pin':rt.admission_pin,
-        'parent':a['parent'],'parent_tree':a['parent_tree'],'candidate':oid,'tree':wanted,'parents':[a['parent']],
+        'parent':a['parent'],'parent_tree':a['parent_tree'],'candidate':oid,'tree':wanted,'parents':a['parents'],
         'selected_files':selected,'selected_count':len(selected),'protected_body_paths_verified':len(rt.m['protected_bodies']),'changed_leaves':sorted(leaves),'new_directories':sorted(dirs),'deleted_directories':[],
         'Main_QUEUE_observation':queue,'body_proof_policy':h.BODY_POLICY,'QUEUE_policy':h.QUEUE_POLICY,
         'full_scope_verified':True,'all_selected_native_bodies_verified':True,'foreign_native_tuples_preserved':True,

--- completion_checkpoint.py TOP OLD
+++ completion_checkpoint.py TOP CURRENT
@@ -1,6 +1,6 @@
-"""Inactive PR218 completion native checkpoint; no ref or PR writer.
+"""Inactive PR239 completion native checkpoint; no ref or PR writer.
 All inputs, gates, admissions and actual receipts are separately Root-bound.
-Adoption55/39 is conditional until separate actual Root terminal; no new publication.
+Two-phase NEW publication;95 retains55/39,100 proposes56/40. Separate Root terminal alone advances.
 """
 import argparse,datetime,hashlib,json,os,re,selectors,signal,stat,sys,time,types
 from pathlib import Path
@@ -9,8 +9,8 @@
 NATIVE=BASE
 PROGRAM=CASE.parents[1]
 CHECKOUT=PROGRAM.parent
-MODEL_PIN={'bytes': 40648, 'sha256': '5f6136ae4335dea22e219c7b1b9d62d416a975e9a8d590a9ca617d732627ae3d'}
-PRIMITIVE_PIN={'bytes': 16405, 'sha256': '6f0162bab7e080445fca633818167476501de9920d566d567fddb1b26f97177c'}
+MODEL_PIN={'bytes': 51455, 'sha256': 'b6e4ea626d0f63aa6c01c8c923d0afdcb810ef629feb2b3dfd15dc3a1613e64e'}
+PRIMITIVE_PIN={'bytes': 16405, 'sha256': '5d3d3072c7a9a95c640ecfbafef466cac50c83ce433b9d57024f772a2cb84d27'}
 RETIRED=set()
 IMMUTABLE_SCOPE='IMMUTABLE_CANDIDATE_ONLY_NOT_MAIN_LEASE_CAS_OR_COMPLETION'
 if __name__=='__main__':main()
--- concurrent_get_extension.py OLD candidate
+++ concurrent_get_extension.py CURRENT candidate
@@ -11,7 +11,7 @@
         entries=[{'path':path,'mode':'100644','type':'blob','content':body.decode('utf-8')}
                  for path,body in sorted(rt.overlay.items())]
         tree_request={'base_tree':rt.admission['parent_tree'],'tree':entries}
-        commit_request,oid=h.commit_request(rt.m,rt.admission['tree'],[rt.admission['parent']])
+        commit_request,oid=h.commit_request(rt.m,rt.admission['tree'],rt.admission['parents'])
         e.put(journal,'ONE_USE_ADMISSION_RESERVATION.json',{'admission_pin':rt.admission_pin,
             'protocol_pin':rt.seed.source_pin,'logical_manifest_pin':rt.seed.manifest_pin,'gate_pin':rt.gate_pin,
             'expected_tree':rt.admission['tree'],'expected_candidate':oid,

--- concurrent_get_extension.py OLD wanted_blobs
+++ concurrent_get_extension.py CURRENT wanted_blobs
@@ -1,8 +1,8 @@
 def wanted_blobs(rt,aux):
     h=rt.h
     need(type(aux) is dict and set(aux)=={'schema','PR','files'}
-         and aux['schema']=='pr218-concurrent-GET-auxiliary-blob-pins-v1'
-         and type(aux['PR']) is int and aux['PR']==218,'Exact auxiliary native body pin descriptor')
+         and aux['schema']=='pr239-concurrent-GET-auxiliary-blob-pins-v1'
+         and type(aux['PR']) is int and aux['PR']==239,'Exact auxiliary native body pin descriptor')
     rows=aux['files']
     need(type(rows) is list and len(rows)<=32 and all(type(r) is dict and set(r)=={'oid','bytes','sha256'} for r in rows)
          and len({r['oid'] for r in rows})==len(rows),'Finite exact auxiliary body pins')
@@ -15,7 +15,11 @@
         p={k:row[k] for k in ('bytes','sha256')}
         need(row['sha'] not in wanted or h.exact(wanted[row['sha']],p),'Protected/selected object pin disagreement')
         wanted[row['sha']]=p
-    required={rt.m['protected_queue']['sha'],h.CURRENT_QUEUE}
+    for row in h.submitted_inventory():
+        p={k:row[k] for k in ('bytes','sha256')};oid=row['native_blob']
+        need(oid not in wanted or h.exact(wanted[oid],p),'Submitted/selected pin disagreement')
+        wanted[oid]=p
+    required={rt.m['protected_queue']['sha'],h.CURRENT_QUEUE,h.native_identity(rt.m)['submitted_base_queue']['sha']}
     for path in (h.VIEWS[2],h.VIEWS[1],h.VIEWS[4]):
         item=rt.pre[path]
         if item is not None:required.add(item[2])

--- concurrent_get_extension.py TOP OLD
+++ concurrent_get_extension.py TOP CURRENT
@@ -1,4 +1,4 @@
-"""Inactive PR218 GET transport extension; no ref/PR writer or new effect authority."""
+"""Inactive PR239 GET transport extension; no ref/PR writer or new effect authority."""
 import argparse,base64,concurrent.futures,hashlib,json,os,re,stat,sys,threading,time,types
 from pathlib import Path
 BASE=Path(__file__).absolute().parent
@@ -6,7 +6,7 @@
 PROGRAM=CASE.parents[1]
 CHECKOUT=PROGRAM.parent
 DRIVER=BASE
-PROTOCOL_PIN={'bytes': 44492, 'sha256': '41386909675f745896475f03e0594835c40118b4f78a65996b4322cf89913487'}
+PROTOCOL_PIN={'bytes': 45277, 'sha256': '457714f6a263efb7fc048acc1a6bed825664698d816caf7ffbeaaa52edf184a6'}
 MAX_BLOBS=664
 MAX_DECODED=32_000_000
 MAX_CANONICAL=48_000_000

--- ROOT_TERMINAL_INSPECTION.py OLD accounting
+++ ROOT_TERMINAL_INSPECTION.py CURRENT accounting
@@ -6,11 +6,11 @@
         need(value.get('conditional_proposal_only') is True,'Five proposals cannot be Root actual terminal authority')
     need(type(progress.get('dated_eligible_total')) is int and progress['dated_eligible_total']==99,'Dated denominator99')
     need(type(baseline) is dict and set(baseline)=={'fully_completed_eligible_PRs','published_PRs'},'Exact baseline fields')
-    for key,count in (('fully_completed_eligible_PRs',54),('published_PRs',38)):
+    for key,count in (('fully_completed_eligible_PRs',55),('published_PRs',39)):
         arr=baseline[key]
         need(type(arr) is list and len(arr)==count and all(type(x) is int for x in arr)
-             and arr==sorted(set(arr)) and all(n not in arr for n in (212,213,215,216,217,218))
-             and exact(progress.get(key),arr+[218]),'Exact prior baseline plus218 only')
-    return {'old_memberships':baseline,'new_memberships':{k:v+[218] for k,v in baseline.items()},
-            'fully_completed_eligible_PRs':baseline['fully_completed_eligible_PRs']+[218],
-            'published_PRs':baseline['published_PRs']+[218],'dated_eligible_total':99}+             and arr==sorted(set(arr)) and all(n not in arr for n in range(219,240))
+             and exact(progress.get(key),arr+[239]),'Exact55/39 baseline plus239 only')
+    return {'old_memberships':baseline,'new_memberships':{k:v+[239] for k,v in baseline.items()},
+            'fully_completed_eligible_PRs':baseline['fully_completed_eligible_PRs']+[239],
+            'published_PRs':baseline['published_PRs']+[239],'dated_eligible_total':99}
--- ROOT_TERMINAL_INSPECTION.py OLD context
+++ ROOT_TERMINAL_INSPECTION.py CURRENT context
@@ -4,8 +4,8 @@
        'Exact terminal configuration fields')
     for key in ('manifest','logical_gate','admission','Root_gate','actual_CAS','pointer','sync','source_acceptance'):
         checked_ref(config[key])
-    need(config['pointer']['path']==str(B/'ROOT_ACTUAL_COMPLETION_POINTER.json'),'Only original actual pointer path')
-    need(type(config['journal']) is str and re.fullmatch('ROOT_COMPLETE218_READ_ROOT_TERMINAL_[A-Za-z0-9_-]{1,35}',config['journal']) is not None,
+    need(config['pointer']['path']==str(B/'ROOT_ACTUAL_COMPLETION100_POINTER.json'),'Only original actual pointer path')
+    need(type(config['journal']) is str and re.fullmatch('ROOT_COMPLETE239_READ_ROOT_TERMINAL_[A-Za-z0-9_-]{1,35}',config['journal']) is not None,
          'Fresh bounded read-only Root terminal journal')
     need(type(config['receipt_name']) is str and config['receipt_name']=='ROOT_ACTUAL_COMPLETION_VERIFICATION_01.json',
          'Exact external Root terminal receipt basename')
@@ -16,15 +16,16 @@
         return own,manifest
     own,manifest=refresh()
     path=B/'completion_checkpoint.py';raw=readonly(path)
-    need(exact(pin(raw),DRIVER_PIN),'Approved pinned PR218 driver differs')
-    driver=types.ModuleType('Root_PR218_terminal_approved_driver');driver.__file__=str(path)
+    need(exact(pin(raw),DRIVER_PIN),'Approved pinned PR239 driver differs')
+    driver=types.ModuleType('Root_PR239_terminal_approved_driver');driver.__file__=str(path)
     exec(compile(raw,str(path),'exec'),driver.__dict__)
     seed=driver.Seed(config['manifest'],config['logical_gate'])
     rt=driver.Runtime(seed,config['admission'],config['Root_gate'])
+    need(rt.m['phase']=='completion100','Separate final phase100 only;95 cannot publish actual terminal')
     need(exact(seed.source_pin,DRIVER_PIN),'Seed did not bind approved driver')
     if config['extension_source'] is not None:
         extpath=checked_ref(config['extension_source']);ext_raw=raw_ref(config['extension_source'])
-        ext=types.ModuleType('Root_PR218_terminal_explicit_extension');ext.__file__=str(extpath)
+        ext=types.ModuleType('Root_PR239_terminal_explicit_extension');ext.__file__=str(extpath)
         exec(compile(ext_raw,str(extpath),'exec'),ext.__dict__)
         need(callable(getattr(ext,'bind_runtime',None)) and callable(getattr(ext,'make_readonly_api',None)),
              'Pinned extension lacks explicit reviewed interface')

--- ROOT_TERMINAL_INSPECTION.py OLD inspect
+++ ROOT_TERMINAL_INSPECTION.py CURRENT inspect
@@ -44,6 +44,6 @@
         publication=exclusive_root_receipt(e,path,enc(record),guard,identity_guard)
         return {'terminal_receipt':{'path':str(path),**pin(enc(record))},'actual_MAIN_observed':observation['actual_MAIN_observed'],
                 'actual_MAIN_tree':observation['actual_MAIN_tree'],'CAS_target':rt.admission['candidate'],
-                'fully_completed_count':55,'published_count':39,'last_completed_PR':218,
-                'next_numeric_intake_cursor':219,'completed_eligible_workflow':True,
+                'fully_completed_count':56,'published_count':40,'last_completed_PR':239,
+                'next_numeric_intake_cursor':240,'completed_eligible_workflow':True,
                 'publication_ready':True,'goal_complete':False,'publication':publication}
--- ROOT_TERMINAL_INSPECTION.py OLD native_semantics
+++ ROOT_TERMINAL_INSPECTION.py CURRENT native_semantics
@@ -14,9 +14,9 @@
          and observation.get('protected_opaque_attempt_audit_verified') is True,'Exact C/R/root/closure association')
     pr=observation.get('fresh_merged_PR_status_observation')
     wanted={'HEAD':h.CURRENT,'state':'closed','draft':False,'merged':True,'current_status':'claimed_solved',
-            'original_merge_commit':h.MERGED,'same_selected_PR_identity':True}
+            'original_merge_commit':h.merge_identity(rt.m)['merge_candidate'],'same_selected_PR_identity':True}
     need(type(pr) is dict and all(k in pr and exact(pr[k],v) for k,v in wanted.items()),
-         'Original already-merged claimed_solved PR218 must remain unchanged')
+         'Actually merged claimed_solved PR239 must match earlier Root merge95 CAS')
     queue=observation.get('Main_QUEUE_observation')
     need(type(queue) is dict and queue.get('policy')==h.QUEUE_POLICY and queue.get('foreign_rows_may_differ') is True
          and exact(queue.get('own_row_pin'),rt.m['protected_queue_row_pin']),

--- ROOT_TERMINAL_INSPECTION.py OLD pointer_and_posts
+++ ROOT_TERMINAL_INSPECTION.py CURRENT pointer_and_posts
@@ -16,6 +16,6 @@
         raw,identity=rt.seed.s.read_regular(driver.CHECKOUT/row['path'])
         need(type(raw) is bytes and raw==rt.overlay[row['path']],'Full local five postimage bytes differ')
         files.append({'path':row['path'],'postimage':pin(raw)});bodies[row['path']]=raw
-    need(exact(h.BASELINE_PIN,BASELINE_PIN),'Exact accepted54/38 baseline pin required')
+    need(exact(h.BASELINE_PIN,BASELINE_PIN),'Exact accepted55/39 baseline pin required')
     lists=accounting(h,rt.m,h.decode(bodies[h.VIEWS[0]]),h.decode(bodies[h.VIEWS[2]]),h.source_baseline())
     return observed_pin,pin(sync_raw),files,lists
--- ROOT_TERMINAL_INSPECTION.py OLD terminal_record
+++ ROOT_TERMINAL_INSPECTION.py CURRENT terminal_record
@@ -6,6 +6,8 @@
     the real consumer without publishing or asserting any actual completion.
     """
     h=rt.h
+    need(rt.m['phase']=='completion100','Only final100 can construct actual terminal')
+    h.merge_identity(rt.m);h.publication_identity(rt.m)
     need(type(source_checks) is int and source_checks>=2,'Executed repeated exact source/gate refreshes required')
     need(actual.get('actual_Root_MCP_CAS_performed') is True
          and actual.get('actual_tool_success_and_readback_accepted') is True
@@ -38,16 +40,21 @@
               and checks['refreshes_completed_before_record']>=2
               and checks['all_exact_pins_and_gates_rechecked_successfully'] is True)
     return {'schema':RECEIPT_SCHEMA,'evidence_scope':'ACTUAL_ROOT_RECEIPT',
-        'UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'PR':218,'problem_id':'30006020',
-        'accepted':True,'completed':True,'workflow_percent':100,'completed_eligible_workflow':True,
+        'UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'PR':239,'problem_id':'30001321',
+        'accepted':True,'completed':True,'phase':'completion100','new_publication_workflow':True,'workflow_percent':100,'completed_eligible_workflow':True,
         'publication_workflow_completed':True,'publication_ready':True,
-        'fully_completed_count':55,'published_count':39,'last_completed_PR':218,
-        'next_numeric_intake_cursor':219,'advance_to_next_PR_authorized_now':True,'goal_complete':False,
+        'fully_completed_count':56,'published_count':40,'last_completed_PR':239,
+        'next_numeric_intake_cursor':240,'advance_to_next_PR_authorized_now':True,'goal_complete':False,
         'numeric_advance_conditional_on_actual_Root_terminal':False,
         'original_eligible_status':'claimed_solved','current_status':'claimed_solved',
-        'current_head':h.CURRENT,'original_merge_commit':h.MERGED,'actual_original_PR_merged':True,
-        'adopted_existing_publication':True,'no_new_provider_publication_or_tracker_append':True,
-        'existing_publication_DOI':h.EXISTING_DOI,'existing_tracker_range':h.EXISTING_TRACKER,
+        'current_head':h.CURRENT,'original_merge_commit':h.merge_identity(rt.m)['merge_candidate'],'actual_original_PR_merged':True,
+        'adopted_existing_publication':False,'no_new_provider_publication_or_tracker_append':False,
+        'new_publication_verified':True,'new_tracker_append_verified':True,
+        'publication_DOI':h.publication_identity(rt.m)['doi'],'tracker_range':h.publication_identity(rt.m)['range'],
+        'publication_record_id':h.publication_identity(rt.m)['record_id'],
+        'actual_publication_receipt':rt.m['evidence_references']['publication'],
+        'actual_tracker_receipt':rt.m['evidence_references']['tracker'],
+        'actual_merge95_receipt':rt.m['evidence_references']['merge'],
         'parent':rt.admission['parent'],'parent_tree':rt.admission['parent_tree'],
         'candidate':rt.admission['candidate'],'tree':rt.admission['tree'],**observation,
         'terminal_source_pin':source_pin,'terminal_source_manifest_pin':manifest_pin,
@@ -63,17 +70,17 @@
         'all_five_local_files_match_actual_checkpoint':True,'files':files,
         'old_memberships':lists['old_memberships'],'new_memberships':lists['new_memberships'],
         'fully_completed_eligible_PRs':lists['fully_completed_eligible_PRs'],'published_PRs':lists['published_PRs'],
-        'only218_added_to_exact54_38_baseline':True,'dated_eligible_denominator':99,
+        'only239_added_to_exact55_39_baseline':True,'dated_eligible_denominator':99,
         'denominator_is_not_current_repository_census':True,'original_stable_writer_lock_held_exact':True,
         'all_selected_native_bodies_verified':True,'full_scope_verified':True,'foreign_native_tuples_preserved':True,
         'source_gates_verified':verified,'source_gate_checks':checks,
         'selected_file_count':len(rt.overlay),'selected_bytes':sum(len(x) for x in rt.overlay.values()),
         'changed_leaf_count':len(proof['changed_leaves']),'new_directory_count':len(proof['new_directories']),
-        'deleted_directory_count':0,'whole_parent_and_candidate_QUEUE_tuple_preserved':rt.m['protected_queue'],
+        'deleted_directory_count':0,'whole_phase100_parent_and_candidate_QUEUE_tuple_preserved':rt.m['protected_queue'],
         'actual_R_QUEUE_whole_body_authenticated':True,'own_Main_QUEUE_row_pin':rt.m['protected_queue_row_pin'],
         'R_foreign_QUEUE_rows_may_differ':True,'Main_QUEUE_observation':queue,
         'opaque_attempt_audit_preserved':True,
-        'numeric_intake_authority_boundary':'Only this separately executed actual Root terminal authorizes numeric215. Conditional five proposals, sync, ancestry and source gates alone do not.',
+        'numeric_intake_authority_boundary':'Only this separately executed actual Root terminal authorizes numeric240. Conditional five proposals, sync, ancestry and source gates alone do not.',
         'terminal_observation_boundary':'UTC is preparation time for a dated jointly checked local-five/coherent R/root. Fsynced pending bytes precede the same-state full mutable guard and exclusive final publication; afterwards only file/source/held-lock identity checks run. C and R remain separate. No perpetual/current-at-write-time Main equality, ancestry-derived CAS or distributed atomic transaction is claimed.',
         'publication_order':'pending full-write/file-fsync/directory-fsync; final full mutable guard; exclusive final-name link; file/lock/source identity afterwards',
         'protected_body_count_boundary':'Exact explicit protected body count only; other existing scientific and audit trees are preserved opaquely by mode/type/OID.',

--- ROOT_TERMINAL_INSPECTION.py TOP OLD
+++ ROOT_TERMINAL_INSPECTION.py TOP CURRENT
@@ -1,4 +1,4 @@
-"""Inactive Root PR218 completion terminal inspector; import has no effects.
+"""Inactive Root PR239 completion terminal inspector; import has no effects.
 
 Preparation does not invoke this CLI. Later actual Root use requires separately
 pinned source acceptance, logical/admission/CAS evidence and actual five sync.
@@ -11,9 +11,9 @@
 A=BASE.parent
 B=BASE
 CHECKOUT=A.parents[2]
-DRIVER_PIN={'bytes': 44492, 'sha256': '41386909675f745896475f03e0594835c40118b4f78a65996b4322cf89913487'}
-RECEIPT_SCHEMA='pr218-root-actual-completion-verification-v1'
-SOURCE_SCHEMA='pr218-root-terminal-inspector-source-acceptance-v1'
-BASELINE_PIN={'bytes': 871, 'sha256': 'ae2786a2fa2d199cd92003830fd2555a1a8d1fa26d32a2e30c79b0e236c66637'}
-FIXED_FACTS={'active_PR': 218, 'workflow_percent': 100, 'completed': True, 'fully_completed_count': 55, 'published_count': 39, 'last_completed_PR': 218, 'next_numeric_intake_cursor': 219, 'goal_complete': False, 'completed_eligible_workflow': True, 'publication_workflow_completed': True, 'publication_ready': True, 'original_eligible_status': 'claimed_solved', 'current_status': 'claimed_solved', 'actual_original_PR_merged': True, 'adopted_existing_publication': True, 'no_new_provider_publication_or_tracker_append': True, 'current_head': '698f85a0f608e5a90924567d761663dfb100f3c2', 'original_merge_commit': '8172b404db36b931005ac48a94ec91fdff866023', 'existing_publication_DOI': '10.5281/zenodo.23387774', 'existing_tracker_range': "'Math Puzzles'!A99:D99", 'numeric_advance_conditional_on_actual_Root_terminal': True, 'advance_to_next_PR_authorized_now': False}
+DRIVER_PIN={'bytes': 45277, 'sha256': '457714f6a263efb7fc048acc1a6bed825664698d816caf7ffbeaaa52edf184a6'}
+RECEIPT_SCHEMA='pr239-root-actual-completion-verification-v1'
+SOURCE_SCHEMA='pr239-root-terminal-inspector-source-acceptance-v1'
+BASELINE_PIN={'bytes': 889, 'sha256': '36258fde3b9a95d4ed8baf7aebff34030a25267b92b08d58256ebac2404b52ce'}
+FIXED_FACTS={'active_PR': 239, 'phase': 'completion100', 'workflow_percent': 100, 'completed': True, 'fully_completed_count': 56, 'published_count': 40, 'last_completed_PR': 239, 'next_numeric_intake_cursor': 240, 'goal_complete': False, 'completed_eligible_workflow': True, 'publication_workflow_completed': True, 'publication_ready': True, 'original_eligible_status': 'claimed_solved', 'current_status': 'claimed_solved', 'current_head': '7f17eef77c52b2d9b2ec3ad0803c016267fa6496', 'new_publication_workflow': True, 'adopted_existing_publication': False, 'no_new_provider_publication_or_tracker_append': False, 'numeric_advance_conditional_on_actual_Root_terminal': True, 'advance_to_next_PR_authorized_now': False}
 if __name__=='__main__':main()
