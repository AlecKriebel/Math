#!/usr/bin/env python3
"""Read-only PR788 priority packet custody; mathematical priority is not mechanized."""
import argparse, hashlib, json, os, pathlib, stat, sys

HEAD = "3412d5a074c3f3a03f75735a9ccf1755e172204a"
SELECTED = "9fecfb4e59ffae554cdbf2e777005361981237b6236a1a16827a6b70e345927b"
GATE = "6411fabd845b616673818ce02c9beb29647056a0f6683ba6731a3cdd68b7e431"
IDENTITY = "5c325a88c0eb5cbae891780b5e5500eaf14565e817aa343a8bcc2bfa346ad32e"
INITIAL = "INITIAL_POSITION.json"
REPORT_PIN = "1cd07885ed60a5d9ebde4d5cda65f205a2622a9ffccf1765ffc2534e0b6490ac"
MAX_BYTES = 16 * 1024 * 1024

def need(condition, message):
    if not condition:
        raise ValueError(message)

def digest(data):
    return hashlib.sha256(data).hexdigest()

def parts(name):
    need(isinstance(name, str) and name != "", "invalid name")
    p = pathlib.PurePosixPath(name)
    need(not p.is_absolute() and str(p) == name and all(x not in ("", ".", "..") for x in p.parts), "noncanonical relative name")
    return p.parts

def root_open(name):
    need(os.path.isabs(name) and os.path.normpath(name) == name, "noncanonical root")
    flags = os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW | os.O_CLOEXEC
    fd = os.open("/", flags)
    try:
        for component in pathlib.PurePosixPath(name).parts[1:]:
            new = os.open(component, flags, dir_fd=fd)
            os.close(fd)
            fd = new
        return fd
    except BaseException:
        os.close(fd)
        raise

def read_regular(root_fd, name):
    seq = parts(name)
    fd = os.dup(root_fd)
    try:
        for component in seq[:-1]:
            new = os.open(component, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW | os.O_CLOEXEC, dir_fd=fd)
            os.close(fd)
            fd = new
        fil = os.open(seq[-1], os.O_RDONLY | os.O_NONBLOCK | os.O_NOFOLLOW | os.O_CLOEXEC, dir_fd=fd)
        try:
            st = os.fstat(fil)
            need(stat.S_ISREG(st.st_mode), "not a regular file: " + name)
            need(st.st_nlink == 1, "hardlink alias: " + name)
            need(st.st_size <= MAX_BYTES, "oversized input: " + name)
            chunks = []
            total = 0
            while True:
                b = os.read(fil, 1024 * 1024)
                if not b:
                    break
                total += len(b)
                need(total <= MAX_BYTES, "growing oversized input")
                chunks.append(b)
            need(total == st.st_size, "concurrent size change")
            data = b"".join(chunks)
            end = os.fstat(fil)
            need((st.st_dev, st.st_ino, st.st_size, st.st_mtime_ns) == (end.st_dev, end.st_ino, end.st_size, end.st_mtime_ns), "concurrent input change")
            return data
        finally:
            os.close(fil)
    finally:
        os.close(fd)

def js(data):
    def unique(pairs):
        out = {}
        for key, value in pairs:
            need(key not in out, "duplicate JSON key")
            out[key] = value
        return out
    return json.loads(data.decode("utf-8"), object_pairs_hook=unique)

def tree_names(fd, prefix=""):
    out = []
    for name in sorted(os.listdir(fd)):
        rel = prefix + name
        st = os.stat(name, dir_fd=fd, follow_symlinks=False)
        if stat.S_ISDIR(st.st_mode):
            sub = os.open(name, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW | os.O_CLOEXEC, dir_fd=fd)
            try:
                nested = tree_names(sub, rel + "/")
                need(nested, "unexpected empty directory")
                out.extend(nested)
            finally:
                os.close(sub)
        else:
            need(stat.S_ISREG(st.st_mode), "nonregular original entry: " + rel)
            out.append(rel)
    return out

