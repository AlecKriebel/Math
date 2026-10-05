# Independent analytic checks for the quasi-conical construction

Problem 30005613 / OWR-14297736-021. Checked 5 October 2026.

These arguments independently expand the analytic steps in the frozen
PROOF.md. They are authored mathematical verification, not quotations from
a source and not a claim of formal verification. No change to the theorem or
to the frozen proof is required.

## 1. The shrinking window in every dimension at least two

Fix a finite stage, its previously opened windows, and the next cube. Write
D0 for their disconnected union before the last window is opened, Dδ for
the union after opening it, and p for the new interface center. The explicit
cube geometry gives

    D0 ⊂ Dδ,
    Dδ \ D0 ⊂ {x1=p1, |xj|<δ for 2≤j≤d}.

In particular, all Dδ have the same L² space, and their difference from D0
is contained in a ball of radius √d δ centered at p. This does not make the
Dirichlet form domains equal: a positive window in a screen cannot simply
be discarded because its d-dimensional Lebesgue measure is zero.

Choose a fixed bounded box B containing the closures of these finite-stage
domains. All H₀¹ spaces below are identified with their zero extensions in
H₀¹(B). We prove the relevant Mosco convergence directly.

The recovery condition is immediate: V0=H₀¹(D0) is contained in every
Vδ=H₀¹(Dδ), so a fixed element of V0 is its own recovery sequence.

For the weak-limit condition, let δm→0 and um∈Vδm converge weakly in H¹(B)
to u. If η is a bounded Lipschitz cutoff vanishing on a neighborhood of p,
then ηum∈V0 for all sufficiently large m. To see this, approximate um by
smooth functions with compact support in Dδm, multiply by η, and observe
that the resulting supports avoid the only part of Dδm outside D0. A
Lipschitz product can then be smoothed inside D0. The closed subspace V0
is weakly closed. Therefore ηu∈V0.

It remains to remove the puncture at p. For d≥3, choose ηr=0 on Br(p),
ηr=1 outside B2r(p), 0≤ηr≤1, and |∇ηr|≤C/r. Then

    ||1-ηr||²_L²(B) ≤ C r^d,
    ||∇ηr||²_L²(B) ≤ C r^(d-2) → 0.

For d=2 one must instead use the logarithmic cutoff, for 0<r<1:

    ηr(x)=0                         if |x-p|≤r²,
    ηr(x)=log(|x-p|/r²)/log(1/r)    if r²<|x-p|<r,
    ηr(x)=1                         if |x-p|≥r.

Polar integration gives

    ||∇ηr||²_L²(R²) = 2π/log(1/r) → 0,
    ||1-ηr||²_L²(B) ≤ πr² → 0.

For bounded v∈H¹(B), dominated convergence applied to
(1-ηr)v and (1-ηr)∇v, together with
||v∇ηr||₂≤||v||∞ ||∇ηr||₂, gives ηr v→v in H¹(B).

Apply this to bounded Sobolev truncations v of the real and imaginary
parts of u. Such v retains the preceding local membership property: for
a cutoff η avoiding p, take a second cutoff θ equal to 1 on supp η and
vanishing closer to p. Since θu∈V0, the Sobolev truncation theorem and
multiplication by η show that ηv∈V0. Hence the cutoff limit puts v in
V0. Truncations converge to u in H¹(B), so u∈V0. This proves the weak-limit
condition, including the critical dimension two. Only the new window is
shrunk; the old windows never change.

The cutoffs can be Lipschitz rather than smooth because each fixed cutoff
is an H¹ multiplier and can be approximated on its transition annulus.
The estimates concern their explicit Sobolev representatives. In dimension
one the cutoff energy does not vanish, and adding the interface point
joins two intervals. This gives a useful check on the dimension restriction.

## 2. From this convergence to operator norm convergence

The following proof also checks that boundedness is used only at one fixed
finite stage. Put Rδ=(A_Dδ+1)^(-1) and R0=(A_D0+1)^(-1), canonically on
H=L²(D0). Equivalently extend all of them by zero to L²(B). Their
variational equations use

    b(v,w)=∫_B (∇v·conj(∇w)+v conj(w)).

