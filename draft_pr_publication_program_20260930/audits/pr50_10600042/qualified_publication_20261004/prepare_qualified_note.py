"""Apply the human-authorized priority qualification to the open document in place."""
from pathlib import Path
import datetime as dt
import hashlib
import json
import shutil

F = Path(__file__).resolve().parent
A = F.parent
P = A / "publication_package_v3"
baseline = json.loads((A / "root_current_promotion_20261004/V3_FINAL_REVIEW_AND_PRIORITY_HOLD.json").read_text())
snapshot = F / "preauthorization_snapshot"
snapshot.mkdir(exist_ok=False)
for name, pin in baseline["reviewed_upload_pins"].items():
    body = (P / name).read_bytes()
    assert len(body) == pin["size"] and hashlib.sha256(body).hexdigest() == pin["sha256"]
    (snapshot / (name + ".before-qualification")).write_bytes(body)
for name in ["README.md", "SOURCE_QUALIFICATIONS.md", "VERIFICATION_RECORD.json", "SHA256SUMS"]:
    (snapshot / (name + ".before-qualification")).write_bytes((P / name).read_bytes())

tex_path = P / "even_strand_markov.tex"
tex = tex_path.read_text()
old = "No historical-priority or present-openness claim is made."
new = "Historical priority remains unresolved: we could not access the identified\nfuller texts of Nencka to complete the priority review. No first-priority or\npresent-openness claim is made."
assert tex.count(old) == 1
tex = tex.replace(old, new)
old = "We have identified fuller related texts~\\cite{Nencka98,Nencka99}, whose bodies\nhave not yet been accessed; the bearing of those texts on exact\nordinary-closure priority remains unresolved."
new = "We could not obtain the full texts of the related 1998 article and 1999\nchapter~\\cite{Nencka98,Nencka99}, or the catalogued 1996 preprint\n\\cite{NenckaPreprint}. The publisher of the 1998 article lists its full text as\nunavailable, and the 1999 chapter requires institutional access. Consequently\nour priority review is incomplete, and the bearing of these texts on exact\nordinary-closure priority remains unresolved. Unavailable text is not evidence\nthat an earlier result is absent or incorrect. This note presents a verified\nexplicit formulation; it does not establish a historically new resolution."
assert tex.count(old) == 1
tex = tex.replace(old, new)
old = "unrefereed; no human peer review or formal proof certification is claimed."
new = "unrefereed and has not undergone conventional human peer review. No formal\nproof certification is claimed."
assert tex.count(old) == 1
tex = tex.replace(old, new)
anchor = "\\bibitem{Nencka98}"
assert tex.count(anchor) == 1
tex = tex.replace(anchor, "\\bibitem{NenckaPreprint} H.~Nencka, \\emph{Cantorian Braid Groups},\nCNRS CPT96/P.3381, Marseille (1996), 12~pp.\n\\href{https://ntb.jinr.ru/arch99/pw32.html}{JINR library catalogue, item~2258};\nfull text not accessed.\n" + anchor)
tex_path.write_text(tex)
tex_pin = {"bytes": len(tex_path.read_bytes()), "sha256": hashlib.sha256(tex_path.read_bytes()).hexdigest()}