def check(args):
    self_path = os.path.abspath(__file__)
    self_root = root_open(str(pathlib.Path(self_path).parent))
    try:
        need(digest(read_regular(self_root, pathlib.Path(self_path).name)) == args.checker_sha256, "checker pin mismatch")
    finally:
        os.close(self_root)
    packet = root_open(args.packet_root)
    intake = root_open(args.intake_root)
    try:
        raw = read_regular(packet, "MANIFEST.json")
        need(digest(raw) == args.manifest_sha256, "manifest pin mismatch")
        manifest = js(raw)
        need(manifest["schema"] == "pr788-priority-question-authored-v1", "manifest schema")
        rows = manifest["files"]
        names = [r["path"] for r in rows]
        need(len(names) == len(set(names)) and names == sorted(names), "duplicate or unsorted manifest members")
        need("MANIFEST.json" not in names, "cyclic self-manifest")
        need(set(os.listdir(packet)) == set(names) | {"MANIFEST.json"}, "packet membership mismatch")
        payload = {}
        for r in rows:
            name = r["path"]
            need(len(parts(name)) == 1 and pathlib.Path(name).suffix in (".json", ".md", ".py"), "non-authored packet member")
            data = read_regular(packet, name)
            need(len(data) == r["bytes"] and digest(data) == r["sha256"], "payload mismatch: " + name)
            payload[name] = data
        initial = js(payload[INITIAL])
        need(initial["target"] == {"pr":788,"problem":"30001522","head":HEAD}, "initial target mismatch")
        need(initial["input_hashes"] == {"SELECTED_PUBLIC_RECORD.json":SELECTED,"ELIGIBILITY_GATE.json":GATE}, "initial intake pins")
        verdict = js(payload["VERDICT.json"])
        need(verdict["status"] == "PRIORITY_UNRESOLVED", "scope inflation: status")
        for key in ("full_matching_prior_verified","firstness_certified","originality_certified","current_worldwide_open_certified","fresh_initialized_session","mathematical_gate_reaudited"):
            need(verdict[key] is False, "scope inflation: " + key)
        need(verdict["reused_session_prior_PR786_exposure"] is True, "session disclosure")
        need(verdict["current_peer_root_priority_conclusions_read_before_report_freeze"] is False, "independence record")
        need(verdict["new_proof_search_turns"] == 0 and verdict["original_budget_used"] == 2 and verdict["original_budget_limit"] == 5, "budget changed")
        need(digest(payload["REPORT.md"]) == REPORT_PIN == verdict["report_sha256_at_independent_freeze"], "frozen report pin")
        need([x["id"] for x in verdict["actionable_context_additions"]] == ["C1"], "context action missing")
        bindings = js(payload["INPUT_BINDINGS.json"])
        need((bindings["pr"], bindings["problem"], bindings["head"], bindings["queue_status"], bindings["original_budget"]) == (788,"30001522",HEAD,"claimed_solved","2/5"), "binding target")
        inrows = bindings["files"]
        innames = [r["path"] for r in inrows]
        need(len(innames) == len(set(innames)) == bindings["intake_file_count"] == 51, "input member count")
        input_data = {}
        for r in inrows:
            data = read_regular(intake, r["path"])
            need(len(data) == r["bytes"] and digest(data) == r["sha256"], "input mismatch: " + r["path"])
            if r["path"] in ("SELECTED_PUBLIC_RECORD.json","ELIGIBILITY_GATE.json","ROOT_SOURCE_IDENTITY.json"):
                input_data[r["path"]] = data
        for n,pin in (("SELECTED_PUBLIC_RECORD.json",SELECTED),("ELIGIBILITY_GATE.json",GATE),("ROOT_SOURCE_IDENTITY.json",IDENTITY)):
            need(digest(input_data[n]) == pin, "fixed intake pin mismatch")
        gate = js(input_data["ELIGIBILITY_GATE.json"])
        need((gate["result"],gate["queue_status"],gate["pr"],gate["problem"],gate["original_explicit_budget"]) == ("ELIGIBLE","claimed_solved",788,"30001522","2/5"), "ineligible target")
        need(gate["pr_metadata"]["headRefOid"] == HEAD, "head mismatch")
        identity = js(input_data["ROOT_SOURCE_IDENTITY.json"])
        expected_original = sorted(r["path"] for r in identity["original_files"])
        need(len(expected_original) == bindings["original_file_count"] == identity["original_file_count"] == 48, "original count")
        need(sorted(n.removeprefix("original/") for n in innames if n.startswith("original/")) == expected_original, "original bindings mismatch")
        orig_fd = os.open("original", os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW | os.O_CLOEXEC, dir_fd=intake)
        try:
            need(sorted(tree_names(orig_fd)) == expected_original, "original membership mismatch")
        finally:
            os.close(orig_fd)
        ledger = js(payload["SOURCE_LEDGER.json"])
        need(ledger["full_matching_prior_verified"] is False and ledger["firstness_certified"] is False and ledger["current_worldwide_open_certified"] is False, "scope inflation: source ledger")
        sources = ledger["sources"]
        need(len(sources) == 16 and len(set(r["id"] for r in sources)) == 16, "source count")
        queries = js(payload["QUERY_LEDGER.json"])
        need(len(queries) == 14 and sum(len(r["queries"]) for r in queries) == 54, "query count")
        matrix = js(payload["COMPARISON_MATRIX.json"])
        need(matrix["priority_certificate"] is False and matrix["full_prior_verified"] is False, "scope inflation: comparisons")
        byid = {r["id"]:r for r in matrix["comparisons"]}
        need(byid["cwy_mundet"]["simple_space_hypotheses"] is False and byid["cwy_mundet"]["actual_free_odd_prime_actions"] is True, "CWY comparison lost")
        need(byid["rational_rank"]["same_fixed_space_required"] is False, "rational invariant conflation")
        body_count = 0
        if args.bodies_root:
            bodies = root_open(args.bodies_root)
            try:
                for r in sources:
                    for kind in ("pdf","text"):
                        data = read_regular(bodies, r[kind+"_file"])
                        need(len(data) == r[kind+"_bytes"] and digest(data) == r[kind+"_sha256"], "body mismatch: " + r["id"])
                        body_count += 1
                visual = js(payload["VISUAL_RECEIPT.json"])
                data = read_regular(bodies, visual["render_file"])
                need(len(data) == visual["render_bytes"] and digest(data) == visual["render_sha256"], "render mismatch")
                body_count += 1
            finally:
                os.close(bodies)
        return {"result":"PASS","pr":788,"problem":"30001522","packet_files":len(names)+1,"bound_intake_files":51,"bound_original_files":48,"primary_sources":16,"external_body_files_replayed":body_count,"external_body_replay":bool(args.bodies_root),"priority_certified":False,"manifest_sha256":args.manifest_sha256,"checker_sha256":args.checker_sha256,"optimization":sys.flags.optimize}
    finally:
        os.close(packet)
        os.close(intake)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--packet-root", required=True)
    ap.add_argument("--intake-root", required=True)
    ap.add_argument("--bodies-root")
    ap.add_argument("--manifest-sha256", required=True)
    ap.add_argument("--checker-sha256", required=True)
    args = ap.parse_args()
    try:
        print(json.dumps(check(args), sort_keys=True))
    except (ValueError, OSError, KeyError, TypeError, UnicodeError) as exc:
        print("FAIL: " + str(exc), file=sys.stderr)
        return 2
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
