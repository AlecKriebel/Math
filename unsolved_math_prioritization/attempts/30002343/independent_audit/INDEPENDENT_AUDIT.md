# Independent audit: stable log surface degree-five partial result

Problem 30002343, OWR-12490-003, queue rank 984. Audit date: 2026-10-07 UTC.

## Verdict

**Accept the frozen packet as a mathematically correct PARTIAL result. No mandatory mathematical correction was found.** In particular, Theorem 5.1 is valid with its stated hypotheses, including its claims for every scheme-theoretic length-two cluster. It does not prove the unrestricted degree-five assertion. The weighted example and the smooth cyclic-cover calculation are correct. The first question is disproved only on the packet's explicitly literal, ordinary-canonical interpretation.

The original packet was not changed. Its manifest has SHA-256 `fe1428032c46c505cfa5e60dc7dd7a13b64535c2b90da8c00c83c85d95db53d8`. All eight listed payloads, totaling 33,812 bytes, match their recorded sizes and hashes. The author checker, manifest checker, and independently reconstructed arithmetic checks pass. The saved author output equals fresh output as parsed JSON.

This report contains authored analysis, mathematical reconstructions, public bibliographic information, and verification metadata. It contains no source PDFs, copied passages, dataset contents, or private coordination material. No remote writes or publication were performed.

## 1. Exact scope and source formulation

The applicable category is connected, reduced, projective, pure-dimensional complex surfaces satisfying the demi-normal and semi-log-canonical conditions, with a reduced boundary avoiding conductor components and with ample Q-Cartier log canonical divisor P = K_X + Delta. Set L = IP, where I is the least positive Cartier index. Merely being slc is insufficient: ampleness is used repeatedly. All multiples used as line bundles really are Cartier.

The original report's printed page 1598 was checked both in extracted text and in its rendered image. It really displays the ordinary K_U in the first question while describing a stable log pair and allowing reduced boundary. Its separate second question uses 5I(K_X + Delta). The counterexample in the packet is therefore a valid correction of the first question's literal wording, without settling either a logarithmic reinterpretation or the second question. The volume year is 2013; the publisher gives 17 March 2014 as publication date. These dates are not contradictory.

The packet correctly distinguishes the index-one convention for a *pair* from the assertion that K_X alone is Cartier. It also correctly distinguishes the open Gorenstein locus from the whole projective surface. One cannot obtain an index-independent exponent on that open locus merely by proving a statement about the global Cartier multiple L.

## 2. Dependency audit

The full statements and relevant surrounding proofs were read in Liu--Rollenske, arXiv:1211.1291v4, and the original curve theorem in Catanese--Franciosi--Hulek--Reid, arXiv:alg-geom/9607021v1. This was not an abstract-only check.

### 2.1 Vanishing and restriction

LR Proposition 3.6 applies to every integral exponent k >= 2 in the reflexive log canonical powers and gives vanishing of positive-degree cohomology. In the restriction sequence for C in |3L|, the kernel is the invertible sheaf O_X(2L). Its exponent relative to P is 2I, which is at least two. Thus H^1(X,2L)=0 is justified, with no appeal to a generally invalid exponent-one vanishing.

For T = D union Delta, LR Corollary 3.5 applies to the ideal of this reduced curve. At a Cartier multiple, twisting that ideal and taking the reflexive hull does not change the ideal-twist sheaf: O_X is S_2, O_T is Cohen--Macaulay of dimension one, and the ideal is S_2 by the depth lemma. Consequently the ordinary restriction exact sequence gives surjectivity from H^0(X,5L) to H^0(T,5L|T). LR Proposition 4.8 gives very ampleness on T at coefficient five for every index. The empty T case is vacuous.

### 2.2 Global generation and finiteness

LR Theorem 4.1 supplies global generation of 3L when I >= 2 and of 5L for every index. It does not supply global generation of 2L. The packet never assumes the latter without labeling it as an additional hypothesis.

