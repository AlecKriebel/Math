# Hostile audit: binary fixed-cubic line row

**Recorded:** 2026-07-25T06:55Z
**Scope:** `WORKING_BINARY_FIXED_CUBIC_LINE_ROW.md`,
`verify_binary_fixed_cubic_complete.py`, and
`verify_binary_fixed_cubic_complete_pari.gp`.
**Verdict:** **PASS mathematically; PASS executable after the fail-closed guard
was added during the audit.** No Keller-compatible leaf was found. There are
two documentation clarifications recommended before promotion, recorded
below.

This audit did not edit the theorem note, its verifiers, or any global ledger.

## 1. Independent artifacts

- `audit_orbits_lower_exact.py` does not import either theorem verifier. It
  reconstructs the root-order formula, universal low-\(\rho\) rank
  determinants, every finite pivot divisor, every discrete orbit
  representative, the complete lower-syzygy kernel, and all eight residual
  constants from exact determinants.
- `audit_exceptional_branches_exact.py` independently reconstructs every
  displayed raw \(E_6\) rank, all nine literal multiplier-square
  contradictions, both signs of every \(\rho=2\) pivot, all \(\rho=3,4\)
  zero-normal kernels, the division-free \(\rho=4\) compatibility tree, both
  conjugate \(d4b\) branches, and the full converse row reduction on the
  \(t4\) branch.
- `test_fail_closed.sh` rejects optimized Python and injects false top
  determinant identities into temporary Python and GP copies. All three
  tests currently fail closed.

All three audit artifacts refuse Python `-O` where applicable.

## 2. Orbit taxonomy

The stabilizer quotient in the note is exhaustive.

### Squarefree divisor \(h_s=pq(p-q)\)

The stabilizer is the finite \(S_3\) on the three marked roots. If their
multiplicities in \(W\) are \(n_1,n_2,n_3\), then
\[
 \rho=\sum_i\min(2,n_i).
\]
Thus:

- \(\rho=0\): no marked factor;
- \(\rho=1\): precisely one marked simple factor;
- \(\rho=2\): patterns \((2,0,0)\), \((1,1,0)\), or \((3,0,0)\);
- \(\rho=3\): patterns \((2,1,0)\) or \((1,1,1)\).

These are exactly the two \(A\)-families, the pure cube, \(p^2q\), and
\(pq(p-q)\) in the note, modulo \(S_3\). The only zeros of the relevant
parametric maximal minors are \(A=0,-1\), precisely where the residual factor
becomes another marked factor and the orbit moves to \(\rho=3\). There is no
hidden interior \(A\)-pivot.

For a completely general
\[
 W=ap^3+bp^2q+cpq^2+dq^3,
\]
the \(r^0\) \(E_7\) determinant is
\[
 -46656\,a^2d^2(a+b+c+d)^2.
\]
Hence the \(\rho=0\) assertion is universal, not a generic-sample claim.

### Double divisor \(h_d=p^2q\)

The stabilizer is the diagonal torus fixing the double and simple endpoints.
The local contributions are
\[
\begin{array}{c|cccc}
n_p&0&1&2&3\\ \hline
\rho_p&1&2&3&4
\end{array},
\qquad
\begin{array}{c|cccc}
n_q&0&1&2&3\\ \hline
\rho_q&0&1&2&2.
\end{array}
\]
Enumerating degree-three multiplicity pairs gives exactly the note's
\(\rho=1,2,3,4\) rows. Diagonal scaling and scaling \(W\) normalize both
nonzero endpoint coefficients of each residual quadratic, producing the
displayed \(B\)-families.

For general \(W\), the gcd of the maximal minors of the \(\rho=1\) \(r^0\)
matrix is a nonzero rational multiple of \(a^2d^2\). Thus no unlisted
low-\(\rho\) leaf occurs. In the \(q\)-family, the \(r^1\) determinant has
divisor \(B\), proving that \(B=0\) is the sole \(\{2,0\}\) splitting point.
The \(p\)-family has no such jump. The normal-projection determinants have
divisor \(B^2-4\), proving that \(B=\pm2\) are the only normal pivots.

### Triple divisor \(h_t=p^3\)

The stabilizer is the affine group on \(u=q/p\). A cubic polynomial in \(u\)
is reduced to:

- \(u^3+u+\Lambda\) when its depressed linear term is nonzero;
- \(u^3+1\) when that term is zero but the constant is nonzero;
- \(u^3\) in the pure-cube case.

