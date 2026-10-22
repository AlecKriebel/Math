# Independent adversarial audit: problem 30000120

Date: 2026-10-05. Target: OWR-744-003, catalog rank 805.

## Verdict

**PASS_SCOPED_PARTIAL. No mandatory mathematical correction to the frozen eight-file author packet was found. The general problem remains unsolved by this work.** Five approaches are documented, with a complete positive result for the specified product family and a complete negative result for the proposed tangent/logarithmic generator set. This is a reconstruction of classical geometry, with no novelty or priority claim.

The accepted positive family is `(P²)^b × (Bl_(v₂(P²)) P⁵)^c`, for nonnegative `b,c` with `b+c>0`, under the product of the specified PGL₂ and PGL₃ actions. It does not contain an additional P³ factor theorem. Unbounded symmetric rank obtained by taking products does not cover arbitrary irreducible symmetric spaces.

The author ZIP is 15,380 bytes, SHA-256 `98bee5d4d337662dcd1948cb8dd6b475e601261d78f862ed26113a508f746b37`. Its manifest SHA-256 is `8230850b1590ae6539b13e1b12ce3c75cd04a8af1558637a144c2d7f72078bbf`. Every archive entry matched its corresponding frozen file before review. This audit is separate: none of those files was edited. Frozen statements that audit was pending are historical, superseded for acceptance purposes by this report, not rewritten.

## 1. Identity, source, and prior-artifact gate

The full bytes of all three specified corpora were independently hashed and parsed. Their sizes, record counts, and hashes match the author metadata: catalog 21,735,099 bytes / 15,458 records; problems 68,931,837 bytes / 15,458 records; research reports 80,334,822 bytes / 6,701 entries. The catalog identifier is a string; the full problem identifier is an integer. Matching those correctly gives a unique rank-805 catalog record and a unique problem record. Every field of the selected full record and its dated literature assessment was inspected. There is no report under the matching problem-number key. This is identity verification of the complete corpora and semantic review of the complete target record, not a claim to have individually audited every unrelated problem.

The independently recomputed statement and full-review hashes are, respectively, `507a455289204b5d979c5233723a5066ad499494d353d5d66399a8c8ed933939` and `356bbe91046be52ff36003f1cea1673024789faeec03761e1ae847fc746f1647`. The precise serialization and corpus hashes appear in BINDINGS.json. Raw corpus contents are excluded.

