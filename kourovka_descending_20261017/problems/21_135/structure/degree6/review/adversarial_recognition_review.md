# Independent adversarial review: the A7-power recognition theorem

Review completed UTC: **2026-10-24 18:17:53**. The reviewer did not author the candidate proof or its primary-data parser. Research planning estimate toward the full Kourovka problem remains **12%** for this family; the present review closes a restricted verification task and does not solve the general problem.

**Verdict: accepted as a complete restricted theorem, conditional only on the explicitly cited established classification and ordinary character-table data. No substantive mathematical gap or counterexample was found.** Its originality is unestablished. Kourovka 21.135 for arbitrary radical-free source groups remains unresolved, and this review supplies no publication authorization or claim of a new solution to that problem.

The theorem audited is: for every nonnegative integer r and every finite group H, equality of the full irreducible complex character-degree multisets of H and A7^r implies H is isomorphic to A7^r.

## Inputs and independence

The audited note is `A7_power_recognition.md`, SHA-256 `b4cd0deac3a951838d09f9ab6bee8e9a01db76062061897e04bee1fcb6af1f12` (10,164 bytes). The note was reread after the author changed the case VIII obstruction to the faithful degree-24 witness and added the named-cover citation clarification requested during this audit. A final status-and-scope synchronization was checked at **2026-10-24 18:20:01 UTC**: the candidate wording now records the restricted mathematical PASS, and the mixed-product and bounded-priority limitations were added. No proof step changed, and the mathematical verdict remains the same.

The reviewer independently read the cached primary Lindsey paper, especially printed pages 771–773, and directly inspected the selected raw ordinary CTblLib source records. The publisher PDF hash is `4f1dfcb2d63f321bed6b92ab89e22529886dc5785f8606a9533ed091c979a9c1`. The author’s parser was not imported or reused. A separate lexical reader in this directory parses ordinary `MOT` records and ordinary-projective `ARC` records, resolves the selected Galois degree references, and checks degree-square sums and class counts. It never reads modular `MBT` records.

