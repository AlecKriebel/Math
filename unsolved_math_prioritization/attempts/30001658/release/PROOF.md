# Functional inequality on the cube: scoped partial results

## 0. Status, source and conventions

**No resolution of the unrestricted inequality is claimed.** The target is the conjectured equation (12) in Alex Samorodnitsky's contribution, *Edge-isoperimetric inequalities in the discrete cube*, printed pp. 33–35 of *Combinatorics*, Oberwolfach Reports 01/2011, DOI [10.4171/OWR/2011/01](https://doi.org/10.4171/OWR/2011/01). The catalog identifier is 30001658 / OWR-4791-015. The current problem webpage could not be read (403), and the full catalog statement record was unavailable. Identification therefore rests on the surviving descriptor and the original report. This limitation is not a mathematical ambiguity in the displayed equation on printed p. 34, which was visually inspected.

Write Q_n={0,1}^n, N=2^n, and take a nonempty A⊆Q_n, m=|A|, a=m/N, k=log₂(N/m). All functions in the target are real-valued, with no support condition. The well-defined target is

(T)  E_c(f)+4 Σ_x f(x)^2 ≥ (2k/m)(Σ_{x∈A}|f(x)|)^2,

where

E_c(f)=Σ_{x∈Q_n} Σ_{i=1}^n (f(x)-f(x⊕e_i))^2.

Thus each undirected edge is counted twice. The report says “pairs” without explicitly saying ordered; its logarithmic-Sobolev normalization and its recovery of edge isoperimetry from equation (13) determine the double-counted convention. Samorodnitsky's later paper [arXiv:1207.1233v1](https://arxiv.org/abs/1207.1233v1), pp. 1–2, explicitly uses the uniform expectation of the sum over neighbors, agreeing with E_c/N. We do not manufacture a counterexample by halving this energy. The empty set makes the displayed quotient undefined; if its right side is conventionally set to zero, the case is immediate.

Let T_i flip coordinate i and L=Σ_i(I-T_i). Inner products without a subscript use counting measure. Then E_c(f)=2⟨f,Lf⟩. If ∂_if=(f-T_if)/2, then E_c(f)=4Σ_i||∂_if||_2^2. Uniform-measure energy is E_μ=E_c/N. For the random-walk generator L/n, the form is E_c=2n⟨f,(L/n)f⟩. No factor 1/n is silently inserted.

All logarithms marked ln are natural. The target uses base two. The coefficient 2 is dimension-independent. No nontrivial universal equality classification is claimed.

## 1. Common reduction: a positive resolvent

Set M=L+2I and b=1_A. Its quadratic form is positive definite since L is positive semidefinite. Replacing f by |f| does not increase E_c, preserves its squared norm, and preserves the right side of (T). It suffices to consider nonnegative f.

Put R=M^{-1}. Cauchy–Schwarz in the M-inner product gives

(bᵀf)^2 ≤ (fᵀMf)(bᵀRb).

Equality holds for f a scalar multiple of Rb. This is an admissible nonnegative function: if H is the cube adjacency matrix, M=(n+2)I-H and

R=(n+2)^{-1} Σ_{j≥0}(H/(n+2))^j.

The series converges because the spectral radius of H is n, and all its entries are nonnegative. Connectivity makes every entry of R strictly positive. Consequently, for any fixed nonempty proper A, (T) for every real f is **equivalent** to

(RC)  q(A):=(k/m)bᵀRb ≤ 1.

This equivalence does not assume f is supported on A. If q(A)>1, f=Rb is a certified positive counterexample. If q(A)<1, only f=0 can give equality. If q(A)=1, nonzero equality functions must be global constant-sign multiples of Rb: equality in |f|-contraction forces matching signs on every edge, since Rb is everywhere positive. For A=Q_n, k=0 and equality in (T) again forces f=0.

With the uniform inner product, H(A):=⟨b,Rb⟩_μ=(bᵀRb)/N and q(A)=kH(A)/a.

## 2. Approach 1: spectral relaxation and the dense regime

For S⊆[n], let χ_S(x)=(-1)^{Σ_{i∈S}x_i}. These form an orthonormal basis under μ; Lχ_S=2|S|χ_S. Therefore

(1)  H(A)=Σ_S \hat b(S)^2/[2(|S|+1)].

Here \hat b(∅)=a and Parseval gives Σ_S\hat b(S)^2=a. Since the denominator for S≠∅ is at least 4,

(2)  H(A) ≤ a^2/2+(a-a^2)/4 = a(1+a)/4.

