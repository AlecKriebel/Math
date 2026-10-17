# A five free blowup counterexample to the Nash intersection assertion

## Main result and scope

Five successive free blowups of the smooth complex surface germ along the smooth branch y=0 give a prime divisor E=D5 with the following property. Let Dj be the divisor created by the jth blowup, and let Fk(E) consist of every prime divisor with the same combinatorial type as E and the same first k blowup centers. In the formal arc space, put Ik(E)=intersection over E′ in Fk(E) of the closed Nash sets Nbar(E′). Then

    I2(E) = {ord_t x >= 3, ord_t y >= 5},
    I3(E) = {ord_t x >= 2, ord_t y >= 5}.

Every reference prefix divisor has valuation ord_Dj=(1,j), and

    C(q ord_Dj) = {ord_t x >= q, ord_t y >= jq}.

Neither intersection equals C(q ord_Dj) for any reference j in {1,2,3,4,5} and any positive integer q. Indeed, equality would require respectively q=3 and 3j=5, or q=2 and 2j=5. This disproves the explicitly mapped natural readings of the primary-source Nash-intersection assertion below. The bare relation and indices in the general printed formulation remain unauthenticated; no author-approved erratum or unspecified replacement statement is claimed.

The primary source uses intersection. A catalogue union transcription is not the mathematical assertion addressed here. This result concerns the stated intersection assertion, not the paper's Conjecture 2 or the broader Nash problem. No global novelty claim is made.

## Coordinates and exhaustive families

Number the successive centers c1=0,c2,...,c5, with Dj created at cj. For the reference branch y=0, a chart following j blowups is

    (x,u_j) -> (x,y=x^j u_j).

For j>=2 the newest divisor Dj is x=0, and the previous exceptional component meets it at u_j=infinity. To see the excluded point, blowing up a finite point (x,u_j)=(0,a) has charts

    u_j=a+xu_(j+1),
    x=zh, u_j=a+h.

In the second chart the new component is h=0, the old component is z=0, and u_(j+1)=1/z on the overlap. Thus the omitted value is exactly the satellite intersection with the old divisor. Every free center is represented once by a finite complex number a. The exceptional configuration is the chain with self-intersections (-2),(-2),(-2),(-2),(-1).

For F2, every allowed completion is determined by a2,a3,a4 in C; for F3, every allowed completion is determined by a3,a4 in C. A blowup on an older component away from the newest one would leave an extraneous blowup in the model of the resulting prime divisor; a blowup at an intersection is satellite and changes the proximity type. Neither belongs to the same minimal all-free type. Successively subtracting a chosen coefficient and dividing by x therefore exhausts the whole family, rather than selecting a subfamily.

Write P(x)=sum from j=k to 4 of a_j x^j, where k=2 or 3. A chart of the final divisor is

    (x,w) -> (x,y=P(x)+x^5 w).

Consequently its valuation in the regular coordinates (x,z=y-P(x)) is monomial of weights (1,5).

## Exact closed Nash cylinders

For every completion, the coordinate change (x,y)->(x,z=y-P(x)) is a polynomial automorphism. The cylinder

    S_P={ord_t x>=1, ord_t(y-P(x))>=5}

is irreducible and reduced: its coordinate ring is a polynomial ring in the unrestricted coefficients of x and z. The nonempty open subset ord_t x=1 is dense. Its arcs have w=(y-P(x))/x^5 in C[[t]] and meet the final divisor transversely at a finite point, hence away from other exceptional components. Conversely transverse arcs satisfy these bounds. Thus their closure is exactly S_P. The definition of the closed Nash set gives the same closure of the transverse locus. Alternatively, in the other chart with coordinates (v,h), the base map is x=vh and y-P(x)=v^4 h^5; every lifted arc meeting the final component h=0 also has the required bounds.

Accordingly Nbar(E_P)=S_P, including constant arcs and arcs with identically zero x through closure. This uses a proved closure identity, not an unproved converse from valuative inequalities to Nash inclusion.

For Dj, the analogous chart y=x^j u gives the irreducible order cylinder {ord x>=q,ord y>=jq}. Its dense open ord x=q lifts with order q along Dj. A smaller open with u(0) nonzero avoids any additional chosen centers and has the same closure. In the other chart x=vh,y=v^(j-1)h^j, exact order q of h also implies the displayed bounds. Thus C(q ord_Dj) has exactly these two thresholds. Exact-q and at-least-q versions have the same closure in these examples.

## Computing the two intersections

For F2 take the all-zero polynomial P and P=x^2. Their common conditions force ord y>=5 and ord x^2>=5, so ord x>=3. Conversely those bounds imply ord P(x)>=6 for every P=a2 x^2+a3 x^3+a4 x^4. They therefore imply every family member's condition. This proves I2=(ord x>=3,ord y>=5).

For F3 use P=0 and P=x^3. Their common conditions force ord y>=5 and 3 ord x>=5, equivalently ord x>=2. These imply every condition with P=a3 x^3+a4 x^4. This proves I3=(ord x>=2,ord y>=5).

These are equalities of closed sets, or equivalently reduced supports. At the four-jet level the F2 ideal includes the coefficients of x(t)^2 below degree 5; its radical kills x1,x2 and y1,...,y4. The F3 radical kills x1 and y1,...,y4. Before taking radicals, nilpotents may remain. The assertion is not a scheme-theoretic equality with a reduced coordinate ideal.

