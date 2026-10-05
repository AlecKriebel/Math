# Independent adversarial audit: problem 30004996

## Verdict

**Pass as an unsolved five-approach research/obstruction report, with two minor source-map corrections. No full solution or counterexample is certified.**

The frozen mathematical arguments survive this audit. In particular, the centralizer/Baire-essential-image lemma proves the stated compact-free-subshift consequence when every nonidentity element has infinite centralizer. It does not provide a Borel map from the entire prescribed free shift into that compact subshift. The parity-factor example correctly prevents promotion of subsystem existence to universality.

The exact audited input is the eight-file packet bound by external `FREEZE_MANIFEST.json`, SHA-256 `b8a4f8d40b4428baec9bdad1d74c3ab8b33c98bf73013cc5dcb4e60d749d9b4d`. All eight byte counts and hashes match. The original 19,861 assertions replay exactly, including byte-identical standard output. An independently authored suite passes 135,653 additional finite controls. Neither suite proves an infinite Borel existence assertion.

The original files were not edited. `CORRECTIONS.json` and `source_map.corrected.md` provide a hash-bound correction overlay. A portable archive can contain only the frozen packet, its two external verification files, and this audit directory; scholarly PDFs, extracted source text, dataset records, and private coordination files must remain excluded.

## 1. Exact problem and source scope

The source is Anton Bernshteyn's contribution, *Constructing equivariant maps to free (and almost free) subshifts*, in [Oberwolfach Report 3/2022](https://ems.press/content/serial-article-files/46942), report pages 149–151. Definition 1 is on page 149, the sufficient theorem with continuous input on page 150, and Problem 2 on page 151. The audit independently inspected the text of these pages and freshly rendered and visually inspected report pages 149 and 151 from the supplied official PDF.

The packet correctly retains the countably infinite discrete group, finite alphabets, original SFT, and Borel requirements. Its conclusion concerns the closure of the entire coding image. An orbitwise statement is weaker. The distinction between pointwise freeness and faithfulness is maintained. The cases q=1 and finite groups are correctly separated; neither is used to misstate the source problem.

