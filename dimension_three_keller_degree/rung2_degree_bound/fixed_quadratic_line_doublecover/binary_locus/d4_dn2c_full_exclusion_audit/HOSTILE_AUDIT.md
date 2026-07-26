# Hostile final audit — `D4-DN-2C`

**Audit time:** 2026-07-26 UTC

**Verdict:** **PASS**, conditional only on the theorem scope stated below.

**Terminal marker:** `D4_DN2C_FULL_EXCLUSION_HOSTILE_AUDIT_STRICT_PASS`

This is an AI-assisted hostile audit of exact computation.  It is not peer
review.  A passing certificate is evidence about the algebra encoded in the
scripts; it is not evidence for the completeness of the larger quartic
taxonomy or for worldwide priority.

## Authorized theorem and forbidden inferences

The audited theorem is:

> Over \(\mathbb C\), let
> \(F=L(p,q,r)^t+H_2+H_3+H_4\), with
> \(H_4=(P,Q,0)\), \(H_3=(U,V,R)\), and \(H_2=(A,B,T)\) homogeneous
> of the indicated degrees.  If its normalized binary top data are
> \[
> h=(p+q)^2,\qquad P=hp^2,\qquad Q=hq^2,\qquad
> R=h(p-2q)
> \]
> and \(F\) is Keller, then \(F\) is a polynomial automorphism.

Equivalently, this one frozen canonical family contains no Keller
counterexample.  The audit does **not** prove any of the following:

- exclusion of the parent fixed-quadratic row;
- exclusion of every exact-\(\delta=4\) family;
- exclusion of every quartic Keller counterexample;
- a universal degree lower bound; or
- completeness of the global fourteen-row taxonomy.

The strict audit contains a required-failure mutation which replaces the
family-only disclaimer by a quartic-wide assertion.  That mutation is
rejected.

## Files and independent routes inspected

The audit read and ran:

1. the frozen SymPy contact atlas in `d4_dn2c_full_rebuild`;
2. the primary complete SymPy descent in `d4_dn2c_full_descent`; and
3. the direct PARI/GP lower reconstruction in `d4_dn2c_pari_lower`.

The first source PARI calculation intentionally started from the frozen
contact atlas and was therefore independent only for the lower descent.
During this audit the source package added
`explore_contact_atlas_pari.gp`: a direct generic-determinant reconstruction
of the \(E_7\) kernel, complete set-theoretic \(E_6\) projection, two-plane
split, all-eighteen-variable rank atlas, and every line/origin boundary.  Its
strict wrapper now ends with
`D4_DN2C_DIRECT_PARI_FULL_FAMILY_STRICT_PASS`.

This audit also retains a shorter independently written check,
`verify_contact_exhaustiveness_pari.gp`, which uses a different constant
\(-144\) minor to derive the same radical and frozen boundaries.  Neither
PARI script imports SymPy output.

As a supplemental derivational check, the separately parameterized
`d4_dn2c_cleanroom` SymPy package was run after its mutation guard was
repaired and ended with `D4_DN2C_CLEANROOM_STRICT_PASS`.  The PASS verdict
does not count that same-CAS replay as the methodologically independent
check; the direct PARI reconstruction supplies that role.

## Formula and completeness audit

### 1. Top data and \(E_7\)

- Direct differentiation confirms
  \[
  \{Q,R\}=-6pq(p+q)^3,\quad
  -\{P,R\}=6p(p+q)^3(p+2q),\quad
  \{P,Q\}=8pq(p+q)^4.
  \]
- Removing \(2p(p+q)^3\) gives the documented contact equation
  \[
  -3qU_r+3(p+2q)V_r+4q(p+q)T_r=0.
  \]
- The three coefficient blocks have ranks \(2,3,4\), hence nullities
  \(0,2,4\).  The displayed six-parameter kernel satisfies the contact
  equation identically.  The eleven binary coefficients are absent from
  \(r\)-derivatives and remain free.

### 2. Complete \(E_6\) projection

- The four documented \(r^3\) coefficients were recomputed.  The first,
  \(-6d^2\), forces \(d=0\); the remaining equations then force \(z=0\)
  set-theoretically in characteristic zero.
- With \(d=z=0\), the six \(r^1\) equations use only
  \(a_{r^2},b_{r^2}\).  The audit-local PARI reconstruction finds the
  constant coefficient matrix
  \[
  \begin{pmatrix}
  0&0\\-12&24\\-36&84\\-36&108\\-12&60\\0&12
  \end{pmatrix}
  \]
  and the constant pivot \(-144\).
- After that solve, the first residual is
  \(\frac23(2b+3y)^2\).  On \(2b+3y=0\), the remaining nonzero residuals
  are \(-f_0/3,-2f_0/3,-f_0/3\), where
  \[
  f_0=8a^2+24ax+27x^2-18xy+9y^2.
  \]
  This proves the set-theoretic projection in both directions without
  relying on a resultant or denominator clearing.
- Over \(\eta^2=-2\), direct multiplication confirms
  \[
  \bigl(9x+(4+2\eta)a+(-3+3\eta)y\bigr)
  \bigl(9x+(4-2\eta)a+(-3-3\eta)y\bigr)=3f_0.
  \]
  Substitution shows the two planes meet exactly on \(2k+3s=0\), giving
  \((a,b,x,y)=(k,k,-2k/3,-2k/3)\); its only omitted point in the punctured
  chart is \(k=0\), the origin.
