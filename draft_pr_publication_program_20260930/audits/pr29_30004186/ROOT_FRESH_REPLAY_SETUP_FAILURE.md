# Root isolated-replay setup failure

2026-10-02T00:27:27.357718+00:00 — The first fresh-gate replay stopped in its copied primary source control. Root had made fake-root .git a gitdir TEXT file. The unchanged reproducer creates a second-depth gitdir reference to ROOT/.git, which is then a FILE rather than a Git directory; Git correctly rejected that nested reference. No scientific assertion failed and no closed input was altered. The entire failed run, stdout/stderr and copied programs remain in owned ignored tmp/root_fresh_complete_tree/.../final_adversary/tmp/replay_20261002T002610801204.

Correction: replace only the outer fake-root .git with a directory symlink to the actual Git directory; the unchanged code uses immutable reads only. Retain failure; fresh successful run still required.
