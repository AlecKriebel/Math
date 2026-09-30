# Independent review: two-hypertorus layer recovery

## Verdict

**PASS_RESTRICTED_TWO_CONNECTED_HYPERTORI.** No mandatory correction is required. The submitted recovery theorem is valid within its stated class. The general rational-cohomology-to-layer-poset question remains **unsolved, 2/5**.

The frozen `PARTIAL_RESULT.md` SHA-256 is

`0902b513e349c0a5a3d811c458a865029441632a36e963580e04eb8838e25111`.

This is an independent adversarial AI review, not human peer review or a novelty assessment.

## 1. Primary question and prior examples

I read and visually inspected Pagaria's complete Question 3 on printed p.114 of [Oberwolfach Report 2/2018](https://ems.press/content/serial-article-files/46724?nt=1), including its preceding theorem and coefficient convention. The question uses **rational** cohomology and asks for the layer poset from the cohomology algebra. The Leray associated graded is discussed separately; the question does not supply its filtration, marked ambient classes, characters, or named meridians. The artifact accurately keeps the abstract graded-algebra scope.

I also read the definitions and exact example statements in the full [Pagaria v3](https://arxiv.org/abs/1804.05767v3). Theorem 2.1 has the same layer poset but different integral cohomology algebras; those examples have isomorphic rational algebras. Theorem 3.1 instead gives the same arithmetic matroid, different layer posets, and different rational cohomology algebras. Neither supplies isomorphic rational cohomology algebras with nonisomorphic layer posets. The artifact's exclusion of those purported counterexamples is correct.

The full-PDF hashes agree with the manifest: OWR `91efb3f45550efd99cbae32c72001ea6b8d40fd0a9c1301c2f524398f9530de5`; Pagaria `2f6f4a0c3aa41d976d4656e483fc527198e854d94b65071e022f07b7d5969714`. This audit establishes the restricted theorem and the fidelity of these cited scopes, not a comprehensive literature-status or priority result.

## 2. Primitive characters and normal form

An integral character vector v can be taken by an integral torus-coordinate change to `(k,0,...,0)`, where k is the gcd of its entries. The kernel then has k components. Hence a nonzero character has a connected kernel exactly when it is primitive.

After making the first primitive character the x-coordinate, write the second as `(a,b_2,...,b_d)`. Distinct connected central kernels cannot have proportional primitive characters: proportional primitive integral vectors differ only by sign and define the same kernel. Therefore the remaining vector is nonzero. Integral operations among the last d-1 coordinates take it to `(m,0,...,0)` with m positive. Primitivity of the second full character gives `gcd(a,m)=1`. This proves the normal form and also explains why two distinct connected central hypertori require d at least two.

Their intersection is exactly x=1, y in the m-th roots of unity, with the other coordinates free. Each of the m pieces is a connected torus and distinct pieces are disjoint. Each is contained in both hypertori and there are no further layers. The asserted abstract poset is therefore completely determined by m.

## 3. Bundle and local-system calculation

Over a simply connected patch in `C* minus {1}`, choose a branch of `x^(a/m)` and put `z=x^(a/m)y`. Then the forbidden equation becomes `z^m=1`, and z remains nonzero. This is an explicit local trivialization, not merely a count of fibers. The base and fiber retract to graphs with first Betti numbers 2 and m+1.

Around the base loop about 0, the removed nonzero points rotate by the step -a modulo m. Around the loop about 1 there is no winding about 0. On first homology, motion of based meridians can introduce conjugations but cannot add another homology class to an individual puncture meridian. Thus the first loop permutes the m meridians in a single cycle and fixes the meridian of 0; the second acts trivially. The dual convention changes a permutation to its inverse and does not change the ranks used here.

The cellular local-system differential on the two-loop graph consequently has the stated form. Its rank is m-1, so its kernel has dimension 2 and cokernel dimension `2(m+1)-(m-1)=m+3`. The only Serre terms lie in columns 0,1 and rows 0,1, leaving no possible higher differential. Possible extension questions do not alter graded vector-space dimensions. Hence `P_X(t)=1+4t+(m+3)t^2` follows.

## 4. Independent finite-cover derivation

I checked the same Betti numbers by a different topological description. Pull back the bundle along `u -> x=u^m`. The covering base is `B'=C* minus mu_m`. With `z=u^a y`, the pullback is the product `B' x (C* minus mu_m)`. The deck group mu_m acts freely through

`(u,z) -> (zeta u, zeta^a z)`.

Both H1 representations are the direct sum of one trivial coordinate (the meridian of 0) and a regular cyclic permutation representation on the m nonzero punctures. The coprimality hypothesis is used for the second factor. Over Q, transfer identifies the quotient cohomology with the invariant cohomology of this finite cover. The invariant H1 dimension is 2+2=4. In H2, the four tensor summands contribute `1+1+1+m`, giving m+3. This independently verifies the submitted spectral-sequence calculation without asserting a ring splitting.

The m=1 case is included: the cover is trivial and the normal-form complement is a product of two twice-punctured complex lines, with polynomial `1+4t+4t^2`.

## 5. Reconstruction and boundary cases

Multiplication by the `(C*)^(d-2)` factor gives exactly the displayed polynomial. Its coefficient in degree d is positive, so the top nonzero cohomological degree recovers d within this class. Expanding its first two coefficients gives `b1=d+2` and

`m=b2-binomial(d,2)-2(d-1)`.

For no hypertori, the polynomial is `(1+t)^d`; for one connected hypertorus it is `(1+2t)(1+t)^(d-1)`. In all three allowed cases, `b1-d` recovers the number of hypertori. The empty d=0 case has only degree-zero cohomology. For d=1 the two-hypertorus case is unavailable, as already implied by primitivity and distinctness. These boundary cases cause no ambiguity.

Because a graded-algebra isomorphism preserves graded dimensions, no marked ambient subalgebra, generator identification, filtration, or character lattice is required for this reconstruction. The theorem does not claim that arbitrary arrangements with the same algebra can be recognized as members of the restricted class. It also does not determine the residue a, a labeled arrangement, or ring isomorphisms between all residues. Those exclusions are important and correctly stated.

## 6. Checks and disposition

All **4,800** author assertions replay byte-identically. The independent standard-library checker passes **6,342** exact assertions. It counts invariant basis orbits in the finite cyclic cover and its tensor representation for 301 coprime parameter pairs, checks the intersection Smith-minor arithmetic, compares the entire Poincare polynomial with the layer sum, and reconstructs all permitted zero-, one- and two-hypertorus cases in finite ranges. It does not import the submitted verifier.

Run from the review directory:

```sh
python independent_checks.py
(cd author_replay && python verify.py)
```

The code does not establish a general bundle theorem or a ring-to-poset algorithm. The unbounded proof has been reviewed separately above. Preserve the restriction to at most two **distinct connected central** hypertori, the unmarked rational graded scope, and the general **unsolved, 2/5** disposition.
