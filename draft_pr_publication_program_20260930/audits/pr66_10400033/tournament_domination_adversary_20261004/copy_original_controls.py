import hashlib,json,pathlib
here=pathlib.Path(__file__).resolve().parent
original=here.parent/'original_source_authentication_20261004/original/unsolved_math_prioritization/attempts/10400033'
replay=here/'original_replay'
replay.mkdir(exist_ok=True)
manifest=[]
for name in ['verify_tournaments.py','verify_jones.py','verify.py','CANDIDATE.md']:
    b=(original/name).read_bytes()
    (replay/name).write_bytes(b)
    manifest.append({'name':name,'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest(),'source':str(original/name)})
(here/'ORIGINAL_REPLAY_MANIFEST.json').write_text(json.dumps(manifest,indent=2)+'\n')
print(json.dumps(manifest,indent=2))
