# Independent adversarial audit: 10400067

**Audit disposition: PASS for the frozen, explicitly unsolved five-turn partial-results packet.**
**HOLD any claim of a solution of Problem 3.17, a realized knot counterexample, or a globally calibrated Kricker–Lescop equality.**

The three algebraic obstruction claims, the relative degree-two comparison,
and the bounded reconstruction statements survive this audit. There is no
blocking mathematical error in their stated scopes. Two normalization/domain
clarifications below should accompany any abbreviated presentation. Neither
requires a sixth search attempt or a change of mathematical disposition.

## 1. Object audited and integrity

- Problem: 10400067 / AMR-103-0067, Ohtsuki Problem 3.17.
- Frozen directory: `packet`, 18 files.
- AUTHOR_MANIFEST SHA256:
  `11afc2553555cd72a0cb571a71c74d8dd2daa300ed1662d3bc74b4396353ee5c`.
- All 17 manifest-listed content hashes match, and every content reference in
  all five incremental manifests also matches. The recorded completion times
  are strictly ordered.
- The GitHub connector was used read-only to inspect
  [immutable WIP commit 0b52c95aff193bc8ed0fd4e4a1a2b4e2112cb7fc](https://github.com/AlecKriebel/Math/commit/0b52c95aff193bc8ed0fd4e4a1a2b4e2112cb7fc).
  All 18 files were fetched at that exact commit and compared byte-for-byte
  with the local packet. All match.
- Neither the frozen packet nor remote state was edited. All audit files are
  in the separate `audit-independent` directory.

The five manuscripts contain genuinely different attempted routes. Their
negative/partial outcomes are not counted as successful solutions. This audit
did not begin a sixth construction search.

## 2. Exact target and normalization

The target is the theta coefficient in equation (26), printed p. 439, in
[the 2002 original source](https://msp.org/gtm/2002/04/gtm-2002-04-024s.pdf).
I inspected the local publisher PDF text and the rendered page image.
The packet correctly keeps the Alexander-product denominator, source loop
degree 1, and simultaneous inversion. A theta graph has first Betti number 2;
the source's loop-degree convention is first Betti number minus 1 for a
connected graph. The invariant-ring calculation therefore addresses the
correct theta symmetry, not three independent inversions.

The printed trefoil expression is indeed not an invariant Laurent polynomial
as literally displayed. Treating it as an unquestioned symmetric
normalization certificate would be invalid. The packet explicitly avoids
that error. Ohtsuki 2007, Section 1.1, defines its numerator by summing the
12 group actions, rather than averaging. The resulting factor 12 is real.
None of the packet's algebraic kernels or support bounds depends on that
nonzero scalar.

### Clarification A: PBW versus wheeling

The original discussion passes through a wheeling algebra identification;
the 2007 numerator used in the genus theorem is expressed using inverse PBW.
The packet warns about conventions but does not spell out why this does not
invalidate the degree bound in the zero-framed theta sector.

Here is the missing low-loop explanation. The zero-framed expansion is
strut-free, and its nonempty connected components have first Betti number at
least 1. A nonidentity wheeling/unwheeling operation glues even wheels, each
with at least two legs, to input components. In any affected connected output,
let r be the number of input components, m the number of inserted wheels,
and k their total glued legs. Its first Betti number is

    sum_i beta_1(input_i) + m + k - (r+m) + 1
    = sum_i beta_1(input_i) + k - r + 1 >= k+1 >= 3.

Thus these operations do not change the two-loop connected component.
This explanation depends on zero framing; one must not silently extend it
to a strut-bearing framed expansion. It supplies the needed low-loop bridge
for using the 2007 support bound, without claiming a scalar calibration of
Lescop's invariant to the source target.

**Recommended wording:** “For the zero-framed strut-free expansion, nontrivial
wheeling corrections first affect connected graphs of first Betti number at
least three, so the theta component is unchanged. The 12-fold sum versus
average only rescales its numerator and leaves the degree bound unchanged.”

The exact scalar/hair identification of Lescop's invariant with the source
P remains outside the packet's proved conclusions, as it should.

## 3. Turn 1: invariant ring and reduced specialization — PASS

Multiplication by a large power of xyz clears Laurent exponents without
altering the class in R. Symmetric functions therefore give Q[a,b], with
a=x+y+z and b=xy+yz+zx; no relation between a and b is introduced by fixing
the third elementary symmetric function to 1. Simultaneous inversion
interchanges a and b, so the invariant ring is Q[u,v].

On (t,1,t^-1), u=2s and v=s^2 for s=t+1+t^-1. Division by v-u^2/4 and
the transcendence of s prove the entire kernel is (u^2-4v). This is an ideal
identity, not an experimental assertion. The displayed product for D has
the correct sign after squaring; its leading logarithmic term and even
parity are also correct.

The common-power divisibility statement is valid for positive and negative
nonzero powers. It is appropriately limited to this algebraic substitution
and is not presented as a general cabling theorem. The statement remains
an ambient-target obstruction, not a pair of realized knot values.

## 4. Turns 2–3: residues, H, and arbitrary finite jets — PASS

Character orthogonality proves for every n that A_n selects precisely
exponent pairs divisible by n. The eventual constant is the coefficient at
(0,0). Finite Möbius inversion therefore recovers exactly the gcd-shell
totals. No limit exchange or unsupported inference from finitely many n is
needed.

The theta action on the exponent lattice is unimodular. The five orbit
supports used for H are disjoint and primitive, with sizes 6,12,12,12,12.
Their weighted coefficient sum is zero. This proves the all-n residue
vanishing, including n=1. The factored expression for H is independently
verified below; its 54 terms, nonzero coefficient at (5,1), and reduced
restriction all agree with the packet.

For H_p, every support exponent has gcd exactly p. This both proves its
all-n vanishing and separates the supports of different p. The finite-jet
argument then uses a genuine interpolation identity at the distinct nodes
p_j^2. Odd logarithmic degrees vanish by simultaneous inversion; all even
degrees through J cancel by the displayed weights. Disjoint supports prove
that the result is nonzero, and clearing rational denominators gives an
integral certificate. This is a proof for every finite J, not a finite
extrapolation. Further common-power probes cannot detect it.

### Clarification B: residues act on the rational coefficient, not its numerator

The packet proves A_n(H)=0. It does **not** prove
A_n(H/[Delta(x)Delta(y)Delta(z)])=0 for arbitrary Delta. Confusing these
would be a substantive error. An independent adversarial negative control
shows the distinction is essential:

    Delta(t)=t+t^-1-1,
    A_5(H)=0,
    A_5(H/[Delta(x)Delta(y)Delta(z)])=12.

This value is exact. On fifth roots,

    (t+t^-1-1)^-1 = t^2+t^-2-1,

since their product is 1 modulo t^5-1. Expanding H times the three displayed
inverse polynomials and applying the exact coefficient-selection rule gives
12. No floating-point root evaluation is used in the certificate.

The intended unrestricted rational-target obstruction is nevertheless
available at every fixed normalized Delta: put

    Q_Delta = Delta(x)Delta(y)Delta(z),
    delta F = Q_Delta H^[J].

Then delta F/Q_Delta=H^[J], so every admissible rational residue, the reduced
restriction, and the prescribed jet still vanish. The numerator perturbation
is nonzero, symmetric, and integral after clearing any needed denominators.
Its degree grows; this extension gives no fixed-genus counterexample.

**Recommended wording:** “H is a kernel element for the polynomial residue
operator. For the rational coefficient with fixed denominator Q_Delta, use
the numerator perturbation Q_Delta H (or Q_Delta H^[J]), not H alone.”

This is a domain clarification to the packet's already careful polynomial
claims. It does not turn the ambient construction into a realized pair of
knots. A theorem about the actual image of the invariant could still defeat
an ambiguity present in the larger ambient ring.

## 5. Turn 4: relative Kricker–Lescop comparison — PASS, with exact scope

The theorem applicability was checked against the primary sources rather
than against the packet's paraphrase:

- [Moussard 2019](https://msp.org/gt/2019/23-4/gt-v23-n4-p07-s.pdf), Theorem
  2.16, identifies integral null-LP surgery classes using the integral
  Blanchfield module. Its filtration agrees with the null-Borromean one.
  Lemma 2.15 and Theorem 2.17 give Corollary 2.18, including G_1^Z(B)=0.
- [Audoux–Moussard 2025](https://londmathsoc.onlinelibrary.wiley.com/doi/full/10.1112/topo.70036),
  Theorem 2.2 gives degree n finite type in A_n(delta). The final paragraph
  of Section 7 explicitly states equality of the maps induced by Kricker
  and Lescop on the integral associated graded. Proposition 6.12 is the
  rational-setting comparison, so citing only that proposition would leave
  an applicability question; the packet correctly also cites Section 7.

The deduction is valid: E kills F_3 and has zero map on F_2/F_3, hence kills
F_2; F_1=F_2 then makes E kill F_1. Any two pairs in the fixed integral
Blanchfield class differ by an element of F_1. Consequently E is constant
on that class. Intermediates may leave S^3 while remaining integral homology
spheres, exactly as allowed by the framework.

This is a common-diagram-normalization, unmarked, rational-vector-space
statement. Replacing the integral Blanchfield class by an Alexander
polynomial or silently passing to a marked theory is not justified. The
packet does neither.

The constants c_B do not follow from normalization on the unknot's class.
Arbitrary class-constant shifts preserve nonempty surgery-bracket values,
but may fail other properties such as connected-sum constraints. The
packet explicitly limits this logical example to the surgery
characterization. Its conditional involution criterion is correct and is
not used to declare an unverified new family solved.

Thus the relative result is credited and valid; the audit does not upgrade
it to absolute equality, a normalization formula for P, or a construction
of the missing class calibrations.

## 6. Turn 5: bounded reconstruction — PASS

The tensor-product Lagrange formula is an exact left inverse to the moment
map on the whole square [-d,d]^2. The rectangle 0<=i,j<=2d is contained in
the total jet through degree 4d. With the zero-framed Ohtsuki degree bound
d=2g, the stated sufficient 8g jet follows. It is deliberately not claimed
optimal. The additional hexagonal support restriction |a-b|<=d follows
from the theta lattice action, but is not needed by the proof.

Multiplying a rational coefficient's jet by the known Alexander-product
jet recovers the numerator jet to the same order, since the denominator has
constant term 1. This does not require an analytic convergence assertion.

The weighted Fourier inversion is correct for N>2d, and requires all the
specified character weights (or equivalently the full sample grid).
The strict inequality is important: at N=2d, x^d and x^-d alias. Choosing a
prime N larger than deg(Delta)+1 excludes nontrivial roots of Delta by the
degree of the cyclotomic minimal polynomial; Delta(1)=1 handles the remaining
sample. The packet does not pretend that one ordinary cover invariant
provides the full weighted transform.

The missing step is genuinely topological: obtaining these inputs
independently and proving they are the exact source coefficient's inputs.
A finite algorithm that simply reads them from the already-defined
Kontsevich invariant does not establish the requested new construction.

## 7. Current-source checks and status language

[Lescop, Theorem 9.2](https://arxiv.org/abs/1008.5026) applies to trivial
Alexander polynomial and compares the hair of her knot invariant to the
primitive two-loop Kontsevich part. The packet does not incorrectly extend
that theorem to arbitrary knots.

[Bar-Natan–van der Veen v4](https://arxiv.org/html/2509.18456v4) still labels
equality with Ohtsuki's two-loop polynomial Conjecture 25; Theorem 24 is a
one-variable specialization. The v4 submission date is verified as
6 May 2026 on the [arXiv version record](https://arxiv.org/abs/2509.18456v4).
These claims do not supply the missing equality.

The exact unsolvedmath access and exhaustive absence-of-prior-attempt
assertions were not independently re-investigated in this mathematical
audit. Their recorded limitation must remain visible. “Unsolved” here
certifies that this five-turn packet does not solve the original problem
and that the cited sources do not supply a certified resolution; it is not
an impossibility theorem or an exhaustive guarantee about all literature.

## 8. Independent computational evidence

The supplied programs reproduce their receipts exactly:

- `verify_core.py`: PASS, 1,127 exact assertions.
- `verify_reconstruction.py`: PASS, 1,372 exact assertions.

The separately written `independent_controls.py` imports neither author
program and uses only the Python standard library. It adds **1,513 exact
assertions**, all PASS. The different controls include:

- a three-exponent Laurent representation modulo diagonal shifts, with H
  constructed from the product formula, not the author's orbit builder;
- direct exact permutation and inversion symmetry checks;
- nonconsecutive dilation parameters, testing complete jets through J=31;
- gcd-shell recovery by downward recurrence on an unrelated coefficient set;
- Gaussian-inverse moment reconstruction on full squares, including points
  outside the theta hexagon, for d=0 through 5;
- actual finite-field weighted root-grid sums for N=3,5,7,11, rather than
  only checking distinct residue indices;
- the N=2d aliasing negative control and the exact rational-denominator
  counter-control above;
- every frozen and incremental manifest content hash.

The receipt is `INDEPENDENT_CHECK.json`. The assertions supplement the
all-n, all-J, and all-d proofs; they do not establish knot realization or
an unknown topological comparison.

## 9. Release recommendation and repairs

**No blocking correction to the scoped theorems is required.** Preserve the
frozen files and their hashes. An audit addendum may include Clarifications
A and B verbatim; they are strongly recommended wherever the result is
compressed into a summary. If a later text claims H/Q_Delta is always
residue-invisible, that claim must be repaired to Q_Delta H as a numerator
perturbation before release. If it claims a general scalar equality of
Lescop and the source P, it must remain on HOLD pending a real comparison
and calibration proof.

Acceptable final classification: **five completed partial attempts;
original target unresolved; credited relative comparison and exact
ambient-algebra/reconstruction results only.**

This is an AI-assisted independent check, not human peer review.
