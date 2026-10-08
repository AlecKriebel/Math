# Independent acceptance: objectwise DS kernels and the socle filtration

Date: 8 October 2026. Problem identifier: 30004018; queue rank: 1070.

## Decision and scope

**Accept the frozen v2 packet as a correct, explicitly incomplete mathematical audit and collection of diagnostic calculations. Do not accept it as a solution of the full conjecture. No mathematical correction to its stated conclusions is required.**

This review is separate from the original author self-check. It reconstructs each argument in the mathematical note, checks the cited primary-source scopes and indexing, independently implements the finite calculations, and tests the unmodified six-file packet under actual UID/EUID 1000. The original files and their original self-audit labels remain unchanged. This supplement supplies current independent acceptance without retrospectively relabeling the historical receipts.

The outstanding claim remains

\[
A_k\subseteq S_k(K),\qquad 2\le k\le\min(m,n),
\]

for the full integral BGG category O of gl(m|n). None of the accepted diagnostics supplies this inclusion. The lower inclusion is credited prior work; the first-layer equality is a consequence of credited prior theorems. The review makes no novelty, priority, or exhaustive current-openness claim.

The acceptance decision applies to MATHEMATICAL_AUDIT.md with SHA-256

`27572974eae9d9a1a5f65c3762ebbacaf8f8ad7cf53caf6e22646c6ff12247bc`

and the complete original packet pinned in `verify_frozen.py`. It does not apply automatically to a later edit. Source PDFs, extracted source text, images of sources, datasets, and private coordination material are absent from this publication-facing supplement.

## 1. Category, scalars, action, and quantifiers

Fix the base field C, g = gl(m|n), a Cartan h, and an even Borel b_0. Work with Z/2-graded g-modules and even morphisms. The category in the note consists of modules whose restriction to g_0 belongs to ordinary BGG category O, with integral h-weights. Thus its objects are finitely generated, h-semisimple, locally b_0-finite, have finite-dimensional weight spaces and finite length. They need not be finite-dimensional. HPS §4.1 defines precisely this category; GHSS §§9.3–9.5 uses the same convention. The category depends on the even Borel, not on a choice of odd positive roots.

The reduced Grothendieck group first imposes [ΠM] = −[M], and is then complexified. All spans and all socles in this audit are over C. The relevant socle is that of the resulting sl(∞)-module under the translation-functor action, not the socle of an individual gl(m|n)-module. Translation functors are exact and commute with the DS functor in the sense used in HPS Lemma 32 and Proposition 36.

The zero object causes no exception: its associated variety is empty, its class is zero, and it contributes nothing to a span. For a nonzero object, DS_0(M) = M, so the origin is in its associated variety. Thus “trivial associated variety” means no nonzero points, with the harmless zero-object convention understood.

For an odd square-zero algebra element x, rank means the rank of x on the natural (m|n)-dimensional representation. It is not the rank of its action on M. The set X_k contains every self-commuting element of this natural rank, including different odd-root orientations. A_k is the span of classes of objects satisfying DS_x(M)=0 for every x in that set. It is not the intersection of kernels of the induced class homomorphisms. In particular, a zero reduced Euler class does not mean that the associated cohomology object is zero.

Use S_0=0 and S_{j+1}/S_j=soc(K/S_j). The first layer S_1 is the socle. For k=0, A_0=0. When min(m,n)=0 the positive-index target is vacuous. No conclusion for higher ranks is obtained by changing these conventions.

### The parity-category bridge in the CS import

CS §2.2 first defines the full supercategory sO, then works in a consistent parity-selected Serre half O, with sO equivalent to O ⊕ O. Consequently its finite-projective-dimension theorem applies separately to the two parity-compatible summands of an object in the full category. Parity change preserves projectivity, finite projective dimension, and the vanishing of DS. The theorem therefore applies to the full graded category used by HPS and the audited note. Restricting further to integral blocks is legitimate: block projections are exact and preserve projectives, and an integral object has no nonintegral block summands. This supplies explicitly the category transfer implicit in the note's rank-one argument.

## 2. Source normalization and imported results

The following are imports, not new results or outputs of the executable checker.

