# Independent adversarial audit of construction exclusions for 21.135

Audit checkpoint: 2026-10-24, 18:09 UTC. Completion estimate for this assigned
audit: 100%; the separate exact-file addendum on the strengthened wreath
statement has also passed. Completion of Kourovka 21.135 itself is **not**
claimed.

## Reviewed scope and exact files

The target is a pair of finite groups with identical multisets of ordinary
complex irreducible character degrees, one with trivial solvable radical and
one with nontrivial solvable radical. The author notes claim only specified
construction exclusions and a bounded library search.

Reviewed author files, with SHA-256 at the time of inspection:

- `approach_constructions.md`:
  `e3512f4f76144e3b8641720cde509280f5e44fce331ca0d936b1360d02fda6bd`.
- `scan_library.g`:
  `02ba25ff7f13ccfe26c8f1301247f94f7f0aa5683da5b43b0ff79dacf3566fa6`.
- `product_scan.py`:
  `451be0b25a52b62f3b538907460eea5fd0602767ca45000093e0bc7f16f58b3a`.
- `../root_wreath_injectivity.md`:
  `3ecf14984d7e31253c97a2f848aed3cc89850d2b895bab7d4fe165d3a6515ccb`.

No author file was edited. A separate child reviewer independently inspected
Sections 2–3; its report is `wreath_proof_independent.md`. The strengthened
general-action statement then passed an additional exact-file audit,
`wreath_general_injectivity_addendum.md`, SHA-256
`18cea0aab03de6a08f2ef726b008f7744ed7e4994e6d560281724ff9f66ac19c`.

## Theoretical verdict

No substantive mathematical error was found in the reviewed construction
exclusions. This is a proof audit of those statements, not an originality
finding and not a resolution of 21.135.

1. **Direct-product cancellation.** The finite Dirichlet-polynomial uniqueness
   argument is correct: after multiplication by the least differing degree
   to the power `s`, the limit as `s` tends to positive infinity is the first
   nonzero coefficient. The common factor is positive on the real axis.
   The solvable-radical product formula follows from projections of normal
   solvable subgroups and the normal solvability of the product of radicals.

2. **Prime-cyclic wreath formula and injectivity.** A prime coordinate cycle
   has constant-tuple orbits of length one and every other orbit has length
   `p`. The constant tensor representation has an actual extension obtained
   by cyclic tensor permutation. Its `p` extensions and the nonconstant
   induced characters give the stated polynomial formula. In the difference
   identity, `z Q(s)` and `p^2-z` are positive for positive `s`, while both
   nonzero differences have the same eventual sign. The contradiction is
   valid. For `p=2`, coincident constant and induced output degrees are added,
   not distinguished. For the trivial base, the output is `C_p`, and the
   formula still applies.

3. **Radical preservation.** If a nontrivial finite base `X` has trivial
   solvable radical, every minimal normal subgroup is a product of
   nonabelian simple groups. Their product `S` is centerless and has trivial
   centralizer in `X`: a nontrivial normal centralizer would contain a
   minimal normal subgroup lying in `S` and its center. For a faithful
   permutation action, the centralizer of `S^Omega` in the wreath product is
   trivial. A solvable normal subgroup intersects that direct product
   trivially and therefore centralizes it, so is trivial. This proof does
   not require transitivity. Conversely `R(X)^Omega` is nontrivial solvable
   normal when `R(X)>1` and `Omega` is nonempty. The root note's alternative
   argument with the centerless whole base is also correct. Nontriviality of
   the base and faithfulness are appropriately retained for this radical
   assertion, whereas degree recovery does not require them.

4. **Ordinary tensor extensions and class counting.** Fix a representation
   model for each base character label. Stabilizing coordinate permutations
   permute equal chosen tensor spaces and compose exactly. Thus these are
   genuine linear extensions, and the multiplicity representations of the
   tuple stabilizer are ordinary representations, not projective ones.
   Clifford theory then gives exactly `k(P_f)` irreducibles per label orbit.
   Enlarging the color set preserves every old orbit and stabilizer and
   adds a new constant orbit. Strict monotonicity therefore holds for a
   nonempty coordinate set. The nonempty qualification should be stated
   explicitly in Section 3 if that section is intended to stand alone;
   Section 2 already imposes it. For empty `Omega`, the output is `P`
   independently of the base. This is an editorial qualification, not a
   substantive objection under the existing convention. The conditional
   partial-coordinate replacement sentence is valid when the changed
   coordinate collection is nonempty and invariant, as stipulated by its
   ordinary permutation-action scope.

## Strengthened fixed-action degree recovery

The exact root note was read in full. Its generalization from prime cycles to
every fixed finite action on nonempty `Omega` is sound.

