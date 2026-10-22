# Four shared values with constant Mues function: a bounded partial investigation

**Target:** UnsolvedMath 30000706 / OWR-1460-013, queue rank 606.
**Disposition:** `unsolved`, five substantive approach families used, 5/5. No complete classification and no novelty claim. Prepared 2026-10-04. AI-generated, unrefereed research documentation; independent audit pending at freeze.

## 1. Exact target and source boundaries

Let distinct nonconstant functions f and g be meromorphic on the entire complex plane. Let a1, a2, a3 be distinct finite complex numbers, put B={a1,a2,a3,infinity}, and require f^{-1}(a)=g^{-1}(a) as sets for every a in B. Multiplicities need not agree. Write

P(w)=(w-a1)(w-a2)(w-a3),
psi=f'g'(f-g)^2/[P(f)P(g)],
U=f'(f-g)/P(f), V=g'(f-g)/P(g).

The task is to determine **all** (a1,a2,a3,f,g) for which psi is identically 1, with removable singularities interpreted meromorphically. The plane domain and four distinct values are essential. Constant functions, coincident functions, and repeated a_i are not part of this problem.

The exact source is Norbert Steinmetz's problem-session contribution, printed pp. 540-542 in *Normal Families and Complex Dynamics*, Oberwolfach Reports 4 (2007), 487-548, DOI [10.4171/OWR/2007/09](https://doi.org/10.4171/OWR/2007/09). Problem 1 is on printed p. 541 (PDF page 55). Its request is a classification, and the subsequent remark proposes that the examples already cited might exhaust it. This is not a theorem of exhaustiveness.

The catalogue URL returned HTTP 403. Its complete pinned record was read instead and compared with the primary PDF, including a rendered inspection of p. 541. The catalogue's label describing DOI [10.1016/S0252-9602(17)30234-5](https://doi.org/10.1016/S0252-9602(17)30234-5) as later work is chronologically misleading: Huang and Du's paper is from **2004**, before this problem. The digits “17” in its DOI are not its publication year.

Relevant later sources were checked with their exact hypotheses:

