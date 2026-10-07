# Independent adversarial audit of family 142

Audit checkpoint: 2026-10-07T04:27:03Z (2026-10-06 in America/Los_Angeles).
Auditor: independent subagent `/root/prime_field_audit`.
Pinned source: `/Users/alec/Desktop/math`, commit
`adc7f1241b42e322a6451854ab7e4b4c146bf78a`, verified by `git rev-parse HEAD`.
The source clone was read only throughout this audit. No repository writes,
builds, staging, publication operations, or external communications occurred.

## Verdict and strongest result

**The unconditional prime-field factorization theorem is not independently
certified by this audit.** Its pivotal dependency is the family 029 theorem
for arbitrary cyclotomic number fields containing the twelfth roots of
unity, not merely the family 003 result over Q(sqrt(-3)). Validation of that
general analytic theorem is required before using family 142 as an
unconditional input.

I accept on the basis of a complete manual proof read the
**algebraic auxiliary-prime reduction** in family 142: for binary prime p and
a nonzero dense polynomial of degree n, supplied auxiliary primes

    ell_q not in {2,3,p,q}, ell_q = 1 (mod 12q),
    p^((ell_q-1)/q) != 1 (mod ell_q), for each prime q <= n,

in the branch p > B^200000, B=20+(n+1)(ceil(log2 p)+1), suffice for complete
deterministic factorization with multiplicities in a fixed polynomial in
B+E, E=max(2,max ell_q). The explicit source bound is
O(B^500000+B^100 E^20). **Its dependence on E is numerical, not logarithmic.**
No concrete algebraic counterexample, hidden field-factorization oracle,
or circularity was found in the complete read of sections 01–09.
This is a manual mathematical audit, not a formal proof or implementation
validation of the entire large-characteristic branch.

At this checkpoint, for the original unconditional follow-on objective,
best-guess completion is 20% mathematical resolution and 0% publication
package from this auditor's information. These percentages reflect the
unresolved pivotal analytic dependency; they are not evidence for any theorem.
The parent project may have additional independent progress.

## Exact dependency chain

1. Family 142, `00-introduction.tex`, `thm:factorization` (line 27), claims
   O(((n+1)ceil(log2 p))^(10^12)) deterministic bit complexity.
2. Its algebraic `thm:reduction` (line 61) is conditional on the supplied
   auxiliary primes above and has no analytic assumptions.
3. `10-analytic.tex`, `analytic:hecke` (line 9), explicitly invokes family
   029, Theorem 1.2: for every cyclotomic K containing mu_12 and every
   finite-order Hecke character chi of K, L_K(s,chi) has no zero in
   Re(s)>1-10^-6, with the principal pole permitted, without a conductor
   or height restriction.
4. `analytic:auxiliary` (line 91) uses K=Q(mu_(12q)) and
   M=K(p^(1/q)); M/K is cyclic of degree q because p is unramified in K
   and X^q-p is Eisenstein at primes above p. Abelian zeta factorization
   transfers the Hecke strip to zeta_M and zeta_K.
5. The smoothed prime-ideal difference Psi_K(x)-q^-1 Psi_M(x) gives an
   auxiliary rational prime ell <= c_0 B^20000000. Numerical enumeration,
   trial division, and modular powering then find it deterministically.
6. Family 003's scope document `lean/docs/003.md` explicitly limits its
   Hecke theorem to Q(sqrt(-3)); this does not contain the required
   varying cyclotomic-field theorem. Its stronger numerical width 7/8
   cannot compensate for the narrower field scope.

The family 029 introduction and complete `06-zero-free.tex` were read.
The latter's Mellin completion depends on its earlier exact cubic-theta,
reflection, and Poisson/Euler-factor construction. Those representation
theoretic inputs are not certified here. The new theorem is a general
cyclotomic extension of the family 003 mechanism, not a stated consequence
of family 003's formalized theorem.

No family 142 or family 029 entry was located in the pinned formalization
catalogue. `lean/docs/142.md` and `lean/docs/029.md` are absent. No Lean
build is relied upon in this report. An unrelated Comparator or existence
of a Lean directory must not be described as verification of the relevant
factorization theorem or general cyclotomic zero-free theorem.
Absence of a formalization is not itself a mathematical gap: a sound
independently checked written proof can establish these theorems. The
remaining validation here is the manual audit of the pivotal general
cyclotomic analytic construction, which is outside this agent's full scope.

## Adversarial checks of the algebraic mechanism

### Primary table and apparent recursion