1. HPS Theorem 24 identifies the socle with the span of projective classes and computes the successive sl(∞) socle layers. OWR Theorems 2 and 5 summarize the same information.
2. HPS Proposition 33 and its proof give preservation of category O and the convergent category-O cohomological spectral-sequence argument for an orthogonal sum of odd root vectors. Lemma 35 obtains equality after passing to reduced Grothendieck classes. It does not assert an objectwise isomorphism between total and iterated cohomology.
3. CS Theorem 5.1 supplies even-Borel representatives by sums of mutually orthogonal, linearly independent isotropic root vectors. The setup preceding the theorem gives B_0-invariance of associated varieties. For gl(m|n), the number of these disjoint root directions is the natural matrix rank.
4. CS Theorem 4.1 characterizes trivial associated variety by finite projective dimension for gl(m|n), with the bound 2ℓ(w_0). The theorem is not available with the same conclusion for arbitrary Lie superalgebras; the source explicitly discusses failures outside its scope.
5. CS Lemma 5.2(2) bounds the support rank of an O-object in a generalized-central-character block by the atypicality of that block. HPS §4.5 uses this statement and its socle-layer calculation for the known inclusion.

### The indexing discrepancy is real

The primary PDF of HPS v4, §3.1, starts its socle filtration at index 0 with the socle itself. Its Conjecture 45 and Proposition 46 nevertheless print a k+1 index while their associated-variety bound is rank at most k. Both the text and the displayed formulas on PDF pages 23–24 were checked, including visual inspection. The author-hosted alternative also retains the target with the same printed k+1 convention. This is not silently treated as an additional theorem with an extra socle layer.

OWR's printed page 3098 gives the layer quotient indexed as soc_{k+1}/soc_k with contraction number k, and page 3100 states its Conjecture 9 using exact-rank-k objectwise annihilation. Its first nonzero layer is therefore the socle in the normalization adopted here. The printed page 3100 was visually checked. The packet's S-notation avoids mixing the incompatible indices.

### Derivation of the normalized known inclusion

For clarity, the normalization can be justified from the layers, not merely from a typographical replacement. Let W_k be the sl(∞)-submodule generated by the weight spaces corresponding to blocks of atypicality at most k−1. In layer S_{r+1}/S_r, the constituent tensor simples in HPS Theorem 24 have contraction number r; their minimal weight atypicality is r. No such simple of contraction number r≥k has a weight of atypicality at most k−1. Exactness of weight-space decomposition therefore puts every generating weight of W_k inside S_k.

Conversely, in each constituent of S_{r+1}/S_r there is a nonzero weight vector of minimal atypicality r, and its sl(∞)-span generates that simple constituent. A weight vector can be lifted to S_{r+1} with the same weight. Induction through the layers, allowing a basis in each multiplicity space, shows that the weight spaces of atypicality at most k−1 generate all of S_k. Thus W_k=S_k.

Every object in any of the generating blocks has support rank at most k−1 by CS Lemma 5.2(2), so its class lies in A_k. A_k is an sl(∞)-submodule because translation functors commute with DS and preserve the defining vanishing condition. Hence S_k=W_k⊆A_k. This is the content of the credited HPS argument after normalization, not a solution of the opposite inclusion.

The finite-dimensional J-summand, its tensor filtration, and the class maps for a fixed root orientation are different constructions. HPS Proposition 42 concerns the tensor filtration of J; Proposition 43 concerns class kernels and Verma classes. Neither identifies A_k with a socle layer in full O.

## 3. Reconstructed first-layer and support arguments

Suppose M is killed objectwise by every rank-one DS functor. Represent any nonzero x by an even-Borel conjugate x_1+⋯+x_r with mutually orthogonal root vectors. Starting with x_1-cohomology, which is zero by assumption, the convergent category-O spectral sequence from HPS Proposition 33 has a zero page and therefore zero total cohomology. Equivalently, one may add the orthogonal root directions successively. B_0-invariance then gives DS_x(M)=0 for all nonzero x.

For M≠0, this says X_M={0}. The parity/category bridge above and CS Theorem 4.1 give a finite resolution by projectives inside the integral category. Its finite Euler sum expresses [M] as a linear combination of projective classes, hence as an element of S_1. Conversely, every projective has trivial associated variety by that theorem, so every projective class is in A_1. HPS identifies their span with S_1. Therefore A_1=S_1.

The same forward implication works for a rank-k partial sum: its cohomology is zero by hypothesis, and adjoining each of the remaining mutually orthogonal directions leaves zero total cohomology. The orbit statement then gives vanishing at every rank at least k. Thus exact-rank-k vanishing is equivalent here to support of rank below k, and A_k⊆A_{k+1} in the applicable range. This uses the imported category-O convergence and orbit statements, rather than a claim that every infinite-dimensional associated variety is closed.