The source asks for explicit generators using Chern classes of **equivariant vector bundles**. It already knows existence. The omitted qualifier in the abbreviated catalog statement must therefore remain in the mathematical target. Independently downloaded [EMS](https://ems.press/content/serial-article-files/45960) and [MFO](https://publications.mfo.de/bitstream/handle/mfo/2861/OWR_2004_42.pdf?isAllowed=y&sequence=1) PDFs match the frozen hashes. Their relevant paragraphs were read; MFO PDF page 11 was rendered and visually inspected. The printed pages differ, 2177 versus 2181, while both are PDF page 11. The exact target website remained unavailable in web retrieval; no live website inspection is claimed.

Read-only GitHub searches for the exact identifier, problem number, wonderful-related PRs, and wonderful-related commits established no earlier actual target artifact. A broader Chern PR query returned unrelated problems. These finite searches are not exhaustive absence proofs, and the historical 0/5 queue value is not an actual mathematical attempt. No skip or prior-solution inference is warranted.

## 2. Geometric identification, checked independently

Let W be three-dimensional over C. Quadratic forms up to scale form P(Sym² W*)=P⁵. Their rank-one locus Z is the smooth degree-four Veronese surface. Congruence of nondegenerate complex symmetric matrices proves transitivity on the rank-three locus. The stabilizer of the identity form in PGL₃ is the image of the conformal orthogonal group, equal over C to PO₃ after rescaling a representative. It is exactly the fixed subgroup of `[g] ↦ [(gᵗ)⁻¹]`. Thus the group and stabilizer really are the adjoint symmetric pair stated in the report; this is not merely an SL₃ construction silently relabeled PGL₃.

The invariant center gives an induced PGL₃ action on X=Bl_Z P⁵. To check the boundary, use a chart in which the upper-left coefficient is nonzero. Divide by that coefficient and complete the square. The matrix becomes

    [ 1   u       v     ]
    [ u   u²+x    uv+y  ]
    [ v   uv+y    v²+z  ].

The center is (x,y,z)=0, and its determinant is xz−y². Consequently the determinant cubic has exact multiplicity two along Z. With H the pulled-back hyperplane class and E the exceptional divisor, its strict transform has class F=3H−2E.

The blowup is locally A² times the blowup of A³ at zero. The latter is the total space of O_P²(−1). The strict transform of xz−y²=0 is the restriction of that line bundle to the nonsingular conic in P². Hence E and F are nonsingular near the exceptional locus and transverse there: the radial coordinate defines E independently of the conic equation. Away from E, the determinant hypersurface is nonsingular along rank-two forms because its adjugate is nonzero. This proves the global simple-normal-crossing claim.

There are precisely four orbits. Outside E, they are ranks three and two. Over a rank-one form, its stabilizer contains a full GL₂ acting by congruence on the normal binary quadratic forms; the remaining action only adds scalings or transformations preserving this rank distinction. Nonzero binary forms in projective space have exactly two congruence orbits, ranks one and two. Since Z itself is homogeneous, these give exactly the closed orbit E∩F and the orbit E\F. The orbit closures are X, F, E, and E∩F. Smoothness, completeness, the dense symmetric orbit, and this boundary/orbit incidence verify the wonderful properties.

The diagonal two-dimensional torus in PGL₃ is inverted by the involution, so symmetric rank is two. PO₃ has rank one, while PGL₃ has rank two. Thus this example is outside the minimal-rank equality.

## 3. Genuine equivariant bundles

For a G-invariant Cartier divisor D on a G-variety, the sheaf O_X(D) sits inside the rational-function sheaf; transporting rational functions by G preserves the divisor condition. This gives the canonical algebraic G-linearization and its cocycle law. Both E and F are invariant Cartier divisors. Therefore O_X(E) and O_X(F) are genuine PGL₃-equivariant line bundles.

One must not replace this argument by an unsupported PGL₃ linearization of O_P⁵(1): the central character on the SL₃ quadratic-form representation is nontrivial. The frozen proof avoids that pitfall correctly. The change of coordinates from (H,E) to (E,F) has determinant of absolute value three. It is invertible over Q and does not give an integral Picard basis. No integral-cohomology generation statement is accepted here.

## 4. Ring, signs, and completeness of presentation

Write z=c₁(O_P²(1)) on Z. Then H|Z=2z and

    c(N_Z/P⁵)=(1+2z)^6/(1+z)^3=1+9z+30z².

This follows from the correctly oriented normal exact sequence `0 → T_Z → T_P⁵|Z → N → 0`. Some informal source notes have typographical problems in this sequence or intermediate coefficients; those errors were not imported into the frozen proof. The center class is 4H³ and restriction onto H*(Z,Q) is surjective, with kernel (H³).

The smooth-center blowup presentation, using E|E=−ξ for ξ=c₁(O_P(N)(1)), gives

    R = Q[H,E] / (H³E, E³−(9/2)HE²+(15/2)H²E−4H³).

The sign is fixed by the exceptional divisor, not by choosing a polynomial fit. The presentation is complete: additive blowup cohomology supplies H*(P⁵,Q), H*(P²,Q) shifted by two real degrees, and a second copy shifted by four. Pullback surjectivity identifies these extra pieces with the exceptional monomials in the report. Thus the twelve displayed monomials span and are independent, odd cohomology vanishes, and the even Betti numbers are (1,2,3,3,2,1).

The ambient relation H⁶ need not be added. If r₃ and r₄ denote the cubic and H³E, respectively, then

    H³r₃ − E²r₄ + (9/2)HE r₄ − (15/2)H²r₄ = −4H⁶.

All reductions to the twelve-dimensional quotient are consequently justified inside the stated two-generator ideal. Independent homogeneous-ideal matrices verify dimensions through degree eight; vanishing in degree six then implies all higher degrees vanish because the polynomial algebra is generated in degree one. The additive geometric theorem, not the finite dimension check, identifies this quotient with cohomology.

Putting a=E and b=F gives H=(2a+b)/3. Substitution multiplies r₃ by 54 and r₄ by 27 to give exactly

    8a³+3a²b−3ab²−8b³,     a(2a+b)³.

The inverse linear substitution proves ideal equivalence and generation by the first Chern classes of the two equivariant boundary lines.

As a separate sign check, invert the normal Chern polynomial: s(N)=1−9z+51z². The projective-bundle pushforward on E, with E|E=−ξ, yields

    ( ∫H⁵, ∫H⁴E, ∫H³E², ∫H²E³, ∫HE⁴, ∫E⁵ )
      = (1,0,0,4,18,51).

For the dual-conic hyperplane ν=2H−E, the mixed intersections of H and ν are (1,2,4,4,2,1). Our checker also reconstructs nondegenerate Poincaré pairings in every degree. These checks are independent of the author's monomial reducer.

A further classical comparison uses μ=H and ν=2H−E. In these variables the cubic and quartic ideal agrees with the one in [Kaveh, Section 5.3](https://arxiv.org/pdf/math/0312503), and the volume polynomial has coefficients (1,10,40,40,10,1). The two ideals were compared in both directions by exact homogeneous linear algebra. This supports the no-novelty classification. Only the ordinary rational ring computation is used from this source, not any unexamined assertion about adjoint-group linearization.

## 5. Tangent/logarithmic obstruction and product scope

The codimension-three center gives K_X=−6H+2E. Therefore c₁(T_X)=6H−2E=2(E+F). For the verified simple-normal-crossing divisor D=E+F, the logarithmic tangent determinant gives c₁(T_X(−log D))=c₁(T_X)−D=E+F. Both bundles are equivariant under the action.

Their degree-two Chern classes span one line, whereas dim H²(X,Q)=2. Higher Chern classes have degrees at least four, and a graded Q-algebra generated in nonnegative degrees cannot use them to supply a missing degree-two class. Consequently the combined Chern classes of both named bundles fail to generate. This refutes only that proposed set, not Brion's arbitrary-bundle target.

For P²=P(Sym² C²*), congruence gives the open orbit PGL₂/PO₂ and the boundary a smooth discriminant conic. The full fixed subgroup PO₂ is disconnected; replacing it by its identity component would change the homogeneous space. There are two orbits, and the symmetric rank is one. Its invariant boundary line has first Chern class 2h, generating Q[h]/(h³). Both PGL₂ and PO₂ have rank one, so this factor also fails the minimal-rank equality.

Products preserve smoothness, projectivity, the normal-crossing boundary, and the precise orbit-intersection condition. The product involution has the product fixed subgroup. Rational Künneth and pullback of the actual equivariant boundary lines prove the theorem for all b,c, not merely the finitely tested cases. The symmetric rank is b+2c; rank(G)−rank(K)=c, so every nontrivial stated product is non-minimal-rank. The asserted Poincaré polynomial follows by multiplication. No arbitrary irreducible reduction or extra P³ family is proved.

## 6. Review of all five approaches and newer literature

1. The primary target is retained, including equivariance. [Brion–Joshua](https://arxiv.org/pdf/0705.1035), Theorem 2.2.1 and Section 3.3, are explicitly minimal-rank statements. They compute restriction descriptions and tangent-type Chern data; this is not an arbitrary-symmetric bundle list. The frozen scope distinction is correct.
2. [Brion 2004](https://arxiv.org/pdf/math/0410039), Theorem 1 and Section 3.5(ii), supplies extensions in its stated setting and an additive K-group shortfall for its extension classes. The report correctly avoids claiming that a proper additive span forces the Chern-generated algebra to be proper. In general algebra it need not: {1,x} spans a proper subspace of Q[x]/(x³) but generates the algebra. Coherent extensions must not silently be called locally free.
3. The tangent/logarithmic obstruction is completely proved in Section 5 above.
4. The finite-resolution criterion is correct: Chern characters of resolution terms are rational polynomials in their Chern classes; alternating sums recover the spanning characters. Odd-vanishing and the supplied spanning hypothesis then suffice. It is conditional, and explicit uniform sheaves and resolutions remain missing. The cycle-map assumption is harmless additional context, not a way to manufacture those inputs.
5. The complete-conic construction and its product theorem are complete only in their stated scope.

The dated literature triage was supplemented independently. [Strickland 2012](https://www.sciencedirect.com/science/article/pii/S0021869312000610) retains the equality rank(H)+rank(G/H)=rank(G); its primary-repository opening text and publisher abstract were inspected. [Banerjee–Can, Theorem 1.1](https://arxiv.org/pdf/1603.04926), is a broader GKM-type equivariant K-theory description for smooth projective spherical varieties, while its Theorem 1.2 specializes to minimal rank. Thus it would be inaccurate to say every later ring-description theorem is minimal-rank. The inspected congruence description does not by itself identify a uniform explicit set of global equivariant vector bundles realizing the requested Chern generators. This is a scope assessment of the inspected statements, not a claimed impossibility of deriving such a construction.

[Can–Joyce–Wyser](https://arxiv.org/abs/1509.03292) concerns classes of spherical-subgroup closed orbits on flag varieties, a different immediate output. [Duan–Li](https://arxiv.org/pdf/0906.4152) gives blowup cohomology and applications to complete conics and quadrics; the retrieved document is v7, not the older v4 with different numbering. [Debnath–Zeng 2026](https://arxiv.org/abs/2604.14536), Section 5 of the retrieved v1 PDF, treats oriented cohomology for the same Veronese blowup. It is a current preprint source for broader cohomology-theory calculations on this particular model, not evidence of the unrestricted adjoint-symmetric generator theorem. Its PDF and experimental HTML display different internal document dates; no single date was inferred from those inconsistent displays.

[Henry July's equivariant-cobordism paper](https://link.springer.com/article/10.1007/s00031-022-09775-z), published online in 2022 and in a 2024 issue, also has general spherical-variety scope. Its abstract and Remark 3.9 concern ring descriptions and the remaining computation of classes, not an asserted uniform list of the global bundles sought here.

No general resolution was established by these searches. This audit neither proves present-day global openness nor exhausts the literature, and it makes no peer-review claim for the packet.

## 7. Reproduction, adversarial controls, and limits

Both author normal and optimized runs passed, including its five integrity mutations, and reproduced RESULTS.json byte-for-byte. The same runs were repeated from fresh ZIP extraction in an unrelated temporary directory. The author's 1,728 associativity cases, 144 commutativity cases, and 12 unit cases are accepted as finite checks only.

The independent checker does not import author code. It constructs homogeneous ideal matrices, recomputes Chern/Segre data, checks the boundary and classical ideals, tests pairings and generation, expands the local determinant symbolically, and verifies 48 product-polynomial examples. Nine deliberately false mathematical claims are rejected, including wrong exceptional signs, wrong Veronese degree, an altered boundary cubic, multiplicity one, integral boundary-basis generation, and the tangent/logarithmic shortcut.

Nine additional integrity mutations test changed report/code, missing or extra files, extra directory, changed manifest, symlink, same-size corruption, and a wrong external pin. Normal, `-O`, and relocated audit runs must give byte-identical CHECKS.json. The optional author-directory argument also checks the complete frozen author inventory and runs both author modes.

These finite computations do not prove smoothness, group equivariance, the blowup theorem, the all-product statement, source accuracy, novelty, or the original conjectural target. Those issues were assessed mathematically above. A malicious replacement of the verifier can lie, so independent trust must begin with the externally supplied ZIP and manifest pins, not with the untrusted verifier's self-report.

No remote mutation, publication, or external outreach was performed. The safe audit contains only authored mathematical review, original verification code/results, and public bibliographic and identity metadata. No PDF, source extract, rendered source image, raw corpus record, or private coordination material is included.
