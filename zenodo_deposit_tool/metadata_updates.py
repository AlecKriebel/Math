"""Metadata-only edits, with durable before/after snapshots and explicit publication."""

from __future__ import annotations

from datetime import datetime, timezone
from contextlib import contextmanager
import os
import re
from urllib.parse import urlsplit

import zenodo


READ_ONLY_METADATA = {"prereserve_doi", "relations"}
PROTECTED_METADATA = READ_ONLY_METADATA | {"doi"}
FINAL_PHASES = {"published", "discarded"}
# Exact empty-value omissions in Zenodo's legacy metadata serializer.
OMITTED_EMPTY_VALUES = {"keywords": [], "references": [], "locations": [],
                        "notes": "", "method": "", "language": "", "custom": {}}
PATCH_NATIVE_KEYS = {
    "title": "title", "description": "description", "creators": "creators",
    "publication_date": "publication_date", "keywords": "subjects", "version": "version",
    "language": "languages", "related_identifiers": "related_identifiers", "references": "references",
    "upload_type": "resource_type", "publication_type": "resource_type", "image_type": "resource_type",
    "notes": "additional_descriptions", "method": "additional_descriptions",
}
NATIVE_METADATA_KEYS = set(PATCH_NATIVE_KEYS.values()) | {"publisher", "rights"}


def native_snapshot(client, record_id: int, draft: bool = False) -> dict:
    record = client.native_get(record_id, draft=draft)
    if (str(record.get("id")) != str(record_id) or not isinstance(record.get("metadata"), dict)
            or not isinstance(record.get("custom_fields"), dict)
            or not isinstance(record.get("access"), dict) or not isinstance(record.get("pids"), dict)):
        raise zenodo.DepositError("Cannot verify the native record representation; refusing metadata writes")
    return {key: record[key] for key in ("metadata", "custom_fields", "access", "pids")}


def require_legacy_coverage(native: dict) -> None:
    try:
        _require_legacy_coverage(native)
    except (TypeError, AttributeError, ValueError, KeyError) as exc:
        raise zenodo.DepositError("Cannot validate native metadata shapes; no edit was opened") from exc


def _require_legacy_coverage(native: dict) -> None:
    """Fail before edit if a legacy PUT would project away richer native fields."""
    metadata = native["metadata"]
    unsafe = bool(native["custom_fields"] or set(metadata) - NATIVE_METADATA_KEYS)
    for author in metadata.get("creators", []):
        person = author.get("person_or_org", {})
        name = person.get("name", "")
        unsafe |= (set(author) - {"person_or_org", "affiliations"} != set()
                   or set(person) - {"type", "name", "given_name", "family_name", "identifiers"} != set()
                   or person.get("type") != "personal" or not isinstance(name, str))
        if isinstance(name, str):
            family, given = (part.strip() for part in name.split(",")) if name.count(",") == 1 else (name, None)
            unsafe |= person.get("family_name") != family or person.get("given_name") != given
        affiliations = author.get("affiliations", [])
        unsafe |= len(affiliations) > 1 or any(set(item) != {"name"} for item in affiliations)
        unsafe |= any(set(item) != {"scheme", "identifier"} or item.get("scheme") not in {"orcid", "gnd"}
                      for item in person.get("identifiers", []))
    unsafe |= any(set(item) != {"subject"} for item in metadata.get("subjects", []))
    unsafe |= len(metadata.get("languages", [])) > 1 or len(metadata.get("rights", [])) > 1
    unsafe |= any(set(item) != {"reference"} for item in metadata.get("references", []))
    descriptions = metadata.get("additional_descriptions", [])
    kinds = [item.get("type", {}).get("id") for item in descriptions]
    unsafe |= (any(kind not in {"notes", "methods"} for kind in kinds) or len(set(kinds)) != len(kinds)
               or any(set(item) - {"type", "description"} for item in descriptions))
    if unsafe:
        raise zenodo.DepositError(
            "Record has rich native metadata that the legacy API cannot preserve (such as organization authors, "
            "multiple/structured affiliations, controlled subjects, or extra fields). No edit was opened; "
            "use Zenodo's native editor for this record"
        )


