# Simultaneous amplification beyond fitness three halves

This is the hostile-audited public preprint replacing the now-superseded
lower-bound paper in `paper_lower_threshold/`.  Version 1.0.0 is archived at
`https://doi.org/10.5281/zenodo.21852072` and tagged as
`simultaneous-amplification-beyond-three-halves-v1.0.0`.

## Central proved result

Let

\[
P(R)=R^6-8R^5+22R^4-30R^3+21R^2-6R+1
\]

and let `R_hyb=1.5028569127905696...` be its unique root in
`(3/2,151/100)`. One fitness-independent family of finite connected
undirected weighted graphs eventually amplifies every fixed
`1<r<R_hyb` under both Bd and dB updating. Therefore

\[
R_{\rm sim}\ge R_{\rm hyb}>3/2.
\]

This refutes the proposed threshold `R_sim=3/2`. The unrestricted exact
value of `R_sim` remains open.

## Status

- `main.tex`: completed and hostile-audited preprint source.
- `MANUSCRIPT_PLAN.md`: theorem/evidence map and remaining editorial work.
- `replay.sh`: one-command exact replay for the new construction.
- `bootstrap_replay.sh`: clean-archive replay after installing the two pinned
  exact-algebra dependencies into a local virtual environment.
- `RELEASE_NOTES.md`: exact scope and status text for the tagged preprint.
- Public project page:
  `https://aleckriebel.github.io/Math/papers/simultaneous-amplification-beyond-three-halves/`.
- No journal submission or external contact occurred.
- The released `R_sim>=3/2` paper remains mathematically correct but is
  superseded by this stronger theorem.

From this folder run:

~~~sh
./replay.sh
./build.sh
~~~

From a clean source-archive extraction, run instead:

~~~sh
./bootstrap_replay.sh
~~~

The bootstrap uses `python3` by default, creates `.venv` at the archive root,
installs the versions in `requirements.txt`, and then runs the same exact
replay.  Set `BOOTSTRAP_PYTHON` to select a different Python executable.

`all.sh` performs both steps. The deterministic PDF is written to
`output/pdf/simultaneous_amplification_beyond_three_halves.pdf`.
