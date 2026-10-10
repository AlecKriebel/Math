"""Offline checks for metadata updates on records published outside this tool."""

import argparse
import copy
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import metadata_updates as updates
import zenodo


class ExistingRecord:
    def __init__(self):
        self.record = {
            "id": 123, "state": "done", "submitted": True, "doi": "10.5281/zenodo.123",
            "metadata": {"title": "Existing paper", "description": "Original abstract",
                         "upload_type": "publication", "publication_type": "preprint",
                         "creators": [{"name": "Kriebel, Alec", "orcid": "0009-0001-9320-500X"}],
                         "publication_date": "2026-09-26", "access_right": "open", "license": "cc-by-4.0",
                         "doi": "10.5281/zenodo.123", "keywords": ["original"],
                         "related_identifiers": [{"identifier": "https://example.org/code", "relation": "isSupplementTo"}],
                         "prereserve_doi": {"doi": "10.5281/zenodo.123", "recid": 123}},
            "files": [{"filename": "paper.pdf", "checksum": "md5:" + "a" * 32, "filesize": 42}],
        }
        self.published = copy.deepcopy(self.record)
        self.calls = []

    def get(self, record_id):
        self.calls.append("get")
        return copy.deepcopy(self.record)

    def native_get(self, record_id, draft=False):
        source = self.record if draft else self.published
        legacy = source["metadata"]
        authors = []
        for author in legacy["creators"]:
            family, given = (part.strip() for part in author["name"].split(","))
            person = {"type": "personal", "name": author["name"], "family_name": family, "given_name": given}
            if author.get("orcid"):
                person["identifiers"] = [{"scheme": "orcid", "identifier": author["orcid"]}]
            authors.append({"person_or_org": person, "affiliations": (
                [{"name": author["affiliation"]}] if author.get("affiliation") else [])})
        metadata = {"title": legacy["title"], "description": legacy["description"],
                    "creators": authors, "publication_date": legacy["publication_date"],
                    "resource_type": {"id": "publication-preprint"}, "publisher": "Zenodo",
                    "rights": [{"id": legacy.get("license", "cc-by-4.0")}]}
        if legacy.get("keywords"):
            metadata["subjects"] = [{"subject": item} for item in legacy["keywords"]]
        if legacy.get("related_identifiers"):
            metadata["related_identifiers"] = copy.deepcopy(legacy["related_identifiers"])
        if legacy.get("notes"):
            metadata["additional_descriptions"] = [{"description": legacy["notes"], "type": {"id": "notes"}}]
        return {"id": str(record_id), "metadata": metadata, "custom_fields": {},
                "access": {"record": "public", "files": "public"},
                "pids": {"doi": {"identifier": source["doi"]}}}

    def edit(self, record_id):
        self.calls.append("edit")
        assert self.record["state"] == "done"
        self.record["state"] = "inprogress"
        # submitted remains true in Zenodo's edit session.
        return self.get(record_id)

    def update(self, record_id, metadata):
        self.calls.append("update")
        assert self.record["state"] == "inprogress"
        self.record["metadata"] = copy.deepcopy(metadata)
        return self.get(record_id)

    def publish(self, record_id):
        self.calls.append("publish")
        self.record["state"] = "done"
        self.published = copy.deepcopy(self.record)
        return self.get(record_id)

    def discard(self, record_id):
        self.calls.append("discard")
        self.record = copy.deepcopy(self.published)
        return self.get(record_id)

    @property
    def mutations(self):
        return [call for call in self.calls if call != "get"]


