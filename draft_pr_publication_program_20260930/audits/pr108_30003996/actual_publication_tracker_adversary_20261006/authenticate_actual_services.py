#!/usr/bin/env python3
"""Independent, GET-only authentication of PR108 publication and target row.

Every write is confined to this script's folder. No original validator is
executed; ZIP members are checked in memory against the exact local manifest.
"""
import datetime as dt
import hashlib
import io
import json
import os
from pathlib import Path, PurePosixPath
import stat
import subprocess
import sys
from urllib.request import Request, urlopen
import zipfile

P = Path(__file__).resolve().parent
A = P.parent
C = A.parents[2]
D = A / "publication_ready_package_v2"
ID = 23181280
DOI = "10.5281/zenodo.23181280"
SID = "1ZljUv5Q98jNXLoHK8WjwrkzSm3dhHC1-7LElcOU7y20"
GID = 1254632077
RANGE = "'Math Puzzles'!A31:D31"
GWS = "/Users/alec/.nvm/versions/node/v22.16.0/bin/gws"
EXPECTED = {
    "PACKAGE_MANIFEST.json": "61f08bd60185b6ef2382fb279fe77d59958974c07c4a44976cc7289eafca8c38",
    "root_dependent_spanning_trees.pdf": "f51acb267822dd082fdb28a14bc581b37fc3b3a75008647a3e04fa8a3d84fbf4",
    "root_dependent_spanning_trees_support.zip": "66f7d7e25370062e0f70b7fdce538dc90a5a264957557714f11d1ac42ebc14aa",
}
CHECKS = []


def now():
    return dt.datetime.now(dt.timezone.utc).isoformat()


def sha(b):
    return hashlib.sha256(b).hexdigest()


def require(ok, label):
    CHECKS.append({"check": label, "passed": bool(ok)})
    if not ok:
        raise RuntimeError(label)


def write(name, obj):
    q = P / name
    require(q.parent == P and not q.exists(), "New audit output confined to own folder: " + name)
    q.write_text(json.dumps(obj, indent=2, ensure_ascii=False, allow_nan=False) + "\n")


def load(path):
    return json.loads(path.read_bytes())


def pin(path):
    b = path.read_bytes()
    return {"path": str(path.relative_to(C)), "bytes": len(b), "sha256": sha(b)}


def check_pin(p):
    path = C / p["path"]
    require(path.resolve().is_relative_to(A.resolve()), "Input pin remains in PR108 audit")
    require(pin(path) == p, "Pinned input bytes/hash: " + p["path"])
    return path


def timestamp(s):
    parsed = dt.datetime.fromisoformat(s)
    require(parsed.tzinfo is not None and parsed.utcoffset() == dt.timedelta(0), "Explicit UTC timestamp")
    require(parsed <= dt.datetime.now(dt.timezone.utc), "Actual timestamp not in the future")
    return parsed


def authenticate_process(name):
    folder = A / "actual_operations" / name
    start = load(folder / "started.json")
    e = load(folder / "execution.json")
    require(e["cwd"] == str(A) and start["cwd"] == str(A), name + ": exact cwd")
    for key in ["UTC_start", "recorder_PID", "argv"]:
        require(start[key] == e[key], name + ": started/execution consistency " + key)
    require(isinstance(e["child_PID"], int) and e["child_PID"] > 0 and e["child_PID"] != e["recorder_PID"], name + ": recorded actual child PID")
    require(e["exit_code"] == 0, name + ": successful process exit")
    require(timestamp(e["UTC_start"]) < timestamp(e["UTC_end"]), name + ": ordered UTC interval")
    for stream in ["stdout", "stderr"]:
        require(e[stream]["path"] == stream + ".bin", name + ": exact stream filename")
        b = (folder / e[stream]["path"]).read_bytes()
        require(len(b) == e[stream]["bytes"] and sha(b) == e[stream]["sha256"], name + ": authentic " + stream + " bytes/hash")
    result = {"name": name, "child_PID": e["child_PID"], "recorder_PID": e["recorder_PID"],
              "UTC_start": e["UTC_start"], "UTC_end": e["UTC_end"], "exit_code": e["exit_code"],
              "started_pin": pin(folder / "started.json"), "execution_pin": pin(folder / "execution.json"),
              "stdout_pin": pin(folder / "stdout.bin"), "stderr_pin": pin(folder / "stderr.bin")}
    return e, load(folder / "stdout.bin"), result


