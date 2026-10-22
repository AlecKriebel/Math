# Independent original-question scope freeze

Checkpoint: 2026-10-17 21:06:18 UTC. Source-scope preparation: 100% complete. PR mathematical audit: 0% performed by this agent. These percentages describe distinct tasks; no estimate of the problem's ultimate solvability is asserted.

## Independence and custody

This report was formed before reading any PR artifact, submitted proof, prior audit, counterexample, or submitted script. No such material was read or executed. No local Git command, provider mutation, publication action, or outreach was performed. The next stage requires Root's frozen artifact packet. This is a scope interpretation, not acceptance or rejection of any PR mathematics or a priority assessment.

The sole mathematical source consulted was Roser Homs (joint with Olga Kuznetsova), *Weak maximum likelihood threshold of colored Gaussian graphical models*, in Oberwolfach Report 55/2022, DOI 10.4171/OWR/2022/55, printed pp. 3146-3149. Official URL: https://ems.press/content/serial-article-files/46992?nt=1 . No cited paper or later work was consulted.

Actual reading: all four complete pages were extracted and inspected as rendered pixels, not merely search excerpts. The PDF's zero-based pages 25-28 correspond to one-based PDF pages 26-29. The web PDF text was read around the contribution; web screenshot attempts returned text-only/error output and do not count as visual evidence. The official PDF was therefore downloaded into an external temporary cache, rendered with Poppler at 130 dpi, and all four resulting whole-page images were opened with `view_image`. Neighboring contributions visible at the top of p.3146 and bottom of p.3149 were inspected only as page context; their mathematics is not used here.

Cached source: `/tmp/pr212_original_source_scope_01/OWR-2022-55.pdf`; SHA256 `56e4555409c330099d6ff15cdda3f8b3d5415af067c1800b0aac846ca5701b65`. Rendered images: `/tmp/pr212_original_source_scope_01/page-26.png` through `page-29.png`. These third-party bytes and renderings are outside this authored report folder and outside its proposed public selection.

## Mathematical object to freeze

Write m=|V|. The model is a real linear concentration model associated with an undirected graph G=(V,E), together with a partition V=V_1 disjoint-union ... disjoint-union V_r and a separate partition E=E_1 disjoint-union ... disjoint-union E_s. Its concentration matrices K are positive definite, vanish on missing off-diagonal edges, have equal diagonal entries within each V_i, and have equal edge entries within each E_j. The source does not impose graph-automorphism, equitable-coloring, or nontrivial-color-class conditions.

A partition may consist of singleton blocks. Consequently the ordinary uncolored graphical model is included by assigning each vertex and each present edge its own color; mixed singleton/nonsingleton partitions are also included. Identical color names across the two partitions do not identify diagonal with off-diagonal parameters. The constraints concern concentration entries, not equality of covariance entries or correlations. A candidate outside the usual finite simple undirected graph convention would need an explicit scope justification; loops and multiple edges are not discussed.

For a symmetric matrix S define the report's linear map exactly by

    pi_G(S) = ( sum_{a in V_i} S_aa )_{i=1}^r
              concatenated with ( sum_{ab in E_j} S_ab )_{j=1}^s.

There is no factor 2 in the source's edge-statistic coordinates. A different trace-pairing convention can be equivalent only after an explicit consistent invertible coordinate rescaling.

Let

    C_G = pi_G(SPD_m).

This is the real open cone used for MLE existence. For any PSD sample covariance S, the report gives

    MLE exists uniquely <=> pi_G(S) belongs to C_G
                         <=> there is S0 in SPD_m with pi_G(S0)=pi_G(S).

The second formulation is a positive-definite completion of the sufficient statistics; it is not necessarily an entrywise completion when colors combine entries.

Let T=(t_1,...,t_{r+s}) and U=(u_ab) be a symmetric m-by-m matrix of independent indeterminates. In the real polynomial ring R[U,T], define

    J_(G,n) = < T-pi_G(U), all (n+1)-minors of U >,
    I_(G,n) = J_(G,n) intersection R[T].

No PSD inequality is in this ideal. Its variety is an algebraic closure object, not by definition the actual projected PSD rank-at-most-n set. In particular, a real point of V_R(I_(G,n)) cannot be silently assumed to have a real PSD rank-at-most-n preimage. A complex point is insufficient for the real cone intersection.

