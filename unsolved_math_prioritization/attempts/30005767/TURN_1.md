# Turn 1: a credited counterexample to the two-radical field

Problem 30005767 / OWR-14298158-012. Complete candidate, pending independent review. This is one substantive author turn. The enumeration below was published by Callan, Mansour and Shattuck in 2017; no novelty claim is made.

## 1. Exact target and counterexample

Brignall's contribution to Oberwolfach Report 6/2024, printed pp. 290–293, Question 5 on p. 292, asks whether every proper permutation subclass of the separables has its generating function in

\[
K=\mathbb Q(z,\sqrt{U},\sqrt{V}),\qquad
U=1-4z,\quad V=1-6z+5z^2=(1-z)(1-5z).
\]

A permutation class is a downset under classical pattern containment. Sep is exactly \(\operatorname{Av}(2413,3142)\). The generating function is the ordinary length series: one term per permutation of \([n]\), with no division by \(n!\) and no quotient by reversal, complementation or tree isomorphism.

Take
\[
\mathcal C=\operatorname{Av}(2341,2413,3142).
\]
This is a pattern-closed subclass of Sep. It is proper: \(2341=123\ominus1\) is separable and is excluded from \(\mathcal C\). Write
\(C(z)=\sum_{n\ge0}|\mathcal C_n|z^n\), including the unique empty permutation. We prove
\[
 C(z)=\frac{1-2z+2z^2-\sqrt{P(z)}}{2z(1-z+z^2)},\qquad
 P(z)=1-8z+20z^2-24z^3+16z^4-4z^5,                 \tag{1}
\]
where the formal square root has constant term 1. This exact formula is already Theorem 11 of Callan–Mansour–Shattuck [2]. We then prove \(C\notin K\). Excluding the empty permutation replaces \(C\) by \(C-1\), so the answer is unchanged. A rational index shift likewise cannot change membership in a field containing \(\mathbb Q(z)\).

## 2. Unique decompositions and the occurrence boundary lemma

For nonempty permutations \(\alpha\) of length \(a\) and \(\beta\) of length \(b\), \(\alpha\oplus\beta\) is the concatenation of \(\alpha\) and \(\beta+a\), while \(\alpha\ominus\beta\) concatenates \(\alpha+b\) and \(\beta\). Each separable permutation of length at least 2 is sum decomposable or skew decomposable, and never both. The equivalence between separability and recursive direct/skew construction is a standard source fact, explicitly stated in [1] and proved/cited as Proposition 1.2 of [3].

For clarity, the uniqueness needed here does not require unique binary parse trees. A sum cut is a position \(k\), \(0<k<n\), for which the first \(k\) values are \(\{1,\ldots,k\}\). Taking the *smallest* such cut gives the unique first sum-indecomposable component. Otherwise a smaller cut inside that component would also be a cut in the whole permutation. Its standardized remainder is unique. The skew version uses the first \(k\) values \(\{n-k+1,\ldots,n\}\) and the smallest skew cut. A permutation cannot have both a sum cut and a skew cut: their two nested nonempty proper initial segments would have to be nested value sets, but a proper bottom interval cannot contain a top interval containing \(n\), and a proper top interval cannot contain a bottom interval containing 1.

An occurrence of a pattern \(\gamma\) meeting both sides of a direct-sum boundary gives a proper sum cut of \(\gamma\): entries chosen on the left precede and are smaller than all entries chosen on the right. Conversely a specified proper cut decomposes such an occurrence into the corresponding patterns on the two sides. The same statement holds for skew sums with 'larger' in place of 'smaller'. This lemma concerns arbitrary subsequences, not consecutive occurrences.

The pattern 2341 has no proper sum cut. Its only proper skew cut is after its first three entries, giving \(123\ominus1\); the first one or two entries are not the largest one or two values. Consequently:

* In \(\alpha\oplus\beta\), an occurrence of 2341 must lie entirely in one factor. The class \(\mathcal C\) is sum closed because Sep is sum closed and avoidance of 2341 is preserved.
* In \(\alpha\ominus\beta\), with both factors nonempty and in Sep, a crossing occurrence of 2341 exists exactly when \(\alpha\) contains 123. Thus the sum avoids 2341 exactly when both factors avoid it and \(\alpha\) avoids 123. Avoidance of 123 in \(\alpha\) itself already implies avoidance of 2341.

These tests also handle an occurrence using three or more canonical components. At the unique first-component boundary it either crosses, and is governed by the lemma, or lies entirely in the remainder, whose membership in \(\mathcal C\) tests all of its internal boundaries. Nothing is assumed about occurrences meeting only two adjacent components.

## 3. The allowed first skew component

Let \(\mathcal L\) be the set of nonempty skew-indecomposable separable permutations avoiding 123, and \(L(z)\) its ordinary generating function. The singleton belongs to \(\mathcal L\). Any longer member must be sum decomposable. In its canonical decomposition into nonempty sum-indecomposable components, there must be exactly two components: choosing one entry from each of three components would give 123. Each of the two components must be decreasing, since an increasing pair in one and any entry in the other would give 123. Conversely the direct sum of two nonempty decreasing permutations is separable, avoids 123 (an increasing subsequence uses at most one entry from each block), and is skew indecomposable because it is sum decomposable. A decreasing permutation is itself sum indecomposable, including the singleton. Thus this description is unique and exact, including length 2:
\[
 L(z)=z+\left(\frac z{1-z}\right)^2
     =\frac{z(1-z+z^2)}{(1-z)^2}.                 \tag{2}
\]
In particular \(L_1=1\) and \(L_n=n-1\) for \(n\ge2\).

## 4. Unambiguous grammar and the series

Let \(F=C-1\) count nonempty members, and let \(S,M\) count their sum- and skew-decomposable members. These categories are disjoint and exhaustive with the singleton:
\[
 F=z+S+M.
\]
The unique first sum-indecomposable component is either the singleton or a member counted by \(M\). Sum closure and unique first-component decomposition therefore give
\[
 S=(z+M)F.
\]
The boundary lemma and the unique first skew-indecomposable component give the bijection
\[
 \mathcal C_{\mathrm{skew}}\longleftrightarrow
 \mathcal L\times(\mathcal C\setminus\{\emptyset\}),\quad
 (\alpha,\beta)\longmapsto\alpha\ominus\beta,
 \qquad M=LF.
\]
This is both necessary and sufficient: the left factor avoids 123 and hence 2341, the right factor avoids 2341, and the only possible crossing cut is excluded. Both are separable. Lengths add and the standardized factors determine the permutation uniquely, so ordinary multiplication, with no binomial coefficient, is correct.

Eliminating \(S,M\) gives
\[
 LF^2+(z+L-1)F+z=0.
\]
Substituting (2), multiplying by \((1-z)^2\), and setting \(C=1+F\) gives
\[
 A C^2-B C+D=0,\qquad
 A=z(1-z+z^2),\ B=1-2z+2z^2,\ D=(1-z)^2.       \tag{3}
\]
The discriminant is \(B^2-4AD=P\). At \(z=0\), equation (3) is \(-C+1=0\), with nonzero derivative in \(C\). Equivalently, the recurrence for \(F\), whose constant term is zero, determines each coefficient from earlier coefficients. Thus the formal solution is unique. The plus radical root has a pole at zero; the minus root in (1) has numerator \(2z+O(z^2)\) and gives \(C(0)=1\). Its first coefficients are
\[
1,1,2,6,21,77,290,1118,4398,17595,71385.
\]
Equation (1) agrees term for term with the published exact formula [2, Theorem 11, pp. 13–14]. That paper uses a different decomposition, by left-right maxima. Only this theorem is needed for credit; its other classification cases are not dependencies of the argument here.

## 5. Exact field exclusion, with no radical cancellation