def authenticate_http_body(body_path, receipt_path, process):
    body = body_path.read_bytes()
    r = load(receipt_path)
    require(r["actual_receipt"] is True and r["PID"] == process["child_PID"] and r["exit_code"] == 0, "Historical GET actual process custody")
    require(r["HTTP_method"] == "GET" and r["status_code"] == 200, "Historical public GET status")
    require(r["URL"].startswith("https://zenodo.org/api/records/23181280") and r["resolved_URL"] == r["URL"], "Historical public endpoint")
    require(timestamp(process["UTC_start"]) <= timestamp(r["UTC_start"]) < timestamp(r["UTC_end"]) <= timestamp(process["UTC_end"]), "Historical GET bounded by child process interval")
    require(r["response_bytes"] == len(body) and r["response_sha256"] == sha(body), "Historical GET response bytes/hash")
    return {"body_pin": pin(body_path), "GET_receipt_pin": pin(receipt_path), "PID": r["PID"],
            "UTC_start": r["UTC_start"], "UTC_end": r["UTC_end"], "status_code": r["status_code"]}


def get(url, filename):
    require(not (P / filename).exists(), "Fresh public download target")
    start = now()
    request = Request(url, method="GET", headers={"User-Agent": "PR108-Independent-Actual-Service-Audit/1.0", "Accept": "*/*"})
    require(not request.has_header("Authorization") and not request.has_header("Cookie"), "Credential-free GET request")
    with urlopen(request, timeout=30) as response:
        body = response.read(2 * 1024 * 1024 + 1)
        require(response.status == 200 and len(body) <= 2 * 1024 * 1024, "Fresh public GET status/body cap")
        require(response.url == url, "Fresh exact public URL")
        receipt = {"actual_receipt": True, "HTTP_method": "GET", "URL": url, "resolved_URL": response.url,
                   "status_code": response.status, "PID": os.getpid(), "UTC_start": start,
                   "request_headers": dict(request.header_items()), "Authorization_header": False, "Cookie_header": False,
                   "response_Content_Type": response.headers.get("Content-Type")}
    (P / filename).write_bytes(body)
    receipt.update({"UTC_end": now(), "response_bytes": len(body), "response_sha256": sha(body),
                    "response_md5": hashlib.md5(body).hexdigest(), "successful_request_completed": True})
    write(filename + ".HTTP_GET.json", receipt)
    return body, {"body_pin": pin(P / filename), "GET_receipt_pin": pin(P / (filename + ".HTTP_GET.json"))}


def exact_metadata(record, expected):
    require(record["id"] == ID and record["doi"] == DOI and record["submitted"] is True, "Exact published public record identity")
    actual = record["metadata"]
    comparisons = []
    for k, v in expected.items():
        if k == "upload_type":
            av = actual["resource_type"]["type"]
        elif k == "publication_type":
            av = actual["resource_type"]["subtype"]
        elif k == "license":
            av = actual["license"]["id"]
        else:
            av = actual.get(k)
        require(av == v, "Exact intended public metadata: " + k)
        comparisons.append({"field": k, "exact": True})
    return comparisons


