#!/usr/bin/env python3
"""Reverse exactly the recorded unsealed source edits; execute no helper body."""
import hashlib
import json
from pathlib import Path
P=Path(__file__).resolve().parent
source=(P/'prepare_current_packet.py').read_bytes().decode()
reversals=[
('import math\n',''),
("\n\ndef utc(value):\n    require(type(value) is str and value,'Explicit ISO UTC clock required')\n    parsed=dt.datetime.fromisoformat(value[:-1]+'+00:00' if value.endswith('Z') else value)\n    require(parsed.tzinfo is not None and parsed.utcoffset()==dt.timedelta(0),'Aware UTC clock required')\n    return parsed\n",''),
("    def floating(value):\n        result=float(value);require(math.isfinite(result),'Nonfinite decoded JSON number')\n        return result\n    return json.loads(data,object_pairs_hook=pairs,parse_constant=constant,parse_float=floating)","    return json.loads(data,object_pairs_hook=pairs,parse_constant=constant)"),
('    values=set();directories=set()','    values=set()'),
("        else:\n            require(path.is_dir(),'Nonregular member')\n            directories.add(relative(path.relative_to(root).as_posix()))\n    expected={parent.as_posix() for value in values for parent in PurePosixPath(value).parents if parent.as_posix()!='.'}\n    require(directories==expected,'Extra empty directory rejected: '+str(sorted(directories-expected)))","        else:require(path.is_dir(),'Nonregular member')"),
("        if name in dependencies:\n            previous=dependencies[name]\n            require(all(equal(previous[key],row[key]) for key in ['path','bytes','sha256']),'Input changed during build')\n            roles=previous['role'] if type(previous['role']) is list else [previous['role']]\n            row['role']=sorted(set(roles+[role]))\n        dependencies[name]=row;return data","        require(name not in dependencies or equal(dependencies[name],row),'Input changed during build')\n        dependencies[name]=row;return data"),
('cwd=repo,stdin=subprocess.DEVNULL,capture_output=True','cwd=repo,capture_output=True'),
("    require(type(preparation) is dict and preparation['status']=='CLOSED_SOURCE_ONLY_CURRENT_PREPARATION','Closed SOURCE-ONLY preparation required')\n",''),
("    require(pins['status']=='SOURCE_ONLY_FIXED_INPUTS_FUTURE_ROOT_PREREQUISITES_PENDING' and pins['current_or_future_root_verdict_claimed'] is False,'No preparation verdict transfer')\n",''),
("        authored=validate_rows(info['members']);foreign_names=validate_rows(info['foreign_members'])\n        require(not authored.intersection(foreign_names) and len(authored)==info['first_party_count'] and len(foreign_names)==info['foreign_count'],'Disjoint individually bound family classes required')\n",''),
("foreign=row['path'] in foreign_names;raw=bind","foreign=row in info['foreign_members'];raw=bind"),
("            require(utc(run['started_utc'])<=utc(run['finished_utc']),'Ordered actual UTC clocks required')\n            require(type(run['argv']) is list and run['argv'] and all(type(x) is str and x for x in run['argv']) and type(run['cwd']) is str and run['cwd'],'Complete actual argv/cwd required')\n            streams=[run[channel] for channel in ['stdout','stderr']]\n            require(len(validate_rows(streams))==2,'Distinct fully retained actual channels required')\n            prefix=pins['root_support']['original' if obj is root else 'families']['directory']\n            for stream in streams:\n                retained=bind(prefix+'/'+stream['path'],'complete_actual_root_stream',stream['sha256'])\n                require(len(retained)==stream['bytes'],'Actual retained channel size differs')","            require(type(run['started_utc']) is str and run['started_utc'] and type(run['finished_utc']) is str and run['finished_utc'],'Actual clocks required')"),
("    require(current['reason'].strip().lower() not in {'yes','approved','pass','ok','root'},'Substantive fresh-input approval reason required')\n    require(utc(current['created_utc'])<=utc(now),'Fresh input UTC may not be future dated')\n",''),
("This argument does not close the expected exterior-length gap from the ordinary axioms. A full SIRSN supplies finite major-road intensity p(1); a weak SIRSN does not automatically do so.","The ordinary axioms do not close the expected exterior-length gap.")]
for before,after in reversals:
 assert source.count(before)==1,repr(before)
 source=source.replace(before,after,1)
data=source.encode();assert len(data)==35227,len(data)
target=P/'HISTORICAL_STOPPED_BUILDER_SOURCE.py';assert not target.exists()
with target.open('xb') as f:f.write(data)
receipt={'kind':'Deterministic reconstruction of the stopped unsealed builder by reversing only the recorded source edits',
 'path':target.name,'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest(),'reversal_count':len(reversals),
 'direct_pre_edit_hash_attestation':False,'expected_stopped_size_matched':True,'source_helpers_imported_or_executed':False,
 'historical_source_not_current_executable':True,'current_source_sha256':hashlib.sha256((P/'prepare_current_packet.py').read_bytes()).hexdigest()}
with (P/'HISTORICAL_STOPPED_SOURCE_RECONSTRUCTION.json').open('x') as f:json.dump(receipt,f,indent=2);f.write('\n')
print(json.dumps(receipt,indent=2))
