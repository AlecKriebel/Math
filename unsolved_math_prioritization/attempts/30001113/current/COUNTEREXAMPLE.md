# A characteristic-two obstruction to the proposed fibre-product factorization

## Status and scope

Complete candidate proof for independent review, 9 October 2026. This addresses the unrestricted questions in Byszewski's OWR 54/2008 contribution (p.3039) and arXiv:1112.0352v1, Question 4.4. Neither question assumes that D_N or D_{G/N} is prorepresentable. In the 2011 paper, the immediately following Remark 4.5 adds these assumptions conditionally for a ring formula, and Theorem 4.9 later states them explicitly for its obstruction-space result. The OWR report likewise states them in Theorem 3, after posing its question. This proof does not address a modified question that additionally assumes D_N and D_{G/N} prorepresentable. No novelty claim is made.

We prove a stronger negative statement: for the explicit local action below, there is no prorepresentable functor F at all for which the indicated restriction–induction morphism to D_N^{G/N}×_F D_{G/N} is formally smooth. Thus prescribing the proposed tangent space of F cannot repair this example.

## 1. The action and quotient

Let k=F_4=F_2[u]/(u²+u+1), G=(F_4,+), and N=(F_2,+)⊂G. Define

rho(a)(t)=t/(1+at),  a∈F_4.

These substitutions are continuous k-algebra automorphisms of k[[t]], rho(a)rho(b)=rho(a+b), and rho is injective. Hence this is a faithful action of the Klein four-group. The subgroup N is normal. All nonidentity elements have conductor one.

Write Q=G/N and take u+N as its generator. A parameter on the N-quotient is

y=t rho(1)(t)=t²/(1+t).

Indeed k[[t]]^N=k[[y]]. One direct verification is that y is invariant and t satisfies t²+yt+y=0; this gives a separable degree-two extension k((t))/k((y)), with nontrivial automorphism rho(1), and intersecting the fixed field with k[[t]] gives k[[y]].

The induced action of the generator of Q is

rho(u)(y)= t²/((1+ut)(1+(u+1)t))
         = t²/(1+t+t²)
         = y/(1+y),

since u(u+1)=1. Therefore D_Q is exactly the deformation functor of the weakly ramified involution

sigma(y)=y/(1+y).

All functors below are on the original category C of local Artinian W(k)-algebras with residue k, and all equivalences are conjugations reducing to the identity. Characteristic-two Artinian k-algebras are objects of C through W(k)→k.

## 2. A tangent direction invisible to every prorepresentable recipient

Put B=k[e]/(e³), A=k[e]/(e²), and let j:B→B send e to e+e². This is a W(k)-algebra automorphism. Over B define an involution

sigma_e(y)=(y+e)/(1+y).

It is an automorphism because its constant term is nilpotent and its linear coefficient is a unit. Its representing matrix M_e=[[1,e],[1,1]] satisfies M_e²=(1+e)I, so it defines an action of Q. Let x∈D_Q(B) be its equivalence class, and v its image in D_Q(A).

The class x is fixed by j. Explicitly, let C=[[1+e,e],[0,1]], corresponding to the coordinate change chi(y)=(1+e)y+e. This reduces to the identity. In B,

M_(e+e²) C = (1+e) C M_e.

Scalar matrices do not change the associated fractional-linear substitution, so sigma_e and sigma_(e+e²) are equivalent. In ordinary composition of fractional-linear functions, chi is the conjugator; in the source's ring-automorphism composition convention the equality is sigma_(e+e²)=chi^(-1) sigma_e chi. Thus j_*x=x. This conjugacy is also the explicit calculation in Byszewski–Cornelissen, Proposition 4.1, p.896; the displayed matrix identity verifies it directly here.

Let F=h_R be any prorepresentable functor on C, and eta:D_Q→F any natural transformation. Write psi:R→B for eta_B(x). Naturality and j_*x=x imply

j∘psi=psi.

Every element of B has a unique expression c_0+c_1 e+c_2 e² with c_i∈k, and j fixes it exactly when c_1=0. Consequently the composite R→B→A has image in the constant subfield k⊂A. Because it is a local W(k)-algebra map inducing the prescribed residue map, this composite is the basepoint R→k→A. Hence

eta_A(v)=0∈T F.

The direction v is nevertheless nonzero in T D_Q. If sigma_e over A were conjugate to sigma by an identity-reducing coordinate change chi(y)=y+e f(y), then, to first order, its perturbation from sigma would be

f(sigma(y))−sigma'(y)f(y).

Its constant coefficient is f(0)−f(0)=0, because sigma(0)=0 and sigma'(0)=1. But sigma_e−sigma=e/(1+y) has perturbation with constant coefficient 1. This is impossible. Thus v≠0.

In summary: the same nonzero tangent element v∈T D_Q is sent to zero by every natural map from D_Q to every prorepresentable F. This conclusion used actual deformation classes and naturality over B and A, not a replacement of D_Q by a hull.

## 3. Injectivity of the restriction tangent map

Let Theta=Der_k k[[t]]. We show

res:H¹(G,Theta)→H¹(N,Theta)

is injective. The standard inflation–restriction exact sequence identifies its kernel with H¹(Q,Theta^N). We compute this last group directly.

### 3.1 Identifying the invariant derivations