def verify_native_preserved(native: dict, session: dict, changed: bool) -> None:
    original = session["native_original"]
    for key in ("custom_fields", "access", "pids"):
        if native[key] != original[key]:
            raise zenodo.DepositError(f"Native {key} changed unexpectedly; do not publish")
    fields = session["patch_fields"] if changed else []
    ignored = {PATCH_NATIVE_KEYS[field] for field in fields}
    before = {key: value for key, value in original["metadata"].items() if key not in ignored}
    after = {key: value for key, value in native["metadata"].items() if key not in ignored}
    if before != after:
        raise zenodo.DepositError("Native metadata not included in the patch changed; do not publish")
    if "additional_descriptions" in ignored:
        replaced = {"notes" if field == "notes" else "methods" for field in fields if field in {"notes", "method"}}
        def retained(metadata):
            return [item for item in metadata.get("additional_descriptions", [])
                    if item.get("type", {}).get("id") not in replaced]
        if retained(original["metadata"]) != retained(native["metadata"]):
            raise zenodo.DepositError("Unpatched native additional descriptions changed; do not publish")


def editable_metadata(deposit: dict) -> dict:
    metadata = deposit.get("metadata")
    if not isinstance(metadata, dict):
        raise zenodo.DepositError("Zenodo returned invalid metadata")
    return {key: value for key, value in metadata.items() if key not in READ_ONLY_METADATA}


def file_snapshot(deposit: dict) -> list[dict]:
    result = []
    for name, entry in sorted(zenodo.server_files(deposit).items()):
        checksum = str(entry.get("checksum", "")).lower().removeprefix("md5:")
        size = entry.get("filesize", entry.get("size"))
        if (not isinstance(name, str) or not re.fullmatch(r"[0-9a-f]{32}", checksum)
                or type(size) is not int or size < 0):
            raise zenodo.DepositError("Cannot snapshot an invalid remote filename/checksum/size")
        result.append({"name": name, "md5": checksum, "size": size})
    return result


def record_doi(deposit: dict):
    return deposit.get("doi") or deposit.get("metadata", {}).get("doi")


def snapshot_path(record_id: int, environment: str):
    return zenodo.STATE_DIR / f"metadata-{record_id}-{environment}.json"


def checkpoint(place, session: dict, phase: str) -> None:
    session.update(phase=phase, updated_utc=datetime.now(timezone.utc).isoformat())
    try:
        zenodo.save_state(place, session)
    except OSError as exc:
        raise zenodo.DepositError(
            f"Cannot save metadata session {place}; no further API mutation was attempted. "
            "Read the record with metadata before retrying"
        ) from exc


def require_published(deposit: dict, record_id: int) -> None:
    zenodo.validate_record(deposit, record_id)
    if not deposit["submitted"] or deposit.get("state") not in {"done", "inprogress"}:
        raise zenodo.DepositError("Metadata edit workflow requires a published record in done/inprogress state")


def unchanged_assets(deposit: dict, session: dict) -> None:
    require_published(deposit, session["id"])
    if record_doi(deposit) != session["doi"]:
        raise zenodo.DepositError("Record DOI changed; inspect the record before any further action")
    if file_snapshot(deposit) != session["files"]:
        raise zenodo.DepositError("Record files changed; inspect the record before any further action")


def verify_metadata(deposit: dict, metadata: dict, session: dict) -> list[dict]:
    unchanged_assets(deposit, session)
    remote = editable_metadata(deposit)
    wanted = dict(metadata)
    normalizations = []
    for field, empty in OMITTED_EMPTY_VALUES.items():
        if field in wanted and wanted[field] == empty and field not in remote:
            del wanted[field]
            normalizations.append({"field": field, "kind": "empty_optional_field_omitted"})
    links = wanted.get("related_identifiers")
    actual_links = remote.get("related_identifiers")
    if isinstance(links, list) and isinstance(actual_links, list) and len(links) == len(actual_links):
        normalized = []
        added_scheme = False
        for expected, actual in zip(links, actual_links):
            if isinstance(expected, dict) and isinstance(actual, dict) and "scheme" not in expected:
                identifier = expected.get("identifier")
                inferred = None
                if isinstance(identifier, str):
                    if re.fullmatch(r"10\.\d{4,9}/\S+", identifier):
                        inferred = "doi"
                    else:
                        try:
                            url = urlsplit(identifier)
                            if url.scheme in {"http", "https"} and url.hostname:
                                inferred = "url"
                        except ValueError:
                            pass
                if inferred and actual == {**expected, "scheme": inferred}:
                    normalized.append(expected)
                    added_scheme = True
                    continue
            normalized.append(actual)
        if added_scheme:
            remote["related_identifiers"] = normalized
            normalizations.append({"field": "related_identifiers", "kind": "inferred_doi_or_url_scheme"})
    if set(remote) != set(wanted):
        raise zenodo.DepositError("Remote metadata fields drifted from the saved edit")
    return normalizations + zenodo.verify({**deposit, "metadata": remote}, wanted, session["files"])


