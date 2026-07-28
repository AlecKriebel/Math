# Hostile review: single-full deletion dichotomy

## Verdict

**PASS.**  Every statement labeled `PROVED` in the reviewed target is
correct at its stated conditional boundary.  The note also correctly
refuses to promote the “canonical configuration or dominating pair” slogan
to a theorem.  No target edit is required.

Reviewed target SHA-256:
`3273c1e4a1b042bcaa2ebdda416d2591ec83c93be535e14ff2c585932c2b5ee1`.

Two steps could be made slightly more explicit without changing the proof:

1. Theorem 2.1's split for \(\gamma(G-x)=2\) uses
   \(\theta(G-x)\geq\alpha(G-x)=3\), so the alternatives really are
   \(\theta=3\) and \(\theta>3\).
2. In Lemma 3.2, the selected link vertices are distinct from the anchors
   because fullness makes \(x\) adjacent in \(G\) to every anchor.

These are immediate from the setup and are not gaps.

## Dependency and scope audit

The deletion, list-preservation, spoke, link-rigidity, and cross-spoke
theorems are used with exactly the hypotheses proved in the accepted
full-list note:

- `k3_full_list_slice/NOTE.md`:
  `ebcf7a6ef902889e5d70a657baf7e79613b3dd0e278be01263cf0882033d23be`;
- its hostile review:
  `8cfc6f38453baf9578034c05b596069172c42048c6644bb962b78251bc644d3c`.

The normalized inclusion-minimal 2-CNF trichotomy is also used within its
proved scope.  The current revised bytes merely add the previously
requested zero-length-path and unit-source clarifications:

- `k3_twosat_bicycle/NOTE.md`:
  `8a934a8194913633821223b070a013dda8e0cd8c0d6870616b32a882e8b2fd59`;
- hostile review with revised-byte `PASS` addendum:
  `8efe5d1cc66970d637784a70967546c7b731a559c4003ed5a4577d0bc9045449`.

The exact no-full-list gluing prerequisite and its hostile review remain at
`fc7f817aa611751b9bedbb9ddebd5830d81f02719f2d8aafe914db34f4c64907`
and
`f797870e45e2f8a0c0e6691a2b5e418ec1148043389fe2049c4453a0cfaf98d3`.

No dependency is silently strengthened.  In particular, the target does
not claim that arbitrary logical chains shorten to induced or bounded
physical graph configurations.

## Theorem 2.1

Deletion preserves
\(\alpha(G-x)=\gamma^\infty(G-x)=3\), while the accepted corollary gives
\(\gamma(G-x)\in\{2,3\}\).

- If \(\gamma(G-x)=3\), then \(G-x\) has eternal equality.  Minimum-order
  minimality forbids it from being a smaller counterexample, so
  \(\theta(G-x)=3\).
- If \(\gamma(G-x)=2\), then
  \(\theta(G-x)\geq\alpha(G-x)=3\).  Thus either \(\theta=3\), or
  \(\theta>3=\alpha=\gamma^\infty\), exactly the inherited near-miss.
- Whenever \(\theta(G-x)=3\), adjoining the singleton clique \(\{x\}\)
  gives \(\theta(G)\leq4\), while the counterexample inequality gives
  \(\theta(G)\geq4\).  Hence \(\theta(G)=4\).
- A deletion clique part avoiding \(R=N_H(x)\) consists entirely of
  \(G\)-neighbors of \(x\), so adding \(x\) to it would contradict
  \(\theta(G)=4\).  This proves color saturation on \(R\).
- In both \(\gamma=2\) branches, the accepted deletion corollary supplies a
  pair in \(R\) dominating \(G-x\), with \(x\) its unique common
  complement neighbor.

The three cases are exhaustive and pairwise disjoint.

## Kempe linkage and forced cross-part move

For two colors \(i,j\), if no bichromatic component contains link vertices
of both colors, swap \(i,j\) on every component meeting an \(i\)-colored
link vertex.  All link vertices formerly colored \(i\) change, and no
\(j\)-colored link vertex changes to \(i\).  The link then avoids \(i\),
allowing \(x\) to receive \(i\), contrary to \(\chi(H)=4\).  The Kempe
argument is exact and does not claim that its paths stay inside \(H[R]\).

