# Independent mathematical spot-check findings

Date: 2026-08-26 (America/Los_Angeles)

Article source references below are relative to
`../package_copy/proof_package/manuscript/sections/`; evidence-script
references are relative to this directory.

## Verdict contribution

These independent checks found **no counterexample inside any stated strict
parameter domain and no critical or major mathematical defect**.  They provide
strong affirmative evidence for the physical-domain algebra, the complete
three-leaf arguments, the bridge/gluing inequalities, representative
four-port obstructions, the stated ledger censuses and transports, the
Krawczyk box, and the cherry inverse.

My mathematical verdict contribution is therefore **supportive**, with three
explicit limits:

1. The four-port work below is representative, not an independent proof that
   the fourteen stored orbits exhaust every raw mixed-graph double coset.
2. The bridge-fibre freeness calculation is complete once every unmarked
   retained component has degree at least three.  I found the expected
   one-parameter stabilizer at unmarked degree two, but did not independently
   enumerate all strong-class topologies to re-prove that the offending
   two-boundary \(K_4-e\) factor has no admissible tree-child rooting.
3. The packaged probe verifier's standalone transport and restriction
   validators are not semantic validators.  A self-consistently hashed but
   incidence-fake transport passes the actual `validate_transport` function.
   Five independently reconstructed sample rows are correct, but that sample
   cannot repair the verifier-wide assurance gap.

Accordingly, this subreview supports acceptance only as one contribution to
the complete referee audit; it is not, by itself, a fresh end-to-end
enumeration of the global theorem.

## Severity-ranked findings

### No critical or major mathematical defect found

All six scripts completed with exit status 0, and a final `py_compile` check
also completed with exit status 0.  Exact result files are listed in
`SHA256SUMS.txt`.

### Major certificate-verification weakness (not a theorem counterexample)

The actual function
`proof_package/probes/verify_k3p_probes.py:96-124` accepts the coherently
self-hashed fake isomorphic transport
`bfc9e39ce0fddae47e137321086466b90e22dc3c4aaa333afbb1147b477339e4`.
Its vertex map sends `source_b` to `target_b`, while its sole claimed target
edge is `target_a--target_not_in_vertex_map`; the true endpoint image is
`target_a--target_b`.  The claimed edge therefore is not induced by the
vertex map and even contains an unmapped vertex.  Nevertheless, the actual
function returns normally because it checks self-hash, separate injectivity,
relation names, and shallow triangle metadata, but not endpoint incidence,
label preservation, or binding to source/target graphs.  The negative test is
at `check_probe_semantic_samples.py:707-739`.

Likewise, `verify_k3p_probes.py:127-135` checks a restriction record's
self-hash, a literal `"isomorphic"` string, an integer label, and three
64-character strings; it neither reconstructs the restriction nor looks up
the restriction transport.  The five sampled rows below are semantically
correct under a fresh reconstruction, including their restriction hashes,
but the verifier's checks at `verify_k3p_probes.py:346-355,386-405,467-488`
do not establish this for all rows.  Whole-file and manifest hashes prevent an
uncoordinated edit, but do not supply missing semantics for a coherently
rehashed fake record.  The verifier's own docstring notes a separately
maintained graph-regeneration audit at lines 4-8; such a genuinely independent
cross-check could compensate, but `validate_transport` alone cannot.

### Medium verification gap (conditional dependency, not a counterexample)

The bridge exponent action is free for marked components and for every
unmarked degree \(d\geq3\), but an unmarked degree-two component has the
genuine stabilizer \((\tau,\tau^{-1})\).  Thus the topological exclusion in
`06_bridge_fibre.tex:51-57,78-81` is essential.  I verified the algebraic
side, including ranks and normalizers, but not the complete topology
enumeration proving that exclusion.  Evidence:
`check_bridge_and_gluing.py:32-52,96-102` and
`bridge_and_gluing_results.json`.

### Low / hypothesis-boundary observations (not defects)

- The tree--sunlet separator fails on excluded boundary cases: all six
  circuits vanish at an identity \(f=(1,1,1)\), and also at
  \(\lambda=0\).  This confirms that the strict-edge and
  \(0<\lambda<1\) hypotheses in `05_three_leaf_geometry.tex:53-63` do real
  work.  See `check_three_leaf_and_domains.py:182-195`.