def matches(deposit: dict, metadata: dict, session: dict) -> bool:
    try:
        verify_metadata(deposit, metadata, session)
    except zenodo.DepositError:
        return False
    return True


def mutate_and_read(client, record_id: int, operation, expected_state: str, verify_result):
    """One mutation only; a lost response can be resolved by one authenticated read."""
    error = None
    try:
        operation()
    except zenodo.DepositError as exc:
        error = exc
    try:
        deposit = client.get(record_id)
        require_published(deposit, record_id)
        if deposit["state"] != expected_state:
            raise zenodo.DepositError(f"Expected {expected_state}, found {deposit['state']}")
        verify_result(deposit)
    except zenodo.DepositError as exc:
        detail = f"{error}; " if error else ""
        raise zenodo.DepositError(
            f"{detail}Metadata operation outcome is unconfirmed or verification failed: {exc}. "
            f"Run metadata {record_id} and reconcile the saved session; no automatic mutation retry was made"
        ) from exc
    return deposit, error is not None


def summary(deposit: dict, environment: str) -> dict:
    metadata = editable_metadata(deposit)
    return {"environment": environment, "id": deposit["id"], "state": deposit.get("state"),
            "submitted": deposit["submitted"], "doi": record_doi(deposit),
            "record_url": zenodo.BASES[environment] + f"/records/{deposit['id']}",
            "metadata": metadata, "files": file_snapshot(deposit)}


def complete(place, session: dict, phase: str, result: dict) -> dict:
    result.update(state=phase, session_file=str(place), receipt_saved=True,
                  verified_utc=datetime.now(timezone.utc).isoformat())
    session["receipt"] = {key: result[key] for key in ("state", "verified_utc")}
    # Persistence failure cannot negate a verified remote result, including retries.
    try:
        checkpoint(place, session, phase)
    except zenodo.DepositError:
        result.update(receipt_saved=False, receipt_warning="Remote action is confirmed, but the local receipt could not be saved")
    return result


