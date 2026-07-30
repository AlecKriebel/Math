# Proof dependency graph

## End-to-end graph

```text
Operational definitions
  ├─ local quantum dimension ≤ 2 on every branch
  ├─ zero projectors allowed
  ├─ shared randomness / convexification
  └─ stochastic PVM postprocessing reduces to deterministic maps
       │
       ├─────────────────────────────────────────────────────────────┐
       │                                                             │
       ▼                                                             ▼
D1: exact rational 3×2 separation                    Two-setting reduction
  ├─ explicit simple POVM strategy                     ├─ binary POVM spectral decomposition
  │    └─ L0 = 20√2 + 16/25                            │
  ├─ strengthened algebraic strategy                   ▼
  │    └─ L1 = (16 + 8√7813)/25                  D2: one-binary-party theorem
  ├─ pure-state / Schmidt reduction                    ├─ 3D Lorentz-cone compression
  ├─ exhaustive ternary-PVM rank patterns              ├─ minimal positive circuits
  ├─ CHSH deficit bounds                               ├─ every nontrivial circuit is 2-vs-2
  ├─ robust auxiliary discrimination bound             └─ canonical-purification PVM lift
  ├─ complete-square PVM upper bound                         │
  │    └─ U = 20√2 + 3/5 + (4+3√2)/250                      ▼
  └─ L0 > U and L1 > U                           D3: residual architecture theorem
       │                                                ├─ maximizing extreme behavior
       │                                                ├─ pure entangled state
       │                                                ├─ extremal local POVMs
       │                                                ├─ common-span filtering
       │                                                ├─ V0 ∩ V1 = RI
       │                                                ├─ one span has dimension 2
       │                                                ├─ D2 excludes two binary inputs
       │                                                └─ other input is ternary rank one
       │                                                     │
       │                                                     ▼
       │                                          Residual (2,3)-by-(2,3) strategy
       │                                                     │
       │                                                     ▼
       │                                          Global strict-separator reduction
       │                                            ├─ compact nearest-point separation
       │                                            └─ D3 maximizer is a full POVM maximizer
       │                                                     │
       │                                                     ▼
       │                                          Lorentz incidence model
       │                                            ├─ five local null rays
       │                                            ├─ four-parameter metric g
       │                                            ├─ Pᵀg⁻¹P conformal Lorentz relation
       │                                            ├─ five equations Fj=0
       │                                            └─ local physical completeness
       │                                                     │
       │                                                     ▼
       │                                          Strict KKT multiplier theorem
       │                                            ├─ finite POVM duality
       │                                            ├─ dual slack = determinant multiplier
       │                                            ├─ zero slack gives deterministic tie
       │                                            └─ λj>0, hence Λ>0
       │                                                     │
       │                         ┌───────────────────────────┼──────────────────────────┐
       │                         │                           │                          │
       │                         ▼                           ▼                          ▼
       │                 rank(D) ≥ 2                  rank(D) = 1                rank(D) = 0
       │                   ├─ square completion         ├─ quadratic-map           ├─ base-ray pentad
       │                   ├─ inertia (4,12)            │  injectivity              │  permutation
       │                   ├─ compatible dim ≥13        ├─ one nonzero row          ├─ equal scaling
       │                   └─ physical uphill curve     └─ no λ>0 in kernel         └─ local transport
       │                         │                           │                          │
       │                         └───────────────┬───────────┴──────────────────────────┘
       │                                         ▼
       │                              No strict residual separator
       │                                         │
       │                                         ▼
       │                    conv Q₂^POVM(2,2) = conv Q₂^PVM(2,2)
       │                                         │
       └─────────────────────────────┬───────────┘
                                     ▼
                    Minimum setting architecture = 3×2
                         (up to exchanging the parties)
```

## Dependency inventory

| ID | Result | Direct dependencies | Frozen source | Status |
|---|---|---|---|---|
| O1 | Operational fixed-qubit model | none | Phase-I §1 | PASS after definition repair |
| D1.1 | Simple exact POVM value \(L_0\) | O1 | Phase-I §3; simple strategy JSON | PASS |
| D1.2 | Strengthened value \(L_1\) | O1 | Phase-I §4; strengthened strategy JSON | PASS |
| D1.3 | Global PVM upper bound \(U\) | O1, state reduction, PVM rank patterns, deficit estimates | Phase-I §§5–8 | PASS |
| D1 | Strict rational \(3\times2\) separation | D1.1 or D1.2, D1.3 | Phase-I Theorem 2.1 | PASS |
| L1 | Square-root locking theorem | complete-square identity | Phase-I §9 | PASS; explanatory, not needed once D1 is proved directly |
| D2.1 | Binary qubit POVM decomposition | spectral theorem | Phase-I Theorem 10.1, opening | PASS |
| D2.2 | Lorentz-cone circuit decomposition | D2.1, cone extremality, Carathéodory circuit bound | Phase-I Theorem 10.1 | PASS after exposition repair |
| D2.3 | PVM lift of a \(2\)-vs-\(2\) circuit | canonical purification | Phase-I Theorem 10.1 | PASS |
| D2 | One-binary-party simulation | D2.1–D2.3 | Phase-I Theorem 10.1 | PASS |
| D3.1 | Pure entangled extreme realization | compactness, behavior extremality | Phase-I Theorem 10.3 | PASS |
| D3.2 | Common-span filtering | Lemma 10.2, full-rank marginal | Phase-I Lemma 10.2 | PASS after zero-effect clarification |
| D3.3 | Span and rank classification | D3.2, dimension inequality, POVM support perturbations | Phase-I Theorem 10.3 | PASS |
| D3 | Residual architecture | D2, D3.1–D3.3 | Phase-I Theorem 10.3 | PASS |
| C1 | Strict residual global maximizer | compact separation, D3 | Closure §2 | PASS |
| C2 | Lorentz incidence model | D3, qubit determinant identity, pure-state steering | Closure §§3–6 | PASS |
| C3 | Positive determinant multipliers | C1–C2, local POVM duality | Closure §7 | PASS after proof-bridge repair |
| C4 | Rank-\(\ge2\) obstruction | C2–C3, square completion, inertia | Closure §§8–10 | PASS |
| C5 | Rank-\(1\) obstruction | C2–C3, projective injectivity of \(\Phi\) | Closure §§11–12 | PASS after exceptional-subcase repair |
| C6 | Rank-\(0\) local decomposition | C2, base-locus classification, transport lemma | Closure §13 | PASS |
| E1 | Universal two-setting equality | C1–C6 | Closure §14 | PASS |
| E2 | Minimum setting classification | E1, D1, one-input locality | Closure §15 | PASS |

