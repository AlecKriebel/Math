# Reproducible local tools

## nauty and Traces 2.9.3

The campaign uses the official 2026-01-01 release of nauty and Traces for
unlabeled graph generation and canonicalization.

- Upstream:
  `https://pallini.di.uniroma1.it/nauty2_9_3.tar.gz`
- SHA-256:
  `9fc4edae04f88a0f5883985be3b39cf7f898fd6cc96e96b9ee25452743cc1b5b`
- Local build: Apple arm64, `gcc -O3 -march=native`, at most two build jobs.
- Required binaries: `geng`, `showg`, `labelg`, `shortg`, and `countg`.

Run `./tools/bootstrap_nauty.sh` from any directory. The downloaded archive,
expanded source, objects, and binaries are ignored by Git; the versioned
bootstrap recipe is the reproducible record.

## Proof-producing SAT tools

`bootstrap_sat.sh` installs CaDiCaL 3.0.1 at commit
`c60730422e758ef1cebe7aeddf2dda31c996bf04` and the independently developed
DRAT-trim checker at commit
`2e5e29cb0019d5cfd547d4208dca1b3ec290349f`. Both downloaded archives are
checked against hard-coded SHA-256 digests before extraction. Builds use at
most two parallel compiler processes.

The solver and checker are separate trust components: an `UNSAT` result is
not accepted unless the saved proof replays successfully with DRAT-trim.