In a three-clique partition of \(G-x\), the independent anchors occupy
distinct parts and saturation supplies \(r_u\in C_u\cap R\).  Starting at
\(S\), make the three unoccupied attacks \(r_u\).  As long as the
same-part successor is retained, it is a legal one-edge move and preserves
one guard per part.  If all three survived, the final state would lie
entirely in \(R\) and would not dominate \(x\), impossible for a state of
\(\mathcal F\).  At the first failure, closure of
\(\mathcal F^{-x}\) supplies a response, but its unique same-part guard
cannot give a retained successor.  Every retained response therefore
crosses parts.  The argument uses only unoccupied attacks and exactly one
moving guard.

## Augmented 2-SAT fork

Because \(F_3(S)=\{x\}\), deletion leaves no full response-list vertex, and
list preservation makes the deletion formula exactly the base formula
\(\Phi\).  Coloring \(x\) with \(w\) affects only
\(R=N_H(x)\): a conflicting singleton is a false constant, and a
conflicting two-list contributes the stated port-forbidding unit.

Every \(\Psi_w=\Phi\wedge U_w\) is unsatisfiable, since a satisfying
orientation would give a compatible proper 3-coloring of \(H\).
If \(\Phi\) is satisfiable and there is no false constant, an
inclusion-minimal unsatisfiable subformula must contain an augmented unit;
otherwise it would be an unsatisfiable subformula of \(\Phi\).  The
normalized terminal trichotomy then leaves:

- a one-unit lollipop, whose sole unit is augmented; or
- a two-unit chain, with at least one augmented terminal.

A unit-free bicycle cannot be newly caused by the augmentation.  This is a
logical-core statement only; the note correctly leaves arbitrary physical
path shortening open.

## Spoke and dominating-pair geometry

If \(L(y)=S-\{u\}\), membership of the other two colors forces the
corresponding graph edges.  The remaining edge \(uy\) is either absent,
placing \(y\) on spoke \(A_u\), or present, placing it in \(A_\ast\);
in the latter case the missing response is exactly the absent direct family
successor.

For \(y\in A_u,z\in A_v\), \(u\ne v\), a common neighbor in the complement
link would give the length-two path \(y-r-z\), placing distinct spokes on
one side of a link component, contrary to cross-spoke separation.  A
common complement neighbor other than \(x\) cannot be an anchor and cannot
lie in \(R\), so it lies in \(Z\).  Therefore the pair either dominates
\(G-x\), with common complement neighborhood exactly \(\{x\}\), or has
the asserted external \(Z\)-witness.  If \(\gamma(G-x)=3\), the first
alternative is impossible.

## Independent control replay

`control_replay.py` uses ordinary sets, a fresh graph6 decoder, literal
greatest-fixed-point deletion, direct subset parameter checks, and direct
enumeration of anchored list colorings.  It imports no campaign evaluator
or response-formula builder.

It reproduced all stated control claims:

- For the labeled order-12 record (canonical `K{eYptMJynEn`),
  \(\gamma(G-x)=2,\theta(G-x)=3\); the only required dominating pairs are
  \(\{6,8\}\) and \(\{10,11\}\).  There are two base anchored colorings,
  extension counts \(0,0,1\) for target colors \(1,2,3\), and the unique
  shortest structural two-unit/one-collision paths are
  \(10-5-4-11\) and \(6-9-7-8\).
- For `HCQebjw`, \(\gamma(G-x)=\theta(G-x)=3\), the greatest-family target
  list is \(\{1\}\), and the unique deletion coloring extends only with
  target color \(1\).
- For the displayed 17-state `FDzro` family, all 68 one-guard obligations
  pass, \(\gamma(G)=2\), the deletion base has one coloring, colors \(1,2\)
  extend, and color \(0\) is immediately blocked by singleton vertices
  \(3,5\in R\).

Replay hashes:

- `control_replay.py`:
  `038207bcbcb3bc179292dcbf8716cc2d8894afd7bc570b1912b49a1146f929a5`;
- `control_result.json`:
  `c6709b4148bb012bf293e7cf08ab77a2c813d42db940bbd7f57f128bd946296f`.

The replay is a control verification, not a counterexample exclusion or a
proof of the unresolved \(k=3\) slice.
