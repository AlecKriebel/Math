"""PROPOSED exact metadata request preparation; never sends a PR write."""
import json
from lifecycle_common import metadata_request
if __name__=='__main__':print(json.dumps(metadata_request()))
