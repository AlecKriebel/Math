"""Offline checks for the local Zenodo deposit flow."""

import argparse
import copy
import hashlib
import json
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import MagicMock, patch
from urllib.error import HTTPError, URLError
from urllib.request import Request

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
        self.records[deposit_id]["doi"] = "10.5281/zenodo.123"
        return self.get(deposit_id)


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
        self.doi_patch = patch.object(zenodo, "doi_status", return_value={"status": "not_resolved", "http_status": 404})
        self.doi_check = self.doi_patch.start()
        self.addCleanup(self.doi_patch.stop)

    def write_manifest(self, files=None):
        self.manifest.write_text(json.dumps({"metadata": self.metadata,
                                            "files": files or [{"path": "paper.pdf"}]}))

    def call(self, command, confirm_id=None, check_doi=False):
        args = argparse.Namespace(command=command, manifest=self.manifest, sandbox=False,
                                  confirm_id=confirm_id, check_doi=check_doi)
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

    def test_published_retry_is_read_only_but_still_checks_id_and_manifest(self):
        self.call("stage")
        first = self.call("publish", 123)
        self.assertEqual(first["state"], "published")
        self.assertEqual(first["doi_resolution"]["status"], "not_resolved")
        self.assertEqual(first["record_url"], "https://zenodo.org/records/123")
        retry = self.call("publish", 123)
        self.assertTrue(retry["already_published"])
        self.assertEqual(self.client.publishes, 1)
        with self.assertRaisesRegex(zenodo.DepositError, "confirm-id"):
            self.call("publish", 124)
        self.metadata["title"] = "Changed title"
        self.write_manifest()
        with self.assertRaisesRegex(zenodo.DepositError, "metadata differs"):
            self.call("publish", 123)
        self.assertEqual(self.client.publishes, 1)

    def test_publish_timeout_recovers_saved_record_without_second_post(self):
        self.call("stage")
        publish = self.client.publish

        def committed_but_response_lost(deposit_id):
            publish(deposit_id)
            raise zenodo.DepositError("connection timed out")

        def check_after_saved(doi):
            state = zenodo.read_json(zenodo.state_path(self.manifest.resolve(), "production"))
            self.assertEqual(state["publication"]["state"], "published")
            self.assertEqual(state["publication"]["doi_resolution"]["status"], "not_checked")
            return {"status": "unavailable"}

        self.doi_check.side_effect = check_after_saved
        with patch.object(self.client, "publish", side_effect=committed_but_response_lost):
            result = self.call("publish", 123)
        self.assertTrue(result["recovered_after_publish_error"])
        self.assertEqual(result["state"], "published")
        self.assertEqual(result["doi_resolution"]["status"], "unavailable")
        self.assertEqual(self.client.publishes, 1)
        self.assertTrue(result["receipt_saved"])

    def test_unconfirmed_post_does_not_claim_publication_or_retry(self):
        self.call("stage")
        for response in (None, zenodo.DepositError("request rejected")):
            with self.subTest(response=response):
                with patch.object(self.client, "publish", side_effect=response, return_value={}) as publish:
                    with self.assertRaisesRegex(zenodo.DepositError, "not confirmed publication"):
                        self.call("publish", 123)
                    publish.assert_called_once_with(123)
        self.doi_check.assert_not_called()

    def test_unavailable_post_confirmation_reports_uncertainty(self):
        self.call("stage")
        original = self.client.get(123)
        with patch.object(self.client, "get", side_effect=[original, zenodo.DepositError("offline")]):
            with patch.object(self.client, "publish", return_value={}) as publish:
                with self.assertRaisesRegex(zenodo.DepositError, "outcome is unconfirmed.*Run inspect"):
                    self.call("publish", 123)
                publish.assert_called_once_with(123)

    def test_identity_and_boolean_state_are_required_before_publication(self):
        self.call("stage")
        for key, value, pattern in [("id", 999, "different deposition"),
                                    ("submitted", "false", "invalid publication state")]:
            with self.subTest(key=key):
                original = self.client.records[123][key]
                self.client.records[123][key] = value
                with self.assertRaisesRegex(zenodo.DepositError, pattern):
                    self.call("publish", 123)
                self.client.records[123][key] = original
        self.assertEqual(self.client.publishes, 0)

    def test_receipt_disk_failure_preserves_confirmed_publication_result(self):
        self.call("stage")
        with patch.object(zenodo, "save_state", side_effect=OSError("disk full")):
            result = self.call("publish", 123)
        self.assertEqual(result["state"], "published")
        self.assertFalse(result["receipt_saved"])
        self.assertIn("Publication is confirmed", result["receipt_warning"])

    def test_malformed_doi_cannot_prevent_saved_publication(self):
        self.call("stage")
        publish = self.client.publish

        def malformed_doi(deposit_id):
            record = publish(deposit_id)
            self.client.records[deposit_id]["doi"] = 123
            return record

        self.doi_check.return_value = {"status": "unavailable"}
        with patch.object(self.client, "publish", side_effect=malformed_doi):
            result = self.call("publish", 123)
        self.assertEqual(result["state"], "published")
        self.assertIsNone(result["doi"])
        self.assertTrue(result["receipt_saved"])
        self.assertIn("publication is confirmed", result["doi_warning"])
        self.assertEqual(result["doi_resolution"]["status"], "unavailable")
        saved = zenodo.read_json(zenodo.state_path(self.manifest.resolve(), "production"))
        self.assertEqual(saved["publication"]["state"], "published")

    def test_missing_doi_does_not_negate_publication(self):
        self.call("stage")
        self.client.records[123]["submitted"] = True
        result = self.call("inspect")
        self.assertEqual(result["state"], "published")
        self.assertEqual(result["doi_resolution"]["status"], "not_assigned")
        self.assertEqual(result["url"], "https://zenodo.org/records/123")

    def test_post_publish_mismatch_explicitly_reports_published_but_unverified(self):
        self.call("stage")
        publish = self.client.publish

        def corrupt_metadata(deposit_id):
            publish(deposit_id)
            self.client.records[deposit_id]["metadata"]["title"] = "Other title"
            return {}

        with patch.object(self.client, "publish", side_effect=corrupt_metadata):
            with self.assertRaisesRegex(zenodo.DepositError, "reports publication, but verification failed"):
                self.call("publish", 123)
        self.doi_check.assert_not_called()

    def test_inspect_doi_check_is_opt_in_and_recovers_existing_receipt(self):
        self.call("stage")
        self.client.publish(123)
        result = self.call("inspect")
        self.assertEqual(result["doi_resolution"]["status"], "not_checked")
        self.doi_check.assert_not_called()
        self.assertEqual(self.call("inspect", check_doi=True)["doi_resolution"]["status"], "not_resolved")
        self.doi_check.assert_called_once_with("10.5281/zenodo.123")

    def test_ambiguous_creation_demands_account_reconciliation(self):
        with patch.object(self.client, "create", side_effect=zenodo.DepositError("connection lost")):
            with self.assertRaisesRegex(zenodo.DepositError, "reconcile your Zenodo account"):
                self.call("stage")

    def test_malformed_metadata_and_file_lists_are_controlled_errors(self):
        self.call("stage")
        for key, value in [("metadata", None), ("files", None), ("files", [None])]:
            with self.subTest(key=key, value=value):
                original = self.client.records[123][key]
                self.client.records[123][key] = value
                with self.assertRaises(zenodo.DepositError):
                    self.call("inspect")
                self.client.records[123][key] = original

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


