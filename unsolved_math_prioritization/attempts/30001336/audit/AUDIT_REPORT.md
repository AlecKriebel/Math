# Independent audit of rooted tree two point partial results

## Verdict

**Accept the frozen packet as scoped partial mathematical work. The original problem remains unresolved.** No correction to the retained identities or written kernel lemmas was found. This verdict does not accept an all-orders solution, a counterexample to the intended conjecture, or a novelty claim. All five approaches retain substantive unresolved obligations.

The object audited is problem 30001336, OWR-4084-010, catalog rank 825. The author archive is bound by SHA-256 `fcb64d4662bb9b54b5047557807ab1a5e3560b2261f1544d0248497a31a627ee`, 18,567 bytes and 10 files. Its manifest SHA-256 is `dfcf5632ba6ac56d177f308bf0dec215fe397c46cc7f1bb3f55ba1efb49088f2`. The author freeze was not edited. This independent packet contains no source PDFs, source extracts, dataset contents, or private coordination material.

## Target and source binding

All three full input corpora were reread and hashed. The target is unique in the catalog and problem corpus; its catalog position and rank are 825. The statement hash and combined record/report hash agree with the author binding. The exact latter hash is `2a87ecb68d9fd292d3b6baec29d17439aa52c62e672da02267811f0e2ddfda69`. `CORPUS_VERIFICATION.json` records byte counts, hashes, counts, and match results without reproducing the imported record.

All six retained public source PDFs independently match their advertised hashes and byte counts. The 2009 equation and second-order expression were compared visually with rendered PDF pages, not solely with text extraction. The public references are recorded in `SOURCE_VERIFICATION.json`.

The target is the continuous-index planar two-point function in the **four-dimensional self-dual** model. The zero-coupling value of the author's rescaled G is 1. The underlying connected propagator has the usual free denominator; conflating these conventions would change the recurrence. The source mass and wavefunction conditions and the four-dimensional radial measure were retained. The two-dimensional Lambert-W paper does not identify the same problem.

