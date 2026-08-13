# Hostile exact-byte audit of the two-linkage composition

**Audit date:** 2026-08-12 PDT.  
**Method:** proof-first composition audit.  Finite computation was used only
for support, tier, affine-subspace, and set-membership identities.  No
reaction orientation, stochastic history, rate vector, or population box was
enumerated to prove a stochastic estimate.

## 1. Frozen target and verdict

The target is frozen at

```text
41fbb5b2b64fccbc5576bc06c9d8d81657b452d930757568909f85a207255052
    research_notes/proof_first_two_linkage_at_most_three_species_theorem.md
```

It has 284 lines and 13,721 bytes.

**Final verdict: STRICT FAIL as a proof of Theorem 1.1.**  The failure is a
single load-bearing composition gap in target lines 116--139: the
both-linkages-available part of the raw two-active support atlas is assigned
an “all-clock access episode,” but no theorem proves a negative drift-cost
estimate for that episode or charges the reaction which activates it.  The
target therefore does not establish that every reduced two-linkage support
pair reaches the 4,761/408 shielded/available input table.

This is a proof-interface failure, not a stochastic counterexample.  No
counterexample to recurrence was found.

The following narrower results retain strict pass status.

| audited component | disposition |
|---|---|
| fixed-class projection, dormant-linkage deletion, linkage merging, and zero-displacement deletion | **STRICT PASS** |
| binary-network nonexplosion | **STRICT PASS** |
| corrected S-tier-superlevel cut and affine151 implication | **STRICT PASS** |
| three literal pre-residual physical seams | **STRICT PASS at their exact supports** |
| disjoint equality of the fourteen rows with the stated 2,511-pair input set | **STRICT PASS as a finite set identity** |
| all fourteen standalone pair-recurrence theorems | **STRICT PASS at their audited row scopes** |
| no cross-row potential comparison and the marked-to-physical conclusion inside those standalone theorems | **STRICT PASS** |
| claim that Sections 3--5 exhaust every reduced two-linkage pair | **FAIL** |
| Theorem 1.1 at the frozen bytes | **STRICT FAIL** |

In particular, this audit does **not** revoke the 2,511-pair union, any of its
fourteen row theorems, or any exact-byte row audit.  The missing supports lie
upstream of that union.

## 2. What the exact projection does prove

If coordinate $i$ is constant on a closed irreducible class $\Gamma$, an
enabled reaction has zero $i$-increment.  From one enabled source, a
directed path through its strong linkage is the literal population path with
one fixed residual population.  Hence the deleted stoichiometry is constant
throughout that active linkage and its falling-factorial contribution is one
fixed positive rate factor.  Deleting constant coordinates is therefore a
generator conjugacy on $\Gamma$.

A dormant linkage has identically zero propensity and may be deleted before
projection.  Projected strong linkages sharing a vertex have strong union;
parallel labelled propensities add.  A projected zero-displacement label has
no off-diagonal generator entry and may be discarded.  A surviving active
projected linkage consequently has at least two distinct vertices.  These
arguments validate target Sections 1--2.

For nonexplosion, a population-increasing binary reaction has source degree
at most one.  Its aggregate increasing intensity is $O(1+|x|_1)$, while
all jumps are bounded.  Finite-population localization and Gronwall exclude
population escape in finite time.  On a fixed population sublevel there are
finitely many states and a finite maximum total rate, so neutral quadratic
clocks cannot accumulate.  This part also passes.

## 3. Exact raw support universe and the omitted stratum

Fix active coordinates $A,B$ and bounded coordinate $C$.  An ordered raw
support assignment sends each of the ten binary complexes to linkage one,
linkage two, or neither, with both linkage supports having size at least two.
Its exact cardinality is

$$
 3^{10}-2\{2^{10}+10\,2^9\}
 +\{1+10+10+10\cdot9\}=46{,}872.                 \tag{3.1}
$$

Across the four workload representatives

