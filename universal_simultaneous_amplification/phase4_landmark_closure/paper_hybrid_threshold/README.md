# Simultaneous amplification beyond fitness three halves

This is the unreleased replacement manuscript for the now-superseded
lower-bound paper in `paper_lower_threshold/`.

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

- `main.tex`: replacement manuscript source in active preparation.
- `MANUSCRIPT_PLAN.md`: theorem/evidence map and remaining editorial work.
- `replay.sh`: one-command exact replay for the new construction.
- No release, DOI, submission, or external contact is performed here.
- The released `R_sim>=3/2` paper remains mathematically correct but is
  superseded by this stronger theorem.

From this folder run:

~~~sh
./replay.sh
./build.sh
~~~

`all.sh` performs both steps. The deterministic PDF is written to
`output/pdf/simultaneous_amplification_beyond_three_halves.pdf`.
