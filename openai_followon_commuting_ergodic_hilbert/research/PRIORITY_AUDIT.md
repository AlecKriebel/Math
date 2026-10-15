# Priority and attribution audit

Audit date: October 6, 2026, America/Los_Angeles (observations continued after
2026-10-07 05:12 UTC, which is October 6, 22:12 PDT). This is an independent
literature/scope audit, not certification of the upstream proof. No individual
was contacted. Compact current primary metadata and source hashes are in
`PRIORITY_EVIDENCE.json`; checked citation entries are in
`PRIORITY_REFERENCES.bib`.

## Exact comparison target

For arbitrary commuting invertible measure-preserving transformations S,T
on a probability space, complex f,g in L^3, and every r>2, the target is

\[
H_N(f,g)(x)=\sum_{0<|n|\leq N}\frac{f(S^nx)g(T^nx)}n,
\qquad H_0=0,
\]

\[
\left\|\sup_{J\geq1,\ 0\leq N_0<\cdots<N_J}
  \left(\sum_{j=1}^J|H_{N_j}-H_{N_{j-1}}|^r\right)^{1/r}
\right\|_{3/2}
\leq C_r\|f\|_3\|g\|_3.
\]

The comparisons must preserve the arbitrary two-generator action, hard
symmetric odd kernel, and supremum inside the output norm. Norm variation
with a fixed partition, an averaged direction, a curved orbit, or powers of
one transformation is a materially different statement. The associated
maximal and a.e./L^(3/2) convergence conclusions are consequences of this
variation estimate. This audit makes no assertion about ordinary one-sided
Cesaro averages or the endpoint r=2.

## Principal prior sources: full statement checks

