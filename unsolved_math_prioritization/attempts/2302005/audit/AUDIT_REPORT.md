# Independent audit: Rényi's two-value question

**Target:** 2302005 / AMR-022-2005, queue rank 518.  
**Reviewed:** 3 October 2026.  
**Verdict:** **PASS — full prior resolution of the explicit two-value existence question.**  
**Approved classification:** `already_solved`, one substantive attempt, with credit to A. A. Gol’dberg (1968).  
**Excluded claims:** a new result, a full classification of possible value sets, an unbounded-countable realization theorem, or prescribed finite growth order.

The six-file author packet was reviewed without alteration. The original theorem, its complete construction and interpolation proof on printed pp.191–198, and its bibliography on p.199 were read from the primary page images. The 2018 problem statement, update, and references were checked independently. The nontrivial approximation dependency was also located and its hypotheses checked in the primary Mergelyan exposition.

## 1. What the prior result resolves

The terminal question in Problem 2.5 is whether an entire function can assume exactly two values infinitely often in every open angle. Gol’dberg's theorem on p.191 realizes every bounded, closed, at-most-countable set as its set of fully scattered values. The specialization to `{0,1}` therefore answers that precise question affirmatively. His introduction explicitly identifies and answers Rényi's two-point question. [Original journal archive](https://real-j.mtak.hu/7416/).

The preceding broad question about possible value sets is not a solved classification problem in this packet. The metadata and prose consistently retain that boundary. Consequently the status approval is for the explicit existence question; it must not be expanded into a claim that all possible sets have been classified.

For a nonconstant entire function, angular density of the arguments of its nonzero a-points is equivalent to infinitely many distinct a-points in every open angle. Otherwise an angle containing only finitely many could be narrowed to avoid their finitely many arguments, contradicting density. Discreteness then makes these infinitely many points unbounded. The converse is immediate. No uniformity over values or angles is introduced.

The resulting function with value set `{0,1}` is nonconstant and transcendental: a polynomial has only finitely many preimages of each value unless it is the corresponding constant. For any distinct finite values a and b, replacing G by a+(b−a)G gives exactly `{a,b}`. Thus arbitrary prescribed pairs are covered without an additional hypothesis.

## 2. Target domains and angular construction

The target-plane domains need not be nested. Their intersection must equal the prescribed compact countable set. The construction on p.192 has this property. One can independently justify its finite polygonal covers by choosing a sufficiently fine rectangular grid whose finitely many horizontal and vertical cutting lines avoid the countable set; compactness permits shrinking occupied rectangles slightly while still covering the set. The resulting disjoint polygons have arbitrarily small diameters. A simple arc through them supplies the two simply connected domains at each scale.

A conformal map P_n from the unit disc to each domain can have its base point outside the countable target set. The inverse target set is compact, avoids zero, and stays away from the unit circle. This gives d_n≤|t|≤1−d_n with d_n>0. Both sides of this annular restriction are used: the upper bound controls the interpolating function, and the lower bound prevents cancellation in its local boundary estimate.

The lower half-plane and the translated dyadic upper sectors used in the packet match the primary formula. Their interiors map conformally to the upper half-plane by the specified affine or power maps. The polygonal joining arc makes a closed connected set κ; its pieces are locally finite because their vertices tend to infinity. Defining F by the sector functions and continuous interpolations on the joining segments gives a function continuous on κ and holomorphic in its interior.

For each fixed sector and target value, the inverse images of the interpolation circles have angular diameter tending to zero. Their angular centers differ by o(1) from the appropriate rescaling of the interpolation arguments. Dense tails, rather than an unjustified claim that any perturbed sequence is literally dense, give infinitely many contours in every smaller open angular interval. Their interiors are disjoint eventually, by radial separation and injectivity of the inverse conformal map.

## 3. The approximation dependency is applicable

The exact general-continuum statement appears in S. N. Mergelyan, *Uniform approximations of functions of a complex variable*, Uspekhi Mat. Nauk 7:2 (1952), 31–122, Chapter 2, §3, Theorem 1.3, printed p.69, equation (19.3). It states that, for a continuum E satisfying condition B, every function continuous at finite points of E and holomorphic in its interior has an entire approximant with error less than ε exp(−|z|^(1/2−η)), for prescribed ε>0 and η>0. [Primary bibliographic record and source](https://www.mathnet.ru/eng/rm8302).

Condition B is stated on printed p.59: complementary points admit Jordan paths to infinity outside E and outside discs of radii r(|z|), where r tends to infinity. The theorem on p.69 reuses condition B alone. It does not require the empty-interior condition A of the separate Carleman-continuum theorem on p.59. This distinction matters because κ contains sectors with interior. The 1945 Jordan-domain formulation by itself would be too narrow to cite without this extension.

Here is a quantitative check of B, strengthening the original paper's brief half-ray observation. Write α_n=π2^(1−n). Rotate the gap between the n-th and (n+1)-st upper sectors by −α_n. It is a semi-infinite strip capped by the joining segment. That segment's longitudinal coordinates are n2^n cos α_n and (n+1)2^(n+1), both nonnegative. The forward strip ray therefore increases its longitudinal coordinate and cannot decrease modulus. The leftmost complementary component has leftward horizontal rays with negative real part, which also increase modulus. The remaining component has rightward horizontal rays and real part at least −8.

To avoid an irrelevant convention at the original origin, translate to w=z+i, so 0 belongs to κ+i. In the right-escape component, a point with x<0 satisfies y+1≥|x|/8: below the real axis this follows from the first joining segment, and above it from −8≤x<0. Its rightward ray stays at distance at least |w|/√65 from the new origin. The other rays still have nondecreasing modulus after translation. Thus condition B holds with r(t)=t/√65 for t>0. Each ray is a Jordan path.

Apply the theorem with η=1/4 and ε=e^(−1) to the translated function. The resulting error is less than exp(−1−|z+i|^(1/4)), which is at most exp(−|z|^(1/4)), since |z|^(1/4)≤|z+i|^(1/4)+1. This verifies exactly the error needed by Gol’dberg's argument. The approximation theorem remains an explicitly identified external theorem; it is not reproved by this audit.

## 4. Independent check of the interpolation estimates

The primary proof uses widely separated nodes ζ_j=r_j exp(iθ_j), a bounded Blaschke product omitting the j-th node, and a localized factor Φ_j(ζ)=(ζ/r_j)^δ exp(−(ζ/r_j)^δ). The radii can meet the height and angular restrictions simultaneously with r_(j+1)>r_j^(1+2/δ), where 0<δ<1/4. Nodes may be assigned so that each target value has dense angular tails.

The product converges locally uniformly, including on compact boundary intervals: separation gives a summable reciprocal-radius bound. Its modulus is at most one on the closed upper half-plane. At the omitted node its modulus has the positive lower bound given by the squared product of (1−B^(−k))/(1+B^(−k)), which tends to one as B tends to infinity.

Normalizing the products gives h_j(ζ_k)=1 for j=k and zero otherwise. The denominator from Φ_j is bounded below by e^(−1). Splitting the numerator sum at the radius closest on the logarithmic scale and summing its two geometric tails gives the stated bound on the sum of |h_j|, with limiting ratio one as B tends to infinity and δ=(log log B)^(−1). Consequently the interpolation series converges locally uniformly, is continuous on the closed half-plane, and has modulus below 1−d/2 after B is chosen sufficiently large.

On |ζ−ζ_j|=1, the logarithm of h_j has leading term

δ(1−exp(iδθ_j))(ζ−ζ_j)/ζ_j.

Its modulus is at least (2δ²/π)r_j^(−5/4), by θ_j>r_j^(−1/4). The logarithmic derivative of the omitted-node Blaschke product is bounded by a constant times r_(j−1)/r_j² + 1/r_(j+1), hence by O(r_j^(−5/3)). This exponent was verified visually on original p.197, not taken from imperfect OCR. The localized-factor Taylor error O(r_j^(−2)) is smaller still. All bounds are uniform on the unit circle.

Since 5/3>5/4, the leading term cannot be cancelled by those errors. Also h_j−1 is asymptotic to log h_j because the latter tends uniformly to zero. The other normalized terms have total modulus O(r_j^(−2)), as follows from equation (18) on p.198 and the stronger radial separation. Multiplication by |t_j|≥d therefore leaves a positive constant times r_j^(−5/4) as the boundary lower bound for |f−t_j|. No cancellation or summation gap remains.

The printed choice r_1=1 is inconsistent with Im ζ_1≥2. The frozen packet correctly starts the radii sufficiently large instead; all subsequent bounds only require lower bounds and separation. This harmless finite initialization correction does not alter the construction or credit.

## 5. Both inclusions survive approximation

For an included target a and fixed sector n, univalence of P_n on a compact subdisc gives a positive minimum modulus of its difference quotient, including its nonzero diagonal derivative. It transfers the interpolation-circle lower bound to a polynomial lower bound on |F−a| on each inverse contour. The entire-approximation error decays faster than every fixed polynomial. Rouché's theorem therefore preserves at least one a-point in each sufficiently distant contour. Dense angular tails and shrinking contour widths imply infinitely many distinct a-points in every angle. This proves A⊆E(G).

For b outside A, some target domain D_n excludes b. The entire image of its source sector under F lies in a compact subset of D_n, at a positive distance from the complement. The approximation tends to zero, so G excludes b on that sector sufficiently far out. A strictly interior angular interval has its whole sufficiently distant tail in the translated sector. Only finitely many b-points can remain in its compact initial portion. This proves E(G)⊆A. The selected sector and radius may depend on b, as the negated quantifiers permit.

Using a strictly interior angle, as the frozen verification does, also avoids an endpoint issue in the original lower-half-plane exclusion sentence. That repair is elementary and requires no stronger theorem.

## 6. Source, status, and scope controls

- The original theorem is bounded, closed, and at most countable. The proof-added note dated 4 December 1967 extends to bounded countable A with A⊆D(G)⊆closure(A). Its boundedness is not discarded.
- The 2018 Update 2.5 omits boundedness in its summary. That broader wording is unnecessary to the finite case and does not support an unbounded extension here.
- The publication year is 1968. The receipt date of 24 April 1967 and proof-added-note date are not publication dates.
- References [310] and [311] on printed p.221 of the 2018 edition have the same author, journal volume, pages, and year, with English and German title descriptions. They represent the same Russian article, not two independent resolutions. [2018 source edition](https://arxiv.org/abs/1809.07200v2).
- The 1966 lecture-note leaf containing the original question was not independently recovered; the 1968 original paper and 2018 problem statement provide direct, mutually consistent evidence sufficient for this audit.
- One substantive attempt is accurately recorded. An already published exact answer does not require four further speculative attempts.

## 7. Reproducibility and release boundary

The author's packet consistency check passed on the frozen bytes. Separate independent controls also passed: all six frozen hashes, the exact public allowlist, scoped status flags, relative links, and relevant exponent comparisons. Negative controls reject altered frozen bytes, a novelty claim, an overbroad classification claim, and the incorrect OCR exponent 1/2.

These finite checks are supplements. They do not prove the interpolation lemma, approximation theorem, or transcendental-entire existence statement. The PASS rests on the source reading and mathematical checks above.

The release material consists of the six frozen author files and the sanitized audit report and controls identified by the audit manifest. Source PDFs, page images, OCR, catalogue extracts, full-source copies, and operational research material are excluded. No remote state was changed during this audit.

**Final recommendation:** accept the credited `already_solved` correction for the explicit two-value question, with all stated scope limits retained. There is no blocking defect in the frozen packet.
