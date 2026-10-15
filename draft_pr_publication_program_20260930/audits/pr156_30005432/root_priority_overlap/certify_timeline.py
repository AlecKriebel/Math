from pathlib import Path
import json, subprocess, datetime, hashlib, base64, urllib.request
A=Path("/Users/alec/Documents/Math/draft_pr_publication_program_20260930/audits/pr85_30001203/isolated_main_integration_20261005/checkout/draft_pr_publication_program_20260930/audits/pr156_30005432"); D=A/"root_priority_overlap"; P=D/"private_sources"
def now(): return datetime.datetime.now(datetime.timezone.utc).isoformat()
def api(path):
    out=subprocess.run(["/opt/homebrew/Cellar/gh/2.85.0/bin/gh","api",path],capture_output=True,check=True).stdout
    return json.loads(out),out
pr=json.loads((P/"github_PR156_readback.json").read_text())
repo,raw=api("repos/AlecKriebel/Math"); (P/"github_repository_metadata.json").write_bytes(raw)
commits,raw=api("repos/AlecKriebel/Math/pulls/156/commits"); (P/"github_PR156_commits.json").write_bytes(raw)
proofpath="unsolved_math_prioritization/attempts/30005432/COUNTEREXAMPLE.md"
checks=[]
expected="cb127cdc60740596a6e08bd0cb1cfb894b1d24ac8bc56a7338a885798b0a33ae"
for item in commits:
    sha=item["sha"]
    data,raw=api("repos/AlecKriebel/Math/contents/"+proofpath+"?ref="+sha)
    body=base64.b64decode(data["content"])
    actual=hashlib.sha256(body).hexdigest()
    if actual!=expected: raise RuntimeError("Original proof changed at "+sha)
    checks.append({"commit":sha,"commit_author_UTC":item["commit"]["author"]["date"],"commit_committer_UTC":item["commit"]["committer"]["date"],"proof_git_blob":data["sha"],"proof_bytes":len(body),"proof_sha256":actual})
v1=json.loads((P/"zenodo_23292254.json").read_text())
f=next(x for x in v1["files"] if x["key"].endswith("paper.pdf"))
with urllib.request.urlopen(f["links"]["self"],timeout=35) as r: body=r.read()
(P/"eulersolve_v1_0.pdf").write_bytes(body)
subprocess.run(["/opt/homebrew/bin/pdftotext","-layout",str(P/"eulersolve_v1_0.pdf"),str(P/"eulersolve_v1_0.txt")],check=True)
receipt={"UTC":now(),"status":"DATED_ORIGINAL_PR_AND_LATER_EXACT_COUNTEREXAMPLE_RECORDED","repository_current_visibility":repo.get("visibility"),"repository_current_private":repo["private"],"historical_visibility_independently_archived":False,"human_context_reports_public_repository":True,"PR_created_at":pr["created_at"],"original_current_head":pr["head"]["sha"],"proof_present_unchanged_in_all_four_original_branch_commits":checks,"initial_proof_commit":checks[0]["commit"],"commit_dates_are_author_supplied_not_provider_publication_receipts":True,"provider_PR_creation_date_is_separate_evidence":True,"later_Zenodo_v1_record":v1["id"],"later_v1_created_UTC":v1["created"],"later_v1_DOI":v1["doi"],"later_v1_pdf_sha256":hashlib.sha256(body).hexdigest(),"later_v1_pdf_bytes":len(body),"matching_core_formula_and_property_s_classification":True,"proof_has_required_substantive_changes_since_original_submission":False,"diagnostic_and_source_wording_repairs_required":True,"literal_simultaneous_release":False,"mutual_awareness_or_independence_certified":False,"priority_or_publication_clearance":False,"MAIN_or_PR_writes":False}
(D/"TIMELINE_RECEIPT.json").write_text(json.dumps(receipt,indent=2)+"\n")
print(json.dumps({k:v for k,v in receipt.items() if k!="proof_present_unchanged_in_all_four_original_branch_commits"},indent=2))

