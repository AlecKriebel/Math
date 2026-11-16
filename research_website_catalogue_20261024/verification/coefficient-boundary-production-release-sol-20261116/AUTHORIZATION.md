# Separate future root authorizations

Source adoption is pending and null. No action authorization or runtime receipt exists in this design packet. The proposed adoption path in PLAN must not be interpreted as an existing authority. All modes reject this pending state before production preflight or mutation. The existing source FINAL and manifest pins identify the proposed frozen input without adopting it.

After actual source adoption is handed off and bound, complete current-code root and independent review precede first read-only execution. Default and `--verify-installed` then offer offline read-only preflight; the latter requires installed state. No helper mode was run during preparation. An old helper or obsolete preflight is not authority for this new baseline.

Future `INSTALL_AUTHORIZATION.json` and `GIT_AUTHORIZATION.json` must be distinct root-authored exact objects. Both bind:

- schema `fixed10-root-authorization-v1` and action `INSTALL_EXACT10_FILESYSTEM` or `PUBLISH_EXACT10_GIT`;
- current plan/helper hashes, actual adoption path/size/hash, the appropriate actual preflight fingerprint and exact sorted ten scope paths;
- concurrency `ROOT_SERIALIZED_NO_OTHER_W_WRITER` and `RETAIN_COMPLETED_OLD_LOCK_USE_NEW_ISOLATED_TRANSACTION_LOCKS`;
- deployment_authorized=false, Sheet_authorized=false, AA=null and follow_up=null;
- future timezone-qualified `expires_UTC`.

The installation object permits exactly those keys. The Git object also requires literal `author_name`, `author_email`, timezone-qualified `commit_date`, and an `installation_SUCCESS` path/size/hash pin. That receipt must belong to this effort's `transactions/<authorization-SHA>/SUCCESS.json`, report FILESYSTEM_INSTALL_VERIFIED_SNAPSHOT, exact682/107/108 and the current plan hash. It must be the completed new installation; the prior674receipt or any partial state does not qualify. Git uses an installed preflight fingerprint, distinct from the filesystem authorization's pre-install fingerprint.

Authorization SHA identifies each new transaction. Exclusive separate install/Git locks retain held inode and byte identity. Prior completed markers are authenticated and retained, never released or repurposed. Replay encounters the retained lock/transaction. Source adoption, authorizations and expiry never derive from an earlier successful run.

All ten buffers plus two backups must be durable before website writes. Effective routing config, singleton fetch/push URLs and absent origin.vcs are authorization-bound and rechecked immediately before each remote operation. After expensive scans and after routing, the current authorization/expiry fence runs again before the remote action. Routing output is hashed opaquely; credentials remain untouched. A parent mismatch or uncertain push stops and preserves state; there is no force push or automatic recovery mode.

The review gates implement this task's preparation boundary and add no human approval requirement to the user's routine research-publication authorization. Installation, scoped Git publication and deployment remain separate root actions; this packet creates none of their authorities.