class ResponseAndResolverTests(unittest.TestCase):
    def api_reply(self, status, body):
        response = SimpleNamespace(status=status, read=lambda maximum: body[:maximum])
        connection = MagicMock()
        connection.getresponse.return_value = response
        with patch.object(zenodo.http.client, "HTTPSConnection", return_value=connection):
            return zenodo.ZenodoClient("production", "private-token").get(123)

    def test_html_traffic_filter_is_distinguished_without_echoing_body(self):
        body = b"<html>restricted due to unusual traffic private-token <script>secret</script></html>"
        with self.assertRaises(zenodo.DepositError) as caught:
            self.api_reply(403, body)
        self.assertIn("HTML traffic filter", str(caught.exception))
        self.assertNotIn("private-token", str(caught.exception))
        self.assertNotIn("secret", str(caught.exception))

    def test_api_auth_errors_and_validation_details_are_redacted(self):
        for status, hint in [(401, "environment"), (403, "token scopes"), (429, "rate limited")]:
            with self.subTest(status=status):
                body = json.dumps({"message": "bad private-token", "errors": ["private-token"]}).encode()
                with self.assertRaises(zenodo.DepositError) as caught:
                    self.api_reply(status, body)
                self.assertIn(hint, str(caught.exception))
                self.assertNotIn("private-token", str(caught.exception))
                self.assertIn("[redacted]", str(caught.exception))

    def test_malformed_success_responses_are_never_treated_as_success(self):
        for body in [b"", b"{}", b"[]", b"<html>proxy error</html>", b"\xff",
                     b'{"data":"' + b"x" * zenodo.MAX_RESPONSE_BYTES + b'"}']:
            with self.subTest(prefix=body[:30]):
                with self.assertRaisesRegex(zenodo.DepositError, "unconfirmed"):
                    self.api_reply(200, body)

    def test_doi_check_reports_http_and_network_results_without_auth(self):
        for outcome, expected in [(404, "not_resolved"), (503, "unavailable"),
                                  (URLError("offline"), "unavailable"),
                                  (ValueError("Invalid IPv6 URL"), "unavailable"), (200, "resolved")]:
            with self.subTest(outcome=outcome):
                opener = MagicMock()
                if isinstance(outcome, int) and outcome != 200:
                    opener.open.side_effect = HTTPError("https://doi.org/test", outcome, "error", {}, None)
                elif isinstance(outcome, Exception):
                    opener.open.side_effect = outcome
                else:
                    opener.open.return_value.__enter__.return_value = SimpleNamespace(
                        status=200, url="https://zenodo.org/records/123")
                with patch.object(zenodo, "build_opener", return_value=opener):
                    result = zenodo.doi_status("10.5281/zenodo.123")
                self.assertEqual(result["status"], expected)
                request = opener.open.call_args.args[0]
                self.assertEqual(request.full_url, "https://doi.org/10.5281/zenodo.123")
                self.assertIsNone(request.get_header("Authorization"))
                self.assertEqual(request.get_header("User-agent"), zenodo.USER_AGENT)
        self.assertEqual(zenodo.doi_status(None)["status"], "not_assigned")
        for invalid in [123, {"doi": "wrong type"}, "10.5281/\ud800"]:
            self.assertEqual(zenodo.doi_status(invalid)["status"], "unavailable")

    def test_doi_redirects_reject_http_and_credentials(self):
        handler = zenodo.PublicDOIRedirects()
        request = Request("https://doi.org/10.5281/zenodo.123", headers={"User-Agent": zenodo.USER_AGENT})
        for url in ["http://zenodo.org/records/123", "https://user:password@zenodo.org/records/123"]:
            with self.assertRaises(HTTPError) as caught:
                handler.redirect_request(request, None, 302, "Found", {}, url)
            caught.exception.close()
        redirected = handler.redirect_request(request, None, 302, "Found", {}, "https://zenodo.org/records/123")
        self.assertIsNone(redirected.get_header("Authorization"))
        self.assertEqual(handler.max_redirections, 3)


if __name__ == "__main__":
    unittest.main()
