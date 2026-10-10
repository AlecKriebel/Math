# Independent adversarial review: property-(s) elements of a skew brace

**Mathematical verdict: PASS_COMPLETE_COUNTEREXAMPLE.** The frozen construction answers the exact original ideal question negatively. No mathematical correction to the counterexample is required. The separately audited source-reconciliation note and the qualification below resolve the nearby-lemma scope issue and must accompany publication. Historical priority remains unestablished.

Reviewed `COUNTEREXAMPLE.md`: SHA256 `cb127cdc60740596a6e08bd0cb1cfb894b1d24ac8bc56a7338a885798b0a33ae`. This review used gpt-6-astra at xhigh. It is independent AI review, not human peer review.

## 1. Original scope and conventions

I read the full relevant contribution in OWR9/2023, printed pp.543–544, and visually checked the original p.543 facsimile. Question1 asks whether the property-(s) elements of an arbitrary skew brace form an ideal. The finite set X in the preceding Yang–Baxter discussion does not impose finiteness on the arbitrary B in this question; the associated structure groups can themselves be infinite. The subsequent periodic/property-(S) discussion concerns the following questions. There is no torsion-free, two-sided or particular structure-brace restriction on Question1.

The source uses star x*b=−x+x circle b−b and names its right fixed subgroup Fix^r(x)={b:x*b=0}; this is a subgroup of the additive group. Its left fixed subgroup is Fix^l(x)={b:b*x=0}, a subgroup of the circle group. The two relevant indices intersect these subgroups with the additive and multiplicative centralizers, respectively. The notation is easy to reverse; the submitted proof uses the source's convention correctly. Published Definition3.7 and its preceding discussion in Colazzo–Ferrara–Trombetti2025 confirm it.

An ideal must at least be an additive subgroup. Failure of additive closure therefore suffices, independently of the further lambda-invariance and normality requirements.

## 2. Independent verification of the infinite brace

Write c=u+2v and d=w+2z, with u,v,w,z binary. Then

    c diamond d = c+d+2cd mod4
                 = (u xor w)+2(v xor z).

Indeed, the carry2uw in u+w is canceled modulo4 by the additional2uw. Thus the finite circle quotient is C2 times C2. Both epsilon(c)=(−1)^v and (−1)^c=(−1)^u are characters of this group.

The proposed circle multiplication is consequently the semidirect product

    (n,c) circle (m,d)=(n+epsilon(c)m,c diamond d).

In the binary coordinates its group is D_infinity times C2. Associativity holds for arbitrary integer coordinates because epsilon is a character; the identity is (0,0) and the inverse is (−epsilon(c)n,c). This is an infinite-group proof, not an inference from reductions modulo a finite integer.

The additive group is Z times Z/4. Direct subtraction gives

    lambda_(n,c)(m,d)=(epsilon(c)m,(1+2c)d mod4).

Each is an additive automorphism, with both diagonal factors units. Therefore a circle (b+e) equals a circle b−a+a circle e. The two verified group structures and this identity are precisely the skew left brace axioms. Equivalently, the two character identities give lambda_(a circle b)=lambda_a lambda_b. There is no dependence on a recent semidirect-product theorem: the operations themselves prove the assertion.

## 3. Exact subgroup indices for the counterexample

The star product is

    (n,c)*(m,d)=((epsilon(c)−1)m,2cd mod4).

Take x=(0,1). Both x*(m,d) and (m,d)*x are (0,2d). Thus both fixed sets are H=Z times {0,2}. Addition is abelian, so its additive centralizer is all B. Also x is circle-central: epsilon(1)=1 and diamond is commutative. Therefore the centralizer intersections do not shrink H.

The additive quotient by H is C2. The circle quotient is also C2, because (m,d) maps to d mod2 by a surjective circle-group homomorphism whose kernel is H. Both required indices are exactly2.

Now y=x+x=(0,2). Its right star operation is

    y*(m,d)=(−2m,0).

Since m is an integer, Fix^r(y)={0} times Z/4. Its additive centralizer remains all B, and the quotient is exactly Z. This proves infinite index. In particular the additive cosets indexed by all integers m are pairwise distinct. As another independent diagnostic, conjugating y by (n,0) in the circle group gives (2n,2), an infinite family.

Thus x has property(s) and x+x does not. The set is not an additive subgroup, hence cannot be an ideal. This settles the exact question with no finite-generation or finite-truncation inference.

## 4. Full set and excluded positive theorem

For c=2 or3, the right fixed equation forces m=0, so the first index is infinite. For c=0 or1 it is finite. The circle centralizer condition for z=(n,c), g=(m,d) is

    (1−epsilon(c))m+(epsilon(d)−1)n=0.

For c in {0,1}, this combines with g*z=0 to give the four cases in the submitted table. The second subgroup is, respectively,

- B for z=(0,0)
- Z times {0,1} for c=0 and n nonzero
- Z times {0,2} for c=1 and n=0
- Z times {0} for c=1 and n nonzero

These are kernels of the appropriate finite quotient characters or of the projection to C2 times C2. Their circle indices are1,2,2,4. Hence the full property-(s) set is exactly Z times {0,1}. It is a normal circle subgroup but is neither additively closed nor lambda-invariant, since lambda_x(x)=(0,3).

