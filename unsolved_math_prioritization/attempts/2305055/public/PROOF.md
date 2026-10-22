# L-atoms on the disk and on arbitrary plane domains

## 0. Attribution and logical inputs

DannyExperiments' 2026 manuscript [D, Version 2.1, §§2–5] publicly gives the
disk theorem, the compact-inverse-image criterion and the arbitrary-perturbation
surjectivization argument. The proof below reconstructs those mechanisms with
an explicit Runge exhaustion justification and an independent error budget.
Section 5 adds a short planar separator lemma, deriving the same equivalence
for unbounded plane domains as well. No historical originality is asserted.

Classical inputs are the open mapping theorem, the holomorphic inverse
function theorem, isolated zeros, local uniform limits of holomorphic
functions, the maximum principle, ordinary Runge approximation on plane
domains, and Rouché's theorem. The Runge form used is: if K is compact in an
open plane domain Omega and Omega minus K has no component relatively compact
in Omega, every function holomorphic near K is uniformly approximable on K
by functions holomorphic on Omega. We give the necessary topology below.

## 1. Definitions and the compact-image criterion

Fix a plane domain U. A sequence escapes U if, for each compact A subset U,
only finitely many of its terms lie in A. For h in O(U), put G_h=h(U).
The L-property means that the image sequence escapes G_h. An ordered pair
(f,g) means that escape of f(z_n) in G_f implies escape of g(z_n) in G_g
on every source-escaping sequence. A nonconstant alpha is an L-atom if every
ordered first partner f can be expressed as phi composed with alpha for a
holomorphic phi on G_alpha.

For a subset S of a plane domain G, write S relatively compact in G when its
closure in C is compact and is contained in G. For nonconstant f,g in O(U),

\[
(f,g)\text{ is ordered}
\quad\Longleftrightarrow\quad
f(g^{-1}(K))\text{ is relatively compact in }G_f
\quad\text{for every compact }K\subset G_g.                 \tag{1}
\]

**Proof.** Suppose the right side holds. Whenever g fails to escape G_g,
infinitely many g-values belong to one compact K. The corresponding f-values
belong to a single compact subset of G_f by (1). Thus f fails to escape as
well, which is exactly the contrapositive of the required ordering.

Conversely, take compact exhaustions A_n of U and C_n of G_f, each increasing
with interiors covering its domain. If (1) fails for K, the set
S=f(g^{-1}(K)) is not contained in any compact subset of G_f. The set

\[
B_n=f(A_n\cap g^{-1}(K))
\]

is compact in G_f: its source is closed in the compact A_n. Select
z_n in g^{-1}(K) with f(z_n) outside the compact C_n union B_n.
Then z_n is outside A_n, so the source sequence escapes; f(z_n) escapes G_f,
while g(z_n) remains in K. This contradicts orderedness and proves (1).

A constant f has singleton image, cannot have the L-property, and is always
a constant pullback. It may therefore be handled separately everywhere below.

## 2. Two Runge topology facts

Call a compact K subset Omega Runge if no component of Omega minus K has
compact closure contained in Omega.

### 2.1 A Runge compact exhaustion exists

Here is a verification for arbitrary plane domains. For a nonempty compact
C subset Omega, define its holomorphic hull by

\[
\widehat C=\{w\in\Omega: |h(w)|\le\max_C|h|
                   \text{ for every }h\in O(\Omega)\}.
\]

The coordinate function bounds this hull in C. If Omega is proper, put
delta=dist(C,C minus Omega)>0. For each a outside Omega the function
1/(w-a) is holomorphic on Omega, so membership in the hull implies
|w-a| >= min_{v in C}|v-a| >= delta. Thus the hull stays at distance at
least delta from the complement. It is closed relative to Omega and therefore
compact in Omega. For Omega=C, its boundedness and closedness already suffice.

If V were a relatively compact component of Omega minus the hull, its boundary
would be contained in the hull. The maximum principle, applied separately to
every h in O(Omega) on V, would put every point of V in the hull, a
contradiction. Consequently the hull is Runge.

Start with any cofinal compact exhaustion of Omega. Recursively take a compact
neighborhood, still contained in Omega, of the previous hull and the next
exhaustion member, and replace it by its hull. This produces Runge compacta
E_n with E_n contained in the interior of E_(n+1), and their interiors cover
Omega. In particular, every prescribed compact subset of Omega is contained
in the interior of some E_n.

### 2.2 One isolated disk may be adjoined

Let K be Runge in Omega, let V be a component of Omega minus K, and assume
the closed disk of center a and radius 2r is contained in V. Then

\[
K\cup\overline{D(a,r)}                                      \tag{2}
\]

