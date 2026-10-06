# Uniform height counts for projective-space embeddings: verified partial results

Problem 30002439 / OWR-12725-016. Research date: 2026-10-06.

## Status and exact scope

This is an authored mathematical audit and a collection of deductions from established theorems. It does **not** prove or disprove the general conjecture and claims no novelty or best-known status for its partial bounds. A bounded literature search cannot certify that no further result exists.

The source is Per Salberger's Problem 11 in the problem session of *Analytic Number Theory*, Oberwolfach Reports 10 (2013), pp. 3031–3032, DOI [10.4171/OWR/2013/51](https://doi.org/10.4171/OWR/2013/51). The source distinguishes a bound with a map-dependent constant from the requested uniform bound and already records the cases d=1 and n=1. The workshop was held in 2013; the catalog's 2014 citation must not change the problem's date.

We interpret the problem over Q. Let n>=1, d>=1, and let homogeneous forms F_0,...,F_m in Q[x_0,...,x_n] of common degree d have no common geometric projective zero. They define a Q-morphism f:P^n -> P^m. Assume f is a closed immersion. For a rational projective point represented by a primitive integral vector y, set H([y])=max_i |y_i|. For every real B>=1, set n_f(B)=#{x in P^n(Q):H(f(x))<=B}. The question asks for every epsilon>0 a constant depending only on d,n,epsilon bounding n_f(B)/B^((n+1)/d+epsilon), uniformly in f, its coefficients, and m. This is multiplicative height, not logarithmic height. Here d is the degree of the coordinate forms, **not** the degree of the image. The latter is d^n.

## 1. A height-nonincreasing reduction of the target dimension

Put r=dim_Q span(F_0,...,F_m), so r<=binomial(n+d,d). Choose a basis consisting of some of the original forms, indexed by I. Define g:P^n -> P^(r-1) using precisely those coordinates. The chosen forms have no common zero: a common zero would annihilate every linear combination and hence every F_i. Expressing all the F_i in this basis gives an injective linear map Q^r -> Q^(m+1) whose I rows are the identity. Its projectivization i is a closed linear embedding and f=i composed with g. The inverse of i on its image identifies g with f; in particular g remains a closed immersion. Also g^*O(1)=O(d).

If y is a primitive integral representative of f(x), its subvector y_I is nonzero. Dividing y_I by the gcd of its coordinates gives a primitive representative of g(x). Consequently H(g(x))<=max_{j in I}|y_j|<=H(f(x)). Thus

    n_f(B) <= n_g(B),       r-1 <= binomial(n+d,d)-1.                 (1)

This reduction introduces no coefficient-dependent height factor. Taking a maximum over the finitely many possible r makes any bound uniform in m. Replacing the forms by arbitrary linear combinations without controlling height would not justify (1); the basis must be selected from the existing coordinates.

## 2. Exact elementary cases and a sharp benchmark

### Linear embeddings

When d=1, basepoint-freeness forces r=n+1, and the reduced map g is a projective automorphism. Therefore (1) bounds n_f(B) by the number of rational points of P^n of height at most B. A primitive nonzero integer vector and its negative represent one point, giving

    n_f(B) <= ((2 floor(B)+1)^(n+1)-1)/2 <= (3^(n+1)/2) B^(n+1).

This proves the requested bound with no epsilon when d=1, with no dependence on f or m.

### Standard Veronese and arbitrary source automorphisms

Let nu_d be the map with every monomial x^alpha of total degree d as a coordinate. For a primitive integer vector x, the monomial vector is primitive: any prime dividing all coordinates would divide every pure power x_i^d, hence every x_i. Its maximum absolute coordinate is H(x)^d, because the pure powers occur and all other monomials are no larger. Hence

    H(nu_d(x)) = H(x)^d,
    n_nu_d(B) = #P^n(Q) of height <= B^(1/d).                       (2)

This count has order B^((n+1)/d), with positive upper and lower constants depending on n,d only. For a self-contained lower estimate put T=floor(B^(1/d)). Among ordered pairs 1<=a,b<=T, the number with a common divisor is at most

    sum_(k=2)^T floor(T/k)^2 <= T^2 sum_(k=2)^infinity k^(-2)
                              <= (3/4) T^2.

The last inequality follows from 1/4+integral_2^infinity t^(-2)dt=3/4. Each remaining coprime pair, followed by arbitrary n-1 coordinates in {0,...,T}, gives a distinct primitive projective point. There are at least T^(n+1)/4 such points. Since floor(t)>=t/2 for t>=1, this is the stated lower order. Thus an exponent below (n+1)/d cannot hold in general, even for one standard embedding.

For any A in PGL_(n+1)(Q), the map x->A(x) permutes P^n(Q). Therefore n_(nu_d composed with A)(B)=n_nu_d(B). This entire family satisfies the exponent without epsilon.

## 3. Why uniform pointwise height comparison cannot solve the problem

Fix n>=1 and d>=1. For an integer T>=1 take

    A_T([x_0:x_1:x_2:...])=[x_0-T x_1:x_1:x_2:...],
    f_T=nu_d composed with A_T,
    x_T=[T:1:0:...].

