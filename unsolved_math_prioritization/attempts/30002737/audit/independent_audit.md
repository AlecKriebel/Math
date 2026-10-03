# Independent full adversarial audit: rank480-30002737

**Verdict: PASS, for the printed dimension-unrestricted conjecture, with absolute continuity relative to ambient Haar measure.**

The frozen candidate supplies a valid unweighted, aperiodic, repetitive FLC Meyer set in the plane whose diffraction has zero two-dimensional absolutely continuous part, although its translation representation has a spectral measure equivalent to two-dimensional Lebesgue measure. I found no mathematical gap requiring another author attempt. This does not settle a separately restricted one-dimensional conjecture, establish historical priority, or constitute peer review by an outside mathematician.

Audit completed 2026-10-03 UTC. This is an independent reviewer artifact, not a second author attempt. The review itself made no remote writes. The separate, unpublished manuscript draft was not opened or used and is excluded from this package.

## 1. Audited corpus and integrity

The proof corpus was exactly the three files in `author/MANIFEST.json`:

- `author/attempts/turn_01.md`: SHA-256 `c412f6bf2e481aa76101aaccee737ce6042d59594abcdb17047da1b1d96969f5`.
- `author/checks/verify_counterexample.py`: SHA-256 `929d20b9c0673e4eb7e83bdf322a48ed4631ebf7d7328a681298c3ee9012aecf`.
- `author/checks/verification_results.json`: SHA-256 `27ea2fd74fe1ad7df096498349335cf36f1222166d9bca9789c422506c39f94e`.

All hashes matched before and after verification. The frozen checker was executed only in an isolated temporary copy because it writes its own result file. Its reproduced JSON agreed exactly with the frozen JSON. The proof was assessed mathematically and through separate controls, not accepted because that checker passed.

Local primary PDFs were read independently. Fresh Poppler text extraction matched the existing extracts byte for byte for the OWR report, Baake-Grimm paper, and van Enter precursor. The actual rendered OWR conjecture page was also inspected.

Source PDF SHA-256 hashes:

- OWR report: `23b89a2f8f2ac139fc32feb347ae05724ec3dd22aed540c59c24f8477ed7b3af`.
- Baake-Grimm RS paper: `637b2eb51d7b75ca0e2f73392bf79b232f445e23cacd88bfb7476a01e64e5734`.
- van Enter 2013 precursor: `d34826964104fd26d1f05ca852f2e40c0b8d99a6a549114977b8263d29011291`.

## 2. Exact target and dimensional scope

The OWR PDF's printed page 2996, PDF page 10, contains the claimed Conjecture 1. It says that absence of an absolutely continuous diffraction component implies absence of an absolutely continuous dynamical component. The statement and its preceding paragraph contain no restriction to dimension one, irreducibility, a single substitution letter observable, spectral multiplicity, or all factor diffractions. Conjectures 2 and 3 on the same page separately state dimensional restrictions, but those concern Gibbs measures and do not limit Conjecture 1.

The report introduction discusses measure dynamics on locally compact Abelian groups. More decisively, van Enter's primary precursor, arXiv:1310.0267v2, explicitly sets up configurations on Z^d on printed page 2 and Fourier correlation measures on R^d or d-dimensional tori on page 3, immediately before the same absence-of-AC question. Thus the planar reading is not based merely on a missing qualifier in an isolated sentence.

The Baake-Grimm primary paper, arXiv:0810.5750v2, page 2, expressly lists a diffraction measure concentrated on a line in the plane as an example of singular continuous diffraction. This independently checks the intended standard measure-theoretic classification. A line measure can be absolutely continuous relative to length on that line and still singular relative to the ambient two-dimensional Haar measure. The candidate consistently uses the latter.

**Scope conclusion:** PASS for the literal unrestricted statement and its standard ambient-Haar reading. An interpretation that deliberately excludes higher-dimensional product examples would be a different assertion. No one-dimensional or novelty claim should be inferred from this result.

## 3. All Rudin-Shapiro inputs checked

