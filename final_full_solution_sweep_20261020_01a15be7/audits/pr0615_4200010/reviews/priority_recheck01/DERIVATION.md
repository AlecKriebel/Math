# Independent check of the classical implication

This is a new audit derivation, not a proposed publication or claim of a newly
proved phenomenon. The target is the unrestricted smooth symplectic reading of
Knill's 2000 item 10, with almost periodicity meaning precompact Koopman orbits
in the entire L2 space of a restricted invariant measure. Invariant subsets are
understood modulo null sets. A discrete-spectrum factor is not a good subset.
The separately marked weak-mixing/genericity guess is outside this target.

## Classical input and its exact match

Anzai (1951), printed pp.91-92, treats T_m(x,y)=(x+alpha,y+mx) on the two-torus,
with alpha irrational and nonzero integer m. Its displayed formula (39) shifts
Fourier indices (p,q) to (p+mq,q), with a phase. The corollary states ergodicity
and continuous spectrum on the orthogonal complement of functions depending
only on x. At m=1 this is the candidate's exact map, not just a related family.

The geometry needed to turn its suspension into a Hamiltonian system is also
explicitly classical: de Leon-Saralegi (1993), Lemma 3.2, p.5036, gives the
symplectic form Omega+eta wedge ds for a cosymplectic pair. Page5037 describes
the extended Hamiltonian and permits an S1 thickening using its length form;
p.5042, equation(6.3), identifies the extended Hamiltonian of h=0 with the Reeb
field. The circle remark establishes a symplectic extension, not a globally
real circle-coordinate Hamiltonian. The latter must still be constructed.

## 1. No new ergodic or spectral mechanism

For F(x,y)=(x+alpha,y+x),

    F^n(x,y)=(x+n alpha, y+n x+alpha n(n-1)/2)

for every integer n. Its derivative and inverse grow at most linearly in |n|.
The character e_(k,l) is sent to a scalar times e_(k+l,l). Invariance forces
the absolute values of Fourier coefficients to be constant along each such
orbit. If l is nonzero, square summability forces these coefficients to be
zero. If l=0, irrationality kills every k except zero. Thus F is ergodic.
For g=exp(2 pi i y), the characters of g composed with F^n have pairwise
different x-frequencies, so these translates are orthogonal at distinct
integer times. This is a direct instance of the exact older Fourier shift.

## 2. Suspension and the Hamiltonian extension

Let N be the mapping torus with (z,t) identified with (Fz,t-1). The invariant
closed forms dx wedge dy and dt descend to beta and tau, with total volume
integral of nu=beta wedge tau equal to one. R=partial_t is the Reeb field.
Its complete flow psi_s has psi_n[z,t]=[F^n z,t] at integer n.

The real suspension flow is ergodic: an invariant L2 function is independent
of t in interior product charts, by the vanishing distributional derivative.
Invariance under time one then makes the remaining function F-invariant, so
constant. This uses time-one invariance as an L2 identity; it does not assume
that an arbitrary L2 representative has a trace agreeing at the seam. The
time-one map alone is not ergodic, since it fixes the fractional t-coordinate.

On N times (0,1), put omega=beta+tau wedge dE and H=E. Direct contraction gives
i_R omega=dE, so this is the classical Hamiltonian realization. Its full
Liouville measure is nu dE, finite total one. Every energy has the same
compact conditional system (N,nu,psi). The flow is complete because E stays
fixed and N is compact. Nothing here substitutes one null energy surface for
a band of positive four-dimensional measure.

## 3. Compact ambient space with a real Hamiltonian

For compactness, take M=N times S1 with the same symplectic expression. Choose
a smooth real function h on S1 that equals the real chart coordinate E on
I=(1/8,3/8), and vanishes near the circle seam; a standard smooth cutoff
supported in (1/16,7/16) supplies it. Then H=h(E) is a genuine global real
Hamiltonian and X_H=h'(E)R. On B=N times I the flow is exactly psi_s in each
fiber and the full normalized Liouville volume is |I|=1/4. This standard
cutoff changes no mechanism. Completeness follows from compactness.

## 4. All tangent exponents, including transverse energy

The frame V1=partial_x-t partial_y, V2=partial_y, V3=partial_t,
V4=partial_E descends because the gluing sends V1(t) to V1(t-1) and fixes the
other frame vectors. At an energy E, write c=h'(E), k=h''(E). In this frame,

    D Phi_s = I+s c L+s k K,
    L(V1)=V2, K(V4)=V3,

and both generators vanish on the other frame vectors. Every product of two
generators is zero. Hence the inverse is I-s c L-s k K. On compact M both
c and k are bounded; derivative and inverse have norm at most 1+C|s|. Every
vector and singular-value Lyapunov exponent is consequently zero. On B,
c=1 and k=0; the energy direction is actually fixed. This does not use the
invalid implication that zero entropy alone forces every pointwise exponent
to vanish. The exact coordinate-to-frame identity is separately checked by
independent_controls.py.

## 5. No positive invariant almost-periodic subregion

Let C be an invariant measurable subset of B of positive measure. Apply
Fubini to the invariance of its indicator at each rational time and intersect
the resulting countable family of full-measure energy sets. At almost every
energy, the section is invariant at all rational times. Strong continuity
of the unitary group, proved first on continuous functions on compact N and
then by L2 density, makes it invariant at every real time. Ergodicity of psi
forces each section to be empty or full modulo nu-null sets. Thus C=N times
J modulo null sets, for some measurable J of positive length.

The L2 function G([x,y,t])=exp(2 pi i y) in the measurable fundamental domain
0<=t<1 is valid even though it is not smooth across the seam. On N times J,
its integer-time translates have squared norm |J| and pairwise zero inner
products, by the Fourier calculation in step1 and integration in t and E.
Their pairwise distance is sqrt(2|J|), so the orbit is not precompact. Thus C
cannot be a good region. A good region of all M meeting B positively would
restrict to a good invariant subregion in B, since restriction is a bounded
intertwiner taking precompact sets to precompact sets. This is impossible.
The band therefore lies outside both good and bad modulo null sets.

## Consequence and bibliographic boundary

The exact unrestricted existence conclusion follows by the standard
suspension and Hamiltonian extension of Anzai's map, plus elementary frame,
cutoff and measure-disintegration arguments. The checks above locate no
remaining central difficulty or new mechanism in the candidate. The cutoff
and positive-volume safeguards are necessary for a correct presentation,
but do not restore a substantive novelty claim for this target.

This does not prove that any older paper explicitly answered the later named
Knill question. No such explicit earlier answer was authenticated by this
recheck. The proof establishes a direct classical implication, not historical
firstness in either direction. An attributed expository corollary may be
useful; it does not clear the present workflow's novel-full-solution priority
gate. A restricted Euclidean, natural-mechanical, analytic, contact, generic
or weak-mixing target would require a different theorem and is not supplied
by this PR.
