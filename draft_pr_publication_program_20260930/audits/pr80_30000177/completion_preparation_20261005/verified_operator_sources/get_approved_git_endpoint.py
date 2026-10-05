"""Return one validated credential-free endpoint; never disclose other config."""
import datetime, json, os, subprocess, sys
if sys.flags.optimize:
    raise RuntimeError('Optimization disables destination validation')
allowed = {b'https://github.com/AlecKriebel/Math.git',b'https://github.com/AlecKriebel/Math',
           b'git@github.com:AlecKriebel/Math.git',b'ssh://git@github.com/AlecKriebel/Math.git'}
configuration = subprocess.Popen(['git','--no-optional-locks','config','--name-only','--list'],
                                 cwd='/Users/alec/Documents/Math',stdout=subprocess.PIPE,stderr=subprocess.PIPE)
keys,configuration_error = configuration.communicate()
# Git can apply a second URL substitution when an explicit URL is passed to
# ls-remote or push. Rule names may themselves contain credentials, so neither
# keys nor values are retained or printed. Reject all such substitutions.
if configuration.returncode or any(key.lower().startswith(b'url.') and
                                    key.lower().endswith((b'.insteadof',b'.pushinsteadof'))
                                    for key in keys.splitlines()):
    raise RuntimeError('Git URL substitutions may change the approved endpoint; configuration withheld')
fetch = subprocess.Popen(['git','--no-optional-locks','remote','get-url','--all','origin'],
                         cwd='/Users/alec/Documents/Math',stdout=subprocess.PIPE,stderr=subprocess.PIPE)
fetch_out,fetch_error = fetch.communicate()
fetch_values = fetch_out.splitlines()
if fetch.returncode or len(fetch_values)!=1 or fetch_values[0] not in allowed:
    raise RuntimeError('Fetch endpoint is not the exact approved repository; configuration withheld')
process = subprocess.Popen(['git','--no-optional-locks','remote','get-url','--push','--all','origin'],
                           cwd='/Users/alec/Documents/Math',stdout=subprocess.PIPE,stderr=subprocess.PIPE)
out,err = process.communicate()
values = out.splitlines()
if process.returncode or len(values)!=1 or values[0] not in allowed:
    raise RuntimeError('Push endpoint is not the exact approved repository; configuration withheld')
print(json.dumps({'UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),
                  'actual_PID':os.getpid(),'configuration_child_PID':process.pid,
                  'configuration_child_exit_code':process.returncode,
                  'rewrite_configuration_child_PID':configuration.pid,
                  'URL_rewrite_rules_absent':True,
                  'fetch_endpoint':fetch_values[0].decode(),
                  'fetch_configuration_child_PID':fetch.pid,
                  'fetch_configuration_child_exit_code':fetch.returncode,
                  'endpoint':values[0].decode(),'credential_free_expected_repository':True}))
