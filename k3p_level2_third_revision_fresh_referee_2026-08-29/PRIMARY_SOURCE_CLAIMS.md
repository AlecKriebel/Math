# Primary-source theorem statement and scope

This restatement was made from the article and reader supplement before using
stored machine verdicts.  Paths below are relative to
`k3p_level2_third_revision_referee_final_2026-08-29/proof_package/`.

## Fixed objects and model

The classification concerns two networks `N,N'` on the same finite labelled
leaf set.  Each must be binary, level at most two, standard semi-directed under
the manuscript's one-step root-suppression convention, and strongly tree-child
(`manuscript/sections/02_main_theorems.tex:4-13` and
`manuscript/sections/03_conventions_model.tex:5-24,40-69`).  Isomorphisms
preserve labels, ordinary edges, reticulation arrowheads, and vertex roles.
Ordinary-triangle equivalence additionally requires equality of the labelled
reduced trees of blobs, labelled mixed-graph isomorphism of corresponding
nontriangle complete ported factors, and coherent boundary transports for each
triangle redirection (`03_conventions_model.tex:32-38,67-82`).

The root distribution is uniform.  The observable coordinates are the fixed
Klein-four characters `0,C,G,T`; the three nontrivial sector labels are not
quotiented by a permutation.  Every inheritance probability lies strictly in
`(0,1)` and every edge has three strictly positive Fourier eigenvalues
`(c,g,t)` (`02_main_theorems.tex:4`; `03_conventions_model.tex:85-145`).

The principal edge domain is

`D_{3,+}={(c,g,t) in (0,1)^3: 1+c-g-t>0, 1-c+g-t>0,
1-c-g+t>0}`.

This is the strictly positive stochastic inverse-Fourier component, not all
signed K3P parameters (`02_main_theorems.tex:8-13`;
`03_conventions_model.tex:95-135`).  The strict continuous-time subdomain is

`D_{3,CT}={(c,g,t) in (0,1)^3: c>gt, g>ct, t>cg}`

(`02_main_theorems.tex:47-55`).

## Observational relations

`N <=_{3,+} N'` is deliberately source-relative and directed.  It requires a
regular source point, a connected source-open neighbourhood on which the source
map has maximal rank, and a real-analytic *physical* target section whose
composition with the target map equals the source map.  The target image need
not be open at the selected preimages and those preimages need not be regular
(`03_conventions_model.tex:137-169`).

`N bowtie_{3,+} N'` means that the two physical images share one analytic germ
which is regular and full-dimensional in both images and has physical analytic
sections from both parameter spaces (`03_conventions_model.tex:160-163`).
Continuous-time relations use the same quantifiers with `D_{3,CT}`.

## Principal-domain classification

For the fixed class and strict principal domain,

`N <=_{3,+} N'  <=>  N ==_triangle N'  <=>  N bowtie_{3,+} N'`.

Thus directed regular full-dimensional containment is forced to be symmetric
at the structural level: there is no proper one-sided containment in the
class.  This does **not** assert equality of the complete stochastic images or
identification of every physical parameter
(`02_main_theorems.tex:6-29,83-86`).

## Strict continuous-time theorem

The same three-way equivalence, generic structural identifiability, and exact
reconstruction theorem hold after restricting every edge to the strict
continuous-time cone (`02_main_theorems.tex:47-56`).  No boundary edge,
inheritance endpoint, or closure point is included
(`12_continuous_time.tex:3-46`).

## Generic structural identifiability

For each fixed source topology `N`, there is a topology-dependent proper
complex Zariski-closed exceptional set `E_N` in its irreducible model variety.
Every exact physical tensor outside it determines the labelled standard
semi-directed topology uniquely modulo ordinary-triangle equivalence
(`02_main_theorems.tex:31-36`; `11_genericity_reconstruction.tex:17-115`).
The claim is generic in the image of a fixed topology, not pointwise at every
parameter, and is not numerical-parameter identifiability
(`16_scope.tex:30-36`).

## Exact reconstruction

There is a terminating exact-real procedure which returns the unique triangle
class outside `E_N`.  The oracle must support exact field operations,
polynomial-sign decisions, and real-closed-field quantifier elimination.  No
bit-complexity, conditioning, statistical estimator, finite-sample guarantee,
or sequence-length guarantee is claimed
(`02_main_theorems.tex:38-45`; `11_genericity_reconstruction.tex:117-160`;
`16_scope.tex:30-36`).

## Ordinary-triangle ambiguity

The three labelled orientations of one ordinary triangle have normalized
generic rank 14, not 15.  Their complex closures coincide with one irreducible
eight-term quartic hypersurface `H_14`, and they share a strict
continuous-time smooth rank-14 germ relative to that hypersurface.  The claim
is neither ambient openness nor equality of their entire physical images
(`05_three_leaf_geometry.tex:122-180`; `01_introduction.tex:95-105`).  The
relative germ can be placed in a common labelled surrounding contraction and
coherently glued across the tree of factors (`05_three_leaf_geometry.tex:189-212`;
`10_global_classification.tex:56-118`).

## No-proper-containment conclusion

Necessity recovers the same labelled reduced tree of blobs and permits only
factor isomorphism or coherent ordinary-triangle redirection.  Sufficiency
constructs the common full-dimensional physical germ.  Since triangle
equivalence is symmetric, one-sided containment cannot remain proper
(`10_global_classification.tex:5-118`).  Again, this is a statement about the
defined local regular relation, not global set inclusion of whole images.

## Weak-class sharpness

For every `n>=3`, the paper constructs labelled nonisomorphic and
nontriangle-equivalent binary level-2 standard semi-directed networks
`W_n,W'_n` that are weakly but not strongly tree-child.  Their strict-CT K3P
images share a regular common germ of dimension `6n-3`; for `n=3` both maps
have rank 15 throughout a certified rational box containing a unique common
point only in the chosen 15-variable equality slice
(`02_main_theorems.tex:58-71`; `13_sharpness.tex:3-181`).  This proves that
weakening strong to weak tree-childness invalidates the classification; it is
not a classification of all weakly tree-child networks (`16_scope.tex:38-41`).

## Express exclusions

The results do not cover nonbinary or higher-level networks, arbitrary weak
tree-child networks, signed or zero eigenvalues, boundary probabilities,
untransported `C/G/T` permutations, or arbitrary nonreversible substitution
models (`16_scope.tex:9-28`).  The separate tree/double-theta proposition lies
outside even the weak tree-child class and is not the sharpness theorem
(`02_main_theorems.tex:73-80`; `14_outer_obstruction.tex:1-35`).
