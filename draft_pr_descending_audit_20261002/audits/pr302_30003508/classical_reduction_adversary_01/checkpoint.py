import datetime, pathlib, sys
root=pathlib.Path(__file__).resolve().parent
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
with (root/'RESEARCH_LOG.md').open('a') as out:
    out.write('\n## '+now+' — '+sys.argv[1]+'\n\n'+sys.argv[2]+'\n')
print(now,sys.argv[1])
