# Independent adversarial audit of the sparse extension

Checkpoint: 2026-10-07 05:33:53 UTC. Reviewer: independent internal AI subagent
`/root/sparse_adversarial`. Work is confined to the dedicated finite-field
project. No external contact, Git action, publication, or frozen-v3 edit was
performed. Best-guess completion for the new sparse mathematical route: 85%;
publication eligibility/package: 0% verified by this review. These estimates are
not proof or evidence of novelty.

## Scope actually reviewed

The parent originally supplied a promise version: sparse input with binary
exponents and arbitrarily large multiplicities, provided no non-X multiplicity
is divisible by the characteristic. While this review was running, the parent
supplied a materially stronger all-multiplicity Cartier recurrence. I separately
derived its polynomial invariant, coefficient identity, degree bound and
termination. I checked the existing finite-field arithmetic interface only to
use its small-field dense factorization as a test oracle. This is a targeted
mathematical/mechanism review, not a complete-package or priority review; no
manuscript or final release candidate exists in the reviewed scope.

No substantive mathematical counterexample was found to either carefully stated
version. The all-multiplicity version removes the promise rather than assuming
it away. It still depends on the previously audited dense finite-field
factorization theorem. This report does not independently revalidate that
upstream analytic dependency, establish novelty, or authorize publication.

## Precise claims and independently derived checks

Let K be a represented finite field of prime characteristic p. Canonical sparse
U has t nonzero terms, distinct nonnegative binary exponents and U(0) != 0. Let
N be its maximum exponent. First remove the minimum exponent from the original
polynomial; its X multiplicity is that exact integer. All following roots are
nonzero. A constant after this removal is an immediate terminal case.

1. **Visible denominator.** For monic irreducible g occurring in U with
   multiplicity e_g, perfectness of K makes g separable. Consequently the reduced
   denominator of U'/U is exactly the product of g with e_g not congruent to 0
   modulo p. In the quotient K[X]/g, the contribution e_g g' is nonzero and the
   other terms are regular, so the pole cannot cancel. The denominator has a
   nonzero constant coefficient and the reduced numerator has strictly smaller
   degree.

2. **Padé discovery without knowing its degree.** For doubled bounds B, obtain
   2B coefficients of U'/U at 0, solve Q(0)=1, deg(Q)<=B, deg(P)<B, then check the
   exact sparse identity U'Q=UP. Use coefficients through order 2B-1. If the true
   denominator degree is at most B, every solution of these constraints has the
   correct rational function: P1 Q2-P2 Q1 has degree at most 2B-1 and its first
   2B coefficients vanish. Thus arbitrary linear-system solution selection is
   safe after the exact check; one need not search solutions. False early zero
   approximants must be rejected. Reduce the resulting fraction before factoring
   its denominator. Derivative-zero U gives P=0 and visible denominator 1.

3. **Known-root multiplicity.** For alpha != 0, set w_i=a_i alpha^(n_i) and
   F(Y)=sum w_i(1+Y)^(n_i). Partition the full integers n_i by residues r modulo p:
   F=sum_r (1+Y)^r H_r(Y^p). If each child has initial order nu_r and leading
   coefficient L_r, let v=min nu_r and P0=sum_(nu_r=v) L_r(1+Y)^r. For s active
   residues, the matrix (binom(r,k))_(0<=k<s) is nonsingular: its determinant is
   the usual Vandermonde determinant divided by product k!, with all k<p.
   Hence P0 has a first nonzero coefficient at k<=s-1<p. Other children start
   at order at least p(v+1), so the parent order is exactly pv+k and the parent
   leading coefficient is that coefficient of P0. Single-term nodes are units
   at Y=0. Original distinct exponents remain distinct inside each child, so no
   nonzero subtree is an identically zero polynomial.

   This proves the computation and the bound e_g mod p <= t-1, also when e_g is
   arbitrarily large or divisible by p. A formal alpha=X mod an irreducible g
   suffices; the field K[X]/g has degree deg(g), and no root-finding, primitive
   root, or integer-factorization subroutine is needed. The order equals the
   g-adic multiplicity because g is separable and alpha != 0.

