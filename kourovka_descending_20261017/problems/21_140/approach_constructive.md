# Constructive search for Kourovka 21.140

Research began earlier in this turn; first verified clock checkpoint 2026-10-17 21:26:18 UTC. Final branch checkpoint 21:33:41 UTC.
Discovery estimate at this checkpoint: **8%**. No complete counterexample or general affirmative proof.

## Exact target and independent scope

Construct a single group `G` satisfying simultaneously:

1. `G` is torsion-free;
2. `G` is geometrically of type `F_infinity` (one `K(G,1)` with finitely many cells in each dimension);
3. `cd_Z(G)=infinity`;
4. no abstract subgroup of `G` is isomorphic to standard Thompson `F`.

This branch independently explored amenable/elementary amenable, residual, ascending-HNN, graph-wreath, small-cancellation, and controlled-envelope constructions. Amenability itself is never used to exclude `F`. Varying groups of type `F_n` do not establish the single-group target. All partial constructions below explicitly record their failed hypothesis.

## Valid exclusion mechanisms

**Lemma 1 (residual filter).** Suppose `G` is residually a family of groups none of which contains `F'`. Then `G` contains no `F`.

Proof. If `i:F->G` were injective, choose `1 != x in F'`. A separating homomorphism `q:G->Q` has `(q i)(x)!=1`. Since `F'` is simple, `(q i)|F'` is injective, contradicting the hypothesis on `Q`. This applies to finite and solvable targets, and to finite-integral-cd targets: `F'` contains a copy of `F` supported in a compact dyadic subinterval, so has infinite integral cd. The same argument shows that a group with no `F` has no `F'`, because `F` embeds in `F'`. Conversely `F'` embeds in `F`.

**Lemma 2 (extensions).** The class of groups containing no `F` is closed under extensions and directed unions.

Proof. For `1->N->E->Q->1`, an embedded `F` restricts on its simple subgroup `F'` either injectively into `Q` or trivially; the first case contradicts absence of `F` in `Q`, and the second embeds `F'`, hence `F`, into `N`. For a directed union an embedded `F` lies in a stage because `F` is finitely generated.

These are valid universal embedding obstructions. They do not merely rule out one standard action or one proposed pair of generators.

## A concrete three-generator attempt, and its precise failure

Let `P=direct_sum_{n>=1} Z g_n`, let `K=P * F(a,b)`, and put

`l_n = a^{-n} b a^n`, `m_n = g_n l_n`.

The subgroup `L=<l_1,l_2,...>` is free on the displayed generators (it is part of the usual basis of the kernel of `F(a,b)-><a>`). The subgroup `M=<m_1,m_2,...>` is also free on its displayed generators: the projection `K->F(a,b)` sends `m_n` to the independent `l_n`, so any relation among the `m_n` would project to an impossible free relation. Thus `l_n -> m_n` gives an isomorphism `L->M`.

Form the injective HNN extension

`E = <K,t | t^{-1} l_n t = m_n for all n>=1>`.

Britton normal form embeds `K`, and hence `P`, in `E`. Each `g_n=t^{-1}l_nt l_n^{-1}` belongs to `<a,b,t>`, so `E` is three-generated. It is torsion-free because `K` is torsion-free and every finite-order element of an HNN extension is conjugate into the base. It has infinite integral cd because it contains `Z^r` for every `r`.

It also contains no `F`. Here is a precise external-theorem check rather than an assumption about the particular presentation. Let `HF` denote Kropholler's hierarchy. Each finite-rank subgroup of `P` has finite cd; `P` lies in `HF` by closure under countable directed unions. The hierarchy is closed under free products and HNN extensions, so `E in HF`. The torsion-free `FP_infinity` finite-cd theorem implies `F notin HF`, and `HF` is subgroup closed. Consequently `F` cannot embed in `E`.

**The failed condition is substantially stronger than merely unproved `F_infinity`: `E` is not even `FP_2`.** For the HNN Mayer--Vietoris sequence, `L` is free, and

`H_1(L;Z) -> H_1(K;Z)=P + Z[a] + Z[b]`

sends the basis element `[l_n]` to `[l_n]-[m_n]=-g_n`. This map is injective. Since `H_j(L;Z)=0` for `j>=2`, exactness gives

`H_j(E;Z) = H_j(K;Z) = exterior_power^j(P)` for every `j>=2`,

and `H_1(E;Z)=Z^3`. In particular `H_2(E;Z)` is free abelian of infinite rank. A group of type `FP_2` has finitely generated second integral homology, so `E` fails `FP_2`, hence fails geometric `F_infinity`.

This is a checkable construction meeting torsion-freeness, infinite cd, and universal `F`-absence, with an exact low-dimensional finiteness obstruction. It is **not** a counterexample to 21.140.

## A stronger finitely presented benchmark