## Thresholds and the adjacent-rank hypothesis

Use p_k(G) for the probability of MLE existence with the report's k observations. Then the meanings are

    WMLT(G) = min { k : p_k(G)>0 },
    MLT(G)  = min { k : p_k(G)=1 }.

The report's rank/observation parameter is k; it does not explicitly describe mean estimation. A later proof must state its sampling convention and must not silently replace k by k-1. For the present freeze, k follows the source's rank-based observation convention. Positive integers are the natural observation scope; n=0 is not expressly treated and must be identified if used.

Proposition 3 assumes the adjacent elimination transition

    H(G,n): I_(G,n+1)=(0) and I_(G,n)=<f_1,...,f_u> != (0).

Thus a proposed example must verify this exact transition, not just I_(G,n) nonzero or an upper bound on MLT. For n>=m the ideal is zero because the rank condition is vacuous, so a nonzero case has n<m.

Theorem 2 supplies only the implication I_(G,k)=(0) => p_k(G)=1. Its converse is not stated here. From H alone, using the stated theorem, one obtains MLT(G)<=n+1; equalities and lower bounds require more than that one implication.

## Proposition 3 and two levels of the conjecture

Let D_m be the set of real lower-triangular m-by-m matrices L with every diagonal entry positive. These parametrize full-rank positive-definite S0=LL^T. Set

    F_f(L) = f(pi_G(LL^T)).

The L in this test is a full-rank Cholesky factor for positive-definite matrices; it is not a positive-diagonal parametrization of rank-n matrices when n<m.

For a fixed generating list define A_list(G,n) by: some f_i has a sign epsilon in {+1,-1} and real polynomials q_1,...,q_v with

    epsilon F_(f_i)(L) = sum_a q_a(L)^2

as a polynomial identity, and that sum is strictly positive at every L in D_m. Define the intrinsic existential version A_ideal(G,n) by the same requirement for some f in I_(G,n). Define

    B(G,n): C_G intersection V_R(I_(G,n)) is nonempty
          <=> there is S0 in SPD_m with all f_i(pi_G(S0))=0.

The source's first antecedent is described as a "non-vanishing (possibly negative) sum of squares". The worked example uses positive Cholesky diagonal entries to ensure strict nonvanishing on D_m. The reliable reading is nowhere zero on D_m, not merely a polynomial that is not identically zero. The SOS identity is a polynomial identity; the report gives no permission to replace it by rational SOS, a constrained Positivstellensatz identity, multiplication by auxiliary factors, or numerical positivity alone.

Under H, the source attaches these numerical conclusions:

    A_list => WMLT=MLT=n+1;
    B      => WMLT=n and MLT=n+1.

The source then states Conjecture 4 verbatim: "The two cases in Proposition 3 are the only possible scenarios."

This leaves two related but distinct readings to audit:

1. Boolean/certificate exhaustion: under H, A or B always holds. For a choice-independent interpretation, A=A_ideal; any ideal element can be appended to a generating list. For a literal fixed-list interpretation, A=A_list. The report supplies neither a canonical generating list nor an explicit quantifier over all lists. This distinction must remain visible.
2. Numerical classification: under H, MLT=n+1 and WMLT is either n or n+1. This is what the two stated conclusions would jointly exhaust if Proposition 3 is valid in the intended scope.

The first numerical conclusion forces p_n=0; the second forces 0<p_n<1, together with zero positive-existence probability at every smaller sample size. Neither threshold pattern specifies the exact value of an intermediate probability. The numerical statement alone does not prove existence of a polynomial SOS certificate. Conversely, a proof of Boolean exhaustion does not independently validate the numerical implication attached to B. An audit must say which statement it resolves.

## Deductions and exact logical hazards

The following are my independent deductions from the frozen definitions, rather than extra assertions attributed to the source.

