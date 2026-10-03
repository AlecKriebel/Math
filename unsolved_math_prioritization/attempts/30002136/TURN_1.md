# Turn 1: exact universal reductions and certification contract

2026-10-03 07:31 UTC. Substantive author turn 1/5. **NO FULL RESOLUTION.** Completion estimate toward the full discovery goal: 3% (planning estimate, not probability of truth).

## 1. Signed exponent sums are forced

Write e_a(w),e_b(w) for the exponent sums. Evaluate b at I and a at diag(x,y,(xy)^(-1)). The trace is x^p+y^p+x^(-p)y^(-p), where p=e_a(w). Laurent monomials are linearly independent; this expression determines the integer p. Indeed its exponent multiset is {(p,0),(0,p),(-p,-p)} with multiplicities, and the only nonzero exponent on the positive/negative x axis is (p,0); p=0 is the constant 3 case. Thus universal SL3 equivalence forces e_a(u)=e_a(v), and similarly for b. Commuting diagonal representations give no information about ordering beyond these exponent sums.

## 2. Universal trace equality already forces inverse traces

For any representation rho, its contragredient rho*(g)=rho(g)^(-T) is again a homomorphism F2→SL3(C), since (MN)^(-T)=M^(-T)N^(-T). Apply the hypothesized equality to rho*: tr(rho(u)^(-1))=tr(rho(v)^(-1)).

For M∈SL3(C), its characteristic polynomial is z^3−tr(M)z^2+tr(M^(-1))z−1. Therefore equality of the universal standard traces implies equality of the characteristic polynomials at every representation. The converse is immediate. Cayley–Hamilton then gives equality of every positive and negative power trace as well. This equivalence is special to the universal quantifier and this dimension; equality of one scalar trace for one pair of matrices does not determine their characteristic polynomials. It does not assert that u and v induce the same matrix-valued word map.

This also confirms that a nontrivial word cannot be universally equivalent to its inverse by an SL2-style argument. The known dominant-word-map obstruction receives credit to Borel as used in Lawton–Louder–McReynolds §4.3; it is not reproved or claimed novel here. The source imposes no exclusion of proper powers, so none is added.

## 3. Extension to GL3 and positive polynomial identities

For arbitrary invertible A,B choose cube roots alpha^3=det A, beta^3=det B and write A=alpha A0, B=beta B0 with A0,B0∈SL3(C). Then w(A,B)=alpha^(e_a(w)) beta^(e_b(w)) w(A0,B0). Equal exponent sums prove that universal SL3 equivalence is equivalent to universal GL3 equivalence. For positive words, trace entries are polynomials in the eighteen matrix entries. Equality on GL3×GL3, a dense open subset, is therefore equivalent to the polynomial identity on all pairs of 3×3 matrices. This last extension cannot simply substitute singular matrices into signed words.

## 4. A finite, exact identity test for any fixed signed pair

Let L and U be arbitrary lower/upper unitriangular 3×3 matrices and D=diag(s,t,(st)^(-1)), with s,t nonzero. The product LDU lies in SL3 and parameterizes its open Gaussian cell. A has a unique such decomposition whenever its first and second leading principal minors are nonzero: pivots are s and st. This cell is dense in irreducible SL3. Use independent eight-parameter cells for A and B.

Every word trace is then a Laurent polynomial in four invertible diagonal parameters and twelve ordinary triangular parameters. A proposed fixed pair is universally equivalent if and only if their Laurent-polynomial difference is exactly zero, equivalently every coefficient vanishes after clearing a sufficient monomial denominator. This is a decidable fixed-pair certificate, not a proof that a nonconjugate pair exists and not a finite reduction of the unrestricted search. Coefficient growth is a practical obstruction; it supplies no universal length bound.

The exact checker verifies the determinant, inverse, and characteristic-polynomial algebra and supplies a tiny source-credited negative control: the positive words aababbaabbab and aababbabaabb discussed by Lawton–Louder–McReynolds are separated by the integer SL3 matrices A=[[1,1,0],[0,1,1],[0,0,1]] and B=[[1,0,0],[1,1,0],[1,1,1]]. Their traces are 2187 and 2180. This is a disproof of this one candidate, not of all candidates. Both words are nonconjugate, checked by cyclic rotation of cyclically reduced words.

## Remaining gap and next route

No pair survives to a universal identity certificate and no argument separates arbitrary word pairs. The next route is an unbounded special-family theorem using exact diagonal/permutation substitutions, followed by bounded exact negative certificates only if they illuminate remaining families. Standard invariant-theory reductions and prior finite searches are not being advertised as novel discoveries.
