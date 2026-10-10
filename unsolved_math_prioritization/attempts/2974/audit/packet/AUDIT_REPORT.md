# Independent audit: fixed-manifold Lefschetz pencils

Problem 2974 / KP-4.98. Audit date: 2026-10-08.

## Verdict

Accept the frozen packet as a source-conscious, five-approach **partial analysis**, with status **unsolved here**. No mathematical correction to the frozen arguments is required for their stated scope. The published classification is correctly kept source-conditional, and the product-polarization caveat is substantiated. The universal claim is not proved or refuted.

This audit adds two useful qualifications without changing the author's freeze:

1. The odd-prime finite models cannot detect one factor-of-two error. Independent even-modulus and integer tests close that particular test-coverage gap.
2. For the full closed-surface Johnson target, any nonzero saturated ambient-invariant subgroup is the whole target. The original quotient criterion therefore has a stricter application limit than its reducible illustration suggests. A separate, proved intrinsic-index criterion in JOHNSON_QUOTIENT_ADDENDUM.md can retain a nonzero saturated initial image.

These are audit refinements of Approach 3, not a sixth approach or a universal construction. No novelty, peer review, formal certification, publication, or global queue modification is claimed.

## 1. Freeze and target

The author archive is exactly 16,496 bytes, SHA-256:

    beabecc7f40e4a064740fc457c5a2f1c735695c63a255021d8f35decae74d342

The external author manifest SHA-256 is:

    b744942d6086721c08ab2508a87b71e6c0d553486964b898e6cb9e1a81d10662

All seven files match both the separately pinned manifest and fresh archive extraction. The original packet, manifest, and archive were checked again after the tests and remain unchanged. The complete authored report, checker, README, status, approach ledger, recorded results, and source metadata were reviewed.

The K3 problem was checked on displayed/PDF page 271. Its fixed-original-manifold requirement, equal-genus comparison, and nonempty pencil base set matter. The usual oriented equivalence allows an orientation-preserving base diffeomorphism. Thus movement of critical values is not an inequivalence invariant. The standard Hurwitz moves preserve the generated closed monodromy subgroup up to global conjugacy; arbitrary partial conjugation is not itself an allowed equivalence move.

The report correctly separates increasing genus, blowups, homeomorphism, a common compatible form, and a result for each prescribed symplectic form. Its CP2 admissible-genus caveat is correct and is not passed off as a solution to the intended multiplicity question. Primary target URL: https://bpb-us-e2.wpmucdn.com/websites.umass.edu/dist/b/22144/files/2026/04/K3-problem-list-watermarked.pdf .

## 2. Highest-priority source issue: HH18 Lemma 3.5

The publisher's final PDF and the arXiv version agree on the relevant issue. The final lemma on displayed page 1527 excludes an underlying elliptic product when the first polarization elementary divisor is one. Its argument imposes a degree-one factor in a product decomposition of the line bundle. Section 2.3 defines polarization type through an integral symplectic normal form, while Remark 3.4 identifies line bundles with the same ample Chern class up to translation. There is no surrounding restriction that converts an arbitrary product surface into a product polarization with a degree-one factor.

The author's counterexample to that literal intermediate exclusion is valid. A product of degree-four and degree-nine line bundles on elliptic curves is very ample: each factor embeds its curve, and their exterior tensor product gives the Segre embedding. Its alternating integral form, in the ordered basis e1,f1,e2,f2, is 4J direct-sum 9J. An explicit integral basis is

    x1 = e1 + e2,
    y1 = -2 f1 + f2,
    x2 = 9 e1 + 8 e2,
    y2 = 9 f1 - 4 f2.

The basis matrix has determinant 1. The pairings are E(x1,y1)=1 and E(x2,y2)=36, and all cross-pairings vanish. This proves type (1,36), without relying only on a numerical guess from the degree. Independent determinant-minor checks also give Smith determinantal divisors 1,1,36,1296. A generic hyperplane pencil in the resulting embedding is Lefschetz and has finite nonempty base set. It lies within the lemma's normalization.

The exact valid restricted assertion is that a product bundle with a degree-one elliptic factor has a fixed divisor and cannot define a Lefschetz pencil of this kind. Merely saying that a polarization is decomposable is not sufficient: the degree-(4,9) example is itself an exterior-product polarization. Read the report's proposed qualification in this precise degree-one-factor sense.

This establishes a defect in the literal intermediate exclusion, **not** a refutation of HH18 Theorem 1.1, and does not decide whether its proof can be repaired. The theorem's high-genus classification is correctly treated conditionally in the author packet. No correction addressing this particular wording was found in a bounded erratum search; no exhaustive negative literature claim is made.

