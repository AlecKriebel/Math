# Independent source/scope derivations — record 23217863

This continues the immutable early reconstruction. These are mathematical
checks of the literal seven-page manuscript and its exact external proof
interfaces, not a source repair. All current sibling/root evaluations remain
unread. The historical deposited audits were consulted only after the early
seal and the independent reconstruction of the relevant primary mechanisms.

## 1. Exact imported cohomology

Family 295 Theorem 1.1 really uses bounded **complex multilinear** maps with
values in the same algebra, ordinary multilinear norm, and the actual image
of the standard Hochschild differential. Its statement ranges over every
complex von Neumann algebra and every integer k≥2. Neither a cb norm nor a
normal-cochain-only quotient is substituted. The fresh pinned/current PDFs
and the bundled PDF agree byte for byte. The controlling upstream sections
1–5, complete 28-page reader, wrapper and proof map were read.

Here is my reconstruction of the load-bearing proof, rather than an appeal
to deposited audit conclusions or the existence of Lean declarations.

For a separable-predual tracial II₁ algebra, Popa's ultraproduct independence
theorem supplies finitely many Haar unitaries free from any prescribed
separable coefficient algebra in a factor ultrapower. In Popa's actual
Theorem 0.1(a), take every coordinate algebra/subalgebra equal to the II₁
factor P. A nonzero diffuse corner cannot intertwine into a finite matrix
amplification of C; the full ultrapower is a factor. The relative commutant
is C, so the required independence is scalar-trace freeness. Iteratively
adjoin each selected Haar unitary, keeping the coefficient algebra separable.
This proves exactly the instance used in upstream Lemma 2.2. No free unitary
inside the original P, free from all P, is asserted.

Each finite path has one fresh label appearing nowhere else in that tested
list. Expanding coefficient unitaries into scalar and centered parts leaves
a nonempty reduced distinguished-letter word between centered coefficients;
freeness makes each trace zero. A finite family of such tests can be realized
at one coordinate of the ultrapower. For a separable II₁ algebra with center,
countable measurable unitary sections are fiberwise 2-dense; take the first
tuple satisfying the finite open trace conditions. This gives measurable
unitaries in the original algebra. No nonseparable disintegration is used.

Use p_l=2^{-2^l}, n_l=p_l^{-3/2}, K_l=l n_l, d_l=K_l^4 and a positive dense
base measure. At stage l there are finitely many relevant labeled path lists
and reduced words, however enormous their numbers. Simultaneous finite
requirements are therefore legitimate. Four bad-event bounds are

    (16/15) l sqrt(p_l),  K_l^{-1},  1/(2K_l²),
    l exp(-p_l^{-1/2}).

They all tend to zero. Labels are sampled before evaluating unitaries, so
coinciding unitary values do not invalidate the collision bound. The measure
is fixed before the harmonic map is chosen. This is convergence of moments
in probability, not convergence of polynomial operator norms.

For a harmonic bounded-ball-2-continuous map T, D(g)=T(g)g* evaluated along
the walk is an L²(M)-valued bounded martingale. Orthogonal increments give
E||Z_n-Z_h||₂²≤e_h→0 uniformly n≥h. If its limit has distinct support points
a,b, the forward half and reverse-inverse half use disjoint increments and
are independent. Their endpoint replacement errors tend to zero. This yields
positive probability of D(G)≈a and D(G^{-1})≈b; it does **not** assume G and
G^{-1} independent. Concatenating signed blocks is a genuine fresh walk only
when their unsigned block indices are distinct. For each fixed finite size
m, the positive conditioning probability c_m is obtained before choosing a
sufficiently late subsequence time; no uniform lower bound on c_m is needed.

The first ultrapower consequently has exact free Haar generators g_i and
R(w)=aw or bw according to the first sign, for distinct unsigned indices.
Bounded-ball continuity gives a uniform modulus on each norm ball, preserves
the tracial ideal, and transfers to each ultrapower. Scalar moment convergence
alone was used before reaching this exact free family.

Now s_r=r^{-1/2}Σg_i has norm≤2 by the free-group length inequality. Its proof
separates the exact number of boundary cancellations; each cancellation piece
is a direct sum of matrices with Hilbert–Schmidt norm bounded by the ℓ² norm
of the length-q coefficients. Summing q+1 pieces gives the stated estimate.
Faithful trace moment roots transfer the regular-representation norm to the
containing algebra. This proof does not silently assume strong convergence
of the original random matrices/products.

In an ordered product of blocks z(z*z)^d, free reduction never eliminates a
whole block: each reduced block starts and ends positively; boundaries join
two positive letters. A reduced coefficient of length q is bounded by
3^L r^{-q/2}, by recording a noncrossing partial matching of the original L
positions. Repeated **surviving** unsigned indices occupy at most
2^q binom(q,2) r^{q-1} words. Their ℓ² norm is O_L(r^{-1/2}), and the length
inequality makes their operator norm tend to zero. Repeated original labels
which disappear remain in coefficients of retained words. Thus the distinct
index identities pass to every ordered block product in a second ultrapower.