Restriction embeds Theta^N in Der_k k[[y]]. A derivation b(y)∂/∂y has a unique extension to the separable field k((t)), and its coefficient in the t-coordinate is

a(t)=b(y)/(dy/dt)=b(y)(1+t)²/t²,

since dy/dt=t²/(1+t)². This extension is N-invariant by uniqueness. It preserves k[[t]] if and only if

2 ord_y(b)−2≥0,

or equivalently b(y)∈y k[[y]]. Conversely every N-invariant integral derivation is obtained this way. Thus, as a Q-module under the quotient coordinate action,

Theta^N ≅ M:=y k[[y]]∂/∂y.

### 3.2 Vanishing of H¹(Q,M)

The generator of Q acts on coefficient functions of vector fields by

T(f)(y)=(1+y)² f(y/(1+y)).

Here T²=1. Set z=y²/(1+y), so k((y))^Q=k((z)), by the same degree-two calculation as above. For f∈y k[[y]], the condition Tf=f is equivalent to f/y² being Q-invariant. Since ord_y(f/y²)≥−1 and valuations of nonzero elements of k((z)) are even in the y-coordinate, it follows that f/y²∈k[[z]]. Therefore

M^Q=y² k[[z]]∂/∂y.

For every h(z)∈k[[z]], invariance of h(z) gives

(T−1)(y h(z))= y² h(z),

because (1+y)²·y/(1+y)−y=y² in characteristic two. Hence (T−1)M=M^Q. For a cyclic group of order two,

H¹(Q,M)=ker(1+T)/im(T−1).

In characteristic two, ker(1+T)=M^Q, so H¹(Q,M)=0. This proves the asserted injectivity of restriction.

For completeness, the tangent identifications T D_H=H¹(H,Theta) and the identification of the tangent map of restriction with cohomological restriction are the usual first-order cocycle calculation: a lift has the form (id+e d_g)rho(g), the group relation is the 1-cocycle equation, and an identity-reducing coordinate conjugation changes it by a 1-coboundary. The argument above therefore applies to the actual unframed set-valued functors. The fixed subfunctor D_N^Q injects into D_N at every ring, so restriction into T D_N^Q has zero kernel as well.

### 3.3 The prescribed obstruction tangent space in this example

The quotient Theta-sharp/Theta^N is (k[[y]]/y k[[y]])∂/∂y≅k, with trivial Q-action because T preserves the constant coefficient. Hence the proposed tangent space H¹(Q,Theta-sharp/Theta^N) is k. The contradiction below is stronger: it excludes any prorepresentable F, including one with this one-dimensional tangent space.

## 4. Contradiction to formal smoothness

Suppose there are a prorepresentable F and natural maps

f:D_N^Q→F,  g:D_Q→F,

such that (res,ind) factors through E=D_N^Q×_F D_Q and D_G→E is formally smooth.

Let 0 denote the basepoint tangent class obtained by base change of the residual action from k to A=k[e]/e². Naturality gives f_A(0)=0. Section 2, applied to g, gives g_A(v)=0, with v≠0. Therefore

(0,v)∈E(A).

Its reduction to E(k) is the unique residual point. Smoothness for the surjection A→k would provide a class w∈D_G(A) satisfying

res(w)=0,  ind(w)=v.

Section 3 forces w=0 because the restriction tangent map is injective. Naturality of induction gives ind(0)=0, contradicting v≠0.

This contradiction proves that no such F exists. It already occurs on a first-order lifting problem; the third-order ring B is used only to constrain which first-order data can be detected by any prorepresentable recipient.

## 5. Relation to the original hypotheses and prior results

- k=F_4 is perfect of characteristic two, the action is faithful, N is normal, and all test rings and maps lie in the specified Artinian W(k)-category.
- No map out of D_N^Q is replaced by a map out of D_N. Only the map out of D_Q is forced to kill v. The invariant functor contributes its genuine basepoint, which always belongs to it.
- The argument does not assume that the requested maps have the cohomological gamma and sigma as their tangent maps. It rules out every choice of natural maps with a prorepresentable recipient, regardless of its tangent dimension.
- The example lies in the exceptional nonprorepresentable-involution case. It does not contradict Byszewski's Theorem 4.9, which separately assumes D_N and D_Q prorepresentable. That theorem gives an obstruction vector space, not the unrestricted desired factorization.
- The proof does not require the universality or versality of a weakly ramified Klein-four deformation ring. It directly computes the restriction kernel and the unavoidable tangent collapse.
- The unrefined introductory question and the refined tangent-space question receive the same negative instance and must not be counted as separate discoveries.

## References

1. Jakub Byszewski, “Dévissage for local deformation functors,” Oberwolfach Reports 54/2008, pp.3038–3040, especially p.3039. https://ems.press/content/serial-article-files/46200
2. Jakub Byszewski, “Deformation functors of local actions,” arXiv:1112.0352v1 (2011), Definitions 1.1–1.2, Proposition 2.4 and Question 4.4. https://arxiv.org/abs/1112.0352v1
3. Jakub Byszewski and Gunther Cornelissen, “Which weakly ramified group actions admit a universal formal deformation?”, Annales de l'Institut Fourier 59 (2009), 877–902, Proposition 4.1, pp.895–896. https://doi.org/10.5802/aif.2450