It follows that (T) holds whenever k(1+a)≤4. In particular it holds for every n and every A of density at least 1/8. For a∈[1/8,1/4], k≤3 and (1+a)/4≤5/16, so q≤15/16. For a≥1/4, k≤2; alternatively Cauchy–Schwarz directly gives (Σ_A|f|)^2≤mΣf² and hence the right side of (T) is at most 4Σf². Thus all dimensions n≤3 are covered without enumeration. This proof also covers the zero function and the full set.

**Exact obstruction.** Mean and Parseval alone do not force (RC). The formal spectral assignment a=1/32, mass a² at degree zero and a-a² at degree one gives q=5(1+1/32)/4=165/128>1. These are relaxation data, not Fourier coefficients of an exhibited indicator, and not a counterexample. Additional restrictions arising from b²=b would have to rule them out. The spectral relaxation therefore does not resolve smaller densities in general.

## 3. Approach 2: all affine subspaces, with a sharp subcube computation

Let A=z+V be an affine subspace over F₂ of codimension k, where k is now an integer. Write W=V^⊥, so dim W=k and a=2^{-k}. Character orthogonality shows \hat b(S)=a(-1)^{S·z} for S∈W and zero otherwise. By (1),

(3)  H(A)/a = 2^{-k} Σ_{S∈W} 1/[2(|S|+1)].

Choose k pivot coordinates for W: restriction to these coordinates is an isomorphism W→F₂^k. For the word corresponding to u∈F₂^k, its full Hamming weight is at least |u|. Since t↦1/[2(t+1)] is decreasing,

H(A)/a ≤ 2^{-k}Σ_{j=0}^k C(k,j)/[2(j+1)]
         = (1-2^{-k-1})/(k+1).

For the last identity integrate (1+t)^k on [0,1], or use C(k,j)/(j+1)=C(k+1,j+1)/(k+1). Thus, for k≥1,

(4)  q(A) ≤ [k/(k+1)](1-2^{-k-1}) <1.

This proves (T) for **every affine subspace in every dimension and every real function on the whole cube**. No support restriction is imposed. For coordinate subcubes the bound on H(A) is exact. Equality in the bound on H(A) occurs only for coordinate subcubes: if equality holds, every word of W has no nonzero coordinate outside the chosen pivots, so W is the full coordinate subspace on them. Conversely such W gives equality termwise. This statement concerns the auxiliary resolvent bound, not equality in (T), which is strict for every nonzero f in these cases.

For a coordinate subcube the exact largest coefficient C in

E_c(f)+4Σf² ≥ (Ck/m)(Σ_A|f|)^2

is C=2(k+1)/[k(1-2^{-k-1})], by the extremizer f=Rb. This exceeds 2 for every finite k and tends to 2. More simply, A={0}, f=1_A gives E_c=2n, Σf²=1, and k=n, so a coefficient valid for all dimensions must satisfy C≤2+4/n for every n. Hence any universal coefficient is at most 2. This is a necessary upper bound, not a proof that 2 is achievable for arbitrary sets.

**Exact obstruction.** Formula (3) uses flat Fourier magnitude on a linear annihilator. General indicators have neither that support nor flat magnitudes. The pivot argument has no demonstrated replacement for arbitrary A. Affine-set verification cannot be promoted to a universal result.

## 4. Approach 3: entropy tensorization and the constant loss

We give a self-contained classical logarithmic-Sobolev route, rather than treat a named inequality as an unexamined proof of the target. For nonnegative h on a finite probability space let Ent(h)=E(h ln h)-(Eh)ln(Eh), with 0 ln 0=0.

### 4.1 Two-point inequality

For real u,v, replacing them by absolute values decreases (u-v)^2, so assume u,v≥0. By homogeneity, normalize (u²+v²)/2=1 unless both vanish. After swapping, put u²=1+s, v²=1-s, 0≤s≤1. The entropy of these two squared values is

F(s)=[(1+s)ln(1+s)+(1-s)ln(1-s)]/2.

We claim F(s)≤1-√(1-s²). Both sides vanish at s=0. Their derivatives are atanh(s) and s/√(1-s²). The latter dominates because these functions vanish at zero and their derivatives satisfy

1/(1-s²) ≤ 1/(1-s²)^{3/2}.

Integrate, and use continuity at s=1. Since (u-v)^2/2=1-√(1-s²), this proves 2Ent_i(f²)≤(u-v)^2.

### 4.2 Tensorization, with its justification

Entropy is convex as a functional of h. For strictly positive h, its second variation in direction r is

E(r²/h) - (Er)²/Eh ≥0

