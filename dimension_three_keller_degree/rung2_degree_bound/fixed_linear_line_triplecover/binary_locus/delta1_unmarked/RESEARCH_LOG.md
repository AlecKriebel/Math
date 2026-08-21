# Research log: fixed-linear binary \(\delta=1\), unmarked divisor

All timestamps are UTC.

## 2026-07-25T13:18:00Z — unmarked component opened

- Used the affine source stabilizer of the fixed point \(p=0\) to place an
  unmarked common divisor at \(q=0\).
- A target change normalizes the \(p^3\)-coefficients of \((A_3,B_3)\)
  to \((0,1)\).  The common-root equations then force
  \(A_3=q^2(a_2p+a_3q)\) and
  \([p^2q]R=(3/4)b_1[p^3]R\).
- The minimal tangent is the divided directional gradient
  \[
  N=q^{-1}\left(\partial_q-\frac{b_1}{4}\partial_p\right)(P,Q,R).
  \]
- Opened the exact contact calculation with every remaining coefficient
  retained.  No exclusion is claimed yet.

## 2026-07-25T13:37:05Z — one genuine contact component provisionally closed

- On the generic chart
  \(a_2=c_0=b_1=1,\ b_2=0\), the contact eliminant splits into three
  rational factors and one irreducible cubic factor.  The
  \(a_3=3/10\) and \(a_3=13/20\) rational leaves jump to higher gcd
  strata; \(a_3=1/2\) is a genuine exact-\(\delta=1\) family.
- Parameterized that family by \(z\).  Its exact open is
  \(z(64z-1)\ne0\), and its nonzero contact tangent has an exact lower
  homogeneous solution through \(E_5\).
- The constant part of \(E_4\) reduces to two independent quartics times
  \(M_1,M_2\).  Their coefficient minor is \(-9216z^2\), so
  \(M_1=M_2=0\), and the literal nonzero vector
  \((1,-4,2u_1)^T\) lies in the kernel of the linear part.
- SymPy reconstruction and an independent PARI/GP replay both pass.
  This closes only the \(a_3=1/2\) contact component, provisionally.

## 2026-07-25T13:50:07Z — circular simplification removed

- An earlier exploratory calculation had specialized free \(E_5\)
  coefficients before examining \(E_4\), which could have manufactured
  the displayed kernel.  The proof and both verifiers were rebuilt with
  \(\ell_{13},\ell_{23},\ell_{32},x_2,y_2,u_3,v_3\) retained.
- The corrected \(E_4\) identity produces the same kernel directly and
  the strict dual-CAS suite still passes.  Added an explicit hostile
  checklist requiring this freedom to be retained.

## 2026-07-25T13:58:58Z — cubic contact factor rerouted to \(\delta\ge3\)

- Solved the degree-three eliminant component over
  \(\mathbb Q[a]/(160a^3-384a^2+310a-85)\).
- The contact coordinates simplify to
  \[
  b_3=-5(2a-1)/16,\quad
  c_2=-3(10a^2-19a+8)/20,\quad
  c_3=-(120a^2-198a+79)/320.
  \]
- Each reduced minor has the same explicit monic quadratic factor \(G\).
  Together with the chart divisor \(q\), this gives gcd degree at least
  three.  Thus this entire algebraic contact component does not meet
  exact \(\delta=1\); no lower-identity calculation is needed.
- Added independent SymPy and PARI/GP reconstructions.  Promotion awaits
  the component-saturation hostile audit.

## 2026-07-25T14:04:18Z — \(b_1=0\) boundary provisionally closed

- On the \(a_2c_0\ne0,b_1=0\) boundary, normalized
  \(a_2=c_0=1,b_2=0\) without dividing by \(b_1\).
- Three contact coefficients give \(bc=0\), then \(b=0\), including the
  \(c=0\) endpoint.
- Every resulting contact point has the common minor divisor
  \(q(2p+3a q)\), so it lies in \(\delta\ge2\), not exact \(\delta=1\).
- Thus exact \(\delta=1\) has zero tangent and the all-binary
  automorphism exit.  Dual-CAS certificates pass; normalization and
  zero-tangent replay await hostile audit.

## 2026-07-25T14:12:07Z — \(c_0=0\) boundary provisionally closed

- After normalization, exact contact has a single orbit:
  \((a,b,d)=(1/2,-1/8,1/4)\).  A nonzero cubic resultant certifies the
  elimination, and direct factors certify exact gcd one.
- Legal target/source/target gauges reduce the nonzero-tangent lower
  equations to three parameters \(u_0,v_2,w\).
- With every free \(E_5\) coefficient retained, \(E_4\) forces two row
  covariants to vanish and gives the literal kernel
  \(L(9,-36,16w)^T=0\).
- Independent SymPy and PARI/GP full weighted-determinant replays were
  added.  Promotion awaits hostile normalization and gauge audit.

## 2026-07-25T14:21:02Z — final \(a_2=0\) boundary provisionally closed

- Avoided the large finite contact decomposition: on \(a_2=0\), the
  first contact coefficient is \(-3a_3/4\) times the \(q=0\) endpoint
  coefficient of \(\alpha/q\).
- Contact therefore makes \(\alpha/q\) divisible by \(q\), while
  \(\beta/q,\gamma/q\) already visibly contain \(q\).  Thus every contact
  point has \(q^2\) in the original gcd and leaves exact \(\delta=1\).
- The identity is division-free in \(b_1,c_0\), so it includes all
  intersections of the previous boundary charts.  Dual-CAS replays were
  added.

## 2026-07-25T14:31:00Z — generic contact saturation tree packaged

- Split \(d=0\), \(d\ne0,a=0\), and the two successive pivot divisors
  \(D=0,E=0\) before taking the open resultant.
- The \(d=0\) component consists of exactly three higher-gcd points.
  Both pivot failures are explicit points of the half family.
- On the fully open chart, the only viable resultant factors are the
  half family and the cubic higher-gcd component; the apparent quadratic
  factor has empty fibre, and \(a=13/20\) returns to \(d=0\).
- Added a primary exact case-tree verifier and a synthesis wrapper that
  runs every independently checked leaf.  The completeness claim still
  awaits an independent saturation audit.
