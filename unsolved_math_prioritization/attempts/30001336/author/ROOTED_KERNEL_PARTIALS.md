# Proven rooted-kernel partials and a finite span experiment

All functions below use the exact source kernel a/(1−ax). The results concern that kernel, not an arbitrary decorated-tree expansion of a generic implicit equation.

## 1. Trees, endpoint bounds and existence

For an unordered rooted tree t with child trees t₁,…,t_k define

I_t(a)=K(∏ I_tj)(a),    Kf(a)=∫₀¹ a f(x)/(1−ax) dx.

The empty child product is 1. Forests mean products of these functions. Let |t| count vertices. For 0≤a<1 the integrals exist, are nonnegative and smooth, vanish at a=0, and satisfy

I_t(a)=O(a) near 0,
I_t(a)=O((1+|log(1−a)|)^|t|) near 1.

**Proof.** Induct on |t|. Products of children have at most logarithmic-power growth at 1 and are bounded near 0. For a in a compact subinterval of [0,1), dominated differentiation and expansion of the kernel apply. For a≥1/2 set δ=1−a and s=1−x. The kernel is bounded by 2/(δ+s). Splitting the integral at s=δ gives an O((1+|log δ|)^(m+1)) bound when the child product has log-power bound m. The integral on s<δ is bounded using ∫₀^δ(1+|log s|)^m ds=O(δ(1+|log δ|)^m). This proves the assertions.

## 2. Single-tree closure under the source divided difference

Define Df(a)=∫₀¹(f(x)−f(a))/(x−a)dx. If F is a forest, let t be its grafted tree and t⁺ the tree with the same child forest and one extra leaf attached at its root. Then

D I_t(a)=I_(t⁺)(a)+c_t,
c_t=∫₀¹ I_leaf(u) I_F(u)/u du.

**Proof.** The exact kernel identity is

[KF(x)−KF(a)]/(x−a)=∫₀¹ F(u)/[(1−xu)(1−au)]du.

For these nonnegative forests Tonelli applies; the resulting integrals are finite by the endpoint bounds. Integrating first in x gives I_leaf(u)/[u(1−au)]. Splitting this as I_leaf(u)/u+a I_leaf(u)/(1−au) yields the formula. The value at x=a follows by continuity. Near u=0 the numerator I_leaf(u) cancels u, and near 1 the remaining powers of logarithms are integrable. Thus no divergent counterterm was hidden in c_t.

For the star s_m with m leaf children, m≥0, this specializes at every m to

D I_(s_m)=I_(s_(m+1))+(m+1)! ζ(m+2).

Indeed c=∫₀¹[−log(1−u)]^(m+1)/u du. The substitution u=1−e^(−v) gives ∫₀^∞v^(m+1)/(e^v−1)dv. Expand the positive denominator geometrically, integrate termwise by Tonelli, and obtain (m+1)!Σ_(k≥1)k^(−m−2). This is an all-size kernel lemma, not an all-order theorem for G.

## 3. Every tree function is a harmonic polylogarithm with MZV coefficients

Use H_empty=1 and integration operators

H_(0w)(a)=∫₀^a H_w(s)/s ds,
H_(1w)(a)=∫₀^a H_w(s)/(1−s) ds.

Nonempty words used as functions end in 1, so they are regular at 0. Products are expressed by the shuffle rule, with multiplicities. For a nonempty word w ending in 1 (and also w empty in the second identity):

K H_(0w)=H_(0w)(1) H_1 − H_0(K H_w),
K H_(1w)=(H_0+H_1)(K H_w).

Also K1=H_1. Here H_0 and H_1 on a function denote the displayed integration operators, not multiplication.

**Proof of the first identity.** Integrate K H_(0w) by parts in x, using K's primitive −log(1−ax). Its derivative in a is H_(0w)(1)/(1−a)−(K H_w)(a)/a. The integration constant is zero at a=0. H_(0w)(1) converges and is a multiple-zeta value.

**Proof of the second identity.** At a cutoff R<1, integrate ∂_a K H_(1w) by parts. Use

x/[(1−x)(1−ax)]=(1/(1−a))[1/(1−x)−1/(1−ax)].

The apparently divergent boundary terms cancel. Their remaining factor is O((1−R) log^k(1−R)) for fixed a<1 and tends to zero. The derivative is (K H_w)(a)/[a(1−a)]. Integrate from 0 to a to obtain the identity.

Induction on word length proves K preserves the MZV-coefficient harmonic-polylogarithm algebra and raises functional word length by at most one. Induction on tree size, using shuffle products for each child forest, therefore proves the stated result. The c_t above is also an MZV combination: shuffle-expand I_leaf I_F and prefix 0 before evaluating at 1. All these evaluations converge.

This proves the direction **tree algebra ⊆ harmonic-polylogarithm algebra**. The reverse direction in all weights is not asserted. Even its proof would still not settle the restricted joint rational prefactors in G.

## 4. Leading-word finite experiment

Discard terms of lower functional word length. The preceding identities send a word w to σ(w)1, where σ is the letter substitution

σ(0)=−0,    σ(1)=0+1.

The leading expression of a forest is the shuffle product of its component expressions. The included verifier enumerates all unordered rooted forests and performs exact Gaussian elimination modulo the prime 1,000,003. Full rank modulo this prime proves full rank over Q for each finite integer matrix; it cannot prove an infinite sequence of rank statements.

For weights 1 through 9 the dimensions of all binary words ending in 1 are

1, 2, 4, 8, 16, 32, 64, 128, 256,

and the forest leading-word matrices attain those ranks. There are respectively

1, 2, 4, 9, 20, 48, 115, 286, 719

forests. Code independently checks these inventories and produces the exact pivot ranks. This is evidence for a possible all-weight spanning argument, not its replacement. It also does not test two-variable rational prefactors or arbitrary compositions of L, M and N.
