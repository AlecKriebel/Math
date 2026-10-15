"""Offline models of native API outcomes; never production receipts or writes."""
import base64
import copy
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch

SPEC = importlib.util.spec_from_file_location("updater", Path(__file__).with_name("update_package.py"))
m = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(m)


class MockAPI:
    def __init__(self):
        self.blobs, self.trees, self.commits, self.calls = {}, {}, {}, []
        self.fail = None
        self.fail_after = False
        self.stale = False
        self.body = "old approved draft body\n"
        self.title = "Synthetic PR411 fixture"
        self.head = m.HEAD
        queue = b"| ID / code | Turns | Status |\n| --- | --- | --- |\n| 6800014 / AMR-067-0014 | 2/5 | claimed_solved |\n"
        self.qblob = self.put_blob(queue)
        self.qhash = m.sha(queue)
        self.old = self.put_blob(b"synthetic old scientific bytes\n")
        self.unrelated = self.put_blob(b"untouched sibling bytes\n")
        self.selected = self.put_tree([self.entry("packet.txt", "blob", self.old)])
        attempts = self.put_tree([self.entry("6800014", "tree", self.selected), self.entry("unrelated", "blob", self.unrelated)])
        unsolved = self.put_tree([self.entry("QUEUE.md", "blob", self.qblob), self.entry("attempts", "tree", attempts)])
        self.root = self.put_tree([self.entry("outside.txt", "blob", self.unrelated), self.entry("unsolved_math_prioritization", "tree", unsolved)])
        self.commits[m.HEAD] = {"sha": m.HEAD, "tree": {"sha": self.root}, "parents": [], "message": "historical text without final newline"}

    @staticmethod
    def entry(path, kind, sha):
        return {"path": path, "mode": "040000" if kind == "tree" else "100644", "type": kind, "sha": sha}

    def put_blob(self, data):
        ident = m.oid("blob", data)
        self.blobs[ident] = data
        return ident

    def put_tree(self, entries):
        ident = m.oid("tree", m.tree_bytes(entries))
        self.trees[ident] = copy.deepcopy(entries)
        return ident

    def request(self, method, endpoint, payload=None):
        self.calls.append((method, endpoint, copy.deepcopy(payload)))
        fail = (method + " " + endpoint) == self.fail
        if fail and not self.fail_after:
            raise OSError("synthetic error before server operation")
        if method == "GET":
            if endpoint == "pulls/411":
                h = m.HEAD if self.stale else self.head
                response = {"number": 411, "state": "open", "draft": True, "title": self.title, "body": self.body,
                            "head": {"sha": h, "ref": m.BRANCH, "repo": {"full_name": m.REPO}}}
            elif endpoint.startswith("git/ref/"):
                h = m.HEAD if self.stale else self.head
                response = {"ref": "refs/heads/" + m.BRANCH, "object": {"sha": h, "type": "commit"}}
            elif endpoint.startswith("git/trees/"):
                ident = endpoint.rsplit("/", 1)[1]
                response = {"sha": ident, "truncated": False, "tree": self.trees[ident]}
            elif endpoint.startswith("git/blobs/"):
                ident = endpoint.rsplit("/", 1)[1]; data = self.blobs[ident]
                response = {"sha": ident, "size": len(data), "encoding": "base64", "content": base64.b64encode(data).decode()}
            elif endpoint.startswith("git/commits/"):
                response = self.commits[endpoint.rsplit("/", 1)[1]]
            else:
                raise AssertionError(endpoint)
        elif endpoint == "git/blobs":
            response = {"sha": self.put_blob(base64.b64decode(payload["content"]))}
        elif endpoint == "git/trees":
            response = {"sha": self.put_tree(payload["tree"])}
        elif endpoint == "git/commits":
            # Independent serialization, validated against git hash-object below.
            lines = ["tree " + payload["tree"], "parent " + payload["parents"][0]]
            for role in ("author", "committer"):
                w = payload[role]
                ts = int(m.dt.datetime.fromisoformat(w["date"].replace("Z", "+00:00")).timestamp())
                lines.append(f"{role} {w['name']} <{w['email']}> {ts} +0000")
            data = ("\n".join(lines) + "\n\n" + payload["message"]).encode()
            ident = subprocess.run(["git", "hash-object", "-t", "commit", "--stdin"], input=data,
                                   capture_output=True, check=True).stdout.decode().strip()
            response = {"sha": ident, "tree": {"sha": payload["tree"]}, "parents": [{"sha": payload["parents"][0]}],
                        "message": payload["message"].removesuffix("\n"), "author": payload["author"], "committer": payload["committer"]}
            self.commits[ident] = response
        elif endpoint.startswith("git/refs/"):
            assert payload["force"] is False
            self.head = payload["sha"]
            response = {"object": {"sha": self.head}}
        elif endpoint == "pulls/411":
            assert set(payload) == {"body"}
            self.body = payload["body"]
            response = {"body": self.body}
        else:
            raise AssertionError((method, endpoint))
        if fail:
            raise OSError("synthetic server applied request; response lost")
        return copy.deepcopy(response)