$$
 (1,1,0),\quad(2,3,0),\quad(1,2,0),\quad(1,3,0),             \tag{3.2}
$$

there are $4\cdot46{,}872=187{,}488$ ordered pair--workload
incidences.  The exact inherited top classifier splits them as follows.

| linkage-one status / linkage-two status | incidences |
|---|---:|
| available / available | 163,612 |
| available / shielded | 11,715 |
| shielded / available | 11,715 |
| shielded / shielded | 446 |

The 4,761 positive-shield and 408 signed-shield support pairs in target
(3.2) are deduplicated **one-shielded/one-available** interfaces.  The 446
both-shielded incidences have the exact invariant/deficiency/service atlas.
The 163,612 both-available incidences are not an input to (3.2).

This omission would be harmless if a separate analytic theorem disposed of
every available-linkage chart before the shielded/available table.  The
frozen target instead says only that an accessible path “gives an all-clock
access episode” and that the episode has an actual endpoint.  Those facts do
not imply any of

$$
 \mathbb E_x\!\left[W(X_\tau)-W(x)+\eta\tau\right]\le-\delta,
 \qquad
 \mathbb E_x\tau<\infty,                                  \tag{3.3}
$$

for one proper potential with uniform positive constants.  They also do not
charge the possibly rare or workload-increasing reaction which first makes
the prescribed source available.

The exact finite implementation confirms the scope boundary: its
`chart_instances` routine is parametrized by a shielded mask and explicitly
requires the other linkage to be nonshielded.  It proves the 4,761/408 set
identity but supplies no branch for an available/available pair.

## 4. Symbolic availability families

Let $T_h(L)$ be the top set of linkage $L$ for
$h=(h_A,h_B,0)$.  The exact top classifier has three nonshielded
mechanisms after excluding the flat case $T_h(L)=L$:

* **Q (quadratic top):** $T_h(L)$ contains a complex with two active
  particles;
* **U (unary top):** after the exact one-particle flat test fails,
  $T_h(L)$ contains a unary complex;
* **C (cofactor carrier):** a top mixed complex uses the bounded cofactor
  $C$, and a lower complex in the same linkage also uses $C$.

After removing strict positive invariants, positive-$A,B$ invariants,
deficiency zero, the three literal seams, corrected tier passes, affine-
infeasible failures, and every symmetry image of the fourteen-row union,
the minimal omitted six-complex incidence library has exactly five
nonempty availability-type families:

$$
        U\text{--}U,\qquad Q\text{--}U,\qquad
        C\text{--}U,\qquad C\text{--}Q,\qquad
        C\text{--}C.                                      \tag{4.1}
$$

The corresponding ordered descriptor-incidence counts at total support size
six are $120,80,112,4,16$, respectively.  A $Q$--$Q$ family does not
survive these filters.  These numbers are finite support identities only;
the analytic significance of (4.1) is that the missing theorem must handle
enabled unary starts, enabled quadratic starts, and activation of disabled
cofactor carriers, including every mixed pairing among them.

## 5. Five minimal omitted witnesses

All five rows below use cap $c=(2,2,0)$, so $C=0$, and each support has
three complexes.  Here $E$ is the top S-tier and $U_1,U_2$ are the
correct D-superlevels at the D-level occupied by $E$.

* **C--C:** $L_1=\{0,C,A+C\}$, $L_2=\{2A,2C,B+C\}$,
  $h=(1,3,0)$, top D-tier $\{B+C\}$, $E=\{2A\}$, and
  $(U_1,U_2)=(\varnothing,\{2A,B+C\})$.

* **C--Q:** $L_1=\{0,C,B+C\}$, $L_2=\{2B,2C,A+C\}$,
  $h=(2,1,0)$, top D-tier $\{2B,A+C\}$, $E=\{2B\}$, and
  $(U_1,U_2)=(\varnothing,\{2B,A+C\})$.

