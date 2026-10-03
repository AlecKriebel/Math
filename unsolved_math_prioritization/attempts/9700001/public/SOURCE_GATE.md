# Primary-source and scope gate

Checked on 2026-10-03 UTC. Problem 9700001 / AMR-096-0001.

## Exact primary target

The problem catalogue URL is https://www.unsolvedmath.com/problems/9700001. Direct retrieval returned HTTP 403; the catalogue was not used to establish any mathematical claim. The authoritative target is David Aldous's complete short problem page:

https://www.stat.berkeley.edu/~aldous/Research/OP/fields.html

It asks for a useful meaning of practical discoverability of a bounded stopping time whose expected process value differs from the initial mean. Separately, it asks about tractable classes obtained from polynomially many stopping equalities in a discrete horizon. It does not specify process encoding, algorithmic resources, observation access, tolerance, or error probability. Its motivation is market efficiency. All five attempts address finite horizons and explicitly declare additional assumptions.

The complete page was read, including its link back to the maintained index. There is no delegated technical paper or linked proof on that page. Its continuous-time motivating equivalence expressly suppresses technical conditions; this packet makes no unrestricted continuous-time optional-stopping claim.

The complete [maintained index](https://www.stat.berkeley.edu/~aldous/Research/OP/index.html) was also read. It places this topic at 0.5 on its conceptual-to-technical spectrum and warns that maintenance can miss relevant current work. The [author's related discussion, section 3](https://www.stat.berkeley.edu/~aldous/Real_World/words_paradox.html) repeats the conceptual difficulty without supplying a solution. These observations support the scope reading, not a proof that later literature has no answer.

## Classical inputs and complete proof coverage

- The telescoping identity, conditional-expectation equivalence, finite optional projection, finite-dimensional rank argument, rational kernel construction, and all counterexamples are proved in the turn files.
- The finite-state backward recursion is the classical Snell-envelope/optimal-stopping method. Bibliographic credit: J. L. Snell, Applications of Martingale System Theorems, Transactions of the AMS 73 (1952), 293-312, https://doi.org/10.1090/S0002-9947-1952-0050209-9 . Bibliographic metadata was verified; direct AMS PDF retrieval returned HTTP 403. No unread theorem is imported: the needed finite induction is proved in full in Attempt 4.
- W. Hoeffding, Probability Inequalities for Sums of Bounded Random Variables, JASA 58 (1963), 13-30, https://doi.org/10.1080/01621459.1963.10500830 . A complete author-paper scan at https://www.cs.rpi.edu/academics/courses/spring06/random/hoefding.pdf was retrieved. Theorem 2, equation (2.6), printed p.16; its complete proof on pp.22-23; the convexity lemma on pp.20-21; and the exponential-Markov/independence setup on p.14 were inspected, with the displays checked visually because the scan has no text layer. Attempt 5 includes an alternative full tilted-variance proof and the exact constants needed here.

No cited external theorem is needed without either a complete proof in this packet or the relevant primary argument having been inspected. Neither the optimal-stopping method nor the concentration bound is claimed new.

## Bounded prior-work checks

GitHub was searched across open and closed PRs in AlecKriebel/Math for 9700001, the title phrase, and AMR-096. Broad 'Martingale' results were inspected and did not concern this target. Code search for 9700001, commit search for 9700001, and branch search for 9700001 returned no match. The expected target README path was also absent. These are bounded negative checks, not a claim that every possible unindexed history or differently named branch was exhaustively inspected.

The main-branch queue at https://github.com/AlecKriebel/Math/blob/main/unsolved_math_prioritization/QUEUE.md showed rank 540 as queued, 0/5; file blob SHA was 24545d98c2c211548377ed2f2555d6a129abfc69. That administrative label alone was not treated as evidence of missing prior work. Nearby AMR-096 PRs found in the search concerned other IDs.

Web searches included the exact problem title and combinations of computational martingales, optional stopping, cryptographic indistinguishability, and market-efficiency complexity. No identified result was used as a resolution of this exact question. These searches do not certify the absence of a published resolution or establish priority for any construction here.

## Retrieved-source byte identities

Source copies are retained solely for reading, not distributed here. SHA-256:

- Aldous problem HTML: a6e69e62ec5ca5c77750245b07d1182dd44488eab863cdc83d8ca1a6122694e5
- Aldous index HTML: 69de0a61207bac04b9452263afbc75321409adb75e673d0f6dfb29a2441adb40
- Hoeffding paper scan: 3021bcc097ef23a99a84d0eef8dcce2fd835c71df79a105727d3e03f8f0b8930

## Gate decision

PASS for developing the explicitly scoped finite-horizon partial results. FAIL for claiming that the original broad definitional problem is settled, that a universal fixed polynomial library captures all efficient stopping algorithms, or that these elementary/classical ingredients are historically novel. Proposed research disposition: unsolved, 5/5 attempts. Any separate review must retain these distinctions.