Primary source: [Grosse and Wulkenhaar 2009](https://arxiv.org/abs/0909.1389v1), equations (18), (19), (25), (29), (42)–(46), and the discussion following (46). The short report is [OWR 41/2009](https://doi.org/10.4171/owr/2009/41).

## Exact recurrence and low orders

The displayed source equation matches (42)–(43), including:

- the denominator G(0,a) in the quotient;
- both origin subtractions by a y and b y;
- the difference N(a,b)−N(a,0);
- the last term C(G−1)y;
- the argument order in every L, M and N term.

Writing the formal inverse of G(0,a) produces the author's triangular recurrence. The inverse has constant term 1; the quotient minus 1 has constant term zero. Accordingly, both nonlinear sums start at k=1, while their other factor can have index zero. There is no missing zero-order or counterterm contribution.

The independent checker compares direct expansion of the complete formal source expression with the stated coefficient recurrence through degree 8, using separate arbitrary rational coefficient arrays. This is an exact finite diagnostic supporting the algebraic derivation, not a proof that physical coefficient integrals exist at every order.

The formulas for L1, M1 and N1 were checked using actual kernels at additional parameter pairs, including a=b and a close to 1. The divided difference is interpreted by its derivative at the diagonal. The source's published g2 agrees with the reconstruction. The y0=y1=1 values follow from removable origin limits; no numerical limiting procedure is needed for these two identities. The origin-normalization induction is valid with its stated existence and differentiability hypotheses. It does not establish physical symmetry for arbitrary formal solutions.

For fixed a<1, the g1 endpoint difference has an explicit factor 1−r. The rational-symbolic endpoint cancellation in g2 similarly supplies this factor after collecting terms. The remaining coefficients have only bounded rational denominators at r=1 and logarithmic growth. Thus the displayed low-order L integrals converge. These calculations are not an all-order endpoint invariant.

## Rooted kernels and the divided difference

For the exact source kernel Kf(a)=∫₀¹ a f(u)/(1−au) du, the tree-size induction is sound. A child forest is bounded near zero and has at most a fixed power of |log(1−u)| near one. Splitting at 1−u=1−a yields the stated logarithmic bound for its grafted tree. On compact subsets a<1, the kernel and all its a derivatives have an integrable common bound. This proves the claimed local smoothness and the O(a) origin behavior.

For a tree t=K(F), the resolvent identity is

(KF(x)−KF(a))/(x−a) = ∫₀¹ F(u)/[(1−xu)(1−au)] du.

Every forest used here is nonnegative. Tonelli therefore justifies the exchange before finiteness is established. Integrating x and then splitting 1/[u(1−au)] gives

D I_t(a) = K(I_leaf F)(a) + ∫₀¹ I_leaf(u)F(u)/u du.

The first term is exactly the tree with one extra leaf at the root. The period converges because I_leaf(u)=O(u) at zero and powers of logarithms are integrable at one. The apparent x=a singularity is removable; this is not a principal-value prescription. No regularized divergent period or unmentioned subtraction enters the proof.

For a star with m leaf children, the period is (m+1)! ζ(m+2). The exponential substitution and positive geometric expansion justify the all-size formula for every integer m≥0. Additional numerical representatives at higher powers are diagnostics only; the all-size justification is the written integral argument.

## Harmonic polylogarithms and endpoint regularization

The 0/1 alphabet and prefix convention are consistent: H_(0w) integrates H_w/s and H_(1w) integrates H_w/(1−s). Words used as functions end in 1, which ensures regularity at zero. Shuffle multiplicities are necessary and were tested independently by choosing interleaving positions.

A useful explicit version of the potentially delicate integration-by-parts step is obtained by differentiating the cutoff integral at R<1. For f=H_(1w),

(d/da)∫₀ᴿ a f(x)/(1−ax) dx
= f(R)[R/(1−aR)−1/(1−a)]
  + (1/(1−a))∫₀ᴿ H_w(x)/(1−ax) dx.

The boundary coefficient is exactly

−(1−R)/[(1−aR)(1−a)].

It kills every fixed logarithmic power in f(R), for fixed a<1. This proves the cancellation without separately assigning finite values to divergent boundary terms. The remaining derivative is K H_w(a)/[a(1−a)]. Both sides vanish at a=0, yielding the author's H1-prefix identity. The H0-prefix identity follows by the same differentiation and integration by parts, with the convergent endpoint H_(0w)(1).

For the standard decreasing-index convention, H_(0^(s1−1)1 … 0^(sk−1)1)(1)=ζ(s1,…,sk) when s1≥2. Every endpoint used in these transformations has an initial 0 and a final 1. Thus no divergent zeta value is silently admitted. After shuffle expansion, the tree period also receives an initial 0 and is convergent.

Induction therefore establishes tree algebra containment in the regular-at-zero HPL algebra with MZV coefficients. It does not establish the reverse containment at every weight, nor does it control the allowed two-variable rational prefactors.

## Independent finite rank verification

The independent implementation uses canonical bracket-string trees, iterative forest generation, position-based shuffles, direct signed word-substitution coefficients, and column-oriented modular elimination. It imports no author code. The two audit primes are 1,000,033 and 1,000,037, both checked prime, rather than the author's 1,000,003.

At each weight 1 through 9 both primes give ranks

1, 2, 4, 8, 16, 32, 64, 128, 256.

The forest counts are

1, 2, 4, 9, 20, 48, 115, 286, 719.

Full modular rank proves rational full rank for these integer matrices. Nothing in the audit turns these nine cases into an all-weight statement. The author's disclosed sign-mutation refinement is appropriate: rank alone can survive a wrong letter transformation. Direct sign and word-orientation tests remain necessary.

## Scope barriers and modern exact results

The polynomial a²+b² is symmetric and obeys the stated origin value and first-derivative conditions. Nevertheless L[f](a) diverges for nonzero a. This correctly refutes unrestricted operator closure on the proposed ring with only origin conditions. It does not refute membership of the actual recursively generated coefficients.

Likewise, the single-tree D formula does not prove closure for arbitrary products carrying the mixed rational kernels arising in N. Membership in a broad hyperlogarithm algebra, or allowing arbitrary rational localization, would be weaker than the requested polynomial form in a,b,A,B and the specified rooted integrals. Origin-removable quotients still require an explicit reduction rule. The 2009 source's MZV convention and third-order divided-integral footnote are disclosed ambiguities, not silently exploited counterexamples.

The [four-dimensional exact solution](https://arxiv.org/abs/1908.04543v1) gives the stated hypergeometric J and finite-renormalization choice. Its two-variable reconstruction and Taylor-subtraction matching do not, by themselves, supply the missing restricted polynomial reduction. The current [quartic-model paper v4](https://arxiv.org/abs/1906.04600v4) and its D=4 subtraction discussion were checked; its official page confirms the 2025 version and publication. The [Lambert-W paper](https://arxiv.org/abs/1807.02945v2) concerns two dimensions. This is a bounded assessment of the inspected statements, not an exhaustive literature nonexistence claim.

## Replay and adversarial controls

The author verifier reproduces 204 checks: 177 exact and 27 numerical. Both normal and optimized Python runs agree. Independent checks add 62 exact and 26 numerical diagnostics. Normal and optimized independent output is identical; relocation is tested separately. Numerical quadrature results are not formal certificates.

The audit replays the author code from a newly extracted temporary directory after externally checking the pinned archive and manifest. Both execution modes reject changed bytes, missing files, unexpected files, unexpected directories, symlinks, FIFOs, bytecode directories and loose bytecode. The independent pre-execution binder rejects these before mathematical execution. Injected bytecode is never executed.

Six deliberately reviewed mathematical mutations are rejected in each mode: removing a y subtraction, removing the quotient denominator contribution, reversing N's numerator, reversing the zero-letter sign, reversing the formal-inverse sign, and dropping a shuffle multiplicity. These tests use temporary copies; the original freeze remains byte-identical.

Manifest verification has an external trust boundary. Neither this packet's manifest nor the author's can authenticate coordinated replacement of itself. Independently retain the archive and manifest hashes supplied with delivery. Standard Python, SymPy and mpmath installations are execution dependencies, not bundled or independently supply-chain certified here.

## Remaining obligation

A full resolution must simultaneously establish coefficientwise endpoint integrability and origin limits at every order, membership in the intended restricted joint-prefactor/rooted-integral class, and closure under the actual quotient, subtraction, removable-division and mixed-kernel operations. An actual coefficient outside that intended class, accompanied by a nonmembership proof, would be an alternative resolution. This audit supplies neither. Status remains **UNRESOLVED, five scoped approaches exhausted**.