The required inputs are only minimality, unique ergodicity, balanced signs, and correlations E[x_0 x_m] = delta(m,0). The Baake-Grimm primary paper states strict ergodicity and equal sign frequencies on page 2 and gives the correlation calculation on pages 2-3. It uses the same Fourier normalization as the candidate.

I independently checked that the stated four-letter substitution really supplies the binary system used by that source. Let rho be a->ab, b->ac, c->db, d->dc and code a,b to +1 and c,d to -1. Every rho^3(letter) contains every letter, so the substitution is primitive. Its incidence matrix has all row and column sums equal to 2, with normalized Perron vector (1,1,1,1)/4, giving balanced binary frequencies. Primitive-substitution strict ergodicity passes to the binary factor.

For an explicit comparison with the source's two-sided recursion, use the legal rho^2-fixed seed c|a. Letters at even positions belong to {a,d}, and letters at odd positions to {b,c}. The codes of rho^2(a), rho^2(b), rho^2(c), rho^2(d) are respectively +++-, ++-+, --+-, ---+. These identities give exactly

w(4n+r) = w(n) for r=0,1;
w(4n+r) = (-1)^(n+r) w(n) for r=2,3,

with w(0)=1 and w(-1)=-1, which is the primary paper's definition. Thus there is no accidental substitution/coding mismatch.

For the infinite correlation proof, the paper introduces a_m=E[w_n w_(n+m)] and parity-weighted b_m. The recurrence at index 1 gives b_1=b_1/4 and a_1=-b_1/4, hence both vanish. The index-2 and index-3 recurrences then vanish, and every later index depends only on smaller indices. With a_0=1, b_0=0, induction gives a_m=b_m=0 for positive m; symmetry gives negative m. These are exactly the delta correlations used in the proof. The parity-weighted limits can also be interpreted in the uniquely ergodic four-letter extension, where position parity is encoded in the letter classes above.

Unique ergodicity gives uniform interval averages for the continuous binary cylinder functions x_0 and x_0 x_m. Consequently the claims hold for every element of the binary hull and not merely a chosen almost-everywhere sample. No independence of different RS coordinates is needed.

## 4. Independent reconstruction of the geometric hull

All four slots 0, e=(1/10,1/10), a=(1/3,0), b=(0,1/3) are distinct modulo Z^2. Their union lies in (1/30)Z^2 and contains Z^2. Thus the resulting set is uniformly discrete, relatively dense, FLC, and Meyer. This uses the actual unweighted union; there are neither coincident slots nor disguised multiplicities.

I enumerated the directed residue differences d-c. The equality d-c=e mod Z^2 occurs only for c=0,d=e. It follows that the set of p with both p and p+e present is exactly the anchor lattice. This remains true in every translate and every hull element. The test cannot be confused by a cross-cell pair, because the computation is modulo Z^2. Negative-control motifs with e=(1/6,0) do fail this test, so the control is not tautologically accepting every four-slot pattern.

Once the anchors are recovered, the slot a at each anchor decodes x_i and slot b decodes y_j. Absence at a or b is meaningful because anchors are already identified and the slot separation is positive. These are finite-radius local tests. Neither taking complements of a sequence nor swapping x and y creates an unobserved fiber: the a and b locations are physically different. Rotations/reflections are not part of the translation hull.

To make the action convention explicit, take (Sx)_i=x_(i+1). Then

Lambda_(S^m x,S^n y) = Lambda_(x,y) - (m,n).

The map Phi([x,u],[y,v])=Lambda_(x,y)-(u,v) therefore respects (x,1)~(Sx,0), is continuous at the suspension seams, and intertwines increasing suspension time with the usual negative-translation action on point sets. Independent integer shifts have dense orbit in X times X, so fractional translates and compactness give surjectivity onto the hull. The decoded anchor phase determines (u,v) modulo integers; fixing representatives in [0,1)^2 then recovers both complete sequences. This proves injectivity modulo exactly the stated seam relations. Compactness and the Hausdorff local topology complete the conjugacy argument. The nontrivial symbolic fibers over the torus phase are retained, not collapsed.