* **C--U:** $L_1=\{0,2C,A+C\}$, $L_2=\{B,C,B+C\}$,
  $h=(1,1,0)$, top D-tier $\{B,A+C,B+C\}$, $E=\{B\}$, and
  $(U_1,U_2)=(\{A+C\},\{B,B+C\})$.

* **Q--U:** $L_1=\{0,2A,2C\}$, $L_2=\{B,C,B+C\}$,
  $h=(1,3,0)$, top D-tier $\{B,B+C\}$, $E=\{B\}$, and
  $(U_1,U_2)=(\varnothing,\{B,B+C\})$.

* **U--U:** $L_1=\{0,A,A+C\}$, $L_2=\{B,2C,B+C\}$,
  $h=(1,1,0)$, top D-tier $\{A,B,A+C,B+C\}$,
  $E=\{A,B\}$, and
  $(U_1,U_2)=(\{A,A+C\},\{B,B+C\})$.

For every row:

1. the supports are disjoint and both linkages are available under the exact
   classifier;
2. there is no strictly positive invariant and no invariant positive on
   $A,B$;
3. the full stoichiometric rank is three and the deficiency is one;
4. the pair is not one of the three literal seams, even after species
   permutation and linkage exchange;
5. the displayed failed descriptor is affine feasible (indeed the
   stoichiometric subspace is all of $\mathbb R^3$); and
6. no species/linkage symmetry image belongs to the fourteen-row 2,511-pair
   union.

Thus none is removed by target items 1--5 or Table 1.  The exact one-pair
fingerprints, in table order, are

```text
3868727e3e6a76d340d2b73ab86cbaba2b2e65252e9299c54bfc34500ec00e7a
5f83af601386b26ba692ce6ca1e178ed2cb1b6cf0a19e05b2bb0dec8758ff59a
8d06d0a6c25c9c66067b0754a77ac55594ee5e8efa01d94413d9fa910719cefa
c6dde5288b5638a9ac752a2b3a0254eab720cc1f4e2b332ccb188571e9b92e8a
3277bb458c026d81e47333d8dfb539dbb1570ba475d467b1590c620d00967c7a
```

The failure of the corrected tier condition is symbolic, not an orientation
search.  The Hamiltonian cycles

```text
C-C:  0 -> C -> A+C -> 0       ; 2A -> B+C -> 2C -> 2A
C-Q:  0 -> C -> B+C -> 0       ; 2B -> A+C -> 2C -> 2B
C-U:  A+C -> 0 -> 2C -> A+C   ; B -> B+C -> C -> B
Q-U:  0 -> 2A -> 2C -> 0      ; B -> B+C -> C -> B
U-U:  A -> A+C -> 0 -> A      ; B -> B+C -> 2C -> B
```

are strongly connected and have no D-descending edge sourced in $E$.
They are exactly the necessity construction for the corrected superlevel
cut: the sole exit from each nontrivial $U_i$ is sourced at a disabled
vertex in $U_i\mathbin{\backslash}E$.  The integer sequences
$(n^{h_A},n^{h_B},0)$ realize the displayed D-order and caps in the
full-dimensional stoichiometric affine class.  This demonstrates failure of
the cited tier route, not nonrecurrence of these networks.

## 6. Why the enabled-181 access word does not close the seam

The exact local access-word theorem is

```text
9be70e2b6c9ce5c4762bf3130246f1ea660bea73f41aa7abdd997853cc0a6b04
    research_notes/proof_first_hard_enabled181_access_word.md
4028c026a7d01c1e0930bdbdaa75216a79402078999d6450c283a77eb2a04883
    research_notes/proof_first_hard_enabled181_access_word_independent_audit.md
```

It is valid when an enabled first source already lies at the common top
scale, and it proves a bounded post-source word estimate through the first
competitor.  This can treat some Q--U or U--U local starts.  It cannot serve
as the missing atlas theorem:

* in C--C and some C--U charts the relevant top source is disabled, so the
  enabled-seed hypothesis fails;
