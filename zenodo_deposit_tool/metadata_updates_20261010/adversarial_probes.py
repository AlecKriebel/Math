"""Offline behavioral probes derived from the official legacy serializer.

Run from zenodo_deposit_tool: python3 metadata_updates_20261010/adversarial_probes.py
No tokens, HTTP requests, or persistent production state are used.
"""

import copy
import sys
from pathlib import Path
from unittest.mock import patch
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import zenodo
import metadata_updates as updates
from test_metadata_updates import MetadataUpdateTests


class AdversarialSerializerProbes(MetadataUpdateTests):
    # Keep the existing independent test setup, without rerunning inherited tests.
    def test_clear_keywords_when_api_omits_empty_keyword_field(self):
        self.write_patch({"keywords": []})
        update = self.client.update

        def actual_serializer(record_id, metadata):
            update(record_id, metadata)
            if not self.client.record["metadata"].get("keywords"):
                self.client.record["metadata"].pop("keywords", None)

        with patch.object(self.client, "update", side_effect=actual_serializer):
            result = self.call(confirm_id=123)
        self.assertEqual(result["state"], "ready_to_publish_metadata")
        result = self.call("publish-metadata", 123)
        self.assertEqual(result["state"], "published")
        self.assertNotIn("keywords", self.client.record["metadata"])

    def test_clear_notes_when_api_omits_empty_note_field(self):
        self.client.record["metadata"]["notes"] = "Old note"
        self.client.published = copy.deepcopy(self.client.record)
        self.write_patch({"notes": ""})
        update = self.client.update

        def actual_serializer(record_id, metadata):
            update(record_id, metadata)
            if not self.client.record["metadata"].get("notes"):
                self.client.record["metadata"].pop("notes", None)

        with patch.object(self.client, "update", side_effect=actual_serializer):
            result = self.call(confirm_id=123)
        self.assertEqual(result["state"], "ready_to_publish_metadata")
        self.assertEqual(self.call("publish-metadata", 123)["state"], "published")
        self.assertNotIn("notes", self.client.record["metadata"])

    def test_new_related_identifier_has_api_added_scheme(self):
        self.client.record["metadata"]["related_identifiers"][0]["scheme"] = "url"
        self.client.published = copy.deepcopy(self.client.record)
        self.write_patch({"related_identifiers": [
            {"identifier": "https://example.org/new-code", "relation": "isSupplementTo"}
        ]})
        update = self.client.update

        def actual_serializer(record_id, metadata):
            update(record_id, metadata)
            for entry in self.client.record["metadata"].get("related_identifiers", []):
                entry["scheme"] = "url"

        with patch.object(self.client, "update", side_effect=actual_serializer):
            result = self.call(confirm_id=123)
        self.assertEqual(result["state"], "ready_to_publish_metadata")
        self.assertEqual(self.call("publish-metadata", 123)["state"], "published")

    def test_already_published_retry_receipt_failure_keeps_confirmation(self):
        self.call(confirm_id=123)
        self.call("publish-metadata", 123)
        mutations = list(self.client.mutations)
        with patch.object(zenodo, "save_state", side_effect=OSError("disk full")):
            result = self.call("publish-metadata", 123)
        self.assertEqual(result["state"], "published")
        self.assertTrue(result["already_complete"])
        self.assertFalse(result["receipt_saved"])
        self.assertEqual(self.client.mutations, mutations)

    def test_omitted_native_author_details_survive_legacy_round_trip(self):
        """Refuse loss-prone native authors before any edit/PUT mutation."""
        native_author = {
            "person_or_org": {"name": "Example Institute", "type": "organizational"},
            "affiliations": [{"name": "Department A"}, {"name": "Department B"}],
        }
        original_author = copy.deepcopy(native_author)
        self.client.record["metadata"]["creators"] = [
            {"name": "Example Institute", "affiliation": "Department A"}
        ]
        self.client.published = copy.deepcopy(self.client.record)
        self.write_patch({"title": "Improved discovery title"})
        update = self.client.update

        def native_get(record_id, draft=False):
            return {
                "id": str(record_id),
                "pids": {"doi": {"identifier": self.client.record["doi"]}},
                "custom_fields": {},
                "access": {"record": "public", "files": "public"},
                "metadata": {
                    "title": self.client.record["metadata"]["title"],
                    "description": self.client.record["metadata"]["description"],
                    "publication_date": "2026-09-26",
                    "resource_type": {"id": "publication-preprint"},
                    "publisher": "Zenodo",
                    "rights": [{"id": "cc-by-4.0"}],
                    "subjects": [{"subject": "original"}],
                    "creators": [copy.deepcopy(native_author)],
                },
            }

        self.client.native_get = native_get

        def actual_deserializer(record_id, metadata):
            update(record_id, metadata)
            author = metadata["creators"][0]
            # Official PersonSchema type Constant("personal"), load_names, and
            # CreatorSchema.load_affiliations reconstruct just this information.
            native_author.clear()
            native_author.update({
                "person_or_org": {"family_name": author["name"], "type": "personal"},
                "affiliations": [{"name": author["affiliation"]}],
            })

        with patch.object(self.client, "update", side_effect=actual_deserializer):
            with self.assertRaises(zenodo.DepositError):
                self.call(confirm_id=123)
        self.assertEqual(self.client.mutations, [])
        self.assertEqual(native_author, original_author)

    def test_repeated_stage_refuses_native_drift_hidden_by_legacy_keywords(self):
        self.call(confirm_id=123)
        native_get = self.client.native_get

        def richer_subjects(record_id, draft=False):
            result = native_get(record_id, draft=draft)
            result["metadata"]["subjects"].append({
                "id": "https://example.org/controlled-vocabulary/extra",
                "subject": "External addition hidden by legacy keyword serializer",
            })
            return result

        with patch.object(self.client, "native_get", side_effect=richer_subjects):
            with self.assertRaises(zenodo.DepositError):
                self.call(confirm_id=123)

    def test_discard_refuses_native_drift_hidden_by_legacy_keywords(self):
        self.call(confirm_id=123)
        native_get = self.client.native_get

        def richer_subjects(record_id, draft=False):
            result = native_get(record_id, draft=draft)
            if draft:
                result["metadata"]["subjects"].append({
                    "id": "https://example.org/controlled-vocabulary/extra",
                    "subject": "External addition hidden by legacy keyword serializer",
                })
            return result

        with patch.object(self.client, "native_get", side_effect=richer_subjects):
            with self.assertRaises(zenodo.DepositError):
                self.call("discard-metadata", 123)
        self.assertNotIn("discard", self.client.mutations)

    def test_publish_requires_completed_native_staging_after_native_read_failure(self):
        native_get = self.client.native_get

        def failed_native_read(record_id, draft=False):
            if draft:
                raise zenodo.DepositError("Native draft read unavailable")
            return native_get(record_id, draft=draft)

        with patch.object(self.client, "native_get", side_effect=failed_native_read):
            with self.assertRaises(zenodo.DepositError):
                self.call(confirm_id=123)
        session = zenodo.read_json(updates.snapshot_path(123, "production"))
        self.assertNotIn("native_staged", session)

        def richer_subjects(record_id, draft=False):
            result = native_get(record_id, draft=draft)
            result["metadata"]["subjects"].append({
                "id": "https://example.org/controlled-vocabulary/extra",
                "subject": "External addition hidden by legacy keyword serializer",
            })
            return result

        with patch.object(self.client, "native_get", side_effect=richer_subjects):
            with self.assertRaises(zenodo.DepositError):
                self.call("publish-metadata", 123)
        self.assertNotIn("publish", self.client.mutations)


if __name__ == "__main__":
    names = [name for name in AdversarialSerializerProbes.__dict__ if name.startswith("test_")]
    suite = unittest.TestSuite(AdversarialSerializerProbes(name) for name in names)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    raise SystemExit(not result.wasSuccessful())
