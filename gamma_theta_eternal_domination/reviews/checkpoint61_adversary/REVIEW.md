# Checkpoint 61 adversarial integration review

Date: 2026-07-27 PDT

## Verdict

**PASS ON THE MATHEMATICS AND CERTIFICATES, SUBJECT TO THE EDITORIAL
SCOPE FIXES BELOW BEFORE PUBLICATION.**

I found no mathematical overclaim in the individual C-085--C-092 ledger
entries.  In particular, C-090 is a valid `CERTIFIED-FINITE` result for
the order-13, parameter-three, full-response branch.  Its coverage and
proof are independent of the discovery generator, do not assume a unique
full target or connectivity, and do not use the new six-witness theorem.
The no-full-list branch remains open, so the finite frontier remains 13
relative to the published through-order-11 premise.

The local public page correctly says that the universal conjecture is
unresolved, that order 14 is not excluded, and that parameters four and
five at order 13 remain live.  Alec Kriebel is correctly attributed as
the research lead/author, and the heavy AI assistance and absence of
external expert review are disclosed.

Before publication, make the narrow wording fixes in the next section and
stage only the audited gamma--theta artifacts.  The current live page is
still the earlier pre-C-090 version.

## Required pre-publication wording fixes

### 1. Qualify every shorthand reference to the C-090 branch by \(k=3\)

The formal C-090 row is correctly scoped, but several summaries say
“the order-13 full-response branch” without the parameter qualifier.  In a
document that also says the \(k=4,5\) slices remain open, that shorthand can
be read too broadly.

Use **“the order-13 parameter-three full-response branch”** in:

- the C-078--C-092 summary paragraph of `CLAIMS.md`, currently “the entire
  order-13 full-response branch”;
- the first strategy paragraph of the public page;
- the C-090 replay-table label on the public page;
- the proof-progress bullet heading on the public page; and
- the corresponding order-13 branch paragraph in `README.md`.

The body of C-090 and its hostile review already have the correct scope.
This is an editorial boundary repair, not a defect in the certificate.

### 2. Replace the ambiguous phrase “static equality” in C-092

C-092 immediately gives the correct tuple
\[
(\gamma,i,\alpha,\gamma^\infty,\theta)=(3,3,3,4,4),
\]
but “realizes the static equality” can be misread as asserting eternal
equality.  Say instead that the graph realizes
\(\gamma=i=\alpha=3<\theta=4\) and the displayed direct-seed/list
conditions, while \(\gamma^\infty=4\).

### 3. State the working directory for public replay commands

The C-050, C-057, and C-090 commands in the public table are valid from
`gamma_theta_eternal_domination/`, but the page does not say that.  Either
add “Run from the campaign directory” above the table or prefix every path
with `gamma_theta_eternal_domination/`.  This is a reproducibility fix, not
a mathematical issue.

### 4. Do not describe the updated page as deployed until it is pushed and
verified

At this review snapshot:

```text
HEAD = origin/main = 21f5042e6a010db53f759177a0f36d90016cc0ba
local page SHA-256 = a696982d68b3ad795f0b449ae45d413955c805531243796098f24ae321d02756
live page SHA-256  = 543884bdfc24d66b9ebedf4330b2b57d66d8d9d73f14d8e881118e70671974f5
```

The live page still contains the older “prove that this ladder cannot close
finitely” text and does not contain C-090.  Commit, push, wait for Pages,
and byte/content-check the live page before reporting deployment.

## Claim-by-claim audit

