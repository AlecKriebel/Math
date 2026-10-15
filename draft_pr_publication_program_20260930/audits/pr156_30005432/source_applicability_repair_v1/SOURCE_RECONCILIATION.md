# Reconciliation with the neighboring finiteness statements

Repair version 1, recorded 2026-10-12 UTC. This supplements the unchanged original PR156 proof; the original submitted files remain preserved separately.

## Literal statement and surrounding discussion

The unrestricted ideal question is Colazzo's Question 1 in OWR 9/2023, printed p.543. No finite-brace, two-sidedness or global property-(S) hypothesis is imposed on that question. CFT's published Definition 3.7 uses exactly the two indices evaluated in our counterexample; Proposition 3.10 proves a positive result for two-sided braces.

On printed p.177 the published CFT paper introduces a discussion of braces with property (S), meaning that every element has property (s). Its Lemma 3.12 on p.178 restarts with an explicit hypothesis about finitely many **additive** generators with property (s). These two observations must be distinguished: the surrounding discussion supplies a restricted context, but it does not justify a categorical assertion about the authors' intended standing hypotheses.

Our additive generators r=(1,0), x=(0,1) both have property (s), whereas (0,2) does not. They generate only Z × {0,1} multiplicatively. Thus the brace is a counterexample to the lemma's isolated unrestricted wording, while the global-(S) conclusion is valid with a separate proof below. We do not describe this as a contradiction to every contextual application in CFT.

Ferudun's later note, version 1.1, Remark 8.2, reports that M. Trombetti intended generators of both group structures. This is a report attributed to that note, not an independently verified communication obtained by this project. No external author contact was conducted.

## Exact displayed-map obstruction

Here ker(lambda)=Z × {0}, the multiplicative center is {0} × {0,1}, and Ann(B)=ker(lambda) intersection Z(B,+) intersection Z(B,circle)=0. For every b=(n,0), all four star products b*r, r*b, b*x, x*b vanish; additive commutators vanish as well. Consequently the displayed finite-data map at the additive generators r,x identifies all these different annihilator cosets.

Being fixed by the lambda maps at additive generators does not imply being fixed by every lambda map: lambda is a homomorphism of the multiplicative group. In particular lambda_(0,2)(n,0)=(-n,0).

The same map obstruction survives in the finite twelve-element brace B3=(Z/3) × (Z/4) with the same formulas. It has global property (S), trivial annihilator, and a noninjective displayed map: b=(1,0) and b=0 have equal recorded values. Therefore that particular injectivity argument is not rescued merely by global (S). This is a defect of the displayed proof certificate, **not a counterexample to the finite-annihilator conclusion**: B3/Ann(B3) is finite.

The independent source reviewer verified the finite example with explicit failures that remain active in ordinary and optimized Python. A corrupted annihilator claim fails in both modes.

## Distinction from JKVV's full theorem

Theorem 5.4 in Jespers–Kubat–Van Antwerpen–Vendramin, arXiv:2001.10967v1, assumes in its converse that the whole star-generated additive subgroup B^(2) and the additive commutator subgroup are finite, together with finite additive generation. Its full converse proof in the available author version was read. The journal-layout version was not independently compared in this audit.

For the infinite counterexample B^(2)=2Z × {0,2}, which is infinite, and [B,B]_+=0. Hence this brace does not satisfy the converse premises and is not a counterexample to the theorem. The finite B3 meets those premises but also meets the conclusion; it isolates the map-injectivity issue rather than falsifying the theorem.

## A separate finite-index proof under global (S)

Let a skew brace B have global property (S) and additive generators x1,...,xr. The orbit of each xi under lambda is finite, so lambda(B) is finite: an additive automorphism is determined by its values on the generators. Choose a1,...,am representing all these lambda maps. The common fixed subgroup F=intersection Fixr(aj) has finite additive index, because every aj has property (s).

The additive center Z=intersection Cadd(xi) also has finite additive index. Put K=ker(lambda). It is an additive subgroup: on K, addition and multiplication agree. Moreover K+b=K circle b for every b, so its additive index equals its finite multiplicative index |lambda(B)|. Thus K intersection F intersection Z has finite additive index.

For k in K intersection Z, k circle b=k+b, while b circle k=b+lambda_b(k). Hence k is multiplicatively central exactly when k belongs to F. Therefore Ann(B)=K intersection F intersection Z, and B/Ann(B) is finite. This proof supplies the context-restricted conclusion independently of the defective displayed map.

## Verification and priority boundary

The infinite brace construction, exact subgroup/coset proof, and original mathematical claim require no substantive change. The original assertion-based checker was replaced in repaired_diagnostics_v1 by explicit raised failures, with the same 33,512 successful controls and meaningful rejected mutants in both modes. Finite controls supplement the proof and do not replace the all-integer argument.

This note is a source-applicability repair, not a novel claimed theorem or a claim to have recertified every result in the cited papers. Priority is audited separately. The later matching example and its dates are recorded in root_priority_overlap/TIMELINE_RECEIPT.json.

