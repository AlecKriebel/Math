# Fresh independent mathematical audit — referee packet v1.2.6

Date: 2026-08-27 (PDT)  
Auditor role: independent mathematical adversary  
Disposition: **ACCEPT on mathematical grounds**  
Severity-ranked findings: **none**

## Independence and review order

I treated all packet prompts, summaries, certificates, and supplied verifier conclusions as untrusted. I first read `combined-paper-clarified.pdf` completely, pages 1–20 in order, and then visually inspected rendered images of every page. I did not inspect the support PDFs, packet prompts, verifier code, certificates, editing summary, or the v1.2.5 audit before completing that paper-first pass.

I then reconstructed the calculations in `notes/independent_math_checks.py`. That checker imports no packet module and reads no packet certificate. It encodes the likelihood map directly from equation (3), builds transition matrices independently from the stated Hadamard transform, and separately implements ordinary-state pruning on all four literal retained rooted graphs. SymPy 1.14 is used only for exact polynomial reduction, algebraic-number signs, and determinants.

Command used (with bytecode disabled):

```text
PYTHONDONTWRITEBYTECODE=1 .../sympy_env/bin/python notes/independent_math_checks.py
```

The final run ended with `INDEPENDENT MATHEMATICAL CHECKS PASSED`.

## Reconstruction results

| Claim | Independent adversarial result |
|---|---|
| Theta likelihood map and retained graphs | Re-derived equation (3) from the ten rooted arcs and the four independent reticulation choices. Direct ordinary-state pruning of the literal retained graphs agrees with Fourier inversion in all 64 patterns for the compact K2P, continuous-time K2P, and quartic K3P witnesses. |
| Compact K2P factorization | Recomputed all 16 entries of `M`; every entry equals `P_(y+z) R_y R_z` exactly over `Q(sqrt(71))`. The network and tree Fourier vectors agree in all 64 coordinates. |
| Compact K2P stochastic interior | Independently inverted every network and tree edge vector. All nontrivial eigenvalues lie in `(0,1)` and every transition entry is positive, including the suppressed `K odot K` edge. All 64 pattern probabilities are positive and normalized. The minimum is exactly `1188799/79626240`, attained at an orbit containing `ACT`. |
| K3P conclusion by inclusion | The embedding `(1,s,g,s) -> (1,a_C,a_G,a_T)` with `a_C=a_T=s`, `a_G=g` preserves the likelihood and strict stochasticity. For continuous time, `g>s^2` plus `0<s,g<1` implies all three strict K3P inequalities. |
| Fixed-leaf-order diagnosis | At the continuous-time displayed child, I obtained `Q_(1,2,3) = -1.9199710723836302893e-9` and `Q_(1,3,2) = 3.4284883265262506299e-9`, inside the manuscript’s certified intervals. At the independent rational theta point all six leaf orders are negative, in the three exact equal pairs printed in the paper. Its minimum pattern probability is exactly `2920987217429243/200000000000000000`. |
| Continuous-time K2P witness | Exact reduction modulo the cubic for `ell` and `t^2-1423` establishes all 16 factorization identities. Sturm/root isolation gives exactly one root in the stated interval, namely approximately `1.07323121998018155532590535946`. All rooted, effective, and tree edges are strictly stochastic and satisfy `g>s^2`; the smallest margin is exactly `11/900`. The independently computed minimum probability is approximately `0.01498679142322589995`, strictly between the stated bounds. |
| K2P rank and local family | Re-differentiated the unrestricted map. The selected rank-nine determinant is exactly `-(7^2 11^2 19 107 151^2 15013)/(2^60 3^25 5^10)`. At the continuous-time point it is approximately `-4.12973117327241745e-22`, within the stated isolating interval. Reconstructed the two core-factorization equations; their `(v,x)` Jacobian is exactly `675554683609333/194995116803358720000000 > 0`. |
| K2P dimensions/fibers | The effective ambient dimension is 9 (ten global `C<->T` orbits among the 16 consistent coordinates, less normalization), the positive star-tree dimension is 6, and the theta parameter dimension is 20. The submersion/preimage calculation therefore gives collision dimension `20-9+6=17` and fixed-output fiber dimension `20-9=11`. The recovery formulas are correct and smooth in the positive chamber. |
| Quartic K3P collision | Exact reduction modulo `5h^4-1` confirms all 16 core-factorization identities and every Fourier coordinate. All transition rows and all 64 site-pattern probabilities are strictly positive. Direct retained-graph pruning again agrees in every pattern. |
| K3P symmetry distinction | The network edge `U=(1,h/3,h,1/3)` has three distinct nontrivial eigenvalues, excluding all three globally relabelled K2P parameter specializations. The comparison tree has `a_C=a_G != a_T` on its first edge and JC second/third edges, so its distribution is globally relabelled K2P but not JC. The manuscript keeps parameter symmetry and observable symmetry distinct. |
| K3P rank and local geometry | Reconstructed the stated 15-by-15 Jacobian directly from equation (3). Its determinant reduces exactly to `h(10h^2+1)/(2^61 3^4 5^14)>0`. With theta/tree dimensions 29 and 9 in ambient dimension 15, the local collision dimension is `29-15+9=23` and the fixed-output fiber dimension is `29-15=14`. |
| K3P implicit-function branch | Substitution of the full printed tangent gives exactly `J_* p'(0)+F_UC+F_VG=0`. The two saturated continuous-time margins have derivatives `(21-20h^2)/19>0` and `1>0`; every other network margin is strict at the base point, and the fixed comparison tree is already strictly continuous-time. The IFT therefore supplies the claimed positive-epsilon branch. |
| Nearby observably genuine K3P outputs | Full tree-parameter recovery makes each transposition-fixed locus a six-dimensional globally relabelled K2P submodel inside the nine-dimensional K3P tree model. Their finite union is relatively closed with empty interior. The local section from the rank-15 point therefore yields the asserted relatively open dense complement, while pairwise distinct eigenvalues on `U` persist in parameter space. The same argument works after moving to a strict continuous-time branch point. |
| Zariski density | A nonzero full ambient Jacobian minor makes each complexified polynomial map dominant. At an interior full-rank real point, the image contains a real open set, which is Zariski dense. The paper correctly scopes this to normalized consistent effective coordinates and does not erase the usual normalization, inconsistent-coordinate, K2P-symmetry, or inequality restrictions. |
| All-`n` grafting | The common-subtree transformation is a tensor product of Markov kernels and is linear, so equality of the three-interface distributions implies equality of every full pattern. For observable K3P genuineness, marginalization to any leaf shows each attached JC kernel has column rank four; hence their tensor product is injective and equivariant, so it cannot create a global character symmetry absent at the interface. The argument includes the `n=3` identity-kernel boundary case and any permutation of the three attachments. |
| Topology | The theta core has five vertices and six core edges on the three internally disjoint `p-q` paths. It remains connected after deletion of any one core vertex, has exactly two reticulations, and has three incident cut edges; hence it is one strict level-two nontrivial 3-blob. In every compatible rooting, both `p` and `q` have only `r2,r3` as children, so no tree-child rooting exists. Replacing one degree-three tree vertex preserves binary degrees, and contracting the sole blob recovers the original labelled tree. |