For the independent Z^2 product action, disintegrating an invariant probability over y shows its x-conditionals are S-invariant and hence equal to mu. The remaining marginal must also be mu. This proves unique ergodicity even if the initially chosen x and y happen to be the same sequence. It is invariance under independent coordinate translations, not probabilistic independence of a selected deterministic pair, that forces the invariant product measure. Minimality follows from the Cartesian product orbit. Constant-roof suspension gives the invariant measure mu times mu times du times dv and inherits these conclusions. Thus the point-set hull is uniquely ergodic and minimal, implying uniform patch frequencies and repetitivity.

Any point-set period preserves the locally recovered anchors and is therefore an integer vector (m,n). Decoding forces S^m x=x and S^n y=y. A nonzero period in a binary RS point would, by minimality, make X a finite orbit, contradicting the delta correlation at that period. Therefore m=n=0. The construction is genuinely aperiodic in the plane.

The additional primitive 16-letter block-substitution claim is also correct: its incidence matrix is the tensor product of the two primitive one-dimensional matrices. Positivity of the same power of each matrix implies primitivity of the product. This additional claim is not needed for the counterexample.

## 5. Independent autocorrelation calculation

Write the occupancy at a as (1+x_i)/2 and at b as (1+y_j)/2. The candidate's decomposition into the periodic mean comb P and signed fluctuations A,B is an exact algebraic identity for the positive, weight-one physical comb.

For a fixed displacement between two motif slots, sum first over the horizontal index and then the vertical index. The infinite pair coefficient is the product of the mean occupancies, except that an a-a pair gains 1/4 when its horizontal integer displacement is zero and a b-b pair gains 1/4 when its vertical integer displacement is zero. Mixed a-b terms are products of separate sign means and vanish. This directly reconstructs the result without assuming independent signs within either RS sequence.

Equivalently:

- P-P contributes (D*D_tilde)*delta_Z2.
- A-A contributes (1/4) delta_0 tensor delta_Z, with the horizontal delta arising from the RS correlation.
- B-B contributes (1/4) delta_Z tensor delta_0.
- P-A and P-B vanish by balanced sign means, including the reverse cross terms.
- A-B and B-A vanish by the product of the two one-dimensional means.

Fixed motif shifts change only O(N) boundary contributions in a square of side O(N). All weights are bounded. Dividing by area removes the error. The difference support is locally finite, so convergence of all coefficients gives vague convergence. Unique ergodicity/FLC additionally gives the canonical shape-independent autocorrelation along standard van Hove averaging; the displayed square computation already establishes the value required here.

With Fourier kernel exp(-2 pi i k.t), delta_Z transforms to delta_Z and delta_0 to Lebesgue measure. Consequently the displayed diffraction formula, including its 1/4 coefficients and the phases in D-hat, is correct. Its Bragg term is at integer pairs; the two other terms are line measures carried by R times Z and Z times R. Their union is a planar null set. The line measures have no atoms, including at line intersections. The entire diffraction is therefore singular with respect to two-dimensional Lebesgue measure, with a nonzero singular continuous part.

At displacement zero the periodic contribution is 1+1+1/4+1/4=5/2, and the two fluctuation terms add 1/2. Hence gamma({0})=3. Direct density is 2+1/2+1/2=3. The Bragg mass at frequency zero is |D-hat(0)|^2=3^2=9. Neither line term adds an atom there. All three normalization checks agree.

The preliminary weighted array was checked separately: expanding (4+x_i+2y_j)(4+x_(i+m)+2y_(j+n)) gives 16+delta(m,0)+4 delta(n,0). Its claimed singular planar diffraction and the torus Haar spectrum of x_0 y_0 are correct. This is a useful consistency check, but the verdict does not rely on treating a weighted example as unweighted.

## 6. Independent dynamical spectral calculation

The section choice h([x,u])=x_0 for 0<=u<1 is bounded Borel measurable. Its possible seam discontinuity is irrelevant to the L^2 translation representation; the seam has invariant measure zero. The established conjugacy makes it a legitimate point-hull observable rather than information unavailable from the physical set.