Primary source: Hamada and Hayano, *Topology of holomorphic Lefschetz pencils on the four-torus*, https://msp.org/agt/2018/18-3/agt-v18-n3-p08-s.pdf . The exact local PDF hash and inspection history are in SOURCE_INSPECTION.json; no source bodies or rendered source images are included here.

## 3. Approach 1: fixed product-T4 finite multiplicity

Accepted. On the fixed product surface, U and V extend to an integral basis, have square zero, and intersect once. Thus F=aU+bV has square 2ab and divisibility gcd(a,b). The two factor degrees may be ordered oppositely under Poincare duality; this does not affect the construction or any formula. K=0 gives genus ab+1. Blowing up 2ab base points and applying the Lefschetz Euler formula gives 6ab critical points.

For (a,b)=(3,12) and (4,9), the common genus is 37, there are 72 base points and 216 critical points, and fiber divisibilities are 3 and 1. Every integral homology automorphism preserves divisibility, so arbitrary allowed total-space diffeomorphisms cannot identify these pencils.

For a square-free product M of k odd primes, each divisor a>1 produces b=M^2/a. Both degrees are at least three, a divides b, and gcd(a,b)=a. Distinct divisors therefore yield 2^k-1 inequivalent pencils of genus M^2+1 on the same product T4. The product complex structure and Kahler form stay fixed. Generic smooth fibers are connected, by ampleness and the Hodge index argument in the report.

The quantifiers are correct: arbitrarily large finite sets are obtained, with genus allowed to grow. This gives no infinite fixed-genus family and no arbitrary-X construction. The generic very-ample-pencil step is standard and is supported by Auroux–Smith Proposition 2.5: https://arxiv.org/abs/math/0401021 .

## 4. Approach 2: coefficient variation and conditional classification

Accepted. The good-pencil locus in the relevant complex Grassmannian is nonempty Zariski open, hence path connected. Along a path, the transverse base points and nondegenerate critical points persist without collision; an isotopy of the base identifies the critical values. Parametric local models and the proper-submersion trivialization on their complement supply an equivalence.

One local detail is worth making explicit: choose the trivializations also in the original standard pencil charts near each moving base point before blowing up. Their lifts are then compatible with the marked exceptional sections and with smooth blowdown. It is not necessary, and would not be correct as a general shortcut, to claim that every arbitrary diffeomorphism matching exceptional sections automatically descends smoothly. The path construction permits the required controlled choices.

The independent coefficient-variation obstruction does not use HH18 Lemma 3.5. Conditional on the published high-genus classification, F=dA and evenness give h-1=d^2 m with positive integer m, so only finitely many divisibilities can occur at a fixed h. Consequently finitely many holomorphic equivalence classes occur at h>5 under that classification. The prime h-1 example and the conclusion about infinitely many nonholomorphic members in an infinite family are valid conditional deductions.

## 5. Approach 3: exact kernel image and conjugacy invariants

Accepted as written. Let a_s=s^-1 f^n s f^-n. The subgroup D generated by its G0-conjugates is stable under G0 and normal in the generated group. Since the changed generators are s a_s, G_n=D G0. Since D lies in N, intersection with N is precisely D(G0 intersect N). Applying the additive equivariant tau gives

    tau(G_n intersect N) = Lambda_0 + nM.

The sign/order convention in s^-1 acting on tau(f) is consistent with the displayed a_s. The argument does not silently discard Lambda_0 or require a free group of generators. It is a written proof; finite examples are not its substitute.

For an ambient-invariant saturated C, L/C is a free abelian group with an induced integral ambient action. Content is unchanged under every such automorphism, and the content of n Mbar is n times the positive content of Mbar. This separates all positive n, and the zero subgroup separates n=0. Hence the report's sufficient criterion is correct.

Both hypotheses matter. A quotient by Z e2 cannot carry the action of an ambient coordinate swap. For a concrete nonsaturated failure, take the infinite dihedral semidirect product Z rtimes C2, G0 generated by reflection and translation by 3, and f translation by 1. Then Lambda_0=3Z and M=2Z. The invariant but nonsaturated C=3Z has nonzero Mbar, yet G1=G2 is the full group since gcd(3,2)=gcd(3,4)=1.

The audit addendum proves the full-Johnson-module restriction and an alternative intrinsic index formula. In the latter, if Lambda_0 is saturated and rank increases by s>0, then for n>0

    [Sat_L(Lambda_n):Lambda_n]
       = n^s [Sat_L(Lambda_1):Lambda_1].

Rank and this index are intrinsic ambient-automorphism invariants, so no invariant fixed quotient is needed. This is additional conditional algebra, not a mapping-class realization theorem.

Closed monodromy nonconjugacy remains sufficient even when base points are unlabelled and the base is reparametrized. The report correctly retains centralization in the boundary mapping class group, positivity, sections of square -1, the original smooth X after blowdown, and form compatibility as separate unsolved geometric obligations.