- The principal domain is strictly larger than the continuous-time domain:
  \((c,g,t)=(2/5,2/5,1/10)\) has all inverse-Fourier probabilities positive
  but minimum CT composition margin \(-3/50\).  This is consistent with, and
  sharpens the reading of, `03_conventions_model.tex:95-135` and
  `02_main_theorems.tex:52`.
- The Krawczyk uniqueness is exactly local to the selected 15-variable scaled
  pivot slice.  It is not global parameter identifiability, as the article
  correctly says at `13_sharpness.tex:119-121`.

## Exact mathematical checks

### 1. Inverse Fourier domains and CT inclusion

Starting from the four inverse-Fourier entries in
`03_conventions_model.tex:95-102`, exact symbolic inversion recovers
\((c,g,t)\).  For the three nontrivial principal margins, I obtained

\[
\begin{aligned}
(1+c-g-t)-(1-g)(1-t)&=c-gt,\\
(1-c+g-t)-(1-c)(1-t)&=g-ct,\\
(1-c-g+t)-(1-c)(1-g)&=t-cg.
\end{aligned}
\]

Thus \(0<c,g,t<1\) and the three strict CT inequalities imply all four
inverse-Fourier probabilities are positive.  The exact proper-inclusion
example above has minimum CT margin \(-3/50\).  Evidence:
`check_three_leaf_and_domains.py:139-165`.

### 2. Tree--sunlet circuits and strict separator

I expanded the literal sunlet map
`05_three_leaf_geometry.tex:23-30` into the six cubic circuits at lines
`34-44`.  All six pullbacks independently factor into the displayed arm,
inheritance, composition-margin, and cross-edge factors; the complete exact
factor strings are in `three_leaf_and_domains_results.json`.

The strictness argument can be checked without numerics.  If, for example,
\(f_Cf_T-f_G\neq0\), simultaneous vanishing of its paired circuits forces
both
\(d_Ce_T=d_Te_Cf_G\) and
\(d_Ce_Tf_G=d_Te_C\), hence \(f_G^2=1\), impossible for a strict positive
edge.  The other two pairs are cyclic.  If all three composition margins
vanish, multiplying
\(f_G=f_Cf_T\), \(f_T=f_Cf_G\), and \(f_C=f_Gf_T\)
gives \(p=p^2\) for \(p=f_Cf_Gf_T\in(0,1)\), also impossible.  Therefore the
sum of squares is strictly positive.  As an adversarial supplement, 5,000
fixed-seed strict-principal rational/float trials found no zero (smallest
sampled sum of squares \(1.1415911152415768\times10^{-17}\)); that finite
sample is not being used as the proof.  Evidence:
`check_three_leaf_and_domains.py:50-77,115-138,166-195`.

### 3. The eight-term \(H_{14}\) pullback and the three closures

Using the literal eight-term polynomial at
`05_three_leaf_geometry.tex:104-118`, exact substitution annihilated it for
all six leaf permutations of the sunlet map, hence in particular for the three
orientation transports.  At the stated isotropic common tensor I independently
obtained normalized Jacobian rank 14 for all three cyclic orientations and a
nonzero exact minor of magnitude
\(1/760840571584512\) in each orientation.  (The sign depends on the transported
row/column order.)  The quartic gradient has exactly six nonzero entries, each
of absolute value \(1/6912\), so the common point is smooth on the
14-dimensional hypersurface.  Exact factorization over \(\mathbb Q\) left the
quartic unchanged, and treating it as linear in \(q_{0CC}\) gave
\(\gcd(\text{coefficient},\text{remainder})=1\); the primitive binomial
coefficient is irreducible.  Rank 14 plus containment and this irreducibility
give equality of each orientation's Zariski closure with \(H_{14}\), while the
constant-rank theorem gives the common relative analytic germ.  This checks
the chain in `05_three_leaf_geometry.tex:122-180`.  Evidence:
`check_three_leaf_and_domains.py:79-113,197-247`.

### 4. Bridge-fibre freeness and capped gluing

For unmarked degrees \(d=3,\ldots,12\), fresh exact exponent matrices have
one-sector rank \(d\), a selected determinant \(-2\), three-sector rank
\(3d\), and leading determinant \(-8\).  The pair-anchor square-root inverse
at `06_bridge_fibre.tex:71-76` was verified symbolically.  Marked
one-character anchors give an identity exponent matrix, and direct
three-sector tests on a three-component bridge path show exact cancellation
of all incidence gauges.