## Uniform exclusion of every contact multiplicity

Two independent coordinate order cylinders {ord x>=A,ord y>=B} and {ord x>=C,ord y>=D} agree only if A=C and B=D. For instance choose a monomial in one coordinate at its threshold and take the other coordinate of arbitrarily large order. Applying this observation excludes all positive integers q, without finite truncation of q.

Explicit witnesses also give a uniform separation. For I2 let r=3; for I3 let r=2. If q<r, the arc (t^q,t^max(5,jq)) lies in C(q ord_Dj) but not in Ik. If q>r, (t^r,t^5) lies in Ik but not C(q ord_Dj). If q=r and jr>5, the same latter arc separates them. If q=r and jr<5, (t^r,t^(jr)) belongs to C(q ord_Dj) and not Ik. The remaining case jr=5 never occurs for r=2 or 3 and integer j. These are nonconstant polynomial arcs.

## Mapping the printed notation to the tested assertions

Select the middle free center c3. Both c4 and c5 still follow it, so fixing this selected point does not make the family a singleton.

1. Last-shared normalization: c3 is first movable, so use F2 and D2. Equality would require (3,5)=(q,2q).
2. Literal created-divisor expression with zero-based centers p0=c1,p1=c2,p2=c3: reading the bare relation as the nearby defined contact-at-least-2 relation gives F2, while the printed divisor created at p2 is D3. Equality would require (3,5)=(q,3q).
3. Fix the selected free point as well: use F3 and D3. Equality would require (2,5)=(q,3q).
4. One-based local labels p3=c3 with contact at least 3: again F3 and D3. This does not purport to reconcile every other index in the source.

Every listed variant fails. As an additional conditional reading, if the undefined bare relation meant exact contact k, its intersection is the same here. The two completions P=x^k and P=2x^k have exact contact k with the all-zero reference. Their simultaneous conditions imply ord x^k>=5 and then ord y>=5. Conversely these bounds imply every exact-contact completion. This observation does not claim the source defines that bare relation as exact contact.

The source's definitions encompass all prime exceptional divisors, including nonsatellite divisors and further free blowups after resolving an associated branch. There is no source-stated restriction to singular curvettas, satellite final divisors, or minimal embedded resolutions of singular branches. The selected center is genuinely free. Imposing any of those restrictions would change the assertion's quantifier rather than invalidate this example.

## The minimal example and the general formula

For n successive free blowups and a fixed prefix of k centers, with 2<=k<n, choose (x,z) so the fixed branch jet is z=0. The same induction exhausts the completions by polynomials P=sum from j=k to n-1 of a_j x^j and proves

    Nbar(E_P)={ord x>=1,ord(z-P(x))>=n}.

The members P=0 and P=x^k force ord z>=n and k ord x>=n. These bounds suffice for every remaining member. Hence

    Ik(E)={ord x>=ceil(n/k),ord z>=n}.

It equals C(q ord_Dk)={ord x>=q,ord z>=kq} exactly when k divides n, in which case q=n/k. The smallest normalized counterexample is n=3,k=2, yielding thresholds (2,3). In that case the intersection is the Nash set of the satellite divisor obtained by blowing up D1∩D2, with chart x=p^2 u,y=p^3 u^2. It is not a multiple of D2.

The three-blowup example alone would be insufficient to defeat a convention fixing the final selected center, because that family becomes a singleton. Five blowups remove that loophole. The question of computing q was conditional on the asserted equality being true; the counterexample negates that premise. The positive divisibility cases in this paragraph are only an explicitly proved all-free subcase.

## Sources and acceptance

The formulation and definitions are credited to Fernández de Bobadilla, Pe Pereira, and Popescu-Pampu, [On the generalized Nash problem for smooth germs and adjacencies of curve singularities](https://arxiv.org/abs/1501.06898v3), especially [§2, §4.1 and §4.2](https://arxiv.org/pdf/1501.06898v3), and [Pe Pereira's workshop contribution, printed pp.2678–2680](https://ems.press/content/serial-article-files/46651). The toric consistency check is credited to Ishii, [Maximal divisorial sets in arc spaces](https://arxiv.org/abs/math/0612185), [Example 2.10, Proposition 3.4 and Lemma 3.11](https://arxiv.org/pdf/math/0612185).

The primary paper already provides combinatorial invariance, finite cylindrical realization and relevant inclusion results. The first-exceptional-divisor specialization in Remark 4.14 is not contradicted. The proof here is elementary and direct; no novelty search or novelty conclusion is asserted.

The full accepted normalized proof and mathematical audit accompany this report as [NORMALIZED_COUNTEREXAMPLE.md](NORMALIZED_COUNTEREXAMPLE.md) and [AUDIT.md](AUDIT.md). [SOURCE_SCOPE_ACCEPTANCE.md](SOURCE_SCOPE_ACCEPTANCE.md) records the interpretation verdict and evidence limitations. [CERTIFICATES.json](CERTIFICATES.json) records exact-control results and source identities. Those finite controls supplement the analytic family exhaustion, closure and all-q arguments; they do not replace them.
