# Root-only one-leaf publication procedure — NOT EXECUTED

This packet authorizes preparation only. Root must read the complete candidate, report, literal custom verdict, verifier, expected scope and this procedure, then separately authorize applying this exact candidate. No step below that creates an object, commit or ref has been executed. This is an isolated remote Git Data procedure; it needs no checkout, local index, local HEAD, local ref, branch creation, full repository download, or source build. All publication writes are confined to the one specified remote leaf via a direct-child commit on main.

## 1. Verify this sealed packet locally

Exact read-only command:

```sh
node /Users/alec/Documents/Math/research_website_catalogue_20261024/redirects/strict-gap-redirect-sol-20261115/verify_redirect.mjs
```

Expected PASS includes 12 executed URL cases, 3 rejected controls and four verified original Git tree hashes. The candidate is `index.html`, 838 bytes, SHA256 `dedb9326ddf053603601dc22355b00c555ed1ec05a8767b6119bcec03455965c`, Git blob `7b7411fefe1638f4721bc2180486574497f69ab0`. Candidate bytes must not be re-serialized, have another newline appended, or be edited during application.

## 2. After separate root approval, capture the THEN-CURRENT parent

Create a NEW root-owned application evidence directory outside this sealed preparation folder. Preserve complete connector results, including failures, under its `raw/` child. Use only read-only connected GitHub `mcp__codex_apps__github_fetch` calls at this stage. The following URLs are exact patterns; substitute only returned actual SHAs, never a stale commit guess:

1. `https://api.github.com/repos/AlecKriebel/Math/git/ref/heads/main` → `raw/remote-ref.json`.
2. `https://api.github.com/repos/AlecKriebel/Math/git/commits/<actual ref.object.sha>` → `raw/remote-commit.json`.
3. `https://api.github.com/repos/AlecKriebel/Math/git/trees/<actual commit.tree.sha>` → `raw/tree-root.json`.
4. From the root entry named `docs`, GET its exact tree SHA → `raw/tree-docs.json`.
5. From its entry named `papers`, GET its exact tree SHA → `raw/tree-papers.json`.
6. From its entry named `strict-dirichlet-gap`, GET its exact tree SHA → `raw/tree-leaf.json`.
7. Require its `index.html` entry to be a regular `100644` blob exactly `b9705a518f76839427ff4f1e0bded6bdf95a7894`. GET `https://api.github.com/repos/AlecKriebel/Math/git/blobs/b9705a518f76839427ff4f1e0bded6bdf95a7894` → `raw/old-blob.json`. This connector returns decoded UTF-8 HTML for that blob endpoint, not a native JSON blob schema; retain its whole result without normalizing it. The helper verifies the decoded bytes against the actual Git blob hash.
8. GET the same main ref again → `raw/remote-ref-end.json`. Require both ref captures and the commit to name the same parent. If the parent changes, preserve the attempted capture and start another bounded capture in a new directory. Do not overwrite or silently mix old/fresh trees.

The API tree responses must be non-recursive, complete and `truncated:false`. The helper recomputes the SHA of each original native tree and verifies all four ancestry links. It needs no child blob downloads or full root-tree enumeration: unchanged sibling tree SHAs preserve every descendant.

The preparation captured parent `3d62606656a8db0ed9331246754e12c4e7728b87` and root `1259b74822e61483b0ca056e53d1a739b58467de`. These are HISTORICAL CAPTURE IDENTITIES, not permission to overwrite a later parent. If another actor has already replaced the target leaf, stop; do not auto-accept another blob as a new base.

## 3. Generate exact structured tool arguments without publication

For an application directory chosen by root, run the verifier using its absolute `raw/` path. The following is the command template; replace `APPLICATION_RAW_ABSOLUTE_PATH` with that newly captured path:

```sh
node /Users/alec/Documents/Math/research_website_catalogue_20261024/redirects/strict-gap-redirect-sol-20261115/verify_redirect.mjs --snapshot-dir APPLICATION_RAW_ABSOLUTE_PATH --plan
```

Save stdout as `PLAN.json` in that new application directory. It contains `create_tree_args`, `create_commit_args_after_tree_verified` and an explicitly gated `update_ref_args_AFTER_SEPARATE_ROOT_AUTHORIZATION_AND_READBACK`. The output placeholder for a future commit SHA is deliberately invalid; never send it. The code only reads files and emits JSON. It cannot apply, push, contact anyone, write files or call GitHub.

