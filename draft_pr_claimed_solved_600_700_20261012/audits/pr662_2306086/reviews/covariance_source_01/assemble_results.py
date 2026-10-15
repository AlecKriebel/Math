#!/usr/bin/env python3
"""Assemble review metadata from already completed exact and numerical replays."""
from collections import Counter
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path

HERE=Path(__file__).resolve().parent
AUDIT=HERE.parents[1]


def data(name):
    return json.loads((HERE/name).read_text())


def identity(path):
    body=path.read_bytes()
    return {"bytes":len(body),"sha256":hashlib.sha256(body).hexdigest()}


normal=data("independent_controls.normal.json")
optimized=data("independent_controls.optimized.json")
if normal != optimized:
    raise ValueError("exact ordinary/optimized outputs differ")
pairs=(("publication.normal.json","publication.optimized.json"),
       ("publication.numerical.normal.json","publication.numerical.optimized.json"),
       ("numerical_detail.normal.json","numerical_detail.optimized.json"),
       ("independent_numerical.normal.json","independent_numerical.optimized.json"))
for ordinary,optimized_name in pairs:
    if data(ordinary)!=data(optimized_name):
        raise ValueError("ordinary/optimized outputs differ: "+ordinary)
publication=data("publication.normal.json")
numeric_publication=data("publication.numerical.normal.json")
num=data("numerical_detail.normal.json")
indnum=data("independent_numerical.normal.json")
snapshot=json.loads((AUDIT/"SCOPE_AND_SNAPSHOT.json").read_text())
now=datetime.now(timezone.utc).isoformat()
pdf=HERE/"tmp/1809.07200v2.pdf"
source={
    "schema":"independent-source-binding-v1",
    "review":"covariance_source_01",
    "recorded_utc":now,
    "native_head":snapshot["original_head"],
    "source":{
        "title":"Research Problems in Function Theory (New Edition)",
        "authors":["Walter K. Hayman","Eleanor F. Lingham"],
        "arxiv":"1809.07200v2",
        "revision_utc":"2018-09-21T13:10:21Z",
        "record_url":"https://arxiv.org/abs/1809.07200v2",
        "pdf_url":"https://arxiv.org/pdf/1809.07200v2",
        "retrieved_date_utc":"2026-10-15",
        "retrieved_file_mtime_utc":datetime.fromtimestamp(pdf.stat().st_mtime, timezone.utc).isoformat(),
        "retrieval":"Successful curl --fail --location; separately opened PDF and versioned landing page through web tool",
        "pdf":identity(pdf),
        "pages_total":256,
        "full_source_copy":"tmp/1809.07200v2.pdf (git-ignored review-local temporary input)",
        "complete_relevant_pages_visually_inspected":True,
        "pages":[
            {"printed":114,"pdf_page_one_based":115,"purpose":"Chapter 6 class S normalization and Koebe slit images", "render":identity(HERE/"tmp/printed114.png")},
            {"printed":147,"pdf_page_one_based":148,"purpose":"Complete Problem 6.86, attribution, update, and surrounding problem context", "render":identity(HERE/"tmp/printed147.png")}
        ]
    },
    "source_bindings":[
        {"claim":"S denotes analytic univalent functions f(z)=z+sum(n>=2) a_n z^n in the unit disk", "printed_page":114, "evidence_type":"explicit definition"},
        {"claim":"Problem 6.86 asks whether the displayed inequality improves under real-on-real / real-coefficient restriction at each fixed z0", "printed_page":147,"evidence_type":"explicit fixed-point question"},
        {"claim":"The displayed inequality is |z0 f''(z0)/f'(z0)-2 rho^2/(1-rho^2)| <= 4 rho/(1-rho^2)", "printed_page":147,"evidence_type":"visually checked equation"},
        {"claim":"rho is interpreted as |z0| and analytic normalized univalence is inherited from chapter context", "printed_page":147, "evidence_type":"standard interpretation; target itself does not explicitly redefine rho or repeat S"},
        {"claim":"No explicit request for a sharp formula, numerical epsilon, extremizers, or full variability region occurs in the target", "printed_page":147,"evidence_type":"complete target inspection"},
        {"claim":"The dated update says the statement was restated and records no reported progress", "printed_page":147,"evidence_type":"historical update only; no present openness or priority certification"}
    ],
    "scope_interpretation":{
        "qualitative_fixed_nonreal_uniform_in_f_answer_responsive":True,
        "literal_question_requires_sharp_numeric_formula":False,
        "all_fixed_points_have_strict_improvement":False,
        "real_nonzero_radius_sharp":True,
        "zero_original_expression_degenerate":True,
        "uncomputed_quantitative_gap_is_failure_of_stated_qualitative_theorem":False,
        "current_literature_or_novelty_established":False
    },
    "not_verified":["exhaustive later literature","historical priority","current openness","upstream dataset/report text beyond supplied queue binding","subscription published chapter"]
}
(HERE/"SOURCE_BINDINGS.json").write_text(json.dumps(source,indent=2,sort_keys=True)+"\n")
files=["independent_controls.py","independent_controls.normal.json","independent_controls.optimized.json",
       "independent_numerical.py","independent_numerical.normal.json","independent_numerical.optimized.json",
       "publication.normal.json","publication.optimized.json","publication.numerical.normal.json",
       "publication.numerical.optimized.json","numerical_detail.normal.json","numerical_detail.optimized.json",
       "requirements_numerical.txt"]