`constructive_baumslag_benchmark.md` independently verifies the classical three-generator, three-relator metabelian group `B = Z[x,x^{-1},(1+x)^{-1}] semidirect Z^2`. It is torsion-free, residually finite, finitely presented, infinite-cd, and universally `F`-free. Its rational homology is `H_1=Q^2`, `H_2=Q^2`, and `H_n` is isomorphic as a vector space to a polynomial ring in `n-2` variables for every `n>=3`. In particular it fails `FP_3`. Both the presentation and the full homology calculation passed independent adversarial checks. This demonstrates that the central gap persists after finite presentability, with a direct obstruction rather than merely an unavailable proof of higher finiteness. It is a classical example, and no novelty is claimed.

## Hierarchy obstruction: why routine envelopes cannot finish the construction

Known theorem used: a torsion-free group in `HF` of type `FP_infinity` has finite integral cohomological dimension. `HF` contains every finite-cd group and is closed under subgroups, extensions, countable directed unions, and fundamental groups of graphs of groups.

Therefore any construction remaining within `HF`, starting with finite-cd pieces and using these operations, is blocked for the target. This covers the explicit construction above, elementary amenable constructions, ordinary ascending HNN extensions of finite-cd bases, and attempts to compress a countable union of free abelian groups by adding finitely many stable letters while preserving only the same hierarchy operations.

A particularly sharp consequence: if `1->N->G->Q->1` has `N in HF`, `Q in HF`, `G` torsion-free, and `cd_Z(N)=infinity`, then `G` is not `FP_infinity`. Thus replacing a split wreath product by a nonsplit extension with infinite-rank abelian kernel over a finite-cd quotient does not remove the obstruction.

**Blocked route:** a hypothetical `F`-free finiteness envelope that carries the displayed `E` to a torsion-free `F_infinity` group while retaining its embedding and remaining in `HF` cannot exist. An envelope escaping `HF` and preserving universal `F`-absence needs a materially new mechanism. Stating that such an envelope exists transfers the central difficulty; it is not progress toward a complete proof.

## Graph-wreath program

The original candidate mechanism was `G=A_Gamma semidirect H`, where `A_Gamma` is a right-angled Artin group on an infinite graph, the graph has unbounded clique size, and `H` permutes its vertices. Unbounded cliques would give embedded `Z^r` for every `r`; torsion-free `H` gives torsion-free `G`; extension Lemma 2 gives `F`-absence if `H` has none, because every finitely generated subgroup of `A_Gamma` lies in a finite-graph RAAG of finite cd.

The exact intended finiteness criterion requires one fixed `H` of type `F_infinity`, finitely many orbits in every clique dimension, and appropriate `FP_infinity` stabilizers. A free group's highly transitive countable actions do not automatically have finitely generated stabilizers. Houghton groups furnish arbitrarily high finite finiteness lengths, but that does not supply `F_infinity` and their finite permutation subgroups also violate torsion-freeness.

**No-first-counterexample proposition (independent audit passed).** Use a nonempty graph, a nontrivial uniform vertex group `A`, and an action of `H` by label-preserving vertex permutations. If the resulting graph-wreath product `W=A^Gamma semidirect H` satisfies all four target conditions, then `A` or `H` already satisfies all four target conditions.

Reason. Since `W` is finitely generated, both `A` and `H` are finitely generated and there are finitely many vertex orbits (Kropholler--Martino, Lemma 2.5; alternatively collect the finitely many support vertices and vertex labels in generators). Thus `H` is countable and its finitely many vertex orbits are countable, so the whole graph has countably many vertices. `A` and `H` embed in `W`, so are torsion-free and `F`-free. `H` is a retract. Although `A` need not be a homomorphic retract of all of `W`, it is a coarse retract and therefore inherits every geometric finiteness property `F_n` by Alonso's theorem. If both `A` and `H` had finite cd, every finite graph product of copies of `A` would have finite cd (use finite-dimensional classifying spaces and the standard graph-product polyhedral construction). The countable graph-product base is their directed union, hence is in `HF`; extension closure gives `W in HF`, contradicting infinite cd for torsion-free `FP_infinity` groups. Thus one input already has infinite cd, and all its other required properties have been established.

For completeness, the coarse retraction can be checked without falsely identifying graph-product elements with coordinate functions. Fix a vertex `u`, let `p_u:A^Gamma->A` be the homomorphism killing every vertex group except `A_u`, and set `beta(k,h)=p_u(k)`. Take finite generators for `H` and for copies of `A` at a finite set of vertex-orbit representatives. Right multiplication by a head generator leaves `beta` unchanged. Right multiplication by `a_v` changes it only when `h(v)=u`, then by right multiplication by `a`. Thus `beta` is Lipschitz. The section `a->(a_u,1)` is Lipschitz and `beta` composed with that section is exactly the identity. This proves the required coarse retraction.

The proposition blocks creating a first counterexample by this family. The infinite graph is not itself a source of a new solution when both ingredients have finite cd.

A separate finite-coloring obstruction, explicit bound, independently checked homology computation, and coarse-retraction audit are preserved in `approach_residual_action.md`. No novelty claim is made for these deductions before a dedicated literature comparison.

## Remaining construction families and exact gaps

