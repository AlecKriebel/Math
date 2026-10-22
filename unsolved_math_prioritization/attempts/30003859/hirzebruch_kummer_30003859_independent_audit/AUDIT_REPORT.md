# Independent adversarial audit: Hirzebruch-Kummer rigidity

Problem 30003859 / OWR-16169-001, rank 741. Audit date: 2026-10-05.

## Disposition: PASS, strictly scoped

The frozen author packet passes this audit as a five-approach partial investigation. No mandatory mathematical corrections were identified. This is **not** a pass for solving the intended nontrivial-incidence conjecture, and it is not proof-assistant certification or peer review.

The controlling result remains:

- The unrestricted projective-orbit formulation admits the four-line/Fermat counterexample.
- The intended nontrivial-incidence problem remains unresolved in this investigation.
- For each fixed nonpencil arrangement, the retained argument establishes eventual periodicity of **infinitesimal-rigidity failure**. It does not establish eventual rigidity or periodicity of local rigidity.

The audit is bound to the 25,533-byte author archive with SHA-256 `e70fb6353ef5a98363dfd3cbe9aa66531a1b45ef92e90bde2c19b4e70cf99bf9` and the author manifest with SHA-256 `e999f3f7d15d19152e106ad898c8f6ec2f36b9f5ca7cedbdb067477accbfa867`. All ten archive members equal the corresponding frozen directory files byte for byte. The author files were not edited.

## 1. Scope and source formulation

All ten author files were read, including every proof and both executable verifiers. The relevant primary sources were retrieved independently. Five PDF byte counts and SHA-256 hashes match the author metadata. The public dataset row response and statement hash also match; no dataset contents or source material are included in this audit packet.

