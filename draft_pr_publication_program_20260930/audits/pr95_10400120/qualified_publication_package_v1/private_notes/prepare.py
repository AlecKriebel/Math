from pathlib import Path
import json,hashlib,datetime
P=Path("/Users/alec/Documents/Math/draft_pr_publication_program_20260930/audits/pr85_30001203/isolated_main_integration_20261005/checkout/draft_pr_publication_program_20260930/audits/pr95_10400120/qualified_publication_package_v1"); A=Path("/Users/alec/Documents/Math/draft_pr_publication_program_20260930/audits/pr85_30001203/isolated_main_integration_20261005/checkout/draft_pr_publication_program_20260930/audits/pr95_10400120")
F=P/"publicfiles"; V=F/"verification"; N=P/"private_notes"
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def dump(p,x):p.write_text(json.dumps(x,indent=2,sort_keys=True)+"\n",encoding="utf-8")
title="An explicit SU(5) lens-space counterexample to the printed Guadagnini-Pilo conjecture"
inputs=[]
for rel in [
 "ROOT_MATHEMATICAL_GATE_20261005.json","PRIORITY_STATUS.md","ROOT_PRIORITY_DISPOSITION_20261005.json",
 "ROOT_PRIORITY_FOLLOWUP_ADJUDICATION_20261005.json","ROOT_PRIORITY_LATER_SOURCE_SCOPES_20261005.json",
 "quantum_source_normalization_adversary_20261005/REPORT.md",
 "quantum_source_normalization_adversary_20261005/NORMALIZATION_DERIVATION.md",
 "root_lattice_topology_adversary_20261005/REPORT.md",
 "root_lattice_topology_adversary_20261005/INDEPENDENT_DERIVATION.md",
 "cyclotomic_reproduction_adversary_20261005/REPORT.md",
 "priority_later_version_followup_20261005/REPORT.md","priority_conjecture_history_20261005/REPORT.md",
 "repaired_certificate_sources_20261005/README.md","repaired_certificate_sources_20261005/PREPARATION_MANIFEST.json"]:
 q=A/rel;inputs.append({"file":rel,"bytes":q.stat().st_size,"sha256":sha(q)})
dump(N/"INPUTS.json",{"UTC":datetime.datetime.now(datetime.timezone.utc).isoformat(),"source_head":"6534ad01e519c719628a18984b108e73cf2e8ead","inputs":inputs})
sources=[]
for name,rel,changes in [
 ("verify.py","repaired_certificate_sources_20261005/verify.py","Artifact hash now identifies pr95_note.tex using script-relative path; exact arithmetic and targets unchanged."),
 ("independent_checks.py","repaired_certificate_sources_20261005/independent_review/independent_checks.py","Copied repaired explicit-guard certificate unchanged."),
 ("root_lattice_check.py","root_lattice_topology_adversary_20261005/root_lattice_check.py","Copied fresh stdlib certificate; comment points to public note instead of private derivation.")]:
 q=A/rel;text=q.read_text(encoding="utf-8")
 if name=="verify.py":
  old="Path('COUNTEREXAMPLE.md').read_bytes()"
  if text.count(old)!=1:raise RuntimeError("author binding anchor")
  text=text.replace(old,"(Path(__file__).resolve().parent.parent / 'pr95_note.tex').read_bytes()")
 if name=="root_lattice_check.py":text=text.replace("INDEPENDENT_DERIVATION.md","pr95_note.tex")
 out=V/name;out.write_text(text,encoding="utf-8")
 sources.append({"file":name,"prepared_input_sha256":sha(q),"public_source_sha256":sha(out),"adaptation":changes})
dump(V/"SOURCE_PROVENANCE.json",{"schema":"pr95-public-source-provenance/v1","source_head":"6534ad01e519c719628a18984b108e73cf2e8ead","source_problem":"10400120 / AMR-103-0120","original_author_effort":"2/5","new_central_proof_search_turns":0,"sources":sources,
 "original_author_code_sha256":"608b10d88b1c57a05a230dd7b4ed954e6cc3305d810ccc804bd58754bcfebf1b",
 "original_historical_checker_sha256":"2267d374524bfc77380d736b1cb45a6d66c48130e53152909e5b0406dd84b980",
 "repairs":"Removable assert statements replaced by explicit conditional exceptions; corrected squared/unsquared sine-product comment. All exact target computations unchanged.",
 "limits":"Input hashes identify bytes, not independent proof or priority. No original archives or third-party primary PDFs redistributed."})