summary={
    "schema":"independent-review-test-results-v1","status":"PASS","recorded_utc":now,
    "native_head":snapshot["original_head"],"native_files":len(snapshot["original_blobs"]),
    "core_interpreter":"/Users/alec/Documents/Math/draft_pr_claimed_solved_600_700_20261012/tooling/math-venv/bin/python",
    "python_version":normal["python_version"],"sympy_version":normal["sympy_version"],
    "independent_controls":{"checks":normal["checks"],"by_kind":dict(Counter(c["kind"] for c in normal["details"])),"normal_optimized_identical":True},
    "publication":{"status":publication["status"],"files":publication["files"],"replay":publication["replay"],"negative_controls_rejected":len(publication["publication_negative_controls_rejected"]),"normal_optimized_identical":True},
    "publication_with_numerical":{"status":numeric_publication["status"],"replay":numeric_publication["replay"],"negative_controls_rejected":len(numeric_publication["publication_negative_controls_rejected"]),"normal_optimized_identical":True},
    "supplied_numerical_reproduction":{"checks":num["audit_checks"],"max_absolute_difference":max(r["absolute_difference"] for r in num["numerical"]["records"]),"numpy":num["numerical"]["numpy"],"scipy":num["numerical"]["scipy"],"certified":False,"normal_optimized_identical":True},
    "independent_alternative_state_reproduction":{"records":len(indnum["records"]),"max_absolute_difference":max(r["absolute_difference"] for r in indnum["records"]),"interpreter":indnum["python_executable"],"numpy":indnum["numpy"],"scipy":indnum["scipy"],"certified":False,"normal_optimized_identical":True},
    "archives":normal["archives"],"artifacts":[dict(path=name,**identity(HERE/name)) for name in files],
    "unchanged_native_sha256_verified_after_replay":True,
    "certificate_boundary":"Exact identities and regression replay do not formalize the analytic theorem; floating point agreement does not supply interval lower bounds, global optimality, or optimizer convergence."
}
(HERE/"TEST_RESULTS.json").write_text(json.dumps(summary,indent=2,sort_keys=True)+"\n")
print(json.dumps({"status":"PASS","independent_checks":normal["checks"],
                  "independent_numerical_max_difference":summary["independent_alternative_state_reproduction"]["max_absolute_difference"],
                  "supplied_numerical_max_difference":summary["supplied_numerical_reproduction"]["max_absolute_difference"],
                  "source_pdf":source["source"]["pdf"]},indent=2))