Quadratic and linear residual polynomials give, respectively, the distinct
root/double-root pair and the single \(\rho=4\) orbit. This is exactly the
note's list.

For general \(W=ap^3+bp^2q+cpq^2+dq^3\), the \(r^1\) determinant is
\[
 3456\,d^2(3bd-c^2).
\]
After depression, \(3bd-c^2=0\) is exactly the separate \(p^3+q^3\)
\(\{2,0\}\) chart. In the \(u^3+u+\Lambda\) chart the normal determinant has
divisor \(27\Lambda^2+4\), and there are no further pivots.

## 3. Root-order and raw tangent audit

At a marked factor \(p=0\), writing \(h=p^mH\), \(W=p^nG\), the leading
coefficient of \(J(qh,W)\) is
\[
 (3m-4n)H(0,q)G(0,q)p^{m+n-1}q^{5-m-n}.
\]
It never vanishes for \(1\leq m\leq3\), \(0\leq n\leq3\). Together with
\(\operatorname{ord}_p J(ph,qh)=2m\), this gives
\[
 \operatorname{ord}_p\gcd(a,b,c)=\min(2m,m+n-1).
\]
The audit recomputed all twelve monomial instances independently.

Every displayed \(E_7\) nullity and every displayed full and \(r^0\) \(E_6\)
matrix shape/rank was reconstructed exactly. The parameter-minor
factorizations above prove that the generic bases do not conceal a
specialization outside the separately listed charts.

## 4. Exceptional \(E_6\) leaves

- Both signs of the \(d2q\) and \(d2p\) pivots and both conjugate triple-root
  pivots have augmented rank larger than coefficient rank. No conjugate chart
  was inferred merely by numerical symmetry.
- Each of the two \(\{2,0\}\) multipliers and all seven \(\rho=3\)
  multipliers occurs in a literal nonzero coefficient times \(g^2\) in
  \([r^3]E_6\). No division is used.
- The six one-dimensional \(\rho=3\) zero-normal kernels are incompatible.
- In each of \(t3d,d4a,d4b,t4\), the two-dimensional zero-normal kernel has a
  denominator-free compatibility pairing equal to a nonzero constant times
  the square of the second coordinate. This leaves exactly the first vector
  quoted in the theorem.
- For \(d4a\), separate literal pairings force both multipliers to zero.
- For \(d4b\), compatibility forces
  \[
  3g_0^2-8g_0g_1+8g_1^2=0
  \]
  and the two displayed linear relations on the \(r^0\) coefficients. If
  nonzero, \(g_1\ne0\). In the quadratic quotient
  \(\mathbb Q[\gamma]/(3\gamma^2-8\gamma+8)\), the complete \(E_6\) system
  has rank eight and \(E_5\) contains \((\gamma+2)/6\), which is a unit.
  Both complex conjugate branches are therefore empty.
- For \(t4\), compatibility first forces \(g_0=0\). On \(g_1\ne0\), it
  forces \(z_1=0\) and \(z_3=z_0\), giving exactly (17).

The audit strengthened the last check from candidate verification to a
converse. A constant \(7\times7\) minor proves that the displayed \(E_6\)
substitution is complete for every \(\alpha,\beta\). The \(E_5\) equations
then successively force, with only numerical pivots,
\[
\begin{gathered}
u_7=0,\quad a_{14}=u_6,\quad a_{10}=2\alpha a_{11},\quad
a_2=2a_5u_6,\\
a_1=-16a_{11}u_6+2a_{13}a_5+8a_8,\\
a_7=l_7-\tfrac34a_1+2a_{11}a_{13}+\tfrac32a_{13}a_5,\\
l_2=2a_5l_8,\qquad l_5=2a_{11}l_8.
\end{gathered}
\]
The three necessary \(E_4\) pivots then give the two proportional columns of
\(L_0\). Thus this is not merely an exhibited \(E_5\)-solution branch.

## 5. The corrected lower-syzygy table

The lower syzygy is exactly the \(r^1\) \(E_7\) matrix with its normal
coordinate interpreted as \((L_0)_{33}\). Computing the kernel of its first
four columns over every orbit gives exactly four zero-normal leaves:

| \((h,W)\) | spanning vector | exact lower constant |
|---|---|---:|
| \((p^3,pq^2)\) | \((\frac85p,q,0)\) | \(-24/5\) |
| \((p^2q,pq^2)\) | \((\frac52p,q,0)\) | \(-15/2\) |
| \((p^2q,p^2q)\) | \((-\frac12p,q,0)\) | \(3/2\) |
| \((p^3,p^2(p+q))\) | \((4p,-3p+q,0)\) | \(-12\) |

