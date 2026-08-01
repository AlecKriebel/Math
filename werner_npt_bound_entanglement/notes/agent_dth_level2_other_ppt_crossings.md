# The remaining grouped PPT crossings at DTH degree three

## Scope

This note closes the local representation layer for the two grouped PPT cuts
not covered by the anchored bivector crossing.  It supplies exact local
censuses and exact diagram-crossing oracles for

\[
 \Gamma_z,\qquad \Gamma_{A_1A_2}.
\]

It does **not** prove that the fixed five-replica obstruction has a positive
degree-three extension.  Candidate spectra and crossing-cache residuals
reported below are discovery-layer numerical data.

The seven replicas are ordered as

\[
 A_1=(1,2),\quad A_2=(3,4),\quad A_3=(5,6),\quad z=7.
\]

## 1. Exact grouped-cut reduction

The degree-three source is invariant under permutations of the three
bivector factors.  For every Hermitian density (T) and every replica subset
(S),

\[
 (T^{\Gamma_S})^{\mathsf T}=T^{\Gamma_{S^c}}.
\tag{1}
\]

Full transpose preserves the spectrum.  Bivector-factor permutations
identify all one-(A) cuts and all two-(A) cuts.  Consequently the three
independent grouped PPT representatives are

\[
 \Gamma_A,\qquad \Gamma_z,\qquad \Gamma_{AA}.
\tag{2}
\]

For computation, (1) and pair symmetry give the lossless complement identity

\[
 \operatorname{spec}(T^{\Gamma_{A_1A_2}})
 =\operatorname{spec}(T^{\Gamma_{A_1z}}).
\tag{3}
\]

We call the right-hand crossing (\Gamma_{Az}).

## 2. Exact local mixed-module censuses

Partial transpose on (t) local replicas changes the local module from
((\mathbb C^3)^{\otimes7}) to

\[
 \overline{\mathbb C^3}^{\otimes t}
 \otimes(\mathbb C^3)^{\otimes(7-t)}.
\]

For (\Gamma_z), (t=1).  The dominant highest weights, multiplicities, and
carrier dimensions are

\[
\begin{array}{c|rrrrrrrrr}
\lambda&(6,0,-1)&(5,1,-1)&(5,0,0)&(4,2,-1)&(4,1,0)&
(3,3,-1)&(3,2,0)&(3,1,1)&(2,2,1)\\ \hline
m_\lambda&1&5&6&9&24&5&30&26&21\\
d_\lambda&63&60&21&42&24&15&15&6&3.
\end{array}
\tag{4}
\]

For (\Gamma_{AA}), (t=4):

\[
\begin{array}{c|rrrrrrrrrr}
\lambda&(3,0,-4)&(3,-1,-3)&(3,-2,-2)&(2,1,-4)&(2,0,-3)&
(2,-1,-2)&(1,1,-3)&(1,0,-2)&(1,-1,-1)&(0,0,-1)\\ \hline
m_\lambda&1&3&2&2&12&18&9&33&24&23\\
d_\lambda&90&60&21&48&42&24&15&15&6&3.
\end{array}
\tag{5}
\]

The complementary (t=3) census for (\Gamma_{Az}) is

\[
\begin{array}{c|rrrrrrrrrr}
\lambda&(4,0,-3)&(4,-1,-2)&(3,1,-3)&(3,0,-2)&(3,-1,-1)&
(2,2,-3)&(2,1,-2)&(2,0,-1)&(1,1,-1)&(1,0,0)\\ \hline
m_\lambda&1&2&3&12&9&2&18&33&24&23\\
d_\lambda&90&48&60&42&15&21&24&15&6&3.
\end{array}
\tag{6}
\]

The involution

\[
 (a,b,c)\longmapsto(-c,-b,-a)
\tag{7}
\]

takes (6) exactly to (5), with multiplicities and carrier dimensions
unchanged.  This is the local contragredient form of (3).

For every one of (4)--(6),

\[
 \sum_\lambda m_\lambda d_\lambda=3^7,
 \qquad
 \sum_\lambda m_\lambda^2=2761.
\tag{8}
\]

### Exact proof

On each dominant integral weight space, form the two raising maps for
(E_{01}) and (E_{12}).  Covariant legs contribute (+E); contravariant legs
contribute (-E^{\mathsf T}).  Modular row reduction gives an upper bound on
the characteristic-zero common-kernel dimension.  The bounds in (4)--(6),
weighted by the Weyl carrier dimensions, already exhaust all (3^7)
dimensions.  Complete reducibility forces every bound to be exact and
excludes omitted irreducibles.

The dependency-free replay is

```text
python verification/verify_dth_level2_other_ppt_censuses.py
```

## 3. Exact matrix-free crossing oracle

Let (P_\pi) be the seven-replica permutation diagram.  For any one of the
three subsets above, define