The limiting s*s has Catalan moments: the leading identity reductions have
d distinct labels, a noncrossing perfect matching and C_d(r)_d assignments;
fewer labels contribute O_d(r^{d-1}). Compact support in [0,4] identifies the
spectral law as (2π)^{-1}sqrt((4-x)/x)dx, with no atom at zero. Faithfulness
and finiteness make the polar part V unitary. Polynomial approximation of
(s*s+epsilon)^{-1/2}, followed by bounded-ball 2-continuity, transfers all
ordered positive and negative power identities to V. No commutation of s
with s*s is introduced.

Finally H_m(z)=Σ_{k≤m}z^k/k has uniformly bounded imaginary part, while its
real part is at least cos(1)h_m on a rotated arc of length≤1/m. Boundedness
of R bounds (a-b)Re H_m(lambda V). Right multiplication by the reciprocal
on each arc gives ||(a-b)e_j||≤C/(cos(1)h_m). The finite faithful trace sums
the squared compression bounds with weights τ(e_j), total weight one, rather
than the number of arcs. Hence a=b. The infinite B(H) example in the source
explains why the finite-trace hypothesis at this intermediate step matters;
the final global argument does not apply this lemma directly to B(H).

For a separately normal cocycle f, the last-variable Cesàro average has a
pointwise ultraweak cluster point F. The countable averaging operator is
continuous on a common cochain norm ball by truncating its probability tail.
Akemann-type continuity follows here from the included gliding-hump proof:
spectral truncations have small trace supports, a subsequence admits mutually
orthogonal two-sided support compressions, and independent random signs
contradict boundedness of the normal map. The modulus survives all averages
and the ultraweak limit. The Liouville conclusion is F(a,x)=h(a)x.

Averaging the **original** cocycle equation at (a_1,…,a_k,v), then multiplying
by v*, gives dh=(-1)^k f. Thus g=(-1)^k h is an actual primitive with
||g||≤||f||. There is no unsupported assertion that averaging commutes with d
or that the cluster point remains separately normal.

For arbitrary trace-state II₁ algebras, each finite set E is placed inside
a countably generated N_E containing E, f(E^k), and unital matrix systems of
every finite size. These systems rule out every finite type-I summand, so
N_E is II₁ with separable predual. The trace-preserving expectation gives a
separately normal cocycle f_E and a uniformly bounded primitive g_E. Extend
by expectation on inputs. The coboundary equals f exactly at E^k, since all
adjacent products and output f(E^k) lie in N_E. A pointwise ultraweak subnet
then gives dg=f. The N_E need not form an increasing family.

For a general II₁ center, partition unity by supports of normal center
states; a maximal orthogonal family exhausts the center. Composing with the
center-valued trace gives trace-state pieces, possibly uncountably many.
Uniform bounds and the explicit central homotopy

    J_z psi(a_1,…,a_{n-1})
      = Σ_{i=1}^{n-1}(-1)^i
          psi(za_1,…,za_{i-1},q,qa_i,a_{i+1},…,a_{n-1})

give dJ+Jd=id-cut_z and norm≤n-1. Expansion by the first q-input proves
cancellation in every degree, including the degree-one endpoint. This
corrects mixed inputs before bounded central-product assembly. The one
non-II₁ piece has its own finite primitive bound by the classical theorem.
No uniform bound for all algebras is needed there. Finally the actual JKR
normal-reduction theorem gives f_original=f_normal+db for arbitrary bounded
cocycles. This establishes the exact ordinary actual-image H²/H³ import
needed downstream, subject to the attributed classical published theorems.

## 2. Fixed-source deformation and all-size geometric extension

For fixed A, actual H³=0 identifies C²/Z² with Z³ by a bounded bijection;
actual H²=0 makes d:C¹→Z² onto. The open mapping theorem gives finite K,L,
enlarged strictly above quotient inverse bounds for nonattained infima. No
bounded linear right inverse is required. Involutions
S_n f=(-1)^{(n-1)(n-2)/2} f(a_n*,…,a_1*)* commute with d: reversing an
internal merge and the outer actions gives s_{n+1}=(-1)^{n-1}s_n. Averaging
over this real involution preserves complex multilinearity and norm bounds.

Associativity of m+Delta implies dDelta=Delta(Delta(.,.),.)-
Delta(.,Delta(.,.)), of norm≤2 delta². Choose dh=z near Delta and put g=id+h.
For b=g^{-1}, direct expansion gives

    g mu(bx,by)-xy
       = [Delta-dh+hDelta-m(h.,h.)](bx,by).

