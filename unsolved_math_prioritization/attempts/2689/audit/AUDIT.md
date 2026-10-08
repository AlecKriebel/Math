# Independent audit of KP-1.30 / catalogue 2689

Audit date: 8 October 2026 (UTC).

## Verdict

**ACCEPT the frozen packet as rigorous partial progress with five approaches, all five unresolved as approaches to the universal conjecture.** No mathematical correction is required. This is not acceptance of a universal proof, a knot counterexample, or a novelty claim.

The audited report correctly concerns ordinary even, unreduced integral Khovanov homology of nontrivial classical knots. Its target is the existence of a nonzero element of order two; a higher-order 2-primary cyclic summand already supplies such an element. Reduced homology, rational Bar–Natan torsion, and the first Bockstein are used as tools and are not silently substituted for the target.

The original public directory, manifest, report, verifier, and archive were not modified. No correction patch was made because none was needed. This audit contains authored analysis, test programs, computed test results, and public-source verification metadata only. No source PDF, source-text extract, dataset contents, or private coordination document is included.

## 1. Frozen input and integrity

| Object | Bytes | SHA-256 |
|---|---:|---|
| Original MANIFEST.json | 1,157 | 859d3ac083256be02e0c0f139b08c502304855d47831af75dd94119dd647d2cc |
| Original REPORT.md | 22,726 | 6e1354f0909e2a45212b1d0723ff85a84f00e179d4ec40ffeaff444886ae5022 |
| Original candidate ZIP | 17,653 | 3feb6d48ac9e30cd1cf36a4a4e42430b9e8cb4f471a6439e1e393711975fe669 |
| Original verify_exact.py | 8,857 | c50db261666ad00895b6325a0f2d0235112a150100622a07652c414655fd8fa0 |
| Original EXACT_CHECKS.json | 5,546 | b59436f1306569a0e4c17070b98b7c1e99d173fbb1240941c742d944260a39b5 |

All five file records in the original manifest match their actual bytes and hashes. The ZIP has exactly the six expected public members, its CRC test passes, and each member is byte-identical to the corresponding original public file. Pre/post checks establish that both the original public directory and original ZIP are unchanged.

All eight locally retained source PDFs match the original source metadata for SHA-256, byte count, and page count. These are integrity checks of the supplied inspection materials, not claims that this audit independently downloaded every PDF again. Source texts and selected rendered pages were inspected locally; selected primary-source records were also checked on the public web. The source records and the mathematics checked against them are detailed below.

Machine-readable records: `RUNTIME_AUDIT.json`, `SOURCE_INTEGRITY.json`, and `INDEPENDENT_COMPARISON.json`.

## 2. Source scope and hypotheses

### 2.1 Problem identification

The author-hosted K3 preliminary volume has 436 PDF pages. Its printed pages 35–36 were checked both as extracted text and as rendered page images. Problem 1.30 is the universal nontrivial-knot question concerning 2-torsion. The nearby rank inequality is explicitly about reduced homology, while the torsion target is unreduced homology. The report preserves this distinction. The source's cited literature and the original Shumakovitch paper establish the ordinary integral even theory intended here.

The preliminary volume's restriction on reposting was checked. The public candidate and this audit contain no copy or excerpted source pages. The older four-page AIM workshop summary is not used as a substitute for the actual problem statement.

