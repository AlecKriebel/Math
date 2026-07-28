# Revised-byte addendum: family mixed-\(P_4\) rank recurrence

Review date: 2026-07-28 PDT

Revised candidate commit:
`64b7ffee426fc5b97921f1d08daae7bcb5ee7e47`

## Verdict

**PASS REVISED BYTES.**

The three proof-binding corrections required by the original hostile review
were made exactly.  The revised package introduces no mathematical or scope
change beyond those repairs.  The original
`FAIL_PENDING_NONSUBSTANTIVE_PROOF_BINDING_CORRECTIONS` verdict is therefore
discharged for candidate v2.

The following partial results may now be promoted:

- exact family mixed-\(P_4\) list transport across an independent root
  ridge;
- exact one-round rank loss in every single-hit deleting row;
- impossibility of the rank-zero endpoint-defect terminal;
- finite descent from single-hit rows to a genuine multi-hit row;
- the complete named-target audit;
- the fresh eight-cell mover/list reduction and its three C-145
  reciprocity consequences; and
- the outer-collision dominating-pair/completion-clique alternative.

The full eight-cell recurrence remains **OPEN**.  The revised package does
not exclude the family-list mixed \(P_4\), prove complete \(k=3\), or resolve
the universal conjecture.

## Revised candidate binding

| Artifact | SHA-256 |
|---|---|
| `math/working/family_mixed_p4_rank_recurrence/NOTE.md` | `97d456cf08eda021a57067aa27ec13f767a5e51ec4705299d3a43a06c375bf84` |
| `math/working/family_mixed_p4_rank_recurrence/OBSERVED_RESULTS.json` | `d0d54d2cd8d6b84e668fcf2d4f6965fc593fb657b305dd6036e4e66ae46f6658` |
| `math/working/family_mixed_p4_rank_recurrence/RESEARCH_LOG.md` | `a4a1b8498bc67da888d80d20c47614e302f4d85dcd6202246b85f9b7aefa64cb` |
| `math/working/family_mixed_p4_rank_recurrence/MANIFEST.json` | `186108347ff44541e2fc7c2f5df7050620aa55add6d69cb34301d35cf6ea85d0` |

The three artifact hashes declared inside the revised manifest match the
files byte for byte.  The manifest parses as valid JSON and identifies
schema `family-mixed-p4-rank-recurrence-candidate-v2`.

## Correction audit

### C-064 exchanged-role proof

Revised NOTE lines 94--110 now:

1. invoke accepted C-064 Theorem 3.1 on the retained independent ridge
   states \(S,S'\);
2. note that the ridge transposition fixes every path target \(x_j\);
3. identify the common successor
   \[
   S-g+x_j=S'-r+x_j;
   \]
4. derive \(rx_j\in E(G)\) from domination of \(r\) and independence of
   \(S'\); and
5. derive \(gx_j\in E(G)\) symmetrically from domination of \(g\) and
   independence of \(S\).

This supplies the missing move-edge justification.  Equality of family
membership is no longer incorrectly asked to imply graph adjacency by
itself.

The revised manifest binds the exact accepted bytes:

| Dependency | SHA-256 |
|---|---|
| C-064 source | `e30a0ac4e028deefbf4c4533646ff934b617d8ff61dce38ec2389a50d622d8e7` |
| C-064 hostile review | `bc5011d85d333fb66fce3ea563e4cc80cf016090cc3427e44187b2e40fb5f9f8` |

Both hashes match the repository files.

### C-058 restoration use

Revised NOTE lines 351--364 now identify C-058 Theorem 3.1 and spell out
the exact state:

\[
D=\{c,x_0,x_1\},\qquad
S-D=\{a,b\},\qquad
D-S=\{x_0,x_1\}.
\]

The exact family-response lists give

\[
L_S(x_0)\cup L_S(x_1)=\{a,c\},
\]

so the missing anchor \(b\) is not restored and \(D\notin\mathcal K\).
The note explicitly observes that the C-058 proof constructs its restoring
swaps inside the specified family, which is the family-list form needed
here.

The revised manifest binds:

| Dependency | SHA-256 |
|---|---|
| C-058 source | `71384d66373ab4cbffa7ced60973971cf39b72a0315eac31ad522abd1afa2f47` |
| C-058 hostile review | `4369b3b85912e3e9a534ea2a63c9cc12ab06cb701cd2227ea77c912665c51d45` |

Both hashes match the repository files.

### C-151 rank-zero terminal

Revised NOTE lines 225--230 now identify accepted C-151 Lemma 1.1 as the
family-response-list one-defect form of the C-148 local kernel.  This is
the exact scope required after ridge transport.  The candidate already
bound the accepted C-151 source and hostile-review manifest, and both
bindings remain unchanged and correct:

| Dependency | SHA-256 |
|---|---|
| C-151 source | `115df65cbeb4e9dffccaad93adc78e7c22d698a5036f431ec2e57ba67598a3d1` |
| C-151 hostile-review manifest | `9172dc9ce7f31d798118f99b9c9ebc376e410e5c9b7d7e3cdfaa4c574f3d9c80` |

### Research log and scope

The revised research log records all three corrections and their exact
dependency hashes.  The only theorem-note changes are the three requested
proof bindings.  `OBSERVED_RESULTS.json` is byte-identical to v1.

The manifest's `open_claim` is unchanged:

> The full eight-cell recurrence to a lower-rank endpoint row, a C-148
> defect core, or a dominating pair remains open.

No candidate claim was broadened or silently promoted from observation.

## Independent replay

The original clean-room checker remains unchanged at SHA-256

`84a0c2c158d0517563914535948669ea914516fcd5e329f2eac4206437f5160b`.

Against candidate v2 it again returns `PASS_BOOKKEEPING_ONLY`.  Its
canonical stdout now has SHA-256

`2b6fbe8a653f25d49af4b411d5ef17386241d8e250c3892e107b42b8628888d3`.

The stdout hash differs from v1 only because the checker reports the
revised candidate artifact hashes; all symbolic mover, rank, C-145, and
completion assertions are unchanged.

## Final status

| Item | Revised verdict |
|---|---|
| C-064 proof and binding | **PASS** |
| C-058 proof use and binding | **PASS** |
| C-151 terminal citation | **PASS** |
| manifest integrity | **PASS** |
| no scope broadening | **PASS** |
| candidate v2 partial recurrence package | **PASS** |
| full eight-cell recurrence | **OPEN** |
| family mixed-\(P_4\) exclusion | **OPEN** |
| complete \(k=3\) theorem | **OPEN** |
| universal conjecture | **OPEN** |