class UpdaterTests(unittest.TestCase):
    def setUp(self):
        # Synthetic fixtures are ephemeral and removed in teardown. Retained
        # request/response models go only to the private fixture directory.
        self.temp = tempfile.TemporaryDirectory(prefix="offline_test_", dir=m.HERE)
        self.tmp = Path(self.temp.name)
        self.evidence_temp = tempfile.TemporaryDirectory(prefix="offline_models_", dir=m.PRIVATE)
        self.api = MockAPI()
        self.qpatch = patch.multiple(m, QBLOB=self.api.qblob, QHASH=self.api.qhash)
        self.qpatch.start()
        self.pkg = self.tmp / "package"; self.pkg.mkdir()
        self.file = self.pkg / "packet.txt"; self.file.write_bytes(b"synthetic complete prepared scientific packet\n")
        data = self.file.read_bytes()
        self.body = self.tmp / "body.md"; self.body.write_text("new parent-approved complete packet body\n")
        self.receipt = self.tmp / "receipt.json"
        source = {"pr": 411, "problem_id": "6800014", "source_head": m.HEAD, "branch": m.BRANCH,
                  "queue_blob_sha": self.api.qblob, "queue_sha256": self.api.qhash, "status": "claimed_solved",
                  "author_turns": "2/5", "selected_tree_sha": self.api.selected, "source_file_count": 1,
                  "files": [{"remote_path": m.PREFIX + "packet.txt", "blob_sha": self.api.old, "mode": "100644"}]}
        self.receipt.write_bytes(m.encoded(source))
        who = {"name": "Synthetic Test", "email": "test@example.invalid", "date": "2026-10-13T00:00:00Z"}
        self.spec = {"schema": 1, "package_root": str(self.pkg), "files": [{"local_path": str(self.file),
                     "remote_path": m.PREFIX + "packet.txt", "sha256": m.sha(data), "blob_sha": m.oid("blob", data),
                     "mode": "100644", "size": len(data)}],
                     "body": {"local_path": str(self.body), "sha256": m.sha(self.body.read_bytes()), "complete_packet_approved": True},
                     "source_receipt": {"local_path": str(self.receipt), "sha256": m.sha(self.receipt.read_bytes())},
                     "commit": {"message": "Prepared synthetic packet\n", "author": who, "committer": who}}
        self.specfile = self.tmp / "spec.json"
        self.write_spec()
        self.journal = self.tmp / "journal.json"
        self.counter = 0

    def tearDown(self):
        self.qpatch.stop(); self.temp.cleanup(); self.evidence_temp.cleanup()

    def write_spec(self):
        self.specfile.write_bytes(m.encoded(self.spec))

    def engine(self, journal=False):
        self.counter += 1
        return m.Engine(self.api, Path(self.evidence_temp.name) / str(self.counter), self.journal if journal else None)

    def prepared(self):
        return self.engine().prepare(self.specfile)

    def writes(self):
        return [x for x in self.api.calls if x[0] != "GET"]

    def test_read_only_plan_and_first_gate(self):
        plan, _, _ = self.prepared()
        self.assertFalse(self.writes())
        self.assertEqual(self.api.calls[0][:2], ("GET", "pulls/411"))
        self.assertEqual(plan["source_receipt_sha256"], self.spec["source_receipt"]["sha256"])
        self.api.head = "f" * 40
        with patch.object(m, "read_regular", side_effect=AssertionError("must gate before local reads")):
            with self.assertRaises(m.Stop): self.engine().prepare(self.specfile)

    def test_native_model_accepts_final_newline_normalization_and_preserves_siblings(self):
        plan, content, body = self.prepared()
        result = self.engine(True).apply(plan, content, body)
        self.assertEqual(result["status"], "confirmed_complete")
        self.assertEqual(result["evidence_kind"], "offline_mock")
        e = self.engine()
        self.assertEqual(e.lookup(plan["root_tree"], "outside.txt")["sha"], self.api.unrelated)
        self.assertEqual(e.lookup(plan["root_tree"], "unsolved_math_prioritization/attempts/unrelated")["sha"], self.api.unrelated)
        patches = [x for x in self.writes() if x[0] == "PATCH"]
        self.assertEqual(len(patches), 2)
        self.assertEqual(patches[0][2], {"sha": plan["commit_sha"], "force": False})
        self.assertEqual(set(patches[1][2]), {"body"})
        self.assertEqual(self.api.commits[plan["commit_sha"]]["message"], self.spec["commit"]["message"][:-1])

    def test_truncated_and_omitted_immediate_tree(self):
        orig = self.api.request
        for truncated in (True, False):
            def damaged(method, ep, payload=None):
                r = orig(method, ep, payload)
                if ep == "git/trees/" + self.api.root:
                    r["truncated"] = truncated
                    r["tree"] = r["tree"][:-1]
                return r
            with patch.object(self.api, "request", side_effect=damaged):
                with self.assertRaises(m.Stop): self.prepared()
        self.assertFalse(self.writes())

    def test_header_derived_status_and_turns(self):
        for status, turns in (("open", "2/5"), ("claimed_solved", "3/5")):
            old = self.api.blobs[self.api.qblob]
            altered = old.replace(b"claimed_solved", status.encode()).replace(b"2/5", turns.encode())
            q = self.api.put_blob(altered)
            for t in self.api.trees.values():
                for entry in t:
                    if entry["path"] == "QUEUE.md": entry["sha"] = q
            # Direct isolated gate-row test uses a valid native Merkle chain.
            a = self.api.put_tree([self.api.entry("6800014", "tree", self.api.selected)])
            u = self.api.put_tree([self.api.entry("QUEUE.md", "blob", q), self.api.entry("attempts", "tree", a)])
            root = self.api.put_tree([self.api.entry("unsolved_math_prioritization", "tree", u)])
            self.api.commits[m.HEAD]["tree"]["sha"] = root
            with patch.multiple(m, QBLOB=q, QHASH=m.sha(altered)):
                with self.assertRaisesRegex(m.Stop, "status/turns"): self.engine().gate()

    def test_candidate_body_receipt_and_mode_pins(self):
        for key, value in (("sha256", "0" * 64), ("blob_sha", "0" * 40), ("mode", "100755"), ("size", 1)):
            old = self.spec["files"][0][key]; self.spec["files"][0][key] = value; self.write_spec()
            with self.assertRaises(m.Stop): self.prepared()
            self.spec["files"][0][key] = old
        for section in ("body", "source_receipt"):
            old = self.spec[section]["sha256"]; self.spec[section]["sha256"] = "0" * 64; self.write_spec()
            with self.assertRaises(m.Stop): self.prepared()
            self.spec[section]["sha256"] = old
        self.assertFalse(self.writes())

    def test_private_symlink_fifo_extra_and_wrong_path(self):
        extra = self.pkg / "extra.txt"; extra.write_bytes(b"synthetic extra")
        with self.assertRaisesRegex(m.Stop, "extras"): self.prepared()
        extra.unlink()
        symlink = self.pkg / "linked"; symlink.symlink_to(self.file)
        with self.assertRaisesRegex(m.Stop, "symlink"): self.prepared()
        symlink.unlink()
        fifo = self.pkg / "fifo"; os.mkfifo(fifo)
        with self.assertRaisesRegex(m.Stop, "nonregular"): self.prepared()
        fifo.unlink()
        with self.assertRaisesRegex(m.Stop, "private"): m.read_regular(m.PRIVATE / "no-read")
        with self.assertRaisesRegex(m.Stop, "private"): m.safe_path(self.tmp / "Private_Sources" / "no-read")
        with self.assertRaisesRegex(m.Stop, "unsafe remote"): m.remote(m.PREFIX + "Private_Sources/no-publish")
        self.spec["files"][0]["remote_path"] = "unsolved_math_prioritization/QUEUE.md"; self.write_spec()
        with self.assertRaisesRegex(m.Stop, "outside positive"): self.prepared()
        self.assertFalse(self.writes())

    def test_body_head_title_drift_before_objects(self):
        for field in ("body", "head", "title"):
            plan, content, body = self.prepared()
            old = getattr(self.api, field); setattr(self.api, field, "drift")
            with self.assertRaises(m.Stop): self.engine(True).apply(plan, content, body)
            self.assertFalse(self.writes()); setattr(self.api, field, old); self.journal.unlink()

    def test_errors_before_objects_and_ref_no_automatic_retry(self):
        for endpoint in ("git/blobs", "git/trees", "git/commits", "git/refs/heads/" + m.BRANCH):
            plan, content, body = self.prepared()
            self.api.fail = ("PATCH " if endpoint.startswith("git/refs/") else "POST ") + endpoint
            with self.assertRaises(m.Stop): self.engine(True).apply(plan, content, body)
            j = json.loads(self.journal.read_text())
            self.assertEqual(j["phase"], "unknown_write")
            self.assertEqual(sum(x[0] + " " + x[1] == self.api.fail for x in self.writes()), 1)
            self.assertFalse(any(x[1] == "pulls/411" for x in self.writes()))
            self.api.calls.clear(); self.api.fail = None; self.journal.unlink()

    def test_ref_applied_unknown_then_stale_get_and_later_reconcile(self):
        plan, content, body = self.prepared()
        self.api.fail = "PATCH git/refs/heads/" + m.BRANCH; self.api.fail_after = True
        with self.assertRaises(m.Stop): self.engine(True).apply(plan, content, body)
        self.assertEqual(self.api.head, plan["commit_sha"])
        self.assertFalse(any(x[1] == "pulls/411" for x in self.writes()))
        self.api.fail = None; before = len(self.writes()); self.api.stale = True
        result = self.engine().reconcile(self.journal)
        self.assertEqual(result["status"], "source_head_observed_no_branch_confirmation")
        self.api.stale = False
        self.assertEqual(self.engine().reconcile(self.journal)["status"], "branch_confirmed_body_pending")
        self.assertEqual(len(self.writes()), before)

    def test_body_unknown_applied_and_unknown_not_applied(self):
        for applied in (False, True):
            self.api.head = m.HEAD; self.api.body = "old approved draft body\n"; self.api.calls.clear()
            plan, content, body = self.prepared()
            self.api.fail = "PATCH pulls/411"; self.api.fail_after = applied
            with self.assertRaises(m.Stop): self.engine(True).apply(plan, content, body)
            before = len(self.writes()); self.api.fail = None
            expected = "confirmed_complete" if applied else "branch_confirmed_body_pending"
            result = self.engine().reconcile(self.journal)
            self.assertEqual(result["status"], expected)
            self.assertEqual(result["evidence_kind"], "offline_mock")
            self.assertEqual(len(self.writes()), before); self.journal.unlink()


if __name__ == "__main__":
    unittest.main(verbosity=2)
