# Corrected mixed-PPT lift in the cloud obstruction block

## Status

The corrected mixed-conjugate support formulation completely removes the
known cloud obstruction block.

Let \(\mathscr B\) be the seven-dimensional binary carrier of the local
Schur--Weyl type

\[
[4,1]\otimes[4,1]\otimes[3,2]
\]

after imposing pair antisymmetry, pair-exchange symmetry, and the first
Pluecker equation.  Both lifted Omega contractions vanish identically on this
carrier.

For every operator \(\rho\) supported on \(\mathscr B\), define

\[
\Phi(\rho)
=
\widehat{\mathcal C}_{\rm supp}
\rho^{\Gamma_A},
\]

where \(A\) is the first bivector factor and
\(\widehat{\mathcal C}_{\rm supp}\) is the exact mixed contraction from
\(\overline{\wedge^2\mathcal H}\otimes\wedge^2\mathcal H\otimes\mathcal H\)
to \(\wedge^2\mathcal H\otimes\overline{\mathcal H}\).

The exact result is

\[
\boxed{
\Phi\big|_{\operatorname{End}(\mathscr B)}
\text{ is injective}.
}
\]

Consequently

\[
\boxed{
\operatorname{ran}\rho\subseteq\mathscr B,qquad
\widehat{\mathcal C}_{\rm supp}\rho^{\Gamma_A}=0
\quad\Longrightarrow\quad
\rho=0.
}
\]

Neither \(\rho\succeq0\) nor \(\rho^{\Gamma_A}\succeq0\) is needed for this
block exclusion.

This is an exact classification of the known obstruction block, not a proof
of the corrected mixed-PPT relaxation over all local Schur--Weyl blocks.

## 1. Exact carrier construction

Use the point-module basis

\[
f_i=e_i-e_4,
\qquad 0\le i\le3,
\]

and the two-subset vectors

\[
r_{ab\mid cd}
=e_{\{a,c\}}-e_{\{a,d\}}-e_{\{b,c\}}+e_{\{b,d\}}.
\]

An exact basis of the local source before global replica constraints is formed
from

\[
f_i\otimes f_j\otimes r,
\]

where \(0\le i,j\le3\) and

\[
\begin{aligned}
r\in\{&r_{01\mid23},r_{01\mid24},r_{02\mid13},\\
      &r_{02\mid14},r_{03\mid14}\}.
\end{aligned}
\]

This gives 80 exact integer vectors.

Apply the commuting source projector

\[
P_{m src}
=P_{12}^-P_{34}^-P_{(12)(34)}^+(I-\mathcal A_4).
\]

Exact rational elimination proves that its image on this carrier has
dimension seven.  The verifier does more than find seven independent
columns: it solves for every one of the 80 projected columns in the chosen
seven-column basis and checks the reconstruction coefficient by coefficient
over \(\mathbb Q\).

The selected basis vectors also satisfy, exactly,

\[
\omega_{125}\nu_i=0,
\qquad
\omega_{345}\nu_i=0,
\qquad 1\le i\le7.
\]

Thus no Omega constraint is being omitted in the local calculation.

## 2. The mixed support map after partial transpose

Write a basis coordinate of the holomorphic source as

\[
(a,b)=\bigl((p,q),((c,d),z)\bigr),
\]

where \((p,q)\) is the first wedge coordinate and \(((c,d),z)\) is
the second wedge coordinate together with replica five.

Up to a common nonzero normalization, the mixed support contraction is

\[
\widehat{\mathcal C}_{\rm supp}
\bigl((p\wedge q)\otimes(c\wedge d)\otimes z\bigr)
=
\begin{cases}
(c\wedge d)\otimes q,&z=p,\\
-(c\wedge d)\otimes p,&z=q,\\
0,&z\notin\{p,q\}.
\end{cases}
\]

For real rational carrier vectors \(\nu_i,\nu_j\), partial transpose on the
first wedge gives

\[
\left(|\nu_i\rangle\langle\nu_j|\right)^{\Gamma_A}
_{(a,b),(a',b')}
=
\nu_i(a',b)\nu_j(a,b').
\]

These two formulas construct every matrix coefficient of

\[
\Phi_{ij}
=
\widehat{\mathcal C}_{\rm supp}
\left(|\nu_i\rangle\langle\nu_j|\right)^{\Gamma_A}
\]

using rational arithmetic only.

## 3. Exact injectivity certificate

There are \(7^2=49\) matrix units in
\(\operatorname{End}(\mathscr B)\).  Reduce the 49 sparse rational vectors
\(\Phi_{ij}\) modulo the prime

\[
p=1000003.
\]

Sparse Gaussian elimination gives

\[
\boxed{
\operatorname{rank}_{\mathbb F_{1000003}}
\{\Phi_{ij}:1\le i,j\le7\}=49.
}
\]

Every denominator occurring in the rational construction is invertible
modulo \(p\).  Full column rank after reduction implies full column rank over
\(\mathbb Q\), hence over \(\mathbb C\).  This proves injectivity of \(\Phi\).

The modular calculation is not numerical evidence: it is an exact finite
certificate.  The dependency-free verifier reconstructs all source vectors,
all replica projectors, the mixed contraction, and the modular elimination
from their definitions.

## 4. Consequences for the cloud obstructions

The vectors \(\xi\) and

\[
\zeta=\sqrt{21}\,\xi_+ + \sqrt{11}\,\xi_-
\]

belong to \(\mathscr B\).  Therefore no nonzero density operator supported
on their entire seven-dimensional orbit block can obey the corrected mixed
support equation.

In particular, a block-diagonal mixture with a physical equality moment in a
different block cannot repair this defect.  The equality moment has

\[
\widehat{\mathcal C}_{\rm supp}\rho_{\rm eq}^{\Gamma_A}=0,
\]

so for

\[
\rho=t\rho_{\mathscr B}+(1-t)\rho_{\rm eq}
\]

the support equation would still require

\[
t\widehat{\mathcal C}_{\rm supp}
\rho_{\mathscr B}^{\Gamma_A}=0.
\]

Injectivity forces \(t\rho_{\mathscr B}=0\).  Off-diagonal coherences between
different local blocks are a separate question and are not excluded here.

## 5. Scope and next finite problem

Exact conclusions:

- the corrected mixed-support equation is well defined at the density level;
- it is injective on the complete seven-dimensional binary cloud-obstruction
  carrier;
- the known \(\xi\) and \(\zeta\) directions do not survive the corrected
  relaxation;
- block-diagonal dilution by a physical equality state cannot restore them.

Not proved:

- injectivity or positivity in every other local carrier/block;
- exclusion of off-diagonal coherences coupling this block to another block;
- positivity of the full corrected mixed-PPT relaxation;
- DTH or any later Werner implication.

The next exact task is to decompose the full mixed moment problem, including
cross-block operator spaces, under the local mixed tensor algebra and test
each resulting finite block.

Completion estimate: 100% for the known seven-dimensional obstruction block;
approximately 10% for the full corrected five-replica mixed-PPT decision.

The exact checker is
`verification/agent_dth_ppt_block.py`.
