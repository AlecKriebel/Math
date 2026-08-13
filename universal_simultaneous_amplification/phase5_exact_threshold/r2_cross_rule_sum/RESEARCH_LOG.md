# Research log: normalized cross-rule endpoint at fitness two

## 2026-08-13 09:53 PDT -- exact shared-arrow tree reduction

- Fixed the decisive sufficient endpoint target

  ```text
  m_L/b_n + m_D/d_n <= 2,
  b_n=n*2^(n-1)/(2^n-1),
  d_n=(n-1)*2^(n-2)/(2^(n-1)-1).
  ```

- Derived its exact common-denominator tree numerator

  ```text
  S_n=2*b_n*d_n*Z_L*Z_D-d_n*Y_L*Z_D-b_n*Z_L*Y_D
     =sum_(A,B) tau_L(A)tau_D(B)
        (2*b_n*d_n-d_n*|A|-b_n*|B|).
  ```

- Proved that the same sign is one root-cost sum for the independent product
  generator `L tensor I + I tensor D`: product-chain cofactors differ from
  `tau_L(A)tau_D(B)` by one positive root-independent factor.
- Specialized the weighted adjoint to fitness two.  Since the reference
  `mu(A)=(r-1)^|A|` is uniform, `L^T=C+V` has only a diagonal defect; hence
  `L(B,A)=C(A,B)` off diagonal.  Reversing a whole `L` in-tree gives a
  weight-preserving `C` out-tree.
- Combined this with the exact fair-geometric targetwise expansion

  ```text
  G_v=sum_(j>=0) 2^(-j-1) S_v^j N_v,
  (I-S_v/2)(G_v-I)=C_v/2.
  ```

  The minimal literal object is therefore a paired out-`C` tree and an
  in-tree made of target-locked histories of the same row arrows.
- Recorded the exact algebraic bridge through `m_C`, but did not assume the
  two pieces have separate signs.
- Reconciled this with the earlier r=2 tree-reflection route closures:
  complement rerooting, fixed-skeleton transport, and fixed-length labelled
  history injection are already exactly false on `K_3`.  A proof of the
  paired sign must use global cancellation between the two tree factors.
- Exact weighted three-path fingerprint:

  ```text
  b=12/7, d=4/3,
  m_L=584/341, m_C=118/75, m_D=6/5,
  2-m_L/b-m_D/d=1033/10230 > 0.
  ```

- **PROVED:** all reductions above.
- **OPEN:** the single all-graph paired-tree sign `SAPT_n`, equivalently the
  normalized cross-rule endpoint inequality.

## 2026-08-13 10:18 PDT -- weaker decisive product and local obstruction

- Added the weaker target `m_L*m_D<=b_n*d_n`, which by itself rules out
  simultaneous strict amplification at fitness two.
- Derived both of its exact shared-arrow tree forms:

  ```text
  P_n=b_n*d_n*Z_L*Z_D-Y_L*Y_D
     =sum_(A,B) tau_L(A)tau_D(B)(b_n*d_n-|A||B|),
  ```

  and, for the dB event-tree cofactors `theta_D`,

  ```text
  P_n^event=b_n*d_n*Z_L*Phi_D-Y_L*Theta_D
           =sum_(A,B)tau_L(A)theta_D(B)
                    (b_n*d_n/|B|-|A|).
  ```

- Compared the arithmetic and product root costs exactly.  Their difference
  is `(b_n-|A|)(d_n-|B|)`; this is sign-indefinite in precisely the relevant
  amplifier--suppressor regime.
- Exactified the first local obstruction on unweighted `K_3`.  A supported
  `L` skeleton has conditional mean `b_3=12/7`, while the dB state-star
  centered at mask `001` forces its only supported in-root to mask `110`, of
  rank two.  Both the conditional arithmetic and product gaps equal `-1/2`.
  Therefore neither target can be signed one pair of tree skeletons at a
  time; a proof must exchange mass globally among skeletons.
- Weighted-P3 product fingerprint:

  ```text
  1-m_L*m_D/(b_3*d_3)=172/1705 > 0.
  ```

- **OPEN:** `PAPT_n`, the weaker decisive shared-arrow product-tree sign.

## 2026-08-13 12:02 PDT -- collision insertion and common-arrow two-step forcing

- Collapsed the post-neutral `C` reciprocal-rank observable exactly.  For
  `k=|A|` and internal directed request mass `I_P(A)`,

  ```text
  g(A)=k*(N_C (1/|.|))(A)
      =1                                  (k=1),
      =1+I_P(A)/(k*(k-1))                 (k>=2).
  ```

  Consequently `beta_C f=(sum tau_C(A)g(A))/Y_C`.
- Derived the stationary internal-mass identity
  `E_piC I_P(A)=m_C/2` from the exact `C` rank drift `k-2I_P(A)`.