Put \(E=\mathbb Q(z)\). The classes of \(U,V\) in \(E^\times/E^{\times2}\) are independent: \(U\) has a simple zero at \(1/4\), where \(V=-3/16\ne0\); \(V\) has a simple zero at 1. Thus \(U,V,UV\) are all nonsquares, and \(K/E\) is biquadratic with basis \(1,a,b,ab\), where \(a^2=U,b^2=V\), and independent sign-change automorphisms of \(a,b\).

**Square-root lemma.** If \(0\ne X\in K\) satisfies \(X^2\in E\), then \(X\) is an \(E\)-multiple of one of \(1,a,b,ab\). Indeed, for each sign change \(\sigma\), \((\sigma X)^2=X^2\), so the field property and characteristic zero give \(\sigma X=\pm X\). Expanding in the displayed basis, an eigenvector of both sign changes can have a nonzero coefficient in only one of their four distinct simultaneous eigenspaces. It follows that \(\sqrt{P}\in K\) only if one of \(P,P/U,P/V,P/(UV)\) is a square in \(E\).

Each alternative fails by an odd valuation:

1. \(\deg P=5\), so its valuation at infinity is \(-5\), odd. Every rational-function square has even valuation at every point, including infinity.
2. \(P(1/4)=-17/256\ne0\). Hence \(P/U\) has a simple pole at \(1/4\), as does \(P/(UV)\), because \(V(1/4)\ne0\).
3. \(P(1)=1\ne0\), so \(P/V\) has a simple pole at 1.

Therefore \(\sqrt P\notin K\). This is exclusion from the *actual specified* two-radical field, not merely proof of nonrationality. The same odd degree proves that (3) is irreducible as a quadratic over \(E\), since its discriminant \(P\) is nonsquare. The generated field is exactly
\[
 E(C)=E(\sqrt P),
\]
because (1) expresses \(C\) in that field and the identity
\[
 \sqrt P=B-2AC                                              \tag{4}
\]
expresses the radical in \(E(C)\). Here \(A\ne0\) as a rational function, and the radical coefficient in (1) is the nonzero function \(-1/(2A)\). Thus it cannot cancel. If \(C\in K\), (4) would put \(\sqrt P\) in \(K\), a contradiction.

## 6. Conclusion, credit and verification limits

The class \(\operatorname{Av}(2341,2413,3142)\) gives a negative answer to Question 5 exactly as printed, including both radicals. Its exact enumeration predates the question: Callan–Mansour–Shattuck (2017), Theorem 11. This packet reconstructs it by a direct/skew grammar and checks the field exclusion; it does not claim priority for either the enumeration or this consequence. The narrower one-radical question, rationality characterization and structural conjectures in the same report are distinct questions and are not being marked resolved here.

`verify_turn1.py` exhaustively checks permutations through length 8, the canonical component grammar and bounded converse constructions, plus exact formal and polynomial controls. Its finite tests corroborate, and do not replace, the all-length proofs in Sections 2–5. It uses only Python's standard library. The source PDFs are kept separately for audit and are not redistributed in this packet.

### Primary references

1. R. Brignall, Enumeration in subclasses of the separable permutations, and related questions, joint work with M. Bóna, C. Defant, M. Opler and V. Vatter, Oberwolfach Report 6/2024, pp. 290–293, Question 5 p. 292. [Official report](https://ems.press/content/serial-article-files/48646).
2. D. Callan, T. Mansour and M. Shattuck, *Wilf classification of triples of 4-letter patterns II*, Discrete Mathematics & Theoretical Computer Science 19:1 (2017), article 6, Theorem 11, pp. 13–14. [DOI](https://doi.org/10.23638/DMTCS-19-1-6); [primary PDF](https://dmtcs.episciences.org/3219/pdf).
3. M. H. Albert, M. D. Atkinson and V. Vatter, *Subclasses of the separable permutations*, Bull. London Math. Soc. 43 (2011), 859–870, Propositions 1.2 and 1.4 and the preceding definitions. [Author preprint](https://arxiv.org/abs/1007.1014v1); [DOI](https://doi.org/10.1112/blms/bdr022).