## D1 internal chain

The global projective comparison is not a finite numerical search. Its exact
logical chain is

\[
\begin{aligned}
\text{arbitrary PVM strategy}
&\longrightarrow \text{one pure Schmidt state}\\
&\longrightarrow
 \begin{cases}
 \text{degenerate CHSH observable},\\
 \text{four nondegenerate Bloch observables}
 \end{cases}\\
&\longrightarrow
\delta=2\sqrt2-S,\quad
\eta\le2^{1/4}\sqrt\delta,\quad
u\le2^{3/4}\sqrt\delta\\
&\longrightarrow
T\le\frac35+\frac25(\eta+u)
\le\frac35+C\sqrt\delta\\
&\longrightarrow
10S+T\le20\sqrt2+\frac35+\frac{C^2}{40}=U.
\end{aligned}
\]

Every displayed output-support pattern is included because a three-label PVM
on a qubit has rank partition either a permutation of \((2,0,0)\) or of
\((1,1,0)\).

## D2 internal chain

For fixed binary PVMs \(B_0,B_1\), the map

\[
\Phi(\sigma)=
(\operatorname{Tr}\sigma,\operatorname{Tr}\sigma B_0,
\operatorname{Tr}\sigma B_1)
\]

determines every observed probability. Its positive image is a Lorentz cone, a
two-dimensional simplicial degeneration, or a deterministic degeneration.
No-signaling gives one positive relation between the two lists of compressed
steered states. Extreme-ray expansion and minimal-circuit elimination reduce
that relation to one-versus-one or two-versus-two pieces. Each two-versus-two
piece lifts to two rank-one decompositions of the same qubit operator and hence
to two PVMs on one canonical purification. Common shared randomness over the
pieces reconstructs the entire behavior.

## D3 internal chain

At a strict full-POVM maximum above the PVM value:

1. choose an extreme behavior in the maximizing face;
2. choose one unrandomized realization;
3. decompose the state and measurements, using behavior extremality to retain a
   pure entangled state and extremal POVMs;
4. apply common-span filtering to prove
   \(V_0\cap V_1=\mathbb RI\) on each party;
5. use
   \[
   \dim(V_0\cap V_1)\ge\dim V_0+\dim V_1-4
   \]
   to force one measurement span to have dimension at most two;
6. replace that measurement by a behavior-preserving deterministic
   postprocessing of a binary spectral PVM;
7. use D2 to rule out both inputs being binary on either party;
8. use linear independence and
   \(\sum_a\operatorname{rank}(M_a)^2\le4\) to identify the other measurement as
   a ternary rank-one extremal POVM.

## Closure internal chain

The residual behavior is encoded by a probability block \(P\), a local
Lorentz metric \(g\), and five null constraints

\[
F_j(P,g)=(Pr_j)^Tg^{-1}(Pr_j)=0.
\]

Local reconstruction proves that the incidence equations are not an algebraic
relaxation. At a putative strict Bell maximum, local POVM duality identifies the
five determinant multipliers and makes them strictly positive. Thus

\[
\Lambda=\sum_j\lambda_jr_jr_j^T>0.
\]

For

\[
\delta P=PW+Hg^{-1}P,\qquad
S=P^Tg^{-1}P,
\]

the weighted constrained second variation is

\[
2q(W),\qquad q(W)=\operatorname{Tr}(SW\Lambda W^T),
\]

and \(q\) has inertia \((4,12)\).

- If \(\operatorname{rank}\mathcal D\ge2\), the compatible \(W\)-space has
  dimension at least \(13\), so it contains \(q(W)>0\), contradicting local
  maximality.
- If \(\operatorname{rank}\mathcal D=1\), projective injectivity of the null-ray
  quadratic map leaves exactly one nonzero row, so
  \(\ker\mathcal D^T\) has no strictly positive vector.
- If \(\operatorname{rank}\mathcal D=0\), the transformed pentad permutes the
  base rays with one common scale; the resulting Lorentz Gram table has an
  explicit deterministic local decomposition.

These cases exhaust the residual architecture.

## Nondependencies and absence of circularity

- D1 is not used to prove the two-setting equality. It is used only after E1 to
  show that \(3\times2\) is attainable.
- D2 is used inside D3 and for boundary architectures; it does not use the
  final residual closure.
- D3 reduces arbitrary finite outputs to the residual architecture; it does
  not assume the closure theorem.
- The final closure uses D3 but not D1.
- Numerical searches, the conjectured exact D1 optima, and the earlier
  conjectured intrinsic Hessian signature are not dependencies.