by Cauchy–Schwarz. Zero values follow by adding a positive constant and taking a limit. For independent finite X,Y the entropy chain rule is

Ent_{X,Y}(h)=E_Y Ent_X(h)+Ent_Y(E_Xh).

Convexity bounds the second term by E_X Ent_Y(h). Induction yields Ent_μ(h)≤Σ_i E_{other coordinates}Ent_i(h). Combining with the two-point inequality gives

(5)  E_μ(f) ≥ 2Ent_μ(f²).

### 4.3 Binary coarse-graining

Assume V=E_μf²>0 and set h=f²/V, so Eh=1. Write q=E_μ(1_Ah). For 0<a<1, Jensen on A and its complement gives

Ent(h)≥q ln(q/a)+(1-q)ln((1-q)/(1-a)).

The right side is at least q ln(1/a)-ln2: discard the nonnegative term -(1-q)ln(1-a), and use q ln q+(1-q)ln(1-q)≥-ln2. If s=E_μ(1_A|f|), Cauchy–Schwarz on A gives q≥s²/(aV). Therefore

(6)  E_μ(f)+2ln2·V ≥ [2ln(1/a)/a]s².

Multiplying by N and using 4>2ln2 proves the weaker, all-dimension inequality

E_c(f)+4Σf² ≥ [2ln2·k/m](Σ_A|f|)^2.

Cases V=0 and a=1 are immediate. This reproduces the classical coefficient loss discussed in the original report; it is not an improvement to coefficient 2.

**Exact obstruction.** The desired logarithm is k, while (6) has k ln2. A fixed additive reserve times V does not bridge a deficit 2(1-ln2)k s²/a uniformly as k grows. At the level of the inequalities used, formal parameters q=1, a=2^{-k}, Ent(h)=k ln2 and E_μ(f)=2k ln2 are admissible, but for k>2/(1-ln2) they violate the desired energy-plus-four bound. These formal parameters are not an actual indicator counterexample: the source geometry supplies extra energy for indicators. They demonstrate the missing information in this relaxation. A sharper argument must use geometry beyond the entropy lower bound and (5).

## 5. Approach 4: supported functions and the Schur-complement gap

Samorodnitsky's published support-restricted theorem, represented in [arXiv:1207.1233v1](https://arxiv.org/abs/1207.1233v1), Theorem 1.1, establishes E_c(g)≥(2k/m)(Σ_A|g|)^2 when g vanishes outside A. This is equation (13), not the unrestricted equation (12), of the report. Its long proof remains credited published work; we do not claim to have independently audited that whole proof. It is not needed by the self-contained results in Sections 1–4 and 6.

Here is the precise obstruction to extending this theorem simply by minimizing outside A. Partition the full M matrix into A and C=Q_n\A:

M = [[L_A+2I, -B], [-Bᵀ, L_C+2I]],

where L_A and L_C are principal submatrices of the full cube Laplacian (diagonal n), and B is the cross-edge incidence matrix. The lower-right block D=L_C+2I is positive definite. Completing the square in the C variables shows that, for prescribed u=f|_A,

min_{f|_A=u} fᵀMf = uᵀS u,
S=L_A+2I-BD^{-1}Bᵀ,

with minimizing exterior values D^{-1}Bᵀu. Thus R_{AA}=S^{-1}. The correction BD^{-1}Bᵀ is positive semidefinite, so

R_{AA} ≽ (L_A+2I)^{-1}.

The direction is opposite to the upper bound one would need to discard the exterior. Already for n=1 and A={0},

L_A+2I=[3], D=[3], B=[1], S=[8/3],
R_{AA}=[3/8] > [1/3]=(L_A+2I)^{-1}.

Nor can the additive 2I always absorb the correction in matrix order. Let A be even parity in Q_4 and C odd parity. Then L_A=L_C=4I and every row/column of B has sum four. Hence on the constant vector,

BD^{-1}Bᵀ1=(16/6)1=(8/3)1 >2·1.

So the sufficient bridge S≽L_A is false. This is an explicit obstruction to that proof strategy, not a counterexample to (T); the parity set lies in the dense regime already proved.

**Remaining requirement.** One would need an upper bound on bᵀS^{-1}b retaining both the support geometry and the positive exterior correction. The supported inverse inequality alone bounds a different matrix. We obtain no such universal bound here.

## 6. Approach 5: distance kernel, compression, and finite certificates

### 6.1 Exact kernel

For 0≤ρ≤1 define T_ρχ_S=ρ^{|S|}χ_S. The one-coordinate transition matrix has diagonal (1+ρ)/2 and off-diagonal (1-ρ)/2; independence therefore gives

