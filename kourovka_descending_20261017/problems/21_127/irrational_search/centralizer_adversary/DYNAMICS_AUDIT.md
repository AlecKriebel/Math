# Independent adversarial review: irrational rotation diagnostic

Completed 2026-10-24T20:45:23.388961+00:00. Estimated completion: **100% of this diagnostic review**; no resolution of Kourovka 21.127. AI review, not independent human peer review. No originality assertion.

## Verdict

**PASS**, with the explicit composition/commutator convention recommended below. The construction produces an irrational value of a homogeneous quasimorphism on an explicit word of the free RAAG F2 while that word's stable commutator length is exactly rational. It rigorously falsifies the inference “irrational rotation value implies irrational scl.” It neither proves all RAAG scl rational nor gives an irrational RAAG scl example.

## Exact checks and attempted falsification

1. **Homeomorphism and exact fixed-point ordering.** Let alpha=sqrt(2)/100. Both lifts are strictly increasing since their derivatives are at least 1-pi/5>0 (pi<22/7 gives the positive lower bound 13/35). They commute with unit translation and are onto, since their difference from the identity is bounded. The g-fixed points alternate between repelling integers and attracting half-integers. For beta=arcsin(sqrt(2)/10) in (0,pi/2), the two h-fixed points modulo one are exactly

       u = 1/2 + beta/(2pi),   v = 1 - beta/(2pi).

   These satisfy 1/2<u<3/4<v<1. The derivative at u lies in (0,1) and at v exceeds one. The displacement h(x)-x is negative on (u,v) and positive on (v,u+1). In particular the apparently unusual map n+1/2 -> u+n+1 is correct: v+n < u+n+1 < v+n+1. Using u+n instead would reverse the fixed-point ordering and break the proposed increasing conjugacy.

2. **Conjugacy gluing.** The intervals (n,n+1/2) and (n+1/2,n+1) map respectively to (v+n,u+n+1) and (u+n+1,v+n+1). On the first pair the homeomorphisms move all interior points right; on the second they move them left. For right-moving interval maps, choose x,y and an increasing homeomorphism F0:[x,g(x)] -> [y,h(y)] taking endpoints to endpoints. For x<=t<=g(x), define f(g^k(t))=h^k(F0(t)) for every integer k. Definitions agree on shared endpoints. The iterates of x under g approach the endpoints, since any finite interior limit would be a fixed point; likewise for h. The glued map therefore extends continuously to both endpoints and is onto and increasing. Apply the construction to inverses on the left-moving pair. Repeating by unit translation makes f(x+1)=f(x)+1. This proves f g f^{-1}=h globally, including at all fixed points. No smoothness of f is asserted or needed. If a unique concrete choice is desired, take the midpoints x,y of each of the two representative intervals and the affine F0; existence alone suffices for the claim.

3. **Commutator convention.** With ordinary function composition and [x,y]=xyx^{-1}y^{-1}, the exact identity is

       [f,g] = f g f^{-1} g^{-1} = h g^{-1} = R_alpha.

   Indeed h(x)=g(x)+alpha, so h(g^{-1}(x))=x+alpha. The cited Fournier-Facio--Lodha source instead writes [x,y]=x^{-1}y^{-1}xy, with right actions. The draft should declare its convention explicitly. Under the inverse-first convention the displayed word is conjugate to the first commutator: (fg)^{-1}[f,g](fg)=f^{-1}g^{-1}fg. Its translation number is still alpha and its scl is still 1/2, but it need not literally equal the rigid translation. This is a presentation qualification, not a defect in the example.

4. **Quasimorphism and defect.** A homomorphism rho from the abstract free group sending a->f,b->g exists by the free universal property; injectivity is not claimed or required. Translation number on the period-one lift group is homogeneous, conjugacy invariant, and has defect at most one. Thus phi=rot o rho is a homogeneous quasimorphism on F2 with phi([a,b])=alpha and defect d<=1. Its defect is positive, since a homomorphism vanishes on commutators. More precisely the homogeneous commutator defect inequality yields alpha<=d. Bavard gives

       scl_F2([a,b]) >= alpha/(2d) >= alpha/2.

   Replacing the actual d by the universal upper bound one weakens the bound legitimately. No equality, irrationality of the ratio alpha/d, or extremality follows. Even d=alpha would be consistent with the rational exact scl value. The diagnostic therefore tests exactly the intended false implication.

5. **Covering upper bound, all odd n.** For left-composed permutations a(i)=i+1 and b(i)=-i on Z/n, b^{-1}=b and a b a^{-1} b^{-1}(i)=i+2. For odd n this is a single n-cycle. The action is transitive because a alone is transitive. The classification of covers of the once-punctured torus then gives a connected oriented n-sheet cover with one boundary component. The boundary wraps n times around the base boundary, and its Euler characteristic is n(-1)=-n. If its genus is g, 2-2g-1=-n, so g=(n+1)/2. Its boundary expresses a conjugate or inverse of [a,b]^n as a product of g commutators in F2. Hence cl([a,b]^n)<= (n+1)/2 for all odd n. Subadditivity gives existence of the scl limit, so this odd subsequence proves the upper bound 1/2. Nonnormality of the cover and the order-two monodromy b cause no issue.

6. **Exact lower bound and source scope.** The free-group estimate of Duncan--Howie says that a nontrivial kth power which is a product of g commutators has k<=2g-1. Applying it to the reduced nontrivial word w=[a,b] and all positive powers gives cl(w^n)>=(n+1)/2, hence scl(w)>=1/2. Together with the preceding upper bound this gives equality. I checked a primary later proof, Louder--Wilton, *Negative immersions for one-relator groups*, accepted manuscript dated 7 May 2021, section 5.3, Corollary 5.8 and proof, printed pp.30–31. That corollary proves the stronger inequality rank(<a_i,b_i,w>)+k-1<=2g; the generated subgroup is nonabelian here, since an abelian subgroup generated by the factors would give a trivial product of commutators. Thus its rank is at least two and the claimed estimate follows. The original 1991 article's metadata were checked (Mathematische Zeitschrift 208,225–237, DOI 10.1007/BF02571522); its original proof was not retrieved and is not claimed reproduced. The accepted later primary proof is cached with its hash.

## Dependencies and exact remaining gap

External facts retained: the standard classification of finite covers, the homogeneous translation-number defect theorem, Bavard duality, and the free-group power/genus theorem. The translation-number defect theorem and Bavard duality are also stated in the independently downloaded primary Zhuang paper (section 2 and appendix). All construction-specific deductions and the permutation identity have been checked above.

The example establishes a strict logical barrier: an irrational rotation quasimorphism value can occur on a RAAG commutator with rational scl. No conclusion about the complete RAAG scl spectrum follows. The missing research mechanism is an exact extremal computation, or some other proof determining a genuinely irrational scl value or proving universal rationality.

## Primary sources checked

- Zhuang, arXiv:0710.0026v1, section 2 and appendix: https://arxiv.org/pdf/0710.0026v1 .
- Louder--Wilton accepted primary manuscript, Corollary 5.8 and proof: https://api.repository.cam.ac.uk/server/api/core/bitstreams/33dc7366-5a5c-49ee-98a0-a1a18fa8ddb0/content . Published Duke Math. J.171(3)(2022),547–594, DOI https://doi.org/10.1215/00127094-2021-0024 .
- Original Duncan--Howie bibliographic record: https://researchportal.hw.ac.uk/en/publications/the-genus-problem-for-one-relator-products-of-locally-indicable-g/ .

Source-manifest hashes freeze all downloaded PDFs. This report is confined to the assigned diagnostic and does not assert new literature priority.