A later primary treatment corroborates the cover names: Cheltsov and Shramov, *Six-dimensional exceptional quotient singularities*, arXiv:1001.3863v4, Theorem 3.2 and Remark 1.15; [institutional primary PDF](https://www.pure.ed.ac.uk/ws/portalfiles/portal/17686631/Six_dimensional_exceptional_quotient_singularities.pdf), DOI [10.4310/MRL.2011.v18.n6.a6](https://doi.org/10.4310/MRL.2011.v18.n6.a6). This is useful corroboration of the named central covers; the main classification input remains [Lindsey's Section 3 theorem](https://doi.org/10.4153/CJM-1971-086-x).

## 1. Degree data and quasiprimitivity survive the audit

The nine A7 degrees are exactly those displayed in the candidate. There is one linear character and one degree-six character. In a direct power, a product degree of 6 must have exactly one nonlinear factor, since two nonlinear factors have product at least 36. Hence there are exactly r degree-six characters. The degree-square sum is 2520^r. A group with this multiset is perfect because its abelianization has exactly one linear character.

Every nonunit base degree is the product of two distinct primes from {2,3,5,7}. Multiplication adds prime valuations, so every possible product has even total prime-factor multiplicity and satisfies the four balance inequalities in (M). These conditions need only be necessary. They correctly exclude every listed forbidden degree for every r; there is no finite-r cutoff in that exclusion. The degree-24 and degree-189 exclusions use a valuation imbalance, while degree 20 and degree 63 have odd total multiplicity. All element orders and group orders of a quotient also have no prime factor 11 or 13.

For a degree-six character, passage to its kernel quotient preserves perfection, makes the representation faithful, and permits inflation of every quotient character back to H. The determinant is a one-dimensional character of a perfect group and is therefore trivial. This verifies unimodularity.

The proposed augmentation argument for quasiprimitivity is valid. If the restriction to a normal subgroup has t distinct constituents, Clifford theory makes the conjugation action on them transitive and gives t at most 6. For t greater than 1, the complex permutation module has a nonzero augmentation submodule of dimension t−1 at most 5. Its invariant space is zero because the action is transitive. Complete reducibility then supplies a nontrivial irreducible constituent of degree at most 5, contradicting the inflated degree data. The possible linear constituents cannot escape this contradiction: perfection allows only the trivial linear character, and that character is absent from the augmentation module. Thus t=1 for every normal subgroup, exactly Lindsey’s definition on printed page 772.

This is a deduction of the needed hypothesis, not an assumption that the classification covers all faithful degree-six representations. It also avoids the invalid replacement of ordinary character degrees of a subgroup by those of its overgroup.

## 2. Classification coverage and the tensor cases

Lindsey states the faithful, irreducible, unimodular, quasiprimitive classification across printed pages 772–773. The listed central orders are explicitly for the perfect case, which is precisely the case needed here. The introductory reference to three historical gaps says that they are filled by the cited references, rather than leaving a conditional gap in the stated final theorem. This review treats the classification as an established external theorem, not as a newly reproduced classification proof.

All cases I–XVII have been accounted for. In particular, the potentially easy-to-miss tensor cases do not create an exception:

- In I, the central quotient is a direct product with one factor among A5, A4, S4. A4 and S4 are nontrivial solvable quotients, incompatible with perfection. In the A5 alternative, projection gives an actual A5 quotient of K, so the degree-three obstruction inflates legitimately, irrespective of the other factor.
- In II, the specified ambient products use A4/S4 and Hessian groups. The largest Hessian group is an extension of C3 squared by SL2(3), and is solvable. Its subgroups are solvable as well. Therefore the central quotient, and then its central extension K, are solvable; a nontrivial perfect K cannot occur.
- Wherever an outer involution enlarges the perfect group in the list, a nontrivial cyclic quotient of order two results. Such an enlarged group cannot be perfect. Likewise S5, S7 and PGL2(7) are removed by their nontrivial abelian quotients.

The other eliminations use genuine simple quotients or the explicitly identified central covers, rather than arbitrary subgroups. Case VI has trivial center in the perfect case and leaves A7. Cases VII and VIII are the named triple and sixfold covers, eliminated by ordinary degree 24. The latter witness occurs directly in a faithful central-character sector, so no use of a degree-four quotient witness is required by the final note.

For citation precision, the named-cover identification is part of the external input. An alternative justification is the standard Schur-cover fact that the multiplier of A7 is cyclic of order 6: every perfect central extension is a quotient of its universal central extension, and the unique kernel of each possible order gives 3.A7 and 6.A7. Merely knowing a quotient and an arbitrary center order would not identify central extensions in general. The named-cover restatement cited above prevents that mistaken general inference here.

## 3. Independent ordinary-data checks

The reviewer’s `independent_degree_witnesses.py` checks all nine selected ordinary simple-group tables from raw source files. Each full first column has the stated number of classes and its degree-square sum equals the order stored in the identity centralizer entry.

| Quotient table identifier | Witness checked | Source file |
| --- | ---: | --- |
| A5 | 3 | `ctoalter.tbl` |
| A6 | 5 | `ctoalter.tbl` |
| A7 | 6, uniquely | `ctoalter.tbl` |
| L3(2), isomorphic to PSL2(7) | 3 | `ctoline4.tbl` |
| U4(2), isomorphic to PSp4(3) | 5 | `ctounit3.tbl` |
| U3(3) | 7 | `ctounit2.tbl` |
| U4(3) | 189 | `ctounit1.tbl` |
| J2 | 63 | `ctoconja.tbl` |
| L3(4) | 20 | `ctoline3.tbl` |

The U4(3) witness is particularly important: the degree-189 row is present in the ordinary simple-group table. This audit does not substitute a degree-20 character from a cover or a modular degree. Similarly the J2 degree-63 and L3(4) degree-20 witnesses occur directly in their ordinary simple-group tables.

The raw A7 ordinary-projective sections have degrees:

- central-character order 2: `4,4,14,14,20,20,36`;
- central-character order 3: `6,15,15,21,21,24,24`;
- central-character order 6: `6,6,24,24,36`.

Each sector has square mass 2520. These are projective characters of A7 that become **ordinary** characters of the indicated central covers; they are not modular Brauer characters. The ordinary `ConstructProj` constructors use these same sections. As an additional consistency check, assembling sectors with counts phi(2)=1, phi(3)=2 and phi(6)=2 gives 16, 23 and 40 ordinary characters and degree-square sums 5040, 7560 and 15120 for 2.A7, 3.A7 and 6.A7 respectively. Those counts also agree with the numbers of ordinary conjugacy classes in the constructors. Thus ordinary degree 24 exists in both 3.A7 and 6.A7. Ordinary degree 4 exists in 2.A7 and inflates to 6.A7 as the original version suggested, but the final proof does not need that extra quotient step.

This is independent parsing and consistency checking of established source data. It is not an independent construction of the exceptional groups or a recomputation of their character tables from matrices. The use of those external character tables remains an explicit dependency, as permitted for an established theorem or table.

The checker additionally verifies all nine distinct forbidden numerical degrees against the parity/balance conditions. Its outputs are in `independent_degree_witness_results.json`; every source-file hash and exact table entry line is preserved there.

## 4. Kernel counting and subdirect products

Once each degree-six image is A7, the r degree-six characters have distinct kernels. For a fixed kernel N with quotient A7 there is exactly one quotient irreducible character of degree 6, regardless of the identification of that quotient with A7. Thus two different characters cannot use the same kernel. There is no need to assume that different coordinate choices in an unknown H already have a direct-product interpretation.

The subdirect-product induction is valid for the nonabelian simple group A7. After surjectivity onto the first r−1 factors is established, the image of its kernel in the last factor is normal. If this image is all of A7, the full product is obtained. Otherwise it is trivial and the last map factors through A7^(r−1). A surjection from that direct product to A7 is nontrivial on exactly one direct factor: the factor images are normal and commute, whereas two full images would make A7 abelian. Its nontrivial factor map is an automorphism. Hence the last quotient kernel would coincide with one already listed, contrary to distinctness.

This proves surjectivity onto A7^r, and equality of group orders makes it an isomorphism. The r=0 boundary is immediate from group order 1; the r=1 boundary is included without an additional assumption. Pairwise projection surjectivity alone is not asserted for arbitrary groups; the actual induction and nonabelian simplicity are essential and are used correctly.

## Status after review

The candidate restricted theorem has a complete proof using the named external inputs. There is no outstanding mathematical objection from this audit. The global degree-six classification and the ordinary tables are the substantial established dependencies and should remain cited if this result is recorded elsewhere.

This does **not** make the original Kourovka problem solved: arbitrary radical-free sources can have larger least nonlinear degrees, different simple factors, and socle-permuting extensions. Nor does the proof establish priority for the A7-power statement. A direct-power recognition literature audit is still required before claiming novelty, and even a novel restricted theorem must not be presented as a complete resolution of 21.135.

The final mixed-product examples are correct as statements about the larger family. More precisely, in A5^a times A7^b, degrees 24=4 times 6 and 63=3 times 21 occur whenever a,b are at least 1. Degrees 20=4 times 5 and 189=3 squared times 21 occur when a is at least 2 and b is at least 1. Degree 20 is absent from A5 times A7, so the family-level sentence is not a claim that every individual mixed product has every listed degree. These examples invalidate retaining the same uniform forbidden-degree set throughout an arbitrary mixed-family induction; they do not establish nonrecognition of mixed products.

The final priority wording was checked against `priority/audit.md`. That report records a bounded search with no all-r A7 theorem located, explicitly marks the single-factor theorem as already known, and preserves inaccessible Hawkes 1994 full text as a concrete unchecked lead. Reporting that gap is accurate. This metadata check is not an independent exhaustive literature audit and gives no positive evidence of novelty.