In `01-table.tex`, U_q is the H_q-invariant subalgebra of
F_p[T]/Phi_ell(T), where H_q is the subgroup of qth powers modulo ell.
Over the algebraic closure it has q coordinates. Frobenius acts by p on
Gamma_ell/H_q. The auxiliary test makes this permutation one q-cycle,
so U_q is a field of degree q. This implication uses both primeness of q
and primeness of ell; the input verifications are explicit.

For odd q, the call that constructs K_q factors Phi_q, of degree q-1.
Every table entry consumed by that factorization has prime index <= q-1.
The table is built once in increasing q; nested factorization does not
restart the table construction. Thus the recursion is well founded and
the total of at most n table factorization inputs has degree <= n.
The temporary V_q=U_q tensor K_q is a field because
[K_q:F_p]=ord_q(p) divides q-1 and is coprime to q.
Its dimension over F_p is at most q(q-1).

In `02-finite-fields.tex`, `ff:unitroot`, the eigenvector step
v^(Q^(d/q))=zeta v for q|d gives an element whose order has full q-part
q^(v_q(Q^d-1)). The lifting-the-exponent argument is only used for odd q
with q|Q-1, as required. The kernel-combination search excludes fewer
than h^2 prime-field scalar values and tries h^2+1 distinct values under
p>h^2. Its repeated digit tests cost polynomial in q and h, not log q.
Here q<=n, so this dependence is compatible with dense degree complexity.

### Norm solver

`03-norms.tex` builds the cyclic algebra with q^2 standard monomials,
using a promised norm G to prove only that it is split. The unknown norm
solution is used in this existence argument and in local solvability
proofs; it is not subsequently supplied to the algorithm.

At ramified places, V'=Y^-w V has qth power G/F^w, whose residue is a
qth power by the norm promise. At unramified places with q not dividing
v(G), the residue of F must be a qth power, because an unramified
extension of degree q would force norm valuations divisible by q.
Both roots are constructed by `ff:unitroot` in squarefree residue
algebras; this avoids factoring those residue moduli.

The selected local orders descend to a maximal order on P^1. A split
generic algebra identifies this order with End(V) for a vector bundle V.
The proof of splitting V over the original finite field, not just its
algebraic closure, is included. Its evaluated global-section algebra is
conjugate to a full block upper-triangular matrix algebra.
The trace-pairing radical is exactly the strictly block upper-triangular
part. Its common column kernel is the first block; any v there and row w
with wv=1 give a rank-one idempotent vw in the evaluated algebra.
An arbitrary global lift b has constant characteristic polynomial
T^(q-1)(T-1), so b^q is a genuine rank-one idempotent generically.
The final linear system Ve=he then produces a norm solution.

For d_H<=N+2D and M=10q^2(N+D+1), the global-section ansatz has
q^2(M(d_H+1)+1) unknowns, at most O(q^2 M(d_H+1)) local scalar
conditions, and quotient dimensions at most (3M+3)d_H. All are uniform
polynomials in q,N,D. The explicit denominator/minor bounds control the
rational coefficient degrees. I found no place where an integer
factorization or finite-field irreducible-factorization oracle is hidden
in this construction.

### Geometry and divisor calculations

`05-geometry.tex` defines T_t from class/infinity-divisor pairs. The lattice
Lambda is free of rank q-1, generated over Z[zeta_q] by
e=(sigma-1)infinity_0, and lambda=1-sigma acts injectively on it.
The injection T_t -> T_(t+1) and equality of its image with
T_(t+1)[lambda^t] follow using that injection, without inferring an
integral lattice division from an equality merely in the Jacobian.

The first torsion layer is generated by the ramification pairs epsilon_i
with sum_i epsilon_i=0. Their Hilbert-90 label formula retains the actual
infinity divisor. Frobenius is identity on the first layer; the binomial
expansion and q~lambda^(q-1) give identity on T_m over an extension of
degree q^r, where m=1+(q-1)r and r=v_q(N). Hence all required divisions,
including every choice made by deterministic division, are rational over
the same field. The bounds q^r<=N, m<=N,
[k:F_p]<=N(q-1) hold.

The final separation proof only asserts lambda d_t=[W_t] when a test is
reached. Equal labels imply zero in T_1 and consequently an *actual*
divisor W' with W_t=lambda W'. At the final level this contradicts
Ne in lambda^(m-1)Lambda but not lambda^m Lambda. The proof does not
silently assert the class/lattice invariant before it has been established.