* it does not wait for or charge a rare activating reaction;
* it does not include the workload cost of that activating jump;
* it does not compare the activation rate with arbitrarily faster clocks of
  the other linkage; and
* its certified finite scope is 181 hard-family incidences, while the target
  invokes an arbitrary available linkage before the 2,511-pair selector.

Even where its hypotheses hold locally, a full pair theorem still needs a
statewise common-potential cover, uniform constants, physical duration and
actual-endpoint integrability, and nonoverlapping concatenation of repeated
starts.  The local access word expressly makes no pair-recurrence claim.

## 7. The previously recorded activation obstruction

The inherited final-certification audit is frozen at

```text
0e7607effd5150838a08a33895e31641c9c0bb8718a39c32b17bbc791573e690
    inherited/workload_reactivation_candidate/inherited/final_certification_hard_stop/proof_audit.md
```

Its Gate G3 rejects the same missing implication.  On the exact cycle

$$
                         0\longrightarrow2A\longrightarrow A\longrightarrow0,
$$

conditioning on activation removes the source-probability factor and makes
the proposed conditioned payoff positive and tending to zero, rather than
coercively negative.  A current-target episode begun after an actual linkage
reaction remains useful, but the activation reaction and intervening
waiting must be charged without overlap.

The smallest repair was already isolated at

```text
c04f65cd2d10f374725e7f56b67579faac0b7ff2ac72f04552ac7a8c3dd214ed
    inherited/workload_reactivation_candidate/inherited/final_certification_hard_stop/source_layer_activation_remaining.md
```

and has not been superseded by any dependency cited in the frozen target.

## 8. Exact repair gate

To turn the target into a theorem, one must prove a **rate-weighted
current-target charging theorem** for every Q, U, and C available-linkage
type.  For a fixed pair, orientation, rates, and closed class, it must form a
nonoverlapping physical path partition containing

1. the actual reaction which activates or launches the available linkage;
2. the complete current-target episode begun at that actual target;
3. every intervening reaction of the other linkage; and
4. every chart, workload, support, and finite-target exit.

With one proper pair-fixed potential, the theorem must prove one of:

* a uniform physical-time drift-cost inequality of the form (3.3), including
  actual endpoints and the moments needed for gluing;
* a positive normalized structural-exit flux which is charged by another
  already proved region using the same potential;
* an exact affine invariant positive on the escape cone; or
* reduction to a literal already audited support theorem.

It must remain valid when the available linkage is rare, its first reaction
is workload-increasing, the other linkage makes arbitrarily many faster
neutral jumps, the activation probability vanishes with population, and the
inactive-coordinate cap grows along the escaping object.  No reaction may be
counted both as one episode's terminal interruption and the next episode's
uncharged activation.

After this theorem is proved, a repaired composition must explicitly show
that every raw support/workload chart either enters that theorem or reduces
to the shielded/available and both-shielded atlases.  Only then may the
already valid 2,511-pair union be invoked.

## 9. Durable disposition

The exact target's projection, nonexplosion, corrected cut, affine151
branch, literal physical seams, fourteen-row finite union, fourteen
standalone recurrence theorems, internal workload handoffs, and
marked-to-physical conclusions all survive hostile replay at their stated
scopes.

The sentence that an accessible path merely “gives an all-clock access
episode” is not a recurrence theorem.  Because the rate-weighted activation
and current-target charge is missing, the frozen target does not exhaust the
raw two-linkage universe.  Theorem 1.1 therefore receives **STRICT FAIL** at
SHA-256 `41fbb5b2...`, pending the exact repair gate in Section 8.

## 10. Render verification

The exact audit Markdown was converted independently with Pandoc and compiled
with Tectonic at 10-point type and 0.8-inch margins.  The result is five
pages.  The compiler reported no TeX error, missing glyph, overfull box, or
other warning.  A separate standalone HTML/MathJax conversion also passed.
