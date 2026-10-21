# An explicit fixed-modular-alphabet theorem for the higher parameter coefficients

## Scope and status

Target: queue row 1874, ID 30006595 / OWR-14299909-010. This note concerns only the coefficients of

\[
H(t,z(\tau))={}_3F_2(\tfrac12+t,\tfrac12-t,\tfrac12;1,1;z(\tau)),\qquad
z(\tau)=64\frac{\eta(\tau)^{24}\eta(4\tau)^{24}}{\eta(2\tau)^{48}}.
\]

It establishes an all-orders, convergent representation in a fixed alphabet of explicit holomorphic modular forms. It does not establish that the individual coefficients are scalar modular forms, nor that they reduce to a finite algebra of ordinary single modular antiderivatives. Consequently it is a precise positive answer in an iterated-integral sense, and a partial result under the more conservative source-status gate. It does not settle the full R(k,1) generator or any higher-depth R(k,ell) program. No publication or queue changes accompany this note.

The source question is on printed p. 469 of Wadim Zudilin's contribution, joint work with Masato Wakayama, in *Multiple Zeta Values and Modular Forms*, Oberwolfach Reports 23 (2026), https://doi.org/10.4171/OWR/2026/7 . The separate source/status gate records the bounded literature check and formulation correction. We make no novelty claim.

## Theorem

Put q=exp(2πiτ), δ=q d/dq, and

\[
A(\tau)=\theta_3(2\tau)^4,\qquad
f(\tau)=\theta_2(2\tau)^4\theta_4(2\tau)^4
=16\frac{\eta(\tau)^8\eta(4\tau)^8}{\eta(2\tau)^8}.
\]

Here theta constants use their usual lattice argument: θ3(2τ)=Σ(n∈Z)q^(n²). A is a holomorphic modular form of weight 2, and f a holomorphic modular form of weight 4, both on Γ0(4) with trivial character. In particular f is NOT a cusp form: its orders at the cusps ∞, 0, 1/2 are respectively 1, 1, 0. It has expansion

\[
f=16q-128q^2+448q^3-1024q^4+2016q^5-3584q^6+\cdots.
\]

For a holomorphic q-series g with g(0)=0 define

\[
I g(q)=\int_0^q g(s)\frac{ds}{s}=\sum_{m\ge1}\frac{g_m}{m}q^m.
\]

Define B0=1 and Bn=I²(f B(n−1)) for n≥1. These are convergent, fully normalized integrals, with Bn(0)=δBn(0)=0. Then

\[
[t^{2n}]H(t,z(\tau))=(-1)^n A(\tau)\sum_{j=0}^n B_j(\tau)B_{n-j}(\tau),\qquad
[t^{2n+1}]H=0. \tag{1}
\]

Equivalently, if

\[
J(a_1,\ldots,a_r;q)=\int_0^q a_1(s)J(a_2,\ldots,a_r;s)\frac{ds}{s},\quad J(\varnothing)=1,
\]

then Bn=J((1,f)^n). The alphabet {1,f} consists of two specified holomorphic modular forms of weights 0 and 4 on the specified group. Every word used ends with f, so convergence requires no tangential-basepoint regularization. The products in (1) may also be replaced by finite sums using the shuffle identity. This is a fixed alphabet and explicit word formula, not an unspecified closure under arbitrary antiderivatives.

## Proof by hypergeometric transformation and modular gauge

Let x=λ(2τ)=θ2(2τ)^4/θ3(2τ)^4. Classical theta/eta identities give

\[
z=4x(1-x),\qquad \delta x=x(1-x)\theta_3(2\tau)^4.
\]

For example, θ2(2τ)=2η(4τ)^2/η(2τ), θ4(2τ)=η(τ)^2/η(2τ), and θ3(2τ)=η(2τ)^5/[η(τ)^2η(4τ)^2]; these directly verify the required eta quotient for z.

Clausen's identity and the quadratic transformation give, near x=0,

\[
H(t,4x(1-x))=G(t,x)^2,\qquad
G(t,x)={}_2F_1(\tfrac12+t,\tfrac12-t;1;x).
\]

Indeed first use a=1/4+t/2, b=1/4−t/2 in Clausen, then the quadratic identity F(a,b;a+b+1/2;4x(1−x))=F(2a,2b;a+b+1/2;x). See DLMF §16.12 (Clausen) and §15.8 (quadratic transformations): https://dlmf.nist.gov/16.12 and https://dlmf.nist.gov/15.8 . The hypergeometric identities are first germ identities at the cusp; all global statements refer to their analytic continuation on the modular upper half-plane, not pointwise reassignment of principal branches.

The Gauss equation is

\[
pG''+p'G'-(\tfrac14-t^2)G=0,\qquad p=x(1-x),
\]

where primes here mean x derivatives. Let G0=G(0,x)=θ3(2τ)^2 and U=G/G0. Cancellation using the t=0 equation yields

