# Independent adversarial audit: KP-3.65

Date: 2026-10-03. Problem ID 2863; queue rank 531.

## Verdict

**PASS as a scoped, unsolved research packet documenting five approaches.** No blocking defect was found in the elementary deductions or in the way the cited theorem inputs are applied. This is not a solution of KP-3.65, a topological counterexample, a novelty certification, or a formal verification of the cited topology. The proposed disposition **unsolved, 5/5** is supported by the packet's actual contents.

The strongest checked conclusion is the following. Let Y be closed, connected and oriented, let R = Q[A,A^{-1}], let M be its skein module over R, and let T be the torsion submodule. If the generic rank r is finite and Y has d distinct SL(2,C) characters, then

    dim_{R/(Phi_{2N})}(T/Phi_{2N}T) >= max(0,d-r)

for every positive odd N. Thus rank one and Y not homeomorphic to S^3 force a nonzero torsion fiber at every such prime. No argument in the packet excludes this behavior for every other prime 3-manifold.

There is one minor terminology clarification: the word **nonspherical** in README.md and RESEARCH_LOG.md should mean **not homeomorphic to S^3** in this packet. In 3-manifold topology, spherical also describes nontrivial spherical space forms. The precise statements in PROOF.md use the correct condition and include those manifolds; the shorthand does not invalidate them. The original eight-file snapshot was preserved unchanged, and this clarification belongs to the review.

## Frozen object and reproducibility

The reviewed object consists of exactly PROOF.md, README.md, RESEARCH_LOG.md, SOURCE_GATE.md, STATUS.json, verify.py, verification.json, and SHA256SUMS.

- Author SHA256SUMS SHA-256: `4fd974d516f0ff406b75b0750ebc69dd9afadc8e8618739b9a668e8bd6b85949`
- Author PROOF.md SHA-256: `f5d739d6c7b6ca42619b89c2964a148955727d4c5c75496e5cf9c40fe01300a1`
- All seven entries in the author manifest passed before review; the eight hashes were checked again after the audit.
- Re-running the unchanged verify.py reproduced verification.json byte for byte: **860 assertions, PASS**.
- independent_controls.py recomputed the same 860 controls without importing or executing verify.py. It uses SymPy 1.14.0 polynomial arithmetic and gcd degrees in place of the author's polynomial implementation and matrix elimination. Every section count, sample result, and interpolation degree agrees.

The complete audit file list and its hashes are in this directory's SHA256SUMS. The independent checker needs SymPy; the original checker remains standard-library-only. Neither checker is a formal proof assistant.

## Source and hypothesis checks

