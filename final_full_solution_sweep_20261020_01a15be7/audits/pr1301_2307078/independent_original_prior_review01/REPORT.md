# PR1301 /2307078: independent original, mathematical and priority audit

**PASS — exact full planar result, already published in1993. No new publication
is warranted.** The candidate proof needs no mathematical repair. A qualified
four-literal-cell existing-publication proposal is in ROW_PROPOSAL.json; B is
blank, C is https://doi.org/10.1112/jlms/s2-47.2.309. This review did not insert a
row, merge a PR, reserve a DOI or mutate any service. Overall sweep estimate80%;
assigned audit100%. Root must refresh live duplicate state before any row action.

## Exact original question and conclusion

Freshly retrieved Hayman–Lingham arXiv1809.07200v2, physical pages186–187,
printed185–186, contains Rubel's Problem7.78. I read the full question, physical
interpretation, update and exact bibliography reference163, and visually checked
both pages. The question asks for an infinite pairwise distinct complex sequence
with summable reciprocal moduli whose unit-charge reciprocal-difference sum is
zero-free. The extra higher-dimensional suggestion is a separate aside. The
candidate correctly proves that no such planar example exists; it actually has
infinitely many distinct zeros off its poles. Zero charge locations are excluded
by the finite reciprocal-modulus hypothesis. Interpreting the sum off its poles
does not weaken the negative answer: the proof produces genuine finite zeros there.
[Versioned primary problem source](https://arxiv.org/abs/1809.07200v2).

The actual pinned PROOF.md is9244bytes, SHA256
01acd0855e1659c3be31d134fa9fd4c7337b8a7e4cd49770e41872b6ea59c425,
Git blob070d700dc7ea5f834bfdd1fe51300fad74e24435, at head
6f3ef788a0007555c325f370648a50d5e2067466. All ten root-pinned public blobs
were independently fetched and their native Git object identities checked without
Git mutations. Their internal nine-file manifest matches. I read all ten files,
including the entire proof, audit and acceptance. A fresh native PR read shows the
same head, open draft and no merge. Historical6243-byte candidate and aggregate
integrity reports inside the PR were not substituted for these current proof bytes
or treated as newly reproduced theorem checks.

## Adversarial analytic review

INDEPENDENT_PROOF.md gives a complete separate reconstruction and explicit attacks.
No source-author code, numerical experiment, compiler or finite toy matrix was used.

1. Summability forces the charge points to leave every compact disk. The distant
   reciprocal terms are bounded by2/|z_n| uniformly on each fixed disk, so absolute
   normal convergence defines S off the poles, with residue1 at each point. The
   result is independent of reordering. There is no conditional regularization.
2. The normally convergent analytic logarithmic tails build the genus-zero product
   F with F(0)=1. The finite head determines its exact, simple zero set. Its
   derivative is nonzero at every charge. Local logarithmic differentiation gives
   F'/F=S; a nonexistent entire logarithm of F is never assumed.
3. A finite-head/summable-tail bound proves log M_F(r)=o(r), not merely order≤1.
   Unit-circle Cauchy, as in the candidate, preserves the needed upper bound for
   F'. I independently used radius-r circles: M_F'(r)≤M_F(2r)/r. F' is not zero
   identically. The derivative growth step has no hidden type assumption.
4. For a putative finite zero set of a nonzero entire G, division by its exact
   multiplicity polynomial P leaves an entire zero-free H. A large-circle lower
   bound on P transfers the logarithmic upper growth bound. This covers a zero
   at0, repeated zeros and the empty zero set. Constructing an entire logarithm
   of H uses simple connectedness of the plane and the primitive of H'/H.
5. A one-sided bound on Re h is enough. I reconstructed the harmonic estimate
   using every Taylor coefficient at0: the k-th boundary coefficient has modulus
   |c_k|R^k/2 and is bounded by the mean of the nonnegative harmonic function
   A_R−Re h. Its mean is o(R), forcing every c_k(k≥1) to vanish. Thus G is a
   polynomial. No unsupported absolute bound on h, factorization theorem or
   circular finite-zero assertion is used.
6. A finite distinct zero set for F' would make F' polynomial, hence F polynomial,
   contradicting its infinitely many simple zeros. Therefore F' has infinitely
   many distinct zeros. None is at a charge; every one yields a zero of S.
7. The normalized potential sum log|1−z/z_n| is convergent on its proper domain.
   Direct real differentiation gives U_x−iU_y=S and U_x+iU_y=conjugate(S), so its
   real equilibria are exactly the zeros obtained. It does not subtract two
   divergent total potentials. A possible equilibrium at0 remains allowed.

The principal failed counterexample route is e^z−1: it has infinitely many simple
zeros and a zero-free derivative, but positive exponential type and divergent
reciprocal-modulus sum of its nonzero zeros. It defeats an order≤1 shortcut while
leaving the actual o(r) argument intact. A single charge demonstrates why infinitude
is used. Repeated product zeros would obstruct the last separation step; the
original distinctness hypothesis prevents that. No unmentioned arrangement,
real-line, symmetry, genericity or extra moment hypothesis enters the proof.

## Exact earlier publication authenticated

I freshly fetched the complete author-hosted1993 PDF and inspected its first two
pages visually. Equations1.1/1.2 supply the convergence and normalized potential;
the paragraph on printed310 immediately before Theorem2.1 explicitly states the
distinct-location unit-charge infinite-zero conclusion. Its genus-zero logarithmic
derivative argument is the exact target, not a weaker dependency. I also read the
full general Theorem2.2 proof text on314 as context; its other dependencies were
not audited or needed for the independent unit-charge proof.

The authors, title and journal footer agree with primary publisher metadata and a
fresh Crossref registered-record response: J. Clunie, A. Eremenko and J. Rossi,
*On Equilibrium Points of Logarithmic and Newtonian Potentials*, Journal of the
London Mathematical Society, series2 volume47, issue2, April1993, pages309–320,
DOI10.1112/jlms/s2-47.2.309. The online2016 date is a later digitization date, not
the original publication year. [Primary full paper](https://www.math.purdue.edu/~eremenko/dvi/cer.pdf),
[publisher record](https://academic.oup.com/jlms/article-abstract/s2-47/2/309/868781).

Hayman–Lingham Update7.78 credits the planar resolution to those three authors;
reference163 identifies this same1993 paper. Thus the DOI is the already published
full resolution itself, not merely the problem-list DOI or a cited technical
input. There is no novelty claim to clear and no reason to create another record.
The arbitrary-real-charge and higher-dimensional variants, and their present
status, are outside this audit and proposed row.

Fresh PDF pins match those claimed in the PR exactly:

- CER1993:711975bytes, SHA256
  c794c298de9929c6319a2938c365b66ff8a9465f9b00ce3762ddb5757eef32c3.
- Hayman–Linghamv2:1706228bytes, SHA256
  8e28fd4403a07e4e19a9816b7efaafddf9f475d59cf8c34a8255cb03833ed4f0.

The direct DOI resolver redirected to the correct Wiley DOI endpoint, where this
client received403. This is recorded exactly in DOI_RESOLUTION.json, not described
as a successful200 landing-page fetch. It does not leave the publication identity
or full mathematical body unavailable: the matching complete author-hosted paper,
primary publisher record, bibliography and Crossref registration jointly establish
the existing record. PUBLICATION_IDENTITY.json contains the fresh metadata and
private raw capture pin. SOURCE_READ_SCOPE.json states all reading limits.

## Fresh deduplication and disposition

The FIRST candidate step was a fresh read-only GWS CLI check. It selected numeric
gid1254632077, confirmed43 columns, read the entire1178-row grid in value and formula
views and bracketed them with stable metadata. Both views returned191 populated
rows and identical raw captures. Initial broad leads in rows41,74,90,94,114,139,
156,162,170 were read and are unrelated results. No exact candidate match existed.

A second fresh read after identifying the publication searched all43 columns in
both views for the catalog/source/PR aliases, exact DOI, paper title and authors.
There was no same-result or same-DOI row. Three substring false positives were
read: Rossi within crossing wording in rows13/106 and7.78 normalized to a different
PR778 in row124. All are unrelated. Exact native Zenodo queries for the catalog
and paper-title phrase returned zero; this is bounded duplicate evidence, not a
claim of worldwide absence. Private ledger bodies remain private.

ROW_PROPOSAL.json contains exactly four strings in A/B/C/D order. It credits the
1993 authors and existing DOI, states the complete planar conclusion, identifies
the original update and PR, and qualifies the PR as AI-assisted unrefereed
exposition only. The blank B cell does not invent a chat link. The proposal gives
no action authority; root must check live state immediately before any append or
update. No new manuscript, publication, DOI reservation or supporting upload kit
should be prepared for this already published result.

All work is within this new dedicated review folder. Root input pins remain
unchanged; all other closed folders were left untouched. No Git/index/ref, STATE,
case, ledger, publication, service-write or outside-communication operation was
performed. Fresh API operations were read-only. The retained packet is below6MiB
and the150MiB free-space reserve is preserved. Exact source and local-artifact
custody are closed by CLOSED_DIRECTORY_SEAL.json. There is no mathematical or
primary-publication blocker remaining for the qualified existing-record proposal.