`PLAN_CAPTURED_PARENT.json` in this packet is a fully concrete example against the captured parent. A fresh parent with unrelated changes is acceptable only if a fresh plan is generated from that exact parent's four trees and the same guarded old HTML blob. Do not reuse the old `base_tree_sha` after a parent change.

## 4. Create ONE remote tree, then verify it before creating a commit

Only after root approval, invoke the connected tool with the generated structured object:

```javascript
await tools.mcp__codex_apps__github_create_tree(plan.create_tree_args);
```

Its exact arguments contain `repository_full_name: "AlecKriebel/Math"`, `base_tree_sha` equal to the actual parent root tree, and ONE tree element:

```javascript
{
  path: "docs/papers/strict-dirichlet-gap/index.html",
  mode: "100644",
  type: "blob",
  content: /* exact complete candidate string from generated plan */
}
```

Never omit the base tree, supply a deletion/null SHA, replace a directory, supply a second element or rebuild from a partial file list. Preserve the whole create-tree response. Its actual new root SHA must equal `plan.predicted_new_root_tree_SHA`.

Read back that created root and its `docs`, `papers` and article path trees with the same GET calls as above; save them in a fresh `post-tree/` directory using the four exact `tree-*.json` filenames. Verify both native hashes and all four predicted tree SHAs:

```sh
node /Users/alec/Documents/Math/research_website_catalogue_20261024/redirects/strict-gap-redirect-sol-20261115/verify_redirect.mjs --snapshot-dir APPLICATION_RAW_ABSOLUTE_PATH --post-snapshot-dir APPLICATION_POST_TREE_ABSOLUTE_PATH
```

Require PASS and `actual_post_tree_checked:true`. Every unchanged immediate entry has the same name, mode, type and object ID at all four levels. The predicted root therefore preserves every other remote root leaf, including root siblings, other papers, shared `docs/index.html`, all old PDF/ZIP/checksum/support assets and the source repository. A digest mismatch is an abort, not a reason to relax scope.

## 5. Create a direct-child commit and perform guarded main update

GET main again and require it still equals the captured parent. If it moved, do not update main; retain any dangling created tree and restart from a fresh parent only after examining the movement. No force or broad overwrite is permitted.

Create the commit from the generated structured args:

```javascript
await tools.mcp__codex_apps__github_create_commit(plan.create_commit_args_after_tree_verified);
```

The commit has exactly the captured current parent and no additional parents, and the verified predicted new root. Read the complete actual commit back through `/git/commits/<actual new commit SHA>`. Require its tree to equal the predicted root and its parents array to contain exactly that one current parent. Require a compare/readback to show precisely the specified modified HTML path and no other path. Stop on omitted/truncated or unexpected comparison data.

GET main again immediately before updating. Require unchanged parent, then invoke the documented guarded connected tool with these exact values:

```javascript
await tools.mcp__codex_apps__github_update_ref({
  repository_full_name: "AlecKriebel/Math",
  branch_name: "main",
  expected_sha: plan.parent_commit_SHA,
  force: false,
  sha: actualVerifiedDirectChildCommitSHA
});
```

The tool documents rejection of a mismatched expected SHA. Non-forced fast-forward and the direct-parent guard are both required. Do not replace this with an unguarded PATCH, force update, merge, local checkout, shared-index operation or broad push. On a rejected lease, inspect the new head and stop before any retry. Preserve the actual complete update response and final main readback. No release, tag or native inventory change accompanies this redirect.

## 6. Root's later delivery verification

After the actual Pages build succeeds, root must check the legacy URL's actual served body against the exact 838 candidate bytes and inspect browser arrival for the plain URL and `?utm_source=legacy#result`. This is an HTML/JavaScript Pages redirect, not an HTTP server 301. With JavaScript disabled, the no-script refresh and visible link use the clean destination. With JavaScript enabled, query and fragment are assigned exactly once, and the no-script refresh cannot compete.

Retain actual deployment/live/browser receipts in the new root application directory. Old PDF/ZIP/checksum/support URLs remain on GitHub Pages because their blobs are unchanged. No native source extraction, mathematical rerun, Sheet write, public-site/core edit, shared local Git mutation, external communication or release is needed. Root's verification and final adoption must precede any claim that this prepared redirect is applied or live.
