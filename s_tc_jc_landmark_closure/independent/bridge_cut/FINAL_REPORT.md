# Independent bridge/cut final report

Timestamp: 2026-08-09T21:22:57-07:00  
Definitions lock SHA-256:
`c3382650fa004d90b2122aff1c95524590b31e436d77d4b804293184aa925b09`

## Verdict

**PROVED.** The bounded bridge/cut assignment is complete.  No counterexample
to the required bridge or cut claim was found.

1. The exact positive contraction fiber over a leaf-supported bridge tree is
   the full incidence-scaling action.  Explicit positive analytic slices
   exist on the locked standard-strong locus.  The observable edge coordinates
   are normalized effective scales, not physical bridge multipliers.
2. Once the labelled bridge tree agrees, source-relative containment localizes
   to the corresponding projective local source germs.  Distant blobs cannot
   compensate for a projectively nonzero local separator.
3. At every open JC parameter point in the locked standard-strong level-2
   class, a split is a cut split exactly when its Fourier flattening has rank
   at most four.
4. Consequently,

   \[
   N\preceq_{\rm JC}N'\Longrightarrow
   \operatorname{Cut}(N)\subseteq\operatorname{Cut}(N').
   \]

   The proof includes the omitted two-active-endpoint crossing and uses no
   boundary specialization.

## Exact replay

`bash s_tc_jc_landmark_closure/independent/bridge_cut/verify_all.sh` completed
successfully from the repository environment.

- bridge-tree exact-kernel regressions: 793;
- group automorphisms: 6;
- simple two-port-theta reticulation pairs rejected: 6 of 6;
- nontrivial three-port endpoint tensors: 76;
- ordinary trivalent endpoint tensors: 1;
- endpoint failures: 0;
- four-port tensors: 72;
- strict wrong-split certificates: 204;
- one-active failures: 0;
- primitive theta orientations: 102 raw, four canonical classes;
- primitive cycle orientations: 12 raw, one canonical class;
- two-active required minors present: 4 of 4;
- adversarial mutations rejected: 9 of 9.

Certificate SHA-256 values:

- `bridge_certificate.json`:
  `64c319b5d238e35fa79583482704436b0e19942e71ffa708c7ea36a5dbc13995`;
- `cut_certificate.json`:
  `da47733278a74690f6a55bccb1aec2771cc14960a286f45e526461f45aca41b5`;
- `mutation_certificate.json`:
  `956bf6129b9bb3c24cdc2610d907f919665ed1b4022dece74894decbdae90e7d`.

## Adversarial findings preserved

**EXACTLY COMPUTED.** The withdrawn reciprocal-only bridge chart fails on

\[
(1/2,1/2,1/2),\qquad(3/5,3/5,25/72),
\]

which have the same observable product `1/8` but are not related by that
action.  Physical bridge recovery is therefore not claimed.

**EXACTLY COMPUTED.** The first endpoint draft omitted the ordinary
trivalent median.  For that endpoint `F=G=0`; the correct universal conclusion
is `F>0` or `F=0` and `a>=bc`.  Because the joining bridge satisfies `0<z<1`,
the two-active contradiction remains strict.  The ordinary case is now an
explicit certificate record and a mutation-sensitive coverage key.

**EXACTLY COMPUTED.** Missing leaf support creates extra bridge-factorization
kernel directions, and a retained unmarked bivalent factor has a local
stabilizer.  Both hypotheses are therefore explicit.  Leaf support follows
from the locked network convention, and the only simple two-port theta core
is `K4-e`; all six reticulation pairs violate the nonvacuous `S_TC` criterion.

## Boundary of this report

**UNRESOLVED HERE.** This package does not classify projective local model
germs modulo ordinary triangle redirection.  It does not certify the separate
bounded topology atlas, probe coherence, root reduction, or converse gluing.
Those nodes must pass their own independent and adversarial reviews before the
landmark global theorem can be promoted.