The converse spectral-sequence implication is not used. Finite projective dimension follows from support restricted to the origin, not merely from absence of rank-k points for k≥2. Consequently the projective-resolution argument stops at k=1 exactly as the note states.

## 4. Independently reconstructed finite obstructions

### 4.1. Reduced class kernels are larger than the objectwise span

For gl(1|1), write e=E_12, f=E_21 and [e,f]=h_1+h_2. The natural square of ue+vf is uv times the identity; its nonzero self-commuting rank-one elements lie on precisely the e- and f-axes. Scaling a differential by a nonzero scalar leaves its kernel, image, and cohomology unchanged.

The two-dimensional module C_a has v even at weight (a,−a), w odd at weight (a−1,1−a), f(v)=w, and e=0. The h_1 and h_2 commutators with e,f and the odd anticommutator all satisfy the gl(1|1) relations. Its DS_e is the original 1|1-dimensional superspace; DS_f is zero. Both reduced classes in K(gl(0|0))=C vanish. The target here is superspaces and parity is retained through the relation [Π]=−1. “Ungraded class kernel” does not mean that parity signs are discarded.

For gl(1|1), the even algebra is the Cartan. Its category O consists of finite-dimensional Cartan-semisimple modules: a finite set of generators has a finite-dimensional Cartan span, and PBW leaves only finitely many odd monomials. The central-zero component has simples L_a and their parity shifts. Hence its reduced complexified group is R=C[t,t^{-1}], where [L_a]=t^a.

Inducing L_a from h gives the four-dimensional exterior module with basis 1,e,f,ef and relative h_1-weights 0,1,−1,0. Odd exterior multiplication supplies e and f, including the sign f(e)=−ef. The restriction category is semisimple, so the induction/restriction adjunction makes this module projective. Its radical is generated by the odd exterior generators and its top is L_a, so it is the projective cover P_a. These covers and their parity shifts exhaust projectives in the component. Their supercharacters are

\[
[P_a]=2t^a-t^{a+1}-t^{a-1}=-t^{a-1}(t-1)^2,
\qquad [C_a]=t^a-t^{a-1}.
\]

The first-layer result, or CS's zero finitistic-dimension bound for gl(1|1), therefore gives A_1∩R=(t−1)^2R. Both class maps on this component are evaluation at t=1, so their simultaneous kernel is (t−1)R. For a Laurent polynomial p, membership in the latter ideal is p(1)=0, whereas membership in the former additionally requires p′(1)=0. Multiplying by a Laurent unit reduces these statements to the ordinary polynomial factor theorem. Thus μ(p)=p′(1) is a well-defined separating functional; μ([C_a])=1, while μ([P_a])=0 for every integer a.

Central-eigenvalue decompositions are exact and projective-preserving direct-summand decompositions. Contributions from other central components therefore cannot cancel this obstruction. The calculation proves a strict containment of the original objectwise span in the simultaneous reduced-class kernel; it does not refute the original target.

### 4.2. Vanishing total DS does not force vanishing iterated DS

In the named basis a,b,c,d, use bidegrees (0,1),(1,1),(1,0),(2,0) and parity equal to their sum modulo 2. Define

\[
u(a)=b,\quad u(c)=d,\quad v(c)=b,
\]

with all other values zero. Taking u and v as the positive generators of separate gl(1|1) factors, the negative generators zero, and the two Cartan pairs (p,−p),(q,−q), gives a genuine integral weight representation of their direct sum. Each positive generator has the expected degree, the two other Cartans commute with it, and u²=v²=uv+vu=0. Finite dimension puts it in the Levi category O.

The natural representation of the Levi is a direct sum of two 1|1 spaces. There, u and v have natural rank one and u+v natural rank two. On the diagnostic four-dimensional module, u alone already acts with rank two. These are different ranks, and the independent check tests that distinction explicitly.

The total map sends a to b and c to b+d. The independent images b,b+d span b,d. Its kernel is also span(b,d); total cohomology is zero. For v, the cycles are span(a,b,d), the boundaries span(b), and the cohomology representatives are a,d. The induced u vanishes because u(a)=b is a v-boundary and u(d)=0. Iterated cohomology has dimension 1|1, not zero. At the next stage, the zigzag using v(c)=u(a)=b produces the nonzero higher differential a↦−d, up to the conventional spectral-sequence sign.

