from pathlib import Path
import datetime,importlib.util,json,subprocess,sys
R=Path("/Users/alec/Documents/Math");D=R/"draft_pr_claimed_solved_700_800_20261012";T=D/"audits/pr789_30001478/tmp";M=T/"root-receipts";U=T/"publication";sys.path.insert(0,str(D))
from graphql_scoped_commit import get_pr,Remote
spec=importlib.util.spec_from_file_location("approved_pr789_driver",T/"publication_driver.py");driver=importlib.util.module_from_spec(spec);spec.loader.exec_module(driver);g,inv=driver.gate()
p=get_pr(789);assert p["state"]=="open"and not p["merged"]and p["head"]["sha"]==g["reviewed_head"]=="aa44dec3baf8c1cd179cf8b55f32be95c74ee81a"
r=Remote(p["head"]["sha"]);q=[l for l in r.read("unsolved_math_prioritization/QUEUE.md").splitlines()if l.startswith("| ")and" 30001478 / "in l];assert len(q)==1 and q[0].split("|")[8].strip()=="claimed_solved"
pub=json.loads((U/"PUBLISH_RECEIPT.json").read_text());public=json.loads((U/"PUBLIC_VERIFICATION.json").read_text());sheet=json.loads((U/"SHEET_VERIFICATION.json").read_text())
assert pub["state"]=="published"and public["result"]==sheet["result"]=="PASS"and pub["doi"]==public["doi"]==sheet["doi"]and not pub["metadata_normalizations"]
doi=pub["doi"];rng=sheet["updated_range"];assert len(g["completed_whole_reviews"])==4 and g["final_current_round_clean"]is True
body=f"""The exact six-relation Rogalski–Sierra algebra has the nonzero homogeneous completely prime ideal I=(x3-x1,x4-x2), strictly below the irrelevant ideal. Its exact quotient is the twisted homogeneous coordinate ring B(P1,O(1),sigma), with sigma[s:t]=[s+beta*t:beta*s+t], Hilbert series (1-z)^(-2), and GK-dimension 2. This refutes both literal assertions in the 2010 OWR problem and the 2012 article. The presentation theorem holds over every field when beta^2 differs from 1, with arbitrary alpha; the journal's fractional geometric parameter identification is used only in characteristic different from two.

The four-page research note [A projective-line quotient of the Rogalski–Sierra algebra](https://doi.org/{doi}), version 1.0, CC BY 4.0, includes a self-contained proof and the exact source/verification archive. It makes no prime classification, embedding, common graded quotient ring, or surface-dimensional image claim.

Historical priority remains unresolved. Classical quantum/Jordan-plane, degree-reduction, graded-twist and THCR machinery is credited. The inspected Nevins–Sierra arXiv versions repeat the contrary no-map assertion, while their canonical-factor and moduli theorems need extra hypotheses. Campbell's baseline infinitesimal deformations and function skew fields of another family do not supply this exact generic algebra's homomorphic curve quotient. Inspected preprints are distinguished from the unread journal body. No firstness, certified novelty, exhaustive absence, or current worldwide-open status is claimed.

Two independent mathematical families and two bounded priority families were followed by four distinct freshly initialized complete whole-preprint adversaries. The final current package has zero actionable issues. Reproduction includes Python 3.14/3.12 normal and optimized modes, exact six-artifact rebuilds, archive relocation, and meaningful rejection controls. All four PDF pages were visually checked. Public Zenodo downloads match the reviewed SHA256 hashes, every supplied metadata value matches without normalization, and the Google tracker has one exact four-cell entry at {rng}.

AI tools were used extensively in solving, verifying, and writing this work. The preprint is unrefereed, with no external human peer review or formal proof verification. All 58 original candidate files and the explicit 1/5 proof-attempt budget are preserved.

The reviewed scientific head is aa44dec3baf8c1cd179cf8b55f32be95c74ee81a. Source-manifest SHA256: {inv["source_manifest_sha256"]}. [Audit, independent reviews, and publication receipts](https://github.com/AlecKriebel/Math/tree/main/draft_pr_claimed_solved_700_800_20261012/audits/pr789_30001478/tmp).
"""
path=M/"FINAL_PR_BODY.md";path.write_text(body)
title="Publish a projective-line quotient refuting the Rogalski–Sierra assertions (30001478)"
out=subprocess.run(["gh","pr","edit","789","--title",title,"--body-file",str(path)],cwd=R,capture_output=True,text=True)
(M/"PR_EDIT_STDOUT.txt").write_text(out.stdout);(M/"PR_EDIT_STDERR.txt").write_text(out.stderr)
if out.returncode:raise RuntimeError(out.stderr or out.stdout)
after=get_pr(789);assert after["head"]["sha"]==p["head"]["sha"]and after["state"]=="open"
if after["draft"]:
 out2=subprocess.run(["gh","pr","ready","789"],cwd=R,capture_output=True,text=True)
 (M/"PR_READY_STDOUT.txt").write_text(out2.stdout);(M/"PR_READY_STDERR.txt").write_text(out2.stderr)
 if out2.returncode:raise RuntimeError(out2.stderr or out2.stdout)
(M/"PR_READY_GATE.json").write_text(json.dumps({"utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),"result":"PASS","before":p,"after":get_pr(789),"title":title,"DOI":doi},indent=2)+"\n")
print(json.dumps({"result":"PASS","ready":True,"head":p["head"]["sha"],"doi":doi}))

