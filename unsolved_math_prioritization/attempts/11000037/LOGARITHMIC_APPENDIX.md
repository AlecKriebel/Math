# Additional proved logarithmic bounds, with limit existence kept separate

This appendix is a partial supplement to MATHEMATICAL_REPORT.md, not a solution of the arbitrary-generating-set density conjecture or of the requested exact logarithmic density. No novelty is claimed for its standard conjugacy-counting and free-subgroup mechanisms.

For g>=2 and a finite symmetric generating set S of G=Mod(S_g), define

D_lower(S) = liminf_(n->infinity) log |I_g intersection B_S(n)| / log |B_S(n)|,
D_upper(S) = limsup_(n->infinity) log |I_g intersection B_S(n)| / log |B_S(n)|.

These always exist as extended liminf/limsup; below they are real and belong to [1/2,1]. We do not assert that they agree for an arbitrary S.

## Proposition 3 (the half-growth bound)

For every g>=2 and every S as above,

1/2 <= D_lower(S) <= D_upper(S) <= 1.

### General conjugacy lemma

Let G be a finitely generated group, N a normal subgroup, and h in N. Set ell=|h|_S. If

|C_G(h) intersection B_S(2n)| <= K(n+1)

for a constant K and all n>=0, then

|N intersection B_S(2n+ell)| >= |B_S(n)|/[K(n+1)].

Indeed x -> xhx^(-1) maps B_S(n) into N intersection B_S(2n+ell). If x and y have the same image, y^(-1)x belongs to the centralizer and has length at most 2n. For any fixed y, the map x -> y^(-1)x injects that fiber into C_G(h) intersection B_S(2n). The fiber bound proves the inequality. Normality is used exactly to ensure that the images lie in N.

### Checking the hypothesis in Torelli

The classical input that I_g contains a pseudo-Anosov h for every g>=2 follows, for example, from Farb-Leininger-Margalit, *The lower central series and pseudo-Anosov dilatations*, Theorem 1.1 (arXiv:math/0603675v2, p.2). Their finite upper bound for the least pseudo-Anosov log-dilatation supplies existence; none of their numerical dilatation estimates is needed here.

McCarthy, *Normalizers and centralizers of pseudo-Anosov mapping classes*, Theorem 1 and Corollary 2 (author manuscript dated June 8, 1994, p.1), proves that C_G(h) is virtually infinite cyclic. In a virtually cyclic group every infinite cyclic subgroup has finite index: intersect it with a finite-index cyclic subgroup, then use the elementary finite-index property of nontrivial subgroups of an infinite cyclic group. Consequently <h> has finite index in C_G(h).

The subgroup <h> is undistorted in the ambient word metric. For completeness, use the standard pseudo-Anosov Teichmuller axis, on which h acts by a translation of length log lambda(h)>0. Fix x on this axis and let L = max_(s in S) d_T(x,sx). L is positive, for otherwise G fixes x and so does h. The triangle inequality gives d_T(x,gx) <= L |g|_S. Thus

|h^m|_S >= |m| log lambda(h)/L.

Choose finite coset representatives r_1,...,r_M for <h> in C_G(h), and put R=max_i |r_i|_S. If |r_i h^m|_S <=2n, then |h^m|_S <=2n+R. There are at most 1+2L(2n+R)/log lambda(h) possible integer m for each i. This proves the required linear centralizer bound. The standard Teichmuller translation fact is recalled in Farb-Leininger-Margalit, p.1.

### Passing from conjugacy counts to ratios

Write b(n)=|B_S(n)| and a(n)=|N intersection B_S(n)|. Submultiplicativity b(n+m)<=b(n)b(m) implies existence of

h_S = lim_(n->infinity) log b(n)/n.

Here h_S>0: the explicit homologically free rank-two subgroup in MATHEMATICAL_REPORT.md has a pair of generators of bounded S-length, and its distinct positive words already give exponential ambient growth. For arbitrary large r put n=floor((r-ell)/2). Monotonicity and the conjugacy lemma give

log a(r) >= log b(n) - log(K(n+1)).

Dividing by r and using n/r ->1/2 yields liminf log a(r)/r >= h_S/2. Since log b(r)/r ->h_S>0, this proves D_lower(S)>=1/2. The upper bound one follows from a(r)<=b(r). QED.

## Corollary 4 (sharp infima over generating sets)

Fix g>=2 and any prescribed finite subset F of G. Among finite symmetric generating sets S containing F (allowing a harmless identity generator if F contains it),

inf_S D_lower(S) = inf_S D_upper(S) = 1/2.

Proof. Start with fixed symmetric T containing F and a generating set, and let d=|T|. For the sets S_k of Theorem 1 in MATHEMATICAL_REPORT.md, that theorem implies

D_upper(S_k) <= log(d+2 sqrt(2k-1))/log(2k-1).

The right side tends to 1/2 as k tends to infinity. Proposition 3 gives the matching lower bound for every S, and D_lower<=D_upper. QED.

The infimum is not asserted to be attained. Even if it is not attained, the statement above is exact. It also does not establish that the logarithmic density itself exists for any particular S_k. An exponentially negligible subgroup may still have logarithmic ratio close to one, and a logarithmic bound is not the missing transfer to a previously fixed arbitrary generating set.

## Source links and verification limits

- Farb-Leininger-Margalit: https://arxiv.org/abs/math/0603675 and versioned PDF https://arxiv.org/pdf/math/0603675v2 . PDF pp.1-2 were visually inspected. The downloaded v2 carries the historical 26 August 2007 arXiv margin and a November 26, 2024 title-page date, apparently a rendering timestamp; no claim of a 2024 new mathematical revision is made.
- McCarthy author manuscript: https://users.math.msu.edu/users/mccarthy/publications/normcent.pdf . The web PDF parser exposed Theorem 1 and Corollary 2 on p.1, and the author's abstract https://users.math.msu.edu/users/mccarthy/publications/normcent.abstract.html independently confirms the centralizer statement. Direct local retrieval returned a non-PDF body, and a web screenshot request did not expose image pixels in this tool interface; no local-PDF hash or visual inspection of that page is claimed. This is an attributed established theorem, not a fresh proof audit of McCarthy's paper.
