# Directive-by-directive change log

1. **Conventional paper.** Replaced the seven-page status report by a
   conventional journal article with abstract, introduction, definitions,
   numbered results, full proofs, computation section, discussion,
   declarations, appendices, and bibliography. Pipeline labels and gate
   language were removed.
2. **Prior work.** Added a comparison table, audited current versions, and
   attributed `F_abc` to Englander et al. The new contribution is its
   restored-support use in the residual seven-port atlas.
3. **Definitions.** Added rooted and standard semi-directed networks,
   admissible rootings, `R_TC/W_TC/S_TC`, blobs, bridges, ports, cores, level,
   triangle redirection, JC Fourier coordinates, images, closures, regularity,
   overlap, one-sided containment, and generic identifiability.
4. **Load-bearing proofs.** Expanded bridge peeling and gauges, directed local
   product localization, semialgebraic genericity, bounded-support recovery,
   cut preservation including two active endpoints, dimensions, and contextual
   triangle gluing.
5. **Sharpness.** Added the complete Theta networks, class membership,
   non-`T` proof, quadratic common point, all Fourier coordinates, Jacobian
   factors, leaf substitution, analytic inverse, and the `2n` dimension proof.
6. **Computational supplement.** Added primitive graph/tensor generators for
   five-, six-, and seven-port theta structures, all bounded cycle atlases,
   complete directed relation universes, seven-port residuals, and cut types;
   added independent reviewers, pinned environments, licenses, runtimes,
   commands, and manifests.
7. **Framing.** Every headline retains JC, genericity, standard semi-directed
   `S_TC`, level 2, and quotient by `T`. The former one-triangle-per-blob
   condition is now proved automatic already for `W_TC`; complete stochastic
   image equality is not asserted.
8. **Figures.** Added eight original TikZ figures for reduction/classes,
   bridge factorization, cycle/theta cores, automatic multi-triangle exclusion,
   triangle redirection, residual orbits, cut cases, and Theta sharpness/leaf
   substitution.
9. **AI disclosure.** Added named-system disclosure, human accountability,
   author contribution, competing-interest, and archive statements. No AI
   system is an author.
10. **Release artifacts.** Added journal PDF, complete source, figures,
    reproducibility archive, clean transcripts, crosswalk, novelty audit,
    cover letters, referee guide, and submission checklist.
11. **Pre-submission strengthening.** Proved that the only possible binary
    level-2 two-triangle core is the `(1,2,2)` theta and that it has no
    tree-child rooting. Independent Python and C++ censuses reproduce 25
    binary acyclic rooted presentations in seven symmetry orbits and zero
    tree-child cases. The headline theorem therefore covers all binary
    standard semi-directed `S_TC` level-2 networks.

## Post-release adversarial corrections (version 1.1.1)

- Narrowed the reconstruction theorem to a canonical structural topology
  modulo ordinary triangle redirection. The optional output is now explicitly
  the structural `T`-equivalence class, not the set of stochastic models
  containing one fixed input distribution.
- Added a formal remark separating structural reconstruction from the
  input-specific semialgebraic triangle-orientation membership problem.
- Repaired the converse sentence in the local strong-tree-child criterion so
  it no longer assumes that a reticulation child edge is ordinary.
- Repaired the corresponding external-arm sentence in the embedded-triangle
  lemma using the local strong criterion.
- Replaced wording that could imply every generic point has an ambiguous
  triangle orientation by the precise full-dimensional-compatibility claim.
- Replaced "independent adversarial reviewers" by an explicit description of
  adversarial AI-assisted review processes and separately implemented checks.
- Added Muhammad Ardiyansyah's 2021 Fourier-invariant level-2 distinguishability
  paper to the introduction, prior-work table, bibliography, referee guide, and
  novelty audit.
- Rebuilt Figures 1, 6, and 7 to remove all text, border, formula, and diagram
  overlaps; replaced the earlier inaccurate visual-inspection report.
- Added explicit unchecked human actions for specialist proof review and
  persistent public archiving. No DOI or human review is fabricated in this
  local release.
