# Independent adversarial review of the Clifford-constraint family

Reviewed UTC: **2026-10-24 18:06**. Reviewer did not author the note or its generator. Research completion estimate remains **12%**, as a planning estimate toward the full problem; this review does not promote that estimate or claim a solution. The review includes the central-unit and group-basis addition made during the audit.

**Verdict: the stated partial deductions and numerical witness pass this audit. There is no resolution of Kourovka 21.135 and no group counterexample.** No substantive mathematical correction was identified. This verdict covers only the exact partial note and arithmetic below, not a general originality audit, formal verification, or a proof that an artificial packet can be realized.

## Frozen inputs

| File | SHA-256 |
| --- | --- |
| `clifford_constraints.md` | `23744c4009b0677d16caabacee6548ffd3ac6b9934f4f74386820143127e7d29` |
| `check_character_constraints.py` | `72f3189bb8346d2c48f651a0566e7446001aaeec38451c173db65eb5638e7ded` |
| `character_constraints_results.json` | `7852d0f2d79d4da40ae16b4a46dfd337f4cb15ac98e4ace3ee915d3f2cb371eb` |

The primary Itô PDF cached by the author was independently read by the reviewer. Its stated theorem is the degree-divides-index result for maximal abelian normal subgroups, and it explicitly recalls the center-index theorem used in the alternative Clifford proof. Every abelian normal subgroup is contained in a maximal such subgroup in a finite group, so the note's formulation follows. The PDF hash is `4ad22e2fe48a33a67dc2d3a7f7d864c7d832ffbefb5b8d3846fd7a920f420849`.

## Attempts to falsify the theoretical deductions

1. **Existence of an elementary abelian minimal normal subgroup.** If the solvable radical is nontrivial, its last nontrivial derived subgroup is nontrivial abelian and normal in the whole group. A minimal whole-group normal subgroup inside it is elementary abelian. This does not require the radical to be abelian or the quotient to be simple.

2. **Itô denominator bound and its use.** For each irreducible degree, Itô gives divisibility by the abelian normal subgroup's index. Taking the least common multiple gives the asserted divisibility of its order by `c=n/L`. The converse interpretation of `c=1` uses prime valuations and permits a different defect-zero character for each prime. This is a sufficient condition, not a claimed necessity for radical-free groups. The direct-product formula for `L` follows prime by prime from maxima of sums of valuations. The displayed A7 example genuinely prevents a universal `c=1` reduction.

3. **Clifford packets.** The relevant character of the inertia group is the Clifford correspondent in `Irr(I|lambda)`. Since lambda is linear and invariant in its inertia group, restriction is `e lambda`, and its degree is `e`, without an extension hypothesis. Frobenius reciprocity applied to `Ind_V^I lambda` gives `sum e^2=|I:V|`. Induction to the whole group multiplies degrees by the orbit length, giving the stated packet mass. The projective representations all use a common factor set for that orbit. Neither the factor set nor the inertia group can be discarded. In the alternate proof of Itô divisibility, `ker(lambda)` is inertia-normal and is killed by the correspondent; `V/ker(lambda)` is central in `I/ker(lambda)`. The center-index theorem therefore applies as stated.

4. **The action constraint.** Minimal normality makes the conjugation module irreducible over F_p, including the possible one-dimensional trivial module. Its image is a quotient of the group and a subgroup of `GL_a(p)`. The kernel of the induced action of `H/V` can indeed be `C_H(V)/V`; faithfulness of that quotient action is not silently assumed.

5. **Central sectors and Galois symmetry.** For central `Z=C_p`, the restriction of an irreducible character is its degree times one linear central character. Frobenius reciprocity gives each sector mass `n/p`. A splitting cyclotomic field contains the pth roots and its Galois group restricts onto the automorphisms of those roots. It therefore permutes the nontrivial central sectors transitively, preserving character degrees. This proves the common nonprincipal multiplicities in equation (2); it does not identify any sector from the unlabelled input multiset.

6. **Multiplicity gcd and determinant obstruction.** If `Z` is not contained in the derived group, a linear character nontrivial on `Z` exists, because the image of `Z` in the abelianization has order p. Its tensor powers permute all p sectors, so p divides every degree multiplicity. Thus `g=1` forces `Z` into the derived group. Determinants of all representations kill the derived group. A nontrivial scalar of order p on a degree-d irreducible representation then forces p to divide d. This justifies (3), the `p^3` order divisibility, and the floor-capacity inequality (4). Each use retains the `g=1` hypothesis where it is needed.

7. **Perfect groups and solvable linear images.** A unique linear character is equivalent to perfection. A homomorphic image of a perfect group is perfect; a finite group that is both solvable and perfect is trivial. The claimed solvable `GL` cases are correct: one-dimensional groups are abelian, `GL_2(2)` is `S3`, and `GL_2(3)` has central order-two kernel over `PGL_2(3)=S4`. A trivial action on a minimal normal elementary abelian subgroup makes every one-dimensional subspace normal, forcing that subgroup to have order p. Proposition 5 then follows by eliminating all possible p. The criterion is explicitly sufficient and does not cover arbitrary dimensions.

