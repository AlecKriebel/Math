# Independent arithmetic adversarial review of PR #628

**Verdict: PASS for the assigned arithmetic lower-bound and sharpness claim. No mandatory or optional finding remains.** This review does not certify historical novelty or the independent upper-bound/source-scope family. It establishes that the frozen explicit example is a valid reduced inner coarse Hurwitz point over Q with minimum ordinary coarse lifting degree exactly two. No cover-object descent is inferred from a coarse point.

Reviewed head: `677673860f9e67dffc610f52384f0bd60e65e363`. Problem: `30000403 / OWR-1188-004`. The exact QUEUE status at the parent snapshot is `claimed_solved`. All 36 captured target files were independently compared both to their declared SHA-256 values and to `git show` at that head; all match. The proof SHA-256 is `20cb77c2ac8befd8d2f9be9a421d2925580c29e24002a1abc8e3dedb13caeb5a`.

## 1. Exact claim and falsification criteria

Let G=C2, let C consist of six copies of its nonidentity conjugacy class, and let H(C) be the inner **coarse** Hurwitz space of covers of a fixed projective line, with **unordered** branch divisor. Let Hrd(C) be its PGL2 quotient. For x in Hrd(C)(Q), minimize degrees [K:Q] for which its ordinary coarse fiber has a K-point.

The example claims that this minimum equals two. A successful falsification would be any of: a repeated branch point; a disconnected cover; different inertia data or marking convention; failure of the reduced class to be Q-rational; an extra geometric base automorphism that cancels the real conic obstruction; an R-rational ordinary coarse point in the same reduced fiber; or failure of the exhibited Q(i)-point to be an actual ordinary coarse point.

| Attack route | Mechanism and evidence | Status and exact remaining gap |
|---|---|---|
| Degenerate or disconnected double cover | Five simple finite roots, odd pole at infinity, exact nonzero discriminant; quadratic valuation argument | Rejected; no arithmetic gap |
| Extra projective symmetries | Independent binary-sextic substitution for every possible image of the ordered triple (0,infinity,1) | Rejected; 120 candidates exhaust PGL2 over the algebraic closure |
| Wrong moduli or branch-order convention | Fresh primary source retrieval; manuscript section 1.1 and Theorems 1.1–1.2 | Rejected; source uses unordered branch divisors and coarse inner points |
| Reduced point not rational over Q | Exact Galois transformation of the sextic; unique marked double cover over an algebraically closed field | Rejected; field-of-moduli argument is sufficient for coarse rationality |
| Nontrivial torsor canceled by stabilizers or gerbes | Stabilizer is trivial; any real coarse lift gives a real branch divisor and a forbidden matrix norm equation | Rejected; no cover-object descent assumption enters |
| Quadratic lift exists only in a stack | Explicit smooth projective connected double-cover model over Q(i) | Rejected; this is stronger than the required coarse point |
| Hidden stronger conclusion | Separate fields of coordinates, coarse moduli, cover objects and degree minimization | No claim beyond the stated coarse sharpness result |

The original proof, original audit report, clarifications and all three supplied calculation programs were read. This review did not import their implementations into its newly written verifier.

## 2. Independent primary-source binding

Fresh direct retrieval succeeded for both primary PDFs; initial browser retrieval attempts had failed. Complete PDFs and extracted text remain only under the ignored `tmp/` directory. Public receipts contain URLs, byte counts, hashes and inspected locators.

