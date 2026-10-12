# Independent in-scope extension search: canonical models, embeddings, certificates

Agent: `new_scope_search`. Checkpoint: 2026-10-07 04:39 UTC / 2026-10-06 21:39 America/Los_Angeles. Read `/Users/alec/Documents/Math/AGENTS.md`, the original project target, current theorem/dependency files, both priority assessments, the construction notes, and the reference field implementation. No external individual was contacted, no PR or git action was taken, and the upstream clone was not modified.

## Result

**No genuinely new theorem or new mechanism was identified in this approach family.** The strongest supported extension is another inherited consequence: after constructing an explicit field, deterministic polynomial-time representation conversion, field isomorphisms, explicit subfields, normal bases, and compatible standard-model canonicalization are already covered by the sources below. Replacing an existing construction subroutine with the newly validated prime-field factoring theorem changes the unconditional availability of those consequences; it does not invent their mechanism.

The assignment's search/audit is complete. Best-guess completion toward a *novel mathematical contribution through this route*: **0%**; toward a *publication package justified by that new contribution*: **0%**. These percentages are bookkeeping, not mathematical evidence. They do not revise the lead's separate estimate for the already audited core consequence.

This is a bounded negative novelty assessment, not a proof that no new finite-field theorem is possible. Publication should not be rescued by unsupported canonicity or certificate claims.

## Positive primary-source overlap

### Lenstra (1991): proved isomorphisms, conversion, subfields, normal bases