(F/"LICENSE.txt").write_text("""Copyright 2026 Alec Kriebel.

The original manuscript, verification code, results and authored documentation in this package are licensed under the Creative Commons Attribution 4.0 International license (CC BY 4.0).

License text: https://creativecommons.org/licenses/by/4.0/legalcode
License summary: https://creativecommons.org/licenses/by/4.0/

Attribution should identify Alec Kriebel and the research note "An explicit SU(5) lens-space counterexample to the printed Guadagnini-Pilo conjecture", link to the published record when available, link to the license, and indicate modifications.

Cited third-party papers and software retain their own licenses and are not redistributed in this package.
""",encoding="utf-8")
(F/"README.md").write_text("""# An explicit SU(5) lens-space counterexample to the printed Guadagnini-Pilo conjecture

Alec Kriebel, independent researcher. [ORCID 0009-0001-9320-500X](https://orcid.org/0009-0001-9320-500X). Research note, 2026-10-05.

In full ordinary SU(5), WZW level 5 and shifted level 10, the S3-normalized squared magnitudes are 3475 + 1550 sqrt(5) for L(5,1) and 4025 + 1800 sqrt(5) for L(5,2). Both are positive; both fundamental groups are Z/5. This contradicts Conjecture 7.5 as printed on p.474 of Ohtsuki's collection (volume nominally 2002, published 1 June 2004), conditional on established RT/modular-category and Hansen-Takata formula inputs.

Historical priority remains unresolved. Takahito Kuriya's directly relevant preprint, The LMO invariant and the Guadagnini-Pilo conjecture for lens spaces, could not be obtained. We cannot establish that it does not already contain or circumscribe this result. No firstness, exhaustive novelty clearance or new historical resolution is claimed. See PR95_PRIORITY_QUALIFICATION.md.

## Files

- pr95_note.pdf: research note.
- pr95_note.tex: standalone LaTeX source and embedded bibliography.
- pr95_support.zip: source, authored support, exact programs, provenance and actual recorded runs.
- PR95_PRIORITY_QUALIFICATION.md: priority and source-read boundaries.
- README.md, LICENSE.txt, SHA256SUMS.txt: instructions, license and digests.

## Reproduction

Verify the separately trusted archive digest, extract the ZIP into a fresh directory, then run from its root:

    python3 -E -B verification/run_all.py --output-dir /a/new/empty/directory

Use Python 3.9+ with NumPy installed for the full modular-word route. The two root-lattice programs use only the standard library and may be run separately:

    python3 -E -B verification/independent_checks.py
    python3 -E -B verification/root_lattice_check.py

The runner performs the full payload hash guard, then six fresh positive processes (three routes in normal and optimized modes) and six false arithmetic targets which must fail. Output must be outside the supplied package and empty/absent. It records argv, actual PIDs, UTC times, sanitized Python environment, versions, source snapshots/hashes, exits and full streams. Stored successes are historical evidence, never proof that a new invocation passed. See verification/VERIFY_README.md.

The analytic proof has an exact five-survivor table. The full-weight computation enumerates 126 labels, 120 permutations and 8,001 symmetric entries with seven final polynomial identities. The historical root-lattice field exact_assertions=2005 counts explicit finite checks, not a quality score or distinct theorems. Repeating under -O does not double mathematical evidence. Fresh lattice output includes explicitly diagnostic floating fields; exact identities and positivity do not depend on them.

## Assistance and review

AI tools were used extensively in solving, drafting, literature comparison, reproduction and adversarial validation. The work is unrefereed and has not undergone conventional human peer review. No global historical priority or publication clearance follows from the certificate suite.

The LaTeX source uses standard article/AMS/geometry/booktabs/lmodern/microtype/hyperref packages. Cited source PDFs, extracted texts, source-page images, private audit receipts and credentials are excluded.
""",encoding="utf-8")
(F/"PR95_PRIORITY_QUALIFICATION.md").write_text("""# PR95: historical priority unresolved

The note gives a verified exact counterexample to the broad nonzero-magnitude statement printed as Ohtsuki Conjecture 7.5, p.474. It does not claim the first counterexample, exhaustive novelty clearance, a newly resolved historical problem, continuous openness, or originality of the underlying RT formulas.

The collection is Geometry & Topology Monographs 4, nominally 2002, actually published 1 June 2004. The conjecture is attributed to Guadagnini and Pilo, Three-manifold invariants and their relation with the fundamental group, CMP 192 (1998), 47-65, DOI [10.1007/s002200050290](https://doi.org/10.1007/s002200050290). The available [1996 preprint v1](https://arxiv.org/abs/hep-th/9612090v1) gives the broad setting and its SU(2) lens-space theorem; the final journal full text was not compared.

## Direct missing source

Takahito Kuriya, The LMO invariant and the Guadagnini-Pilo conjecture for lens spaces, is listed as a preprint by his [Kyushu institutional record](https://www2.math.kyushu-u.ac.jp/coe/staff/staff_sub/kuriya.html), cited in the [2004 Topology Symposium proceedings](https://www.mathsoc.jp/~topology/topsymp/kouenshu/ts2004all.pdf), printed p.54 reference [12], and associated with an exact-title talk on 21 February 2003 in a [Kyushu report](https://www2.math.kyushu-u.ac.jp/coe/report/pdf3/report-6.pdf), printed p.121. No verified DOI or journal publication is asserted for it.

Its full text, complete conclusions and hypotheses could not be obtained. We cannot establish that it does not already contain or circumscribe this result. Its title, public author record, an unverified aggregator abstract and later perturbative results cannot supply the missing finite-level comparison. No inference about its original language is made. This is the decisive reason priority remains unresolved.

## Bounded comparisons and boundaries

The proof input is [Hansen-Takata arXiv:math/0209403v2](https://arxiv.org/abs/math/0209403v2), Eq.(12), Sections 4-5 and Theorem 5.1. The journal publication is JKTR 13(5) (2004), 617-668, DOI [10.1142/S0218216504003342](https://doi.org/10.1142/S0218216504003342); its final full text and possible later corrections were not obtained. The note identifies the actual preprint formula source.

The history audit examined selected primary passages of Kuriya's 2008 On the LMO conjecture, Kuriya-Le-Ohtsuki 2012, Guadagnini-Mancarella 2010, Hikami 2005/2006, Ionicioiu-Williams 1998, Garoufalidis-Le-Marino 2008 and Oriti's 2003 thesis. It authenticated no earlier qualifying pair in those passages. Perturbative recovery, equal-magnitude complex-value separation and rank-one tests do not alone answer this finite-level full SU(5) comparison. These are bounded read outcomes, not absence theorems.

Later selected reads included [Gang arXiv:0912.4664v2](https://arxiv.org/abs/0912.4664v2), [Kubo-Yokoyama arXiv:2108.09300v2](https://arxiv.org/abs/2108.09300v2) and the [final JHEP article](https://doi.org/10.1007/JHEP04(2022)074). Gang's final pagination is 1119-1128, JKPS 74 (2019), DOI [10.3938/jkps.74.1119](https://doi.org/10.3938/jkps.74.1119); its final full text remains unread. The selected general-q localization formula is U(N) and retains a sector-sign assumption, so no full ordinary SU(N) conclusion was inferred from it.

Kubo-Yokoyama's later ordinary SU(N) WZNW comparison is explicitly spin-independent; proposed background fields are distinguished from spin dependence. A relative phase discrepancy can vanish for even shifted coupling. The selected lens models and tables have q=1 and do not authenticate an earlier same-theory pair L(5,1), L(5,2). No blanket dismissal of all SU(N) expressions as spin invariants is warranted.

A bounded check of Hansen-Takata's older sl4 lens-space remark found equal nonzero magnitudes in four exact reconstructions, leaving a discrepancy with its printed complex-separation statement. It remains an unresolved source discrepancy, neither a proved historical erratum nor evidence of firstness; it is unnecessary for the present proof.

Unread or access-limited sources include Sokolov 1997, Takata 1996 projective-category full text, a reliably readable complete Zhang-Carey 1996 source, Yamada 1995, the final HT article, Gang final text and unexamined portions of the later works. Bibliographies and searches are not exhaustive.

No individual was contacted and no outreach was prepared. Extensive AI assistance and absence of conventional human peer review are disclosed. The publication qualification permits reporting the checkable result with unresolved priority; it does not resolve the missing source.
""",encoding="utf-8")
(V/"VERIFY_README.md").write_text("""# PR95 exact reproduction

The tested runtime is CPython 3.12.14 with NumPy 2.3.5. Python 3.9+ syntax is intended; other runtimes need fresh execution. The two lattice programs need only the standard library. NumPy arrays in verify.py hold arbitrary-precision Python integers with object dtype; certificate arithmetic is exact.

From the clean extracted archive root:

    python3 -E -B verification/run_all.py --output-dir /a/new/empty/directory

Output must be absent/empty and outside the archive root. Every run is fresh. First the runner verifies every member in PAYLOAD_MANIFEST.json and rejects missing, linked, changed or unsafe paths. It runs all three programs normally and with -O, then arithmetic false-target copies in both modes. Each false target must raise an explicit exception, exit nonzero, emit no success stdout, and create no author success JSON.

Child flags are -E -B, plus -O for optimized runs. PYTHON* variables are removed and LC_ALL=C set. Complete records capture input snapshots, argv, actual PID, UTC start/end, Python/NumPy versions, exit and full streams. Inspect a fresh exit/status; included earlier results cannot establish a new pass.

## Mechanisms

1. verify.py: original full 126-label modular-word computation, repaired guards and artifact binding to pr95_note.tex. Exact coefficient targets are unchanged. It writes verification.json in the child's fresh output directory.
2. independent_checks.py: earlier distinct root-lattice route in Z[zeta10], explicit guards and corrected sine-product comment. Historical field exact_assertions=2005 counts finite explicit checks.
3. root_lattice_check.py: fresh independent reconstruction in Z[zeta50], 625 representatives and 120 Weyl permutations, q=1,2,3,4,6,7,-1,-2, exact orientation/inverse/periodicity/S3 controls. Floating fields are diagnostics only.

The lattice programs separately implement the same published theorem; they are not independent foundation proofs. The full modular-word route is a distinct finite mechanism. The manuscript table can be checked by hand.

SOURCE_PROVENANCE.json identifies authenticated original and repaired/public sources. recorded_results.json and recorded_processes/ preserve actual initial assembly executions as historical results. The final clean-extraction run is separately retained in private preparation evidence, leaving archive bytes fixed.

The payload manifest excludes itself to avoid recursive hashing. The external SHA256SUMS includes the ZIP: establish a trusted archive digest first. A mutable manifest alone cannot authenticate authorship or protect against simultaneous replacement of manifest and payload. Hashes identify bytes, not proof correctness, novelty, priority, peer review or release authority.

Ordinary full modular-category and RT/Hansen-Takata surgery results are imported inputs. No copyrighted source PDFs, extracted texts, source-page images, private source-audit receipts, raw retrieval headers or credentials are included.
""",encoding="utf-8")
support=["pr95_note.tex","README.md","LICENSE.txt","PR95_PRIORITY_QUALIFICATION.md"]+["verification/"+n for n in ["VERIFY_README.md","SOURCE_PROVENANCE.json","run_all.py","verify.py","independent_checks.py","root_lattice_check.py"]]
dump(F/"PAYLOAD_MANIFEST.json",{"schema":"pr95-support-payload/v1","files":[{"file":s,"bytes":(F/s).stat().st_size,"sha256":sha(F/s)} for s in sorted(support)],"hash_scope":"Every support archive member except this manifest; authenticate external ZIP digest."})
meta={"title":title,"upload_type":"publication","publication_type":"preprint",
 "description":"<p>For the ordinary full SU(5) Reshetikhin-Turaev invariant at WZW level 5, shifted level 10, L(5,1) and L(5,2) have fundamental group Z/5 but unequal nonzero magnitudes. With S3 normalization equal to one, their squared magnitudes are 3475 + 1550 sqrt(5) and 4025 + 1800 sqrt(5). An exact A4 root-lattice reduction and reproducible cyclotomic certificates establish this counterexample to Conjecture 7.5 as printed on p.474 of Ohtsuki's collection (volume nominally 2002, published 1 June 2004), conditional on established full modular-category and RT/Hansen-Takata surgery inputs.</p><p>Historical priority remains unresolved. Takahito Kuriya's directly relevant preprint, The LMO invariant and the Guadagnini-Pilo conjecture for lens spaces, could not be obtained. We cannot establish that it does not already contain or circumscribe this result. No first counterexample, exhaustive novelty clearance, current global open status or new historical resolution is claimed. Bounded source comparisons and their limitations are documented.</p><p>AI tools were used extensively in solving, drafting, literature comparison, reproduction and adversarial verification. This is an unrefereed research note without conventional human peer review. The package includes PDF, LaTeX source, a manifest-bound portable archive with exact programs and actual recorded runs, priority qualification, instructions, license and digests. Checks remain active under optimized Python, and false arithmetic targets must be rejected. Floating fields are diagnostics only; counts are algorithmic counts, not quality claims. No general category reconstruction or priority certification is asserted.</p>",
 "creators":[{"name":"Kriebel, Alec","affiliation":"Independent researcher","orcid":"0009-0001-9320-500X"}],
 "publication_date":"2026-10-05","version":"1.0","access_right":"open","license":"cc-by-4.0",
 "keywords":["Reshetikhin-Turaev invariant","SU(5)","lens spaces","Guadagnini-Pilo conjecture","Ohtsuki Conjecture 7.5","cyclotomic certificate","root lattice"],
 "related_identifiers":[{"identifier":s,"relation":"references","scheme":scheme} for s,scheme in
 [("10.1007/s002200050290","doi"),("10.1142/S0218216504003342","doi"),("https://arxiv.org/abs/math/0209403v2","url"),("https://msp.org/gtm/2002/04/gtm-2002-04-024s.pdf","url"),("https://www2.math.kyushu-u.ac.jp/coe/staff/staff_sub/kuriya.html","url")]]}
