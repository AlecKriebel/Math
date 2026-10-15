import json,sys
print(json.dumps({"executable":sys.executable,"version":sys.version,"version_info":list(sys.version_info)},indent=2))