| Claim | Status | Audit result | Decisive reviewed bytes |
|---|---|---|---|
| C-085 | `PROVED` | PASS.  The fixed core is chosen before the deletion coloring; the fixed hitting set has at most two physical terminals.  The rainbow transversal is coloring-dependent, as stated.  The terminal-cube attack uses unoccupied targets and one guard only. | `full_list_terminal_hitting/NOTE.md` `d91fe6087283f92a6ca295f5b9a2a43e7d8ad0a34e89a811490d22bc729595ce`; hostile review `ee31aef1555dec1ff59edfcdc11a21d7579157bf979222373c7e1f50711aee1f` |
| C-086 | `PROVED` | PASS.  Kempe linkage, cap-location trichotomy, side-purity, and singleton continuation all retain their branch hypotheses.  No family-preserving Kempe swap or arbitrary cross-projection continuation is asserted. | previous note/review plus `k3_side_purity_cap_cycle/NOTE.md` `64312289f6d3d87a4c302692c92901caeb9788b16354493e07be01920549f11b`; hostile review `094ee0e88d20bd3454e49ec8c9a82e3d6799b470d1eeba106f5a11776ffadeef` |
| C-087 | `REFUTED` | PASS.  `GCXfVG` is a positive equality graph, not a counterexample.  The clean-room checker confirms 26 dominating triples, all eternal, and no C-079 fan, complement \(K_4\), or dominating pair. | source result `f9dd30333986b0c984910fe3e13464c28bd64a98d85932c8e2df14f805fb1998`; independent result `9f3285541225a7bd495811853cfbd5a65dce6171fd46cbac6b7fa1f6c5ff90cb` |
| C-088 | `PROVED` | PASS.  The order 13/14 statements are conditional on the exact induced nine-vertex complement and exact response lists; they are not a frontier claim.  The gamma-two bow-tie is only a control. | note `6b9f39e443e99894ffb7490c572149a9ae220ed1d6c445e66df7e0796eec36ff`; hostile review `f8877823ce54fd82884541dd09ac5f96aa037d7ece3554e882b6219f3c56cce7`; evidence `0c66e111583e06404d98e001be5c081e883fe0f5afb72e4bf2b13d38a911a586` |
| C-089 | `PROVED` | PASS.  Anchor purity, the two forced cross-anchor responses, layer disjointness, and the six-vertex count follow from literal one-guard closure.  The \(n\ge15\) corollary is only for the exact separated-port core. | `full_response_disjoint_witnesses/NOTE.md` `b5c845cee5d887596d1c26660fe741c5ef54763d87d42033c1826f341b4fe6e4`; independent review `d59a0b4663cbb7c4b56faaaad103dd0a2add80a0ebe3c42cc075fd3daf55a6ec` |
| C-090 | `CERTIFIED-FINITE` | PASS.  See the dedicated audit below.  This excludes exactly the order-13, \(k=3\), full-response incidence branch. | formula `d5a2f17ad6e61cb7ca5cb9d2930b6a0738fec32ee1d9956207dc67bb297dcb13`; proof `653b01e904b97c01bfa25fbbea29fbadee603918dbaff0ea41b7ad09460fb910`; clean checker `87f01851aef06da770373058e662fff11a273cfd51eb47251a6e60b6d812b95d`; hostile review `d59a0b4663cbb7c4b56faaaad103dd0a2add80a0ebe3c42cc075fd3daf55a6ec` |
| C-091 | `PROVED` | PASS.  The physical representative retains both positive responses and has a literal complement edge to the omitted anchor.  The proof explicitly does not preserve arbitrary logical connector edges. | `separated_core_n14_attack/NOTE.md` `a619c7acf0dfccbc5767379f68d25f6272d3318db33e433cede39aa70b5ce279`; hostile review `538dfd4182d1ca6217cd7fa20226e097270861d3124cdf976406587d18082f51` |
| C-092 | `CERTIFIED-FINITE` | PASS after the terminology fix above.  The independent checker reproduces \((3,3,3,4,4)\), all 200 triple deletions in rounds \(140,60\), and the four failed seed attacks.  It is not a counterexample. | source and independent result `f4b1ed7caf63d93798134353233306402202d2ff1439f7eef3f82068e8bfa489`; independent checker `b5eb2f7f1c1fada8e765d2799710347211ae46a864bdfb120c5bc81ca847a0fc` |

## Dedicated C-090 certification audit

The clean-room checker allocates all 9,802 variables and reconstructs all
85,409 clauses without importing the discovery `search.py`.  The generated
DIMACS is byte-identical to the frozen instance.  The four variable
families and clause counts agree:

```text
78 complement-edge variables
858 pair-witness variables
286 retained-state variables
8,580 response variables

715 no-H-K4 clauses
1,794 pair-common-neighbor clauses
2,860 retained-state domination clauses
20,020 literal closure clauses
10 fixed-anchor/full-target clauses
59,049 anchored noncoloring clauses
960 signature-sorter clauses
1 redundant family-nonempty clause
```

