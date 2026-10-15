"""PROPOSED exact metadata request preparation; never sends a PR write."""
import json
from lifecycle_common import production_entrypoint,metadata_request
if __name__=='__main__':print(json.dumps(production_entrypoint(metadata_request)))