8. **Central units and group bases.** Assigning scalar signs to individual Wedderburn blocks defines a central involution because both packets are nonempty. The trace of left multiplication on a matrix block `M_d(C)` is `d` times the ordinary matrix trace, so the two equal square masses give regular trace zero for `z`. On each negative block the displayed `J,D` matrices give `u^2=z`, `u^4=v^2=1`, and `vuv=u^-1`. A negative block exists and this two-dimensional representation is faithful on the generated eight-element group, so the global units generate a copy of D8. Positive blocks contribute `n/2` to the trace of `u`, and negative blocks contribute zero. Thus these units cannot be elements of a group basis, except that the separate involution `z` itself has the necessary zero trace. Since a member of the original `G` that is algebra-central would lie in `Z(G)=1`, the nontrivial `z` is outside `G`; adjoining it gives the direct product with C2. Every index-two subgroup is a kernel of a homomorphism to C2, and perfection of `G` makes this kernel uniquely `G`. Finally, the proposed trace criterion is sufficient: if `sum c_k k=0`, multiply on the left by any `h^-1` and take the regular trace. Only `k=h` contributes, with trace `n`, proving `c_h=0`. An order-n set of independent elements in an n-dimensional algebra is a basis. This proof requires all nonidentity elements of the proposed finite subgroup to have zero trace, not just its central involution.

Boundary checks also show that these obstructions do not falsely prohibit every central kernel. For `D8=<r,s | r^4=s^2=1, srs=r^-1>`, the degrees are four copies of 1 and one copy of 2. The center `C2=<r^2>` lies in the derived group; the four linear characters have principal-sector mass 4, and the degree-two character has nonprincipal-sector mass 4. Here the multiplicity gcd is 1 and `p^3=|D8|`, so equality in the bounds is allowed. Conversely, the center of the group `C2` is not in its derived group, and its two degree-one characters have gcd of multiplicities 2. This confirms why dropping the gcd assumption would invalidate the determinant-based inference.

## Independent exact arithmetic reproduction

The separate checker `independent_packet_checker.py` does not import, call, or copy the hook-length routine, partition routine, convolution routine, or packet search. It starts from the explicit lists

- A5: `1,3,3,4,5`;
- A7: `1,6,10,10,14,14,15,21,35`.

For every power from 1 through 6 it enumerates all ordered tuples of those lists and multiplies their entries. It compares the resulting complete multiplicity map with the supplied record and independently checks every reported order, least common multiple, denominator gap, multiplicity gcd, linear-character count, and prime-free square mass. All **12 records** pass. This reproduction assumes the stated standard base degree lists; it is independent of their hook-length generation.

For the A7-cubed central-C2 packet, the independent checks find:

| Quantity | Exact value |
| --- | ---: |
| Total order | 16,003,008,000 |
| Total character count | 729 |
| Distinct degrees | 70 |
| Principal-sector character count | 94 |
| Nonprincipal-sector character count | 635 |
| Square mass of each sector | 8,001,504,000 |
| Principal linear-character count | 1 |
| Nonprincipal linear-character count | 0 |
| Total odd-degree square mass | 6,772,724,288 |
| Available even-degree square mass | 9,230,283,712 |

Every available multiplicity is used exactly once across the two packets; no negative, zero-listed, or excessive multiplicity occurs. Every odd-degree occurrence is principal, every nonprincipal degree is even, and every degree in either sector divides the half order. The half order and central constraints (1)–(4) are satisfied. For p=2, the Galois multiplicity equation has just one nontrivial sector, so there is no extra equality between different nontrivial sectors to check.

The author's bounded-subset search is not claimed to be exhaustive. Its greedy large-weight choices may miss witnesses, but this does not affect a returned witness: all required identities are exact and have now been checked by a different method.

The checker also enumerates the group generated by the displayed 2-by-2 matrices with exact integer multiplication. It has eight elements, the commutator is `-I`, and its global regular traces have multiplicities: one at `n`, one at zero, and six at `n/2`. This independently verifies the new finite-unit example and its failure of the group-basis trace requirement.

Independent checker SHA-256: `f41d33ca40a1aae1650ff3c15031078a5e20da40b35a9ae3e95d96327b8a3b28`.

Independent results receipt SHA-256: `d2f9bcca0d583d316fea3bf3281517e0a52ab3ca22e2b4e994d0533894f5958c`.

Reproduction from this directory's parent:

```text
python3 review/independent_packet_checker.py
```

The receipt includes a check timestamp, so its bytes change on rerunning even when all mathematical results agree. The input and checker hashes are preserved inside the receipt.

## Exact scope and unresolved obstruction

The artificial principal packet has **not** been proved to be the character-degree multiset of a group. The nonprincipal packet has **not** been realized as the irreducible degrees of one twisted group algebra of an actual quotient. No extension is constructed. These missing realization requirements are central mathematical information, and are not consequences of the verified integer equalities.

Accordingly the witness disproves only a proposed inference from the *retained numerical conditions alone* to a contradiction. It does not disprove the Kourovka assertion, does not exclude stronger constraints, and does not prove that a radical-free source can share its multiset with a group having a radical. The note correctly marks these limitations and asserts no new recognition theorem or publication-ready solution. The route remains partial at its stated exact gap.