deposit_files=["pr95_note.pdf","pr95_note.tex","pr95_support.zip","PR95_PRIORITY_QUALIFICATION.md","README.md","LICENSE.txt","SHA256SUMS.txt"]
dump(P/"zenodo-deposit.json",{"metadata":meta,"files":[{"path":"publicfiles/"+s} for s in deposit_files]})
dump(N/"PUBLICATION_SOURCE_METADATA.json",{"schema":"pr95-qualified-publication-inputs/v1","source_head":"6534ad01e519c719628a18984b108e73cf2e8ead","problem":"10400120 / AMR-103-0120","original_author_effort":"2/5","new_central_proof_search_turns":0,"qualifications":{"historical_priority":"unresolved; directly relevant Kuriya full text unavailable","novel_firstness_claim":False,"human_peer_review":False,"publication_clearance":False},"metadata_sha256":sha(P/"zenodo-deposit.json"),"metadata":meta,"support_members":support})
(N/"RESEARCH_LOG.md").write_text("# PR95 qualified package preparation log\n\n"+datetime.datetime.now(datetime.timezone.utc).isoformat()+" - Inputs read and hashed; narrow theorem and missing Kuriya text recorded. Note authored; built-in compilation succeeded. Explicit-guard code copied/adapted without mathematics changes. Preparation completion estimate: 55%; mathematical specialization 100%; historical priority unresolved; publication clearance false. Zero new central proof-search turns. No outside contact or Git/service/UI mutation.\n",encoding="utf-8")
print(json.dumps({"prepared":str(P),"members":len(support),"priority":"unresolved","publication_clearance":False}))