Primary source: [K3 preliminary volume](https://bpb-us-e2.wpmucdn.com/websites.umass.edu/dist/b/22144/files/2026/04/K3-problem-list-watermarked.pdf), printed pp. 35–36.

### 2.2 Characteristic-two splitting

Shumakovitch's Corollary 3.2.C supplies the bigraded reduced/unreduced splitting over F2. This is exactly the coefficient field needed for the torsion-count identity; the report does not extend that splitting to integral or rational coefficients. The original conjecture's elementary link exceptions are irrelevant to the stated knot-only target and are not discarded when discussing the broader literature.

Primary source: [Torsion of Khovanov homology, inspected v2](https://arxiv.org/abs/math/0405474v2), Corollary 3.2.C.

### 2.3 Rational Bar–Natan bars

The reduced/unreduced mapping-cone formulas and the three types of summand contributions were checked in Proposition 9.3 and its proof, including visual inspection of printed page 81. The reduced cone uses H; the unreduced cone uses H squared. A free rational Bar–Natan summand contributes dimensions 1 and 2, a length-one torsion summand contributes 2 and 2, and a torsion summand of length at least two contributes 2 and 4. The report uses precisely these counts. The rank-one free part for a knot is also explicitly used in the published Gujral–Wang argument.

Question 9.4 is a question, not an available theorem. The report correctly identifies it as the stronger proposed route and does not assume its answer.

Primary source: [Immersed curves in Khovanov homology, v2](https://arxiv.org/abs/1910.14584v2), Proposition 9.3 and Question 9.4. The public version record confirms v2 dated 17 December 2019.

### 2.4 Turner and Bockstein input

The thin-knot paper's Theorem 2.3.A gives the Turner differential's degree, the page indexing, the two-dimensional limit for a knot, and collapse at E2 under F2-homological thinness. Lemma 3.2.A gives the first-page identity involving beta and nu. The report neither promotes this first-page identity to a higher-page identity nor drops the collapse hypothesis. In particular, E1 is Khovanov homology, the first differential has quantum degree two, and the next possible differential has quantum degree four.

Primary source: [Torsion in Khovanov homology of homologically thin knots, v1](https://arxiv.org/abs/1806.05168v1), Theorem 2.3.A and Lemma 3.2.A.

### 2.5 Proper rational tangle replacement

The full published Gujral–Wang argument was inspected. Its maps are module maps between rational reduced Bar–Natan homologies, and both compositions equal multiplication by H. Their properness hypothesis preserves endpoint connectivity; a crossing change qualifies, while a general smoothing does not. The report uses that hypothesis correctly throughout.

The relevant definitions and proof of Theorem 1.1 in Iltgen–Lewark–Marino were also checked. Their chain maps may be ungraded, and the composition statements are up to chain homotopy; passing to total homology gives the module identities needed here. The audited argument counts total summands and does not incorrectly require those comparison maps to preserve either grading. The published Gujral–Wang proof explicitly identifies the base change from the Z[G] framework to Q[H].

Primary sources: [Gujral–Wang, published article](https://msp.org/agt/2025/25-7/agt-v25-n7-p10-p.pdf), Theorem 1, Corollary 2, Lemma 3, and Remark 4; [Iltgen–Lewark–Marino, inspected v2](https://arxiv.org/abs/2110.15107v2), Definitions 1.7 and 3.2 and the proof of Theorem 1.1. The latter public record now also lists Quantum Topology 16 (2025), no. 4, 655–741, DOI 10.4171/QT/244. Citing the inspected arXiv version in the original report is nevertheless valid and requires no correction.

### 2.6 Detection and diagrammatic input

The reduced-rank-three trefoil detection used through Gujral–Wang was independently checked against Baldwin–Sivek Theorem 1.4. It is a statement about integral rank, equivalently rational dimension, not merely a mod-two dimension test. Thus the exclusion of reduced rational ranks 1 and 3 is valid. Unknot detection and the odd-rank conclusion imply the stated lower bound of 5 for a hypothetical nontrivial counterexample.

The new torsion-pattern paper's Theorem 8 requires all ladder heights at least two, periphery conditions, a ladder of height at least three, and the stated condition on the remaining smoothing arcs. Corollary 10 weakens which ladders require periphery number one, but does not remove the remaining hypotheses. The report cites them only as sufficient conditions and does not claim every nontrivial knot has such a diagram.

Primary sources: [Baldwin–Sivek, trefoil detection](https://arxiv.org/pdf/1801.07634), Theorem 1.4; [Díaz–Manchón, new torsion patterns](https://arxiv.org/abs/2508.00606v1), Theorem 8 and Corollary 10. The original Frobenius-extension source is contextual; no necessary step depends on a theorem asserted only from its title or abstract.

A bounded public search found no verified later universal proof or counterexample. This supports retaining the report's cautious literature statement; it is not an exhaustive certification of the literature.

## 3. Audit of Approach I: coefficient fields and length-one bars

Let u be the total rational unreduced rank, r the reduced rational rank, and t and a the counts of unreduced and reduced 2-primary cyclic factors, respectively. A cyclic 2-power factor in integral degree i contributes one mod-two dimension in degree i and one in degree i−1. Therefore UCT gives total dimensions u+2t and r+2a. This counts factors, not their exponents, and ignores odd-primary torsion, as required.

The basepoint complex is termwise free over A=Z[X]/(X squared). Its marked-X subcomplex and marked-1 quotient identify, with the stated normalizations, with reduced complexes shifted by minus and plus one in quantum degree. The rational long exact sequence consequently has connecting map of degree (1,2). Summing kernel and cokernel dimensions gives u=2r−2rho. Characteristic-two splitting gives u+2t=2r+4a. Subtraction proves

    t = 2a + rho.

All quantities are finite and nonnegative, so the torsion-free characterization is an equivalence. No assumptions about thinness or torsion exponents were inserted.

For one free Bar–Natan summand and m torsion bars, with s1 length-one bars, the inspected cone formulas give

    r = 1+2m,
    u = 2+2s1+4(m−s1) = 2+4m−2s1.

Thus rho=s1 and t=2a+s1. This is an exact consequence of the rational cone formulas and integral UCT, not a conflation of H-torsion and integer torsion. The formal module with three length-two bars correctly gives r=7, u=14, and rho=0. It is appropriately labeled an algebraic profile; no knot realization is claimed.

**Outcome:** accepted exact reductions. They do not force a>0 or rho>0 for every nontrivial prime knot.

## 4. Audit of Approach II: higher-page cancellation

If t=0, the 2-primary Bockstein sequence has no nonzero differential. In particular beta=0, and the cited first-page identity gives the first Turner differential zero. Under the additional E2-collapse hypothesis, the initial total mod-two rank must then equal the knot's limiting rank 2. The reduced splitting, UCT, and rational unknot detection finish the conditional argument. F2-thinness is a legitimate sufficient collapse hypothesis.

For the abstract four-generator block, d(c)=b and T(a)=b, T(c)=e. The two differentials have the displayed bidegrees and form a double complex over F2. Integral d-homology is free on a and e; T induces zero there. To lift a along the filtration, its first error T(a)=b is canceled using c because d(c)=b. The next error is T(c)=e, which is a nonzero d-homology class. This is exactly a nonzero second differential. The total matrix is invertible, confirming disappearance of both initial classes.

The doubled construction is also valid. Pair corresponding generators in the two copies by nu and the reverse map X, then add a surviving pair. These maps square to zero, commute with d, and satisfy Xnu+nuX=identity. Integral d-homology remains free. The first-page Turner identity is satisfied because both sides are zero. The examples intentionally do not claim the entire package of knot-specific local Frobenius identities or realizability by a knot.

Independent full-matrix checks confirm:

| Doubled blocks | Chain dimension | E1 dimension | First differential rank | Second differential rank | Total homology dimension |
|---|---:|---:|---:|---:|---:|
| 1 | 10 | 6 | 0 | 2 | 2 |
| 3 | 26 | 14 | 0 | 6 | 2 |

Their integral nonzero Smith factors are all 1. Thus these examples genuinely demonstrate insufficiency of the listed algebraic premises, while making no claim about actual knot behavior.

The two-term multiplication-by-2-to-the-e examples are also correct. The first Bockstein coefficient is 2-to-the-(e−1) modulo 2, nonzero only at e=1; nevertheless every e≥1 leaves a cyclic integral 2-power cokernel. Orders 2, 4, 8, and 16 were independently checked.

**Outcome:** accepted conditional result and obstruction. No unjustified universal spectral-sequence collapse is inferred.

## 5. Audit of Approach III: the quantitative module lemma

This is the principal new algebraic refinement in the report, and its proof is sound for arbitrary coefficient fields and the stated free-plus-H-primary modules.

For M, let W=ker(H) intersect HM. A torsion bar of length at least two contributes its terminal vector to W, a length-one bar contributes nothing, and a free summand contributes nothing. Hence dim W=m−s.

Set C=g inverse(ker H on M). It is an H-stable submodule of N. For z in C,

    g(Hz)=H g(z)=0,
    H squared z = f g(Hz)=0.

Therefore C is a subspace of ker(H squared on N), and is finite-dimensional even when N has a free part. This finiteness justifies applying rank-nullity to H restricted to C; it is not an unstated finiteness assumption about N itself.

If y=Hx belongs to W, then y=g f(x) and f(x) lies in C. Thus W is contained in g(C). Moreover g kills HC, giving

    dim W <= dim g(C) <= dim(C/HC)
          = dim ker(H restricted to C) <= dim ker(H on N)=n.

This proves m−s<=n. The report's proof does not need a classification of f and g, and neither homogeneity nor equality of free ranks is required for this inequality. The sharp sample with M=R/(H squared) plus R/(H) and N=R/(H) satisfies both composition relations and R-linearity.

Using the source's proper-replacement maps and the exact torsion identity now legitimately gives

    t(K) >= 2a(K) + max(0, (r(K)−r(J))/2).

The ranks are odd, so the half-difference is integral. The inequality applies at the knot where a rank decrease occurs; it does not propagate torsion backward through previous steps. This is exactly why an arbitrary crossing-change path cannot prove the conjecture by this argument.

For a sequence M0,...,Md with each adjacent pair of maps composing to H, the forward composite F and reverse composite G satisfy GF=H to the d and FG=H to the d, by repeated cancellation of adjacent pairs and R-linearity. If Md is the free unknot module, F kills all torsion in M0, so H to the d kills it. Thus every exponent is at most d. If t(K)=0, no exponent is one, yielding the interval [2,d]. At d=2 all bars must have length two. The report's projection/inclusion example has both composites equal to H squared, including on the torsion summand, where H squared is zero; it is a correct formal consistency example.

Independent exhaustive checks over F2 covered all 49 pairs of nilpotent Jordan profiles with total dimension at most three in each module. There were 3,126 pairs of R-linear maps satisfying both composition equations; every pair satisfies the lemma in both directions, and 38 pairs attain equality in the displayed direction. This finite enumeration supplements, and does not replace, the arbitrary-field proof with free summands.

**Outcome:** accepted quantitative bound and exponent restriction. A global rank-descent theorem or a knot-realizability obstruction remains missing.

## 6. Audit of Approach IV: local order-two certificates

If dx=2v in a free integral cochain complex, then 2dv=0 and hence dv=0. If lambda annihilates all boundaries mod 2 and lambda(v)=1, v cannot be an integral boundary. Since twice its class is a boundary, its class has exact order two. This proof uses freeness in the next cochain group, not freeness of homology. The limitation concerning a divisible order-two element in Z/4 is correct: every homomorphism to F2 vanishes on twice a class.

The unsigned incidence calculation is correct. A spanning tree reduces all generators to a signed root; a bipartite graph imposes no additional root relation, whereas an odd cycle imposes twice the root. The cycle Smith forms for lengths 3 through 8 were independently recomputed, producing the claimed terminal factor 2 or 0.

In the short-exact-sequence example, the inclusion of the first source coordinate and the target identity are chain maps. The quotient is Z in degree zero. A lift of its generator has differential 1 in the target of A, representing the generator of Z/2. Consequently the connecting homomorphism is surjective, H1(A)=Z/2 disappears in B, and H0(B)=Z while H1(B)=0. The degreewise splitting does not split the homology sequence. This is a correct obstruction to an unqualified skein-induction claim.

**Outcome:** accepted certificate and counterexample to the naive survival step. No unsupported universal diagrammatic pattern is asserted.

## 7. Audit of Approach V: connected sums

The basepoint chain identification is valid. In each resolution, connected sum joins the two marked circles. Tensoring their two A-factors over A produces exactly the marked-circle factor of the sum. Other factors and Frobenius edge maps persist, with the tensor differential's Koszul sign. All chain terms are free over A. Quantum normalization may supply overall shifts, which do not affect any vanishing or total-rank argument here. Reduction gives the ordinary tensor product of reduced integral complexes over Z.

Write the A-linear differential in a homogeneous A-basis as d0+X d1. The constant coefficient of its square says d0 squared=0; the X coefficient says d0 d1+d1 d0=0. A lifted reduced cycle has differential X d1 of that lift, so d1 induces the rational connecting map of degree (1,2). No claim that d1 squared vanishes is needed.

Expanding the tensor differential gives the signed Leibniz rule for the connecting map. Under rational Künneth, choose homogeneous x with delta_K(x) nonzero and nonzero homogeneous y. The two potential terms live in different factorwise homological degrees, (i+1,j) and (i,j+1), even when they have the same total degree. They therefore cannot cancel. This proves that the tensor connecting map vanishes exactly when both factor connecting maps vanish. It does not require adding their ranks. The sample rank 4 for two rank-one maps is independently verified and properly presented only as a sample.

Field Künneth and UCT give

    r(K#J) = rK rJ,
    r(K#J)+2a(K#J) = (rK+2aK)(rJ+2aJ).

Thus

    a(K#J) = aK rJ + aJ rK + 2aK aJ.

Each reduced rational rank is positive, for example from the reduced Euler characteristic at q=1. Consequently a(K#J)=0 exactly when both aK and aJ vanish. Combining this with the connecting-map vanishing equivalence and t=2a+rho proves the report's full if-and-only-if for unreduced integral 2-torsion under connected sum. It is an actual proof, not an inference from numerical samples and not an unjustified claim that torsion directly embeds.

Prime decomposition now reduces the universal question to nontrivial prime knots. This step is valid in both directions, but cannot further decompose a prime knot into easier knots.

**Outcome:** accepted exact prime-knot reduction.

## 8. Independent cube computation

The additional `independent_cube.py` does not import, invoke, or reuse routines from the candidate verifier. It builds resolutions using four half-edges per crossing, braid-closure edges, and graph traversal. Merge and split maps are determined by changed connected components. Rational ranks use Fraction elimination; mod-two ranks use bitsets. This differs from the candidate's level-vertex union-find and SymPy rank implementation.

Every integer differential was checked to square to zero. All reduced and unreduced bigraded dimensions, not just totals, match the original saved results:

| Knot | Unreduced Q | Unreduced F2 | Reduced Q | Reduced F2 | Direct connecting rank |
|---|---:|---:|---:|---:|---:|
| T(2,1) | 2 | 2 | 1 | 1 | 0 |
| T(2,3) | 4 | 6 | 3 | 3 | 1 |
| T(2,5) | 6 | 10 | 5 | 5 | 2 |

The audit also computes the rational connecting map directly: take cycles of the marked-1 quotient, apply the off-diagonal differential to the marked-X subcomplex, and compute the image rank modulo subcomplex boundaries. This calculation does not infer rho from 2r−u. Its nonzero components are:

- Trefoil: reduced bidegree (2,6) to (3,8), rank 1.
- Cinquefoil: (2,8) to (3,10), rank 1, and (4,12) to (5,14), rank 1.

These directly confirm the connecting-map degree and the ranks inferred by the original verifier. All nine comparison records pass. Both independent programs were replayed in normal, -O, and -OO modes, yielding byte-identical saved JSON each time.

## 9. Read-only replay and semantic mutation controls

The candidate was copied to a separate directory with mode 0555 and files mode 0444. The actual UID and EUID were both 1000, with GID 1000. Attempts to create a file and to truncate REPORT.md both failed with PermissionError. This establishes actual read-only enforcement rather than relying on a root process's interpretation of mode bits.

From that directory, normal Python, -O, and -OO runs all exited zero and produced exactly the frozen 5,546-byte output with hash b59436f1306569a0e4c17070b98b7c1e99d173fbb1240941c742d944260a39b5. Python was 3.12.14; the output reports SymPy 1.14.0. Bytecode-cache creation was disabled through the environment for these replays. The original code contains zero Python assert statements.

Eight isolated semantic mutations were then compiled from in-memory altered copies, never applied to frozen files:

1. Change the expected trefoil mod-two rank.
2. Remove cube edge signs.
3. Remove a comultiplication term.
4. Move the nonzero first Bockstein to the wrong exponent.
5. Swap odd/even incidence Smith predictions.
6. Break the module example's composition map.
7. Remove the Turner perturbation.
8. Change the expected tensor connecting-map rank.

Each mutation failed in all three Python modes with the candidate's explicit verification RuntimeError: 24 substantive negative-control failures. None was counted as a successful control merely because of a syntax error, missing dependency, permission failure, or other unrelated exception. The read-only copy and original freeze remained unchanged afterward.

The original verifier has sensible finite-example scope. Some descriptive output fields encode known algebraic consequences rather than computing a general-purpose Smith or spectral-sequence solver. The independent algebra program checks the relevant explicit matrices, including full doubled Turner constructions and the connecting-map lift in the short exact sequence. Neither test suite is a computer proof of the universal conjecture.

## 10. Remaining conditions and publication scope

Each of the six listed necessary conditions for a hypothetical counterexample follows from the audited arguments. In particular, rank at least 5 makes its mod-two unreduced rank exceed 2; the vanishing first Turner differential and two-dimensional limit then force a nonzero higher differential. The interval [2,d] applies to any proper-replacement path to the unknot and does not assert existence of a length-one bar.

There is no contradiction established among these conditions. The final unresolved status and the count of five mathematical approaches are accurate. Source retrieval, computational checking, and this audit are not extra solution approaches.

**Final acceptance boundary:** the original packet is suitable as an authored partial-results report with reproducibility evidence and explicit limitations. It must retain its unresolved status. This audit makes no publication, repository, or global queue changes and does not authorize any broader disclosure beyond the supplied scope.

## Reproduction

- `python independent_cube.py` reproduces `INDEPENDENT_CUBE.json`.
- `python independent_algebra.py` reproduces `INDEPENDENT_ALGEBRA.json`.
- `python audit_runtime.py ORIGINAL_DIRECTORY FRESH_WORK_DIRECTORY` checks the original packet and reproduces the runtime tests. ORIGINAL_DIRECTORY contains `public/`, the receipt, and the original ZIP. Run as UID 1000 and choose an unused work directory. The printed metadata are saved in `RUNTIME_AUDIT.json`.

The audit manifest hashes this audit's authored public files and records the original frozen anchors. It deliberately excludes source inspection copies and runtime work directories.