The fractional-ideal representation of finite divisor parts in
`04-divisors.tex` has dimension 2q deg H. Its addition, minimum, maximum,
and inversion are operations on these finite subspaces. Characteristic
polynomials of multiplication by X give exact pushforwards including
residue degrees and ramification multiplicities. The simultaneous trace
of ideals uses only s(b-1)+1 scalar combinations to produce a product
ideal; it does not enumerate b^s generator tuples. Large infinity
coefficients are handled by binary class additions and product circuits,
so exponentially large coefficient magnitudes do not become divisor
degree parameters.

### Driver, characteristic, and encoding boundaries

The Berlekamp fixed algebra has dimension r, the number of irreducible
components. The moment-curve separator rejects at most
binom(r,2)(r-1)<r^3 values; its totally split characteristic polynomial
has degree r<=n. gcd pullback returns factors in F_p.
All simultaneous-extension gcds also return F_p polynomials because
the original totally split polynomial has all roots in F_p.

The pth-root step in family 142 copies coefficients only because they
are in F_p. A follow-on implementation over F_(p^m) must apply inverse
coefficient Frobenius; copying extension-field coefficients is incorrect.
Derivative-zero recursion multiplies multiplicities by p and does not
run an enumeration of p coefficient positions. Nonzero-derivative
repeated-factor branches merge repeated monic factors by adding their
multiplicities. Constants and linear factors terminate directly.
Characteristic two lies wholly in the scalar-search branch, so no odd
characteristic geometric formula is asserted there.

For p<=B^200000 the enumeration has polynomial length in B even though
it is not polynomial in log p considered in isolation. For the large
branch, every scalar grid and polynomial degree is strictly below p
under that cutoff. The numerical auxiliary algebra dimension ell-1 is
charged explicitly to E, and only the analytic polynomial bound on E
converts the reduction into a polynomial in (n+1)log p.

### Independent check of section 09's exponent accounting

The bounds in `09-complexity.tex` were recomputed independently, taking
B>=20. They have ample slack; no numerical exponent contradiction was
found. In particular:

| Quantity | Direct degree/dimension reasoning | Published upper bound |
|---|---|---|
| Extension dimension | N(q-1)<=B^2 | <B^2 |
| Norm bad-place degree | N+2D_G<=B+2B^3 | <B^4 |
| Norm valuation allowance | 10q^2(N+D_G+1) | <B^7 |
| Section coefficient degrees | M(d_H+1) | <B^12 |
| Truncated residue dimension | (3M+3)d_H | <B^13 |
| Section equations/unknowns | O(q^2 M(d_H+1)) | <B^17 |
| Primary powering bit length | d [k:F_p] log2 p, d<=B^4 | <B^8 |
| Idempotent coefficient degree | q P_*+(q-1)(N+D_G) | <B^15 |
| Norm output coefficient degree | q times cleared final-system degree | <B^20 |
| Norm function divisor degree | 4q(E_a+N) | <B^40 |
| Division reduction input | two times sum of q orbit partial sums | <B^46 |
| Riemann--Roch coefficient degree | deg H+norm(D)+g | <B^50 |
| Inverse function degree | q-row minor bound after clearing denominators | <B^54 |
| Temporary ideal bounds | products of these denominator/support polynomials | <B^60 |
| Ideal quotient dimension | 2q deg H | <B^65 |

The trace product has N<=B factors. Each reduced component has support
bound <B^3 and generator list <B^6; before curve reduction its determinant
has degrees <B^10 in X and Y. The trace scalar grid has length <B^8.
Binary infinity coefficients have length <B^4. Across m<=B^2 tests,
q<=B infinity differences and <B^4 binary digits use fewer than B^10
class/circuit instructions. Adding or doubling valuations increases their
bit lengths linearly in this circuit length, so B^12 covers evaluation.

