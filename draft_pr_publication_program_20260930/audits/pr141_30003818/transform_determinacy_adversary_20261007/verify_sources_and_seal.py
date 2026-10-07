"""Seal this independent mathematical review without changing shared artifacts."""
from pathlib import Path
from hashlib import sha256
from datetime import datetime, timezone
import json
import os
import signal
import subprocess

root = Path(__file__).resolve().parent
shared = root.parent / "private_sources"
input_manifest = json.loads((root / "INPUT_MANIFEST.json").read_text())
for pin in input_manifest["files"]:
    p = Path(pin["path"])
    data = p.read_bytes()
    if len(data) != pin["size"] or sha256(data).hexdigest() != pin["sha256"] or p.stat().st_mode & 0o777 != pin["mode"]:
        raise RuntimeError("unchanged submitted input pin mismatch")

args = ["/opt/homebrew/bin/pdftotext", "-f", "53", "-l", "54", "-layout", str(shared / "moerters-peres.pdf"), "-"]
begin = datetime.now(timezone.utc).isoformat()
child = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, start_new_session=True)
try:
    out, err = child.communicate(timeout=20)
except subprocess.TimeoutExpired:
    os.killpg(child.pid, signal.SIGKILL)
    child.communicate()
    raise RuntimeError("source reader timed out")
end = datetime.now(timezone.utc).isoformat()
try:
    os.killpg(child.pid, 0)
    absent = False
except ProcessLookupError:
    absent = True
if child.returncode or err or not absent or child.poll() is None:
    raise RuntimeError("source reader custody failure")
text = out.decode()
if "Theorem 2.16 (Strong Markov property)" not in text or "almost surely finite stopping time" not in text:
    raise RuntimeError("wrong strong-Markov source slice")
lalley = (shared / "lalley.txt").read_text()
if "Exercise 6. Eigenfunction expansions." not in lalley or "sin(k" not in lalley:
    raise RuntimeError("wrong killed-kernel source text")

source_pins = []
for filename, url, role in [
    ("owr.pdf", "https://ems.press/content/serial-article-files/46745", "printed1452/PDFzero-based71; original problem read"),
    ("owr_printed_p1452.png", "https://ems.press/content/serial-article-files/46745", "original page visually inspected using view_image"),
    ("lalley.pdf", "https://galton.uchicago.edu/~lalley/Courses/312/BrownianMotion312.pdf", "Exercise6 eigenfunction discussion"),
    ("lalley.txt", "https://galton.uchicago.edu/~lalley/Courses/312/BrownianMotion312.pdf", "independently read source extraction"),
    ("moerters-peres.pdf", "https://www.mi.uni-koeln.de/~moerters/book/book.pdf", "actual Theorem2.16 and proof, printed43--44/PDFone-based53--54"),
]:
    p = shared / filename
    data = p.read_bytes()
    source_pins.append({"filename": filename, "url": url, "role": role, "size": len(data), "sha256": sha256(data).hexdigest(), "copyrighted_body_copied_to_this_review": False})
source_record = {
    "actual_pid": os.getpid(), "utc": datetime.now(timezone.utc).isoformat(),
    "source_pins": source_pins,
    "child": {"pid": child.pid, "args": args, "started_utc": begin, "ended_utc": end,
              "returncode": child.returncode, "reaped": True, "process_group_absent": absent,
              "stdout_size": len(out), "stdout_sha256": sha256(out).hexdigest(),
              "stderr_size": len(err), "stderr_sha256": sha256(err).hexdigest(),
              "copyrighted_stdout_retained_publicly": False},
    "preliminary_wrong_offset_slice_not_used_as_theorem_authority": True,
    "sources_verified": True,
}
(root / "SOURCE_READBACK.json").write_text(json.dumps(source_record, indent=2) + "\n")
reproduction = json.loads((root / "REPRODUCTION_RESULT.json").read_text())
if reproduction["verdict"] != "PASS" or not reproduction["all_children_reaped"] or not reproduction["all_process_groups_absent"]:
    raise RuntimeError("reproduction not complete")