No other representative has a zero-normal lower kernel. Direct full
determinants give the stated \(E_5\) shapes/ranks
\[
(6,19)/6,\ (5,19)/5,\ (5,19)/5,\ (5,19)/5
\]
and the four constants above. The parallel fixed-\(E_7\) reconstructions give
\[
24/25,\quad15,\quad3/2,\quad-12.
\]

In particular, the corrected \((p^3,pq^2)\) leaf and its \(-24/5\) constant
are genuine and complete.

## 6. Coordinate exits and automorphism conclusion

The three exits are valid with the stated degree bounds.

1. A quadratic submersion has a constant derivative direction, hence a
   coordinate inverse of degree at most two.
2. For \(L^3+Q+\ell\), failure of a constant derivative direction forces a
   critical point by solving the Hessian equation on the quotient by its
   kernel. Hence a submersion of this form has coordinate inverse degree at
   most three.
3. For \(f=(y+c)r+g(x,y)\), absence of a critical point forces
   \(g_x(x,-c)\) to be a nonzero constant. Division by \(y+c\) gives the
   displayed shear with inverse degree at most six.

After using such a component as a source coordinate, the remaining two
components form a plane Keller map over \(\mathbb C(t)\) of degree at most
\(8,12,\) or \(24\), respectively. Base change to an algebraic closure of
\(\mathbb C(t)\) permits the established plane lower bound. The plane map is
birational, hence the original threefold Keller map is birational; the
birational Keller theorem then makes it a polynomial automorphism.

If every nonlinear piece is binary, target linear normalization followed by
the source shear in the third coordinate reduces directly to a degree-four
plane Keller map. Thus the theorem concludes automorphism, not merely
nonexistence of one chosen normal form.

## 7. Adversarial failures attempted

- all residual-root collisions in both \(A\)-families;
- \(B=0,\pm2\) in both double-root families;
- both roots of \(27\Lambda^2+4\);
- the depressed-cubic missing-linear chart and its pure-cube endpoint;
- general low-\(\rho\) cubics rather than one sample representative;
- both signs/conjugates of every pivot;
- rank drops in every displayed raw matrix;
- mixed zero-normal directions before setting a coordinate to zero;
- nonzero multiplier charts with \(g_1=0\);
- possible vanishing of \(\gamma+2\) in the quadratic quotient;
- special \(\alpha,\beta\) rank drops in the \(t4\) branch;
- candidate-only versus converse use of the \(t4\) substitutions;
- optimized Python and forged top identities;
- conclusion “no normalized solution” versus “automorphism.”

None produced a mathematical counterleaf.

## 8. Required/recommended corrections

1. **Resolved during audit:** the Python verifier initially had no
   `__debug__` guard, so `python3 -O` skipped every assertion and exited zero.
   The current file now rejects optimized execution, and the fail-closed test
   passes.
2. **Recommended clarification:** when \(g_1\ne0\), state why one may
   normalize \(g_1=1\). This is not homogeneity of \(E_6\). It uses the source
   scaling \(r\mapsto c r\) with \(c^2\) chosen appropriately over
   \(\mathbb C\), while the \(r^0\) parameters are rescaled. No branch is lost.
3. **Recommended documentation correction:** Section 10 says the promoted
   SymPy verifier prints every raw \(E_6\) dimension/rank and exact row
   reduction. It does not print all of those data. Either narrow that sentence
   or include the two audit reconstructions in the promoted verification
   package; the audit scripts do assert all claimed ranks and the missing
   \(t4\) converse pivots.

With items 2--3 treated as documentation/package cleanup, the theorem is
ready for promotion.

## 9. Reproduction

From `rung2_degree_bound/`:

```text
/usr/bin/python3 -u audit_binary_fixed_cubic_hostile/audit_orbits_lower_exact.py
/usr/bin/python3 -u audit_binary_fixed_cubic_hostile/audit_exceptional_branches_exact.py
./audit_binary_fixed_cubic_hostile/test_fail_closed.sh
```

Observed terminal sentinels:

```text
ALL INDEPENDENT ORBIT/LOWER CERTIFICATES PASSED
ALL INDEPENDENT EXCEPTIONAL-BRANCH CERTIFICATES PASSED
ALL FAIL-CLOSED TESTS PASSED
```
