# Independent review: 30001767, symmetric-subgroup centralizer blocks

**Verdict: PASS_SCOPED_P_GROUP_FIXED_ALGEBRA_THEOREM. No mandatory correction.**

The reviewed artifact is PARTIAL_RESULT.md, SHA-256
\[
\texttt{3006c576a208c7307cc578c407c9914a14d73fa840064b960eda5d51d78f61e3}.
\]
The all-\(n\), \(\ell=2\), characteristic-two result is valid. The unrestricted naturally embedded symmetric-subgroup conjecture remains unresolved by this attempt. Recommended campaign status: **unsolved, 2/5**. This is an independent AI mathematical audit, not human peer review or a priority certification.

## 1. Original question and current-source check

I inspected the full original Ellers contribution, joint with Murray, in [OWR 21/2011](https://ems.press/content/serial-article-files/46337), printed pp.1183–1184, and visually checked the displayed original page. The natural subgroup fixes every letter greater than \(\ell\); the sufficiently large modular-system convention is retained. The target concerns **primitive central idempotents**, rather than arbitrary primitive idempotents or equality of entire centers.

For ambient and subgroup block idempotents \(e,f\), their products lie in the centralizer and are central there. The products are orthogonal and sum to one. Thus the asserted equivalence with primitivity of each **nonzero** product is correct. The original already records \(n-\ell\le3\).

The [Fayers–Putignano author manuscript](https://webspace.maths.qmul.ac.uk/m.fayers/papers/ribbonblocks.pdf), carrying the Journal of Algebra 685 (2026), 271–312 publication notice, still states the full assertion as Conjecture 2.5 and translates it into nonzero central products in §2.8. Its abstract and Corollaries 3.10/3.22 concern the specified generalized ribbon/belt families. I checked those scopes, without auditing the complete new combinatorial proof or claiming a line-by-line comparison with the journal edition.

The [published Danz–Ellers–Murray paper](https://www.cambridge.org/core/services/aop-cambridge-core/content/view/18B69524BB77FC4B356AFE1A2471C310/S0013091512000077a.pdf/the-centralizer-of-a-subgroup-in-a-group-algebra.pdf) confirms the \(S_6/A_4\), characteristic-five counterexample and the normal-\(p\)-subgroup hypothesis of Proposition 3. Neither provides a counterexample for the source's natural symmetric subgroup. Its reported finite computations concern the stronger center assertion. The submitted qualifications and attributions are accurate; no exhaustive present-day literature or novelty certification is implied.

## 2. Universal fixed-algebra argument

The fixed-vector lemma is correct over every field of characteristic \(p\). A central element of order \(p\) has nilpotent operator \(z-I\), hence a nonzero kernel. Centrality makes that kernel stable, and the quotient action allows induction on the group order. No averaging or algebraic closure is needed.

For \(e\in Z(A^P)\) idempotent, its membership in \(A^P\) makes both Peirce spaces
\[
eA(1-e),\qquad (1-e)Ae
\]
\(P\)-stable. If either were nonzero, the fixed-vector lemma would supply a nonzero fixed vector in that space. That vector would belong to \(A^P\) and fail to commute with \(e\), contradicting centrality. Therefore both Peirce spaces vanish and \(ea=eae=ae\) for every \(a\in A\).

This proves exactly
\[
\operatorname{Idem}Z(A^P)=\operatorname{Idem}(Z(A)^P).
\]
The finite-dimensional decomposition into primitive central idempotents is valid over an arbitrary field. Automorphisms permute these idempotents, and minimal nonempty invariant subsets are precisely their \(P\)-orbits. The orbit-sum conclusion follows.

**No normality assumption is concealed in this proof.** Stability follows from the action fixing \(e\), and requires neither a normal subgroup of units nor a normal subgroup of an ambient finite group. The proof also does not imply equality of the full centers.

## 3. Application and limiting controls

For an inner action, every ambient central element is fixed, so the two algebras have the same central-idempotent set and hence the same blocks. Conjugation by an arbitrary \(p\)-subgroup of a finite group is an inner action, including nonnormal subgroups.

For \(P=S_2\) and \(p=2\), this applies to every \(kS_n\), \(n\ge2\). The subgroup algebra is \(k[t]/(t-1)^2\), which is local with only block idempotent \(1\). Every centralizer block is therefore \(e\cdot1\), exactly the required source form. The stronger arbitrary-field conclusion includes the source's sufficiently large residue fields. The observation that \(S_\ell\) is not a \(p\)-group for \(\ell\ge3\) is correct.

The characteristic-three control is also exact. For \(k\oplus\mathrm{sgn}\), the transposition acts by \(\operatorname{diag}(1,-1)\), and its fixed algebra in \(M_2(k)\) is diagonal. Its two primitive central idempotents are not ambient central. The off-diagonal Peirce module is nonzero with zero fixed space. The stated \(S_3\) class-sum identities verify that \(Z(kS_3)\) is local, so merely having a one-block acting group algebra does not rescue the proof.

This control is explicitly outside the source's prescribed group algebra and natural subgroup embedding. It is correctly used only to identify the failed extension step. The general problem still needs primitivity of nonzero \(efC\) for the non-\(p\)-group cases not already covered by credited results.

## 4. Reproduction and independent diagnostics

All **147** submitted assertions replayed, with a byte-identical verification receipt. The author checker must be run with its replay directory as the working directory, because it reads the sibling mathematical file relative to that directory:
\[
\texttt{cd author\_replay \&\& python verify.py}.
\]

The separately written standard-library checker passes **121** additional exact assertions. It checks:

- Matrix fixed algebras in characteristics two, three and five, including all central idempotents in the finite examples
- A nonabelian order-eight unipotent action on a nonsemisimple triangular algebra
- External actions that permute blocks and yield the predicted orbit sums
- The characteristic-three sign and class-sum controls
- A fresh odd-prime nonnormal subgroup \(C_3\le A_4\): fixed-algebra dimension six, center dimension six, and four central idempotents, exactly matching the ambient idempotent set
- A cautionary generator test: order-two unipotent generators in characteristic two can generate a group of order six with zero common fixed vectors, so the whole-group \(p\)-group hypothesis cannot be weakened to a condition on the generators alone

These are finite diagnostics. The all-group and all-\(n\) conclusions rest on the written fixed-vector and Peirce-space proof, whose complete logical steps were independently checked.

## 5. Publication disposition

The frozen artifact is suitable for one scoped partial-result PR with this report and its exact controls. Preserve **unsolved, 2/5**, all source qualifications, the central-versus-primitive distinction, and the absence of a historical-priority claim. There are no requested mathematical edits.