- The full-lower atlas retains all eighteen lower columns.  Its nonzero
  pivots and exact ranks are:

  | chart | localization | pivot | rank |
  |---|---|---:|---:|
  | plus plane | \(2k+3s\ne0\) | \(93312(\eta-1)(2k+3s)^2\) | 7 |
  | minus plane | \(2k+3s\ne0\) | \(93312(-\eta-1)(2k+3s)^2\) | 7 |
  | common line | \(k\ne0\) | \(186624k\) | 6 |
  | origin | none | \(31104\) | 5 |

  Solving each displayed minor and substituting into all thirteen equations
  proves equality of coefficient and augmented ranks.  Therefore no
  denominator-defined contact component is omitted.

### 3. Transverse plane interiors

- The primary coefficients \([p^3r^2]E_5\) and
  \([p^2qr^2]E_5\), including the factors \(Q_1,Q_2\) and denominators
  \(162,243\), agree with direct determinant reconstruction.
- The displayed Bézout identity for \(Q_1(1,t),Q_2(1,t)\) expands to one.
  At \(k=0\), the coefficient \(18-45\eta\) has norm \(4374\), so the
  projective point at infinity is not lost.
- Independently, PARI obtains three lower-free cubics whose projective gcd
  is \((3t+2)/486\); their \(k=0\) values are all nonzero.  Thus the only
  common zero is the removed common line.  Conjugation covers the minus
  plane.

### 4. Punctured common line

- Both systems recompute this chart before division by the vanished plane
  pivot.
- The primary safe pivots are
  \(186624k,-64k^3/9,-32k^3,-2k^2/3,4k^2\).
  PARI deliberately selects different minors, obtaining
  \(186624k,-16k^3/3,32k^3,2k,-4k^2\).
  Every pivot divisor is already excluded by \(k\ne0\); the differences are
  changes of pivot, not discrepancies.
- The primary reduced \(E_5\) ideal is exactly
  \(\langle\mathcal Q,\mathcal A\mathcal B\rangle\), checked by equality of
  reduced Gröbner bases.  \(E_4\) forces
  \(\mathcal S=0\), after which \(\mathcal Q=\mathcal D^2\).
- On \(\mathcal B=0,\mathcal A\ne0\), the residual factor
  \(\mathcal F_B\) divides \(\det L\), so the Keller condition fails.
  The boundary \(\mathcal A=0\), including the overlap, is recomputed.
- On \(\mathcal A=0\), the square compatibility \(\mathcal C^2=0\) is
  solved without a new divisor.  The documented signs in
  \(\mathcal F_A\) now agree with the encoded polynomial.  If
  \(\mathcal F_A=0\), then \(\det L=0\).  Otherwise the \(E_3\) pivot is
  \(k^2\mathcal F_A^2/144\), and both remaining residuals are
  \(k\mathcal F_A^2/288\), a contradiction.
- For both determinant factorizations, the verifier checks that the
  purported quotient has denominator one; neither “divides” assertion is
  the tautology obtained by defining a rational quotient.
- The direct PARI descent uses a different compatibility tree:
  \(S=0,T_\Delta=0,YB=0\), then \(B=0\), then \(YW=0\).
  The \(W=0\) branch has \(\det L=0\).  On \(Y=0,W\ne0\),
  \([p^3]E_3=kWH\); after the divisor-free \(H=0\) solve, the remaining
  residuals are both \(-kW^2/2\).  This independently closes the same
  punctured chart.

### 5. Origin and plane exit

- The fresh constant pivot \(31104\) gives the five documented formulas.
  The coefficients
  \[
  [p^3r]E_4=-3b_{qr}^2,\qquad
  [q^3r]E_4=\frac23(3b_{qr}+2L_{33})^2
  \]
  force \(b_{qr}=L_{33}=0\).  Literal substitution kills all five pivot
  values and hence all six nonbinary quadratic coefficients.
- All nonlinear terms are then binary.  The PARI verifier constructs
  \(\operatorname{adj}(L)\) and checks
  \[
  \operatorname{adj}(L)L=\det(L)I,\qquad
  \partial_r\widetilde F_1=\partial_r\widetilde F_2=0,\qquad
  \partial_r\widetilde F_3=\det L,
  \]
  together with
  \[
  \det J_{p,q}(\widetilde F_1,\widetilde F_2)
   =\det L\,\det JF .
  \]
  Hence the first two transformed coordinates form a plane Keller map of
  degree at most four.  Moh's unconditional degree-\(<100\) theorem makes
  it an automorphism, and the third coordinate is a triangular lift.

## Defects found and resolution

The first hostile read found four omitted plus signs in the displayed
\(\mathcal F_B,\mathcal F_A\) formulas.  The encoded formulas were correct;
the note was corrected.  It also found:

- “recorded exactly” for an \(H_A\) factor which is computed but not printed;
  this now reads “computed exactly”;
- an undefined \(K(k)\) after the note was scoped to \(\mathbb C\); this now
  reads \(\mathbb C(k)\); and
- incomplete publisher metadata for the Moh reference; it now follows the
  publisher record.

All blocking defects were corrected in the source package before this PASS.

## Mutation and runtime audit

The aggregate strict run requires:

- all frozen-atlas, primary SymPy, direct-PARI contact-atlas, lower-descent,
  and full-family markers;
- rejection of optimized Python;
- rejection of corrupted transverse and origin identities in the primary
  package;
- rejection of corrupted doubled-contact, projective-gcd, and final-\(E_3\)
  identities in the direct PARI package;
- rejection of a quartic-wide scope mutation; and
- rejection of a corrupted direct-PARI contact quadratic.

No resultant, denominator clearing, numerical sampling, or irreducibility
assumption is used in the audited exclusion.
