# Canonical tightening of wavelet frames: scope and status audit

Audit date: 2026-10-14 UTC. Target: OWR-720-011, dataset ID 30000043, queue row 1781. This is a source-clarification pass, not a new proof or counterexample attempt.

## Outcome

The source asks a genuine question about the **canonical normalized tight frame**, not the canonical dual. The standard, defensible operational reading is preservation of the **same affine dilation/translation system, with the same generator count and natural indexing**. A more permissive reindexing or change-of-lattice question is different and must not silently replace it.

No primary source inspected in this bounded pass supplies an explicit classical counterexample or a general affirmative theorem answering the full question. This is a statement about the checked evidence, not a certification that the question remains open in 2026. The original source records it as unknown in 2004. A 2011 paper gives an exact conditional formulation and uses stronger introductory language, but its inspected theorem does not itself display a classical counterexample.

## Source identity and convention

Michael Frank, “Approximation of Frames by Normalized Tight Ones,” in *Mini-Workshop: Wavelets and Frames*, Oberwolfach Reports 1 (2004), report 10, DOI [10.4171/OWR/2004/10](https://doi.org/10.4171/OWR/2004/10). Relevant printed pages: **529–531**, especially the paragraph immediately preceding Theorem 5 on p.531. Primary report: [MFO PDF](https://publications.mfo.de/bitstream/handle/mfo/2828/OWR_2004_10.pdf?isAllowed=y&sequence=1).

Frank defines his operator S on p.529 as (θ*θ)^−1. Consequently his family {S^(1/2)x_i} is the usual canonical tightening {F^(−1/2)x_i}, where F=θ*θ is the modern synthesis–analysis frame operator. Reading Frank’s S as F would reverse the meaning.

The surrounding discussion fixes a unitary system U and its complete frame vectors. Theorem 5 uses one generator φ and affine atoms |det M|^(m/2)φ(M^m x−k), m∈Z and k∈Z^d. It states the positive semi-orthogonal case, citing Deguang Han’s 2003 paper. The short question does not separately enumerate every permitted dilation matrix, distinguish all frame-for-subspace variants, or expressly quantify over multiwavelets. Those are limits of the recovered wording, not licenses to add assumptions.

## Proposed acceptance contract

### Core classical, single-generator contract

Fix an admissible classical affine setting on H=L²(R^d), with unitary dilation D_M f(x)=|det M|^(1/2)f(Mx), translations T_k f(x)=f(x−k), and j∈Z, k∈Z^d. The dilation class must be stated explicitly. At minimum, the source question includes the usual one-dimensional dyadic setting M=2.

Let φ∈H generate a frame x_(j,k)=D_M^j T_kφ for all of H, with 0<A≤B<∞. Define

Ff = Σ_(j,k)〈f,x_(j,k)〉x_(j,k),

y_(j,k) = F^(−1/2)x_(j,k).

The proposition to test is:

For every such φ, there exists ψ∈H such that y_(j,k)=D_M^j T_kψ for every j,k, using the original dilation, translation lattice, and indexing.

Since (j,k)=(0,0) is included, the candidate is forced: ψ=F^(−1/2)φ. Thus acceptance requires precisely

F^(−1/2)D_M^jT_kφ = D_M^jT_kF^(−1/2)φ for all j,k.

This is local commutation on the generating orbit; it does not require claiming global commutation of F with every translation. Dilation covariance alone does not establish translation covariance.

### What establishes an answer

- **Negative answer:** Give an admissible single-generator frame, prove its frame bounds or bounded positive invertibility of F, and rigorously show failure of the displayed indexed identity for some j,k. A one-dimensional dyadic example is enough to refute an assertion covering every classical wavelet frame. Numerical truncation alone is insufficient.
- **Positive answer:** Prove the identity for every frame under the explicitly stated dilation/lattice/Hilbert-space hypotheses. An affirmative result only for tight, semi-orthogonal, diagonal-frame-operator, MRA-based, painless, or other restricted classes is a partial result unless the source’s full scope has first been proved to be that class.
- **Literature resolution:** An existing theorem or counterexample must use F^(−1/2), or supply a rigorous explicit implication to it, and must match these hypotheses and quantifiers. Supply its exact version, theorem/page, and public primary-source URL. Do not classify the row as solved merely from a similarly titled paper or its abstract.

### Separately labeled variants

1. **Finite multiwavelets.** For generators φ_1,…,φ_L, retain L, M, the lattice, and all indices. The output generators, if indexed equality holds, are forced to be F^(−1/2)φ_l. The original local setup explicitly supplies the single-generator case; do not silently turn a result proved only for L>1 into a single-generator counterexample.
2. **Changed generators or lattice.** Allowing more generators, a sparser/finer translation lattice, another dilation, arbitrary permutation, or merely setwise equality changes the contract. Under the fixed-index contract there is no freedom to pick a different ψ. A proof that another unrelated tight wavelet frame exists says nothing about the given canonical tight family.
3. **Affine versus quasi-affine.** The target family is the affine D_M^jT_k orbit. Quasi-affine constructions resample/renormalize scales and have their own frame operator. Equivalences of frame bounds or duality do not by themselves identify the two canonical tightenings.
4. **Canonical dual.** F^(−1)x_(j,k) is not F^(−1/2)x_(j,k). Failure of canonical-dual structure, absence of any affine dual, and a sufficient condition for dual structure are not standalone answers to this row. A claimed transfer requires a proof.
5. **Other ambient spaces.** Abstract Baumslag–Solitar representations, direct sums, continuous wavelets, finite filterbanks, and frames only for proper subspaces must be identified as separate scopes unless an explicit bridge establishes the classical contract.

## Checked primary results and their limits

### Conditional canonical-Parseval formulation: Bownik–Jasper–Speegle (2011)

M. Bownik, J. Jasper, D. Speegle, *Orthonormal dilations of non-tight frames*, Proceedings of the AMS 139 (2011), 3247–3256, DOI [10.1090/S0002-9939-2011-10887-6](https://doi.org/10.1090/S0002-9939-2011-10887-6). [Author-hosted published PDF](https://pages.uoregon.edu/mbownik/papers/44.pdf); [arXiv:1004.3552v1](https://arxiv.org/abs/1004.3552v1), submitted 2010-04-20; arXiv lists only v1 and gives the journal reference.

Theorem 4.1 and Remark 4.1, printed p.3255, formulate the relevant property exactly as F^(−1/2) belonging to the local commutant at ψ. Their equation (4.3) is the indexed orbit identity above. The result characterizes when a particular orthonormal dilation construction exists in an abstract BS(1,2) representation. Its introductory discussion on pp.3248 and 3254 says the admissible class is a proper subset / excludes arbitrary non-tight frames, but the inspected paper presents no explicit classical L²(R) counterexample proving failure of canonical tightening. Retain this as important status evidence and a precise scope reference; do not report a verified full resolution from Theorem 4.1 alone. Also observe that the paper’s convention for abstract D is DTD^−1=T²; this must be aligned explicitly with any physical dilation convention.

### Canonical-dual counterexamples and corrected proof: Bownik–Lemvig (2007)

M. Bownik, J. Lemvig, *The canonical and alternate duals of a wavelet frame*, Applied and Computational Harmonic Analysis 23 (2007), 263–272, DOI [10.1016/j.acha.2007.04.004](https://doi.org/10.1016/j.acha.2007.04.004). [Author-hosted published PDF](https://pages.uoregon.edu/mbownik/papers/29.pdf), available online 2007-04-29.

Pages 264–265 explicitly use the same number L of generators when defining preservation of wavelet structure; p.265 gives the corresponding indexed local-commutant identity for F^−1. Proposition 2 on p.266 separately treats ML generators with translation lattice MZ. Theorem 1 proves a smooth bandlimited single-generator example with no single-generator canonical wavelet dual but infinitely many alternative wavelet duals. Theorem 3’s actual quantifiers are: for each J there is an example whose canonical dual needs at least 2^J generators. This is not automatically one example excluding every finite number. The paper replaces the flawed argument in Daubechies–Han, ACHA 12 (2002), 269–285, DOI 10.1006/acha.2002.0381, identifying a frame-operator sign error. All these are dual results, not a canonical-tight resolution.

### Affine/quasi-affine separation: Bownik–Lemvig (2011)

M. Bownik, J. Lemvig, *Affine and quasi-affine frames for rational dilations*, Transactions of the AMS 363 (2011), 1887–1924, DOI [10.1090/S0002-9947-2010-05200-6](https://doi.org/10.1090/S0002-9947-2010-05200-6). [Author-hosted published PDF](https://pages.uoregon.edu/mbownik/papers/42.pdf), electronically published 2010-11-05.

The introduction distinguishes the affine orbit from its oversampled quasi-affine family. Theorem 1.1 concerns frame existence with uniform bounds over oversampling lattices; Theorem 1.3 concerns equivalence of pairs of dual frames; Theorem 5.6 concerns the canonical dual of a quasi-affine frame with unchanged generator count. These results do not assert that canonical tightening always preserves an affine wavelet orbit. In the rational noninteger case, Theorem 1.4 even separates frame existence for the two constructions, further ruling out an unqualified substitution.

### Recent dual-structure result checked at abstract/version level

A. Benavente, O. Christensen, M. Hasannasab, H. O. Kim, R. Y. Kim, F. D. Kovac, *Approximately dual pairs of wavelet frames*, [arXiv:2107.03938v1](https://arxiv.org/abs/2107.03938v1), submitted 2021-07-08. The checked arXiv page lists only v1. Its abstract concerns nonexistence of approximately dual affine frames and recovery by oversampling. It does not state a canonical-tight closure theorem. Full proof auditing was not performed for this peripheral paper.

## Bounded search conclusion

The search covered exact and synonymous formulations involving canonical normalized tight, canonical tight, canonical Parseval, wavelet structure, local commutant, and counterexample/negative-answer terms, plus the directly relevant Bownik author bibliography and the cited primary papers above. Search hits about canonical filters, finite signal transforms, graphs, Gabor windows, and canonical coefficient sequences were excluded as different meanings of “canonical.” A misleading search snippet concatenating a Gabor canonical-tight theorem and a wavelet canonical-dual counterexample was not accepted as evidence.

Recommended bounded status: **source clarified; no full canonical-tight resolution verified in this pass**. The 2004 historical unknown statement is verified. Present-day open status is unverified. The local-commutant criterion and semi-orthogonal positive subclass are existing context, not new mathematical work. Any future full claim must address the stated operator, indexing, and scope directly.