* A_ideal and B are incompatible: if S0 is positive definite, its Cholesky factor belongs to D_m, so the certified f is nonzero at pi_G(S0); this precludes that point from the ideal's real variety. Therefore Boolean exhaustion amounts to proving that failure of B forces a strict signed SOS pullback certificate. Merely observing A=>not B proves only disjointness.
* Define P_n=pi_G({XX^T:X in R^(m by n)}). Then P_n is contained in V_R(I_(G,n)). The relevant actual-data event is P_n intersection C_G nonempty. In general algebraic closure membership alone is weaker than belonging to P_n.
* Under the usual nondegenerate Gaussian full-support data law, P_n intersection C_G nonempty is equivalent to p_n>0: the inverse image of the open cone under X->pi_G(XX^T) is open; a single witness gives a nonempty open set and hence positive probability. A lower-rank witness can be padded with zero columns and then perturbed. This reasoning uses an actual PSD factor X, not a formal variety point.
* B therefore requires a further bridge to actual rank-n data before one may infer p_n>0. Even after that bridge, p_n>0 initially establishes WMLT<=n, not equality WMLT=n. MLT=n+1 also requires exclusion of p_n=1. These are proof obligations, not a verdict that the source proposition or any submission is false.
* In contrast, a strict signed-SOS certificate excludes the whole variety from C_G, hence excludes actual rank-at-most-n data from C_G. Together with the elimination criterion at n+1, this establishes the first numerical conclusion.
* Nonnegativity on D_m and being polynomial SOS are different properties. A failure to express one displayed generator as SOS does not rule out another generator or another element of the ideal. A numerical solver's unsuccessful search does not exclude all polynomial degrees or real coefficients.

The source's example uses above-diagonal symbols l_13, l_24, etc., despite the proposition's lower-triangular convention. This is an indexing/convention ambiguity to resolve by a checked identity or transpose renaming if that example is later used; I do not import its displayed expansion as a verified certificate.

## Four-cycle scope

Proposition 3 is stated for G and n under H with no four-cycle qualifier. Conjecture 4 likewise states no explicit restriction on G. The paragraph between them discusses completing four-cycle computations, and the worked figure is a four-cycle. My primary frozen interpretation is the general colored-graph claim under H, with the four-cycle sentence describing an application. A narrower four-cycle-only authorial intention cannot be eliminated from this terse report alone; it must be named as an alternative, not silently substituted.

A proof restricted to four-cycles is consequently partial evidence for the general reading. A counterexample on another graph would address the general reading but would not refute an expressly restricted four-cycle version. A construction in singleton colors remains inside the formally defined general class.

## What counts as a decisive resolution

For every proposed resolution first identify G, its two explicit color partitions, n, the coordinate convention, and exact independently checkable evidence for H. Distinguish a computed subideal from the full elimination ideal. A single nonzero minor relation proves nonzeroness but does not identify all generators; a claimed zero ideal needs an elimination/dominance argument or a validated exact computation.

To prove the Boolean conjecture in the general reading, establish A_ideal or B for every pair satisfying H, with a stated generating-list interpretation. To refute that existential-ideal version, one admissible pair must satisfy H, fail B, and fail every allowed ideal-element strict signed-SOS certificate. Checking a short list of generators or a bounded-degree SOS search is not that last universal negation. For a fixed-list version, pin the exact list before testing its generators and label the narrower result.

To prove the numerical classification, independently justify the threshold equalities, including all smaller-sample lower bounds and failure of almost-sure existence at n. To refute it, a verified inequality contradicting one equality is sufficient; complete numerical threshold computation is not always necessary. Such a refutation of the numerical implication attached to B does not by itself refute Boolean A-or-B if B actually holds.

Exact symbolic certificates, complete quantified arguments, validated positivity/PD infeasibility proofs, and reproducible exact elimination computations can be decisive. Floating-point eigenvalues near zero, generic random sampling, approximate variety membership, a complex lift without a real PSD lift, or empirical MLE frequencies are partial evidence unless upgraded to appropriate certificates.

## Outstanding uncertainty and handoff

Unresolved from the single source: fixed generating list versus existential ideal element; the precise formal meaning of nonvanishing; the unstated observation/mean convention; the narrow possible four-cycle intention; and the Cholesky indexing mismatch. The selected operational interpretations above are explicit and can be revisited only with new primary evidence. No historical-priority reading or submitted mathematics has contaminated this freeze. Await Root's frozen artifact packet before any PR mathematical audit.