Under delta≤1/(2K),1/(4L), ||h||≤2L delta and ||b||≤2. The residual is
therefore ≤(8K+8L+16L²)delta². The manuscript's stricter delta_A makes errors
halve; Σ||h_n||≤1/4. Ordered products converge in norm to an invertible
*-preserving complex-linear Phi, ||Phi-id||≤e^{1/4}-1<1/2. Onto multiplicative
conjugacy handles the unit. This is classical perturbation machinery, with
the required symmetry justified explicitly, not a new general mechanism.

Roydor's actual Corollary 2.4, Lemma 2.5, Proposition 2.13, Lemma 3.1 and
Theorem 3.2 were read with their complete proofs. Their hypotheses concern
ordinary norms and contain no separability assumption. Lemma 3.1 explicitly
normalizes the raw compression by sandwiching with T_tilde(p)^{-1/2}, so its
T_p^q **is unital**, resolving the provisional unit concern in my early notes.
Its inverse bound is 1+988 sqrt(t). Theorem 3.2 works whenever the source
unit halves, including all infinite type-I cardinals and II/III summands,
using a single 2×2 matrix system and finitely many norm estimates.

The central hom/anti-hom orientations form one product on the entire fixed
halving source V, with W's opposite product on its anti block. Its defect is
≤(1+988 sqrt(t))3147585 sqrt(t)→0. Correct it **once on V**, not separately
on comparison-dependent orientation corners. For M=A⊕P⊕O, the only sources
whose deformation constants are selected are the fixed P and E=eOe.

For full h and a rounded k, let w=c_D(k), z=theta^{-1}(w). Approximate order
under T^{-1} gives

    h-z ≤ [280(1+t)sqrt(t)+2(1+t)sqrt(2t+t²)]1.

The bracket tends to zero. Since z is central, h(1-z) is a projection;
the bound <1 forces it zero, and full carrier forces z=w=1. This works for
h and 1-h when both are full, without using Roydor's problematic Lemma 4.3.

For the fixed finite odd part O, e has rank n-1 in every degree-n component,
and its complement is abelian; both are full. The rounded q and 1-q remain
full. The complementary target corner is abelian by near-isometry of that
corner and Proposition 2.13, hence the target is type I. The corrected even
corner gives an exact Jordan map E→qDq. Full-corner center identification
induces beta:Z(O)→Z(D), preserving arbitrary joins by order isomorphism.
On w_n=beta(z_n), w_nq is a sum of n-1 equivalent abelian projections, each
with carrier w_n; w_n(1-q) is another abelian projection with that carrier.
Equal-carrier abelian projections are equivalent, so w_n is a sum of n such
projections and its algebra is homogeneous of degree n. Finite homogeneous
matrix classification plus beta recovers the full degree-n algebra. Their
bounded central product recovers O. The countable finite odd degree labels
do not impose any density bound on the centers. No infinite-cardinal
subtraction, measurable-field selection, or moving-corner threshold is used.

These full-corner/equivalence/classification interfaces were checked against
the actual primary-author Nelson notes, Lemmas 5.3.11–13, Proposition 5.3.15,
Theorem 5.3.17 with its finite-degree proof. The proof only needs the finite
case of that matrix theorem. All infinite type-I degrees stay inside P and
are treated by halving, without enumerating their cardinalities.

All remaining conditions are finitely many functions of the original excess
which tend to zero, plus at most two fixed positive deformation thresholds.
One sufficiently small positive epsilon_M therefore works for every N. This
is the required quantifier order, not a computed universal epsilon.

For the preduals, S*:N→M and (S^{-1})* have exactly the same two norms as S
and its inverse; hence d_BM(M,N)≤d_BM(M_*,N_*). Jordan maps and inverses are
positive order isomorphisms; they preserve bounded increasing nets, and are
normal isometries, giving isometric canonical preadjoints. Conversely a
predual isometry adjoints to an algebra isometry; Kadison's theorem allows
its unitary multiplier and gives Jordan structure. Zero algebras, zero
summands, strict inequalities and absence of infimum-attaining maps are
handled by the stated conventions.

## 3. Scope and diagnostic limits

The ordinary transpose is isometric yet can have cb norm n; the exact flip
partial-transpose witnesses in exact_controls.py rule out replacing an
ordinary near-isometry by a cb near-isometry. Its finite matrix calculations
check signs, the exact transported-product identity, and scalar sufficient
bounds. They do not prove any infinite-algebra theorem. The universal
arguments above and the actual primary theorem hypotheses do that work.

No universal numerical threshold, associative orientation recovery, cb
upgrade, arbitrary Banach comparison, real-linear variant, comparison at
equality, stability for other L^p, or formal/kernel certification follows.
The normal/cb/actual-image distinctions remain load bearing. No substantive
gap was found in the literal theorem or the checked import interfaces; this
is an internal scientific scope assessment, with root authority separate.
