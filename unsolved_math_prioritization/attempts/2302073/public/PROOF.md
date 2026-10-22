# Rubel's two-parameter normal-family problem: verification of a known affirmative answer

Problem 2302073 / AMR-022-2073, Hayman–Lingham Problem 2.73.

## Status and attribution

The answer to the existence question is **yes**. Yixin He, Quanyu Tang and Teng Zhang give this affirmative resolution in *A Solution to a Problem of Rubel on Two-Parameter Normal Families of Entire Functions*, [arXiv:2603.20883v1](https://arxiv.org/abs/2603.20883v1), submitted 21 March 2026, Theorem 1.2. Their construction and its essential choice of coefficient domain are credited throughout this note. This is a verification of that prior result, not a new solution or a priority claim. A journal publication or human peer-review status is not asserted.

We give all the needed arguments, including a quantitative specialization of the classical attracting-basin argument. The latter follows the normalized-iterate mechanism of Rosay and Rudin, *Holomorphic maps from C^n to C^n*, Transactions AMS 310 (1988), 47–86, [DOI](https://doi.org/10.1090/S0002-9947-1988-0929658-4), Theorem 9.1, pp. 73–74. Thus the existence of the required parametrization is not left as an unverified black box. No novelty is claimed for the explicit normalization of its Jacobian below.

## 1. The precise question and convention

We seek a jointly entire function F on C_z × C_a × C_b such that:

1. The family of functions z ↦ F(z,a,b), with (a,b) ranging over **all** C², is normal on **all** C.
2. There do not exist entire functions G:C²→C and H:C²→C with F(z,a,b)=G(z,H(a,b)) for every (z,a,b).

Normality here uses the usual spherical convention: every sequence has a subsequence converging locally uniformly to an entire function or to the constant infinity. Allowing infinity matters. The elementary normal family z+c in the source's discussion would not be normal under a convention that demands only finite holomorphic limits. No restriction to bounded parameter sets is being made.

We construct F affine in z, but genuinely two-dimensional in (a,b). In the normalization used here it satisfies

    F_b F_{a,z} − F_a F_{b,z} = 1/625

at every point of C³.

## 2. A polynomial automorphism and its basin

Use the same polynomial dynamics as He–Tang–Zhang:

    f(x,y) = (y, (y²−x)/2),
    g(x,y) = (x²−2y, x).

Direct substitution gives f∘g=g∘f=id. In particular, these are mutually inverse automorphisms of C². Write

    M(x,y) = (y, −x/2),    R(x,y) = (0,y²/2),

so that f=M+R and M²=−I/2. Both det Df and det M equal 1/2. Define

    ‖(x,y)‖_* = max{3|x|/4, |y|},
    B = {p: ‖p‖_*<1/6},
    D = {p: f^n(p)→0 as n→∞}.

For r=‖p‖_*<1/6,

    ‖f(p)‖_* ≤ max{3r/4, r²/2+2r/3} ≤ 3r/4.

The last bound follows because 3r/4−(r²/2+2r/3)=r(1−6r)/12≥0. Consequently f(B)⊂B, every point of B tends to 0, and

    D = ⋃_{n≥0} g^n(B).

Indeed, convergence to 0 implies eventual membership in B, and eventual membership implies convergence by the contraction estimate. The sets in this union are open and connected, and they increase because B⊂g(B). Thus D is a domain, with f(D)=D=g(D).

## 3. Complete construction of the basin parametrization

This section supplies the specialized classical basin theorem used by the prior construction. We will construct a biholomorphism h:D→C² normalized by Dh(0)=I and det Dh=1.

The weighted operator norm of M is at most 3/4. Its inverse is

    M⁻¹(x,y) = (−2y,x),

whose weighted operator norm is at most 3/2: its two weighted coordinates are bounded by 3r/2 and 4r/3. Also ‖R(p)‖_*≤‖p‖_*²/2.

For n≥0 put h_n=M^(−n)∘f^n. These maps are entire automorphisms. If p∈B and r=‖p‖_*, then

    h_{n+1}(p)−h_n(p) = M^(−n−1) R(f^n(p)),

and therefore

    ‖h_{n+1}(p)−h_n(p)‖_*
      ≤ (1/2)(3/2)^(n+1)(3/4)^(2n) r²
      = (3/4)(27/32)^n r².

Since 27/32<1, the series of differences converges uniformly on B, hence locally uniformly there. It defines a holomorphic map h₀:B→C² and the explicit tail bound

    ‖h₀(p)−h_N(p)‖_* ≤ (24/5)(27/32)^N ‖p‖_*².

Every h_n fixes 0 and has derivative I there, so h₀(0)=0 and Dh₀(0)=I. Derivatives converge locally uniformly, by the Cauchy integral formula on polydiscs. Since

    det Dh_n = (det M)^(−n) (det Df)^n = 1,

we also obtain det Dh₀=1 throughout B. Taking limits in h_n∘f=M∘h_{n+1} gives

    h₀(f(p)) = M h₀(p),    p∈B.

For p∈D choose n with f^n(p)∈B and set

    h(p) = M^(−n) h₀(f^n(p)).

The displayed functional identity and forward invariance of B show that this value is independent of n once the iterate lies in B. These formulas agree on the increasing open sets g^n(B), so define a holomorphic map on D. They also give h∘f=M∘h and det Dh=1 everywhere.

For completeness, we verify global bijectivity rather than infer it merely from convergence. The holomorphic inverse function theorem gives a neighborhood of 0 on which h₀ is injective. Choose a weighted ball W about 0 contained in that neighborhood and in B. The contraction estimate makes W forward invariant.

If h(p)=h(q), take n large enough that f^n(p), f^n(q) lie in W. Then

    h₀(f^n(p)) = M^n h(p) = M^n h(q) = h₀(f^n(q)).

Injectivity on W gives f^n(p)=f^n(q), and injectivity of f^n gives p=q.

For surjectivity, let w∈C². Since ‖M‖_*≤3/4, M^n w→0. The set h₀(W) contains a neighborhood of 0. Choose n so that M^n w∈h₀(W), let p=(h₀|_W)⁻¹(M^n w), and put q=g^n(p). Then q∈D and h(q)=w. Hence h is bijective. Since det Dh=1, its local holomorphic inverses agree globally, and h is biholomorphic.

Write Ψ=h⁻¹:C²→D. Then Ψ is entire, injective, onto D, and det DΨ=1. Only elementary uniform-convergence and inverse-function facts were used after the explicit polynomial construction.

## 4. Geometric containment of the basin

We now verify the trapping estimates in He–Tang–Zhang's construction. Put

    E₁ = {(x,y): |x|<25 and |y|<5},
    E₂ = {(x,y): |x|≥10+|y|}.

We claim g(E₁)⊂E₁∪E₂ and g(E₂)⊂E₂.

First take (x,y)∈E₁ and put (X,Y)=g(x,y). If |x|<5, then |Y|<5. Either |X|<25, giving membership in E₁, or |X|≥25>10+|Y|, giving membership in E₂. If instead 5≤|x|<25, let t=|x|. The triangle inequality gives

    |X| > t²−10,
    (t²−10)−(10+t) = (t−5)(t+4) ≥ 0.

Thus |X|>10+|Y| and g(x,y)∈E₂. These estimates include the threshold t=5 because |y|<5 supplies the strict inequality.

Next take (x,y)∈E₂. Then t=|x|≥10 and |y|≤t−10, so

    |X|−|Y| ≥ t²−2|y|−t
              ≥ t²−3t+20
              = 90+(t−10)(t+7) ≥ 90 >10.

Hence g(E₂)⊂E₂. Since B⊂E₁, induction gives g^n(B)⊂E₁∪E₂ for every n, and therefore D⊂E₁∪E₂. In particular D≠C², as (0,10) belongs to neither E₁ nor E₂.

Apply the automorphisms

    L(x,y) = (y/25,x/25) = (s,t),
    A(s,t) = (s+t²,t) = (u,v).

For (x,y)∈E₁, |s|<1/5<1+|t|. For (x,y)∈E₂,

    |s| ≤ (|x|−10)/25 = |t|−2/5 <1+|t|.

It follows that Ω=A(L(D)) is biholomorphic to C² and is contained in

    S = {(u,v)∈C²: |u−v²|<1+|v|}.

Define Φ=A∘L∘Ψ=(U,V):C²→Ω. This is a biholomorphism. Since det DA=1, det DL=−1/625 and det DΨ=1,

    det DΦ = −1/625.

## 5. Normality on the entire z-plane

We verify directly that the family {u+vz:(u,v)∈S} is normal. Take any sequence (u_n,v_n)∈S. If (v_n) has a bounded subsequence, then u_n=v_n²+δ_n with |δ_n|<1+|v_n| shows that the corresponding (u_n) is bounded too. A further subsequence converges in C², say to (u,v), and u_n+v_n z→u+vz locally uniformly.

If no bounded subsequence is selected, an unbounded sequence (v_n) has a subsequence with |v_n|→∞. For every R≥0 and |z|≤R,

    |u_n+v_n z|
      ≥ |v_n|²−(R+1)|v_n|−1 →∞.

This convergence is uniform on the disk |z|≤R and hence is local uniform spherical convergence to infinity. Either alternative provides the subsequence required for normality, on all C at once.

This is not normality of all affine functions: the restriction to S prevents zeros from remaining in a fixed compact set when the slopes become unbounded.

## 6. The entire family and the obstruction to factorization

Set

    F(z,a,b) = U(a,b)+zV(a,b).

Because U and V are entire on all C², F is jointly entire on all C³. Its slices belong to the normal family just proved, so the required parameter family is normal.

Differentiation yields

    F_b F_{a,z}−F_a F_{b,z}
      = (U_b+zV_b)V_a−(U_a+zV_a)V_b
      = U_b V_a−U_a V_b
      = −det DΦ
      = 1/625.

If F=G(z,H(a,b)) for entire G and H, the chain rule instead gives

    F_a=G_w H_a,       F_b=G_w H_b,
    F_{a,z}=G_{zw} H_a, F_{b,z}=G_{zw} H_b,

with G evaluated at (z,H(a,b)). The same differential expression would vanish identically, a contradiction. No converse factorization theorem is needed. This settles both conditions of the original existence question.

## 7. Scope of the certificate

The argument is a complete, attributed reconstruction of a known affirmative answer. The basin map Ψ is rigorously defined by the inverse of the normalized-iterate limit and its global continuation. It is not asserted to be a polynomial or an elementary closed-form formula. Numerical orbit calculations are unnecessary.

The companion verifier checks exact algebraic identities and the rational contraction/trapping constants. Those finite checks supplement the analytic proof. They do not constitute a formal proof-assistant verification of holomorphic convergence, inverse-function theory, normality or the global quantifiers. This note is AI-assisted and unrefereed; OpenAI tools were used extensively for research, derivation, drafting and checking.