For gluing, the article's cap at
`10_global_classification.tex:30-60` reduces exactly to

\[
\left(\frac{\varepsilon}{U}-\frac{\varepsilon^2}{L^2}\right)
-\frac{7\varepsilon}{8U}
=\frac{\varepsilon}{8U}-\frac{\varepsilon^2}{L^2}\geq0
\quad\text{when}\quad
\varepsilon\leq\frac{L^2}{8U}.
\]

I also ran 1,000 fixed-seed exact-rational adversarial trials: all effective
and actual bridge spectra stayed physical; the smallest actual physical
margin was
\(710136325/572588765896\), and the smallest excess over the stated CT lower
bound was
\(67093889841/458071012716800\).  These samples supplement, rather than
replace, the exact inequality.  Evidence:
`check_bridge_and_gluing.py:14-102`.

### 5. Representative four-port obstructions — sampled, not complete

This check starts from the frozen literal source/target graphs and implements
the switching formula of `03_conventions_model.tex:104-122` without importing
the package compiler.  It confirms that the stored lock contains 14 unique
canonical records whose raw-member counts sum to 38, plus two pre-lock items,
matching `08_primitive_bounded.tex:98-162`.  **This is accounting of the stored
lock, not independent regeneration of the orbit space.**

Three representative quartics were expanded exactly.  In each case the target
pullback is the zero polynomial and a fresh strict-CT rational source point is
nonzero:

| Orbit | Independent source terms | CT margin | Exact source value |
|---|---:|---:|---|
| H21-01 | 1080 | \(1/361\) | \(-7176647562500561181712818480000/317066233566434024279851177356762764777\) |
| L20-01 | 90 | \(6/361\) | \(-48383982802757952000000/1912221247082067153383052514327\) |
| L23-02 | 32 | \(4/841\) | \(1614037051203423436800/2890325545652798745324691469\) |

The term counts are after my split-signature/effective-edge collection and are
not intended to reproduce a certificate's uncollected parameter convention.

At fresh strict-CT points, exact selected-projection Jacobian ranks and
nonzero rational minors were independently found for three rank orbits:
H21-02 \(11>10\), L20-02 \(14>12\), and L21a-02 \(11>10\).  The exact rows,
columns, determinants, and margins are in `four_port_spot_results.json`.

For upper bounds rather than merely sampled ranks, I checked eleven exact H21
target identities through the ten rational generators
\(U,V,Z,D,I,A_0,B_0,A,B,\rho\).  The only divisors are
\(e_{2C},e_{2G},D=di,I=i\), all strictly positive/nonzero on the stated strict
domain, so the saturation step is valid there.  Exact ordinary-sunlet
compression gives 12 generators for the checked L20-02 projection and 10 for
the checked L21a-02 projection.  These are genuine target upper bounds for the
three checked rank cases; a rank at one target point alone would not be.

**Completeness limitation:** I checked only 3 of 11 quartic cases (counting the
two sink swaps) and 3 of 5 rank cases, and did not regenerate all 2,814 target
completions, seven H21 double cosets, 38 raw transports, or the two sink swaps
claimed at `08_primitive_bounded.tex:185-211`.  Evidence:
`check_four_port_spots.py:37-292,328-500`.

### 6. Restoration, probe censuses, and transport samples

An independent streaming reader visited every stored row and recomputed
canonical self-hashes, ordered roots, references, and counts.  It found:

- restoration: 36,824 rows = 36,568 depth-one + 256 depth-two;
  proof-use counts 36,006 quartet, 614 tree--sunlet, 148 quadratic, 56
  quartic; 457 unique proofs; 2,540 roots; ordered root
  `c82e3c4678063ce2fc6be8180268437a2fa3228f7abe278d3e2aacd5333bb2a7`;
- one-port counts: 27,758 quartet, 99 tree--sunlet, 1,915 isomorphic, 192
  triangle; 2,107 equality survivors; ordered root
  `0fcf60ef05365d0a9fb4d260b2c724964eb689ad9c37785f98ed4be742997a2b`;
- two-port counts: 511,266 quartet, 576 tree--sunlet, 30,969 isomorphic,
  1,760 triangle; 544,571 raw pairs; ordered root
  `ae95e826a0be2c77196e90702b48225f28fba175a27d9d8b08ae36e0671c0a14`;
