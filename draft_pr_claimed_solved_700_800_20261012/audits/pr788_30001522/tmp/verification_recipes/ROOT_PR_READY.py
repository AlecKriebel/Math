from pathlib import Path
import datetime,json,subprocess,sys
R=Path("/Users/alec/Documents/Math");D=R/"draft_pr_claimed_solved_700_800_20261012";T=D/"audits/pr788_30001522/tmp";M=T/"root-receipts";sys.path.insert(0,str(D));from graphql_scoped_commit import get_pr,Remote
p=get_pr(788);assert p["state"]=="open"and not p["merged"]and p["head"]["sha"]=="3412d5a074c3f3a03f75735a9ccf1755e172204a"
r=Remote(p["head"]["sha"]);q=[l for l in r.read("unsolved_math_prioritization/QUEUE.md").splitlines()if l.startswith("| ")and" 30001522 / "in l];assert len(q)==1 and q[0].split("|")[8].strip()=="claimed_solved"
g=json.loads((T/"FINAL_READINESS.json").read_text());assert g["publication_DOI"]=="10.5281/zenodo.23422039"
body="""The fixed Wu manifold W = SU(3)/SO(3) answers Hanke's printed 2010 existence question (OWR-4413-005 / problem30001522): it is a finite simply connected complex of rational homotopy type S^5, with actual free toral rank0 and free p-rank1 for every odd prime. The proof excludes arbitrary continuous free circle and involution actions and proves the all-prime rank upper bound; it distinguishes actual free actions from almost-free and rational toral rank.

The published four-page research note is [A classical Wu-manifold answer to a free-rank question](https://doi.org/10.5281/zenodo.23422039), version1.0, CC BY4.0, with the exact reviewed PDF and source/verification archive. This is a classical explanatory assembly: Yeroshkin's action, Kuhn–Lloyd's involution obstruction and the classical characteristic number are credited. CWY–Mundet examples already admit actual free odd-prime cyclic actions with no nontrivial continuous circle action; their nonabelian fundamental groups exclude them from Hanke's abelian-pi1 target. Historical priority remains unresolved; no firstness, novelty or current worldwide-open status is certified.

Two independent mathematical approach families and two bounded priority families were followed by two distinct freshly initialized whole-preprint adversaries. The final current package has zero actionable issues. Reproduction includes Python3.14/3.12 normal/optimized modes, exact artifact rebuilds, archive relocation and rejection controls; all four PDF pages were visually checked. Public Zenodo downloads match the reviewed SHA256 hashes, all supplied metadata matches without normalization, and the Google tracker was appended once with exact four-cell readback at A128:D128.

AI tools were used extensively in solving, checking and writing this work. The preprint is unrefereed, with no external human peer review or formal proof verification. Original48candidate files and the explicit2/5 proof-attempt budget are preserved.

The reviewed scientific head is 3412d5a074c3f3a03f75735a9ccf1755e172204a. The source-manifest SHA256 is 0af7587170f147a5a0075ebeacb007cca8a4a4eee68d536bbe9339125622fd4d. [Audit, independent reviews and publication receipts](https://github.com/AlecKriebel/Math/tree/main/draft_pr_claimed_solved_700_800_20261012/audits/pr788_30001522/tmp) bind the exact result and files.
"""
# Format prose with standard word spacing while retaining exact technical identifiers.
for a,b in[("problem30001522","problem 30001522"),("rank0","rank 0"),("p-rank1","p-rank 1"),("version1.0","version 1.0"),("BY4.0","BY 4.0"),("Python3.14/3.12","Python 3.14/3.12"),("Original48candidate","Original 48 candidate"),("explicit2/5","explicit 2/5")]:body=body.replace(a,b)
path=M/"FINAL_PR_BODY.md";path.write_text(body)
title="Publish a classical Wu-manifold answer to the free-rank question (30001522)"
out=subprocess.run(["gh","pr","edit","788","--title",title,"--body-file",str(path)],cwd=R,capture_output=True,text=True)
(M/"PR_EDIT_STDOUT.txt").write_text(out.stdout);(M/"PR_EDIT_STDERR.txt").write_text(out.stderr)
if out.returncode:raise RuntimeError(out.stderr or out.stdout)
# Ready only after current exact-head gate and all publication evidence passed.
after=get_pr(788);assert after["head"]["sha"]==p["head"]["sha"]and after["state"]=="open"
if after["draft"]:
 out2=subprocess.run(["gh","pr","ready","788"],cwd=R,capture_output=True,text=True)
 (M/"PR_READY_STDOUT.txt").write_text(out2.stdout);(M/"PR_READY_STDERR.txt").write_text(out2.stderr)
 if out2.returncode:raise RuntimeError(out2.stderr or out2.stdout)
(M/"PR_READY_GATE.json").write_text(json.dumps({"utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),"result":"PASS","before":p,"after":get_pr(788),"title":title,"DOI":g["publication_DOI"]},indent=2)+"\n")
print(json.dumps({"result":"PASS","ready":True,"head":p["head"]["sha"],"doi":g["publication_DOI"]}))