@contextmanager
def record_lock(record_id: int, environment: str):
    """A local process lock releases automatically on exit, including crashes."""
    try:
        import fcntl
    except ImportError as exc:
        raise zenodo.DepositError("Metadata writes require file locking on macOS/Linux") from exc
    place = snapshot_path(record_id, environment).with_suffix(".lock")
    try:
        place.parent.mkdir(mode=0o700, exist_ok=True)
        fd = os.open(place, os.O_CREAT | os.O_RDWR, 0o600)
    except OSError as exc:
        raise zenodo.DepositError("Cannot open the local metadata lock; no API writes attempted") from exc
    with os.fdopen(fd, "a+b") as stream:
        try:
            fcntl.flock(stream.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
        except OSError as exc:
            raise zenodo.DepositError("Another local command is editing this record; no API writes attempted") from exc
        try:
            yield
        finally:
            fcntl.flock(stream.fileno(), fcntl.LOCK_UN)


def run_metadata(args, client=None) -> dict:
    record_id = args.record_id
    if type(record_id) is not int or record_id <= 0:
        raise zenodo.DepositError("record_id must be a positive integer for a specific record version")
    environment = "sandbox" if args.sandbox else "production"
    confirm_id = getattr(args, "confirm_id", None)
    if confirm_id is not None and getattr(args, "dry_run", False):
        raise zenodo.DepositError("Choose dry-run or confirm-id, not both")
    if confirm_id is not None and (type(confirm_id) is not int or confirm_id != record_id):
        raise zenodo.DepositError(f"This action requires --confirm-id {record_id}")
    if args.command in {"publish-metadata", "discard-metadata"} and confirm_id is None:
        raise zenodo.DepositError(f"This action requires --confirm-id {record_id}")
    if confirm_id is not None:
        with record_lock(record_id, environment):
            return _run_metadata(args, client, environment, confirm_id)
    return _run_metadata(args, client, environment, confirm_id)


def _run_metadata(args, client, environment: str, confirm_id: int | None) -> dict:
    record_id = args.record_id
    patch = None
    if args.command == "update-metadata":
        document = zenodo.read_json(args.patch.resolve())
        patch = document.get("metadata")
        if set(document) != {"metadata"} or not isinstance(patch, dict) or not patch:
            raise zenodo.DepositError("Patch must contain exactly one nonempty 'metadata' object")
        if PROTECTED_METADATA & patch.keys():
            raise zenodo.DepositError("Cannot patch doi, prereserve_doi or relations; the record DOI is preserved")
        if set(patch) - PATCH_NATIVE_KEYS.keys():
            raise zenodo.DepositError("Supported patch fields: " + ", ".join(sorted(PATCH_NATIVE_KEYS)))
        if any(value is None for value in patch.values()):
            raise zenodo.DepositError("Null is not a deletion instruction; use [] or an empty string to clear optional fields")
    if client is None:
        client = zenodo.ZenodoClient(environment, zenodo.token_for(environment))
    deposit = client.get(record_id)
    zenodo.validate_record(deposit, record_id)
    result = summary(deposit, environment)
    if args.command == "metadata":
        return result
    require_published(deposit, record_id)
    place = snapshot_path(record_id, environment)
    session = zenodo.read_json(place) if place.exists() else None
    if session is not None and (type(session.get("id")) is not int or session.get("id") != record_id
                    or session.get("environment") != environment
                    or session.get("phase") not in {"prepared", "edit_requested", "update_requested", "staged",
                                                     "publish_requested", "discard_requested", *FINAL_PHASES}
                    or "doi" not in session
                    or not isinstance(session.get("native_original"), dict)
                    or not isinstance(session.get("patch_fields"), list)
                    or not isinstance(session.get("original_metadata"), dict)
                    or not isinstance(session.get("target_metadata"), dict)
                    or not isinstance(session.get("files"), list)):
        raise zenodo.DepositError(f"Invalid local metadata session: {place}")
    if args.command == "update-metadata":
        active = session is not None and session.get("phase") not in FINAL_PHASES
        original = session["original_metadata"] if active else editable_metadata(deposit)
        target = {**original, **patch}  # Field-level replacement, including entire lists.
        changes = [{"field": key, "before": original.get(key), "after": value}
                   for key, value in target.items() if key not in original or original[key] != value]
        result.update(changes=changes, metadata=target, dry_run=confirm_id is None)
        native = native_snapshot(client, record_id, draft=deposit["state"] == "inprogress")
        if not active:
            require_legacy_coverage(native)
        if confirm_id is None:
            result["native_metadata_preservation_checked"] = True
            return result
        if active and target != session["target_metadata"]:
            raise zenodo.DepositError("A different metadata edit is pending; publish or discard it before staging another patch")
        if active:
            staged_native = session.get("native_staged")
            if staged_native is not None and native not in (session["native_original"], staged_native):
                raise zenodo.DepositError("Native metadata drifted from the saved session; refusing to restage")
            if staged_native is None:
                require_legacy_coverage(native)
                verify_native_preserved(native, session, changed=True)
        if not active:
            if deposit["state"] != "done":
                raise zenodo.DepositError("Record already has an editing session; reconcile it in Zenodo before staging")
            if not changes:
                result["state"] = "unchanged"
                return result
            session = {"id": record_id, "environment": environment, "original_metadata": original,
                       "target_metadata": target, "files": file_snapshot(deposit), "doi": record_doi(deposit),
                       "native_original": native, "patch_fields": list(patch)}
            checkpoint(place, session, "prepared")
        unchanged_assets(deposit, session)
        if deposit["state"] == "done" and matches(deposit, target, session):
            verify_native_preserved(native, session, changed=True)
            result.update(already_published=True, metadata_normalizations=verify_metadata(deposit, target, session))
            return complete(place, session, "published", result)
        if not (matches(deposit, original, session) or matches(deposit, target, session)):
            raise zenodo.DepositError("Remote metadata drifted from the saved edit; reconcile before staging")
        if deposit["state"] == "done":
            checkpoint(place, session, "edit_requested")
            deposit, recovered = mutate_and_read(
                client, record_id, lambda: client.edit(record_id), "inprogress",
                lambda remote: verify_metadata(remote, original, session))
            result["recovered_after_edit_error"] = recovered
        if not matches(deposit, target, session):
            checkpoint(place, session, "update_requested")
            deposit, recovered = mutate_and_read(
                client, record_id, lambda: client.update(record_id, target), "inprogress",
                lambda remote: verify_metadata(remote, target, session))
            result["recovered_after_update_error"] = recovered
        result["metadata_normalizations"] = verify_metadata(deposit, target, session)
        native = native_snapshot(client, record_id, draft=True)
        session["native_staged"] = native
        checkpoint(place, session, "update_requested")
        verify_native_preserved(native, session, changed=True)
        checkpoint(place, session, "staged")
        result.update(state="ready_to_publish_metadata", session_file=str(place),
                      publication_required=True)
        return result
    if session is None:
        raise zenodo.DepositError("No saved metadata edit for this record/environment; stage one first")
    unchanged_assets(deposit, session)
    publishing = args.command == "publish-metadata"
    expected = session["target_metadata"] if publishing else session["original_metadata"]
    phase = "published" if publishing else "discarded"
    native = native_snapshot(client, record_id, draft=deposit["state"] == "inprogress")
    if deposit["state"] == "done":
        result["metadata_normalizations"] = verify_metadata(deposit, expected, session)
        verify_native_preserved(native, session, changed=publishing)
        if publishing and session.get("native_staged") is not None and native != session["native_staged"]:
            raise zenodo.DepositError("Published native metadata differs from the staged snapshot; inspect the record")
        result["already_complete"] = True
        return complete(place, session, phase, result)
    if session.get("phase") in FINAL_PHASES:
        raise zenodo.DepositError("Saved metadata edit is complete; refusing to alter a newer editing session")
    if publishing:
        if not isinstance(session.get("native_staged"), dict):
            raise zenodo.DepositError("Native staging was not completed; resume update-metadata with the same patch before publishing")
        verify_metadata(deposit, expected, session)
        verify_native_preserved(native, session, changed=True)
        if session.get("native_staged") is not None and native != session["native_staged"]:
            raise zenodo.DepositError("Native metadata drifted from the staged snapshot; do not publish")
    elif not (matches(deposit, session["original_metadata"], session)
              or matches(deposit, session["target_metadata"], session)):
        raise zenodo.DepositError("Remote metadata drifted; refusing to discard another editing session's changes")
    if not publishing and native not in (session["native_original"], session.get("native_staged")):
        if session.get("native_staged") is not None:
            raise zenodo.DepositError("Native metadata drifted from the saved session; refusing to discard")
        require_legacy_coverage(native)
        verify_native_preserved(native, session, changed=True)
    checkpoint(place, session, "publish_requested" if publishing else "discard_requested")
    operation = (lambda: client.publish(record_id)) if publishing else (lambda: client.discard(record_id))
    deposit, recovered = mutate_and_read(
        client, record_id, operation, "done", lambda remote: verify_metadata(remote, expected, session))
    result = summary(deposit, environment)
    try:
        native = native_snapshot(client, record_id)
        verify_native_preserved(native, session, changed=publishing)
        if publishing and session.get("native_staged") is not None and native != session["native_staged"]:
            raise zenodo.DepositError("Native metadata differs from the staged snapshot")
    except zenodo.DepositError as exc:
        raise zenodo.DepositError(f"Zenodo reports the {phase} action completed, but native verification failed: {exc}. "
                                 "Inspect the record; no automatic action retry was made") from exc
    result.update(metadata_normalizations=verify_metadata(deposit, expected, session),
                  recovered_after_action_error=recovered)
    return complete(place, session, phase, result)
