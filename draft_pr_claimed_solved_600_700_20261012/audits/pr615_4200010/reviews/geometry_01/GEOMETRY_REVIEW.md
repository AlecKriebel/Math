# PR #615 / problem 4200010: independent geometry and source-scope review

Review completed 2026-10-12 PDT. AI-assisted and unrefereed. The original
packet was read without modification. This review does not determine priority,
approve a PR merge, or authorize publication on its own.

## Verdict and exact verified claim

**PASS. No mandatory mathematical repair was found in the frozen geometry or
in its stated source interpretation.**

The packet constructs a connected closed smooth symplectic four-manifold of
Liouville volume one, a real smooth autonomous Hamiltonian, and an invariant
open band of Liouville volume exactly 1/4. Every full tangent Lyapunov exponent
in the band exists and equals zero at every point. Every connected energy
component there is ergodic for its normalized conditional measure and has a
nonprecompact Koopman orbit. No positive-Liouville-measure invariant subset of
the band has an almost-periodic Koopman representation. These conclusions
answer the printed existential question in the smooth symplectic category
with the conventional measure/spectral meaning of almost periodicity.

The derivative computation actually proves that this particular Hamiltonian
has zero exponents everywhere on its whole four-manifold. This is an optional
strengthening, not a required repair or a premise of the band argument.

The 24 frozen input files have unchanged hashes after replay; see
`FROZEN_INPUTS.json` and `REPLAY_SUMMARY.json`. In particular the full proof
hash is `541bc3c95d8f04b1d89cac3d2af21815ab331c7eeff9d79ff3591ba8f53eabd1`.

## 1. Smooth quotient, closed forms, and volume

Write the deck generator as

\[
 D(z,t,E)=(Fz,t-1,E),\qquad F(x,y)=(x+\sqrt2,y+x)\pmod{\mathbb Z^2}.
\]

The integer action is free because a fixed point of its n-th iterate would
require t-n=t, hence n=0. It is properly discontinuous because a compact
covering-space set has bounded t-coordinate, so only finitely many deck
translates can meet it. The smooth quotient N is the compact mapping torus
of a smooth diffeomorphism of the torus. It is connected because the original
torus and the gluing cylinder are connected.

The derivative of F is [[1,0],[1,1]] and has determinant one. Thus the covering
forms dx wedge dy and dt are invariant under D, and descend to closed forms
beta and tau on N. No asserted global real-valued coordinate x, y, t or E is
needed; their differential forms and the indicated vector fields have the
required deck equivariance. The second circle has its standard global closed
one-form dE.

On M=N times the E-circle,

\[
 \omega=\beta+\tau\wedge dE,\qquad
 \frac{\omega^2}{2}=\beta\wedge\tau\wedge dE.
\]

Both summands square to zero; their cross terms give the displayed density.
It is nowhere zero in covering coordinates. Hence omega is closed and
nondegenerate. Integration on the fundamental cell, whose seams have measure
zero, gives total volume one. The exact symbol-level checker confirms the
form's Pfaffian, its deck invariance, and its nondegeneracy.

**Attempted obstruction:** F is not isotopic to the identity on its original
torus, so it need not be a Hamiltonian map of that torus. This does not
invalidate a Hamiltonian flow on the different four-manifold M. Its vector
field and Hamiltonian are checked directly. Similarly, omega is nonexact:
its integral on an embedded torus fiber is one. Exact or Euclidean phase-space
claims would require a different argument, and are already excluded in the
frozen text.

## 2. Cutoff, Hamiltonian sign, invariant band, and energy components

For every real r at least one of r and 1-r is positive, so
eta(r)+eta(1-r)>0. The usual exponential-flat function eta is smooth, and the
quotient q is therefore smooth. It is zero for r<=0 and one for r>=1.

The two factors of chi force h(E)=E chi(E) to be identically zero for
E<=1/16 and E>=7/16 inside the chosen circle chart. Therefore h is zero on
neighborhoods of both seam endpoints and its periodic real extension is
smooth. This avoids the invalid globally real Hamiltonian H=E on a circle.
On the band I=(1/8,3/8), both factors are identically one. Hence h'=1 and
h''=0 there, exactly, rather than approximately.

Using the explicit convention i_X omega=dH,