| Source and public version history | Checked scope and consequence for priority |
| --- | --- |
| [Ciprian Demeter, *Pointwise convergence of the ergodic bilinear Hilbert transform*](https://arxiv.org/abs/math/0601277v1), v1 submitted 2006-01-12 08:56:51 UTC; only version currently listed. | [Full text, Theorem 1.2 and Remark 1.3](https://arxiv.org/html/math/0601277): symmetric Hilbert sums f(tau^n x)g(tau^-n x)/n converge a.e. for bounded inputs; the remark extends to 1<p,q<=infinity with 1/p+1/q<3/2 using a maximal inequality. The action is one invertible transformation and its inverse. This includes L^3 inputs in that special case. It does not state arbitrary independent commuting generators or the present full r>2 variation theorem. |
| [Lars Becker and Polona Durcik, *The shifted bilinear Hilbert transform*](https://arxiv.org/abs/2603.20173v1), v1 submitted 2026-03-20 17:48:52 UTC; only version currently listed. | [Full text, Section 1.2, Theorems 1.2–1.3 and Corollary 1.4](https://arxiv.org/html/2603.20173v1): M_n=n^-1 sum_(i=0)^(n-1) f_1(T^i x)f_2(T^-i x). Corollary 1.4 gives full variation for 1/r<min(3/2-1/p,1/2), with 1/p=1/p_1+1/p_2, 1<p_1,p_2<=infinity and p>2/3. At p_1=p_2=3 this allows every r>2. These are averages for one transformation. Theorem 1.9 concerns a one-dimensional BHT with a low-regularity kernel, not the arbitrary commuting triangular operator. Equation (1.8) and its surrounding discussion explicitly leave arbitrary commuting Cesaro a.e. convergence open. Neither the abstract's bilinear terminology nor its sharp r-range changes its action/kernel scope. |
| [Ciprian Demeter and Christoph Thiele, *On the two dimensional Bilinear Hilbert Transform*](https://arxiv.org/abs/0803.1268v1), v1 submitted 2008-03-08 23:26:13 UTC; published Amer. J. Math. 132 (2010), 201–256. | [Section 6](https://arxiv.org/html/0803.1268): Question 6.1 is arbitrary commuting Cesaro convergence; the flat triangular Hilbert operator is displayed as a further desired step. Theorem 6.2 proves particular two-parameter averages, not the single-parameter target. The paragraph and footnote 36 preceding Theorem 6.3 already describe R^2 -> Z^2 -> X transference using step functions and orbit arrays. Thus the general reduction is inherited, although the precise fixed positive-area restriction with a summable singular-kernel error must be supplied here. Their prose also records the known power-of-one-transformation case; Demeter's displayed 2006 Hilbert theorem uses opposite powers specifically. |
| [Polona Durcik, Vjekoslav Kovac, Kristina Ana Skreb and Christoph Thiele, *Norm-variation of ergodic averages with respect to two commuting transformations*](https://arxiv.org/abs/1603.00631v3), v1 2016-03-02 09:42:38 UTC; v2 2016-06-27 18:46:44 UTC; v3 2017-08-02 19:52:18 UTC; ETDS 39 (2019), 658–688. | [Theorem 1](https://arxiv.org/html/1603.00631) gives sum_j ||M_(n_j)-M_(n_(j-1))||_2^2 <= C||f||_4^2||g||_4^2 for each fixed partition. It is norm variation of averages. Corollary 3 gives short pointwise variation in the continuous averaging setting. Corollary 5 is an L^4 x L^4 -> L^2 smooth square-function estimate; the following paragraph says no bounds were then known for the triangular singular integral. Section 5 supplies another explicit continuous-to-lattice and orbit-transference precedent, including integration over phases of positive area. None of these gives the target's full point-dependent partition bound. |
| [Yen Do, Richard Oberlin and Eyvindur A. Palsson, *Variation-norm and fluctuation estimates for ergodic bilinear averages*](https://arxiv.org/abs/1504.07134v2), v1 2015-04-27 15:36:21 UTC; v2 2015-04-28 16:20:42 UTC; Indiana Univ. Math. J. 66 (2017), 55–99. | [Section 1 and Theorems 1.2–1.3](https://arxiv.org/html/1504.07134) define averages using T^n and T^-n. Ergodic full variation is obtained for sufficiently large r, while suitable smooth continuous bilinear averages have r>2 variation. Section 2 details classical transference adaptations. This is a further source for methodology and the older special case, not an arbitrary commuting Hilbert theorem. |

The mathematical transference mechanism should be credited to
[A. P. Calderon, *Ergodic theory and translation-invariant operators*](https://doi.org/10.1073/pnas.59.2.349),
Proc. Natl. Acad. Sci. U.S.A. 59(2) (February 1968), 349–353. The citation was
checked against [PubMed PMID 16591604](https://pubmed.ncbi.nlm.nih.gov/16591604/),
the original article's PMC record, and current Crossref metadata. The publisher
PDF and live PMC scan were inaccessible during this audit; no new assertion
about the exact theorem hypotheses of that scanned paper is being certified.
The modern self-contained finite-window proof can be checked directly without
relying on an uninspected general multilinear transference theorem.

## Family 082 companion audit

All source files below were read from the read-only clone pinned at
`adc7f1241b42e322a6451854ab7e4b4c146bf78a`. Exact main/consequence statements
were inspected, and all three TeX source trees were searched for action,
restriction, lattice, phase, half-integer, and transference passages.

| Manuscript-specific source | Actual result stated; overlap with the proposed follow-on |
| --- | --- |
| [*Annular variation of the triangular Hilbert transform at the symmetric point*](https://github.com/openai/math/blob/adc7f1241b42e322a6451854ab7e4b4c146bf78a/preprints/Annular-variation-of-the-triangular-Hilbert-transform-at-the-symmetric-point-October-5-2026/annular-variation.pdf), author OpenAI, manuscript date October 5, 2026. | Introduction Theorem `thm:variation` is exactly the continuous complex L^3(R^2) x L^3(R^2) -> L^(3/2)(R^2) annular r-variation theorem for all r>2. Partitions are pointwise, unrestricted within scales, and rational positive endpoints exhaust all endpoints by continuity. Its consequences are the continuous two-endpoint maximum, joint principal values and scalar flat/simplex equivalence. There is no ergodic theorem or fixed-width Hilbert cell restriction. Lattice arrays in the proof are Riemann sampling for continuous estimates. This is the pivotal inherited analytic assertion; the present audit does not validate its proof. |
| [*The maximal triangular Hilbert transform at the symmetric point*](https://github.com/openai/math/blob/adc7f1241b42e322a6451854ab7e4b4c146bf78a/preprints/The-maximal-triangular-Hilbert-transform-at-the-symmetric-point-September-24-2026/paper.pdf), author OpenAI, manuscript date September 24, 2026. | Theorem `thm:main` gives the continuous hard two-endpoint maximum and continuous joint a.e./norm principal values at the same exponents. Commuting transformations appear as motivation. It states neither annular r-variation nor the arbitrary commuting discrete consequence. Its arrays and mesh passage do not implement the required fixed-width restriction. |
| [*An L^3 bound for the dyadic triangular Hilbert form*](https://github.com/openai/math/blob/adc7f1241b42e322a6451854ab7e4b4c146bf78a/preprints/An-L3-bound-for-the-dyadic-triangular-Hilbert-form-October-5-2026/dyadic-triangular-hilbert.pdf), author OpenAI, manuscript date October 5, 2026. | Main theorem is a real-input Walsh/XOR dyadic sum of absolute local triangular contributions, bounded by 40 times the three L^3 norms. The history section distinguishes this model from the continuous operator. It does not assert the arbitrary commuting Hilbert theorem or its restriction proof. |

The [family 082 Lean scope document](https://github.com/openai/math/blob/adc7f1241b42e322a6451854ab7e4b4c146bf78a/lean/docs/082.md)
names only the older maximal continuous result. The document and presence of
related Lean files cannot certify full annular variation or this follow-on.
Actual formal declaration/build validation belongs in the dependency audit.

### Public timing and corrections

Live GitHub primary metadata reports repository creation
2026-10-06 21:47:02 UTC, an initial commit dated 21:58:50 UTC, and last push
22:01:11 UTC that day. The path-specific history of the annular manuscript and
current `main` each list just that initial commit. A read-only current remote
query still resolves `main` to the pinned commit. There was no later correction
visible in this history at this audit.

These are creation/commit/push dates, not a certificate of the exact first
public accessibility instant: a repository can change visibility and commit
dates are not publication certificates. The three papers were verified
publicly accessible during this audit on October 6 PDT. Consequently their
September 24 / October 5 manuscript dates must not be presented as independently
verified earlier public disclosure dates. This is a correction to any timing
claim inferred solely from their filenames. No separate arXiv or journal
disclosure of these OpenAI manuscripts was verified.

## Adjacent current literature and boundary checks

- [Lin and Slavikova, *Rough averages of triangular Hilbert transforms*](https://arxiv.org/html/2607.20206v1), v1 submitted 2026-07-22 14:26:36 UTC: equations (1.1)–(1.2) and Theorem 1.1 average H_theta over directions with an L^q angular function, q>1. The text explicitly distinguishes a Dirac directional mass, which recovers the unresolved individual flat operator. Angular L^q bounds do not include that mass. This contemporary theorem does not duplicate the fixed-direction target.
- [Hsu and Lin, *Smoothing inequalities for corner-type bilinear averages: geometric characterization and applications*](https://arxiv.org/html/2410.15791v2), v1 submitted 2024-10-21 09:02:11 UTC, v2 2026-07-18 09:49:47 UTC: Theorem 1.37 assumes asymptotically homogeneous definable coordinate curves and (1.27), a positive limiting curvature ratio involving gamma'_1 gamma'_2/(gamma' wedge gamma''). For gamma(t)=(t,t), the wedge is identically zero, so that condition fails. The introduction explicitly calls the flat triangular operator the remaining unknown case. The result is not the flat commuting action theorem.
- [Durcik, Kovac and Thiele, *Power-type cancellation for the simplex Hilbert transform*](https://arxiv.org/html/1608.00156v2), Theorem 1: at degree n=2 the hard-truncation bound has factor (log(R/r))^(1/2) and scalar exponents (4,4,2). Cyclic permutation/interpolation gives the symmetric tuple with scale-range dependence still present. It is neither uniform full annular variation nor pointwise ergodic convergence. The arXiv version label is v2, December 11, 2016; regenerated HTML also displays a 2026 internal date, so the submission record controls public version timing.
- [Kovac, Thiele and Zorin-Kranich](https://arxiv.org/html/1506.00861v1), Theorem 1.7 and Appendix B.1, supply restricted-input Walsh bounds and the established flat/simplex coordinate equivalence. These are attribution precedents, not a proof of unrestricted full continuous variation. The public submission is June 2, 2015; regenerated HTML's later internal date is not the original disclosure date.

## Search record and limits

Searches during this audit used the exact phrases `bilinear ergodic Hilbert`,
`arbitrary commuting` with `Hilbert`, `commuting transformations` with
`Hilbert transform`/`variation`, `annular variation` with `triangular Hilbert`,
and the named authors/titles. Citation chains from the recent Becker–Durcik,
Lin–Slavikova and family 082 bibliographies were checked for materially
overlapping statements. Relevant exact theorem statements were inspected in
the primary arXiv texts, not inferred from keyword hits. Generic irrelevant
search results and unofficial indexes are not evidence used for mathematical
claims. A failed search is not proof that no earlier equivalent theorem exists.

No exact arbitrary-commuting discrete Hilbert full-variation theorem, or the
same fixed-width restriction proof, was found in the audited public sources.
This is a scoped negative finding, not a claim of being first. No corrections
or later versions of the two specifically requested arXiv papers are listed
in their live histories. A final current-history check should precede any
publication because the intended source is newly public.

## Attribution/novelty verdict

The appropriate contribution, if the pivotal upstream proof passes independent
mathematical audit, is an explicit discrete restriction and ergodic consequence
of OpenAI's full continuous annular variation assertion. The positive-area cell
kernel bookkeeping makes the consequence independently checkable. Finite-window
Calderon transference, orbit-array embedding, and the deduction of convergence
from finite variation are established machinery. The new note must not claim
to have independently proved the triangular Hilbert breakthrough or invented
transference. The inherited symmetric-point restriction and r>2 range must
remain visible in the abstract and metadata.

The exact ergodic formulation is absent from the inspected companions, so this
audit does not identify complete duplication of the proposed note. Its strongest
honest novelty description is a newly available corollary with a complete
restriction/transference proof. Whether that is publication-worthy does not
override the separate mathematical validation gate: any substantive upstream
gap blocks an unconditional solution claim. On such a gap, retain the valid
conditional reduction and record the unresolved analytic dependency rather
than publishing a full-solution preprint.

Priority-audit completion estimate: 95% for this scoped comparison, pending a
final refresh and any material new citation from mathematical/package reviewers.
Mathematical-resolution and publication-package percentages are maintained by
the parent research log; this audit supplies no proof-based percentage for them.