The OWR contribution states the nonpencil setup on printed p.1696 and the eventual-rigidity conjecture on p.1697. The latter page was independently rendered and visually inspected. It does not explicitly add the high-valency restrictions. [Official OWR report](https://publications.mfo.de/bitstream/handle/mfo/3650/OWR_2018_28.pdf?isAllowed=y&sequence=1)

In the configuration paper, Definition 1.2 uses the local projective-orbit notion. Remarks 1.3 and 1.5 subsequently assert the high-valency conditions as consequences. Printed pp.5-6 were independently rendered and visually inspected. A four-line projective frame refutes those consequences under the unrestricted definition. Interpreting the surrounding work as targeting a nontrivial-incidence class is justified, but this is an interpretation, not an author-issued corrected conjecture. The author packet handles that distinction appropriately. [Configuration paper](https://arxiv.org/pdf/1803.02984)

The source's equisingular theorem uses the deformation subspace defined by the kernel of the local singularity-deformation map in Definition 2.1. Thus it must not be expanded into a theorem for arbitrary abstract deformations of the resolution, or merely for constant incidence/topology. This supports the packet's stated missing bridge; it does not supply that bridge.

The credited quadrangle theorem is for that arrangement, with exponent at least four. Proposition 8.1 separates the positive cases four and six from a nonzero tangent space at three. The later configuration paper explicitly states the rigidity threshold as an if-and-only-if theorem. No general-arrangement theorem is inferred. [Rigidity paper](https://arxiv.org/pdf/1609.08128)

The tangent-eigensheaf formula was checked in Lemma 2.8 of the publisher's primary text, together with the character convention and the stronger hypotheses in the deformation-equivalence criterion. [Boehning-Graf von Bothmer-Pignatelli](https://link.springer.com/article/10.1007/s40574-021-00296-3)

## 2. Proof-by-proof findings

### Proof 1: four-line frame and maximal cover — PASS

The dual-frame normalization is algebraic and has trivial projective stabilizer. Consequently it identifies the ordered incidence space with PGL(3), including the tangent-space assertion. The coordinate-power morphism has generic degree n^3 and adjoining three coordinate ratios gives the full exponent-n abelian cover. Its Fermat hypersurface is smooth and connected, so no unresolved singularities or missing quotient invalidate the example.

### Proof 2: genuine abstract deformations — PASS

The singularity equations force the last two coordinates to vanish and the first two to be nonzero. Eliminating the perturbation parameter yields the stated lower bound on its absolute value, excluding singular fibers on the unit disk for every n >= 4.

The restricted Euler sequence really gives all ambient vector fields along the embedding: the needed first cohomology of the structure sheaf vanishes. The perturbation monomial has every exponent below n-1, so it survives the Fermat Jacobian quotient. Modding out by the defining polynomial introduces no exception because that polynomial is already in the Jacobian ideal. The resulting class is a nonzero **abstract** Kodaira-Spencer class, not just an embedded tangent direction.

The family is actual, smooth, and proper. Fischer-Grauert therefore rules out local rigidity; there is no unsupported inference from nonzero H^1 alone. The quartic count is correctly 19 embedded directions and is not confused with the full 20-dimensional unpolarized K3 tangent space.

### Proof 3: invariant deformations — PASS

The root-map local calculation gives exactly the logarithmic tangent fields, including crossings with independent inertia. Finite pushforward and characteristic-zero averaging justify passage to invariant first cohomology. Vanishing of this summand does not eliminate nontrivial characters. The packet neither identifies all deformation functors nor infers abstract rigidity from branch rigidity.

### Proof 4: fixed base and finite sheaf types — PASS

The nonpencil hypothesis ensures that a meridian basis can omit a line outside any high-valency point. The local meridians at that point are independent; at crossings, the two inertia groups are independent even for composite n. No prime-exponent assumption is hidden in the argument.

The resolution calculation is consistent: over a valency-v point, a local exceptional component has degree n^(v-1) over the exceptional base curve and self-intersection -n^(v-2). For n >= 2 and v >= 3 this excludes exceptional (-1)-curves. Thus the fixed-base cover is the minimal desingularization required by the problem.

The character line-bundle relation bounds integral coordinates on the fixed rational blow-up. Its torsion-free Picard group identifies the line bundle, rather than merely a numerical class. A selected subset of the fixed branch components identifies the logarithmic sheaf. There is consequently no unrecorded continuous parameter or n-dependent cohomology inside a given type.

For the root map x=u^n, the least nonnegative exponent of an eigenvector-field coefficient is k=(a+1) mod n. Its image contains a logarithmic x factor exactly when a is not n-1. This independently confirms the potentially delicate boundary in the formula. Character-sign conventions can relabel the summands and do not change the asserted dimension or total vanishing.

### Proof 5: exceptional exponent-three summand — PASS

The ten divisor classes and inertia values were reconstructed from the six edges of a projective frame, independently of the author's monodromy table. The selected character has L=-K and the four stated logarithmic components. Their divisor classes have rank four in Picard rank five. Since their individual first structure-sheaf cohomologies vanish, the residue sequence gives a one-dimensional logarithmic H^1, hence a one-dimensional tangent-character summand by duality.

This is an exact summand calculation, not a computation of the whole tangent space. Integrability is not asserted from this calculation. Prior quadrangle results are credited rather than presented as new.

### Proof 6: all-exponent eventual periodicity — PASS

This proof was checked independently rather than inferred from any finite character census. The critical points are:

1. The arrangement, rational blow-up, branch components, integral meridian vectors, and divisor classes are fixed before n varies. The finite sheaf-type list is therefore valid for every exponent.
2. Each carry has a uniform finite bound. After fixing carries, the occurrence constraints are affine integer-linear constraints. Expressions such as n*k do not multiply two variables because k has already been fixed.
3. Boundary residues are included exactly: omitted logarithmic components have residue n-1; included components have residues from zero through n-2. Coordinate zero facets and negative carries are also retained. No passage to open chambers, generic characters, or a dense asymptotic region discards exceptional types.
4. Replacing n by 2+u and adding nonnegative slack variables gives an affine integer system. Dickson's lemma makes the minimal solutions finite. The homogeneous monoid is generated by its minimal **nonzero** elements, using subtraction and induction on the coordinate sum.
5. Projection to n preserves finite unions of linear sets. In one dimension, each nontrivial finitely generated monoid fills all sufficiently large integers in its attained residues modulo any positive generator; singleton components contribute only finite exceptions. Finite unions have an eventual common period.
6. The cohomology of each fixed sheaf is independent of n. The finite union of occurrence sets for positive-cohomology types is exactly the failure set. Multiplicities of characters do not affect whether the total first cohomology vanishes.

Thus the fan/chamber and boundary objections are resolved directly by the integer-linear argument. Its conclusion allows an infinite periodic set of failures. It supplies neither the relevant cohomology values nor the assertion that no bad type occurs at large exponents. It also does not promote infinitesimal information to a statement about nonreduced Kuranishi spaces or actual local rigidity.

### Fifth approach's stopping point — PASS as an unresolved gap

Persistence of exceptional curves, compatible contraction, and the required preservation of local singularity deformation type have not been proved for arbitrary small abstract deformations. Negative self-intersection alone does not provide that statement. Fibrations or equivariance do not repair the gap automatically. The packet explicitly stops rather than claiming a theorem here.

## 3. Executable evidence

The author manifest verifier was run with replay and self-tests. It reproduced the mathematical output in normal and optimized Python and rejected all six listed integrity mutations. The author result still records 4,858,415 consistency checks and 220,824 enumerated characters; neither count is treated as a universal proof.

The independently written verifier imports no author code and uses a different character parameterization: five line residues determine the sixth by their sum, and incidence determines exceptional residues and Picard coefficients. It independently enumerates all 630,707 characters for 2 <= n <= 12. On the author's range, the complete sheaf-type digest agrees exactly. The additional type counts are 2,669 at n=11 and 2,674 at n=12.

Other independent controls include:

- projective-frame determinants and a concurrent-frame negative control;
- Fermat witnesses and exact singularity bounds for 4 <= n <= 100;
- Jacobian dimensions by inclusion-exclusion, rather than the author's monomial enumeration;
- four invalid Fermat witnesses and a mutated exceptional character;
- 819 local root-map eigenweight calculations through order 40;
- signed-carry and residue-boundary checks;
- affine integer occurrence examples with periods two and three, and a finite preperiod exception.

Independent normal and optimized outputs are byte-identical. These are finite executable controls, with the all-n conclusion resting on the audited proof. Neither verifier solves general logarithmic sheaf cohomology.

## 4. Mandatory corrections and optional precision

Mandatory corrections: **none** for this exact frozen packet and its stated scope.

Two optional wording improvements would make future revisions even harder to misread:

- In Proof 6B, write “the componentwise-minimal elements of H minus {0}” instead of “the nonzero componentwise-minimal elements of H.” The argument plainly requires minimality among nonzero homogeneous solutions.
- When expanding the fifth approach, specify the source's local-singularity deformation condition rather than using “equisingular” without definition. No abstract-to-equisingular bridge is supplied by this audit.

Neither optional clarification changes the present disposition or author bytes.

## 5. Audit limits and release guardrails

This is an independent mathematical/code/source audit, not a full re-proof of the cited long quadrangle theorem. The general abelian-cover formula, standard deformation theory, Serre duality, and projective-space cohomology remain explicit external dependencies. A bounded fresh literature search found no general resolution among the primary results inspected; this is not proof of absence. Historical repository/conversation search claims were read as author-reported history and were not independently replayed. The 68,931,837-byte cached corpus was not redownloaded; its fresh matching public row was checked instead.

A PASS may accompany this scoped investigation only. It must not be relabeled “intended conjecture solved,” “all arrangements eventually rigid,” “local rigidity eventually periodic,” or “independently proved full quadrangle theorem.” The author's unresolved status, no-novelty claim, and separation of rigidity notions must remain visible.

No remote writes were performed. This audit directory contains only original audit analysis, independent code/results, integrity records, and public verification metadata. It excludes source PDFs, extracted source text, page images, dataset contents, private sources, and coordination records.
