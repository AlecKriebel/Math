import hashlib, pathlib
base=pathlib.Path('/Users/alec/Documents/Math/draft_pr_publication_program_20260930/audits/pr66_10400033/original_source_authentication_20261004/original')
paths=['AGENTS.md','unsolved_math_prioritization/AGENTS.md']
paths += ['unsolved_math_prioritization/attempts/10400033/'+x for x in ['source_record.json','verify.py','verify_tournaments.py','verify_jones.py','SOURCES.md','README.md']]
for p in paths:
    data=(base/p).read_bytes()
    print('\nFILE '+p+' SHA256 '+hashlib.sha256(data).hexdigest()+'\n'+data.decode())