- 67,741 exact transports = 63,996 isomorphic + 3,745 triangle, ordered
  root
  `cc214fcfe782ea0ea9f8874a31675fbb46bc5035ef8a1c40ddef03a9b1578b3b`;
  4,379 restrictions, ordered root
  `a2a97296f236daa4c2236f99b290cb0fa6d026f90d7e190c22cc6e9e3b415787`.

Every stored transport's internal vertex-map injectivity, encoded mixed-edge
endpoint image, and (for triangle transports) recorded common-arrowhead
pattern passed.  This all-record streaming check did not bind those fields to
freshly reconstructed source/target graphs.  Representative exact
transport IDs are
`d36206c63e2262bc13495519b217d2e600b576e64ddcb603c34529dcd4025f8c`
(isomorphic) and
`2a903618bd1e5ef19734d1fd3831ed0d4add596ad2ec12826b213448722fc29a`
(triangle).  These match the article's claims at
`09_restoration_words.tex:17-54,65-98`.

**Producer limitation:** this is a full mechanical validation of the stored
ledgers, not an independent reconstruction of the restoration forest, probe
candidate graphs, or every polynomial pullback.  Evidence:
`check_census_and_transports.py:23-200`.

### 6a. Five semantic probe-row reconstructions and adversarial validator test

I then reconstructed five deliberately small records from the literal anchor
profiles, insertion sites, and labelled graph data without importing the
probe producer or atlas.  The inputs are the `four:raw2040` and
`four:raw2042` anchors at
`input_frozen/model_independent_topology_package/anchor_inputs/probe_input_contract.json:104,799`
and logical lines 1, 2, 123, and 146 of `probes/one_port_ledger.jsonl.gz`,
plus logical line 1 of both the two-port parent inventory and two-port ledger.
The independent implementation is at
`check_probe_semantic_samples.py:140-704`; only the isolated negative test
imports the verifier.

- One-port isomorphism, logical line 1: fresh graph construction and insertion
  reproduce child hashes
  `c239e6578ed65aff6e50402e751c7812b353ef88b075844bfd9fd75b43c09600`
  and
  `1159d4984558624da3c5197854b6b462347281b51d90ee03984cb40cf4cb172c`.
  The 12-vertex/13-edge mixed-graph map preserves labels, incidence, and every
  arrowhead and is exactly the parent map extended by the new stem and leaf.
- Ordinary-triangle relation, logical line 146: fresh child hashes are
  `af549c8ec7b084dbd9e6842aea1979a17a0db3aa5f5623c84653912ad64b6e8d`
  and
  `7d719cc986b8912c766c8606204e308c17336abb984f61b7c9a3a92ec89ffb68`.
  The underlying 12-vertex/13-edge incidence map and labels agree; outside
  the unique triangle all arrowheads agree, while each triangle has exactly
  two arrows entering the independently recovered common reticulation.
- Quartet separator, logical line 2: independent displayed-tree switching on
  quartet \(\{0,1,2,4\}\) gives source splits
  \(02\mid14,04\mid12\) and target splits
  \(01\mid24,04\mid12\), exactly reconstructing a genuine mismatch before
  comparison with proof ID
  `Q:d50e67ad80c853ec5b9e9b2092b23740bd515a6ccdf515f2aac266847eeafd36`.
- Tree--sunlet separator, logical line 123: restricting to
  \(\{0,1,4\}\) independently gives a three-edge tree on the source and a
  six-node/six-edge ordinary sunlet with degree sequence
  \((1,1,1,3,3,3)\) on the target.  A fresh literal K3P switching compiler
  makes all six source circuits coefficientwise zero and all six target
  circuits nonzero.  At the strict-CT point with every edge spectrum
  \((1/2,1/2,1/2)\) and inheritance \(1/3\), every circuit equals
  \(-1/36864\), so \(\mathcal S=1/226492416>0\).
- Two-port parent restriction, logical line 1: the 13-by-13 second-site
  inventory gives 169 pairs; fresh second insertion reproduces child hashes
  `4c8dc31cbaa2c66650dafe997d8e5b883fd211163e3f32d67f6c69c79e4bb839`
  and
  `b0fa331d1f9f9f9c74570beef295610ec0adfdcbf87be58184c6c270046718b0`.
  Removing label 5 and suppressing its stem exactly recovers the one-port
  parent on each side, reconstructs both stored mixed-graph and restriction
  transport hashes, and restricts the child transport to the stored parent
  transport.