The relevant published sufficient theorem still requires a continuous equivariant input: [Bernshteyn, arXiv:2106.09673v3, Theorem 1.5 and Corollary 1.6](https://arxiv.org/pdf/2106.09673v3). A merely Borel coloring cannot be substituted, and an unrelated refinement of the domain topology does not establish continuity for this hypothesis.

## 2. Lemma 1 and the compactness controls

For fixed g, the disagreement cylinders U_d = {y : y(d) differs from y(dg)} are clopen. A free compact image closure is covered by them and admits a finite subcover. Conversely, if a finite union of these cylinders contains the coding image, that union is closed and contains its closure. This proves exactly the asserted uniform-witness equivalence, with no SFT assumption needed.

The single-marker example is valid. A binary Z configuration with precisely one 1 has no nonzero period; translating the marker outside any prescribed finite queried set makes all queried equalities hold. Its translates converge to the zero configuration. This only defeats keeping the original coding map and closing its image.

The dilation example also works. Every point of the chosen compact free binary subshift T contains a 1. In a phase of its n-dilation, all 1s lie in one residue class modulo n. A period must preserve that residue class, hence is divisible by n; sampling then gives a forbidden period of the original T point. The union of the n phases is compact and invariant. A phase can place an arbitrary central finite window entirely between permitted support sites when n is large. Thus the union over n has zero in its closure although each of its points has free orbit closure. This is a genuine orbitwise/global separation.

## 3. Detailed attack on the Baire-essential-image lemma

All category statements here are in the topology of M. It is essential that M is a nonempty compact metrizable space and that group elements act by homeomorphisms. No invariant probability measure is being assumed or used.

### Countability and nonemptiness

A finite-alphabet subshift S of a countable group is compact, metrizable, and zero-dimensional. Its relative cylinder sets form a countable clopen basis. Every clopen subset of S is compact and is a finite union of such basis elements. Consequently the family B of all clopen subsets is countable, as the proof needs.

Let N be the union of the clopen sets U whose preimages under psi are meager, and put K=S\N. Then psi^{-1}(N) is a countable union of meager sets. It cannot equal the nonempty Baire space M, so K is nonempty. K is closed in compact S, hence compact. This does not require that psi(M) itself be closed.

### Equivariance and invariance

For each group element a, equivariance gives psi^{-1}(aU)=a psi^{-1}(U). Translation preserves clopenness and meagerness. Hence N and K are invariant. In particular, psi^{-1}(K) is a Borel invariant comeager subset of M. This is all the argument presently says about which source points land in K.

### Local category and minimality

For fixed nonidentity g, the sets A_d are Borel because coordinate evaluation is continuous and psi is Borel. Pointwise freeness of psi(M) gives their countable cover of M. At least one is nonmeager; otherwise M would be meager in itself. The Baire property yields a nonempty open V with V\A_d meager in M. One may obtain this directly by taking an open set whose symmetric difference with A_d is meager, so no unjustified relative-to-global meagerness step is needed.

Minimality of C_Gamma(g) means every one of its orbits meets V. Thus its inverse translates of V cover M. Compactness supplies finitely many h_i in that centralizer covering M by h_i^{-1}V. The complement of the union of h_i^{-1}A_d is contained in the finite union of h_i^{-1}(V\A_d), and is therefore meager. The claimed comeagerness step is valid even though each A_d need only be comeager locally.

### Noncommutative orientation

For x in h_i^{-1}A_d, equivariance yields a disagreement at the two coordinates d h_i and d g h_i. The centralizer condition is used exactly to identify the latter with d h_i g. The right-coordinate convention is therefore correct. Replacing centralizer elements by arbitrary group elements would be invalid; the independent dihedral controls explicitly exhibit that failure.

The resulting finite union U_g of disagreement cylinders has comeager preimage. Its complement is clopen with meager preimage and was removed in the construction of K. Therefore K is contained in U_g and has no g-fixed point. Repeating this for each nonidentity g proves freeness of K.

**Finding:** no mathematical defect found in Lemma 2. Its topology, category, countability, and centralizer hypotheses are all doing legitimate work. The proof is valid for any finite-alphabet subshift, not only an SFT.

## 4. External input to the restricted corollary

The audit freshly read [Bernshteyn–Frisch, *Flows with minimal subdynamics*, arXiv:2509.03139v2](https://arxiv.org/pdf/2509.03139v2): Theorem 1.3 on page 2, Corollary 1.11 on page 3, and the relevant material in Section 8, pages 21–22. Its group is countably infinite and discrete. The simultaneous family must be countable and consist of infinite sets. The family of centralizers indexed by nonidentity elements meets both conditions under the packet's stated assumption.

Corollary 1.11 gives a free binary subshift with the required simultaneous minimality, so compact metrizability is available. One can simply include that binary subshift in Free(k^Gamma) and restrict the given coding map; this is a shorter route to psi. The packet instead invokes the free-shift mapping theorem, which is also legitimate. [Seward–Tucker-Drob, arXiv:1402.4184v1, Theorem 1.1, page 3](https://arxiv.org/pdf/1402.4184v1) applies to a free Borel action on a standard Borel space. A compact metrizable source qualifies. Coordinate inversion conjugates its left-coordinate convention to the convention in the packet.

The countable centralizer family does not require countably many arbitrary subgroups or any finite-generation assumption. Infinite abelian groups satisfy the condition. In a torsion-free group the cyclic group generated by each nonidentity element is infinite and lies in its centralizer. No conclusion is justified for unrestricted finite-centralizer cases by this corollary.

The manuscript is publicly listed as a preprint on the author's [current publication page](https://bahtoh-math.github.io/), and arXiv currently exposes v2 dated 13 September 2025. The audit verifies the relevant stated hypotheses, not an independent reconstruction of the full external theorem.

**Important:** a free compact K existing inside S is not a Borel-universal target. Nor does the comeager invariant set psi^{-1}(K) make psi land in K at every point, or produce an equivariant Borel retraction onto that set. This remains a full-target gap.

## 5. Parity obstruction: probability hypotheses checked

Take any nonempty compact free binary Z-subshift T and the two-point alternating subshift P. Their coordinatewise product K is a four-symbol compact invariant system. Its stabilizer at a pair is the intersection of the coordinate stabilizers, so K is free.

A hypothetical Borel equivariant map from Free(2^Z) into K would, after projecting onto P and evaluating coordinate zero, give a Borel bit a with a(sigma x)=1-a(x). Put A={x:a(x)=0}. The fair Bernoulli measure assigns measure one to the free part: for each nonzero period, its fixed configurations have measure zero, and there are countably many periods. Thus A can be treated as a measurable set in the full probability space. Shift invariance of the measure and the complementary-bit relation imply mu(A)=1/2. The square of the shift preserves A.

The Bernoulli shift squared is ergodic. More precisely it is mixing: even translates eventually separate the finite supports of any two cylinder events, yielding independence, and approximation of arbitrary measurable events by finite-coordinate events passes this limit to all measurable sets. An invariant measurable A must consequently have measure 0 or 1, contradicting 1/2. There is no category/measure substitution in this proof.

The example is an obstruction to a proposed inference, not a counterexample to Problem 2. In particular K is not claimed to be an SFT or to admit the original antecedent map. The packet correctly records both limitations.

## 6. Remaining approaches and edge cases

- **Continuity-set shortcut:** the invariant dense G_delta set of nonzero binary Z configurations with arbitrarily long zero blocks is indeed free. A nonzero periodic sequence cannot have unbounded zero runs. Each orbit closure contains zero, so this set has no nonempty compact invariant subset. It validly defeats the unrestricted compact-subset inference.
- **Independent decoration:** pairing the original q-coloring with a hyper-aperiodic binary coloring is Borel and yields a compact free image closure in S times a free compact binary subshift. The output alphabet has 2q symbols. Projection can restore periods; nothing compresses this construction back to q symbols while preserving S.
- **SFT exhaustion:** for finitely many group elements and finite witnesses, the windows are finite and the universal translate variable gives shift-invariant local constraints. These define nested SFTs. If every level is nonempty, compactness gives a nonempty intersection and the identity translates ensure freeness. Neither consistent witnesses nor a Borel map into that intersection follows from the antecedent.
- **Monotone SFT:** avoiding 10 leaves only the two constants and a single orbit of interfaces. Every interface orbit closure contains constants. An equivariant map from the source's conull free Bernoulli action into the interface orbit would partition a probability-one set into countably many disjoint translates of equal measure, which is impossible. Thus this candidate fails the antecedent. For any countably infinite group, the analogous probability obstruction excludes any countable union of infinite target orbits: all atoms on an infinite orbit must have equal mass and hence zero. Bernoulli measure is invariant without an amenability assumption.

## 7. Required minor corrections

1. In `source_map.md`, the reference to **Proposition 8.2** in the Bernshteyn–Frisch paper should be **Lemma 8.2**. The PDF and HTML agree on the label. The mathematical use is unchanged.
2. The phrase about an essential **closure bar in the definition** is visually inaccurate for the cited OWR definition. Page 149 expresses the requirement with the words **topological closure**. The corrected source map records fresh audit visual inspection of pages 149 and 151 and attributes the whole-image requirement to Definition 1 on page 149.

No proof correction, changed problem status, sixth research approach, or originality claim is required. The correction overlay is explicit and hash-bound; the frozen source map remains preserved.

## 8. Retrieval, provenance, and publication boundaries

The existing OWR PDF has 591,122 bytes and SHA-256 `da55fc521b2e1454a01838882d8d7eb5484ede9ed63cc92b0f79bc08a2a0865a`. The audit independently verified these bytes, PDF metadata, and page count (64), and rendered its pages afresh. The supplied history says the official report materialized during an earlier partially completed scholarly-download batch before an approval-review interruption. This audit reused those existing bytes. It does not claim that no download occurred or that the interrupted batch never created a file.

Fresh web reads retrieved the official OWR document, the three arXiv papers, and the author's publication page. Web screenshot requests failed with a tool/content-type limitation; visual OWR verification instead used the existing local PDF. The arXiv verification here is PDF-text/HTML inspection; no locally downloaded arXiv PDF or byte hash is claimed. A DOI request for the published Bernshteyn paper failed; its author-listed publication and readable arXiv theorem were used. No denied action was bypassed.

The canonical selected source-record hash was independently recomputed and matches the frozen metadata. The two full dataset hashes and sizes are retained as prior provenance, not represented as independently recomputed from full dataset files in this audit. Historical queue/state/PR-search claims are outside this mathematical audit and were not refreshed through remotes.

A targeted current search did not identify a full resolution. This is not exhaustive open-status certification. Public deliverables may contain the authored audit, finite scripts/results, corrected authored source map, public URLs, bibliographic facts, and verification metadata. They must not contain the source PDFs, extracted text, selected dataset records, screenshots of source pages, or private coordination material.