is Runge in Omega. Indeed, removing the inner disk from V leaves a connected
set: a point with r<|w-a|<3r/2 can move radially to the circle of radius 3r/2;
from any other point a path in V to a can be stopped at its first meeting with
that circle. These paths avoid the inner closed disk, and the circle itself
connects their endpoints. The remaining component cannot be relatively compact
in Omega, since adjoining back the inner disk would then make V relatively
compact, contrary to K being Runge. Other components are unchanged. This
proves (2), including when V or Omega is unbounded or multiply connected.

## 3. Surjectivization with a prescribed analytic perturbation

**Lemma.** Let alpha in O(U) be nonconstant, let Omega=alpha(U), and fix any
b in O(U). There exists H in O(Omega) for which

\[
F=H\circ\alpha+b:U\longrightarrow\mathbb C
\]

is onto. No boundedness assumption on b is needed in this lemma.

**Proof.** Omega is a plane domain. Choose the exhaustion in §2.1. We construct
Runge compacta K_n, holomorphic H_n on Omega, and disks Delta_n. Begin with
K_0=E_1 and H_0=0. At stage n>=1, the open set
alpha^{-1}(Omega minus K_(n-1)) is nonempty. Since the zeros of alpha' are
isolated, it contains a point x_n with alpha'(x_n) nonzero. This only requires
a regular preimage, not a value all of whose preimages are regular.

Set a_n=alpha(x_n). There is a holomorphic local inverse s_n of alpha near
a_n. Choose r_n>0 so that the closed disk of radius 2r_n is contained both
in the inverse-branch neighborhood and in the component of Omega minus
K_(n-1) containing a_n. Let Delta_n=D(a_n,r_n), and define near its closure

\[
P_n(w)=\frac{n+2}{r_n}(w-a_n),\qquad
q_n(w)=P_n(w)-b(s_n(w)).                                    \tag{3}
\]

The compact K_(n-1) union closure(Delta_n) is Runge by §2.2. Its two pieces
have disjoint neighborhoods. Prescribe H_(n-1) on the old piece and q_n on
the new one. Ordinary Runge approximation with epsilon_n=4^(-n) supplies
H_n in O(Omega) such that

\[
\sup_{K_{n-1}}|H_n-H_{n-1}|<4^{-n},\qquad
\sup_{\overline\Delta_n}|H_n-q_n|<4^{-n}.                    \tag{4}
\]

Take K_n to be a sufficiently late E_j whose interior contains
K_(n-1), closure(Delta_n), and E_n. All old disks are thus protected against
later corrections, and the K_n remain cofinal.

The first bound in (4), together with summability of 4^(-n), gives local
uniform convergence H_n to some H in O(Omega). For a fixed n, its own
approximation error and all subsequent corrections yield

\[
\sup_{\overline\Delta_n}|H-q_n|
\le T_n:=\sum_{j=n}^{\infty}4^{-j}
=\frac{4^{1-n}}3\le\frac13.                               \tag{5}
\]

Let xi be any complex number with |xi|<=n. On the boundary of Delta_n,
|P_n-xi| >= n+2-|xi| >=2, whereas (3)–(5) imply

\[
|(H+b\circ s_n-\xi)-(P_n-\xi)|\le\frac13<2.
\]

The affine map P_n-xi has precisely one zero inside Delta_n, because that
zero is a_n+r_n xi/(n+2), at distance at most r_n n/(n+2)<r_n from a_n.
Rouché's theorem therefore gives a zero w in Delta_n of H+b composed with
s_n-xi. At z=s_n(w) we have F(z)=xi. Consequently the whole closed disk
|xi|<=n is contained in F(U) for every n, and F(U)=C.

This is an infinite existence argument. No finite numerical search is
substituted for Runge approximation, uniform convergence, or Rouché's theorem.

## 4. Reconstruction of the prior disk result

Take U=D. If alpha is injective, alpha is biholomorphic onto its image;
for every holomorphic f, the function phi=f composed with alpha^{-1} is
holomorphic on G_alpha and f=phi composed with alpha. Thus alpha is an L-atom.

If alpha is not injective, choose p!=q with alpha(p)=alpha(q). Apply §3
with b(z)=z. The resulting F has image C and is H composed with alpha + z.
For every nonempty compact K subset G_alpha (the empty case is trivial),

\[
|F(z)|\le\max_{w\in K}|H(w)|+1\qquad(\alpha(z)\in K).       \tag{6}
\]

Thus F(alpha^{-1}(K)) is bounded, hence relatively compact in its actual
image C. Formula (1) makes (F,alpha) ordered. However,

\[
F(p)-F(q)=p-q\ne0,
\]

so F cannot be a function of alpha. This contradicts atomicity and proves
the disk equivalence. This result and mechanism are credited to [D].

## 5. Separate consequence for every plane domain

Call b in O(U) alpha-moderate if b is bounded on alpha^{-1}(K) for every
compact K subset G_alpha. The following elementary separator avoids using
the possibly unbounded coordinate function on an unbounded domain.