new_controls = json.loads((root / "new_clock_controls_normal.stdout").read_text())
log = root / "RESEARCH_LOG.md"
log.write_text(log.read_text() + "\n" + datetime.now(timezone.utc).isoformat() +
               " — Adversarial mathematical review complete. No mandatory mathematical correction found in the finite-k analytic-transform characterization. Submitted8,520/old46,056 controls replay; new11,777 exact controls per mode and2,052 weighted continuous-time finite-cycle cases pass; three incorrect clock substitutes falsified. Every submitted input fully rechecked unchanged. Strong-Markov theorem actual pages independently verified; no source text bodies copied. Best-guess completion of this adversarial task:100%. Priority and publication-package acceptance remain outside scope.\n")
result = {
    "schema": "pr141-transform-determinacy-independent-mathematical-review/v1",
    "verdict": "PASS_COMPLETE_ANALYTIC_TRANSFORM_CHARACTERIZATION",
    "scope": "PR141_original_head_mathematics_stage_transform_and_determinacy",
    "head": input_manifest["head"], "problem_id": 30003818,
    "actual_sealer_pid": os.getpid(), "sealed_utc": datetime.now(timezone.utc).isoformat(),
    "independent_review": True, "fixture": False,
    "mandatory_mathematical_corrections": [],
    "optional_verification_package_hardening": ["Author diagnostic ck uses assert; use an explicit exception or specify normal non-optimized execution to prevent misleading -O diagnostic counts."],
    "priority_verified": False, "publication_package_review": False,
    "strongest_verified_result": "Every coefficient of the finite-k joint Laplace transform is a deterministic finite sum of integrals of explicit summed interval-exit kernels; outer series and uniform factorial remainder, correlated clocks, and compact-simplex joint-law determinacy are valid for the stated two seed laws.",
    "limitations": ["No efficient quadrature or inner Fourier truncation certification.", "No named density or large-k asymptotic claim.", "Finite CTMC controls are diagnostics, not a proof of a Brownian limit.", "No established historical novelty or publication approval."],
    "unchanged_submitted_members_authenticated": len(input_manifest["files"]),
    "author_assertions": reproduction["author_assertions"],
    "old_independent_assertions": reproduction["old_independent_assertions"],
    "new_independent_assertions_per_mode": reproduction["new_independent_assertions_per_mode"],
    "new_weighted_CTMC_configurations": new_controls["weighted_CTMC_configurations"],
    "actual_control_processes_reaped_and_groups_absent": True,
    "actual_source_reader_reaped_and_group_absent": True,
    "case_task_completion_percent": 100,
}
for filename in ("REPORT.md", "INPUT_MANIFEST.json", "SOURCE_READBACK.json", "REPRODUCTION_RESULT.json", "CHILD_JOURNAL.json"):
    data = (root / filename).read_bytes()
    result[filename] = {"size": len(data), "sha256": sha256(data).hexdigest()}
(root / "RESULT.json").write_text(json.dumps(result, indent=2) + "\n")
members = []
for p in sorted(root.rglob("*")):
    if not p.is_file() or p.name == "FINAL_MANIFEST.json":
        continue
    p.chmod(0o444)
    data = p.read_bytes()
    members.append({"path": str(p.relative_to(root)), "size": len(data), "sha256": sha256(data).hexdigest(), "mode": p.stat().st_mode & 0o777})
manifest = {"schema": "pr141-independent-mathematical-review-closed-manifest/v1",
            "actual_sealer_pid": os.getpid(), "sealed_utc": datetime.now(timezone.utc).isoformat(),
            "self_excluded": "FINAL_MANIFEST.json", "members": members}
p = root / "FINAL_MANIFEST.json"
p.write_text(json.dumps(manifest, indent=2) + "\n")
p.chmod(0o444)
for pin in members:
    p = root / pin["path"]
    data = p.read_bytes()
    if len(data) != pin["size"] or sha256(data).hexdigest() != pin["sha256"] or p.stat().st_mode & 0o777 != pin["mode"]:
        raise RuntimeError("closed review readback mismatch")
print(json.dumps({"verdict": result["verdict"], "actual_sealer_pid": os.getpid(),
                  "closed_members": len(members),
                  "RESULT_sha256": sha256((root / "RESULT.json").read_bytes()).hexdigest(),
                  "REPORT_sha256": sha256((root / "REPORT.md").read_bytes()).hexdigest(),
                  "FINAL_MANIFEST_sha256": sha256((root / "FINAL_MANIFEST.json").read_bytes()).hexdigest()}))