The exact problem and all remarks on printed pp. 178-179 of the 2026 K3 list were checked in both text and page images. The original question uses generic rank over Q(A), with closedness, connectedness, orientation and primeness. It does not assume finite generation over a Laurent polynomial ring. The same pages retain the unrestricted question and distinguish the known conditional cases. [K3](https://bpb-us-e2.wpmucdn.com/websites.umass.edu/dist/b/22144/files/2026/04/K3-problem-list-watermarked.pdf#page=178)

The final DKS journal source labels the stronger rank-at-least-two question **Question 10.5**, on printed p. 43. Number 10.3 is a finite-generation conjecture. The packet correctly separates this from rank-one recognition, which by itself says nothing about rank zero. [DKS, final version](https://users.math.msu.edu/users/kalfagia/skein.pdf#page=43)

The proof-reading scope was DKS Sections 2 and 3 in full; Theorems 4.2-4.3 and their proofs; the evaluation-map and nonvanishing argument in Section 9; and the comparisons and questions in Section 10. The detailed readable proof copy was arXiv v3, with final-journal statements cross-checked. The root theorem's irreducible, central, and noncentral abelian branches were all inspected, including finite-character separation. [DKS v3](https://arxiv.org/abs/2305.16188v3)

Zentner's complete final Section 9 was read, including the degree-one reduction and its three cases. The imported recognition input is an SL(2,C) irreducible representation for every integral homology 3-sphere other than S^3; an unproved SU(2) replacement is unnecessary. [Zentner](https://zentner.app.uni-regensburg.de/splicing.pdf)

Kitaeff's Theorem 1.10 was checked through the basis argument in Section 2 and the even-q evaluation calculation in Section 3. The nonzero vector uses the imported dimension theorem, whereas cancellation uses the displayed evaluation formula. It is an obstruction to universal evaluation-map injectivity, not a rank-one manifold example. [Kitaeff](https://nyjm.albany.edu/j/2026/32-20p.pdf)

The geometric, gauge-theoretic, surface-skein and quantum-invariant foundations cited by these papers were not independently re-proved. A bounded fresh search found the exact K3 question and DKS question, but no unrestricted solution. That is not an exhaustive literature certification, and the catalogue access claim in SOURCE_GATE.md was not upgraded to a fresh successful catalogue verification.

## Adversarial algebra checks

### 1. Base change and the correct field

The skein presentation is a quotient of a free module on framed-link isotopy classes by the local relations. Tensoring that presentation changes coefficients, even with infinitely many generators or relations. No unproved finite presentation is required.

For p = Phi_{2N}(A), R/(p) is the cyclotomic number field obtained by sending A to a primitive root of order 2N. The element A remains invertible, so using Laurent polynomials creates no additional quotient issue. Tensoring first by R/(p), then by C through that embedding, gives the complex specialization. Field extension preserves vector-space dimension; a factor of the cyclotomic degree must not be inserted in the claimed inequality. The checker's rational matrix dimensions do contain that degree and are correctly converted to residue-field dimensions.

### 2. The exact sequence does not assume a splitting

For an arbitrary module over a domain, Q = M/T is torsion-free: if a(m+T) is zero for a nonzero a, some nonzero b kills am, so ba kills m. The author's proof of T intersect pM = pT is valid for exactly the same reason. Therefore

    0 -> T/pT -> M/pM -> Q/pQ -> 0

is exact without finite generation, a structure theorem, or a direct-sum decomposition. Equivalently, over the PID R the torsion-free quotient is flat, but invoking flatness is unnecessary. In particular, tensoring an arbitrary short exact sequence was not silently assumed to preserve injectivity.

### 3. Finite generic rank gives an inequality, not equality

Take r+1 lifts in Q of putatively independent residue classes. Since Q embeds into its localization, a cleared-denominator dependence is an actual relation in Q. Divide the coefficients by their largest common power of p. Such a power exists for a finite list of nonzero coefficients in a PID, and torsion-freeness permits the cancellation in Q. At least one remaining coefficient has nonzero residue, contradicting the chosen independence. Hence dim(Q/pQ) <= r.

This argument covers arbitrary non-finitely-generated Q and r = 0. It does not use Nakayama's lemma or require Q to be free. R[1/p] has rank one and zero p-fiber, so replacing the inequality by equality would be false. The packet explicitly avoids that mistake.

Exactness now implies the proposed torsion-fiber bound. For infinite character sets, applying the statement to every finite set is enough to obtain an infinite-dimensional fiber. No comparison with an uncountable cardinal of complex points is needed. Finite generic rank is an explicit hypothesis of the quantitative proposition; in the recognition application r = 1 supplies it directly.

### 4. Torsion fibers, primary length, and divisibility

The passage from a nonzero class in T/pT to a submodule R/(p) is sound. For a representative with annihilator (f), coprimality of f and p would force the class to vanish by Bezout. Write f = p^e g with e >= 1 and p not dividing g. Then p^{e-1}gt is nonzero because f/p does not belong to the exact annihilator ideal, and p kills it.

The converse is correctly rejected: R[1/p]/R has p-torsion while multiplication by p is surjective. A cyclic R/(p^e) contributes one dimension over R/(p), regardless of e. This is distinct from its primary length e.

The displayed specialization equation in the proof of DKS Theorem 3.1 uses the full primary-torsion dimension. In the abstract model R/(A+1)^e that quantity is e, whereas its residue fiber has dimension one. That displayed argument is not a general module identity. Crucially, the audited packet does not import it: its own exact sequence and fiber bound are independent of that step. This observation does not assert that the published theorem has a manifold counterexample. [DKS, Section 3](https://users.math.msu.edu/users/kalfagia/skein.pdf#page=13)

### 5. Conditions that really suffice

If one odd cyclotomic fiber vanishes, rank one bounds the number of characters by one. If the module contains no R/(p) submodule for one such p, its torsion fiber vanishes by the preceding implication. Finite generation of T is sufficient because a product of finitely many annihilators kills T; outside its finite prime support, Bezout makes multiplication by p invertible. Finite cyclotomic torsion support likewise supplies a missing prime.

None of these properties follows from generic rank one. The direct-sum examples E and E_infinite are genuine abstract module countercontrols: localization kills each torsion element, while precisely the relevant summands survive at a selected prime. Tensor product commutes with these direct sums. No manifold realization is claimed.

## Character recognition and topology checks

For nonzero finitely generated H_1, a nontrivial character into C* gives a diagonal SL(2,C) representation. Its trace differs from the trivial character at some element, including when the image is {1,-1}: the value -1 gives trace -2. Thus the finite 2-torsion cases are not missed.

When H_1 is zero, closedness and orientation give an integral homology sphere by duality. Zentner's theorem then supplies a second character unless Y is S^3. There is also an elementary way to check that an irreducible representation cannot have the trivial character: if every trace equals 2, a nonidentity matrix is nontrivial unipotent. Conjugate it to [[1,a],[0,1]] with a nonzero. For any other image matrix B, equality of the traces of B and its product with that unipotent matrix forces B's lower-left entry to be zero. Every image matrix preserves the same line, contradicting irreducibility.

This covers nontrivial spherical space forms as well as other closed oriented manifolds; it does not discard them by terminology. Primeness is not needed for this recognition lemma. No nonorientable extension of the quantum-topological input is claimed. All such statements should retain the closed, connected, oriented scope fixed in PROOF.md.

For finite abelian H, the inversion-orbit count is correct. A diagonal character is determined up to simultaneous inversion, not independent inversion of its values on separate generators. The author's comparison at g and gh proves precisely this point. The fixed-point count is |H[2]|. For positive first Betti number, a quotient onto Z gives arbitrarily many distinct diagonal characters. The proof does not infer generic nonvanishing of every mod-2 grading sector.

The only primitive-root restrictions used are positive odd N, with order exactly 2N. N = 1 is separately justified by evaluation at distinct points of the character ring. Nilpotents cannot obstruct that evaluation surjection. No even-N quantum theorem, prime-N restriction, or reducedness assumption is silently substituted.

## The two other routes remain conditional

For a rational homology sphere of generic rank one, the nonzero empty skein is a basis over Q(A). Each fixed skein is consequently one rational-function multiple of it. Applying the linear evaluation map gives equality outside a finite exceptional set that may depend on that skein. There is no division by a potentially zero quantum invariant and no claim of one common exceptional set for all links.

Chinese-remainder interpolation is valid only for compatible residues in the cyclotomic fields, as the packet states. It does not interpolate arbitrary unrelated complex values by rational polynomials. A finite sample therefore does not establish nonrationality at all orders. The 41 scalar-cancellation controls test the substitution in Kitaeff's formula; they do not prove that formula or the nonzero-skein assertion.

The Dehn-filling route retains the necessary corner-unit hypothesis and the exact exceptional slope sets. Invertibility over Q(A) cannot replace a unit over the coefficient ring. The conclusion is limited to the stated finite-generation families, and the exceptional slopes are not removed without argument. The conjectural Floer comparison is not used as a theorem to settle the general case.

## Final assessment

The five named approaches are substantive and related; they are not five independent proofs, and the packet says so. The numerical progress estimates are subjective commentary rather than mathematical evidence. The 860 controls strengthen reproducibility of the finite algebra but provide no computation of an arbitrary manifold's skein rank.

The unresolved implication is exactly the one advertised: no established argument in this packet forbids the all-orders cyclotomic torsion pattern for every prime manifold outside S^3 and S^1 x S^2. Retain **unsolved, 5/5**, the conditional qualifiers, and the distinction between an abstract module example and a topological counterexample. No remote changes were made during this audit.