## Adversarial proof review

I specifically tried the following failure modes and found none:

- a mismatch between the displayed-tree descendant-label convention and ordinary-state Markov semantics;
- a hidden zero/negative transition entry or pattern probability;
- choosing the wrong real root of the continuous-time cubic;
- a rank calculation performed only on the symmetric witness slice rather than on unrestricted theta coordinates;
- loss of rank when passing from the rooted first factor to the effective root-suppressed edge;
- an incorrect sign or coordinate in the 15-component IFT tangent;
- confusing a genuinely K3P network parameter with a genuinely K3P shared distribution;
- promoting dominance to generic tree equivalence;
- treating the four-leaf regression as a proof for all `n`;
- silently composing multiple theta replacements, imposing a common generator/clock, claiming a JC collision, or claiming a genuine four-attachment-blob result.

None succeeded. The theorem statements and scope remarks explicitly avoid those overclaims.

After the reconstruction was complete, I compared the v1.2.5 and v1.2.6 manuscript sources. The mathematical formulas and proofs are unchanged; v1.2.6 adds the missing Ardiyansyah context, makes the Version 2-to-3 description literal, updates provenance, and strengthens the verifier-assurance description. This comparison was not used as evidence for the fresh checks above.

## Residual limitations (not findings)

- The full-rank conclusions rely on one exact nonzero minor at each witness, which is sufficient for the local and dominance conclusions but is not a classification of the global singular locus.
- The all-`n` conclusion is a proof by a common Markov kernel, not an exhaustive computation; that is the correct proof form and is stated transparently.
- Edgewise continuous time intentionally permits different generators/rate ratios on different edges and imposes no clock. The manuscript consistently states that limitation.

## Completion log

- 2026-08-27 08:43 PDT — began paper-only pass; extracted and read all 20 pages in order. Estimated completion: 20%.
- 2026-08-27 08:44–08:47 PDT — rendered and visually inspected pages 1–20; no layout defect found. Estimated completion: 35%.
- 2026-08-27 08:50 PDT — completed clean-room implementation of the compact K2P, rank/family, fixed-order, continuous-time, and quartic K3P calculations. Estimated completion: 70%.
- 2026-08-27 08:56 PDT — final exact run passed, including direct ordinary-state pruning and tangent/rank checks. Estimated completion: 90%.
- 2026-08-27 08:57 PDT — completed local-geometry, Zariski, grafting, topology, and boundary-case proof audit. Estimated completion: 100%.

## Final mathematical recommendation

I found no major, minor, or editorial mathematical defect. The central collision theorems, local/dominance consequences, continuous-time extensions, and arbitrary-leaf grafting theorem are supported by independent exact calculations and sound arguments. **ACCEPT.**