\[
(pG_0^2 U')'=-t^2G_0^2U.
\]

Since δx=pG0², multiplication by δx gives the particularly simple, exact equation

\[
\boxed{\delta^2U=-t^2 f U},\qquad
f=pG_0^4=\theta_2(2\tau)^4\theta_4(2\tau)^4. \tag{2}
\]

The cusp data are U(0)=1 and δU(0)=0. Expanding U=Σ(n≥0)(−1)^n t^(2n)Bn and solving (2) with these cusp data gives precisely Bn=I²(f B(n−1)). Squaring G=G0 U proves (1), including all integration constants.

For completeness the eta-quotient modularity criterion applies to the exponents (r1,r2,r4)=(8,−8,8): the weight is 4, the two congruence sums are 24, and the character factor 1^8 2^(−8)4^8=256 is a square. The cusp-order formula gives (1,1,0), proving holomorphy. The analogous standard theta-series transformation gives A∈M2(Γ0(4)).

## Analytic, not merely formal

On any closed disk |q|≤r<1, put Mr=max|f(q)/q|. Successive radial integrations give

\[
|B_n(q)|\le \frac{(M_r|q|)^n}{(n!)^2}.
\]

Inductively, multiplication by f adds one power of |q|, and each of the two integrations divides its exponent n by n. Thus Σ(−1)^n t^(2n)Bn converges locally uniformly for every t, so (2) and (1) hold analytically. All functions are holomorphic on |q|<1; the cusp-normalized continuation is unambiguous. This proof is independent of finite coefficient checks.

## Explicit Eisenstein identification and low orders

The same kernel is the explicit Eisenstein combination

\[
f=\frac{E_4(\tau)-17E_4(2\tau)+16E_4(4\tau)}{15}. \tag{3}
\]

Both sides are holomorphic weight-4 forms on Γ0(4). Its index is 6 and the weight-4 Sturm bound is 2. Equality of their q^0, q^1, q^2 coefficients (0,16,−128) therefore proves (3). Although f vanishes at ∞, its individual Eisenstein summands do not. Expanding each letter in a convergent word into individual unregularized E4 integrals would introduce divergent pieces; retain f as the letter, or separately define tangential regularization. No such expansion is needed here.

Writing B=I²f and C=I²(fB), the first coefficients are

\[
h_0=A,\quad h_2=-2AB,\quad h_4=A(B^2+2C),
\]

and h6=−2A[I²(f C)+B C]. In particular

\[
h_2=-32q-192q^2-\frac{3200}{9}q^3-\frac{1408}{9}q^4+O(q^5),
\]

\[
h_4=384q^2+\frac{13312}{9}q^3+\frac{1792}{3}q^4+O(q^5).
\]

For all n the leading term is

\[
h_{2n}=(-1)^n16^n\frac{\binom{2n}{n}}{(n!)^2}q^n+O(q^{n+1}).
\]

## Five substantive approaches and what each establishes

1. **Original third-order differential equation.** With θ=z d/dz, L0=θ³−z(θ+1/2)³, the defining series gives L0 h(2n)=−z(θ+1/2)h(2n−2). This proves an exact inhomogeneous hierarchy, but by itself identifies no modular alphabet and is not a solution to the modularity question.
2. **Clausen/quadratic reduction.** The exact square reduction above exposes a second-order Gauss equation rather than tackling the third-order hierarchy blindly. It preserves the original parameter, including its signs and factors of two. This step is essential to the theorem.
3. **Modular uniformization/gauge.** The λ(2τ) substitution and division by G0 remove the first derivative exactly, producing a single explicit level-4 weight-4 modular kernel. The eta-quotient cusp audit and Eisenstein identification determine the actual group, character, weight and cusp behavior.
4. **Convergent iterated-integral construction.** Formula (1), the fixed word (1,f)^n, the cusp normalization and the majorant prove an analytic all-orders modular-iterated-integral representation. This is stronger than an arbitrary-antiderivative recurrence or finite fit, while still not a theorem of scalar modularity.
5. **Monodromy/automorphy boundary check.** The Gauss local exponents at x=∞ are 1/2±t, hence parameter-dependent local monodromy prevents one from transferring the t=0 scalar automorphy to the family without proof. Equivalently, setting V=δU/t gives δ(U,V)^T=t[[0,1],[−f,0]](U,V)^T, with cusp value (1,0). Its path-ordered series is precisely the fixed-word construction. This clarifies why iterated integrals are natural; it does NOT prove that a smaller ordinary-primitive class is impossible. No monodromy-based nonmembership claim is made.

## Independent checks and acceptance boundary

An independent adversarial review rederived the gauge equation, checked the modular character and all three cusp orders, and supplied the analytic majorant. A separately constructed exact-rational script compares the original 3F2 after substitution by its eta quotient against (1), through q^13 and t^12. The script also checks (3) to that order. Its passing output is `exact_checks.json`; the runnable test is `check_fixed_alphabet.py`. These checks support normalization and implementation, but the symbolic proof above, not the finite test, establishes the all-orders theorem.

Acceptance: retain a partial/scoped result unless the intended problem is explicitly accepted in the fixed modular-iterated-integral sense. Do not claim classification as scalar modular forms, reduction to ordinary single antiderivatives, a full R(k,1) solution, higher-depth resolution, or literature novelty. All sources and coefficients discussed here concern the public mathematical object; no copied primary text or private coordination materials are included.

## Further definition and modularity references

- L. Adams and S. Weinzierl, *Feynman integrals and iterated integrals of modular forms*, arXiv:1704.08895, especially the definition on pp. 2–3, explicitly allows the constant modular form 1 of weight 0 among the letters: https://arxiv.org/pdf/1704.08895 . This supports the terminology used here; our integral identity and convergence are proved independently above.
- D. Savitt, *An elementary proof of Newman's eta-quotient theorem*, Theorem 1.1 and Remark 1.2, for eta-quotient modularity, character, and cusp holomorphy: https://math.jhu.edu/~savitt/papers/pdfs/newman.pdf .
- The exact quadratic transformation used above is DLMF 15.8.18: https://dlmf.nist.gov/15.8.E18 . Its principal-branch region is not claimed globally; the theorem uses continuation from the q=0 germ.
