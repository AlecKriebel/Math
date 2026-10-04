#!/usr/bin/env python3
"""One-shot local custody seal. Final mode requires the parent's explicit approval."""
import argparse
import datetime as dt
import json
import pathlib
import stat
import sys
sys.dont_write_bytecode = True
from verify_review import CONTAINERS, identity, inventory, read, require, safe_name

def encode(value):
    return (json.dumps(value, indent=2) + '\n').encode()

def seal(root, diagnostic_fixture=False):
    root = root.resolve()
    require(not any((root / name).exists() for name in CONTAINERS), 'already sealed or partial seal')
    require(diagnostic_fixture or root == pathlib.Path(__file__).resolve().parent,
            'final seal limited to this own review namespace')
    plan = read(root / 'PUBLIC_PLAN.json')
    public_names = [safe_name(name) for name in plan['public_payload_paths']]
    require(len(public_names) == len(set(public_names)), 'duplicate public paths')
    all_names = inventory(root)
    require(set(public_names) <= all_names and not set(public_names) & CONTAINERS,
            'invalid public inventory')
    approval = None
    if not diagnostic_fixture:
        approval = read(root / 'ROOT_APPROVAL.json')
        require(approval['authorized_one_shot_closure'] is True, 'parent has not approved closure')
        for name, pin in approval['approved_artifact_bindings'].items():
            require(identity((root / safe_name(name)).read_bytes()) == pin, 'approved artifact changed: ' + name)
        pins = read(root / 'METADATA_REPAIR_CHECKS.json')['current_final_pins']
        for name, pin in pins.items():
            require(identity((root / 'current_submission_private/kit' / name).read_bytes()) == pin,
                    'submission changed: ' + name)
    else:
        pins = {}
    manifests = {}
    for name, paths in [('PUBLIC_MANIFEST.json', set(public_names)),
                        ('PRIVATE_MANIFEST.json', all_names - set(public_names))]:
        rows = []
        for rel in sorted(paths):
            path = root / rel
            rows.append({'path': rel, **identity(path.read_bytes()),
                         'mode': stat.S_IMODE(path.stat().st_mode)})
        manifests[name] = encode({'schema': 1, 'files': rows})
    closure = {'schema': 1, 'status': 'DIAGNOSTIC_FIXTURE' if diagnostic_fixture else 'CLOSED',
               'closed': not diagnostic_fixture, 'utc': dt.datetime.now(dt.timezone.utc).isoformat(),
               'manifest_bindings': {name: identity(data) for name, data in manifests.items()},
               'approval_binding': None if approval is None else identity((root / 'ROOT_APPROVAL.json').read_bytes()),
               'current_submission_pins': pins,
               'review_scope': 'Fresh source-first first-submission adversarial review; no claim of human peer review or universal novelty.',
               'post_seal_policy': 'No subsequent writes anywhere under this namespace. Read-only verification outputs must be captured externally.'}
    # No imports or process runs after inventory. Containers are the only new
    # files, and the closure is written last. Failure leaves an explicit partial
    # seal that cannot be silently overwritten by another invocation.
    for name, data in manifests.items():
        with (root / name).open('xb') as target:
            target.write(data)
    with (root / 'CLOSURE.json').open('xb') as target:
        target.write(encode(closure))
    print(json.dumps({'status': closure['status'], 'root': str(root),
                      'closure': identity((root / 'CLOSURE.json').read_bytes()),
                      'public_payloads': len(public_names),
                      'private_payloads': len(all_names - set(public_names))}, indent=2))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=pathlib.Path, default=pathlib.Path(__file__).resolve().parent)
    parser.add_argument('--diagnostic-fixture', action='store_true')
    args = parser.parse_args()
    seal(args.root, args.diagnostic_fixture)