T_ρ(x,y)=2^{-n}(1+ρ)^{n-d}(1-ρ)^d,  d=|x⊕y|.

Integrating eigenvalues yields R=(1/2)∫_0^1T_ρ dρ. Thus R(x,y)=K_n(d), where

(7)  K_n(d)=2^{-n-1}∫_0^1(1+ρ)^{n-d}(1-ρ)^d dρ
           = [Σ_{j=d+1}^{n+1} C(n+1,j)]/[(n+1)C(n,d)2^{n+1}].

For the second identity substitute t=(1-ρ)/2, obtaining ∫_0^{1/2}t^d(1-t)^{n-d}dt. The derivative of Σ_{j=d+1}^{n+1}C(n+1,j)t^j(1-t)^{n+1-j} telescopes to (n+1)C(n,d)t^d(1-t)^{n-d}; evaluate at 0 and 1/2. In particular all kernel values are positive rationals, strictly decreasing with d: the integrand for d+1 is that for d times (1-ρ)/(1+ρ), which is strictly less on 0<ρ<1.

The criterion becomes

(8)  [log₂(N/m)/m] Σ_{x,y∈A}K_n(|x⊕y|) ≤1.

Both orders of every pair are included, and the diagonal is included.

### 6.2 Coordinate compression

Compress A in coordinate i by moving the occupied point of every singleton i-fiber to its endpoint with i=0, leaving empty and double fibers unchanged. Cardinality is preserved. Consider two distinct fibers at distance d in the other coordinates. If both are singleton and they originally have opposite i-values, their two ordered cross contributions rise from 2K_n(d+1) to 2K_n(d). If the singleton values agree, nothing changes. If at least one fiber is empty or double, its summed cross contributions are unchanged. Contributions within a fiber are unchanged. Therefore compression cannot decrease the double sum in (8).

Each nontrivial compression strictly reduces Σ_{x∈A}|x|, a nonnegative integer. Repeatedly compress any available coordinate until none changes. The terminal set is a downset (if x is present and x_i=1, its i-deletion is present), has the same size, and has no smaller kernel sum. Consequently the full conjecture reduces to (8) for arbitrary downsets. This is an exact all-dimension reduction, not an assertion that a downset must be a subcube.

### 6.3 Exhaustive finite check with rational logarithm enclosures

A downset in Q_n has restrictions D_0,D_1 in Q_{n-1} with D_1⊆D_0; conversely every such ordered pair yields one downset. Starting from the two subsets of Q_0, this is a complete, duplicate-free recursion. It gives 7,581 downsets in Q_5, including the empty one. The retained checker examines all 65,808 nonempty sets across n=1,2,3,4, and every nonempty downset in n=5. It also verifies coordinate compression on every subset through n=4.

No floating-point logarithm decides an inequality. To bound log₂(N/m), set j=⌊log₂m⌋, r=m/2^j∈[1,2), z=(r-1)/(r+1). The positive series

ln r=2Σ_{l≥0} z^{2l+1}/(2l+1)

has, after t terms, remainder at most 2z^{2t+1}/[(2t+1)(1-z²)]. Thus exact rational lower and upper bounds for ln r and ln2 give the upper bound

log₂(N/m) ≤ n-j-(ln r)_lower/(ln2)_upper.

The checker uses t=24 and exact rational comparisons with (7). For powers of two it uses the exact integer logarithm. All comparisons pass. Together with the proved compression lemma, this is a reproducible finite certificate covering n≤5; it is not a proof for unbounded dimension, a formal proof-assistant verification, or independent peer review.

**Exact obstruction.** Compression leaves all downsets, whose number grows rapidly; the recursion imposes D_1⊆D_0 but does not by itself prove the target bound on their cross-kernel interaction. Enumerating dimensions up through five supplies no induction step. The radial exploratory calculations were merely a search and are not used as a theorem or part of this certificate.

## 7. Final scope

The unresolved statement is precisely (RC) for all dimensions and all nonempty proper sets, equivalently for all downsets by Section 6. Coefficient 2 has the necessary universal upper bound, but its universal validity and general nonzero equality possibilities remain unproved in this work. No counterexample under the source-consistent convention was found. The support-restricted 2017 theorem does not close the gap. Bounded literature non-discovery is not a claim that no prior solution exists.

The five routes retain different information: spectral first moments, linear-code structure, entropy tensorization, exterior minimization, and combinatorial compression. Each leaves an explicit obstruction. The authored statements and proofs are AI-assisted research notes, with no historical-novelty claim and no human refereeing claim.
