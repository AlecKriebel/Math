# Mesoscopic pair construction track

This directory studies growing strong-pair windmill modules whose number of
blades and number of weakly coupled copies may both diverge.  It is a
first-principles construction/obstruction track; no literature search or
external contact is used.

Current result:

- `MESOSCOPIC_PAIR_BURST_NO_GO.md` proves a cross-rule obstruction for the
  entire balanced, separated strong-pair burst regime.  For every fixed
  fitness

  \[
    r>{1+\sqrt3\over2},
  \]

  a uniformly initialized mutant cannot have positive limiting gain under
  both Bd and dB, even if reaching an unbounded number of mutant pairs is
  declared immediate global fixation.  In particular this closes this
  mesoscopic pair route throughout the target range above `3/2`.

- `verify_mesoscopic_pair_tradeoff.py` independently checks the symbolic
  identities and sign reductions in the proof.

- `check_full_homogeneous_windmill.py` rebuilds both update chains from the
  vertex-level rules, verifies the homogeneous `(portal, heterotypic,
  mutant-pair)` lumping symbolically, and checks finite chains against the
  compound-branching limits.

This is a class obstruction, not a universal theorem about arbitrary
weighted graphs.  Architectures without a separated single-portal pair
burst phase remain open.