A globally generated positive multiple of ample L defines a finite morphism. Indeed its pullback of O(1) is ample. A positive-dimensional projective fiber would contain a curve on which that ample line bundle has degree zero, a contradiction. Proper and quasi-finite then implies finite. This finiteness is the hypothesis used in LR's hyperplane construction, and is available here.

### 2.3 LR Lemma 5.4(i), including infinitesimal clusters

The restriction in Lemma 5.4(i) is precisely global generation plus failure to embed the given length-two subscheme. Part (i) has no extra requirement m >= 4 and no nodality hypothesis. Those restrictions occur in a different clause, part (ii), and are not needed in the packet. Thus applying part (i) with m = 3 and I >= 2 is legitimate.

Over C, a scheme of length two is either two distinct reduced points or one local dual-number scheme. With a globally generated line bundle, failure of its evaluation map to have rank two means rank one. Its projective image is then a reduced point even for the dual-number case: after choosing a nonvanishing section as denominator, all projective coordinate ratios restrict to constants. Every target hyperplane through this image point therefore pulls back to a divisor containing the cluster *as a scheme*, not just its support.

The finite morphism has only a finite base fiber above that point. A general hyperplane through it avoids entire images of conductor, boundary, and branch components. In characteristic zero, away from those components its pullback is generically reduced; the Cartier pullback is Cohen--Macaulay, so generic reducedness implies reducedness. The hyperplane can also avoid containing any image surface component, so its pullback really is Cartier. These facts reconstruct the mechanism behind the cited part (i).

There is no need to invoke part (ii), no hidden assumption about chi(O_X), and no restriction to ordinary reduced pairs of points.

### 2.4 Subcurves and the CFHR criterion

LR Lemma 5.6 applies to a reduced log-well-behaved curve C in |mL| and every subcurve B of C. It yields

    2 p_a(B) - 2 <= (m + 1/I)(L.B).

The Cartier curve C is Cohen--Macaulay because X is a two-dimensional S_2 scheme. For the CFHR theorem the relevant subcurves are pure one-dimensional Cohen--Macaulay subschemes, not arbitrary quotients with additional embedded point structure.

Every such subcurve of a reduced C is reduced. At each surviving generic point its local ring is a quotient of a field and is therefore that field. Its nilradical is consequently supported on finitely many closed points. A Cohen--Macaulay curve has no nonzero point-supported subsheaf of its structure sheaf, so that nilradical must vanish. A reduced subcurve is generically Gorenstein. Therefore the reduced subcurves checked by the packet exhaust all CFHR subcurves; no nonreduced or embedded-point exception is omitted.

CFHR Theorem 1.1 gives the sufficient criterion deg(M|B) >= 2p_a(B)+1 for every such B. LR Theorem 2.15 records this same sufficient version. The original CFHR theorem has a further borderline refinement; ignoring that refinement makes the criterion weaker, not invalid. The packet does not claim its numerical exceptions are actual non-embeddings.

## 3. Independent reconstruction of Theorem 5.1

Suppose I >= 2 and 3L does not separate a length-two subscheme xi. The preceding construction gives a reduced log-well-behaved C in |3L| containing xi scheme-theoretically. Vanishing makes H^0(5L) -> H^0(C,5L|C) surjective.

For each nonempty CFHR subcurve B, put d = L.B and g = p_a(B). Since L is ample and Cartier, d is a positive integer. The published genus estimate is

    2g - 2 <= (3 + 1/I)d.

If d = 1, the right side is at most 7/2, so integrality gives g <= 2 and 5d >= 2g+1. If d >= 2, then

    5d - (2g-2) >= (2-1/I)d >= 3.

Thus CFHR embeds all of C by 5L|C. Composing the restriction maps separates xi on X. This argument includes tangent vectors at every kind of slc point, provided 3L contracts them; it does not require those vectors to lie in the conductor or in a smooth surface chart.