H. W. Lenstra, Jr., *Finding isomorphisms between finite fields*, Math. Comp. **56** (193), January 1991, 329–347; DOI [10.1090/S0025-5718-1991-1052099-2](https://doi.org/10.1090/S0025-5718-1991-1052099-2). [Author-hosted primary scan](https://pub.math.leidenuniv.nl/~lenstrahw/PUBLICATIONS/1991b/art.pdf).

Read the exact statements and proof passages: Theorems 1.1/1.2, §2, Theorem 3.1 and its full linear-algebra proof, and §9 Theorem 9.3/Lemma 9.4. Explicit data are multiplication tables of dimension `n`, encoded by `n^3` prime-field entries; polynomial time means bit time polynomial in `n` and `log p`. Theorem 1.1 converts an explicit field to an irreducible-polynomial representation. Theorem 1.2 computes same-cardinality isomorphisms unconditionally; Theorem 9.3 gives the relative-base version. Section 2 computes subfields by Frobenius kernels and reduces field-table validation to primality testing. Theorem 3.1 constructs normal bases deterministically by exact linear algebra, without a factoring oracle. Thus merely adding representation/certificate flexibility, relative isomorphisms, subfields, or normal bases supplies no new result. A modern deterministic primality algorithm removes the historical primality obstacle.

The full isomorphism proof's cyclotomic-ring lemmas were not independently re-audited in this search. This is positive priority evidence, not a claim of a new formal verification or a reproduced complete-package audit.

### de Smit–Lenstra (2013): public canonicalization statements, proof-status qualification

Bart de Smit and Hendrik Lenstra, *Standard models for finite fields*, in Mullen and Panario (eds.), *Handbook of Finite Fields*, CRC Press, 2013, §11.7, 401–404. [Author-hosted chapter scan](https://pub.math.leidenuniv.nl/~smitbde/prep/2013-standard_models.pdf).

Inspected all four pages visually after rendering and checked exact theorem numbers. Theorem 11.7.5 supplies polynomial-time isomorphisms satisfying `phi_B,C o phi_A,B = phi_A,C`. Theorem 11.7.10 computes a fixed standard model and an isomorphism to it from any explicit input field, in deterministic polynomial time. Definition 11.7.13 and Remark 11.7.15 define compatible standard embeddings. Theorem 11.7.16 and Remark 11.7.17 explain that constructing a field model from `p,n` is the remaining randomized/GRH step; normalization itself is deterministic. Thus composing deterministic field construction with that public canonicalization statement is an inherited corollary.

**Qualification:** the chapter's reference `[789]`, used for those algorithmic theorems, is *Standard models for finite fields, in preparation*. Reference `[790]` is the 2008 definition slides. I checked these bibliography entries in the [complete Handbook scan](https://archive.ymsc.tsinghua.edu.cn/pacm_download/672/12637-dingjt-p2.pdf), printed p.891 / PDF p.928. No complete proof of the canonicalization theorem was found or independently reproduced here. Public priority overlap remains positive evidence; the theorem must not be silently upgraded to a fully audited dependency.

### Later canonical-lattice work does not create an easy fresh route

Luca De Feo, Hugues Randriam, Édouard Rousseau, *Standard Lattices of Compatibly Embedded Finite Fields*, ISSAC 2019, 122–130, DOI [10.1145/3326229.3326251](https://doi.org/10.1145/3326229.3326251), [primary full text](https://arxiv.org/html/1906.00870). Read §1's precise compatibility, incrementality, uniqueness and generality requirements; its discussion of Lenstra, de Smit–Lenstra and Bosma–Cannon–Steel; and Propositions 3/5/6 and Corollary 7. It already distinguishes a deterministic/standard lattice from arbitrary root choices and constructs compatible Kummer embeddings. Its cyclotomic-lattice input is not a license to assume primitive roots or efficient Conway-polynomial construction. I did not validate its entire algorithm or practical cost experimentally.

Frank Lübeck, *Standard Generators of Finite Fields and their Cyclic Subgroups*, J. Symbolic Comput. **117** (2023), 51–67, DOI [10.1016/j.jsc.2022.11.001](https://doi.org/10.1016/j.jsc.2022.11.001), [arXiv v2 primary full text](https://arxiv.org/html/2107.02257v2). Read the introduction's complexity qualification, §5.4 Algorithm 5.5 and its proof, and §6 Algorithm 6.1/Remark 6.2. The paper explicitly declines asymptotic claims for its practical general search. Exhausting its fixed pseudorandom enumeration does not establish polynomial bit complexity. Its cyclic-generator construction is parameterized by supplied prime factors of the desired order; choosing the full multiplicative order would require the missing integer factorization. These facts exclude casual primitive-root/Conway upgrades.

Earliest-disclosure claims were not attempted here. The inspected public 1991/2013/2019/2023 statements suffice to establish overlap; source filenames and manuscript dates are not evidence of an exact first-disclosure time.

## Checkable mechanisms and boundary checks

### Deterministic embedding is already an easier problem

Let `A=F_p[u]/h_A`, `B=F_p[v]/h_B` have degrees `a|b`. In `B`, the kernel of `Frob_p^a-I` is the unique size-`p^a` subfield. Its `F_p` dimension is exactly `a`. Build the `b x b` Frobenius matrix by powering the basis vectors, take an exact kernel basis, and solve linear systems to express products in that basis. This yields an explicit subfield with an inclusion matrix. Apply the already proved same-size isomorphism theorem to `A` and that subfield. All steps are polynomial in `b` and `log p`; no integer factorization of `p^b-1` is involved. This is directly Lenstra's §2 plus Theorem 1.2, not an improvement in the core factorization problem.

Alternatively, after full polynomial factorization is available, factoring `h_A` in `B[X]` and choosing a root describes an embedding. Forming its image matrix is exact evaluation. This standard oracle reduction also adds no new mechanism.

### Pairwise smallest-root choices need not compose

The following exact counterexample was independently reproduced with the project's `FiniteField` arithmetic. It is a boundary certificate for a tempting *false* canonicalization argument, not a claimed research discovery.

Set `A=F_5[a]/(a^2+a+1)` and `B=F_5[b]/(b^2+b+2)`. Both quadratics are irreducible: their discriminants are `2` and `3`, both nonsquares mod 5. Order elements `c_0+c_1 t` by the integer `c_0+5c_1`.

- The smallest root of `X^2+X+1` in `B` is `3+2b` (integer encoding 13); the other is `1+3b` (16).
- The smallest root of `X^2+X+2` in `A` is `3+2a` (13); the other is `1+3a` (16).
- The smallest root of `X^2+X+1` in `A` is `a` (5); its other root is `4+4a` (24).

Consequently the two smallest-root isomorphisms compose as

`a -> 3+2b -> 3+2(3+2a) = 4+4a`,

which differs from the direct smallest-root map `A->A`, namely the identity. A pairwise deterministic tie-break is therefore insufficient for transitive coherent embeddings. A standard model or established compatible-lattice construction is a substantive additional mechanism, already present in the literature.

One must also distinguish coordinate-dependent standard models from a selector natural under **every** abstract field automorphism. Such a natural generating-element selector cannot exist when the extension degree exceeds one: Frobenius invariance would force its output into the prime subfield. This elementary observation does not obstruct standard coordinate models, which use specified encodings and choices.

### Field/certificate flexibility is inherited

For a quotient representation `F_p[t]/h`, deterministic irreducibility checks use Frobenius congruences and gcds with degrees polynomial in `deg h`; factoring the numeric degree by trial division is allowed by the dense input. Returning those congruences and gcd Bézout identities makes verification explicit but does not add a theorem.

For a commutative associative unital `n`-dimensional algebra given by structure constants over a verified prime field, a transparent check is: its Frobenius matrix `F` satisfies `F^n=I`, and `dim ker(F-I)=1`. The first condition makes Frobenius injective, excludes nilpotents, and hence makes the finite commutative algebra a product of finite fields. Each component contributes one dimension to the `p`-fixed subalgebra, so the second condition gives one field component. Conversely a size-`p^n` field satisfies both conditions. Basic algebra axioms are checked on basis vectors and the unit is found/checked by linear equations. These polynomial checks refine Lenstra's already published field-table validation scope; they are not positive novelty evidence.

## Approach decision table

| Candidate | Supported status | Exact new-contribution gap |
|---|---|---|
| Polynomial/tower/structure-table representations with certificates | Inherited exact-linear-algebra and Frobenius machinery | No newly unresolved claim identified |
| Isomorphisms, relative isomorphisms, subfield embeddings | Already unconditionally deterministic polynomial-time | Does not need the upstream breakthrough |
| Normal bases or explicit trace-dual bases | Existing deterministic linear algebra | No new theorem/mechanism |
| Fixed output depending only on `p,n` | Any deterministic construction already fixes an output; stronger standard models publicly stated | No novel canonicity established |
| Coherent compatible embeddings via standard model | Public de Smit–Lenstra statement and later lattice constructions | Full canonicalization proof not independently audited here; priority overlap positive |
| Pairwise smallest-root shortcut | False as coherent-embedding assertion | Explicit `F_25` counterexample above |
| Conway polynomials/primitive multiplicative generators | Unsupported under requested bounds | Integer-order factorization and/or exhaustive canonical search cannot be assumed |
| Lexicographically first irreducible polynomial among *all* degree-`n` polynomials | Not supplied by Shoup or mere deterministic factoring | Enumerating `p^n` candidates is not polynomial in `n log p`; no new polynomial mechanism supplied |

## Reproducibility and source preservation

The downloaded primary scans are research evidence, not proposed publication files. Redistribution rights were not established, so omit them and OCR/render outputs from any Zenodo upload kit. Their URLs, byte lengths and SHA-256 values are recorded in `sources/newscope-source-manifest.json`:

- `newscope-lenstra1991.pdf`: SHA-256 `d533832fa891bd136c1f057246e96119e16dda5fe4b2755beabe5a4c2ac0a39e`.
- `newscope-desmit-lenstra2013.pdf`: SHA-256 `a945a53faec6ebe69b052f275824c8d407c87403b52348c69a4e47493776dc4b`.

The standard-model chapter's four relevant pages were rendered with system Poppler and visually inspected; OCR is saved only as auxiliary reading evidence. No formal build or new theorem proof certification is claimed.

Recommendation to lead: record this approach as **inherited / no new mechanism identified**, preserve the false-shortcut counterexample, and do not promote this family to a new-solution deposit. Reopen only for an actual new mechanism or independently verified theorem beyond the positively overlapping literature.