The norm construction places all charged objects below U=B^25; its
O(U^30) operations, multiplied by O(B^40) scalar cost and generous integer
costs, fit inside B^2000. Divisor objects are placed below U'=B^200;
O((U')^30) operations plus scalar costs and polynomially many lift/test
instructions fit inside B^20000 per split. These are deliberately loose
uniform polynomial bounds rather than practical estimates.

At most B table entries cost O(B^41 E^10) outside their decreasing-degree
factorization calls. O(B^4) total factoring calls then cost O(B^20004).
The small-p enumeration costs O(B^201000). Squaring their sum for the
sequential-bit simulation gives

    O(B^402000+B^82 E^20)
      <= O(B^500000+B^100 E^20).

If E<=c_0 B^20000000 for absolute c_0, the second term has power
400000100. Finally B<=22(n+1)L for L=ceil(log2 p)>=1, so the claimed
10^12 exponent absorbs this power and all absolute constant factors.
The only nonalgebraic step in this accounting remains the asserted
uniform polynomial numerical bound on E.

## Reproducible checks and their limits

`prime_audit_table_checks.py` is an independently written standard-library
implementation of small auxiliary-table calculations. It constructs
cyclotomic quotient algebras, computes invariant kernels, verifies all
subgroup invariance equations, checks Frobenius-fixed dimension one,
checks Frob^q identity, and extracts the specified primary generators.
For odd examples it deliberately chooses p=1 (mod q), so K_q=F_p.
It uses small exhaustive searches only for the finite regression inputs.
It is not a uniform replacement for the source factorization algorithm.

Run from the dedicated project folder:

    python3 agent_notes/prime_audit_table_checks.py

Python version used: 3.14.6. Exact observed output is preserved in
`prime_audit_table_checks.jsonl`.

| p | q | ell | dim U_q | dim Frobenius fixed | primary generator | order |
|---|---|---|---|---|---|---|
| 5 | 2 | 73 | 2 | 1 | 2 | 4 |
| 7 | 2 | 73 | 2 | 1 | 6 | 2 |
| 13 | 2 | 73 | 2 | 1 | 8 | 4 |
| 7 | 3 | 37 | 3 | 1 | 2 | 3 |
| 13 | 3 | 37 | 3 | 1 | 3 | 3 |
| 11 | 5 | 181 | 5 | 1 | 3 | 5 |
| 31 | 5 | 61 | 5 | 1 | 2 | 5 |

These are checks of finite algebraic subroutines, not evidence for a
uniform zero-free strip, auxiliary-prime asymptotics, the whole norm
solver, or the full prime-field algorithm. The enormous large-p branch
was not executed. No practical efficiency claim is warranted.

## Exact reviewed source hashes (SHA-256)

All paths below are relative to
`preprints/Deterministic-Polynomial-Factorization-over-Prime-Fields-October-4-2026/build/sections/`.

| File | SHA-256 |
|---|---|
| 00-introduction.tex | a7048b62d7a31c5029827ad5db7e32187f5d29035138d6cc0677d48309a05af9 |
| 01-table.tex | 3cec5c2a6de5fe8b8759cdc20fd2c11723de54774c7e385626e3caa60ad92639 |
| 02-finite-fields.tex | a55ede868711f34fcca8c3adb788611e0c1bed4653bef1e568f67467fbe5dde2 |
| 03-norms.tex | 25c456356962e8ccc68e22e2b7c81feb4f0dc854fba9e0f3bdcb8cfb0f762d2f |
| 04-divisors.tex | 59a8b0d3e550838ef2cb507e2d06984bf21862d97d93f689e49488cf21e5a1d9 |
| 05-geometry.tex | a1291e26082593224df707cc5914976c0e764378bf633b87c2e5f3fde6d62094 |
| 06-division.tex | cf4edc99584ef070d2a7f24c9f217bc525c0b27a3f3aa422e9aeeb3ea4cef169 |
| 07-odd-split.tex | b77810b3c92751113f2da014d96227970a5f8b89bdb21dac34d17c69a2abb02b |
| 08-driver.tex | 2424818377cd664f42cf95da862733ad28932c525ce0b2fac18830443709440e |
| 09-complexity.tex | b9b69f8a0515a2af0d9b2a8e037809bab138aef74b0388b6ce74d8df3efb045a |
| 10-analytic.tex | 61a920fb8ef1e22d487b8dbeaaf3d3bd98328d08992807b40ed20b467ce0645e |

Additional hashes:

- Family 029 `build/sections/01-introduction.tex`:
  5cb01a814c568efa5bb6324ecfb9d556ea367e11fa5d59f455a5b203f9ce390d.
- Family 029 `build/sections/06-zero-free.tex`:
  c565166640d5e8210a2af70f00f6b9072112033a182ec7dede17e1517e76be33.
- `lean/docs/003.md`:
  41e52ed718260e6feb1db218f8e97287e703cb63c6f16e6c36f5563e6e2395ce.

## What remains outside this audit

The original follow-on's construction reduction, extension-field trace
coordinates, priority audit, complete candidate package, and publication
actions are owned by the parent effort or other agents. I have not
asserted novelty of known Berlekamp, primary-group, divisor, or Shoup
machinery, and have not relabeled upstream nonresidue consequences as new.
This source-level review is not one of the required complete-package
reviews. A candidate relying on family 142 must still state its complete
analytic dependency faithfully and independently validate or repair it.