For ||fm||₂≤1 and δm→0, the solutions um=Rδm fm are bounded in H₀¹(B)
by their energy identities. If norm convergence failed, one could choose
such fm with ||(Rδm-R0)fm||₂ bounded below by a positive constant.
Pass to a subsequence with fm weakly converging to f in L²(B), um weakly
converging in H₀¹(B), and um strongly converging in L²(B), by Rellich
compactness. Section 1 puts the limit u in V0. For every v∈V0⊂Vδm,

    b(um,v)=<fm,v> → <f,v>.

Thus u=R0 f. The operator R0 is compact, by the same bounded-box embedding,
so R0 fm→R0 f strongly. This contradicts the lower bound and proves

    ||Rδ-R0|| → 0.

No regularity of the slit boundary is used. The proof permits arbitrary
fixed earlier apertures and treats all δ→0, not just a specially chosen
subsequence. It establishes precisely the fact imported in PROOF.md §2
from Krejcirik--Lotoreichik, arXiv:2205.08172v2, Propositions 2.2–2.3 and
Section 3: https://arxiv.org/abs/2205.08172v2 .

## 3. Protected full spectral subspaces

Let S be the finite protected set of distinct eigenvalues of the old
bounded-stage operator. For a∈(b,c), a cube resonance with λ∈S forces

    Σ mi² = 4a²λ/π² < 4c² max(S)/π².

This bounds all positive integers mi independently of a. There are only
finitely many multi-indices, and each pair (λ,(mi)) excludes at most one
positive a. The nonempty interval is therefore not exhausted. This is an
existence argument over real widths; it does not pretend to compute old
domain eigenvalues or a certified numerical spectral gap.

After a nonresonant cube is fixed, every λ∈S is an isolated eigenvalue of
A_D0 with exactly its old multiplicity. Under t↦(1+t)^(-1), these become
isolated nonzero eigenvalues of the bounded compact resolvent R0. Choose
disjoint contours, each separated from the rest of its spectrum and from
zero. For small δ the resolvent identity and a Neumann-series inverse
give uniform convergence of (z-Rδ)^(-1) on every contour. Integration
therefore gives operator norm convergence of the full cluster projections.

A repeated eigenvalue can split into many eigenvalues inside its contour.
The cluster projection still converges to the whole old eigenspace. It is
incorrect in general to insist on convergence to any preselected basis
inside that eigenspace. For example, the matrix [[1,t],[t,1]] has fixed
diagonal/antidiagonal eigendirections for every t>0, even as t→0.

Every protected projection is a sum of the full clusters. Since their
number is finite, one positive δ satisfies all its required smallness
bounds. Subsets of the same disjoint family remain nested and are full
spectral projections at the new finite stage. The new largest cutoff
can contain them all and approximate the finite test set simultaneously.
There is no requirement to control infinitely many clusters in a single
inductive step and no uniform lower bound on successive spectral gaps.

For orthogonal projections P,Q with ||P-Q||<1, the restriction of Q to
ran P has trivial kernel: Qv=0 and Pv=v would imply
||v||≤||P-Q|| ||v||. Interchanging P and Q proves equal finite ranks.
This supplies the exact rank-stability fact used at each stage and limit.

## 4. The growing domain and the correct limiting resolvent

The final Hilbert space H is the orthogonal direct sum of all cube L²
spaces. It is fixed only after the induction. Every earlier estimate
continues to hold on H because extension by zero preserves operator norm
and rank. The null interface faces do not add another L² summand.

Write V=H₀¹(O), Vn=H₀¹(On), all by zero extension. These are increasing
closed subspaces of V under b. Their union is dense: every compact support
inside O is contained in one member of the increasing open exhaustion,
and C_c^∞(O) is dense in V by definition. For f∈H, the solution Rn f is
the b-orthogonal projection of Rf onto Vn. Consequently Rn→R strongly,
where R=(A_O+1)^(-1), and ||Rn||≤1.

The zero-extended Rn have a kernel on the unbuilt cubes. They are not
being incorrectly treated as resolvents of densely defined self-adjoint
operators on all of H. Only their boundedness, self-adjointness, and the
explicit variational convergence are used. Nor is norm convergence of
Rn to R asserted; the large untouched future cubes would obstruct that.