These five exact successes are positive sample evidence only.  They do **not**
establish semantic correctness or completeness of all
\(29,964+544,571=574,535\) one-/two-port ledger rows.  Exact output:
`probe_semantic_sample_results.json`; code:
`check_probe_semantic_samples.py:742-963`.

### 7. Krawczyk inclusion, interval ranks, and margins

I wrote a self-contained exact-rational interval implementation and rebuilt
both 32-parameter network maps and their interval Jacobians directly from the
literal DAGs.  The stored center residual and point Jacobian were reproduced
exactly before comparison.  Fresh Gauss--Jordan inversion and interval
evaluation give:

- largest normalized Krawczyk distance
  \(9.740999384091\times10^{-41}\), exact-fraction SHA-256
  `333c16e167e0c10879c2105210e72bca92fd397a365eaf06eb3bee51b815fb2a`;
- \(\lVert I-YJ(X)\rVert_\infty=
  8.077023076476\times10^{-47}<1\), exact-fraction SHA-256
  `42bc1b9804a1f28fb8037af5f38cdd9f8a9af7486757688055ab7e097fcc2d07`;
- strict self-inclusion, hence existence and uniqueness in the 15-dimensional
  scaled pivot slice box;
- point equality-Jacobian determinant
  \(-3.056932495160\times10^{-2}\), exact-fraction SHA-256
  `ec778fa5ec3493bef3be29c1e17af08b7b5e469a5bdd76d8f00e50f2db6368e1`;
- rank-15 Neumann bounds throughout the box
  \(1.543152096600\times10^{-45}\) for \(W\) and
  \(4.582719524575\times10^{-45}\) for \(W'\);
- CT lower bounds
  \(4.964484595360\times10^{-10}\) for \(W\) and
  \(1.395195552339\times10^{-9}\) for \(W'\), with every eigenvalue,
  inheritance, and transition-probability lower bound positive.

The full exact-fraction digit counts and hashes for the rank determinants,
Neumann bounds, and physical margins are in
`krawczyk_literal_results.json`.  This independently confirms the numerical
claims at `13_sharpness.tex:66-117`.

**Input boundary:** the rational center, frozen coordinates, pivot scaling,
box radius, and selected rank columns are certificate inputs; the polynomial
maps, point/interval Jacobians, inverse, Krawczyk operator, rank intervals, and
physical inequalities were rebuilt.  Evidence:
`check_krawczyk_literal.py:33-407`.

### 8. Six-dimensional cherry inverse

For each sector, direct differentiation of
\(R_h=u_h/v_h\), \(P_h=u_hv_h\) gives a 2-by-2 determinant
\(2u_h/v_h\).  The three blocks therefore give exactly

\[
\det\frac{\partial(R_C,P_C,R_G,P_G,R_T,P_T)}
{\partial(u_C,v_C,u_G,v_G,u_T,v_T)}
=\frac{8u_Cu_Gu_T}{v_Cv_Gv_T}.
\]

At the article's point the determinant is exactly \(176/25\); the minimum CT
margins are \(22/105\) for \(u\) and \(157/693\) for \(v\).  The positive
inverse is independently recovered as
\(u_h=\sqrt{R_hP_h}\), \(v_h=\sqrt{P_h/R_h}\), confirming
`13_sharpness.tex:123-178`.  Evidence:
`check_three_leaf_and_domains.py:249-274`.

## Reproduction

Run from this directory with SymPy 1.14:

```text
/Users/alec/Documents/Math/k3p_level2_identifiability_final/.venv/bin/python check_three_leaf_and_domains.py
/Users/alec/Documents/Math/k3p_level2_identifiability_final/.venv/bin/python check_bridge_and_gluing.py
/Users/alec/Documents/Math/k3p_level2_identifiability_final/.venv/bin/python check_four_port_spots.py
/Users/alec/Documents/Math/k3p_level2_identifiability_final/.venv/bin/python check_krawczyk_literal.py
/Users/alec/Documents/Math/k3p_level2_identifiability_final/.venv/bin/python check_census_and_transports.py
/Users/alec/Documents/Math/k3p_level2_identifiability_final/.venv/bin/python check_probe_semantic_samples.py
```

The saved `*.stdout.txt` files are byte-for-byte identical to their
corresponding `*_results.json` files.  Exact hashes are in
`SHA256SUMS.txt`.