4. **All-multiplicity polynomial invariant.** Maintain F=U/V as a polynomial,
   with U sparse, V dense and both constant coefficients nonzero. Initially V=1.
   Let A_U=product g^(e_U(g) mod p), constructed only from the visible factors
   of U, and A_V=product g^(e_V(g) mod p) from dense factorization of V. There
   exist polynomial pth roots H_U and H_V with U=A_U H_U^p, V=A_V H_V^p, including
   their scalar coefficients. Because V divides U,
   floor(e_U(g)/p)>=floor(e_V(g)/p), so H=H_U/H_V is a polynomial.

   Define the zero Cartier section S_0(A)(Y)=sum_j A_(pj) Y^j and let sigma be
   coefficient Frobenius a -> a^p. The exact identity is
   S_0(U)=S_0(A_U) sigma(H_U). Therefore
   U_next=sigma^(-1)(S_0(U)), W=sigma^(-1)(S_0(A_U)),
   V_next=W H_V give U_next= W H_U, V_next=W H_V and U_next/V_next=H.
   The sparse numerator retains at most t terms and its maximum exponent is
   at most floor(N/p). Its constant coefficient and W(0) are nonzero.

   Multiplicity vectors satisfy
   mult(F)=mult(A_U)-mult(A_V)+p mult(H).
   Accumulating signed residues with weights p^j therefore recovers every
   original multiplicity when the numerator becomes constant. Intermediate
   negative contributions and artifact factors must be permitted and canceled.
   The original leading coefficient fixes the final scalar since all factors
   are monic.

5. **Denominator growth.** Let D be the original total degree of distinct
   non-X factors. The radical of H is contained in that of F: a positive
   difference of the two floor multiplicities implies e_U>e_V. Thus this D
   bound persists. If v=deg(V), the total distinct degree of U is at most D+v.
   Writing d_U for it,
   deg(A_U)<= (p-1)d_U and deg(H_V)<=v/p imply
   deg(V_next)<=((p-1)(D+v)+v)/p = v+(1-1/p)D.
   In particular deg(V_j)<=jD. Also deg(A_U)<=(t-1)d_U by item 3, so constructing
   its dense coefficients never requires work polynomial in numeric p.
   Each visible denominator has degree at most (j+1)D. There are at most
   floor(log_p(N))+1 stages, proved by shrinking U's maximum exponent, not by
   assuming every multiplicity of F is floor-divided.

6. **Bit and certificate bounds.** A Padé system has 2B rows and 2B unknowns;
   exact sparse verification has O(tB) products of terms with binary exponents.
   Doubling stops at B<=2 max(1,(j+1)D). Coefficients stay in the original
   represented K. Trie depth is at most the binary bit length of N; at most
   t times that number of nodes are required, and the sum of O(s^2) binomial
   work at any level is at most O(t^2). Each scalar binomial is computed with
   k<p using modular products and inverse integers, rather than scanning p.
   Formal-root field arithmetic is polynomial in deg(g), m and log(p).
   Coefficient inverse Frobenius uses a^(p^(m-1)), an exponent with O(m log p)
   bits. Dense oracle calls occur only on degrees O(D log(N+1)). All candidate
   factors over all stages have total stored degree O(D log(N+1)^2).
   These facts give polynomial bit complexity in t, log(N+1), m, log(p), D,
   when the audited dense oracle has its asserted polynomial bound.

   A separate final certificate can verify each monic factor's irreducibility,
   its original-input multiplicity by the trie (X by minimum exponent), distinct
   factors, weighted-degree equality and original leading coefficient. Actual
   divisibility plus equality of degree proves the product identity. This avoids
   expanding enormous multiplicities. Do not use the frozen dense
   Factorization.verify/reconstruct method for this new certificate.

## Counterexamples and implementation obligations