The source's positive result assumes a two-sided brace of abelian type. Here the additive group is abelian, but right distributivity fails: with u=v=(0,1) and w=(1,0), the two sides are (−1,2) and (1,2). Thus that positive theorem does not apply. Both underlying groups are finitely generated; additive torsion is present, and the original question permits it.

## 5. Reconciliation with the nearby finite-generation lemma

The source audit uncovered a point that should not be hidden. Published Colazzo–Ferrara–Trombetti Lemma3.12, printedp178, has standalone wording asserting finite B/Ann(B) when the additive group is generated by finitely many property-(s) elements. The immediately preceding paragraph assumes the **whole brace** has property(S), but that hypothesis is not repeated in the lemma's displayed statement.

The present construction shows why the standalone weaker wording cannot be used here. Its additive generators r=(1,0) and x=(0,1) both have property(s). However,

    ker(lambda)=Z times {0},
    Ann(B)=ker(lambda) intersect Z(B,circle)={0}.

For every b=(n,0), all coordinates of the finite-data map displayed in Lemma3.12 are zero:

    b*r, b*x, r*b, x*b, [b,r]_+, [b,x]_+.

Thus that map has an infinite fibre here and is not injective under the weaker standalone hypotheses. Additive generators r,x only generate Z times {0,1} multiplicatively. They both have lambda maps fixing (n,0), whereas lambda_(0,2) negates it.

I also checked the cited Jespers–Kubat–Van Antwerpen–Vendramin Theorem5.4 in the full primary preprint arXiv2001.10967v1 (29 January2020); no final-journal comparison of that proof is claimed. Its converse assumes that the **entire** star-generated subgroup B^(2) and the additive commutator subgroup are finite. In this example,

    B^(2)=2Z times {0,2},

which is infinite: the star products yield (−2m,0) and (0,2), and every star product lies in that subgroup. Therefore the full theorem's finiteness hypothesis fails, and this review does not claim that theorem is contradicted. Its displayed inference from being fixed by lambda at additive generators to being fixed by every lambda is not a general identity. It cannot justify the weaker standalone lemma.

There is a further precision check: reduce the integer coordinate modulo3. This finite brace has global property(S), trivial annihilator, and the same additive generators r,x. The displayed map still sends all three elements (n,0) to zero. Thus global property(S) alone does not validate that particular injectivity argument. The full2021 theorem's conclusion is nevertheless true in this finite example, since its quotient is finite. No counterexample to that theorem's finiteness conclusion is asserted.

The frozen counterexample does not use Lemma3.12 or Theorem5.4. The direct operations and index calculations above remain decisive. The preceding whole-brace property(S) context is a possible intended restriction of the2025 lemma; this review does not assert authorial intent or a complete correction to its proof. Publication should include this precise qualification rather than silently treating all nearby source statements as applicable. The author has supplied `SOURCE_RECONCILIATION.md`, SHA256 `23527ada41ac8ce6769fc330286d96a1e3d554626b706b968b2dae0cd6adc177`. I read it in full and verified its equations and scope qualifications. It preserves the frozen counterexample and does not claim an intended repair or a counterexample to the full2021 theorem. The additional finite-quotient diagnostic above is part of this review.

## 6. Verification and literature limits

All **33,512** author assertions reproduce with a byte-identical receipt. The independent checker passes **9,562** exact controls. It verifies the group and brace identities as coefficient identities in three arbitrary integer variables, finite quotient characters, subgroup membership equations and exact finite quotient indices. It also checks the explicit infinite-family formulas, the annihilator calculation and the source-map diagnostic. The finite tests supplement the algebraic proofs of infinite index; finite quotients cannot prove that failure because all their indices are finite.

Reproduce with `python independent_checks.py` in this directory, and `cd author_replay && python verify.py` for the submitted receipt. The independent checker uses only the standard library.

The four-element brace and the semidirect-product construction are credited. The2026 papers are not dependencies of the direct proof. Their distinctions between finite lambda-orbits and property(s) are consistent with the calculated example. A bounded primary-source search did not establish priority or locate this exact prior example; absence from that search is not a novelty certificate.

Subject to preserving the source-reconciliation qualification, recommend **claimed_solved, 2/5 approaches** for the original ideal-closure question. No stronger torsion-free, finite-brace or two-sided counterexample is asserted.

## Primary references

- [Original OWR9/2023](https://ems.press/content/serial-article-files/47003), printedpp.543–544, Question1 and preceding definitions
- [Colazzo–Ferrara–Trombetti2025](https://mat.uab.es/pubmat/fitxers/download/FileType%3Apdf/FolderName%3Av69%281%29/FileName%3A6912508.pdf), Definition3.7, Example3.8, Proposition3.10 and Lemma3.12
- [Jespers–Kubat–Van Antwerpen–Vendramin](https://arxiv.org/abs/2001.10967), Theorem5.4; published Advances in Mathematics385 (2021),107767
- [Cascella–Properzi–Van Antwerpen postprint](https://arxiv.org/abs/2603.06177v2), scope/credit only
- [Di Matteo–Ferrara preprint](https://arxiv.org/abs/2607.20222v1), scope/credit only