\[
 \Delta^S_\mu(\pi)
 =G_\mu^{-1}H_\mu^\dagger
   \Gamma_S(P_\pi)H_\mu,
\tag{9}
\]

where (H_\mu) is an exact rational highest-weight basis and
(G_\mu=H_\mu^\dagger H_\mu).  If (X_\lambda) are holomorphic multiplicity
blocks, finite-group Fourier inversion gives

\[
 a_\pi={1\over7!}\sum_\lambda f^\lambda
 \operatorname{Tr}(R_\lambda(\pi^{-1})X_\lambda),
 \qquad
 Y_\mu=\sum_{\pi\in S_7}a_\pi\Delta^S_\mu(\pi).
\tag{10}
\]

Equations (9)--(10) are an exact rational, matrix-free crossing oracle.
The verifier checks the identity diagram, all six adjacent generators, and a
seven-cycle.  For every audited pair (\pi,\sigma), it proves exactly

\[
 \sum_\mu d_\mu
 \operatorname{Tr}\!\left(
   \Delta_\mu^S(\pi)^\sharp\Delta_\mu^S(\sigma)
 \right)
 =3^{c(\pi^{-1}\sigma)},
\tag{11}
\]

and

\[
 \sum_\mu d_\mu\operatorname{Tr}\Delta_\mu^S(\pi)
 =3^{c(\pi)}.
\tag{12}
\]

Thus the exact audit proves the crossing orientation, trace normalization,
nonorthogonal Gram convention, and Hilbert--Schmidt isometry on a generating
diagram family.  It does **not** certify the signs of any floating-point
candidate eigenvalues.

The replay is

```text
python verification/verify_dth_level2_other_local_crossings.py
```

## 4. Numerical full crossings and the complement bridge

`discovery/agent_dth_level2_other_local_crossings.py` evaluates all (5040)
diagrams and stores the normalized (2761\times2761) local crossings.  The
observed weighted-isometry/trace errors were

\[
\begin{array}{c|cc}
\text{cut}&\text{weighted-isometry Frobenius error}&\text{trace error}\\\hline
\Gamma_z&8.95\,10^{-15}&2.66\,10^{-15}\\
\Gamma_{AA}&9.03\,10^{-15}&2.33\,10^{-15}\\
\Gamma_{Az}&8.95\,10^{-15}&3.11\,10^{-15}.
\end{array}
\tag{13}
\]

The untracked cache hashes are respectively

```text
acd61f2a810e14fa926a00fd1b8b9125ca577805ac94a59385bfee3598ea8cf6
a8d0bc09aa57f34ee68dbc9d2720e863931f0b40fdcef9faa11610f4a4496931
ca5652b509735ba59fb1b890ac15659992abc9f08eb9e03d1f5abaf0c656b33e
```

There is an efficient relative bridge.  Let (C_A) and (C_{Az}) be the two
normalized crossing matrices, let (H) repeat the holomorphic carrier
dimensions, and let (D_A) repeat the mixed (\Gamma_A) carrier dimensions.
Weighted isometry gives the exact formula

\[
 B_{A\to Az}=C_{Az}H C_A^{\mathsf T}D_A,
 \qquad B_{A\to Az}C_A=C_{Az}.
\tag{14}
\]

Numerically, the reconstruction error in (14) is (3.60\,10^{-15}) and the
weighted-isometry error is (3.54\,10^{-15}).  All 39 nonzero local bridge
blocks have numerical Choi rank at most two; the maximum Choi asymmetry is
(2.30\,10^{-15}).  These rank statements are numerical, not exact.

The bridge builder is

```text
discovery/agent_dth_level2_complement_bridge.py
```

## 5. Site-orbit candidate streaming

`discovery/agent_dth_level2_cross_other_candidate_orbits.py` consumes any
of the crossing caches and reconstructs only the 112 site-orbit
representatives.  It supports signed Choi--Gram streaming and direct
four-index contraction.  For (\Gamma_z), every nonzero local crossing block
has numerical Choi rank at most two.  For direct (\Gamma_{AA}) the largest
rank is 166, while direct (\Gamma_{Az}) lowers it to 53; selected small
blocks remain safe to stream without assembling a dense global operator.

As a discovery check, crossing the round-four (\Gamma_A)-corrected source
gave material negative blocks under both new cuts.  At cap 500,

\[
 \lambda_{\min}^{\Gamma_z}=-3.4839610312\,10^{-10}
 \quad\text{in block }(0,5,7),
\]

with trace quotient (-0.0983111).  At cap 100,

\[
 \lambda_{\min}^{\Gamma_{Az}}=-8.8280373324\,10^{-10}
 \quad\text{in block }(1,1,9),
\]

with trace quotient (-0.235747).  These values only disprove PPT of that
particular numerical extension.  They are not an obstruction to the
existence of another extension and not a physical DTH counterexample.