Next suppose 3L separates xi and its support avoids Bs|2L|. For each of its at most two support points, vanishing there is a proper hyperplane in H^0(2L). A vector space over C cannot be a union of these finitely many proper subspaces. Choose s avoiding them. On each local Artin algebra of xi, the residue of s is nonzero, so s is a unit. Multiplication by s is therefore an isomorphism from 3L|xi to 5L|xi, including on the nonreduced dual-number scheme. Multiplying the separating sections of 3L by s supplies the required global sections of 5L. Surjectivity of the entire multiplication map of global-section spaces is neither claimed nor needed.

Combining these cases proves the first two claims. If 2L is globally generated, the second applies to every xi, so the length-two criterion implies that 5L is very ample. Finally, 5L is globally generated in general; any failure of its closed-immersion property is witnessed by a length-two subscheme. Such a witness must meet Bs|2L|, must already be separated by 3L, and cannot be scheme-theoretically contained in T.

This is a genuine improvement of the numerical curve-restriction bound to coefficient five on the stated branch. It is not an improvement of the general published surface bound without additional hypotheses. Coefficient four cannot be certified by these numerical inputs alone: at I = 2 the allowed pair d = 1, g = 2 has 4d < 2g+1. No geometric realization of that numerical test is asserted.

### Index one

When I = 1 the bound becomes g <= 2d+1. For d >= 3 this implies 2g+1 <= 5d. At d = 1 or 2 the only integer exceptions are respectively g = 3 or 5. Negative arithmetic genera, possible for disconnected subcurves, introduce no additional exception because the target inequality is then automatic. Thus Proposition 5.2 correctly identifies exactly the failures of this sufficient numerical criterion.

Those pairs are not established to occur, and even their occurrence would not prove non-very-ampleness. In addition, degree-three global generation can fail at index one, so the curve construction is not automatically available there. The packet correctly retains both limitations.

## 4. Explicit examples independently checked

### 4.1 The smooth plane quartic pair

For the Fermat quartic on P^2 the gradient has no common projective zero. The pair is log smooth with reduced boundary; hence it is lc. Its log canonical divisor is H, ample and Cartier. The relevant open locus is the whole surface under either the ordinary or pair index-one interpretation. Ordinary positive pluricanonical sections vanish because rK = O(-3r). The logarithmic system, in contrast, is O(r) and embeds already at r = 1. This is a valid literal counterexample and no logarithmic counterexample.

### 4.2 The weighted surface and its special point

For S: w^2 = z^5 + x^10 + y^10 in P(1,1,2,5), the cone gradient only vanishes at the origin. The ambient singular locus consists of the two coordinate points of weights two and five; both miss S. Thus S is smooth. Weighted adjunction gives K_S = O_S(1), an ample line bundle. The right-hand side is nonsquare in C(x,y)(z), since its valuation at the z-infinity place is -5. Hence the hypersurface is integral and the projection forgetting w is generically degree two.

The weighted hypersurface ring is Cohen--Macaulay of dimension three. Its local cohomology in degrees zero and one at the irrelevant ideal vanishes, so the graded ring pieces agree with H^0(S,O_S(m)). Below degree five none contains w. Thus all those rational maps factor through the degree-two projection and cannot be birational. This reasoning does not incorrectly assume they are everywhere-defined morphisms.

In degree five, x^5 and y^5 cover their respective ordinary affine charts and their section ratios recover the full affine coordinate algebras, including w. On their complement x = y = 0 there is exactly one weighted orbit P with z,w nonzero. The section w covers it, so the degree-five system is basepoint-free.

Here is an explicit algebraic verification of the compressed local-parameter argument in the packet. On z,w nonzero define invariant functions

    a = x z^2 / w,    b = y z^2 / w,    u = z^5 / w^2.

Set r = w/z^2, an invertible function of weight one. Then x = ar, y = br, z = ur^2, w = u^2 r^5. Taking the weight-zero ring identifies this affine quotient chart with

    Spec C[a,b,u,u^(-1)] / (u^4(1-u)-a^10-b^10).

The special point is (a,b,u) = (0,0,1). The derivative with respect to u is 4u^3-5u^4, equal to -1 there. Thus a,b are a regular system of local parameters. They are exactly ratios of degree-five sections xz^2, yz^2 to w, so the map has injective differential at P.