Every f_T is a degree-d closed immersion. But H(x_T)=T whereas H(f_T(x_T))=1. Thus no positive c(d,n) can satisfy H(f(x))>=c(d,n)H(x)^d for all such f and all x. The same family satisfies the desired count by (2). It refutes only the proposed pointwise intermediate assertion, **not** the conjecture. The usual height-machine estimate with a constant depending on f is compatible with this example and does not remove that dependence.

## 4. Curve case from an exact literature theorem

Miguel N. Walsh, *Bounded rational points on curves*, Theorem 1.1 ([arXiv:1308.0574v2](https://arxiv.org/abs/1308.0574v2); IMRN 2015, pp. 5644–5658), gives N(C;B)<=C_(delta,N) B^(2/delta) for any irreducible degree-delta projective curve C in P^N over Q, uniformly in C. This is a cited theorem, not reproved here.

For n=1, reduce the target by (1). The image C=g(P^1) is isomorphic over Q to P^1, has degree d, and lives in dimension at most d. Closed immersion gives a bijection on Q-points. Walsh's theorem therefore yields n_f(B)=O_d(B^(2/d)), uniformly also in m. This is a pre-existing solved subcase, explicitly distinguished from the unresolved general question.

## 5. Uniform surface bounds with an explicit remaining gap

Write X=g(P^2) and N=r-1 after (1). Then N<=binomial(d+2,2)-1 and deg X=D=d^2. If C is any geometric integral curve on X, its inverse image in P^2 has some positive plane degree e. Restricting g^*O(1)=O(d) to that curve gives

    deg C = d e >= d.                                             (3)

In particular X has no lines if d>=2. The following inputs are established results of Per Salberger, *Counting rational points on projective varieties*, PLMS 126 (2023), 1092–1133, [DOI 10.1112/plms.12508](https://doi.org/10.1112/plms.12508):

- Theorem 0.9(b), p. 1095: degree-D geometrically integral surfaces admit O_(D,N)(B^(3/(2 sqrt(D))) log B+1) bounded-degree geometric curves covering all but O_(D,N,eta)(B^(3/sqrt(D)+eta)) points.
- Theorem 0.8, same page: a degree-four surface carrying a two-dimensional conic family has, off its lines, O_(N,eta)(B^(43/28+eta)) points.

We now deduce a bound for every degree-d closed immersion of P^2, d>=2. The first input supplies O_d(B^(3/(2d)) log B+1) curves of degrees <=K(d). A curve defined over Q contributes O_d(B^(2/d)) by (3) and Walsh. If a covering curve is not defined over Q, choose a distinct Galois conjugate. All its rational points lie in their intersection. Pull back to P^2 and apply plane Bezout; the contribution is at most e^2<=K(d)^2. This also satisfies O_d(B^(2/d)). Thus, for B>=2,

    n_f(B) <= C_(d,eta) [B^(3/d+eta)
                         +(B^(3/(2d)) log B+1) B^(2/d)].

Take eta=epsilon/2 and absorb log B into B^(epsilon/2). Since 3/(2d)+2/d=7/(2d)>3/d, this proves

    n_f(B) = O_(d,epsilon)(B^(7/(2d)+epsilon)).                     (4)

The case 1<=B<2 follows by monotonicity from B=2, after enlarging the same uniform constant. This is a deduction of known theorems; no claim of originality or optimality is made.

For d=2, images of the lines of P^2 form a two-dimensional family of conics on X: distinct lines give distinct curves under the isomorphism. Also D=4 and X has no lines. The second input therefore improves (4) to

    n_f(B) = O_epsilon(B^(43/28+epsilon))       (n=2,d=2).           (5)

The missing exponent is 1/(2d) in (4), and 1/28 in (5), compared with the proposed 3/d. These positive gaps cannot be renamed epsilon: the conjecture requires the bound for **every** epsilon>0.

## 6. General dimension growth is insufficient

Salberger's 2023 Theorem 0.3 gives O_(D,N,epsilon)(B^(dim X+epsilon)) when D>=4. For n>=2,d>=2, the image has D=d^n>=4. Together with (1) this gives O_(d,n,epsilon)(B^(n+epsilon)). But

    n - (n+1)/d > 0  for n>=2,d>=2.

Thus this theorem does not yield the proposed exponent. Recent improvements to dimension growth do not change this elementary comparison. In particular the precise hypersurface statement in Cluckers–Debes–Hendel–Nguyen–Vermeulen, *Improvements on dimension growth results and effective Hilbert's irreducibility theorem*, Theorem 4.21, is not a theorem asserting the present exponent for embeddings of P^n. Liu's 2026 preprint arXiv:2601.10895 concerns conics on cubic surfaces in P^3; those hypotheses do not describe the degree-four images in (5). These are scope checks, not claims that these papers exhaust the literature.

## 7. Stopping condition and validation limits

Four mathematical approaches were assessed: (i) pointwise height comparison and automorphism tests; (ii) coordinate-subset reduction and exact special cases; (iii) general dimension growth; (iv) the surface covering method. The target remained out of reach after the last approach. No fifth approach, general proof, or general counterexample is claimed.

The checker tests finite integer instances of coordinate height monotonicity, the Veronese identity and count, the shear example, and exact rational exponent gaps. Such tests corroborate arithmetic details; the universal arguments above and the cited theorems carry the mathematical proofs. They cannot certify an open conjecture, the absence of literature, or novelty. A fresh independent audit is required before any publication of this packet.