Let `m0` be the smallest coordinate-orbit size. The number of output linear
characters is `ell_X^c ell_P`, where `c>=1` is the number of coordinate
orbits, so the base number of linear characters is determined. If a tuple
uses a degree `e>=2` in one coordinate orbit, let `S` be all its positions in
that orbit with degrees at least `e`, and set `a=|S|`. The tuple stabilizer
preserves `S`. Its `t` cosets yield at most `t` translates of `S`, and their
union is that entire coordinate orbit. Repetitions do not hurt the bound
`ta >= |Omega_j| >= m0`. The output degree is at least
`t e^a >= t a e >= m0 e`, since `e^(a-1)>=a` for `e>=2` and `a>=1`.

At the first different base degree `d>=2`, orient the bases so the second has
more labels of that degree. Embed the smaller label collection of degrees
at most `d` into the larger, preserving degrees and identifying the trivial
characters. Equality patterns, stabilizers, orbit lengths, tuple products,
and stabilizer-character multiplicities remain identical under that
embedding. All output degrees at most `m0 d` depend only on those truncated
label collections. A new degree-`d` label at one point of a smallest
coordinate orbit, with trivial characters elsewhere, has orbit length
exactly `m0`; the stabilizer's trivial character produces a new output
character of degree `m0 d`. This orbit is not an old orbit, so the
multiplicity at that degree strictly increases. Labels of greater degree
cannot cancel the difference by the preceding lower bound.

The proof also covers singleton coordinate orbits, the trivial base, trivial
top actions, and nonfaithful actions. Empty `Omega` is correctly excluded.
The note does not assert reconstruction of base-group isomorphism or
recognition of arbitrary groups with the same wreath spectrum. No claim of
novelty is justified by this proof check alone.

## Independent finite computation

The author's input contains 2,157 ordinary CTblLib rows of order at most
`10^8`. The independent GAP script `independent_library_check.g` enumerated
all 2,678 table names in reverse order, extracted each degree list from
`Collected(List(Irr(table), chi -> chi[1]))`, independently checked the
degree-square sum, and summed class sizes over the radical positions.
The process exited with status zero and logged
`INDEPENDENT_COMPLETE 2678 names, 2157 retained rows`. Every complete retained
row agrees with the author input when matched by table name. Evidence:
`independent_library_comparison.json` and the independent scan/log files.

The independent scan uses the same trusted GAP attribute
`ClassPositionsOfSolvableRadical`. Its implementation in
`tools/gap-4.16.1/lib/ctbl.gi` was also inspected. It uses the full-table
normal-subgroup lattice and constructs a normal chain with prime-power
quotients. Each chain term is solvable. If it stopped strictly below the
radical, a minimal normal subgroup of the ambient quotient inside the
remaining solvable radical would supply a further elementary-abelian
quotient, a contradiction. Thus this computation is not an inference from
degree multisets alone. The independent rerun does not establish formal
correctness of GAP or independently reconstruct CTblLib from groups.

The independent Python checker imports none of the author code and uses a
different necessary prefilter: only group order, class count, and number of
linear characters. Every surviving pair is compared by the full integer
degree-multiplicity convolution. It obtained:

- 1,717 distinct degree multisets, including the explicit trivial group;
- 218 radical-free multisets;
- 15,441 radical-free unordered two-factor pairs of order at most `10^12`;
- 1,237,165 unordered two-factor pairs with nontrivial radical in that bound;
- 408 nontrivial-radical pairs surviving the weaker prefilter;
- 443 full exact cross-radical spectrum comparisons;
- no equal spectra across the radical distinction.

These pair counts match the author scan. The author's additional fingerprint
components are all necessary multiplicative invariants of a spectrum, so
their zero-candidate result is also logically sufficient within its scope.
Our weaker filter forced actual full multiset comparisons and independently
reproduced the absence of a collision.

Input SHA-256:
`62e62d56cdc2cfd0ef3a72127b54a0107110614ee9ea29131d3f22c434cbbe3c`.
The independent reversed input file has a different byte order, SHA-256
`ff1439ef3ebda9454a7ff9eea969368de2cd781e7dea6a470a527ff17b473309`;
row-by-name equality, rather than byte equality, is the relevant check.

Run from the construction directory:

```
python3 adversary/independent_product_check.py
tools/gap-4.16.1/gap -q --bare --quitonbreak adversary/independent_library_check.g
python3 adversary/compare_library_inputs.py
```

The GAP output path is relative to that working directory. Package warnings
about optional unavailable group libraries occurred, as in the author's
scan; the completed scripts used the ordinary character-table operations
and reported no execution error.

## Remaining gap

None of these computations exhausts finite groups up to either order bound.
The product search examines at most two representatives from the specified
library spectra, with a trivial factor allowing single tables. It does not
test arbitrary group extensions, distinct wreath tops/actions, products
with arbitrarily many unlisted factors, or all groups sharing a listed
spectrum. The construction exclusions therefore cannot be promoted to a
general radical-recognition theorem. There is no target counterexample,
complete resolution, originality conclusion, publication approval, human
peer-review claim, or formal-verification claim in this audit.