The morphism is injective on closed points: the x and y charts embed, a point with x nonzero cannot share its image with x zero, the corresponding statement holds for y, and P is the only point with both coordinates zero. Properness and quasi-finiteness give a finite morphism.

For completeness, the final finite-local-algebra step is sound. At a closed image point there is a unique point above it. If B is the target local ring and A is its finite source algebra, A is local with residue C. Cotangent surjectivity says n = mA+n^2. Applying Nakayama to n/mA gives n = mA. Then A/mA = C is generated by 1 over B/m; Nakayama applied to the finite B-module A/B gives A/B = 0. Thus B -> A is surjective. Checking at all closed image points suffices for this finite coherent cokernel, so the morphism is a closed immersion.

The weighted example therefore establishes a lower bound of five in a smooth boundary-free subclass and achieves five on this example. It does not supply a stable counterexample to 5I.

### 4.3 Smooth cyclic plane covers

The smooth branch divisor has positive degree and is irreducible, since distinct plane-curve components must intersect. The valuation along that divisor shows t^n-F defines an integral extension of degree n. The derivative argument verifies smoothness also on the branch. The cyclic algebra decomposition and ramification formula give K_X = pi^*O(a), a = (n-1)d-3 > 0.

If q = ma < d, every section is pulled back from the base, so the map factors through a degree-n cover and cannot be birational. If q >= d, the sections u_i^q have no common zero. On u_i nonzero, their ratios recover both base affine coordinates and t/u_i^d. They generate the full finite-cover algebra, so the map is a closed immersion on the inverse image of each corresponding target affine chart. These charts cover the image; the image is closed by properness. This proves a global closed immersion, not merely point separation or a dimension count.

The exact first birational and very ample exponent is therefore ceil(d/a). The bound four follows symbolically from 4a >= d in every admissible case: n=2 requires d>=4, n=3 requires d>=2, n=4 requires d>=2, and n>=5 allows d>=1. Equality of the ceiling with four occurs at n=2,d=4. The independent finite check covers 2<=n<=30 and 1<=d<=100 and finds 2,895 admissible cases, agreeing with the packet. The infinite-family argument is the symbolic inequality, not this scan.

## 5. Conductor and infinitesimal negative control

In R = C[x,y,z]/(xy), the conductor curve V(x,y) is reduced and one-dimensional. Sending (x,y,z) to (epsilon,-epsilon,0) defines a surjection to C[epsilon]/(epsilon^2), since xy maps to zero. Its kernel does not contain x or y, so this cluster is not contained in the conductor even though its support lies there. Both z and x+y vanish on the cluster, so the indicated linear system has only constants on it. The restriction to the conductor is nevertheless an embedding.

This correctly detects the difference between tangent vectors *along* T and all vectors supported on T. A local dual-number cluster already exhausts length-two nonreduced possibilities over C; an additional hidden embedded-point type is not being ignored. The example concerns an arbitrary local system, not 5L of an actual stable surface. It consequently diagnoses an invalid inference without pretending to provide the missing global counterexample.

## 6. Literature bounds and status

The packet accurately reports LR's full hypotheses: global generation at coefficient four, coefficient three when I>=2, very ampleness at coefficient eight generally, birational morphisms at coefficient six, and very ampleness at coefficient six for I>=2. LR Theorem 5.2(iii)'s degree-five conclusion requires the stated nodal conductor-plus-boundary condition, smoothness of the normalization along the conductor, and canonical singularities off the conductor. An arbitrary Gorenstein slc surface is not automatically covered.

Fujino's full Corollary 1.5, Remark 5.3, and Remark 7.3 were checked in the author-hosted PDF. They genuinely allow the more general boundary in the freeness assertion and give the recorded 12I/9I very-ampleness bounds, not a universal five theorem. The publisher independently confirms PRIMS 53 (2017), 349--370 and the DOI.

