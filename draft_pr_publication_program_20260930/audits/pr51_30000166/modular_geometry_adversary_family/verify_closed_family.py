#!/usr/bin/env python3
"""Separate complete readonly readback; externally pinned manifest required."""
import argparse
import json
import family_custody as c

parser = argparse.ArgumentParser()
parser.add_argument('--manifest-sha256',required=True)
args = parser.parse_args()
print(json.dumps(c.verify(args.manifest_sha256),sort_keys=True,indent=2))
