# Bounded priority audit for arbitrary powers of A7

Checkpoint: 2026-10-24T18:18:08.690593+00:00. Completion estimate: 100% of the assigned bounded literature screen; this is not an originality certification or a mathematical-proof audit. The target is the restricted statement that, for every r>=0, a finite group with the same multiset of irreducible complex character degrees as A7^r is isomorphic to A7^r. Kourovka 21.135 remains the broader radical-recognition question.

## Outcome

No primary theorem covering all r for A7^r was located. No general recognition theorem for arbitrary direct powers of all nonabelian finite simple groups was located. The accompanying independent broad-search report is `general/findings.md` when complete. This outcome means **priority remains unestablished**, not that the statement is new. The case r=1 is already known, and the candidate rests on a classical finite-linear classification; these antecedents must be credited explicitly.

## Primary results checked and their exact limits

1. **M. Baniasad Azad and B. Khosravi, Recognition of some characteristically simple groups by their complex group algebras**, Mathematical Reports 22(72), no.1 (2020),1–10. [Primary journal PDF](https://imar.ro/journals/Mathematical_Reports/Pdfs/2020/1/1.pdf).

   The paper's stated families are powers of A5 up to exponent5, PSL2(7) up to7, PSL3(3) up to13, and PSL2(17) up to17. Its numerical hypotheses involve order and existence of specified degrees, yielding complex-group-algebra recognition. A7 is absent. Its introduction cites preceding direct squares of PSL2(p), squares of simple K3-groups, and products of distinct Suzuki groups. None of those source families includes A7. The paper supplies no all-simple-powers transfer theorem.

2. **C. Bessenrodt, H.N. Nguyen, J.B. Olsson and H.P. Tong-Viet, Complex group algebras of the double covers of the symmetric and alternating groups**, Algebra & Number Theory9(3) (2015),601–628, [DOI10.2140/ant.2015.9.601](https://doi.org/10.2140/ant.2015.9.601); [primary publisher PDF](https://msp.org/ant/2015/9-3/ant-v9-n3-p04-s.pdf).

   Theorem B recognizes every finite quasisimple group by its complex group algebra; Theorem6.2 explicitly treats perfect central covers of A6 and A7. This covers A7 itself. For r>=2, A7^r is not quasisimple: its quotient by its trivial center is a nontrivial direct product. The theorem therefore does not cover arbitrary powers. Recognition of single factors supplies no automatic decomposition theorem for unknown groups with matching algebra.

3. **J. Guo, Y. Liu, Z. Wu and D. Xiao, Non-solvable groups whose non-linear character degrees have the same number of different prime divisors**, arXiv2604.10100v1 (11April2026), [primary full text](https://arxiv.org/html/2604.10100v1).

   Definition1.1 and Theorem1.3 require the number of *distinct* prime divisors to be identical for every nonlinear degree. A7 is among the classified factors. This hypothesis fails for A7^r as soon as r>=2: degree6 has two distinct prime divisors, whereas degree6*35=210 has four. The theorem consequently does not recognize arbitrary A7 powers. The constancy condition must not be confused with the candidate's even total number of prime factors counted with multiplicities.

4. **B. Huppert and O. Manz, Nonsolvable groups whose character degrees are products of at most two prime numbers**, Osaka Journal of Mathematics23 (1986),491–502, [primary repository PDF](https://ocu-omu.repo.nii.ac.jp/record/2008995/files/111F0000002-02302-18.pdf).

   The opening theorem classifies the case where every degree has at most two prime factors counted with multiplicity. It includes A7 up to an abelian direct factor, but not A7^r for r>=2, which has degree36. This is another source for already-known r=1 recognition, not all r.

5. **M.L. Lewis and D.L. White, Nonsolvable groups all of whose character degrees are odd-square-free**, author manuscript dated30July2009, [author-hosted primary PDF](https://www.math.kent.edu/~white/papers/oddsqfree.pdf).

   Its hypothesis excludes degrees divisible by an odd prime square. A7^r has degree36 for r>=2. The introduction also describes recognition of nonsoluble groups with no degree divisible by4, again excluding powers r>=2. These results cannot be extrapolated to bounded arbitrary p-adic valuations.

6. **A. Moretó, Complex group algebras of finite groups: Brauer's Problem1**, [author-hosted primary manuscript](https://www.uv.es/amoquin/24.pdf).

   Theorems B–C concern bounds for the order from the maximum multiplicity of a degree, with a restriction on alternating composition factors in TheoremC. They do not identify all groups matching a prescribed direct-power degree multiset. This was checked because searches for degree patterns and semisimple groups returned it as a possible broad theorem.

## Bibliographic leads not promoted to verified priority conclusions

- K. Aziziheris, *Degrees of irreducible representations of direct products of nonabelian simple groups*, RACSAM114 (2020), DOI10.1007/s13398-020-00799-2. The available author abstract concerns degree **sets** and proves only quasiperfectness for an enumerated list of classical and sporadic homogeneous powers; the list does not include alternating groups. The primary full text was not accessible, so no stronger exclusion or attribution is made.
- T. Hawkes, *On groups with isomorphic complex group algebras*, Journal of Algebra167(3) (1994),557–577, DOI10.1006/jabr.1994.1202. [Warwick institutional metadata](https://wrap.warwick.ac.uk/id/eprint/20399/) explicitly provides no full research output. The publisher endpoint was inaccessible (403/failed retrieval). This remains an unchecked older structural-priority lead. Its title alone cannot establish or exclude an A7-powers consequence.
- Later Suzuki-product recognition was screened independently by the broad-search subagent. Results about Suzuki powers, even unbounded families of parameters, do not include alternating factors.
- Spectrum, element-order prime graphs, conjugacy-class-size multisets, ordinary character tables, modular Brauer degrees, and codegrees were excluded as different inputs. They cannot be silently substituted for the ordinary complex degree multiset.

## Search scope and residual gap

Queries included A7, A_7, A_{7}, alternating groups of degree7, direct powers, homogeneous powers, characteristically simple, semisimple finite groups, degree pattern, character-degree multiset, complex group algebra, and recognition. Later literature searches included2021–2026. Exact all-simple-powers and mixed-product formulations were also searched. The independently checked2020 bibliography and2015 theorem statements constrain several common false-positive references.

The remaining gap is a theorem not located by these bounded searches, possibly under another formulation or in an inaccessible older source. A new proof of a known theorem remains possible. This report author did not audit Lindsey's classification or the candidate proof, because a separate fresh reviewer owns that mathematical audit. No external communication, Git mutation, publication, or upload was undertaken. Raw third-party caches are under `sources/`; only authored notes and SHA-256 provenance manifests should be included in checkpoints.