- Steinmetz, [arXiv:1102.3383v1](https://arxiv.org/abs/1102.3383v1), 2011, especially §§2, 6, 7; published as *Southeast Asian Bulletin of Mathematics* 36 (2012), 399-417. It discusses established examples and reductions, not a full solution of the present classification.
- Steinmetz, [*Algebraic curves and meromorphic functions sharing pairs of values*](https://doi.org/10.54330/afm.157535), Annales Fennici Mathematici 50 (2025), 79-95; also [arXiv:2410.01624v1](https://arxiv.org/abs/2410.01624v1). Its main hypothesis contains **four finite pairs plus a fifth pair at infinity shared CM**. Those five pairs are not supplied by this problem's four shared values. Its genus-zero conclusion cannot be imported here.
- Li, Zhai, Yi, [arXiv:2402.03248v8](https://arxiv.org/abs/2402.03248v8), revised 2026-01-06, Theorem 7 on printed p. 4, claims the finite-order 3IM+1CM theorem. Its hypothesis requires at least one CM value, which this target does not require. Its 39-page proof has **not** been independently audited here, and none of our proved partials depends on it. The downloaded v8 PDF, rather than the partially stale abstract-page wording, fixes the claim inspected.

No full classification was located in this bounded search. This is a search outcome, not proof that none exists. The adjacent catalogue problem 30000707 concerns prescribed U,V exponential systems and remains a separate target; neither its result nor its turn count is asserted here.

## 2. Approach 1: local divisors and exact leading coefficients

**Mechanism:** use psi=1 at every shared point rather than ignore exceptional divisors. This gives unconditional necessary conditions, but not a global classification.

### Proposition 1 (finite shared points)

Fix a in {a1,a2,a3}, set D=P'(a)≠0, and let t=z-z0. Suppose

f-a=A t^p+O(t^{p+1}), g-a=B t^q+O(t^{q+1}), A B≠0.

Then min(p,q)=1. If p=q, necessarily p=q=1, A≠B, and (A-B)^2=D^2. If p=1<q, then q A^2=D^2. If q=1<p, then p B^2=D^2.

**Proof.** For p<q, f-g=A t^p(1+O(t)), so

psi=(p q A^2/D^2) t^{2p-2}(1+O(t)).

The constant nonzero value forces p=1 and the stated coefficient. Interchange f and g for q<p. If p=q and A≠B the leading expression is p^2(A-B)^2 t^{2p-2}/D^2. If p=q and A=B, let k>p be the first order at which f-g is nonzero; its contribution gives order 2k-2>0, impossible. These calculations also cover all higher-order leading cancellation cases. QED.

At these finite points both U and V are finite and nonzero, and U V=1. More precisely U^2=p/q. This follows directly from U's leading term: U=A/D when p=1<q; U=-pB/D when q=1<p; and U=(A-B)/D when p=q=1.

### Proposition 2 (common poles)

If f=A t^{-p}(1+O(t)), g=B t^{-q}(1+O(t)), then min(p,q)=1. If p=1<q, A^2=q; if q=1<p, B^2=p. If p=q, both are 1, their residues differ, and

(A-B)^2=A^2 B^2.

**Proof.** For p<q, f-g=-B t^{-q}(1+O(t)) and psi=(p q/A^2)t^{2p-2}(1+O(t)). For equal p with unequal residues the leading coefficient is p^2(A-B)^2/(A^2B^2) and the same exponent. If the leading principal parts agree, write f-g=O(t^{-r}) with r≤p-1 (or a holomorphic difference); psi then has positive order at least 2p, again impossible. QED.

The orders of U at a pole are

ord(U)=2p-max(p,q)-1.

Thus if (p,q)=(1,m), U has a pole of order m-1 and V a zero of order m-1. If (p,q)=(m,1), the roles reverse. Both factors are nonzero and finite at common simple poles. Away from B, neither derivative vanishes and f-g cannot vanish. Consequently all zeros and poles of U are supported on unequal common poles. **It is false that psi=1 by itself makes U and V entire.** Gundersen's example below is a control for this mistake.

**Exact gap:** these local restrictions do not bound the possible unequal multiplicities globally or prove an algebraic relation between f and g. Locally allowed does not mean globally realizable.

## 3. Approach 2: compactification and the Möbius-related subclass

### Proposition 3 (no rational pair)

There are no nonconstant rational f,g satisfying psi=1, even without the sharing condition.

**Proof.** For any nonconstant rational h, each A_k(h)=h^k h'/P(h), k=0,1,2, is O(1/z) at infinity. If h tends to a root of P, this follows by a local expansion and the logarithmic derivative; if h tends to a finite non-root it is smaller; if h tends to infinity it follows from h'/h=O(1/z). Expanding the square gives

psi=A_2(f)A_0(g)-2A_1(f)A_1(g)+A_0(f)A_2(g)=O(1/z^2),

contrary to psi=1. QED.

### Change-of-variable identities

For an entire h,

psi_{F∘h,G∘h}(z)=h'(z)^2 psi_{F,G}(h(z)).

For postcomposition of the pair and the shared values by T(w)=alpha w+beta, alpha≠0, psi is multiplied by alpha^{-2}. For T(w)=1/(w-a), where a is one of the three finite shared values, it is multiplied by P'(a)^2. These identities follow by the chain rule and cancellation of denominators; the verifier also checks them symbolically. General Möbius maps taking a member of B to infinity have one of these forms or their composition.

In particular, arbitrary entire precomposition of a known nonzero-constant-psi pair preserves psi=1 only if h'^2 is a fixed nonzero constant; then h is affine. This removes a spurious infinite-dimensional freedom without proving exhaustion by known pairs.

### Proposition 4 (complete Möbius-related classification)

Every target pair for which g=M∘f for a Möbius map M is of the following form, with the finite shared values permuted arbitrarily:

f(z)=T(exp(lambda z+b)), g(z)=T(exp(-lambda z-b)),

where T is a Möbius transformation taking {-1,0,1,infinity} to B, b is any complex number, and lambda is nonzero and satisfies lambda^2 c_T=1. Here:

- if T(w)=alpha w+beta, c_T=alpha^{-2};
- if T(w)=alpha/(w-r)+beta with r∈{-1,0,1}, c_T=(3r^2-1)^2/alpha^2.

Conversely every such pair satisfies all the required conditions.

**Proof.** M is not the identity, because psi is nonzero. A shared value a that is not fixed by M must be omitted by f, as must M^{-1}(a): otherwise sharing would imply M(a)=a. A nonconstant plane meromorphic function omits at most two sphere values by Picard's theorem. M fixes at most two values, so of the four shared values exactly two are omitted and exactly two are fixed. The omitted pair is permuted, not fixed, by M. Normalizing the omitted pair to 0 and infinity makes M(w)=c/w; rescaling its coordinate gives M(w)=1/w and the fixed pair {-1,1}. The normalized f omits 0 and infinity and therefore is exp(h) for an entire h; the normalized g is exp(-h). Direct substitution gives base psi=h'^2. The postcomposition identities give psi=c_T h'^2. Thus h'=lambda is a nonzero constant and h=lambda z+b. The reverse calculation verifies the converse. QED.

This is a complete restricted classification, not a solution of the target. In particular it does not assume that arbitrary four-value sharing implies Möbius dependence; that assertion is false.

**Exact gap:** eliminate or classify all non-Möbius-related pairs. Both subsequent examples show that eliminating them is impossible.

## 4. Approach 3: rational functions of one exponential

Consider f(z)=R(exp(lambda z)), g(z)=S(exp(lambda z)), lambda≠0, for rational R,S. This is an additional ansatz, not a consequence established for arbitrary target pairs.

### Proposition 5 (puncture and degree constraints)

At each t∈{0,infinity}, R(t) and S(t) are distinct members of B. Furthermore deg R=deg S=d, and exactly 2d points of C* lie over the four shared values, counted without multiplicity.

**Proof.** In the t coordinate the differential expression is

lambda^2 t^2 R'(t)S'(t)(R(t)-S(t))^2/[P(R(t))P(S(t))]=1.

At t=0 its bracketed expression must have order -2. Local expansions show that order -2 is possible only when R(0) and S(0) are distinct shared values; if one is not a shared value the order is at least -1, while if they agree it is at least 0. The same analysis in the local coordinate 1/t proves the assertion at infinity. This is a finite local expansion argument, including a pole as a shared value.

All critical points on C* lie over B, by psi≠0. Let e0,e∞ denote the local degrees of R at the two punctures and let n be the number of shared points on C*. Counting all four fibers gives total multiplicity 4d-e0-e∞ on C*. Their ramification is 4d-e0-e∞-n. Riemann-Hurwitz adds puncture ramification e0+e∞-2 to obtain 2d-2, whence n=2d. The same n works for S. QED.

### Proposition 6 (degree two)

If deg R=deg S=2 and the pair is not Möbius-related, it is obtained from Gundersen's pair

R0(t)=(t+1)/(t-1)^2, S0(t)=(t+1)^2/[8(t-1)]

by a common target Möbius map and by replacing t with a nonzero scalar multiple of t. The resulting constant psi is normalized to 1 by the change-of-variable identities.

**Proof, including one established external theorem.** Proposition 5 gives n=4. Suppose a shared value is omitted on C*. Its two full degree-two fibers are supported on the punctures. The puncture values of R and S differ, so R takes it at one puncture with local degree 2 and S at the other with local degree 2. Each map has at most one remaining critical point. Thus among the four shared points on C* at least two have multiplicity (1,1). In degree two any value with a (1,1) point is shared CM on C*: there is room for at most one further preimage in either fiber, which must also be common and simple. We have obtained two distinct CM values, one omitted and one attained. The established Gundersen 2CM+2IM theorem implies Möbius dependence, contrary to hypothesis. This invocation is explicitly credited, as summarized in Steinmetz 2011, §2; its general proof is not re-proved by our code.

Therefore all four shared values are attained; with n=4, each has exactly one C* preimage. If one point has multiplicity (1,1), the remaining preimages of its value must be at opposite punctures for the two maps. Only two puncture images remain to account for the other three values, so at least one of those values has its full degree-two fiber on C* for both R and S. Its single shared point would be (2,2), forbidden by Proposition 1 or 2. Hence all four points have multiplicities (1,2) or (2,1). Counting multiplicities shows each puncture is unramified for both maps.

Postcompose so that R(infinity)=0, S(infinity)=infinity, and scale t so their common pole is 1. The preceding fiber structure then forces, for alpha beta≠0 and r≠0,1,

R(t)=alpha(t-r)/(t-1)^2, S(t)=beta(t-r)^2/(t-1).

The remaining critical points are x=2r-1 for R and y=2-r for S. The simple fiber of S at x has its other point at 0, and likewise R's simple fiber at y. Therefore R(y)=R(0) and S(x)=S(0). These give

r^2-r-2=0 and 2r^2+r-1=0.

Their unique common root is r=-1. Equality of R and S at x=-3 gives beta=alpha/8; the equality at y=3 then also holds. This is the asserted family after an affine target scaling. QED.

Direct factorizations provide a separate check of the known example:

R0-1=-t(t-3)/(t-1)^2,
R0+1/8=(t+3)^2/[8(t-1)^2],
S0-1=(t-3)^2/[8(t-1)],
S0+1/8=t(t+3)/[8(t-1)].

On C*, the four fibers 0,1,-1/8,infinity are exactly at -1,3,-3,1, respectively, with complementary simple and double multiplicities. The factor t introduces no extra plane preimage after t=exp(lambda z). Direct computation gives base psi=8. Hence the explicit target pair is R0(exp(z/sqrt(8))), S0(exp(z/sqrt(8))) with these shared values, and arbitrary domain translation is allowed.

**Exact gap:** no upper bound on d has been proved. An unrestricted search through degrees or an assumption that all solutions have this rational-exponential form would not be a proof.

## 5. Approach 4: compact elliptic curves and ramification

Assume, additionally, that f and g are elliptic with a common period lattice.

### Proposition 7 (elliptic reduction)

Any distinct such pair sharing B has nonzero constant psi. After an affine rescaling of the domain it satisfies psi=1. If the common degree is d and at each shared point m_j denotes the larger of the two local multiplicities, then

number of shared points = 2d,   sum_j m_j=6d,   sum_j(m_j-3)=0.

**Proof.** Sharing cancels all possible poles of psi by the same expansions as in §2, without needing psi=1. Thus psi is entire and periodic in two independent directions, hence constant. It is not identically zero because neither derivative nor f-g is identically zero. Local restrictions from §2 apply after normalization. All ramification lies over B. For a degree-d map from a torus to a sphere, Riemann-Hurwitz gives total ramification 2d. The four fibers have total multiplicity 4d, so their union has 2d points. Applying this to each map shows their degrees agree. Every shared point has minimum multiplicity 1; adding the two maps' fiber multiplicities gives sum(1+m_j)=8d, which is the displayed balance. QED.

Consequences are limited but exact: a uniform pattern (1,q) requires q=3; if all larger multiplicities are at least 3 then they all equal 3; any points with larger multiplicity 1 or 2 require compensating multiplicities at least 4 elsewhere. The balance does not forbid mixed patterns. In particular it must not be used to erase Steinmetz's established third family with mixtures of (1,1) and (1,4) points (2011 survey, §2).

### Reinders's known elliptic example, independently checked

On the smooth elliptic curve v^2=12u(u+1)(u+4), use a uniformizing coordinate with u'=v and v'=6(3u^2+10u+4). Define

F=uv/[8sqrt(3)(u+1)], G=(u+4)v/[8sqrt(3)(u+1)^2].

They share {-1,0,1,infinity} with complementary simple and triple orders. At u=0 the orders are (3,1); at u=-4 they are (1,3); at u=-1 the pole orders are (1,3); at the elliptic point at infinity they are (3,1). The remaining fibers follow from

F^2-1=(u-2)(u+2)^3/[16(u+1)],
G^2-1=(u-2)^3(u+2)/[16(u+1)^3].

At u=±2, G/F=(u+4)/[u(u+1)]=1, so the signs of the shared values also agree. The local u-coordinate is unramified there because v≠0. These factorizations establish sharing, not just coincidence of the squared values.

Differentiating in this elliptic function field gives

U=12sqrt(3)/(u+1), V=4sqrt(3)(u+1), psi=144.

Thus F(z/12),G(z/12), with any uniformizing translation, is an explicit target pair. The construction is credited to Reinders; this calculation is verification, not discovery. The symbolic verifier works exactly modulo the elliptic curve equation, not by floating-point samples.

**Exact gap:** the degree and ramification balance do not classify elliptic covers, do not prove a bound on their primitive degree, and do not show arbitrary plane solutions are elliptic. The 2025 five-pair genus-zero theorem has a missing extra hypothesis here; indeed these elliptic examples prevent simply importing that conclusion.

## 6. Approach 5: differential systems, global continuation, and rescaling

On the ordinary locus, psi=1 is equivalent to the system

f'=U P(f)/(f-g), g'=P(g)/[U(f-g)],

where U is a meromorphic function with the divisor restrictions in §2. Choosing U or deriving this system is not a classification. Entire zero-free U,V follow if infinity is shared CM; they do not follow for the general target.

The scalar identity admits many local germs without settling global continuation. For example, set f=z near z=2, P(w)=w(w^2-1), and solve

g'=P(z)P(g)/(z-g)^2, g(2)=3.

The right-hand side is holomorphic near (2,3), so the analytic ODE existence theorem supplies a local germ, with g'(2)=144 and psi=1. This construction says nothing about a single-valued meromorphic continuation to the whole plane with all four shared fibers. The latter is precisely a missing global constraint.

### Proposition 8 (shrinking-rescaling obstruction)

Let f,g satisfy the target and let rho_n be nonzero with rho_n→0. Put f_n(z)=f(z_n+rho_n z), g_n(z)=g(z_n+rho_n z). If both sequences converge spherically locally uniformly to nonconstant meromorphic functions F,G, then F=G.

**Proof.** Their Mues expressions equal rho_n^2. If F and G were distinct, choose a point and a small neighborhood where both limits are finite, outside B, have nonzero derivatives, and differ. Such a neighborhood exists since the excluded sets are discrete. Spherical convergence there becomes ordinary holomorphic convergence, including derivatives. Passing to the differential identity gives

F'G'(F-G)^2/[P(F)P(G)]=0,

contradicting those choices. QED.

Thus shrinking Zalcman-type rescaling of this already normalized class loses distinctness whenever both nonconstant limits exist. It cannot justify replacing arbitrary solutions by distinct bounded-spherical-derivative examples. This sharpens the specific route obstruction; it is not an obstruction to the existence of the original pair.

**Exact final gap:** prove an exhaustive global classification of meromorphic plane pairs satisfying the local divisor restrictions and the differential identity, including non-Möbius pairs beyond degree-two rational-exponential and the exhibited elliptic families. No step here establishes algebraic dependence, finite order, bounded spherical derivative, or a bound on primitive algebraic degree for all solutions. The target therefore stays `unsolved` after 5/5.

## 7. Reproducibility, limitations, and disclosure

Run `python3 check.py` from this directory. The receipt records exact algebraic identities and explicit negative controls; `CONTROL_RESULTS.json` is deterministic apart from separately recorded environment metadata. Python 3 and SymPy 1.14.0 were used. A shell timeout of 120 seconds and one process suffice; no exhaustive search or numerical optimization is run.

The finite local multiplicity controls test p,q≤6. They are diagnostics, not a replacement for the proofs for all positive integers. Symbolic identities verify example formulas and transformation constants, not meromorphic global existence, Picard's theorem, Riemann-Hurwitz, or the cited 2CM+2IM theorem. Those dependencies and arguments are stated above. There is no proof-assistant formalization, expert peer review, or certified full classification.

Only the authored files enumerated by SHA256SUMS are proposed for publication. Downloaded source PDFs, extracted source text, complete dataset records, and private repository/source snapshots are excluded. There have been no remote writes in preparing this packet. Publication requires the campaign's separate audit and release gate.