The formula-to-theorem implications are correct:

- the anchor \(H\)-triangle and no \(H\)-\(K_4\) give \(\alpha=3\);
- an outside common \(H\)-neighbor for every pair gives \(\gamma\ge3\);
- the retained dominating anchor state gives \(\gamma\le3\);
- a nonempty closed family of dominating triples gives
  \(\gamma^\infty\le3\), hence equality by \(\gamma\le\gamma^\infty\);
- the complete anchored bank is exactly \(\chi(H)>3\), i.e.
  \(\theta(G)>3\); and
- the fixed three direct successors express a full family response at
  \(x\), with all three required \(G\)-edges.

Every closure obligation attacks only \(r\notin D\).  Each response names
one occupied guard, requires the corresponding \(G\)-edge, and retains the
single resulting successor.  There is no all-guards move, occupied-vertex
attack, graph/complement reversal, or clique-cover/coloring reversal.

The sorter is sound.  Its eight 120-clause adjacent-comparator blocks were
truth-tabled on all \(8\cdot16^2=2,048\) local signature pairs.  The
nonsorter formula is covariant under the full \(S_9\) on vertices
\(4,\ldots,12\), including witness, family, response, and complete coloring
variables.  Thus sorting the four-bit signatures loses no orbit, including
ties.

Fresh execution of the hostile checker passed.  It reconstructed the
formula byte for byte and replayed both streams twice:

```text
full:    11,846 of 85,409 clauses in core; 8,277 core lemmas;
         485,709 resolution steps; 0 RAT lemmas; VERIFIED
reduced: 11,343 of 11,846 clauses in core; 8,036 core lemmas;
         479,565 resolution steps; 0 RAT lemmas; VERIFIED
```

The no-sorter discovery run reached its 120-second cap and remains a
nonclaim.  It is not needed: the \(S_9\) orbit proof supplies coverage.
The no-closure and no-clique-gap ablations are SAT controls only.  Neither
is used as an UNSAT premise.

The source discovery note and its source `result.json` intentionally retain
their pre-review “pending clean-room audit” boundary.  Do not rewrite those
frozen provenance bytes.  The promotion authority is the hostile
`REVIEW.md` and its deterministic `result.json`.

## Public-page and README audit

The following statements pass:

- the conjecture is explicitly labeled unresolved;
- no counterexample or universal proof is claimed;
- the global finite frontier is 13, explicitly relative to the published
  computation through order 11;
- the \(C_5,C_7\) order-13 \(k=3\) templates and the complete \(k=4,5\)
  slices remain open;
- the order-13 no-full-list timeout is explicitly a nonclaim;
- no general order-14 search or lower bound of 14 is claimed;
- exact-pattern floors of 13, 14, or 15 are repeatedly distinguished from
  a global frontier;
- the one-guard model, unoccupied attacks, \(G\) versus \(\overline G\),
  and clique cover versus complement coloring are stated correctly;
- only the order-12 frontier paper is issued; the earlier component draft
  is identified as superseded rather than a second paper;
- Alec Kriebel is named as research lead/author in metadata and visible
  text; and
- heavy ChatGPT assistance, Alec Kriebel's inability to independently
  validate the mathematics, and the lack of external expert review are
  disclosed.

Local syntax checks passed:

```text
git diff --check: PASS
HTMLParser parse: PASS
```

## Staging audit

The worktree is heavily shared.  Do not use `git add .`, a repository-root
glob, or a broad `gamma_theta_eternal_domination/**` add.

### Audited C-085--C-092 publication scope

The intended source/review directories are:

```text
docs/research/gamma-theta-conjecture/index.html
gamma_theta_eternal_domination/CLAIMS.md
gamma_theta_eternal_domination/README.md
gamma_theta_eternal_domination/math/working/full_list_terminal_hitting/
gamma_theta_eternal_domination/math/working/full_response_disjoint_witnesses/
gamma_theta_eternal_domination/math/working/full_response_witness_bound/
gamma_theta_eternal_domination/math/working/k3_side_purity_cap_cycle/
gamma_theta_eternal_domination/math/working/order13_single_full_squeeze/
gamma_theta_eternal_domination/math/working/separated_core_n14_attack/
gamma_theta_eternal_domination/reviews/full_list_terminal_hitting_hostile/
gamma_theta_eternal_domination/reviews/full_response_witness_bound_hostile/
gamma_theta_eternal_domination/reviews/k3_side_purity_cap_cycle_hostile/
gamma_theta_eternal_domination/reviews/order13_full_target_hostile/
gamma_theta_eternal_domination/reviews/separated_port_two_color_ladder_hostile/
gamma_theta_eternal_domination/reviews/two_response_replication_hostile/
gamma_theta_eternal_domination/reviews/checkpoint61_adversary/
```

