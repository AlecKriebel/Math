"""Independent OFFLINE adversarial models. Never native write evidence."""
import sys
sys.dont_write_bytecode = True
import importlib.util
from pathlib import Path
import json, subprocess, threading, unittest, copy, hashlib, datetime
from unittest.mock import patch

OWN = Path(__file__).resolve().parent
PREP = OWN.parent
PRIVATE = PREP.parent / 'private_sources/package_update_preparation/software_adversary0'
PRIVATE.mkdir(parents=True, exist_ok=True)
spec = importlib.util.spec_from_file_location('existing_tests', PREP / 'test_update_package.py')
t = importlib.util.module_from_spec(spec); spec.loader.exec_module(t)
m = t.m
# Existing tests create synthetic files only inside this review's allowed paths.
m.HERE = OWN
m.PRIVATE = PRIVATE

class IndependentTests(t.UpdaterTests):
    def test_exclusive_journal_is_atomic_under_concurrent_creation(self):
        target = self.tmp / 'race_journal.json'
        barrier = threading.Barrier(2)
        replace = m.os.replace
        link = m.os.link
        outcomes = []
        def rendezvous(src, dst):
            if Path(dst) == target:
                barrier.wait(timeout=3)
            return replace(src, dst)
        def rendezvous_link(src, dst, **kwargs):
            if Path(dst) == target:
                barrier.wait(timeout=3)
            return link(src, dst, **kwargs)
        def writer(value):
            try:
                m.durable(target, {'writer': value}, exclusive=True)
                outcomes.append(('success', value))
            except Exception as exc:
                outcomes.append((type(exc).__name__, value))
        with patch.object(m.os, 'replace', side_effect=rendezvous), patch.object(m.os, 'link', side_effect=rendezvous_link):
            threads = [threading.Thread(target=writer, args=(n,)) for n in (1, 2)]
            for thread in threads: thread.start()
            for thread in threads: thread.join(timeout=6)
        self.assertTrue(all(not thread.is_alive() for thread in threads))
        report = {'evidence_kind':'offline_mock', 'outcomes':outcomes,
                  'final_journal':json.loads(target.read_text()),
                  'required_success_count':1}
        (OWN / 'journal_race_result.json').write_bytes(m.encoded(report))
        self.assertEqual(sum(outcome[0] == 'success' for outcome in outcomes), 1,
                         'exclusive=True admitted both writers and overwrote one journal')

    def test_git_tree_order_and_all_supported_sibling_modes(self):
        entries = [
            {'path':'foo', 'mode':'040000','type':'tree','sha':'1'*40},
            {'path':'foo.bar', 'mode':'100644','type':'blob','sha':'2'*40},
            {'path':'foo0', 'mode':'100755','type':'blob','sha':'3'*40},
            {'path':'link', 'mode':'120000','type':'blob','sha':'4'*40},
            {'path':'submodule', 'mode':'160000','type':'commit','sha':'5'*40},
            {'path':'é', 'mode':'100644','type':'blob','sha':'6'*40}]
        expected_order = [entries[i] for i in (1,0,2,3,4,5)]
        raw = b''.join((e['mode'].lstrip('0')+' '+e['path']).encode()+b'\0'+bytes.fromhex(e['sha']) for e in expected_order)
        self.assertEqual(m.tree_bytes(entries),raw)
        independent = subprocess.run(['git','hash-object','-t','tree','--stdin'],input=raw,capture_output=True,check=True).stdout.decode().strip()
        self.assertEqual(m.oid('tree',m.tree_bytes(entries)), independent)
        for bad in (
            entries + [copy.deepcopy(entries[0])],
            [{**entries[0],'path':'a/b'}],
            [{**entries[0],'mode':'100644','type':'tree'}]):
            with self.assertRaises(m.Stop): m.tree_bytes(bad)

    def test_untouched_selected_nested_and_root_siblings_preserved(self):
        extra = self.api.put_blob(b'untouched nested selected bytes\n')
        symlink = {'path':'link','mode':'120000','type':'blob','sha':extra}
        executable = {'path':'tool','mode':'100755','type':'blob','sha':extra}
        gitlink = {'path':'module','mode':'160000','type':'commit','sha':'7'*40}
        selected_entries = self.api.trees[self.api.selected] + [executable, symlink, gitlink]
        selected = self.api.put_tree(selected_entries)
        attempts = self.api.put_tree([self.api.entry('6800014','tree',selected),self.api.entry('unrelated','blob',self.api.unrelated)])
        unsolved = self.api.put_tree([self.api.entry('QUEUE.md','blob',self.api.qblob),self.api.entry('attempts','tree',attempts)])
        root = self.api.put_tree([self.api.entry('outside.txt','blob',self.api.unrelated),self.api.entry('unsolved_math_prioritization','tree',unsolved)])
        plan, _, _ = self.prepared()
        # Build a root directly for this test. Source receipt regular-file restriction
        # is separate; replacement should preserve any untouched tree entry type.
        engine = self.engine()
        replaced, trees = engine.replace(root, plan['files'])
        for tree in trees: self.api.trees[tree['sha']] = tree['entries']
        for entry in (symlink,executable,gitlink):
            self.assertEqual(engine.lookup(replaced,m.PREFIX+entry['path']),entry)
        self.assertEqual(engine.lookup(replaced,'outside.txt')['sha'],self.api.unrelated)
        self.assertEqual(engine.lookup(replaced,'unsolved_math_prioritization/QUEUE.md')['sha'],self.api.qblob)

    def test_commit_message_and_identity_boundary_inputs(self):
        commit = copy.deepcopy(self.spec['commit'])
        for message in ('missing newline','two newlines\n\n','nul\0\n'):
            commit['message'] = message
            with self.assertRaises(m.Stop): self.engine().commit_object(commit,'1'*40)
        commit = copy.deepcopy(self.spec['commit'])
        for bad in ('injected\nidentity','x<bad>','nul\0'):
            commit['author']['name'] = bad
            with self.assertRaises(m.Stop): self.engine().commit_object(commit,'1'*40)
        commit = copy.deepcopy(self.spec['commit'])
        ident, raw_sha, payload = self.engine().commit_object(commit,'1'*40)
        raw = ('tree '+'1'*40+'\nparent '+m.HEAD+'\nauthor Synthetic Test <test@example.invalid> 1791849600 +0000\ncommitter Synthetic Test <test@example.invalid> 1791849600 +0000\n\nPrepared synthetic packet\n').encode()
        git_ident = subprocess.run(['git','hash-object','-t','commit','--stdin'],input=raw,capture_output=True,check=True).stdout.decode().strip()
        self.assertEqual(ident,git_ident)
        self.assertEqual(raw_sha,hashlib.sha256(raw).hexdigest())

    def test_gate_drift_after_object_creation_prevents_ref_patch(self):
        plan, content, body = self.prepared()
        original = self.api.request
        def raced(method, endpoint, payload=None):
            response = original(method,endpoint,payload)
            if method == 'POST' and endpoint == 'git/commits': self.api.title = 'raced title'
            return response
        with patch.object(self.api,'request',side_effect=raced):
            with self.assertRaisesRegex(m.Stop,'title drift'): self.engine(True).apply(plan,content,body)
        self.assertFalse(any(c[0]=='PATCH' for c in self.writes()))

    def test_body_patch_waits_for_every_package_readback(self):
        plan, content, body = self.prepared()
        original = self.api.request
        def corrupted(method, endpoint, payload=None):
            response = original(method,endpoint,payload)
            if method=='GET' and endpoint=='git/blobs/'+plan['files'][0]['blob_sha']:
                response['content'] = 'Y29ycnVwdGVk'
            return response
        with patch.object(self.api,'request',side_effect=corrupted):
            with self.assertRaisesRegex(m.Stop,'blob byte mismatch'): self.engine(True).apply(plan,content,body)
        self.assertEqual(self.api.head,plan['commit_sha'])
        self.assertFalse(any(c[0]=='PATCH' and c[1]=='pulls/411' for c in self.writes()))

    def test_approved_reconcile_digest_and_recomputed_root_binding(self):
        plan, content, body = self.prepared()
        self.api.fail='PATCH git/refs/heads/'+m.BRANCH
        with self.assertRaises(m.Stop): self.engine(True).apply(plan,content,body)
        self.api.fail=None
        before=len(self.writes())
        with self.assertRaisesRegex(m.Stop,'approved plan digest'): self.engine().reconcile(self.journal,'0'*64)
        result=self.engine().reconcile(self.journal,m.sha(m.encoded(plan)))
        self.assertEqual(result['status'],'source_head_observed_no_branch_confirmation')
        self.assertEqual(len(self.writes()),before)
        journal=json.loads(self.journal.read_text())
        journal['plan']['root_tree']='8'*40
        journal['plan_sha256']=m.sha(m.encoded(journal['plan']))
        self.journal.write_bytes(m.encoded(journal))
        with self.assertRaisesRegex(m.Stop,'preservation prediction'): self.engine().reconcile(self.journal,journal['plan_sha256'])
        self.assertEqual(len(self.writes()),before)

    def test_case_variant_private_parts_and_canonical_paths_rejected(self):
        for name in ('Private_Sources','SeCrEtS','.GiT','.SsH','CrEdEnTiAlS'):
            with self.assertRaisesRegex(m.Stop,'private'): m.safe_path(OWN/name/'synthetic.txt')
            with self.assertRaisesRegex(m.Stop,'unsafe remote'): m.remote(m.PREFIX+name+'/synthetic.txt')
        for suffix in ('a/../packet.txt','a//packet.txt','a/./packet.txt','packet.txt/'):
            with self.assertRaises(m.Stop): m.remote(m.PREFIX+suffix)
        with self.assertRaisesRegex(m.Stop,'local traversal'): m.safe_path(OWN/'a'/'..'/'synthetic.txt')

    def test_native_transport_failure_preserves_exact_nonutf8_custody(self):
        stdout=b'partial response \xff\x00'
        stderr=b'native transport \xfe failure'
        completed=subprocess.CompletedProcess(['gh'],1,stdout=stdout,stderr=stderr)
        transport=m.Native()
        with patch.object(m.subprocess,'run',return_value=completed) as run:
            with self.assertRaises(m.Stop): transport.request('GET','git/ref/heads/'+m.BRANCH)
        import base64
        self.assertEqual(base64.b64decode(transport.last_native['stdout_base64']),stdout)
        self.assertEqual(base64.b64decode(transport.last_native['stderr_base64']),stderr)
        self.assertEqual(transport.last_native['returncode'],1)
        self.assertEqual(run.call_args.args[0][3],'GET')

    def test_native_transport_timeout_preserves_partial_uncertain_custody(self):
        partial=b'partial \xff reply'
        failure=subprocess.TimeoutExpired(['gh'],120,output=partial,stderr=b'timed out')
        transport=m.Native()
        with patch.object(m.subprocess,'run',side_effect=failure):
            with self.assertRaises(subprocess.TimeoutExpired): transport.request('GET','git/ref/heads/'+m.BRANCH)
        import base64
        self.assertIsNone(transport.last_native['returncode'])
        self.assertTrue(transport.last_native['uncertain'])
        self.assertEqual(base64.b64decode(transport.last_native['stdout_base64']),partial)
        self.assertEqual(base64.b64decode(transport.last_native['stderr_base64']),b'timed out')

    def test_body_patch_race_is_unavoidable_without_cas(self):
        plan,content,body=self.prepared()
        original=self.api.request
        observed=[]
        def raced(method,endpoint,payload=None):
            if method=='PATCH' and endpoint=='pulls/411':
                self.api.body='concurrent edit after the last GET\n'
                observed.append(self.api.body)
            return original(method,endpoint,payload)
        with patch.object(self.api,'request',side_effect=raced):
            result=self.engine(True).apply(plan,content,body)
        self.assertEqual(result['status'],'confirmed_complete')
        self.assertEqual(self.api.body,body)
        self.assertEqual(len(observed),1)
        (OWN/'body_cas_limit_result.json').write_bytes(m.encoded({'evidence_kind':'offline_mock','status':result['status'],'concurrent_edit_overwritten':True,'limitation':'PR body PATCH has no compare-and-swap; a post-gate edit is overwritten and final readbacks cannot detect that prior edit.'}))

if __name__ == '__main__':
    suite=unittest.TestSuite()
    suite.addTests(unittest.defaultTestLoader.loadTestsFromTestCase(t.UpdaterTests))
    names=[n for n in IndependentTests.__dict__ if n.startswith('test_')]
    suite.addTests(IndependentTests(n) for n in names)
    result=unittest.TextTestRunner(verbosity=2).run(suite)
    metadata={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'evidence_kind':'offline_mock','tests_run':result.testsRun,'failures':len(result.failures),'errors':len(result.errors),'helper_sha256':hashlib.sha256((PREP/'update_package.py').read_bytes()).hexdigest(),'test_sha256':hashlib.sha256((PREP/'test_update_package.py').read_bytes()).hexdigest()}
    (OWN/'test_result.json').write_bytes(m.encoded(metadata))
    sys.exit(0 if result.wasSuccessful() else 1)