qualification = "We could not obtain the full texts of Nencka's identified 1998 article, 1999 chapter, or catalogued 1996 preprint CPT96/P.3381. The priority review is therefore incomplete, and historical ordinary-closure priority remains unresolved. This note establishes the displayed formulation from explicitly credited unrestricted theorems; it does not establish a historically new resolution. Unavailable text is not evidence of absence or invalidity of earlier work."
readme = (P / "README.md").read_text()
old = "This note makes no first-priority claim."
assert readme.count(old) == 1
readme = readme.replace(old, "This note makes no first-priority claim. " + qualification)
(P / "README.md").write_text(readme)
q = (P / "SOURCE_QUALIFICATIONS.md").read_text()
q = q.replace("## Authenticated fuller texts and remaining priority hold", "## Incomplete priority review and unavailable fuller texts")
q = q.replace("Fair credit does not resolve the global priority gate.", qualification)
(P / "SOURCE_QUALIFICATIONS.md").write_text(q)
metadata_path = P / "zenodo-deposit.json"
metadata = json.loads(metadata_path.read_text())
metadata["metadata"]["description"] += "<p><strong>Incomplete priority review:</strong> " + qualification + "</p>"
metadata_path.write_text(json.dumps(metadata, indent=2, ensure_ascii=False) + "\n")
record_path = P / "VERIFICATION_RECORD.json"
record = json.loads(record_path.read_text())
record["schema"] = "even-strand-markov-portable-verification-record/v3"
record["manuscript_provenance"]["historical_tex_binding_before_access_qualification"] = record["manuscript_provenance"]["submission_tex_binding"]
record["manuscript_provenance"]["submission_tex_binding"] = tex_pin
record["manuscript_provenance"]["change"] = "Priority/access and review disclosures clarified in place; all mathematical statements, universal proof, checker and expected results are unchanged."
record["priority_review"] = {"status": "INCOMPLETE_ACCESS_LIMITED", "historical_priority": "UNRESOLVED", "novelty_certified": False,
    "fuller_Nencka_bodies_accessed": False, "qualification": qualification}
record_path.write_text(json.dumps(record, indent=2, ensure_ascii=False) + "\n")
members = ["LICENSE-CODE.txt", "LICENSE-TEXT.md", "README.md", "SOURCE_QUALIFICATIONS.md", "VERIFICATION_RECORD.json", "build_verification_zip.py", "even_strand_markov.tex", "expected_results.json", "verify_even_calculus.py"]
(P / "SHA256SUMS").write_text("".join(hashlib.sha256((P / n).read_bytes()).hexdigest() + "  " + n + "\n" for n in members), encoding="ascii")
# The old reviewed archive is preserved before freeing its original destination for the builder.
assert (snapshot / "even-strand-markov-verification-v3.zip.before-qualification").read_bytes() == (P / "even-strand-markov-verification-v3.zip").read_bytes()
(P / "even-strand-markov-verification-v3.zip").unlink()
now = dt.datetime.now(dt.timezone.utc).isoformat()
authorization = {"UTC": now, "PR": 50, "submitted_head": baseline["submitted_head"],
    "user_instruction": "Let's do this. We can note that we were not able to access this to complete a fully priority. Publish, then, continue with the goal.",
    "authorized_exception": "Publish PR50 as a mathematically verified, unrefereed research note with Nencka credited and historical priority explicitly unresolved; then complete tracker/merge and continue the original goal.",
    "exception_scope": "PR50 only; unchanged claimed_solved eligibility and ascending order for later PRs", "priority_cleared": False, "novelty_certified": False,
    "manuscript_edited_in_place": str(tex_path), "new_tex_binding": tex_pin,
    "unchanged_checker_sha256": hashlib.sha256((P / "verify_even_calculus.py").read_bytes()).hexdigest(),
    "unchanged_expected_sha256": hashlib.sha256((P / "expected_results.json").read_bytes()).hexdigest(),
    "fresh_complete_package_reviews_required": True, "publication_performed": False, "new_central_proof_attempts": 0,
    "estimates": {"qualified_wording_percent": 100, "qualified_publication_workflow_percent": 10, "program_percent": 3.030303}}
(F / "USER_AUTHORIZATION_AND_PREPARATION.json").write_text(json.dumps(authorization, indent=2) + "\n")
(F / "RESEARCH_LOG.md").write_text("# Qualified PR50 publication\n\n" + now + " — Applied the human-authorized publication exception to PR50 only. Preserved preauthorization payload bytes, edited the open manuscript in place, and propagated explicit incomplete priority/access wording to metadata and portable materials. Mathematics, checker, expected results and original 1/5 attempt budget are unchanged. Fresh exact-package reviews and real publication/readback/tracker/merge remain required. Wording 100%; current qualified workflow 10%; overall program 3.030303%.\n")
print(json.dumps(authorization, indent=2))