For each t and almost every u, suspension time t replaces x by S^floor(u+t)x. Integrating over x gives delta(floor(u+t),0). The set of u in [0,1) with 0<=u+t<1 has length (1-|t|)_+. This handles negative t and all integer/end-point cases. Thus h has the triangle correlation.

The triangle is the convolution of the unit-interval indicator with its reflection. Under the stated Fourier normalization, its spectral density is exactly sinc^2(k), where sinc(k)=sin(pi k)/(pi k), with the removable value 1 at k=0. Its integral is 1, matching ||h||_2^2. The two-coordinate product observable H has product correlation and hence density sinc^2(k_1)sinc^2(k_2). This density vanishes only when a coordinate is a nonzero integer, a countable union of planar null lines. It is positive almost everywhere, so its finite spectral measure is equivalent to planar Lebesgue measure.

This proves a nonzero absolutely continuous dynamical component. It does not assert that the full representation has only continuous spectrum or any particular multiplicity. The coordinate phase eigenfunctions and constants cause no contradiction. No theorem equating pure-point diffraction and dynamics applies because the physical diffraction is not pure point. Dworkin inclusion and reconstruction from factor diffractions are respected: the locally decoded product factor x_i y_j has full planar Lebesgue diffraction, while the original physical comb only records separate row/column fluctuations.

## 7. Independent controls and adversarial checks

The independent script and JSON are alongside this report. They do not import the frozen checker or enumerate IID signs.

- Compared 262,144 substitution-coded sites with the independent binary formula (-1)^popcount(n & (n>>1)); all matched.
- Compared 8,192 sites of the two-sided c|a construction with the source recursion, including negative indices; all matched.
- Verified primitivity at power 3.
- Tested all 64 choices of three row signs and three column signs by constructing their physical unweighted points; the directed marker selected exactly all anchors in every case.
- A deliberately faulty marker motif produced an extra directed pair and was rejected as expected.
- Built actual unweighted point sets with 12,800, 51,200, and 200,704 points. At each size, directly counted pairs for 117 physical displacements and compared them with an independently factorized finite expression that retains every boundary and nonzero-mean term. All 351 comparisons matched exactly.
- The largest tested patch had density 3.0625; this finite deviation from 3 is correctly explained by finite RS imbalance. No finite sample was falsely treated as the exact infinite limit. The maximum discrepancy from the asymptotic coefficients over its 117 displacements was 0.0625.
- The maximum absolute empirical RS correlation over lags 1 through 64 decreased from 0.0146484375 at length 1,024 to 0.000057220458984375 at length 262,144. These are diagnostics; the infinite theorem is established analytically above and in the primary source.
- Verified 334 rational suspension times by integrating the floor function over its exact discontinuity partition, including negative times and integer boundaries.
- Replayed the original checker in an isolated copy and obtained the identical frozen output; rechecked that all three frozen hashes remained unchanged.

The original checker's temporary use of independent signs is not a hidden flaw: every tested occupancy product uses at most two signs from one sequence, and balanced binary signs with zero off-diagonal correlation have the required two-variable moments. Nevertheless, the independent physical controls explicitly avoid that modeling shortcut.

## 8. Gaps, repairs, and release guidance

**Mandatory mathematical repairs: none.** No unsupported extra assumption is needed for the stated counterexample. The independent audit supports stopping substantive author attempts at one.

Optional exposition improvements, which do not change the frozen proof:

1. State Phi([x,u],[y,v])=Lambda_(x,y)-(u,v) to make the suspension action/sign convention explicit.
2. Cite van Enter's 2013 d-dimensional setup and the primary RS paper's line-in-plane example when explaining scope.
3. Give the short c|a and rho^2 computation above if a reader wants a direct bridge between the chosen substitution and the cited RS recursion.

Retain the limitations prominently: this is a planar product counterexample to the printed unrestricted implication, not a resolution of a separately one-dimensional question. Do not claim novelty, historical priority, journal acceptance, or externally certified proof. The unpublished draft was outside the audit and is not covered by this verdict.