class MetadataUpdateTests(unittest.TestCase):
    def setUp(self):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        self.root = Path(directory.name)
        patched = patch.object(zenodo, "STATE_DIR", self.root / "state")
        patched.start()
        self.addCleanup(patched.stop)
        self.client = ExistingRecord()
        self.patch_path = self.root / "patch.json"
        self.write_patch({"keywords": ["group theory", "spectral bounds"], "description": "Improved abstract"})

    def write_patch(self, metadata):
        self.patch_path.write_text(json.dumps({"metadata": metadata}))

    def call(self, command="update-metadata", confirm_id=None, sandbox=False, **kwargs):
        args = argparse.Namespace(command=command, record_id=123, patch=self.patch_path,
                                  sandbox=sandbox, confirm_id=confirm_id, **kwargs)
        return zenodo.run(args, self.client)

    def test_default_preview_is_read_only_and_preserves_omitted_fields(self):
        result = self.call()
        self.assertTrue(result["dry_run"])
        self.assertEqual(self.client.mutations, [])
        self.assertFalse((self.root / "state").exists())
        self.assertEqual({item["field"] for item in result["changes"]}, {"keywords", "description"})
        for field in ("creators", "publication_date", "license", "doi", "related_identifiers"):
            self.assertEqual(result["metadata"][field], self.client.record["metadata"][field])
        self.assertNotIn("prereserve_doi", result["metadata"])

    def test_stage_then_publish_preserves_identity_assets_and_lists_replace(self):
        original = copy.deepcopy(self.client.record)
        staged = self.call(confirm_id=123)
        self.assertEqual(staged["state"], "ready_to_publish_metadata")
        self.assertEqual(self.client.mutations, ["edit", "update"])
        self.assertEqual(self.client.record["metadata"]["keywords"], ["group theory", "spectral bounds"])
        self.assertEqual(self.client.published, original)
        session = zenodo.read_json(updates.snapshot_path(123, "production"))
        self.assertEqual(session["original_metadata"]["keywords"], ["original"])
        self.assertEqual(session["phase"], "staged")
        self.assertEqual(updates.snapshot_path(123, "production").stat().st_mode & 0o777, 0o600)
        result = self.call("publish-metadata", 123)
        self.assertEqual(result["state"], "published")
        self.assertEqual(result["doi"], original["doi"])
        self.assertEqual(self.client.record["files"], original["files"])
        self.assertEqual(self.client.mutations, ["edit", "update", "publish"])
        self.assertTrue(self.call("publish-metadata", 123)["already_complete"])
        self.assertEqual(self.client.mutations.count("publish"), 1)

    def test_discard_restores_original_metadata_and_repeated_discard_is_read_only(self):
        original = updates.editable_metadata(self.client.record)
        self.call(confirm_id=123)
        result = self.call("discard-metadata", 123)
        self.assertEqual(result["state"], "discarded")
        self.assertEqual(result["metadata"], original)
        self.assertTrue(self.call("discard-metadata", 123)["already_complete"])
        self.assertEqual(self.client.mutations, ["edit", "update", "discard"])

    def test_confirmation_and_invalid_patch_are_checked_before_requests(self):
        for command in ("update-metadata", "publish-metadata", "discard-metadata"):
            with self.subTest(command=command):
                with self.assertRaisesRegex(zenodo.DepositError, "confirm-id"):
                    self.call(command, 124)
        for command in ("publish-metadata", "discard-metadata"):
            with self.assertRaisesRegex(zenodo.DepositError, "confirm-id"):
                self.call(command)
        for metadata in ({}, [], {"doi": "10.1234/other"}, {"prereserve_doi": True}, {"notes": None}):
            self.write_patch(metadata)
            with self.assertRaises(zenodo.DepositError):
                self.call(confirm_id=123)
        self.assertEqual(self.client.calls, [])

    def test_external_edit_session_and_unpublished_draft_are_rejected(self):
        self.client.record["state"] = "inprogress"
        with self.assertRaisesRegex(zenodo.DepositError, "already has an editing session"):
            self.call(confirm_id=123)
        self.client.record["submitted"] = False
        with self.assertRaisesRegex(zenodo.DepositError, "requires a published record"):
            self.call(confirm_id=123)
        self.assertEqual(self.client.mutations, [])

    def test_noop_does_not_open_session(self):
        self.write_patch({"title": "Existing paper"})
        self.assertEqual(self.call(confirm_id=123)["state"], "unchanged")
        self.assertEqual(self.client.mutations, [])

    def test_stage_resume_does_not_repeat_edit_or_update(self):
        self.call(confirm_id=123)
        self.call(confirm_id=123)
        self.assertEqual(self.client.mutations, ["edit", "update"])
        self.write_patch({"title": "Different patch"})
        with self.assertRaisesRegex(zenodo.DepositError, "different metadata edit is pending"):
            self.call(confirm_id=123)

    def test_state_written_before_every_mutation(self):
        for method, expected in (("edit", "edit_requested"), ("update", "update_requested"),
                                 ("publish", "publish_requested")):
            original = getattr(self.client, method)

            def wrapped(record_id, *args, original=original, expected=expected):
                session = zenodo.read_json(updates.snapshot_path(123, "production"))
                self.assertEqual(session["phase"], expected)
                self.assertEqual(session["original_metadata"]["description"], "Original abstract")
                return original(record_id, *args)

            replacement = patch.object(self.client, method, side_effect=wrapped)
            replacement.start()
            self.addCleanup(replacement.stop)
        self.call(confirm_id=123)
        self.call("publish-metadata", 123)

    def test_snapshot_write_failure_prevents_mutations(self):
        with patch.object(zenodo, "save_state", side_effect=OSError("disk full")):
            with self.assertRaisesRegex(zenodo.DepositError, "no further API mutation"):
                self.call(confirm_id=123)
        self.assertEqual(self.client.mutations, [])

    def test_publish_blocks_changed_files_doi_metadata_and_unrequested_fields(self):
        self.call(confirm_id=123)
        staged = copy.deepcopy(self.client.record)
        for change in (lambda record: record["files"][0].update(filesize=999),
                       lambda record: record.update(doi="10.1234/other"),
                       lambda record: record["metadata"].update(title="Different paper"),
                       lambda record: record["metadata"].update(notes="Unreviewed edit")):
            self.client.record = copy.deepcopy(staged)
            change(self.client.record)
            with self.assertRaises(zenodo.DepositError):
                self.call("publish-metadata", 123)
        self.assertNotIn("publish", self.client.mutations)

    def test_discard_refuses_to_erase_external_changes(self):
        self.call(confirm_id=123)
        self.client.record["metadata"]["notes"] = "Someone else's change"
        with self.assertRaisesRegex(zenodo.DepositError, "refusing to discard"):
            self.call("discard-metadata", 123)
        self.assertNotIn("discard", self.client.mutations)

    def test_lost_response_after_edit_update_and_publish_is_recovered_once(self):
        for method in ("edit", "update", "publish"):
            original = getattr(self.client, method)

            def wrapped(*args, original=original):
                original(*args)
                raise zenodo.DepositError("response lost")

            replacement = patch.object(self.client, method, side_effect=wrapped)
            replacement.start()
            self.addCleanup(replacement.stop)
        staged = self.call(confirm_id=123)
        self.assertTrue(staged["recovered_after_edit_error"])
        self.assertTrue(staged["recovered_after_update_error"])
        published = self.call("publish-metadata", 123)
        self.assertTrue(published["recovered_after_action_error"])
        self.assertEqual(self.client.mutations, ["edit", "update", "publish"])

    def test_failed_update_can_be_discarded_or_explicitly_resumed(self):
        with patch.object(self.client, "update", side_effect=zenodo.DepositError("rejected")) as mutation:
            with self.assertRaisesRegex(zenodo.DepositError, "unconfirmed or verification failed"):
                self.call(confirm_id=123)
            mutation.assert_called_once()
        self.assertEqual(self.client.record["state"], "inprogress")
        result = self.call(confirm_id=123)
        self.assertEqual(result["state"], "ready_to_publish_metadata")
        self.assertEqual(self.client.mutations, ["edit", "update"])

    def test_unavailable_confirmation_keeps_session_and_does_not_retry(self):
        self.call(confirm_id=123)
        get = self.client.get
        count = 0

        def unavailable(record_id):
            nonlocal count
            count += 1
            if count > 1:
                raise zenodo.DepositError("offline")
            return get(record_id)

        with patch.object(self.client, "get", side_effect=unavailable):
            with self.assertRaisesRegex(zenodo.DepositError, "outcome is unconfirmed"):
                self.call("publish-metadata", 123)
        # This fake publish modifies the remote state before losing its response.
        self.assertEqual(self.client.mutations.count("publish"), 1)
        self.assertEqual(zenodo.read_json(updates.snapshot_path(123, "production"))["phase"], "publish_requested")
        self.assertTrue(self.call("publish-metadata", 123)["already_complete"])
        self.assertEqual(self.client.mutations.count("publish"), 1)

    def test_completed_session_cannot_control_later_external_edit(self):
        self.call(confirm_id=123)
        self.call("publish-metadata", 123)
        self.client.edit(123)
        for command in ("publish-metadata", "discard-metadata"):
            with self.assertRaisesRegex(zenodo.DepositError, "newer editing session"):
                self.call(command, 123)

    def test_backend_drops_preserved_field_before_publish_is_failure(self):
        update = self.client.update

        def drops_license(record_id, metadata):
            update(record_id, metadata)
            del self.client.record["metadata"]["license"]

        with patch.object(self.client, "update", side_effect=drops_license):
            with self.assertRaisesRegex(zenodo.DepositError, "fields drifted"):
                self.call(confirm_id=123)
        self.assertNotIn("publish", self.client.mutations)

    def test_explicit_empty_list_clears_keywords(self):
        self.write_patch({"keywords": []})
        self.call(confirm_id=123)
        self.assertEqual(self.call("publish-metadata", 123)["metadata"]["keywords"], [])

    def test_known_creator_normalization_is_accepted(self):
        self.call(confirm_id=123)
        self.client.record["metadata"]["creators"][0]["affiliation"] = None
        result = self.call("publish-metadata", 123)
        self.assertEqual(result["metadata_normalizations"], [
            {"field": "creators", "kind": "omitted_creator_affiliation_to_null"}])

    def test_read_only_metadata_supports_unpublished_records(self):
        self.client.record["submitted"] = False
        self.client.record["state"] = "unsubmitted"
        self.assertFalse(self.call("metadata")["submitted"])
        self.assertEqual(self.client.mutations, [])

    def test_environment_separation_cannot_publish_production_session(self):
        self.call(confirm_id=123)
        with self.assertRaisesRegex(zenodo.DepositError, "No saved metadata edit"):
            self.call("publish-metadata", 123, sandbox=True)
        self.assertNotIn("publish", self.client.mutations)

    def test_client_uses_documented_edit_and_discard_endpoints(self):
        client = zenodo.ZenodoClient("sandbox", "private-token")
        with patch.object(client, "request", return_value={"id": 123}) as request:
            client.edit(123)
            request.assert_called_with("POST", "https://sandbox.zenodo.org/api/deposit/depositions/123/actions/edit")
            client.discard(123)
            request.assert_called_with("POST", "https://sandbox.zenodo.org/api/deposit/depositions/123/actions/discard")

    def test_client_requests_native_record_and_draft_representations(self):
        client = zenodo.ZenodoClient("production", "private-token")
        with patch.object(client, "request", return_value={"id": "123"}) as request:
            client.native_get(123)
            request.assert_called_with("GET", "https://zenodo.org/api/records/123",
                                       accept="application/vnd.inveniordm.v1+json")
            client.native_get(123, draft=True)
            request.assert_called_with("GET", "https://zenodo.org/api/records/123/draft",
                                       accept="application/vnd.inveniordm.v1+json")

    def test_rich_native_metadata_refused_before_edit(self):
        original = self.client.native_get(123)
        changes = [
            lambda native: native["metadata"]["creators"][0]["person_or_org"].update(type="organizational"),
            lambda native: native["metadata"]["creators"][0].update(affiliations=[{"name": "One"}, {"name": "Two"}]),
            lambda native: native["metadata"]["creators"][0].update(affiliations=[{"name": "One", "id": "01abc"}]),
            lambda native: native["metadata"]["creators"][0]["person_or_org"].update(identifiers=[{"scheme": "isni", "identifier": "123"}]),
            lambda native: native["metadata"].update(subjects=[{"id": "123", "subject": "Controlled"}]),
            lambda native: native["metadata"].update(additional_titles=[{"title": "Another"}]),
            lambda native: native["custom_fields"].update(rich="data"),
            lambda native: native["metadata"].update(languages=[{"id": "eng"}, {"id": "fra"}]),
            lambda native: native["metadata"].update(references=[{"reference": "Text", "identifier": "10.1234/a"}]),
        ]
        for change in changes:
            with self.subTest(change=change):
                native = copy.deepcopy(original)
                change(native)
                with patch.object(self.client, "native_get", return_value=native):
                    with self.assertRaisesRegex(zenodo.DepositError, "rich native metadata"):
                        self.call(confirm_id=123)
        self.assertEqual(self.client.mutations, [])

    def test_native_author_loss_after_put_cannot_be_published_and_can_be_discarded(self):
        native_get = self.client.native_get

        def hidden_change(record_id, draft=False):
            native = native_get(record_id, draft=draft)
            if draft and "update" in self.client.mutations:
                native["metadata"]["creators"][0]["person_or_org"]["given_name"] = "Other"
            return native

        with patch.object(self.client, "native_get", side_effect=hidden_change):
            with self.assertRaisesRegex(zenodo.DepositError, "not included in the patch changed"):
                self.call(confirm_id=123)
            with self.assertRaisesRegex(zenodo.DepositError, "not included in the patch changed"):
                self.call("publish-metadata", 123)
            self.assertEqual(self.call("discard-metadata", 123)["state"], "discarded")
        self.assertNotIn("publish", self.client.mutations)

    def test_native_drift_in_patched_fields_blocks_publication(self):
        self.call(confirm_id=123)
        native_get = self.client.native_get

        def hidden_change(record_id, draft=False):
            native = native_get(record_id, draft=draft)
            if draft:
                native["metadata"]["subjects"] = [{"subject": "group theory", "id": "Unexpected"},
                                                  {"subject": "spectral bounds"}]
            return native

        with patch.object(self.client, "native_get", side_effect=hidden_change):
            with self.assertRaisesRegex(zenodo.DepositError, "drifted from the staged snapshot"):
                self.call("publish-metadata", 123)
        self.assertNotIn("publish", self.client.mutations)

    def test_confirmed_retry_and_first_action_receipt_write_failures_keep_remote_status(self):
        self.call(confirm_id=123)
        save = zenodo.save_state

        def fail_final(place, value):
            if value["phase"] == "published":
                raise OSError("disk full")
            save(place, value)

        with patch.object(zenodo, "save_state", side_effect=fail_final):
            first = self.call("publish-metadata", 123)
            retry = self.call("publish-metadata", 123)
        for result in (first, retry):
            self.assertEqual(result["state"], "published")
            self.assertFalse(result["receipt_saved"])
        self.assertTrue(retry["already_complete"])
        self.assertEqual(self.client.mutations.count("publish"), 1)

    def test_local_lock_blocks_another_mutator_but_allows_read_only_preview(self):
        with updates.record_lock(123, "production"):
            with self.assertRaisesRegex(zenodo.DepositError, "Another local command"):
                self.call(confirm_id=123)
            self.assertTrue(self.call()["dry_run"])
        self.assertEqual(self.client.mutations, [])

    def test_related_scheme_exception_rejects_changed_relation_type_or_extra_fields(self):
        self.write_patch({"related_identifiers": [{"identifier": "https://example.org/new", "relation": "isSupplementTo"}]})
        self.call(confirm_id=123)
        staged = copy.deepcopy(self.client.record)
        for changed in ({"scheme": "doi"}, {"scheme": "url", "relation": "isSupplementedBy"},
                        {"scheme": "url", "unexpected": "field"}):
            self.client.record = copy.deepcopy(staged)
            self.client.record["metadata"]["related_identifiers"][0].update(changed)
            with self.assertRaisesRegex(zenodo.DepositError, "metadata differs"):
                self.call("publish-metadata", 123)
        self.assertNotIn("publish", self.client.mutations)

    def test_malformed_native_response_is_controlled_failure_without_mutations(self):
        for native in ({}, {"id": "123", "metadata": []}, {"id": "999", "metadata": {}}):
            with patch.object(self.client, "native_get", return_value=native):
                with self.assertRaisesRegex(zenodo.DepositError, "Cannot verify the native"):
                    self.call(confirm_id=123)
        self.assertEqual(self.client.mutations, [])


if __name__ == "__main__":
    unittest.main()
