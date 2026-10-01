# 30001781: five-turn partial result, original unsolved

**Proposed status: unsolved, 5/5 substantive author turns. Independent review pending.**

The exact source is Litvak's contribution to OWR 24/2011, printed pp. 1343–1344. The question asks for the sharp maximal Euclidean submatrix bound when independent centered isotropic log-concave rows need not be coordinatewise unconditional. The correct scale is

    Lambda_(k,m) = sqrt(m) log(3N/m) + sqrt(k) log(3n/k).

The logarithms are outside the radicals. The imported dataset's stronger formula is a transcription error; its elementary exponential-entry counterexample is not a counterexample to the original. No full proof or valid counterexample to the corrected original was obtained.

## Retained claims and where they are proved

1. **Common coisometric images of unconditional rows.** `TURN_1.md` proves the sharp expectation and benchmark additive tail for X_i=T Z_i with one common TT*=I and independent isotropic unconditional log-concave Z_i. D may exceed N and the latent row laws may differ. A rotation example proves the resulting laws can fail coordinate unconditionality. The proof uses the actual published Chevet theorem in latent coordinates, with an explicit lower-dimensional-body limit.

2. **Asymmetric common-weight Dirichlet rows.** `TURN_2.md` proves all-p moments C(Lambda+p), hence the benchmark tail, for isotropic Dirichlet rows with alpha_ij=c_i alpha_j>=1 and a common coisometry determined by the shared weight ratios. The Gamma coupling and conditional Jensen avoid any sample-size restriction. Uniform regular simplices are included. Arbitrary different simplex orientations or weight ratios are not included.

3. **Flat row tests under arbitrary allowed laws.** `TURN_3.md` proves a Bernstein/net estimate for signed flat row coefficients; when their support size is at least m it gives the sharp order for that test class. A harmonic deterministic vector shows that a dimension-free convex-hull replacement of all coefficient profiles by flat vectors is impossible. This is a proof-route obstruction, not a log-concave matrix counterexample.

4. **All coefficient profiles for m=1, and a general elementary net bound.** `TURN_4.md` proves

       P(A_(k,m)>C[sqrt(k)log(3n/k)+m log(5eN/m)+t]) <= 2exp(-t).

   It yields the sharp full one-column case m=1 and any regime where m log(5eN/m) is bounded by a fixed multiple of sqrt(k)log(3n/k). The independent order-statistic lemma covers nonidentical row laws and every nonflat row coefficient profile. The column-net term is too large in general.

5. **Exact k=1 quantile/tail/moment equivalence.** `TURN_5.md` proves that uniform sharp median bounds over all sample sizes for iid maxima of the one-row top-m norm are equivalent, up to constants, to its shifted exponential tail and Lp bound C(sqrt(m)log(3N/m)+p). A precisely stated weak–strong comparison for that norm would suffice, but is only a hypothesis here. Even that conditional one-row result does not establish the full row-coefficient chaining needed for k>1.

All five turns contain mathematical arguments beyond source lookup, bookkeeping or finite tests. No claim of historical novelty is made. The positive partials are credited consequences of published probabilistic tools and elementary reductions, and their separate review is required before publication.

## Known full general-row theorem remains stronger than our general estimates

Adamczak–Latała–Litvak–Pajor–Tomczak-Jaegermann, *Tail estimates for norms of sums of log-concave random vectors*, PLMS 108 (2014), 600–637, Theorem 5.1 in the pinned full author version, proves for arbitrary allowed rows and t>=1

    P(A_(k,m)>=C t lambda_(k,m)) <= exp(-t lambda_(k,m)/sqrt(log(3m))),

where

    lambda_(k,m)=sqrt(loglog(3m))*sqrt(m)*log(e max(N,n)/m)
                  +sqrt(k)*log(en/k).

The general elementary estimates of turns 3–4 are not improvements on that theorem. The restricted classes of turns 1–2 and the exact reductions are the scoped contents of this attempt. The final EJP 2024 comparison paper checked during the source gate also retains unconditionality in the relevant sharp extension. Limited targeted literature checking is not a certification of the present worldwide status of the problem.

## Unclosed gap

We have neither removed the extra general-row factors nor shown that every allowed law admits the common latent/conditional representation used above. Pointwise bounds for projections, dimension-free first moments, central symmetrization, arbitrary-norm Chevet counterexamples, deterministic flat-atomic obstructions and finite controls do not supply that missing general theorem. The original source's qualitative high-probability language is kept distinct from the precise additive-tail benchmark established under unconditionality.

## Reproducibility and provenance

Run `python verify_turn1.py` through `python verify_turn5.py` from any directory. Each uses only the Python standard library and prints a deterministic JSON receipt. The assertion counts are 12,911; 3,374; 30,449; 14,132; and 999. These checks cover exact finite algebra, probability and geometric identities; they do not prove the analytic tail estimates or the unresolved conjecture.

`source_manifest_v2.json` lists the six primary PDFs with public retrieval URLs and exact hashes; they are not redistributed. `SOURCE_LOCATORS.md` maps every external theorem input to its location. The historical source and four turn manifests are preserved byte-for-byte. `FROZEN_MANIFEST.json` binds the final public packet; `RESEARCH_LOG_v6.md` and `TURN_STATE_v6.json` are the final author ledger. No source gate, audit or packaging step is counted as a sixth author turn.