## 6. Approaches 4 and 5: characteristic-number obstructions

Both accepted, within the specified operations.

For fiber sum, e(Y#_F Z)=e(Y)+e(Z)-2e(F), while signature is additive. Substituting Y=X#b CPbar2 and e(Z)=4-4h+r_Z gives the stated e and signature. Ordinary blowup or blowdown preserves e+signature. Recovery of the original oriented X would therefore require r_Z+sigma(Z)=0. For the fourfold-blown-up ruled family, h=2q, e(Z)=8-4q, sigma(Z)=-4, and r_Z=4q+4. The defect is 4q>0. More blowups and blowdowns cannot remove it.

For cyclic degree-d base change with its two branch values regular, every old critical point has d preimages. The ramification components upstairs are fibers of square zero. The signature correction vanishes, so sigma(Y_d)=d sigma(Y). Combining this with the Euler count yields

    (e+sigma)(Y_d)-(e+sigma)(X)
      = (d-1)(e(X)+sigma(X)+4h-4).

The CP2, T4, and K3 values in the report are correct. Pullback of a section's normal line bundle multiplies its degree by d, so the distinguished lifted section has square -d. The report does not overstate this as a classification of all exceptional spheres; the numerical obstruction already prevents any repair by the allowed ordinary operations in the listed cases.

The square-zero use of the branched signature formula was checked against Geske–Kjuchukova–Shaneson Theorem 1: https://academic.oup.com/imrn/article/2021/6/4605/5880468 . No claim is made for the zero-defect cases or for operations such as rational blowdown.

## 7. Literature and accounting

The 2026 Lee–Servan preprint is correctly credited for its ruled-surface infinite fixed-genus families, fixed fiber class, four base points, and a common compatible form. The arXiv page still displayed only v1 during this audit. Its Section 7 does not establish identical smooth total spaces in the broader homeomorphic examples. This literature is substantial prior progress, not a newly completed approach: https://arxiv.org/abs/2602.10051 .

The existing problem-11000156 report and its citation correction were checked for the inherited Baykur mechanism and the distinction between Hurwitz and partial-conjugation equivalence. That supporting work is properly credited and is not counted again: https://github.com/AlecKriebel/Math/pull/955 . The five entries in APPROACHES.json correspond to five mathematically different construction attempts. Retrieval, normalization, integrity checks, this audit, and its algebraic refinement count zero additional approaches.

## 8. Independent replay and mutation evidence

REPLAY_RESULTS.json records actual UID=EUID=1000. A fresh extracted packet and a separate current directory were mode 0555, with files mode 0444. Three actual writes were denied by permissions: creating in the packet, creating in the current directory, and appending to a packet file. The author checker passed normal, -O, and -OO, with identical output hashes. Recorded CHECK_RESULTS.json matched the replay's mathematical results. No assert statements occur in the author checker; its explicit exception checks remain active.

Eleven integrity mutations, each under all three modes, were rejected: same-length report mutation, removed file, extra file, symlink, FIFO, directory replacing a file, wrong trust pin, modified untrusted manifest, malformed JSON with its updated pin, wrong schema with its updated pin, and wrong byte count with its updated pin. Both one-sided manifest option combinations were rejected in all modes. This gives 39 integrity/CLI rejections.

Seven arithmetic mutations were rejected in all three modes: changed genus, changed polarization pairing, removed n-dependence, omitted initial lattice, incorrect content input, wrong blowup signature, and wrong base-change coefficient. These were run without manifest verification so failures came from mathematical guards, not simply changed hashes.

One deliberately tested arithmetic mutation passed all three author modes: replacing 2n by n in the expected odd-prime kernel sets. Over each odd prime used there, these generate the same cyclic subgroup. This is a coverage limitation, not a false result of the original unmutated checker. The independent checker includes 992 exact semidirect-product cases over moduli 4,6,8,9, exact integer reflection normal forms, and a deliberate even-modulus control rejecting that factor loss. It also checks an explicit polarization basis, larger divisor families, 900 base-change parameter cases, and 180 unimodular intrinsic-index cases.

The independent checker also passed normal, -O, and -OO from a read-only directory with identical outputs. Neither checker certifies holomorphic existence, arbitrary group proofs, mapping-class realizability, the external classification, or smooth manifold equivalence. Integrity pins authenticate neither authorship nor mathematics.

## 9. Final disposition

Keep the frozen author packet unchanged and retain status unsolved here, five approaches completed. Preserve the HH18 qualification and the common-genus/fixed-manifold scope in any later summary. Include this audit and its Johnson addendum when relying on the stronger algebraic analysis. No source text, PDF, screenshot, dataset content, private coordination material, or external publication is included in this audit packet.
