# Actual native-index observations and binding hold

This note records an observed transition requiring root reconciliation. It does not authorize index restoration, chmod, Git mutation, installation or a fresh baseline. No claim is made that root's earlier native index stayed unchanged. Root reported its prior direct authentication as prefix 0f58 / mode 0600. I did not personally observe that earlier state in this task.

My first index stat/hash in this task was W/.git/index: 9,049,366 bytes, mode 0644, SHA256 8db8d40ce28617085e5e3b7e61ba00bf2e68748a981b881e31d49d3edef21d6e. The one later printed W hash matched this value. Every Git invocation below explicitly used --no-optional-locks. No status/add/reset/clean/branch call, project helper, Git mutation, W write, restore or chmod was issued. There was no index hash before the first read-only diff calls, so causality or uninterrupted continuity from the earlier root state is not inferred.

Exact W Git chronology (all command blocks ran in /Users/alec/Desktop/alec-dev/aleckriebel.com using exec_command's default login shell; no per-command environment override was supplied):

1. Tool result dbffad, before the first index stat/hash:

   git --no-optional-locks rev-parse HEAD HEAD^{tree}
   git --no-optional-locks rev-parse --git-path index
   git --no-optional-locks diff --name-only -- public
   git --no-optional-locks diff --cached --name-only

   HEAD f632ad3949cecd62a92f711d5ba008cee92adb8c; tree 7d5180d490008693987c000a1592214a3282a5c2; index path .git/index; both diff-name outputs empty. Aggregate/CSS byte counts were also read.

2. Tool 433205, before the public snapshot block, authenticated Math HEAD/tree/index only (Math a4ce3c37dad209339e490d18dcced6c48cf912d2; tree 214df4f88d2e2d9dcf9546eaa6fcf342d669afbe; 25,854,746-byte mode-0644 Math index SHA256 91b10d938f7d737226662bbff3b07016dcc0e501376a045811ab4e930c6fbb11; 131,043 stage records). It did not bind W's earlier state.

3. Tool result 3db4b3: ordinary find/shasum/stat captured public file hashes/topology and copied only index.html/sitemap.xml into this owned audit folder. Then stat -f '%Sp %Lp %z %N' .git/index and shasum -a 256 .git/index produced the first actual index observation above. This was followed by:

   git --no-optional-locks ls-files --stage -z | tr '\000' '\n' | wc -l

   It printed 58,651. No raw native index backup was copied or altered.

4. Tool result d6343b: git --no-optional-locks ls-tree -r --name-only HEAD -- src package.json package-lock.json firebase.json .firebaserc .gitignore README.md. This only identified the four current root configuration/readme paths for opaque source guards. No status/diff/cached query in this block.

5. Tool result f82287: after ordinary read-only selected root-file hashes/stat and article-shell lines:

   git --no-optional-locks symbolic-ref -q HEAD
   git --no-optional-locks rev-parse HEAD HEAD^{tree}
   shasum -a 256 .git/index

   It printed refs/heads/master, the same f632ad39 / 7d5180d4 values, and the same full 8db8d40c index SHA. There was exactly ONE W ls-files count, in 3db4b3; the other count in 433205 was Math. My earlier parent status sentence suggesting a second W count was mistaken and explicitly corrected to root. No additional query was made to resolve this; the actual prior command history was sufficient.

Root then instructed: no restoration/chmod or further W Git status/diff/cached/ls-files queries, and hold final baseline binding pending its concrete reconciliation. I acknowledged and issued no further W command after that instruction. Source and requirements reading may continue. All currently captured W values remain observations, not a newly adopted install/publication lease.

Environment qualification: the explicit command-line flag is known. No index-affecting Git environment variable was authored by me; the inherited process environment during earlier blocks was not captured at that time. A later local shell environment observation is separately logged and cannot retroactively prove those earlier inherited values.

Later environment observation 6c8166 at 2026-11-16T20:03:28Z, from the owned audit directory, resolved git to /opt/homebrew/bin/git. printenv GIT_OPTIONAL_LOCKS GIT_INDEX_FILE GIT_WORK_TREE GIT_DIR printed no values and exited 1, so all four were absent in that later shell. No Git command or W operation ran in that observation. These later values are not a retrospective guarantee for the earlier blocks.

Root subsequently supplied the concrete transition disposition and fresh-baseline GO. I personally read the complete actual verification/website-index-transition-20261116/ROOT_DISPOSITION.json, 11,166 bytes, SHA256 3b9c97fbfbe71918b0456c91b4d971e67e43f5913c6763096389d512cd08de77. It reports identical path/OID/mode/flags/stage/padding semantics and extension bytes, 121 stat-cache-only changed records and 58,530 whole raw identical records between prior 0f58/0600 and current 8db8/0644. Cause remains unattributed. Root authenticated all 711 public files' byte/mode preservation and HEAD f632. I did not parse the two native index bodies myself or restore/chmod either. Root explicitly adopts actual 8db8/0644 as this fresh baseline; the old 0f58 state is historical. BASELINE_ADOPTION.json records this binding, including preservation of 58,649 current untargeted whole raw records and native mode 0644 in any separately authorized future 18-path transaction. No further W Git status/diff/cached/ls-files query was issued.
