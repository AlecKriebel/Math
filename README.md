# Hadamard branch and two local stashes

This archive preserves the original commit IDs from the November 24, 2026 local repository. The Git bundle is split into parts to fit GitHub’s ordinary file limit. The prerequisite is commit `6035382b18c4aa0969e999959feb034fccfc9d59` on GitHub’s `codex/h668-theory` branch.

Clone this archival branch and check both the parts and the reassembled bundle.

```sh
git clone --single-branch --branch archive/local-math-2026-11-24/h668-and-stashes https://github.com/AlecKriebel/Math.git math-history-parts
cd math-history-parts
shasum -a 256 -c SHA256SUMS
cat h668-and-stashes.bundle.part-* > h668-and-stashes.bundle
shasum -a 256 -c BUNDLE.sha256
```

In a Math clone that has the prerequisite commit, import the saved refs. The recovered branch and stash refs use new names so they can coexist with existing local work.

```sh
git fetch origin refs/heads/codex/h668-theory
git bundle verify /absolute/path/to/math-history-parts/h668-and-stashes.bundle
git fetch /absolute/path/to/math-history-parts/h668-and-stashes.bundle \
  refs/heads/codex/h668-theory:refs/heads/recovered-h668-theory \
  refs/archive/stash-0:refs/archive/recovered-stash-0 \
  refs/archive/stash-1:refs/archive/recovered-stash-1
```

The original branch tip is `c8e5db68f225bfe0195cf79870c18c6e2018fb39`. The saved stashes are `15d74cc94e1867b2ca009dd3b8194c48ead5f42d` and `9f116f631c0feabf231c1097eb7afb7fe390f567`.
