"""Offline checks for the local Zenodo deposit flow."""

import argparse
import copy
import hashlib
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import zenodo


class FakeZenodo:
    def __init__(self):
        self.records = {}
        self.creates = 0
        self.uploads = 0
        self.publishes = 0

    def create(self, metadata):
        self.creates += 1
        record = {"id": 123, "metadata": copy.deepcopy(metadata), "files": [],
                  "submitted": False, "links": {"bucket": "https://zenodo.org/api/files/test",
                                                 "html": "https://zenodo.org/deposit/123"}}
        self.records[123] = record
        return copy.deepcopy(record)

    def get(self, deposit_id):
        return copy.deepcopy(self.records[deposit_id])

    def upload(self, bucket, entry):
        self.uploads += 1
        self.records[123]["files"].append({"filename": entry["name"],
                                            "checksum": "md5:" + entry["md5"],
                                            "filesize": entry["size"]})
        return {}

    def update(self, deposit_id, metadata):
        self.records[deposit_id]["metadata"] = copy.deepcopy(metadata)
        return self.get(deposit_id)

    def publish(self, deposit_id):
        self.publishes += 1
        self.records[deposit_id]["submitted"] = True
        return {"doi": "10.5281/zenodo.123", "doi_url": "https://doi.org/10.5281/zenodo.123"}


class DepositFlowTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        root = Path(self.temp.name)
        self.state_patch = patch.object(zenodo, "STATE_DIR", root / "state")
        self.state_patch.start()
        self.addCleanup(self.state_patch.stop)
        (root / "paper.pdf").write_bytes(b"paper content")
        self.manifest = root / "deposit.json"
        self.metadata = {"title": "Test paper", "description": "Abstract", "upload_type": "publication",
                         "publication_type": "preprint", "creators": [{"name": "Kriebel, Alec"}]}
        self.write_manifest()
        self.client = FakeZenodo()

    def write_manifest(self, files=None):
        self.manifest.write_text(json.dumps({"metadata": self.metadata,
                                            "files": files or [{"path": "paper.pdf"}]}))

    def call(self, command, confirm_id=None):
        args = argparse.Namespace(command=command, manifest=self.manifest, sandbox=False,
                                  confirm_id=confirm_id)
        return zenodo.run(args, self.client)

    def test_stage_resumes_and_publish_requires_exact_id(self):
        checked = self.call("check")
        self.assertEqual(checked["files"][0]["sha256"], hashlib.sha256(b"paper content").hexdigest())
        first = self.call("stage")
        self.assertEqual(first["id"], 123)
        self.call("stage")
        self.assertEqual((self.client.creates, self.client.uploads), (1, 1))
        self.assertEqual(self.call("inspect")["state"], "ready_to_publish")
        with self.assertRaisesRegex(zenodo.DepositError, "confirm-id"):
            self.call("publish", 999)
        self.assertEqual(self.client.publishes, 0)
        result = self.call("publish", 123)
        self.assertEqual(result["doi"], "10.5281/zenodo.123")
        with self.assertRaisesRegex(zenodo.DepositError, "already published"):
            self.call("stage")

    def test_changed_file_and_unlisted_file_block_publication(self):
        self.call("stage")
        (self.manifest.parent / "paper.pdf").write_bytes(b"changed")
        with self.assertRaisesRegex(zenodo.DepositError, "checksum/size differs"):
            self.call("publish", 123)
        self.assertEqual(self.client.publishes, 0)
        (self.manifest.parent / "paper.pdf").write_bytes(b"paper content")
        self.client.records[123]["files"].append({"filename": "extra.txt", "checksum": "md5:0", "filesize": 1})
        with self.assertRaisesRegex(zenodo.DepositError, "file list differs"):
            self.call("publish", 123)

    def test_duplicate_names_rejected_before_network(self):
        self.write_manifest([{"path": "paper.pdf"}, {"path": "paper.pdf"}])
        with self.assertRaisesRegex(zenodo.DepositError, "Duplicate"):
            self.call("stage")
        self.assertEqual(self.client.creates, 0)

    def test_token_file_permissions_and_environment_separation(self):
        secrets = self.manifest.parent / "zenodo.env"
        secrets.write_text("ZENODO_TOKEN=production\nZENODO_SANDBOX_TOKEN=sandbox\n")
        with patch.object(zenodo, "SECRETS", secrets), patch.dict("os.environ", {}, clear=True):
            secrets.chmod(0o644)
            with self.assertRaisesRegex(zenodo.DepositError, "mode 600"):
                zenodo.token_for("production")
            secrets.chmod(0o600)
            self.assertEqual(zenodo.token_for("production"), "production")
            self.assertEqual(zenodo.token_for("sandbox"), "sandbox")

    def test_api_request_uses_bearer_header_and_rejects_other_hosts(self):
        class Response:
            status = 201

            def read(self, maximum):
                return b'{"id": 123}'

        class Connection:
            def __init__(self, host, timeout):
                self.host = host
                self.headers = {}
                self.body = b""

            def putrequest(self, method, target):
                self.method, self.target = method, target

            def putheader(self, key, value):
                self.headers[key] = value

            def endheaders(self):
                pass

            def send(self, data):
                self.body += data

            def getresponse(self):
                return Response()

            def close(self):
                pass

        connections = []

        def connect(host, timeout):
            connection = Connection(host, timeout)
            connections.append(connection)
            return connection

        client = zenodo.ZenodoClient("production", "private-token")
        with patch.object(zenodo.http.client, "HTTPSConnection", side_effect=connect):
            self.assertEqual(client.create(self.metadata)["id"], 123)
            with self.assertRaisesRegex(zenodo.DepositError, "outside"):
                client.request("PUT", "https://other.example/api/files/steal")
        self.assertEqual(len(connections), 1)
        self.assertEqual(connections[0].headers["Authorization"], "Bearer private-token")
        self.assertEqual(connections[0].headers["User-Agent"], "Math-Zenodo-Deposit-Tool/1.0")
        self.assertNotIn("private-token", connections[0].target)
        self.assertEqual(json.loads(connections[0].body), {"metadata": self.metadata})


if __name__ == "__main__":
    unittest.main()