\[
 i_{\partial_t}\omega=dE,\quad X_H=h'(E)\partial_t,\quad
 \Phi_s(q,E)=(\psi_{s h'(E)}q,E).
\]

The sign agrees with the deck identification: [z,t+n]=[F^n z,t], so the
first-return map at unit positive time is F. Reversing the global Hamiltonian
convention would reverse all times and preserve the conclusions.

The band N times I is open and invariant. Its measure is
1 times (3/8-1/8)=1/4. Completeness holds globally because M is compact and
X_H is smooth.

For E0 in I, h'(E0)=1, so E0 is an isolated point of the closed set
h^{-1}(h(E0)). Since N is connected, N times {E0} is a connected component
of the entire level set N times h^{-1}(h(E0)). It is regular along the
component. Other components, including any critical points elsewhere at the
same Hamiltonian value, do not change this local regularity assertion. The
candidate correctly avoids an unsupported claim that the energy is globally
a regular value.

**Attempted obstruction:** an individual slice N times {E0} is nonseparating
in M. A component of a real Hamiltonian level can be nonseparating when the
whole level has several components. There is no requirement that the single
component be the entire boundary of a sublevel region.

On the band the Liouville measure is nu dE and H=E, so its disintegration in
Hamiltonian energy is exactly nu=beta wedge tau. Thus the stated conditional
invariant measure has no omitted speed or coarea factor.

## 3. Global frame and all tangent directions

The frame is

\[
 V_1=\partial_x-t\partial_y,\quad V_2=\partial_y,
 \quad V_3=\partial_t,\quad V_4=\partial_E.
\]

The deck derivative sends V1 to
partial_x+(1-t)partial_y, exactly V1 evaluated at t-1. The other three
vectors are fixed. The frame is also unchanged under ordinary integer
translations in the torus and circle coordinates. It therefore defines a
smooth, everywhere independent frame on M and a genuine smooth global metric
by declaring that frame orthonormal.

To retain the transverse energy derivative, set b=h'(E) and c=h''(E).
On the cover, differentiating t+s b(E) gives s c in the t/E matrix entry.
Expressing source and target tangent vectors in the above global frame gives
the universal exact matrix

\[
 S_E(s)=\begin{pmatrix}
 1&0&0&0\\ s b&1&0&0\\0&0&1&s c\\0&0&0&1
 \end{pmatrix}.
\]

This formula is intrinsic, so it includes arbitrarily many seam crossings.
In a fundamental chart the integer return count contributes a coordinate
shear, and source/target frame changes convert it to the same real-time
formula. Fractional and negative times cannot change its sign or magnitude.
The checker verifies the identity for all formal real parameters s,b,c,t,
and verifies symplecticity and the inverse S_E(-s).

On the band b=1,c=0. Write S=Id+sP with P^2=0 and norm(P)=1. The triangle
inequality gives norm(S), norm(S^{-1})<=1+|s|. Consequently for every nonzero
v,

\[
 \frac{\|v\|}{1+|s|}\leq\|D\Phi_s v\|\leq(1+|s|)\|v\|.
\]

The logarithms divided by |s| squeeze to zero. This proves both upper and
lower limits for every vector; it does not infer zero exponents from one
positive-time upper bound or from an energy-tangential calculation. Metrics
on compact M are uniformly equivalent, so the conclusion is independent of
the chosen frame metric. In the full matrix, replacing 1 by the bounded
quantity max(|b|,|c|) proves zero exponents globally as well.

## 4. Measure and non-almost-periodicity cross-check

The Fourier pullback under F sends the character (k,l) to (k+l,l), times a
unit scalar. For l!=0, every invariant Fourier coefficient belongs to an
infinite distinct-index chain with equal absolute value. Square summability
forces it to vanish. Irrationality of sqrt(2) eliminates every nonconstant
l=0 invariant character. Haar measure on the torus is therefore ergodic.

An L2 function invariant under the full suspension flow is independent of t
almost everywhere inside product charts: its distributional t derivative
vanishes. The gluing then forces the remaining torus function to be
F-invariant. The suspension's volume nu is ergodic. Invariance under time one
alone would not suffice because it preserves the clock; the candidate uses
continuous-time invariance and does not make that error.

The fundamental-cell function G=exp(2 pi i y) is a valid measurable L2
observable. Its possible mismatch on a seam has measure zero. At integer n
its y phase is y+n x+sqrt(2)n(n-1)/2. Thus distinct integer translates have
zero inner product after integration in x. The infinite unit orthogonal orbit
is not precompact. This proves failure of almost periodicity on every
band energy component independently of the clock eigenfunctions.

For an arbitrary invariant measurable C in the band, take all rational times
first, then use Fubini and their countability. Almost every energy section is
invariant at all those times. Strong continuity extends this to every real
time: it follows from continuous functions by uniform continuity on compact
N, then L2 density and unitarity. Ergodicity makes each section full or null.
Therefore C equals N times J modulo null sets, for a measurable J. If C has
positive measure, the same orthogonal G orbit persists after normalization.
There is no invariant positive-volume subset escaping the witness.

Almost periodicity passes to invariant restrictions because restriction is a
bounded intertwining map. Hence an almost-periodic global region cannot meet
the band in positive measure. A maximal such region can be taken modulo null
sets: countable invariant unions retain orbit precompactness by finite-sum
approximation in L2, and a sequence approaching the supremum of measures
gives the maximal region. This is the appropriate measure-theoretic reading
of the source's maximal set; literal maximal point sets including arbitrary
null modifications would not be a well-defined invariant-measure question.

## 5. Full source-resolution verdict

The [original HTML list](https://people.math.harvard.edu/~knill/seminars/intr/)
and [printed list, page 2](https://people.math.harvard.edu/~knill/seminars/bozeman/intr-l.pdf)
agree: item 10 asks for positive Liouville measure outside an almost-periodic
invariant region and a positive-exponent region. No particular phase-space
manifold, exactness, analyticity, mechanical Hamiltonian, contact condition or
genericity is specified. Weak mixing appears in a separately marked guess.
The original item itself leaves almost periodicity informal. Its adjoining
discussion uses invariant measures and discrete spectrum; the manuscript's
precise Koopman convention is a defensible mathematical interpretation, not
an extra hypothesis removing the central difficulty.

The [cited 1998 spectral paper](https://people.math.harvard.edu/~knill/publications/knill_singularcontinuous1.pdf)
was inspected in full from fresh bytes. It treats Koopman operators and
spectral measures and supports the spectral context. Its Hamiltonian
corollary concerns a time-dependent unitary evolution on a function space,
not this finite-dimensional compact real Hamiltonian construction. It is not
a prior proof of the claimed four-dimensional band theorem.

In [Knill's 2016 discussion, section 4, printed page 8](https://people.math.harvard.edu/~knill/pde/pde.pdf),
almost periodicity of an invariant-measure dynamical system is expressly
identified with pure discrete Koopman spectrum. This corroborates the stated
definition but is not a formal retroactive amendment of the older list.

**Resolution verdict:** affirmative for the printed existential question in
the usual smooth symplectic and spectral interpretation. The result also
fails almost periodicity on each energy component, so it does not exploit
averaging continuously varying integrable frequencies. A manuscript may
accurately say it gives a positive answer to Knill's existence question in
this explicit category. It must keep the category and definition visible.
It must not claim the source's additional generic weak-mixing guess, a
prescribed Euclidean/cotangent realization, or historical novelty on this
geometry review's authority. No such stronger claim occurs in the frozen
proof. Priority remains a separate publication gate.

Fresh source-byte hashes and URLs are in `SOURCE_METADATA.json`. Complete
third-party PDFs, extracts and the page render are confined to the ignored
`sources.private/` directory and are not authored review deliverables.

## 6. Reproduction and mandatory repairs

Run `python3 -B check_geometry.py` in this review directory. It imports no
candidate code and verifies 16 universal formal polynomial identities, plus
four negative controls. The controls reject the wrong frame sign, reversed
return shear, omitted transverse energy derivative, and omitted real-time
shear. These are algebraic validations, not a replacement for the analytic
arguments above.

Also replayed unchanged: the candidate's 3,248 exact checks, its six controls,
the existing audit's 2,460 exact checks and eight controls, all four prior
manifest mutation controls, and both manifests. Results are recorded in the
review JSON files. Counts report coverage rather than proof strength.

**Mandatory repairs: none for the frozen geometric theorem.** Keep the
already present scope and AI/unrefereed statements when preparing the
preprint. Adding a brief maximal-region lemma or the later terminology
reference would improve exposition but is not necessary to repair the proof.
Any revised manuscript must be audited against its own final bytes.