## 5. Fixed rank means the limit cannot lose its eigenvectors

Fix the birth index k. The summable transport bounds give a norm limit Pk
and, for n≥k,

    ||Pk-Pn^k|| ≤ Σ(j≥n) 2^(-j-2) = 2^(-n-1).

Norm continuity preserves self-adjointness and idempotence. Rank stability
then gives rank Pk=rank Pk^k<∞. Taking the two adjacent birth indices
separately preserves nesting: Pk P(k+1)=Pk.

For any f∈H,

    ||Rn Pn^k f-R Pk f||
      ≤ ||Pn^k-Pk|| ||f|| + ||(Rn-R)Pk f|| → 0,

and

    ||Pn^k Rn f-Pk R f||
      ≤ ||Pn^k-Pk|| ||Rn f|| + ||Pk(Rn-R)f|| → 0.

Since Rn Pn^k=Pn^k Rn, the limit commutes with R. This is a vectorwise
strong-limit argument for bounded operators. It uses no norm-convergent
full-rank resolvent sequence and no unbounded-operator commutator limit.

The actual resolvent R is positive and injective. Its restriction to the
finite-dimensional reducing space ran Pk is a positive definite matrix,
so it has an orthonormal eigenbasis with eigenvalues μ>0. If Rv=μv,
then v=μ^(-1)Rv belongs to dom A, and Av=(μ^(-1)-1)v. Thus every vector
of ran Pk lies in the pure point subspace of A. A uniform positive lower
bound on μ across all k is neither available nor needed.

The distinction between norm and strong projection convergence matters.
On ℓ², the rank-one projections onto e_n converge strongly to zero while
their pairwise operator distances are 1. Rank would be lost under that
weaker hypothesis. The proof has norm convergence at each fixed k.

## 6. Completeness really removes the residual continuous subspace

Let f=f_(j,l) be a normalized sine-basis vector in cube j. For every
n≥max(j,l), the birth cutoff Pn^n approximates it with error <2^(-n).
The estimate in Section 5 applies also when k=n, since it is the tail
bound for the entire future trajectory starting at that birth. Hence

    ||(I-Pn)f|| < 2^(-n)+2^(-n-1) = 3·2^(-n-1) → 0.

Every Pn f belongs to the closed span of genuine eigenvectors of A.
The cube bases form an orthonormal basis of H, so the closed span is H.
This excludes absolutely continuous and singular continuous spectral
subspaces simultaneously. Nesting additionally permits an explicit
orthogonal eigenbasis by diagonalizing R on ran P1 and on the finite
orthogonal differences ran(P(k+1)-Pk).

This proves substantially more than existence of a dense set of
eigenvalues. The latter alone would allow a nonzero continuous spectral
summand. For instance, a diagonal operator on ℓ² with a dense set of
positive eigenvalues can be direct-summed with multiplication by x on
L²(0,∞); the sum still has dense point spectrum and a nonzero absolutely
continuous part. The birth-test estimate rules out exactly this gap.

## 7. Spectral support and the zero endpoint

The cube widths grow by more than 1 at each step, and their centers and
left faces escape to infinity. Each cube contains a ball of radius an.
For a unit L² cutoff χ∈C_c^∞(B1), a plane wave e^(iξ·x), |ξ|²=λ≥0,
and rn=an/2, scaling gives a unit test un supported in cube n and

    ||(A-λ)un||₂ ≤ rn^(-2)||Δχ||₂
                      +2|ξ|rn^(-1)||∇χ||₂ → 0.

These test functions lie in dom A: for any compactly supported smooth
function in an open set, integration by parts identifies its Dirichlet
operator action with -Δ, with no boundary regularity requirement.
Their supports are disjoint, so they are orthonormal and weakly zero.
Weyl's criterion gives [0,∞)⊂σess(A); nonnegativity gives equality with
σ(A). A complete eigenbasis then implies closure σp(A)=[0,∞).

If Au=0, the form identity makes its weak gradient zero. Connectedness
makes u constant, and the infinite volume excludes a nonzero L² constant.
Thus 0 is not an eigenvalue. Pure point spectral type is fully consistent
with an interval as the spectral set and with all eigenvalues embedded.