**Separator lemma.** Suppose alpha(p)=alpha(q)=c with p!=q in U. Let m>=1
be the finite zero order of alpha-c at p, and put

\[
b(z)=\frac{\alpha(z)-c}{(z-p)^m}\quad(z\ne p),               \tag{7}
\]

with its removable value at p. Then b is alpha-moderate and b(p)!=b(q).

**Proof.** Locally alpha(z)-c=(z-p)^m u(z), where u is holomorphic and
u(p)!=0. Consequently b extends holomorphically across p with b(p)=u(p),
whereas b(q)=0. Choose delta>0 with the closed disk closure(D(p,delta))
contained in U. Continuity gives a finite number
B=max_{|z-p|<=delta}|b(z)|. For nonempty compact K subset G_alpha, let
M_K=max_{w in K}|w-c|. Every point of alpha^{-1}(K) either lies in that
closed source disk or satisfies |z-p|>=delta. In the latter case (7) gives
|b(z)|<=M_K/delta^m. Hence

\[
\sup_{\alpha^{-1}(K)}|b|
\le\max\{B,M_K/\delta^m\}<\infty.                          \tag{8}
\]

This estimate covers all finite boundary approaches and escape to infinity
simultaneously. It does not require alpha^{-1}(K) to be compact or connected.

**Theorem for plane domains.** Under the compact-source-escape definition of
§1, the L-atoms on any plane domain U are exactly its injective holomorphic
functions.

**Proof.** The injective direction is the inverse-map argument of §4. If
alpha is noninjective, take (7), and apply §3 to this fixed holomorphic b.
The resulting F=H composed with alpha+b maps U onto C. On each compact
alpha-inverse image, both summands are bounded by continuity of H on K
and (8). Thus (F,alpha) is ordered by (1). But F(p)-F(q)=b(p)-b(q)!=0,
so F does not descend through alpha. Therefore alpha is not an L-atom.

The separator uses the global plane coordinate z-p. The proof does not
assert that an analogous bounded-on-tubes separator exists on every open
Riemann surface. No such surface classification follows merely by replacing
z-p with an arbitrary local coordinate.

## 6. Adversarial checks and boundaries of the conclusion

1. **Ordering:** all compact estimates prove the contrapositive
   'alpha fails L implies F fails L', giving the exact required direction.
2. **Actual range:** without F(U)=C, bounded values could tend to an omitted
   point. For example, z in D is bounded but escapes its actual range along
   z_n=1-1/n. Surjectivity is indispensable to the boundedness argument.
3. **Critical fiber:** m in (7) is the full multiplicity. If one divided only
   by z-p at a multiple zero, both b(p) and b(q) could be zero; that weakened
   construction would not supply the separator.
4. **Inverse branches:** no global inverse of alpha is assumed. Only one
   regular preimage per auxiliary island is used; other sheets are irrelevant.
5. **Topology:** the disks have a double-radius collar disjoint from the
   previous Runge compact. One cannot add arbitrary compact sets that create
   relatively compact holes and still invoke the same approximation theorem.
6. **Tail:** every previous island is inside all later protection sets, so
   its infinite error tail is bounded by (5). Checking just H_n on its own
   island would not suffice for the limit H.
7. **Surjectivity:** each entire target disk is covered by Rouché; a dense
   image or interpolation on countably many targets is not substituted.
8. **Quantifiers:** H depends on b. Choosing b=-H composed with alpha after
   H was fixed invalidates a universal-H-for-all-analytic-b claim.
9. **Finite controls:** the script checks the arithmetic identities and
   diagnostic examples only. It is not a formal proof of these theorems.

## References

[D] DannyExperiments, *Rubel's L-atoms on the disk and a several-variable
counterexample*, manuscript Version 2.1, release 1.0.0, 5 August 2026.
[Immutable TeX](https://github.com/DannyExperiments/rubel-l-atoms/blob/65b6668e63e7fa3aec7ff28e36396f0a59af2aa9/paper/manuscript.tex).
This is an AI-assisted, unrefereed public proposed proof; its correctness is
assessed by the reconstruction above, not by its stated audit count.

[HL] W. K. Hayman and E. F. Lingham, *Research Problems in Function Theory*,
arXiv:1809.07200v2 (2018), Problem 5.55, printed p. 106; related Problem 2.56,
printed p. 43. [Primary PDF](https://arxiv.org/pdf/1809.07200v2).

[KN] T. Kalmes and M. Nieß, *Composition and differentiation operators and
fast approximation*, J. Approx. Theory 164 (2012), 57–76,
doi:10.1016/j.jat.2011.09.007, Lemma 2, author-manuscript p. 4.
[Author manuscript](https://www.tu-chemnitz.de/mathematik/analysis/kalmes/Preprints/Composition_and_differentiation_operators_and_fast_approximation_manuscript.pdf).
This verifies the established escaping-islands approximation background;
the proof above instead spells out the recursive ordinary-Runge route.