`STATE.md` and `RESEARCH_LOG.md` changed during this audit in another
workstream.  Review their final diff separately before adding them.
`order13_no_full_probe/` may be archived as an explicit timeout/nonclaim,
but it is not evidence for C-090.  The newly appearing
`order13_no_full_decomposition/` and `physicalized_twosat_endgame/` files
are active exploratory work and were not reviewed here.

### Definitely exclude from this checkpoint commit

```text
dimension_three_keller_degree/**
gamma_theta_eternal_domination/certificates/order12_k4_v3_case0111_recovery_attempt000001/**
gamma_theta_eternal_domination/certificates/synthesis_k3_hole5_signature_seed0_lrat_c033/**
gamma_theta_eternal_domination/certificates/synthesis_k3_hole7_full_bank_seed0_addition_only/**
gamma_theta_eternal_domination/results/order12_k4_aggregate_verifier_v3_case1111/**/replay.lock
gamma_theta_eternal_domination/reviews/order12_k4_v3_aggregate_hostile_replay_8b09516c/replay.lock
gamma_theta_eternal_domination/results/synthesis_k3_template_bank_runs/hole5_seed0_600s/proof.drat
gamma_theta_eternal_domination/math/working/terminal_cube_patterns/**
gamma_theta_eternal_domination/math/working/order13_no_full_decomposition/**
gamma_theta_eternal_domination/math/working/physicalized_twosat_endgame/**
```

Python `__pycache__/` files are ignored and must remain unstaged.  The
19,874,489-byte C-090 proof is intentional and below GitHub's individual
file limit; the similarly named legacy proof/certificate files above are
not part of C-090 and must not be swept in.

## Final boundary

After the four editorial/deployment fixes, C-085--C-092 and the updated
public page are suitable for this campaign checkpoint.  They establish a
substantial structural and finite advance, especially C-090, but they do
not prove the \(k=3\) case, exclude all order-13 graphs, advance the global
frontier to 14, or resolve the universal gamma--theta conjecture.

## Re-audit addendum

Re-audit time: 2026-07-27 PDT

Current reviewed hashes:

```text
CLAIMS.md  34817c7972ab97519c66a086d654ac06014886d3b37d54246865411dfcd2eb19
README.md  7ea616dd2492b37d6b56cd5958c6b5f14288707c9bb910a7f41e1460ad83aa1c
page       7940257532fbdd14efb22eab455b5e66f055dacb0cdf30115455fe1772eb5b35
```

**PASS** on the first three requested fixes:

1. C-090 is now consistently called the **order-13 parameter-three
   full-response branch** in the ledger summary, README, public strategy
   text, replay table, proof-progress heading, and timeline.
2. C-092 now states the static tuple explicitly as
   \(\gamma=i=\alpha=3<\theta=4\), separately states
   \(\gamma^\infty=4\), and no longer uses the ambiguous phrase “static
   equality.”
3. The public verification section now says to run all displayed commands
   from `gamma_theta_eternal_domination/`.

`git diff --check` passes on all three current files.

**One remaining deployment step, not a content defect:** the update is
still local.  At this re-audit snapshot,

```text
HEAD = origin/main = 21f5042e6a010db53f759177a0f36d90016cc0ba
live page SHA-256 = 543884bdfc24d66b9ebedf4330b2b57d66d8d9d73f14d8e881118e70671974f5
```

The live page still contains the superseded “ladder cannot close finitely”
paragraph.  After the reviewed files are committed and pushed, wait for
GitHub Pages and verify that the live content includes the parameter-three
C-090 qualifier and replay-directory instruction.  No active
no-full-list, decomposition, or physicalized-endgame draft was assessed in
this addendum.