- **Invisible derivative factors:** X^2+1=(X+1)^2 over F2 has zero derivative.
  The initial promise algorithm can only report a promise violation by its
  degree certificate. The all-multiplicity recurrence correctly continues to
  the sparse pth root instead of calling this a complete factorization.
- **Artifact factor:** over F2, U=X^3+X^2+1, V=1 is squarefree and irreducible.
  A_U=U, W=X+1, so next U=next V=X+1 even though X+1 does not divide the original
  input. Signed cancellation is necessary; an intermediate factor list cannot
  simply be unioned into the output.
- **Coefficient inverse Frobenius:** in F4=F2[a]/(a^2+a+1), U=X^2+a has pth root
  X+a^2. Retaining the coefficient unchanged gives X+a, whose square is X^2+a^2.
  Apply inverse Frobenius to both sparse numerator section and dense section,
  and to the dense pth-root coefficients.
- **Floor-dividing F is false:** U=g^p,V=g gives F=g^(p-1), H=g. The new
  multiplicity is floor(e_U/p)-floor(e_V/p), possibly a ceiling of e_F/p.
  Radical containment and sparse-numerator degree decrease suffice instead.
- **Do not reduce exponents modulo the multiplicative group order:** this keeps
  weights alpha^n but changes the trie and loses multiplicities. Exponents remain
  full binary integers throughout digit partitioning.
- **Recursion depth:** allowed binary inputs can have more than Python's ordinary
  recursion-limit number of digits. The reference implementation should use an
  explicit stack or otherwise avoid imposing an unproved input restriction.
- **Sparse certificate:** reconstructing g^e by e repeated multiplications, as
  the old dense test verifier does, breaks the desired complexity.

## Reproducible checks actually run

Run these three owned scripts from the project root with Python 3; they write
small JSON receipts. They do not edit the frozen v3 record.

- `python3 agent_notes/sparse_adversarial_checks.py`: 8,556 trie results compared
  against full dense Taylor expansion over F2,F3,F4,F9; 5,821 Padé results compared
  against independently implemented dense Euclid over F2,F3,F5; an early false
  zero approximation rejected; six huge-exponent cases up to 2,001 exponent
  bits. The explicit-stack trie passes beyond ordinary recursive call depth.
- `python3 agent_notes/sparse_adversarial_recurrence_checks.py`: 742 small complete
  recurrence results compared with the previously supplied small-field dense
  oracle; three sparse huge-degree examples with mixed p-divisible/nondivisible
  multiplicities, up to 161-bit degree and only 18 terms, distinct output degree
  3. Sparse U is never expanded. Exact sparse Padé identity, formal-root trie,
  original-input final multiplicities and weighted degrees are checked. Every
  denominator bound passes, and artifact X+1 cancels from the cubic fixture.
- `python3 agent_notes/sparse_adversarial_frobenius_checks.py`: 1,669 one-step
  recurrence identities over F4,F9, including nontrivial dense divisors V of U,
  and the explicit coefficient-Frobenius omission counterexample above.

Each JSON contains its script SHA-256. These computations are finite falsification
attempts, not replacements for the algebraic derivation. The first script uses
existing field arithmetic, the second uses existing dense factoring only as a
small-field oracle, and the third uses dense factorization and dense pth roots
as explicit checkable test oracles. Test-only field/coefficient enumeration is
not claimed as a polynomial-log(p) implementation.

## Priority and alternate mechanism caveat

Novelty remains unestablished. A competing algebraic mechanism is available:
the Cartier sections of A_U have gcd 1, because a common section factor would
make A_U divisible by a pth-power polynomial despite all root multiplicities
being <p. A dense Bézout combination of these sections can therefore recover
sigma(H_U) as a sparse sum of dense-times-sparse products. It may inflate
sparsity at repeated stages, whereas the single-section rational recurrence
keeps t bounded by its original value. Existing literature on sparse squarefree
decomposition, Cartier-section gcd, sparse exact division, root multiplicity
and output-sensitive lacunary factorization must be inspected before claiming
this stronger reduction is new. I did not conduct that literature audit.
