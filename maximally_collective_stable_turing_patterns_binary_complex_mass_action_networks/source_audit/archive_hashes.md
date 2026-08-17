# Frozen historical-lineage archives

| Required filename | SHA-256 |
|---|---|
| `qbio_mass_action_turing_final_flagship.zip` | `e3c116643e566f905ae72aa2556874319db1845d88520e646c2c88f295dd1e0e` |
| `qbio_mass_action_turing_all_spectrum_paper.zip` | `56db8bb8b3e2f23bfa4066a7f1a0c6432f75e50cf71ae742713d23d406cf9b96` |
| `qbio_mass_action_turing_all_spectrum_stable.zip` | `d084e646181f455b80aa336e8448f52cdb9afdb6e3351575f1442595ef65e861` |
| `qbio_mass_action_turing_diffusion_design.zip` | `61d9ff96b0c5bbf74d80bc2b640afcdc23a7f429e8abb0478cd35903b3df0d90` |
| `qbio_mass_action_turing_nonlinear_frontier.zip` | `816dbb043f859d60cf6a32af45bfc7ab2ec46edd75cf51b56eae5bed5345077c` |

These archives record lineage; they are not inputs to the current theorem
verifiers, numerical source, document builds, or packages. The top-level replay
checks all five hashes once, during startup and before it opens
`release/replay.log`. It does not extract the archives. The portable replay in
`public/repository` has no dependency on them.