def main():
    start = now()
    gate = load(A / "ROOT_READY_FOR_PUBLICATION_20261006.json")
    root = load(A / "ROOT_ACTUAL_PUBLICATION_RECEIPT_20261006.json")
    sr = load(A / "ROOT_ACTUAL_GOOGLE_SHEET_SERVICE_RECEIPT_20261006.json")
    intended = load(A / "TRACKER_ROW_INTENDED_20261006.json")
    manifest_bytes = (D / "PACKAGE_MANIFEST.json").read_bytes()
    manifest = json.loads(manifest_bytes)
    deposit = load(D / "zenodo-deposit.json")
    require(gate["publication_ready"] is True and gate["findings_remaining"] == [], "Prior root publication gate issued without findings")
    require(gate["native_execution_or_merge_clearance"] is False, "Prior gate does not clear native execution or merge")
    for n, h in EXPECTED.items():
        require(sha((D / n).read_bytes()) == h, "Independent task source binding: " + n)
    require(gate["package_manifest_sha256"] == EXPECTED["PACKAGE_MANIFEST.json"] and gate["PDF_sha256"] == EXPECTED["root_dependent_spanning_trees.pdf"] and gate["archive_sha256"] == EXPECTED["root_dependent_spanning_trees_support.zip"], "Gate matches exact audited source pins")
    require(len(manifest["files"]) == 46 and len({x["relative_path"] for x in manifest["files"]}) == 46, "46 distinct logical payloads")
    require(root["actual_receipt"] is True and root["published"] is True and root["DOI"] == DOI and root["logical_payload_count"] == 46 and root["archive_member_count"] == 47, "Root receipt exact publication scope")
    require(root["package_manifest_sha256"] == EXPECTED["PACKAGE_MANIFEST.json"] and root["metadata_exact_after_documented_public_schema_mapping"] is True and root["kit_metadata_normalizations"] == [], "Root metadata/source attestations")

    processes = []
    ze = {}
    previous_end = timestamp(gate["UTC"])
    for suffix, command in [("stage", "stage"), ("pre_publish_inspect", "inspect"), ("publish", "publish"), ("post_publish_inspect", "inspect"), ("public_download_readback", None)]:
        n = "zenodo_publication_v2_" + suffix
        e, body, summary = authenticate_process(n)
        processes.append(summary)
        ze[suffix] = e
        require(timestamp(e["UTC_start"]) > previous_end, n + ": occurs after preceding publication operation")
        previous_end = timestamp(e["UTC_end"])
        if command:
            require(e["argv"][0:4] == ["/opt/homebrew/bin/python3", "-E", "-B", "/Users/alec/Documents/Math/zenodo_deposit_tool/zenodo.py"], n + ": real root Zenodo CLI")
            require(e["argv"][4:6] == [command, "publication_ready_package_v2/zenodo-deposit.json"], n + ": exact manifest and operation")
            require(body["environment"] == "production" and body["id"] == ID and body["metadata_normalizations"] == [], n + ": production record without metadata normalization")
            require(body["files"] == [{"name": x["path"], "size": (D / x["path"]).stat().st_size, "sha256": EXPECTED[x["path"]]} for x in deposit["files"]], n + ": exact two uploaded files")
            require(body["state"] == ("ready_to_publish" if suffix in ["stage", "pre_publish_inspect"] else "published"), n + ": correct service lifecycle state")
            if suffix in ["publish", "post_publish_inspect"]:
                require(body["doi"] == DOI and body["record_url"] == "https://zenodo.org/records/23181280", n + ": exact public DOI")
                require(body["doi_resolution"] == {"status": "resolved", "http_status": 200, "url": "https://doi.org/" + DOI, "resolved_url": "https://zenodo.org/records/23181280"}, n + ": completed DOI resolution")
                require(timestamp(e["UTC_start"]) <= timestamp(body["verified_utc"]) <= timestamp(e["UTC_end"]), n + ": service verification within process")
            if suffix == "publish":
                require(e["argv"][6:] == ["--confirm-id", str(ID)], "Exact confirmed publication id")
        else:
            require(e["argv"] == ["/opt/homebrew/bin/python3", "-E", "-B", "verify_actual_zenodo_publication.py"], "Historical credential-free readback exact script")
            require(body == {"published": True, "DOI": DOI, "logical_payloads_verified": 46, "both_uploaded_files_byte_identical": True, "public_metadata_exact": True}, "Historical completed public readback stdout")
    require(check_pin(root["actual_publish_command"]) == A / "actual_operations/zenodo_publication_v2_publish/execution.json", "Root receipt bound to actual publication process")
    root_bodies = []
    old_out = A / "published_download_verification_20261006"
    for filename in ["record.json", *[x["path"] for x in deposit["files"]]]:
        root_bodies.append(authenticate_http_body(old_out / filename, old_out / (filename + ".HTTP_GET.json"), ze["public_download_readback"]))
    require(root["PID"] == ze["public_download_readback"]["child_PID"] and root["UTC_start"] == load(old_out / "record.json.HTTP_GET.json")["UTC_start"], "Root record GET actual PID and UTC")
    for p in [root["metadata_response"], root["metadata_HTTP_GET_receipt"], *[v for x in root["individual_upload_downloads"] for v in [x["body"], x["HTTP_GET_receipt"]]]]:
        check_pin(p)
    require(len(root["payload_readbacks"]) == 46 and {x["relative_path"] for x in root["payload_readbacks"]} == {x["relative_path"] for x in manifest["files"]}, "Root logical payload receipt exact inventory")
    expected_members = {x["relative_path"]: x for x in manifest["files"]}
    for x in root["payload_readbacks"]:
        require(x["transport"] == "zip_member" and x["member_path"] == x["relative_path"], "Root zip transport exact member")
        q = check_pin(x["downloaded_file"])
        ent = expected_members[x["relative_path"]]
        require(q == old_out / "extracted" / ent["relative_path"] and q.read_bytes() == (D / ent["relative_path"]).read_bytes(), "Root extracted payload matches reviewed source")
        require(check_pin(x["archive_file"]) == old_out / "root_dependent_spanning_trees_support.zip" and check_pin(x["HTTP_GET_receipt"]) == old_out / "root_dependent_spanning_trees_support.zip.HTTP_GET.json", "Root member custody bound to actual downloaded archive")
    exact_metadata(load(old_out / "record.json"), deposit["metadata"])

    row = intended["values"]
    require(intended["spreadsheet_id"] == SID and intended["sheet_id"] == GID and intended["sheet_title"] == "Math Puzzles" and intended["DOI"] == DOI, "Exact intended tracker identity")
    require(len(row) == 4 and all(isinstance(v, str) for v in row), "Exactly four intended string cells")
    require(row[0] == "https://doi.org/10.4171/owr/2018/50" and row[1] == "" and row[2] == "https://doi.org/" + DOI, "Authentic source URL, authorized blank chat, actual DOI")
    for phrase in ["30003996 / OWR-16633-013", "Original author effort 2/5 (structured ledger absent)", "new central proof-search turns 0", "Extensive AI use; unrefereed", "no absolute-first or continued-open-status certification"]:
        require(phrase in row[3], "Precise intended note: " + phrase)
    require(sr["actual_receipt"] is True and sr["range"] == RANGE and sr["row_index"] == 31 and sr["values"] == row and sr["chat_url_not_supplied_blank_preserved"] is True, "Root service receipt exact row")
    require(sr["spreadsheet_id"] == SID and sr["sheet_id"] == GID and sr["sheet_title"] == "Math Puzzles" and sr["columns"] == ["Original Problem", "Solution Chat URL", "DOI", "Notes"], "Root service receipt exact sheet and columns")
    check_pin(sr["publication_receipt"])
    require(set(sr["processes"]) == {"metadata", "headers", "write", "readback", "independent_readback"}, "Exactly five real tracker process pins")
    for role, suffix in [("metadata", "metadata"), ("headers", "headers"), ("write", "append"), ("readback", "readback"), ("independent_readback", "independent_readback")]:
        name = "tracker_postpub_" + suffix
        e, body, summary = authenticate_process(name)
        processes.append(summary)
        rp = sr["processes"][role]
        require(rp["actual_process_record"] is True and rp["PID"] == e["child_PID"] and rp["exit_code"] == e["exit_code"] and rp["argv"] == e["argv"] and rp["UTC_start"] == e["UTC_start"] and rp["UTC_end"] == e["UTC_end"], role + ": root receipt exact process")
        require(e["argv"][0] == GWS and e["argv"][1:3] == ["sheets", "spreadsheets"], role + ": actual GWS Sheets CLI")
        params_string = e["argv"][e["argv"].index("--params") + 1]
        require(rp["params_bytes"] == len(params_string.encode()) and rp["params_sha256"] == sha(params_string.encode()), role + ": exact parameter byte pin")
        params = json.loads(params_string)
        require(params["spreadsheetId"] == SID, role + ": exact service target")
        require(timestamp(e["UTC_start"]) > previous_end, role + ": postpublication sequential operation")
        previous_end = timestamp(e["UTC_end"])
        for k in ["stdout_pin", "stderr_pin", "response_body_pin", "raw_execution_record"]:
            check_pin(rp[k])
        require(rp["stdout_pin"] == rp["response_body_pin"], role + ": actual response body is stdout")
        if role == "metadata":
            require(e["argv"][3] == "get" and body["spreadsheetId"] == SID, "Metadata service identity")
            target = [x["properties"] for x in body["sheets"] if x["properties"]["sheetId"] == GID]
            require(len(target) == 1 and target[0]["title"] == "Math Puzzles", "Exact target gid/title from private metadata response")
        elif role == "headers":
            require(e["argv"][3:5] == ["values", "get"] and params["range"] == "'Math Puzzles'!A1:D1", "Header exact GET operation")
            require(body == {"majorDimension": "ROWS", "range": "'Math Puzzles'!A1:D1", "values": [sr["columns"]]}, "Authentic four-column schema")
        elif role == "write":
            require(e["argv"][3:5] == ["values", "append"], "Historical actual append")
            require(params == {"spreadsheetId": SID, "range": "'Math Puzzles'!A:D", "valueInputOption": "RAW", "insertDataOption": "INSERT_ROWS", "includeValuesInResponse": True}, "Exact historical append parameters")
            request = json.loads(e["argv"][e["argv"].index("--json") + 1])
            request_path = check_pin(rp["request_body_pin"])
            require(request == load(request_path) == {"majorDimension": "ROWS", "values": [row]}, "Historical append request all four exact values")
            u = body["updates"]
            require(body["spreadsheetId"] == SID and u["spreadsheetId"] == SID and u["updatedRange"] == RANGE and u["updatedRows"] == 1 and u["updatedColumns"] == 4 and u["updatedCells"] == 4, "Actual one-row four-cell append acknowledgment")
            require(u["updatedData"] == {"majorDimension": "ROWS", "range": RANGE, "values": [row]}, "Actual append returned exact target data")
        else:
            require(e["argv"][3:5] == ["values", "get"] and params == {"spreadsheetId": SID, "range": RANGE}, "Historical exact row GET")
            require(body == {"majorDimension": "ROWS", "range": RANGE, "values": [row]}, "Historical all-four-string row readback")
    require(len({x["child_PID"] for x in processes}) == len(processes), "Historical ten distinct child processes")
    require(timestamp(root["verification_completed_UTC"]) < timestamp(sr["processes"]["write"]["UTC_start"]), "Actual public download verification completed before tracker append")
    check_pin(sr["DOI_dedup_actual_execution"])

    record_bytes, record_custody = get("https://zenodo.org/api/records/23181280", "fresh_record.json")
    record = json.loads(record_bytes)
    comparisons = exact_metadata(record, deposit["metadata"])
    remote = {x["key"]: x for x in record["files"]}
    require(len(record["files"]) == 2 and set(remote) == {x["path"] for x in deposit["files"]}, "Fresh exact two-file remote inventory")
    downloads = []
    downloaded = {}
    for f in deposit["files"]:
        n = f["path"]
        body, custody = get("https://zenodo.org/api/records/23181280/files/" + n + "/content", "fresh_" + n)
        source = (D / n).read_bytes()
        md5 = hashlib.md5(body).hexdigest()
        require(len(body) == len(source) == remote[n]["size"] and sha(body) == EXPECTED[n] and md5 == hashlib.md5(source).hexdigest(), "Fresh download exact size/SHA256/MD5: " + n)
        require(remote[n]["checksum"] == "md5:" + md5 and body == source, "Fresh downloaded file matches remote checksum and original bytes: " + n)
        downloaded[n] = body
        downloads.append({"file": n, "bytes": len(body), "sha256": sha(body), "md5": md5, "byte_identical_to_source": True, **custody})
    members = []
    with zipfile.ZipFile(io.BytesIO(downloaded["root_dependent_spanning_trees_support.zip"])) as z:
        infos = z.infolist()
        require(len(infos) == 47 and len({x.filename for x in infos}) == 47 and {x.filename for x in infos} == set(expected_members) | {"PACKAGE_MANIFEST.json"}, "Fresh ZIP exactly 47 unique members")
        require(z.read("PACKAGE_MANIFEST.json") == manifest_bytes, "Fresh ZIP exact manifest bytes")
        for info in infos:
            path = PurePosixPath(info.filename)
            require(not path.is_absolute() and ".." not in path.parts and not info.is_dir() and not stat.S_ISLNK(info.external_attr >> 16) and not info.flag_bits & 1, "Fresh member safe path/mode: " + info.filename)
            b = z.read(info)
            if info.filename == "PACKAGE_MANIFEST.json":
                require(sha(b) == EXPECTED[info.filename], "Fresh manifest exact hash")
            else:
                ent = expected_members[info.filename]
                require(len(b) == info.file_size == ent["bytes"] and sha(b) == ent["sha256"] and b == (D / info.filename).read_bytes(), "Fresh full logical payload authenticated: " + info.filename)
                members.append({"relative_path": info.filename, "bytes": len(b), "sha256": sha(b), "exact_source_bytes": True})
    require(len(members) == 46, "Fresh all 46 logical payloads authenticated without extraction")

    params = json.dumps({"spreadsheetId": SID, "range": RANGE}, separators=(",", ":"))
    argv = [GWS, "sheets", "spreadsheets", "values", "get", "--params", params]
    cli_start = now()
    child = subprocess.Popen(argv, cwd=P, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    started = {"actual_process_record": True, "recorder_PID": os.getpid(), "child_PID": child.pid, "argv": argv,
               "cwd": str(P), "UTC_start": cli_start, "HTTP_method": "GET", "range": RANGE}
    write("fresh_gws_started.json", started)
    stdout, stderr = child.communicate(timeout=45)
    cli_end = now()
    (P / "fresh_gws_stdout.bin").write_bytes(stdout)
    (P / "fresh_gws_stderr.bin").write_bytes(stderr)
    cli_receipt = {**started, "UTC_end": cli_end, "exit_code": child.returncode,
                   "stdout_pin": pin(P / "fresh_gws_stdout.bin"), "stderr_pin": pin(P / "fresh_gws_stderr.bin"),
                   "params_bytes": len(params.encode()), "params_sha256": sha(params.encode()), "target_only_read": True}
    write("fresh_gws_execution.json", cli_receipt)
    require(child.returncode == 0, "Fresh GWS target-row actual child exit zero")
    fresh_row = json.loads(stdout)
    require(fresh_row == {"majorDimension": "ROWS", "range": RANGE, "values": [row]}, "Fresh exact target row all four strings")
    require(timestamp(cli_start) > timestamp(sr["UTC"]), "Fresh independent service GET after root receipt")

    inputs = ["ROOT_READY_FOR_PUBLICATION_20261006.json", "ROOT_ACTUAL_PUBLICATION_RECEIPT_20261006.json", "ROOT_ACTUAL_GOOGLE_SHEET_SERVICE_RECEIPT_20261006.json", "TRACKER_ROW_INTENDED_20261006.json", "verify_actual_zenodo_publication.py", "publication_ready_package_v2/PACKAGE_MANIFEST.json", "publication_ready_package_v2/zenodo-deposit.json", "operational_cli_reference_relocation_20261006/private_generated/skills/gws-shared/SKILL.md"]
    result = {"schema": "pr108-independent-actual-publication-tracker-authentication/v1", "UTC_start": start, "UTC_end": now(),
              "actual_auditor_PID": os.getpid(), "PR": 108, "problem_id": 30003996, "DOI": DOI,
              "audit_scope": "Actual completed Zenodo publication and exact Google Sheet target row; no math/priority re-review, native helper/configuration/execution or merge clearance, or future process/service inference.",
              "scope_complete": True, "required_findings": [], "optional_findings": [],
              "independent_live_Zenodo_readback_authenticated": True, "independent_live_GWS_target_row_authenticated": True,
              "public_schema_mapping": {"resource_type.type": "upload_type", "resource_type.subtype": "publication_type", "license.id": "license"},
              "all_other_metadata_values_exact": True, "metadata_comparisons": comparisons,
              "package_manifest_sha256": EXPECTED["PACKAGE_MANIFEST.json"], "logical_payload_count": 46, "archive_member_count": 47,
              "prior_process_custody": processes, "prior_HTTP_body_custody": root_bodies,
              "fresh_record_custody": record_custody, "fresh_downloads": downloads, "fresh_logical_payloads": members,
              "fresh_target_row": {"spreadsheet_id": SID, "sheet_id": GID, "sheet_title": "Math Puzzles", "range": RANGE,
                                   "all_four_strings_equal_intended": True, "chat_url_authorized_blank": True, "actual_GWS_process": cli_receipt},
              "input_pins": [pin(A / n) for n in inputs], "auditor_script_pin": pin(Path(__file__)),
              "no_service_mutations": True, "no_human_outreach": True, "no_Git_or_editor_operations": True,
              "non_target_sheet_titles_and_rows_omitted": True, "historical_PID_records_not_freshly_observed": True,
              "historical_process_evidence_limit": "Stored child process/stream custody is internally authenticated and corroborated by independent fresh live service GETs; historical PIDs are not retroactively observed and authorize no future execution.",
              "checks": CHECKS}
    write("VERDICT.json", result)
    print(json.dumps({"scope_complete": True, "required_findings": [], "optional_findings": [], "DOI": DOI,
                      "fresh_live_publication": True, "logical_payloads": 46, "members": 47, "exact_target_range": RANGE,
                      "four_strings_exact": True, "fresh_GET_PID": os.getpid(), "fresh_GWS_child_PID": child.pid}))


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        write("FAILED_ATTEMPT.json", {"UTC": now(), "actual_auditor_PID": os.getpid(), "error": str(exc), "checks": CHECKS})
        raise
