"""PROPOSED gated exact-kit uploader wrapper; no action on import."""
import json,sys
from lifecycle_common import production_entrypoint,run_zenodo
if __name__=='__main__':print(json.dumps(production_entrypoint(run_zenodo,sys.argv[1],sys.argv[2] if len(sys.argv)>2 else None)))