This exactly diagnoses the prohibited reversal of HPS Lemma 35's class-level argument. It is not an object of a constructed gl(2|2)-representation in the packet and is not tested against every rank-two element of gl(2|2). No such extension or counterexample is inferred.

## 5. The two restricted routes and their limits

### 5.1. External products of rank-one factors

The relevant factors are objects of the integral gl(1|1) category O, hence finite-dimensional. For an external product and a choice x_i∈{e_i,f_i}, the differential of the total complex uses the Koszul sign; over C, splitting each finite complex into its cohomology and contractible part proves the Künneth isomorphism. A tensor product of nonzero finite-dimensional superspaces is nonzero.

A projective factor has zero DS in both directions. Conversely, if a factor is not projective, it cannot vanish in both directions: CS Theorem 4.1 gives finite projective dimension and bound zero when the even Weyl group is trivial, so two-direction acyclicity would imply projectivity. Thus, if no factor is projective, choose independently for each factor a direction with nonzero DS; Künneth then gives nonzero total DS. Therefore all direction choices vanish exactly when at least one factor is projective. The zero factor causes no problem, as zero is projective. Finite direct sums satisfy the same test summand by summand because cohomology commutes with those sums.

In the all-central-zero component, every such class is a sum of Laurent multiples of a factor (t_i−1)^2. Conversely, tensoring P_a in one factor with one-dimensional modules in the others realizes every Laurent monomial multiple of each generator. Hence the span is precisely

\[
I=((t_1-1)^2,\ldots,(t_r-1)^2)\subset
C[t_1^{\pm1},\ldots,t_r^{\pm1}].
\]

The quotient is isomorphic to C[ε_1,…,ε_r]/(ε_i²) by t_i↦1+ε_i. The inverse is well-defined since 1+ε_i is invertible, with inverse 1−ε_i. Its basis consists of all square-free ε-monomials, so its dimension is 2^r. This is an all-r argument; merely counting binary vectors in a finite checker is not a proof of the ring isomorphism or independence.

This class of externally decomposable objects excludes arbitrary indecomposable Levi representations and general gl(m|n) category-O objects. No finite resolution or translation-generation statement for all rank-k-acyclic objects is established. Enlarging the conclusion to those objects would insert the missing argument by assumption.

### 5.2. Ordinary universal cohomology and specialization

In A=C[u,v]/(uv), every element has a unique expression as a constant plus a polynomial in positive powers of u plus a polynomial in positive powers of v. Multiplication by u annihilates exactly the positive-v part, because its other monomial images are distinct; multiplication by v behaves symmetrically. Therefore ann(u)=(v) and ann(v)=(u).

For d(a,b)=(ub,va), the kernel is (u)⊕(v), as is the image. The ordinary cohomology module is zero. Specializing the differential to u=v=0 instead gives the zero differential on C^{1|1}, whose cohomology is C^{1|1}. Thus specialization of this ordinary cohomology module cannot recover every fiber DS. This is the algebra in GHSS v2 Example 11.4, whose example and scope were checked.

The discrepancy occurs at the origin. The calculation does not disprove a punctured-cone statement, and it does not show that any particular derived or support-theoretic replacement solves the full problem. General O-objects may be infinite-dimensional, so a finite-rank coherent-bundle assumption also requires a new justification. These are precisely the limitations retained by the frozen note.

## 6. Reproducibility and adversarial checks

The complete commands, stdout, stderr, return codes, before/after hashes, file modes, and read-only probe results are in `INDEPENDENT_VERIFICATION.json`.

- Actual UID and effective UID were both 1000. The original directory was mode 0555, with all six files mode 0444.
- The attempted creation of a new file and the attempt to open the original note for append each failed with errno 13, Permission denied. No bytes were appended. Original file bytes, names, sizes, hashes, and modes were unchanged after all checks.
- The original checker completed in normal, −O, and −OO modes, reporting 678 guard evaluations each time. That number includes its expected negative-control guard evaluations; it is not 678 independent mathematical theorems.
- The new checker does not import or call the original checker. It constructs the projective by exterior multiplication, checks both Cartan operators and all relevant Lie-superalgebra relations, uses a separate fraction-free Bareiss determinant implementation for rank, checks cohomology in both parities, and verifies the named quotient representatives. It reports 3,885 guard evaluations in each of the same three modes, including arithmetic-oracle guards.
- Eight independent mutations were rejected with process return code 1 in every mode: exterior sign, Cartan weight, parity, replacing zero reduced class by a zero-object assertion, erasing the moment separation, dropping a total-complex arrow, confusing natural rank with module-action rank, and dropping the tensor Koszul sign. These are 24 explicit negative-process runs.
- The original packet is pinned externally by literal byte counts and SHA-256 values for all six files, including its own manifest. Five integrity attacks were rejected in all three modes: altered note, altered note with correspondingly regenerated internal manifest, missing file, extra file, and same-content symlink substitution. These are 15 explicit integrity-negative runs. Only disposable copies of authored files were mutated.
- The seven locally available source PDFs were independently rehashed and matched their recorded sizes and hashes. This establishes byte identity with the pinned local inputs, not a cryptographic attestation by their publishers. No fresh PDF download is claimed by this hash receipt. Public source pages were separately opened to verify current identifiers, versions, and scope.