| Family | Verified mechanism | Exact gap / status |
|---|---|---|
| Elementary amenable / solvable | Automatically no `F`; many torsion-free infinite-cd examples | `FP_infinity` forces a finite-dimensional classifying space; **blocked** |
| Finite-dimensional linear | No `F` by Tits alternative, since `F` is neither virtually solvable nor contains a nonabelian free subgroup | `FP_infinity` linear groups have finite vcd; torsion-free case finite cd; **blocked** |
| Residually solvable or finite | Lemma 1 excludes every embedding of `F` | No constructed single torsion-free `F_infinity` example of infinite cd; residuality alone does not establish higher finiteness |
| RAAG / graph-wreath | Torsion-free, unbounded clique cd witness, universal exclusion via extension | Cannot produce first counterexample from finite-cd ingredients; **blocked in this form** |
| Countable abelian union plus HNN compression | Explicit three-generator `E` above | Infinite-rank `H_2`, so not even `FP_2`; **blocked** |
| Hyperbolic / finite aspherical small cancellation | Strong subgroup controls exclude `F` | Torsion-free hyperbolic and finite-dimensional aspherical outputs have finite cd; **blocked** |
| Infinite graded small cancellation | Can preserve torsion-freeness and exclude `F` in many constructions | No finite-presentation or all-dimensional finiteness proof; replacing this by an unspecified envelope transfers the target difficulty; **blocked absent a new finiteness mechanism** |
| Acyclic / perfect-kernel envelopes | May hide ordinary integral homology obstructions | Acyclicity does not prove `FP_infinity`; within `HF` the finite-cd obstruction still applies; **blocked without a new mechanism** |

## Source map (primary sources)

- Kropholler, Martinez-Perez, Nucinkis, *Cohomological finiteness conditions for elementary amenable groups*, Theorem 1.1. Author PDF: https://eprints.soton.ac.uk/349586/2/KrophollerMartinezNucinkis.pdf . Saved as `sources_constructive/elem_amenable2009.pdf` and extracted text. It implies elementary amenable `FP_infinity` groups virtually have finite classifying spaces.
- Kropholler, *On groups of type (FP)_infinity*, JPAA 90 (1993), 55--67, https://doi.org/10.1016/0022-4049(93)90136-H . Hierarchy closure and finite-cd theorem; also used explicitly in the primary source below.
- Kropholler and Mislin, *Groups acting on finite-dimensional spaces with finite stabilizers*, Comment. Math. Helv. 73 (1998), 122--136, Theorem A. It yields a finite-dimensional proper classifying space for `FP_infinity` groups in `HF`; torsion-free gives finite cd.
- Kropholler and Martino, *Graph-wreath products and finiteness conditions*, https://arxiv.org/abs/1407.0302 , Theorems A--D and Lemma 2.5. Saved as `sources_constructive/graph_wreath2015.pdf` and extracted text.
- Alonso, *Finiteness conditions on groups and quasi-isometries*, JPAA 95 (1994), 121--129, https://doi.org/10.1016/0022-4049(94)90069-8 . Geometric finiteness properties pass to coarse retracts.
- Fournier-Facio, Kropholler, Lyman, Zaremsky, *Finiteness properties of stabilisers of oligomorphic actions*, https://arxiv.org/html/2506.02319v2 . Theorem 1.5 rules out geometric `F_infinity` for infinite-base graph-wreath products over an infinite-dimensional flag complex when the head lies in `HF`; Lemma A.4 gives the coarse retraction used above. Its discussion also identifies the finiteness gap in oligomorphic-action constructions. No current-status conclusion for 21.140 is inferred from this source.
- Cannon--Floyd--Parry, *Introductory notes on Richard Thompson's groups*, Enseign. Math. 42 (1996), 215--256. Simplicity of `F'` and dyadic supported copies used in Lemma 1; parent effort preserves source text in `sources/raw/cannon_floyd_parry_1996.txt`.

## Checkpoint log

- **2026-10-17 21:26:18 UTC — discovery estimate 7%.** Initial constructive screening recorded. Elementary amenable and linear mechanisms blocked. Residual exclusion lemma and graph-wreath stabilizer gap isolated. Independent child assigned residual/action audit. No outside communication, Git, publication, or queue mutation in this branch.
- **2026-10-17 21:28:36 UTC — discovery estimate 8%.** Explicit three-generator torsion-free, infinite-cd, `F`-free HNN construction derived. Mayer--Vietoris proves it fails `FP_2`. Graph-wreath first-counterexample inheritance argument isolated.
- **2026-10-17 21:33:41 UTC — discovery estimate 8%.** Independent and fresh adversarial checks pass the HNN construction and graph-wreath obstruction. Added the label-preserving-action hypothesis, finite-generation preliminaries, and countability explicitly. A stronger classical finitely presented Baumslag benchmark is fully verified in `constructive_baumslag_benchmark.md`: it is TF/RF/metabelian, infinite-cd and `F`-free, but its explicitly computed rational `H_3` has infinite rank, so it fails `FP_3`. Two adversaries pass its complete derivation. No novelty or solved-status claim. Strongest conclusion is a collection of construction obstructions and rigorously rejected three-of-four candidates.
