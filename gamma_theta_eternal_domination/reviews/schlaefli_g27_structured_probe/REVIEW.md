# Independent review: Schläfli \(G(27)\), one-guard \(k=3\)

Review time: `2026-07-26T22:18:15Z`
Repository base observed: `06230d40f25f186e7f92857209546f694a864ba6`

## Verdict

`ACCEPT_STRUCTURED_K3_STRESS_TEST`

Accepted statements:

- `PROVED`: the graph reconstructed from the displayed 27-line incidence
  rules has \(\gamma=i=\alpha=3\);
- `PROVED`: no one-guard-moves eternal dominating family of size three exists;
- `CERTIFIED-FINITE`: the synchronous kernels have sizes
  \(1125\to45\to0\), with \(K_0\) equal to 45 \(H\)-triangles plus 1,080
  induced \(H\)-paths;
- `CERTIFIED-FINITE / COMPUTATIONAL`: \(\theta(G)=6\), from two independent
  complete searches and an explicit six-coloring.  No SAT proof log is claimed.

Not accepted or asserted:

- an exact value of \(\gamma^\infty(G)\) above the lower bound \(4\);
- any order-frontier improvement;
- any resolution of the universal \(\gamma\)–\(\theta\) conjecture.

## Independent construction and replay

The author program uses integer bit masks.  The review program imports no
campaign or author code: it reconstructs the E/C/L incidence graph using
tuples and `frozenset`s, builds moves with set replacement, and performs
simultaneous deletion rounds.

Both programs verify:

```text
H parameters                 (27,10,1,5)
G parameters                 (27,16)
gamma,i,alpha                3,3,3
theta                         6
triple table (edges,centers) (0,3):720 (1,1):1080
                              (2,0):1080 (3,0):45
kernel sizes                 1125,45,0
P3 lethal attacks            exactly 4 for each of 1080 states
triangle first responses     exactly 2, both P3, for each attack
```

The review's independent five-color exclusion enumerates 72 stable six-sets,
no stable seven-set, all 756 disjoint pairs of stable six-sets, and rejects a
three-coloring of every 15-vertex residue in 7,800 recursive calls.  Residual
edge counts are 36 in 720 cases and 45 in 36 cases.

Replay from the repository root:

```sh
python3 -I -B gamma_theta_eternal_domination/math/working/schlaefli_g27_probe.py
python3 -I -B gamma_theta_eternal_domination/reviews/schlaefli_g27_structured_probe/audit.py
```

Artifact hashes before this review file was added:

```text
3645819e3953e30db22b062ff0f87b00cf3d4f928f543dff79f9a967f1761fd9  math/working/schlaefli_g27_probe.py
81a079c1f737950996cd7e91a646b95464814fd068512a09d2c926735ce0168d  math/working/schlaefli_g27_two_attack_obstruction.md
37878e79b1c1527bd3230cf94599083ebe01313fc028e4a34e8b443de03097da  reviews/schlaefli_g27_structured_probe/audit.py
```

SHA-256 of the deterministic standard output:

```text
d50d01db88689bee6ef42e30ca3ad8062031813eabe19a551a2d1f5859de4cc5  author output
7c1af42d52293409158543809799ce62f1885cf587bad12ebf6b605b1853ff34  review output
```

Both independent constructions produce the same newline-terminated labeled
\(G\)-edge-list digest:

```text
c507b9d74f40bb73f7fdf63700e30009ff48fef87dde71af1ab11b8779fd414b
```

## Human obstruction audit

The machine kernel has a compact mathematical explanation:

1. The dominating triples are exactly the \(H\)-triangles and induced
   \(H\)-paths.
2. For an induced path \(a-b-c\), inclusion-exclusion in
   \(\operatorname{srg}(27,10,1,5)\) leaves exactly four vertices adjacent in
   \(H\) to none of \(a,b,c\).  Attacking one in \(G\) makes every possible
   replacement a non-dominating zero- or one-edge \(H\)-triple.
3. Every vertex outside an \(H\)-triangle meets exactly one triangle vertex.
   Thus every legal dominating first response from a triangle is an induced
   \(H\)-path, to which item 2 applies.

The only graph-specific sublemma not forced just by the SRG pair parameters is
that an \(H\)-independent triple has a common neighbor.  The note discharges it
by an exhaustive six-type incidence classification, not by solver output.

## Process disclosure

An initial disposable stdin prototype accidentally invoked the campaign's
brute-force independence-number routine at order 27 and remained CPU-bound
after its tool cell returned blank output.  PID `33724` was subsequently found
to be absent when explicitly checked; a final process scan found no lingering
Schläfli/Python job.  That prototype contributed no accepted result.  The two
frozen replays above take approximately 0.3 and 0.8 seconds respectively and
perform no \(k\ge4\) eternal-kernel computation.