The positive finite calculations and negative controls do not mechanically prove CS/HPS, quantify over all integers by enumeration, or solve the full conjecture. The all-parameter conclusions above come from the written algebraic arguments. The tests are source-free, use the Python standard library, do not use removable Python assertions, and require no network connection.

For a rerun, invoke `python3 -B run_acceptance.py ORIGINAL_PACKET OUTPUT_JSON SOURCE_PDF_DIRECTORY`; omit the last argument to run without the local source bytes. OUTPUT_JSON must be outside ORIGINAL_PACKET. The six-file original packet must retain its read-only modes and exact pinned contents. The runner expects actual UID/EUID 1000; it does not impersonate or simulate that UID.

## 7. Version checks and final disposition

The primary pages were checked on 8 October 2026. HPS is still identified by arXiv v4 dated 21 August 2018 and its JLMS DOI. CS's arXiv record identifies v4 and its Transactions AMS publication. GHSS's v2 record identifies the 13 July 2023 version and states acceptance to the Journal of the Indian Institute of Science. These metadata do not turn the finite-dimensional or class-kernel statements into the full target.

Hirota's arXiv:2603.01390v1 is the March 2026 manuscript titled “Duflo-Serganova functors and Brundan-Goodwin's parabolic inductions.” Its Example 4.6 agrees with the rank-one DS behavior used for comparison. The current public record is v5, dated 14 August 2026, titled “Some closed formulas for super Kazhdan-Lusztig polynomials.” The locally pinned v5 PDF has its own internal 17 August date. These are distinct version scopes. The v5 abstract, introduction, theorem scopes, DS section, and target-related terminology support no claim in this review that it resolves A_k=S_k in full O. Statements about socles of particular supermodules must not be identified with the sl(∞) socle filtration of the entire Grothendieck module.

A short source-validation search for the named conjecture and the DS/socle/category-O combination identified no full-resolution source. This supports only the bounded statement that no resolution was identified in the checked sources. It is not a comprehensive bibliography or a certificate of global openness.

**Final disposition:** preserve the original mathematical note; attach this independent acceptance supplement and its complete verification receipts. Retain the full-conjecture status as unresolved, with the exact remaining direction A_k⊆S_k for k≥2. No sixth attempt at proving the remaining conjecture is supplied by this audit.

## Primary references

- V. Serganova, joint with C. Hoyt and I. Penkov, “Representations of sl(∞) arising from categorical action,” OWR 52/2018, printed pp. 3098–3100. [Published report](https://ems.press/content/serial-article-files/46773).
- C. Hoyt, I. Penkov, V. Serganova, “Integrable sl(∞)-modules and Category O for gl(m|n).” [Pinned arXiv v4](https://arxiv.org/abs/1712.00664v4); [JLMS DOI](https://doi.org/10.1112/jlms.12176); [author-hosted alternative](https://math.constructor.university/penkov/papers/newcategory_v5.pdf).
- K. Coulembier, V. Serganova, “Homological invariants in category O for the general linear superalgebra.” [arXiv record](https://arxiv.org/abs/1501.01145); [institutional manuscript](https://backoffice.biblio.ugent.be/download/8550956/8550957); [published DOI](https://doi.org/10.1090/tran/6891).
- M. Gorelik, C. Hoyt, V. Serganova, A. Sherman, “The Duflo–Serganova functor, vingt ans après.” [Pinned arXiv v2](https://arxiv.org/abs/2203.00529v2); [published DOI](https://doi.org/10.1007/s41745-022-00334-9).
- S. Hirota, [arXiv:2603.01390v1](https://arxiv.org/abs/2603.01390v1) and [arXiv:2603.01390v5](https://arxiv.org/abs/2603.01390v5), with the distinct titles and scopes recorded above.