- [Cadoret's contribution to The Arithmetic of Fields, OWR 6/2006](https://publications.mfo.de/bitstream/handle/mfo/2936/OWR_2006_06.pdf?isAllowed=y&sequence=1), contribution printed pp. 325–328; definitions on p.325 and the exact lifting question on p.326. Retrieved 558725 bytes; SHA-256 `803471040d06fcc1f83d5a0bd605e72bfd3a61434ee2a3dcd5259c48e2869412`.
- [Cadoret, Lifting results for rational points on Hurwitz moduli spaces, author manuscript](https://webusers.imj-prg.fr/~anna.cadoret/GPGL2.pdf), section 1.1, Theorems 1.1–1.2 and section 1.2, manuscript pp.2–4. Retrieved 341279 bytes; SHA-256 `705e6ec3b07bb11140f05ac70467ab96456f0ba444805e905ee60b188d402f76`.

The original report specifies characteristic zero, inner G-markings, a configuration space of r-element subsets of a fixed projective line, a PGL2 quotient, and residue-field degrees of coarse points in its fiber. The manuscript explicitly calls the branch points unordered and specifies compatibility of Galois action with geometric cover classes. Consequently the antipodal permutation of the six branches is allowed. An ordered-branch variant would require a different example and is not silently substituted here.

For this datum the single nonidentity element of C2 is invariant under every cyclotomic power action, so QC=Q. In fact the geometric Nielsen class for six copies of that element has one member: the tuple generates C2 and its product is one. Thus the finite étale branch map has degree one and identifies this coarse Hurwitz space with the six-point configuration space. This observation makes the absence of a hidden marking or coarse-cover obstruction especially transparent; the lower-bound proof below only needs the forward branch map.

## 3. Reconstructing the ordinary Q(i)-point

Put a=2+2i and b=−(1+i)/4. They satisfy b=−1/conjugate(a). The six projective points are

    D = {0, infinity, 1, −1, a, b}.

Their pairwise homogeneous determinants are all nonzero. The affine polynomial is

    f(x) = x^5 − (7/4)(1+i)x^4 − (1+i)x^3
           + (7/4)(1+i)x^2 + i x.

The independent exact calculation gives discriminant `342225 i / 128`, in particular nonzero. Its five finite roots are simple and its pole at infinity has odd order five. The smooth projective normalization of y²=f(x) is therefore branched precisely at D, with ramification index two at every point. It is connected because f has odd valuation at x=0 and hence is not a square in Q(i)(x). Characteristic zero makes the quadratic extension separable. Riemann–Hurwitz gives 2g−2=2(−2)+6=2, hence g=2.

This is an actual connected C2-cover over Q(i) of the fixed split target P1. It therefore supplies an ordinary coarse point p over Q(i), with the required six inertia classes. Since Aut(C2) is trivial, there is no extra choice of deck-group marking to track.

Over an algebraically closed field a reduced even divisor on P1 determines its connected double cover up to target-preserving isomorphism: any two defining functions differ by a function with even divisor; Pic(P1) has no two-torsion, and the remaining scalar is a square. Conversely, a base map that takes one cover to an isomorphic one preserves its branch divisor. Therefore the geometric stabilizer of the inner coarse cover point equals the projective stabilizer of D.

## 4. Exhaustive geometric stabilizer check

The new `arithmetic_checks.py` represents the branch divisor by the binary sextic

    F(u,v) = u v (u²−v²)(u−a v)(u−b v).

For each of the 6·5·4 possible distinct images of 0, infinity and 1, the verifier constructs the unique projective transformation with those images. It checks invertibility, projective distinctness of the 120 matrices, and whether **all coefficients of F(M(u,v)) are proportional to those of F(u,v)**. This is different from the original point-set-membership implementation and the older audit's 720 full-correspondence linear systems.

Because the sextic is squarefree, coefficient proportionality is equivalent to equality of its six-point zero divisor. Because a projective transformation is determined by three distinct point images, these 120 candidates exhaust every possible automorphism over C or Qbar. Each such matrix necessarily has coefficients in Q(i), since all three prescribed images do; the calculation is not restricted to a proper arithmetic subset of possible automorphisms.

The only surviving matrix for the sharp example is the identity, with permutation (0,1,2,3,4,5). Two controls exercise the possibility of missed symmetries: replacing a by 2+i returns a stabilizer of order two, and replacing it by i returns the octahedral six-point configuration with stabilizer of order 24. The latter prevents a checker that accidentally returns only a preferred cyclic subgroup from passing unnoticed.

The supplied 15 four-subset invariants also reproduce exactly. Their pairwise distinctness is a separate valid proof: every geometric automorphism must fix each four-subset, hence every complementary pair, hence each individual point.

Thus the base stabilizer E is genuinely trivial. It is not C2: the hyperelliptic deck involution acts trivially on the target and is not a nontrivial element of E.

## 5. Reduced Q-rationality

Let A be the matrix [[0,−1],[1,0]], representing z↦−1/z, and let j be ordinary complex conjugation. The antiholomorphic involution tau=A j exchanges the pairs (0,infinity), (1,−1), and (a,b). Hence A(conjugate(D))=D. The new verifier independently checks the stronger polynomial identity

    conjugate(F)(−v,u) = i F(u,v).

Every element of Gal(Qbar/Q) acts on the coefficients either as identity or conjugation on Q(i). In the latter case A takes the conjugate branch divisor back to D. By uniqueness of the geometric marked C2-cover, the corresponding reduced coarse class x is fixed by every such Galois element. A geometric point of the Q-variety Hrd(C) fixed by Gal(Qbar/Q) is a Q-rational point.

This proof does not require the isomorphism between the conjugate cover and its coordinate transform to be defined over Q(i). For example the displayed sextic identity permits a square root of i in a geometric isomorphism. Such auxiliary coordinates and failure of an object-level cocycle have no bearing on rationality of a coarse point. Nor does this argument assert an actual cover model over Q.

## 6. The obstruction survives passage to coarse points

Suppose that the ordinary coarse fiber over x had a real point p'. Its branch divisor D' is a real unordered divisor because the branch map is defined over R. The quotient is geometric on these stable orbits, so over C one has D'=h(D) for some h in PGL2(C).

Then rho=h^(-1) j h is an antiholomorphic map preserving D. So does tau=A j. Their quotient rho tau^(-1) is a projective-linear automorphism of D. Section 4 shows that it is identity, and thus rho=tau.

Here is an algebraic contradiction avoiding any reliance on a picture of fixed circles. The equality h^(-1) j h=A j means h^(-1) conjugate(h)=A in PGL2(C). Choose H in GL2(C) representing h. For some nonzero complex scalar lambda,

    conjugate(H) = lambda H A.

Conjugating again and using the real matrix A and A²=−I yields

    H = |lambda|² H A² = −|lambda|² H,

which is impossible because |lambda|² is nonnegative. Equivalently, the necessary norm equation is r²+s²=−1 over R. The new exact controls check the negative scalar square and the symbolic norm identity; the positivity argument is an ordinary mathematical deduction, not a finite numerical test.

This rejects **real coarse points**, rather than just real models of a cover. Therefore there cannot be a rational coarse point either. Potential cancellation by a target stabilizer is excluded by E=1. Potential source automorphisms or central gerbes do not enter: every coarse point already has an actual branch divisor on its fixed split target, which suffices for the contradiction.

The explicit Q(i)-point from section 3 gives mQ(x)≤2. Absence of a Q-point gives mQ(x)>1, so mQ(x)=2. The same reasoning over R gives mR(xR)=2. No assertion is made about every quadratic extension, every individual point, or actual-cover descent for arbitrary G.

## 7. Independent rational-conic reconstruction

As a second arithmetic certificate, consider the smooth conic

    B: X²+Y²+Z²=0

and its Q-rational degree-six divisor cut out by

    X Z (4X−4Y−7Z)=0.

The conic has no real point: a real sum of three squares vanishes only at the excluded zero vector. Over Q(i) it has the parametrization

    [u:v] ↦ [u²−v² : i(u²+v²) : 2uv].

The verifier checks the conic equation identically, and it computes

    (4X−4Y−7Z)(u,v) = 4(1−i)(u−a v)(u−b v),
    [X Z (4X−4Y−7Z)](u,v) = 8(1−i) F(u,v).

Thus the three rational lines cut exactly the same six distinct geometric branches. Coefficient conjugation on this conic pulls back to the antipodal map on its split parametrization, also checked symbolically. This realizes the precise nonsplit conic behind the obstruction, rather than merely invoking an arbitrary nontrivial Brauer class.

The reconstruction is corroborating evidence and a concise optional certificate for supporting materials. It is not a new historical priority claim or a mathematical defect requiring repair. In particular no actual double cover over B/Q is asserted: a rational branch divisor on a nonsplit conic and existence of the necessary cover line bundle are different issues.

## 8. Reproducibility, implementation corrections and limits

The pinned runtime is Python 3.12.14 with SymPy 1.14.0. Final runs:

- Original `verify.py`: 1754 exact assertions; stdout byte-identical to `CONTROL_RESULTS.json`.
- Original `verify_symbolic.py`: 32 symbolic assertions plus its candidate calculations; stdout byte-identical to `SYMBOLIC_RESULTS.json`.
- Original audit `independent_checks.py`: 96 assertions; stdout byte-identical to `INDEPENDENT_RESULTS.json`.
- New `arithmetic_checks.py`: 977 explicit checks in both ordinary and optimized Python; outputs byte-identical. Its checks use explicit exceptions and remain active under `-O`.
- Independent final provenance comparison: all 36 native files equal both the parent snapshot and the original Git objects.

Two review-implementation mistakes were caught and fixed before these final results. First, SymPy Gaussian-domain zero does not compare equal to Python integer zero; the new verifier now uses exact domain truth tests for determinants. Second, resolving the virtual-environment Python symlink before subprocess launch lost the virtual environment and caused three initial imports of SymPy to fail. Retaining the absolute virtual-environment invocation fixed the harness; the complete suite was rerun. The initial harness receipt is preserved as `INITIAL_REPLAY_RUNTIME_ERROR.json`. Neither issue changed an original input or supported a mathematical verdict.

Finite controls prove their finite identities and exhaustive candidate classifications. They do not mechanically verify general coarse-moduli existence, all Galois descent theory, the universal bound for other stabilizers, or historical novelty. The required moduli/Galois properties were checked against the primary source and used transparently above. The parent has assigned the full upper-bound/source-scope argument and subsequent priority audit separately.

No communication with outside individuals or other research shards was attempted. No PR, queue, branch, shared Git index, spreadsheet or Zenodo record was modified by this review. Only this arithmetic review directory was written. No remaining arithmetic concern was found for the assigned sharpness result.