The full relevant FPR Propositions 3.6 and 3.7 give embeddings from degree five for K^2=1, positive-geometric-genus Gorenstein stable surfaces. Rollenske's stable Godeaux construction explicitly discusses the unsuccessful search for a degree-five counterexample and obtains degree-five embeddings in its family. The canonical-ring paper arXiv:1611.06810 was checked at record/abstract level only; it is not used as a theorem for unrestricted surfaces.

Independent targeted public searches on 2026-10-07 did not locate a later resolution of the unrestricted question. This is bounded evidence, not a proof of current openness. Publication listings were used as leads rather than as mathematical evidence. No stronger novelty or literature-exhaustiveness claim is warranted.

Primary public references:

- Original report and publication date: https://ems.press/journals/owr/articles/12490
- Liu--Rollenske full inspected version: https://arxiv.org/pdf/1211.1291v4 ; publication: https://doi.org/10.1016/j.aim.2014.03.009
- CFHR full inspected preprint: https://arxiv.org/pdf/alg-geom/9607021 ; published record: https://www.cambridge.org/core/journals/nagoya-mathematical-journal/article/embeddings-of-curves-and-surfaces/7FEAD216C2F054EFB04C655991150B60
- Fujino author PDF: https://www.math.kyoto-u.ac.jp/~fujino/Fujita-type4.pdf ; published record: https://ems.press/journals/prims/articles/14886
- FPR: https://arxiv.org/abs/1511.03238
- Rollenske's stable Godeaux family: https://arxiv.org/abs/1404.7027
- Franciosi--Rollenske canonical rings: https://arxiv.org/abs/1611.06810
- Wenfei Liu's publication listing: https://sites.google.com/site/liubenew/

## 7. Reproducibility, acceptance, and the remaining gap

The author program is a deterministic finite regression suite, not a geometric prover. Its four negative controls are meaningful in their limited role: index-one numerical extension, changing five to four, shifting the deck-generator weight, and replacing the cyclic maximum by three each cause a detectable false statement. The tangent check by itself tests a vector equation, so the ring-map justification was independently supplied above.

An independent checker was written without importing the author program's functions. It independently verifies all payload hashes, exact author-output agreement, all six supplied PDF hashes and byte counts, weighted monomial counts, integer-ceiling cyclic thresholds, the numerical exceptional pairs, and the dual-number relation. Source-byte verification is a comparison against the supplied local PDF bytes. Public web versions/records were independently inspected, but this audit does not claim a second byte-for-byte network retrieval of each PDF. The verification record states this limitation explicitly.

All five ledger entries correspond to substantive mathematical approaches, not elapsed-time bookkeeping. The central refinement is a correct application and optimization of published machinery; no priority claim is established. No mandatory correction patch is issued because there is no identified false claim to patch. The detailed local and subcurve arguments above can be incorporated as optional exposition without changing any conclusion.

Accepted partial conclusions are exactly:

1. The literal positive ordinary-canonical assertion for pairs fails on the smooth quartic pair on P^2.
2. The explicit smooth weighted surface needs exponent five for birationality and embeds in degree five.
3. The stated smooth cyclic-plane-cover family has the exact threshold ceil(d/((n-1)d-3)), at most four.
4. Every length-two scheme contained in T is separated by 5L, but support on T alone is insufficient for that argument.
5. For I>=2, every length-two scheme not separated by 3L is separated by 5L. Every scheme avoiding Bs|2L| is also separated by 5L. In particular, generation of 2L implies very ampleness of 5L.
6. The index-one sufficient numerical criterion leaves exactly (d,g)=(1,3),(2,5), subject also to the missing global-generation/curve-construction hypotheses.

The unresolved branch is precise: at I>=2, a possible degree-five failure must meet Bs|2L|, must already embed under 3L, and must not be scheme-theoretically contained in T. At I=1 further curve-existence and small-degree issues remain. Neither existence nor nonexistence of a global stable-log-surface degree-five counterexample is proved. The packet should stay **PARTIAL**, never SOLVED.
