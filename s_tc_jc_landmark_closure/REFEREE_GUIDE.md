# Specialist referee guide

Status: **PROVED — final independent whole-proof verdict VERIFIED**

## Headline

The paper claims a sharp boundary under one exact standard convention:

1. standard semi-directed strongly tree-child binary level-2 JC networks are
   generically identifiable modulo ordinary triangle redirection;
2. no proper one-sided generic stochastic containment exists in that class;
3. the result is sharp because the immediately larger weakly tree-child class
   has an explicit all-taxa non-`T` ambiguity.

The positive theorem concerns the simple reticulation-preserving `sd_0`
convention.  It does not quantify over rooted presentations that become
simple only after broader parallel-edge or degree-two cleanup.

## Suggested reading order

1. `source/paper/main.tex`, Sections 2--5: definitions, cores, cuts, and the
   corrected bridge quotient.
2. Section 6: the complete local theorem and the exact finite lemma.
3. Section 7: the short local-to-global synthesis.
4. Section 9: the independently frozen weak-class sharpness theorem.
5. `THEOREM_CERTIFICATE_CROSSWALK.md` for the exact artifacts behind each
   computer-assisted statement.
6. `reviews/final_outcome_p_referee_v2/REPORT.md` for the terminal adversarial
   verdict and preserved release-level defects.

## Five delicate points

### 1. The bridge fiber

The observable fiber is the full incidence action

```text
P_u -> a_(u,e) P_u,
P_v -> a_(v,e) P_v,
x_e -> x_e/(a_(u,e)a_(v,e)).
```

No physical bridge multiplier is identified.  The regression
`(1/2,1/2,1/2)` versus `(3/5,3/5,25/72)` is included to prevent reintroduction
of the withdrawn reciprocal-only chart.

### 2. One-sided cut preservation

The split theorem is pointwise throughout the open parameter domain.  Hence
both cut inclusions follow on the shared source-open set even though
`preceq_JC` is not reversed.  The two-active crossing is the inequality
`aA >= bcBC > z^2bcBC` after exact minors force both endpoint `F` values to
zero.

### 3. The local finite theorem

The finite object is a decorated directed source-target relation, not a
target graph or signature hash.  It includes both incoming roles, all port
matches, omitted-role placeholders, and explicit transports.  The theta-2
gate's `18+42+132` partition is the final repair of the previous hidden
presentation mismatch.

### 4. Marginals are never lifted

The complete source-target relation is fixed before restoration.  Every
larger prefix is a direct marginal of that full containment.  The proof never
infers containment of `Q union D` from containment of `Q`.

### 5. What ordinary `T` means

The three orientations share one full-dimensional regular local germ.
Neither the theorem nor the reconstruction algorithm asserts equality of
their complete open images or that every orientation realizes every generic
point.

## Reproduction

From a fresh repository clone:

```bash
bash s_tc_jc_landmark_closure/reproducibility/verify_quick.sh
bash s_tc_jc_landmark_closure/reproducibility/verify_full.sh
bash s_tc_jc_landmark_closure/reproducibility/verify_regenerate_all.sh
```

The scripts create a pinned local virtual environment if needed.  The
regeneration command is bounded by the structurally proved support universe;
it does not launch a broad topology search.

## Scope of novelty

The result extends the triangle-free strongly tree-child level-2 JC theorem
to triangles modulo their exact ordinary redirection, strengthens the
conclusion to classify one-sided generic containment, and combines it with an
exact weak-class sharpness family.  The release does not claim K2P/K3P
classification, level 3, unrestricted cleanup conventions, physical branch
parameter identifiability, or a minimal exceptional locus.