- Split the event-Palm product gap, without assigning separate signs, into

  ```text
  1/m_D-m_L/(b*d)
   =(1/m_D-beta_C f)+(beta_C f-m_L/(b*d)).
  ```

  The second bracket is the global determinant numerator
  `b*d*Z_L*sum(tau_C*g)-Y_L*Y_C` after positive normalization.
- Exactly refuted the tempting statewise comparison `K_D f>=K_R f`: on the
  weighted three-path with edge weights `1,2`, the minimum pointwise
  difference is `-17/280`.  Its stationary persistence term remains
  positive, exactly `7/1416`.
- Added the common-arrow marked reduction.  With
  `q_L(C,v)=pi_L(V\C)/m_L`, the first marked step satisfies

  ```text
  (M psi)(C,v)=1                                  (|C|=0),
               =1/(k+1)+P_v(C)/(k*(k+1))          (k>=1).
  ```

  Defining
  `F_P(A)=sum_(v in A)(M^2 psi)(V\A,v)` gives the exact normalization
  `E_piL F_P=m_L*q_L*M^2*psi`.  Thus the proposed two-step floor is exactly

  ```text
  E_piL F_P >= m_L^2/(b*d).
  ```

  It is also the mean of the symmetric two-copy forcing
  `(F_P(A)+F_P(A'))/2-|A||A'|/(b*d)` under `pi_L tensor pi_L`.
- Derived and independently enumerated a closed local-arrow formula for
  `F_P(A)` for complement-cache rank at least two.  It uses only the
  one-step cut masses, their squares, the cache internal mass, and two
  quadratic new-sample masses: the row-square sum `sum P_vi^2` and
  `sum P_vi` times the incoming-plus-outgoing cache mass at `i`; no marked
  resolvent remains.
- Weighted-P3 exact fingerprint:

  ```text
  q_L*M^2*psi=123/146,
  E_piL F_P=492/341,
  b*d*E_piL F_P-m_L^2=296960/813967 > 0.
  ```

- **OPEN:** the all-graph common-arrow two-step floor and its proposed
  persistence for every time `t>=2`.  The next proof-first target is the
  complete radial two-copy Poisson solve for this exact forcing, followed by
  a pointwise residual/SOS audit.

## 2026-08-13 12:40 PDT -- common marked current and product-Poisson obstruction

- Put the two rules on one literal marked space.  The complemented occupied
  `L` Palm measure is

  ```text
  lambda_L(C,v)=pi_L(V\C),   lambda_L 1=m_L,
  ```

  while the normalized stationary dB marked law `mu_D` satisfies
  `mu_D psi=1/m_D`.  At the complete kernel `lambda_L=b_n U`, with `U` the
  complete marked dB law.  Hence the decisive product target is exactly

  ```text
  1/m_D-m_L/(b_n*d_n)=mu_D psi-lambda_L 1/(b_n*d_n).
  ```

- Inverted the marked continue/stop branches exactly to obtain a closed
  pointwise formula for `(lambda_L M_P)(D,w)` in terms of `pi_L` on the
  neighbouring occupied sets and the same row-`P` arrows.
- With `g` the actual marked group-inverse potential, derived the single
  current/covariance identity

  ```text
  m_L*(1/m_D-m_L/(b*d))
   =lambda_L*(M-I)*g + lambda_L*psi-m_L^2/(b*d).
  ```

  On the weighted path the radial covariance is `-293/581405`, while the
  marked current is `739/5115`; their sum is `50224/348843>0`.  Thus the
  two summands cannot be signed separately.

- For the exact two-step forcing `F_P`, formed the two-copy target

  ```text
  G_P(A,B)=(F_P(A)+F_P(B))/2-|A||B|/(b_n*d_n).
  ```

  If `Phi` solves the complete product Poisson equation
  `-Q_K^x Phi=G_K`, stationarity gives the exact shared current

  ```text
  E G_P=E [G_P+Q_P^x Phi].
  ```

- Exactified the first pointwise strengthening as false.  On the weighted
  three-path `w01=1,w02=2,w12=0`, the residual minimum is

  ```text
  -107/288 at (A,B)=(001,101),
  ```

  split as marked forcing `-25/144` plus generator current `-19/96`.
  Fourteen of 49 ordered pairs are negative.  The stationary integral is
  nevertheless `18560/116281>0`.
- Therefore the canonical complete radial product potential does not give a
  pointwise supersolution.  A proof must add a zero-mean overlap/full-pair
  correction or group the currents globally into cycle/tree packets.
- The bare overlap correction `H(A,B)=|A intersect B|` is already too
  coarse.  At `(A,B)=(001,111)` its product-generator drift is zero while
  the residual is `-11/36`; hence no graph-dependent scalar multiple of
  this overlap drift can repair the pointwise sign.
- **PROVED:** all normalizations and current identities above.
- **REFUTED:** pointwise complete radial product-Poisson closure.
- **OPEN:** the integrated two-step floor and `PAPT_n`.
