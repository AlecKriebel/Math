# Read-only unpublished case-alias scope audit

2026-10-16: Started bounded audit of stable unpublished PRs 1033,1034,1037,1041,1047,1052,1064,1071,1085. All writer tests will use one disposable extraction at a time. No canonical edits, service calls, Git mutations, external communication, mathematical reclassification, or repair claims. Scope audit completion estimate: 5%.

2026-10-16T04:09:32.446827+00:00: Six actual fresh-uppercase archive reproductions confirmed P3 location-contract findings for PR1064, PR1071, PR1085 in normal and optimized Python. Six canonical-spelling rejection controls passed. PR1052 uppercase paths were rejected and its intended in-kit outputs succeeded in both modes. All generated ZIPs matched current canonical archives; all original extraction bytes and all 2244 canonical inventory records remained exact. No mathematical defect, prior-file overwrite or repair completion is asserted. Bounded scope audit estimate: 95%; final report/seal pending filesystem write capacity.

## Exact original command-receipt custody before inode reuse

BEGIN_COMMAND_RECEIPT_JSON
{
  "schema": "exact-original-command-receipt-custody-v1",
  "receipts": [
    {
      "original_file": "command_000.json",
      "bytes": 1594,
      "sha256": "a3fa40faa9505daafb913ff84cac790199a2a0bf45e786771552eee4bf0c4def",
      "exact_utf8_bytes": "{\n  \"argv\": [\n    \"/opt/homebrew/opt/python@3.14/bin/python3.14\",\n    \"-B\",\n    \"/Users/alec/Documents/Math/draft_pr_actual_claims_1000_1100_20261012/reviews/case_alias_scope_20261016/scratch/clean/build_support.py\",\n    \"--output\",\n    \"/Users/alec/Documents/Math/draft_pr_actual_claims_1000_1100_20261012/reviews/case_alias_scope_20261016/scratch/CLEAN/case_alias_0.zip\"\n  ],\n  \"cwd\": \"/Users/alec/Documents/Math/draft_pr_actual_claims_1000_1100_20261012/reviews/case_alias_scope_20261016/scratch/clean\",\n  \"label\": \"pr1052_normal_case_alias\",\n  \"returncode\": 1,\n  \"stderr\": \"Traceback (most recent call last):\\n  File \\\"/Users/alec/Documents/Math/draft_pr_actual_claims_1000_1100_20261012/reviews/case_alias_scope_20261016/scratch/clean/build_support.py\\\", line 36, in <module>\\n    main()\\n    ~~~~^^\\n  File \\\"/Users/alec/Documents/Math/draft_pr_actual_claims_1000_1100_20261012/reviews/case_alias_scope_20261016/scratch/clean/build_support.py\\\", line 21, in main\\n    out.resolve().relative_to(ROOT)\\n    ~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^\\n  File \\\"/opt/homebrew/Cellar/python@3.14/3.14.6/Frameworks/Python.framework/Versions/3.14/lib/python3.14/pathlib/__init__.py\\\", line 490, in relative_to\\n    raise ValueError(f\\\"{str(self)!r} is not in the subpath of {str(other)!r}\\\")\\nValueError: '/Users/alec/Documents/Math/draft_pr_actual_claims_1000_1100_20261012/reviews/case_alias_scope_20261016/scratch/CLEAN/case_alias_0.zip' is not in the subpath of '/Users/alec/Documents/Math/draft_pr_actual_claims_1000_1100_20261012/reviews/case_alias_scope_20261016/scratch/clean'\\n\",\n  \"stdout\": \"\"\n}\n",
      "parsed": {
        "argv": [
          "/opt/homebrew/opt/python@3.14/bin/python3.14",
          "-B",
          "/Users/alec/Documents/Math/draft_pr_actual_claims_1000_1100_20261012/reviews/case_alias_scope_20261016/scratch/clean/build_support.py",
          "--output",
          "/Users/alec/Documents/Math/draft_pr_actual_claims_1000_1100_20261012/reviews/case_alias_scope_20261016/scratch/CLEAN/case_alias_0.zip"
        ],
        "cwd": "/Users/alec/Documents/Math/draft_pr_actual_claims_1000_1100_20261012/reviews/case_alias_scope_20261016/scratch/clean",
        "label": "pr1052_normal_case_alias",
        "returncode": 1,
        "stderr": "Traceback (most recent call last):\n  File \"/Users/alec/Documents/Math/draft_pr_actual_claims_1000_1100_20261012/reviews/case_alias_scope_20261016/scratch/clean/build_support.py\", line 36, in <module>\n    main()\n    ~~~~^^\n  File \"/Users/alec/Documents/Math/draft_pr_actual_claims_1000_1100_20261012/reviews/case_alias_scope_20261016/scratch/clean/build_support.py\", line 21, in main\n    out.resolve().relative_to(ROOT)\n    ~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^\n  File \"/opt/homebrew/Cellar/python@3.14/3.14.6/Frameworks/Python.framework/Versions/3.14/lib/python3.14/pathlib/__init__.py\", line 490, in relative_to\n    raise ValueError(f\"{str(self)!r} is not in the subpath of {str(other)!r}\")\nValueError: '/Users/alec/Documents/Math/draft_pr_actual_claims_1000_1100_20261012/reviews/case_alias_scope_20261016/scratch/CLEAN/case_alias_0.zip' is not in the subpath of '/Users/alec/Documents/Math/draft_pr_actual_claims_1000_1100_20261012/reviews/case_alias_scope_20261016/scratch/clean'\n",
        "stdout": ""
      }
    },
    {
      "original_file": "command_001.json",
      "bytes": 678,
      "sha256": "961f49a77f55dddcac05f33bd87a877158fdb7047619f1c69ebbd3f9452746f3",
      "exact_utf8_bytes": "{\n  \"argv\": [\n    \"/opt/homebrew/opt/python@3.14/bin/python3.14\",\n    \"-B\",\n    \"/Users/alec/Documents/Math/draft_pr_actual_claims_1000_1100_20261012/reviews/case_alias_scope_20261016/scratch/clean/build_support.py\",\n    \"--output\",\n    \"/Users/alec/Documents/Math/draft_pr_actual_claims_1000_1100_20261012/reviews/case_alias_scope_20261016/scratch/clean/direct_0.zip\"\n  ],\n  \"cwd\": \"/Users/alec/Documents/Math/draft_pr_actual_claims_1000_1100_20261012/reviews/case_alias_scope_20261016/scratch/clean\",\n  \"label\": \"pr1052_normal_direct_control\",\n  \"returncode\": 0,\n  \"stderr\": \"\",\n  \"stdout\": \"0bb83d60cc0454870282dc251e1f459bced13165634933d0b5bf853b172b6a6d  direct_0.zip\\n\"\n}\n",
      "parsed": {
        "argv": [
          "/opt/homebrew/opt/python@3.14/bin/python3.14",
          "-B",
          "/Users/alec/Documents/Math/draft_pr_actual_claims_1000_1100_20261012/reviews/case_alias_scope_20261016/scratch/clean/build_support.py",
          "--output",
          "/Users/alec/Documents/Math/draft_pr_actual_claims_1000_1100_20261012/reviews/case_alias_scope_20261016/scratch/clean/direct_0.zip"
        ],
        "cwd": "/Users/alec/Documents/Math/draft_pr_actual_claims_1000_1100_20261012/reviews/case_alias_scope_20261016/scratch/clean",
        "label": "pr1052_normal_direct_control",
        "returncode": 0,
        "stderr": "",
        "stdout": "0bb83d60cc0454870282dc251e1f459bced13165634933d0b5bf853b172b6a6d  direct_0.zip\n"
      }
    },
    {
      "original_file": "command_002.json",
      "bytes": 1607,
      "sha256": "efb7160070fdcea5293174831c794979245d65b6e379e57cdabda94f6ae4f9a3",
      "exact_utf8_bytes": "{\n  \"argv\": [\n    \"/opt/homebrew/opt/python@3.14/bin/python3.14\",\n    \"-O\",\n    \"-B\",\n    \"/Users/alec/Documents/Math/draft_pr_actual_claims_1000_1100_20261012/reviews/case_alias_scope_20261016/scratch/clean/build_support.py\",\n    \"--output\",\n    \"/Users/alec/Documents/Math/draft_pr_actual_claims_1000_1100_20261012/reviews/case_alias_scope_20261016/scratch/CLEAN/case_alias_1.zip\"\n  ],\n  \"cwd\": \"/Users/alec/Documents/Math/draft_pr_actual_claims_1000_1100_20261012/reviews/case_alias_scope_20261016/scratch/clean\",\n  \"label\": \"pr1052_optimized_case_alias\",\n  \"returncode\": 1,\n  \"stderr\": \"Traceback (most recent call last):\\n  File \\\"/Users/alec/Documents/Math/draft_pr_actual_claims_1000_1100_20261012/reviews/case_alias_scope_20261016/scratch/clean/build_support.py\\\", line 36, in <module>\\n    main()\\n    ~~~~^^\\n  File \\\"/Users/alec/Documents/Math/draft_pr_actual_claims_1000_1100_20261012/reviews/case_alias_scope_20261016/scratch/clean/build_support.py\\\", line 21, in main\\n    out.resolve().relative_to(ROOT)\\n    ~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^\\n  File \\\"/opt/homebrew/Cellar/python@3.14/3.14.6/Frameworks/Python.framework/Versions/3.14/lib/python3.14/pathlib/__init__.py\\\", line 490, in relative_to\\n    raise ValueError(f\\\"{str(self)!r} is not in the subpath of {str(other)!r}\\\")\\nValueError: '/Users/alec/Documents/Math/draft_pr_actual_claims_1000_1100_20261012/reviews/case_alias_scope_20261016/scratch/CLEAN/case_alias_1.zip' is not in the subpath of '/Users/alec/Documents/Math/draft_pr_actual_claims_1000_1100_20261012/reviews/case_alias_scope_20261016/scratch/clean'\\n\",\n  \"stdout\": \"\"\n}\n",
      "parsed": {
        "argv": [
          "/opt/homebrew/opt/python@3.14/bin/python3.14",
          "-O",
          "-B",
          "/Users/alec/Documents/Math/draft_pr_actual_claims_1000_1100_20261012/reviews/case_alias_scope_20261016/scratch/clean/build_support.py",
          "--output",
          "/Users/alec/Documents/Math/draft_pr_actual_claims_1000_1100_20261012/reviews/case_alias_scope_20261016/scratch/CLEAN/case_alias_1.zip"
        ],
        "cwd": "/Users/alec/Documents/Math/draft_pr_actual_claims_1000_1100_20261012/reviews/case_alias_scope_20261016/scratch/clean",
        "label": "pr1052_optimized_case_alias",
        "returncode": 1,
        "stderr": "Traceback (most recent call last):\n  File \"/Users/alec/Documents/Math/draft_pr_actual_claims_1000_1100_20261012/reviews/case_alias_scope_20261016/scratch/clean/build_support.py\", line 36, in <module>\n    main()\n    ~~~~^^\n  File \"/Users/alec/Documents/Math/draft_pr_actual_claims_1000_1100_20261012/reviews/case_alias_scope_20261016/scratch/clean/build_support.py\", line 21, in main\n    out.resolve().relative_to(ROOT)\n    ~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^\n  File \"/opt/homebrew/Cellar/python@3.14/3.14.6/Frameworks/Python.framework/Versions/3.14/lib/python3.14/pathlib/__init__.py\", line 490, in relative_to\n    raise ValueError(f\"{str(self)!r} is not in the subpath of {str(other)!r}\")\nValueError: '/Users/alec/Documents/Math/draft_pr_actual_claims_1000_1100_20261012/reviews/case_alias_scope_20261016/scratch/CLEAN/case_alias_1.zip' is not in the subpath of '/Users/alec/Documents/Math/draft_pr_actual_claims_1000_1100_20261012/reviews/case_alias_scope_20261016/scratch/clean'\n",
        "stdout": ""
      }
    },
    {
      "original_file": "command_003.json",
      "bytes": 691,
      "sha256": "d96c9d0326879f3f6610186c8e2e3c887c3e54c68e1e2143cd8a310743e49d53",
      "exact_utf8_bytes": "{\n  \"argv\": [\n    \"/opt/homebrew/opt/python@3.14/bin/python3.14\",\n    \"-O\",\n    \"-B\",\n    \"/Users/alec/Documents/Math/draft_pr_actual_claims_1000_1100_20261012/reviews/case_alias_scope_20261016/scratch/clean/build_support.py\",\n    \"--output\",\n    \"/Users/alec/Documents/Math/draft_pr_actual_claims_1000_1100_20261012/reviews/case_alias_scope_20261016/scratch/clean/direct_1.zip\"\n  ],\n  \"cwd\": \"/Users/alec/Documents/Math/draft_pr_actual_claims_1000_1100_20261012/reviews/case_alias_scope_20261016/scratch/clean\",\n  \"label\": \"pr1052_optimized_direct_control\",\n  \"returncode\": 0,\n  \"stderr\": \"\",\n  \"stdout\": \"0bb83d60cc0454870282dc251e1f459bced13165634933d0b5bf853b172b6a6d  direct_1.zip\\n\"\n}\n",
      "parsed": {
        "argv": [
          "/opt/homebrew/opt/python@3.14/bin/python3.14",
          "-O",
          "-B",
          "/Users/alec/Documents/Math/draft_pr_actual_claims_1000_1100_20261012/reviews/case_alias_scope_20261016/scratch/clean/build_support.py",
          "--output",
          "/Users/alec/Documents/Math/draft_pr_actual_claims_1000_1100_20261012/reviews/case_alias_scope_20261016/scratch/clean/direct_1.zip"
        ],
        "cwd": "/Users/alec/Documents/Math/draft_pr_actual_claims_1000_1100_20261012/reviews/case_alias_scope_20261016/scratch/clean",
        "label": "pr1052_optimized_direct_control",
        "returncode": 0,
        "stderr": "",
        "stdout": "0bb83d60cc0454870282dc251e1f459bced13165634933d0b5bf853b172b6a6d  direct_1.zip\n"
      }
    },
    {
      "original_file": "command_004.json",
      "bytes": 805,
      "sha256": "103727ed9058028007489fa68b2feb75eb523f10d7976e63f039f8459cc31394",
      "exact_utf8_bytes": "{\n  \"argv\": [\n    \"/opt/homebrew/opt/python@3.14/bin/python3.14\",\n    \"-B\",\n    \"/Users/alec/Documents/Math/draft_pr_actual_claims_1000_1100_20261012/reviews/case_alias_scope_20261016/scratch/clean/build_archive.py\",\n    \"--output\",\n    \"/Users/alec/Documents/Math/draft_pr_actual_claims_1000_1100_20261012/reviews/case_alias_scope_20261016/scratch/CLEAN/case_alias_0.zip\"\n  ],\n  \"cwd\": \"/Users/alec/Documents/Math/draft_pr_actual_claims_1000_1100_20261012/reviews/case_alias_scope_20261016/scratch/clean\",\n  \"label\": \"pr1064_normal_case_alias\",\n  \"returncode\": 0,\n  \"stderr\": \"\",\n  \"stdout\": \"/Users/alec/Documents/Math/draft_pr_actual_claims_1000_1100_20261012/reviews/case_alias_scope_20261016/scratch/CLEAN/case_alias_0.zip SHA256 aeb9344ff84b46412d4532dc463cad4b151edba363172620978129c2964b2dbc\\n\"\n}\n",
      "parsed": {
        "argv": [
          "/opt/homebrew/opt/python@3.14/bin/python3.14",
          "-B",
          "/Users/alec/Documents/Math/draft_pr_actual_claims_1000_1100_20261012/reviews/case_alias_scope_20261016/scratch/clean/build_archive.py",
          "--output",
          "/Users/alec/Documents/Math/draft_pr_actual_claims_1000_1100_20261012/reviews/case_alias_scope_20261016/scratch/CLEAN/case_alias_0.zip"
        ],
        "cwd": "/Users/alec/Documents/Math/draft_pr_actual_claims_1000_1100_20261012/reviews/case_alias_scope_20261016/scratch/clean",
        "label": "pr1064_normal_case_alias",
        "returncode": 0,
        "stderr": "",
        "stdout": "/Users/alec/Documents/Math/draft_pr_actual_claims_1000_1100_20261012/reviews/case_alias_scope_20261016/scratch/CLEAN/case_alias_0.zip SHA256 aeb9344ff84b46412d4532dc463cad4b151edba363172620978129c2964b2dbc\n"
      }
    },
    {
      "original_file": "command_005.json",
      "bytes": 1426,
      "sha256": "88df9890483fe7ba6e2c46519d2ee9dc316f1475c2fad69a46e193d40a3d9df8",
      "exact_utf8_bytes": "{\n  \"argv\": [\n    \"/opt/homebrew/opt/python@3.14/bin/python3.14\",\n    \"-B\",\n    \"/Users/alec/Documents/Math/draft_pr_actual_claims_1000_1100_20261012/reviews/case_alias_scope_20261016/scratch/clean/build_archive.py\",\n    \"--output\",\n    \"/Users/alec/Documents/Math/draft_pr_actual_claims_1000_1100_20261012/reviews/case_alias_scope_20261016/scratch/clean/direct_0.zip\"\n  ],\n  \"cwd\": \"/Users/alec/Documents/Math/draft_pr_actual_claims_1000_1100_20261012/reviews/case_alias_scope_20261016/scratch/clean\",\n  \"label\": \"pr1064_normal_direct_control\",\n  \"returncode\": 1,\n  \"stderr\": \"Traceback (most recent call last):\\n  File \\\"/Users/alec/Documents/Math/draft_pr_actual_claims_1000_1100_20261012/reviews/case_alias_scope_20261016/scratch/clean/build_archive.py\\\", line 17, in <module>\\n    if out.is_relative_to(root):v.require(out==root/'support.zip' or out.is_relative_to(root/'tmp'),'inside package output must be support.zip or under tmp/')\\n                                ~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\\n  File \\\"/Users/alec/Documents/Math/draft_pr_actual_claims_1000_1100_20261012/reviews/case_alias_scope_20261016/scratch/clean/verify_package.py\\\", line 8, in require\\n    if not c:raise ValueError(m)\\n             ^^^^^^^^^^^^^^^^^^^\\nValueError: inside package output must be support.zip or under tmp/\\n\",\n  \"stdout\": \"\"\n}\n",
      "parsed": {
        "argv": [
          "/opt/homebrew/opt/python@3.14/bin/python3.14",
          "-B",
          "/Users/alec/Documents/Math/draft_pr_actual_claims_1000_1100_20261012/reviews/case_alias_scope_20261016/scratch/clean/build_archive.py",
          "--output",
          "/Users/alec/Documents/Math/draft_pr_actual_claims_1000_1100_20261012/reviews/case_alias_scope_20261016/scratch/clean/direct_0.zip"
        ],
        "cwd": "/Users/alec/Documents/Math/draft_pr_actual_claims_1000_1100_20261012/reviews/case_alias_scope_20261016/scratch/clean",
        "label": "pr1064_normal_direct_control",
        "returncode": 1,
        "stderr": "Traceback (most recent call last):\n  File \"/Users/alec/Documents/Math/draft_pr_actual_claims_1000_1100_20261012/reviews/case_alias_scope_20261016/scratch/clean/build_archive.py\", line 17, in <module>\n    if out.is_relative_to(root):v.require(out==root/'support.zip' or out.is_relative_to(root/'tmp'),'inside package output must be support.zip or under tmp/')\n                                ~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/Users/alec/Documents/Math/draft_pr_actual_claims_1000_1100_20261012/reviews/case_alias_scope_20261016/scratch/clean/verify_package.py\", line 8, in require\n    if not c:raise ValueError(m)\n             ^^^^^^^^^^^^^^^^^^^\nValueError: inside package output must be support.zip or under tmp/\n",
        "stdout": ""
      }
    },
    {
      "original_file": "command_006.json",
      "bytes": 818,
      "sha256": "af7386b14adab6a2bb2e8b190bd3de83fd56fafd939edc8132253006678099fb",
      "exact_utf8_bytes": "{\n  \"argv\": [\n    \"/opt/homebrew/opt/python@3.14/bin/python3.14\",\n    \"-O\",\n    \"-B\",\n    \"/Users/alec/Documents/Math/draft_pr_actual_claims_1000_1100_20261012/reviews/case_alias_scope_20261016/scratch/clean/build_archive.py\",\n    \"--output\",\n    \"/Users/alec/Documents/Math/draft_pr_actual_claims_1000_1100_20261012/reviews/case_alias_scope_20261016/scratch/CLEAN/case_alias_1.zip\"\n  ],\n  \"cwd\": \"/Users/alec/Documents/Math/draft_pr_actual_claims_1000_1100_20261012/reviews/case_alias_scope_20261016/scratch/clean\",\n  \"label\": \"pr1064_optimized_case_alias\",\n  \"returncode\": 0,\n  \"stderr\": \"\",\n  \"stdout\": \"/Users/alec/Documents/Math/draft_pr_actual_claims_1000_1100_20261012/reviews/case_alias_scope_20261016/scratch/CLEAN/case_alias_1.zip SHA256 aeb9344ff84b46412d4532dc463cad4b151edba363172620978129c2964b2dbc\\n\"\n}\n",
      "parsed": {
        "argv": [
          "/opt/homebrew/opt/python@3.14/bin/python3.14",
          "-O",
          "-B",
          "/Users/alec/Documents/Math/draft_pr_actual_claims_1000_1100_20261012/reviews/case_alias_scope_20261016/scratch/clean/build_archive.py",
          "--output",
          "/Users/alec/Documents/Math/draft_pr_actual_claims_1000_1100_20261012/reviews/case_alias_scope_20261016/scratch/CLEAN/case_alias_1.zip"
        ],
        "cwd": "/Users/alec/Documents/Math/draft_pr_actual_claims_1000_1100_20261012/reviews/case_alias_scope_20261016/scratch/clean",
        "label": "pr1064_optimized_case_alias",
        "returncode": 0,
        "stderr": "",
        "stdout": "/Users/alec/Documents/Math/draft_pr_actual_claims_1000_1100_20261012/reviews/case_alias_scope_20261016/scratch/CLEAN/case_alias_1.zip SHA256 aeb9344ff84b46412d4532dc463cad4b151edba363172620978129c2964b2dbc\n"
      }
    },
    {
      "original_file": "command_007.json",
      "bytes": 1439,
      "sha256": "2062f751728944df094f044d6fa646aa963b58bfca98fb0a4e6d2244a39c3581",
      "exact_utf8_bytes": "{\n  \"argv\": [\n    \"/opt/homebrew/opt/python@3.14/bin/python3.14\",\n    \"-O\",\n    \"-B\",\n    \"/Users/alec/Documents/Math/draft_pr_actual_claims_1000_1100_20261012/reviews/case_alias_scope_20261016/scratch/clean/build_archive.py\",\n    \"--output\",\n    \"/Users/alec/Documents/Math/draft_pr_actual_claims_1000_1100_20261012/reviews/case_alias_scope_20261016/scratch/clean/direct_1.zip\"\n  ],\n  \"cwd\": \"/Users/alec/Documents/Math/draft_pr_actual_claims_1000_1100_20261012/reviews/case_alias_scope_20261016/scratch/clean\",\n  \"label\": \"pr1064_optimized_direct_control\",\n  \"returncode\": 1,\n  \"stderr\": \"Traceback (most recent call last):\\n  File \\\"/Users/alec/Documents/Math/draft_pr_actual_claims_1000_1100_20261012/reviews/case_alias_scope_20261016/scratch/clean/build_archive.py\\\", line 17, in <module>\\n    if out.is_relative_to(root):v.require(out==root/'support.zip' or out.is_relative_to(root/'tmp'),'inside package output must be support.zip or under tmp/')\\n                                ~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\\n  File \\\"/Users/alec/Documents/Math/draft_pr_actual_claims_1000_1100_20261012/reviews/case_alias_scope_20261016/scratch/clean/verify_package.py\\\", line 8, in require\\n    if not c:raise ValueError(m)\\n             ^^^^^^^^^^^^^^^^^^^\\nValueError: inside package output must be support.zip or under tmp/\\n\",\n  \"stdout\": \"\"\n}\n",
      "parsed": {
        "argv": [
          "/opt/homebrew/opt/python@3.14/bin/python3.14",
          "-O",
          "-B",
          "/Users/alec/Documents/Math/draft_pr_actual_claims_1000_1100_20261012/reviews/case_alias_scope_20261016/scratch/clean/build_archive.py",
          "--output",
          "/Users/alec/Documents/Math/draft_pr_actual_claims_1000_1100_20261012/reviews/case_alias_scope_20261016/scratch/clean/direct_1.zip"
        ],
        "cwd": "/Users/alec/Documents/Math/draft_pr_actual_claims_1000_1100_20261012/reviews/case_alias_scope_20261016/scratch/clean",
        "label": "pr1064_optimized_direct_control",
        "returncode": 1,
        "stderr": "Traceback (most recent call last):\n  File \"/Users/alec/Documents/Math/draft_pr_actual_claims_1000_1100_20261012/reviews/case_alias_scope_20261016/scratch/clean/build_archive.py\", line 17, in <module>\n    if out.is_relative_to(root):v.require(out==root/'support.zip' or out.is_relative_to(root/'tmp'),'inside package output must be support.zip or under tmp/')\n                                ~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/Users/alec/Documents/Math/draft_pr_actual_claims_1000_1100_20261012/reviews/case_alias_scope_20261016/scratch/clean/verify_package.py\", line 8, in require\n    if not c:raise ValueError(m)\n             ^^^^^^^^^^^^^^^^^^^\nValueError: inside package output must be support.zip or under tmp/\n",
        "stdout": ""
      }
    },
    {
      "original_file": "command_008.json",
      "bytes": 968,
      "sha256": "1d5f941f244c7e5a591e1040a760841d14bda6d65317bb489a2746cf254ee413",
      "exact_utf8_bytes": "{\n  \"argv\": [\n    \"/opt/homebrew/opt/python@3.14/bin/python3.14\",\n    \"-B\",\n    \"/Users/alec/Documents/Math/draft_pr_actual_claims_1000_1100_20261012/reviews/case_alias_scope_20261016/scratch/clean/scripts/build_archive.py\",\n    \"--out\",\n    \"/Users/alec/Documents/Math/draft_pr_actual_claims_1000_1100_20261012/reviews/case_alias_scope_20261016/scratch/CLEAN/case_alias_0.zip\"\n  ],\n  \"cwd\": \"/Users/alec/Documents/Math/draft_pr_actual_claims_1000_1100_20261012/reviews/case_alias_scope_20261016/scratch/clean\",\n  \"label\": \"pr1071_normal_case_alias\",\n  \"returncode\": 0,\n  \"stderr\": \"\",\n  \"stdout\": \"{\\n  \\\"archive\\\": \\\"/Users/alec/Documents/Math/draft_pr_actual_claims_1000_1100_20261012/reviews/case_alias_scope_20261016/scratch/CLEAN/case_alias_0.zip\\\",\\n  \\\"members\\\": 150,\\n  \\\"compression\\\": \\\"ZIP_STORED\\\",\\n  \\\"fixed_time\\\": \\\"2026-10-14T00:00:00\\\",\\n  \\\"permissions\\\": \\\"regular-file 0644\\\",\\n  \\\"order\\\": \\\"lexicographic explicit manifest allowlist\\\"\\n}\\n\"\n}\n",
      "parsed": {
        "argv": [
          "/opt/homebrew/opt/python@3.14/bin/python3.14",
          "-B",
          "/Users/alec/Documents/Math/draft_pr_actual_claims_1000_1100_20261012/reviews/case_alias_scope_20261016/scratch/clean/scripts/build_archive.py",
          "--out",
          "/Users/alec/Documents/Math/draft_pr_actual_claims_1000_1100_20261012/reviews/case_alias_scope_20261016/scratch/CLEAN/case_alias_0.zip"
        ],
        "cwd": "/Users/alec/Documents/Math/draft_pr_actual_claims_1000_1100_20261012/reviews/case_alias_scope_20261016/scratch/clean",
        "label": "pr1071_normal_case_alias",
        "returncode": 0,
        "stderr": "",
        "stdout": "{\n  \"archive\": \"/Users/alec/Documents/Math/draft_pr_actual_claims_1000_1100_20261012/reviews/case_alias_scope_20261016/scratch/CLEAN/case_alias_0.zip\",\n  \"members\": 150,\n  \"compression\": \"ZIP_STORED\",\n  \"fixed_time\": \"2026-10-14T00:00:00\",\n  \"permissions\": \"regular-file 0644\",\n  \"order\": \"lexicographic explicit manifest allowlist\"\n}\n"
      }
    },
    {
      "original_file": "command_009.json",
      "bytes": 1668,
      "sha256": "b7e68ee017fe4b4778d6dba90b06e4e048b192e9e0fb376ae9543917bc5f6ac8",
      "exact_utf8_bytes": "{\n  \"argv\": [\n    \"/opt/homebrew/opt/python@3.14/bin/python3.14\",\n    \"-B\",\n    \"/Users/alec/Documents/Math/draft_pr_actual_claims_1000_1100_20261012/reviews/case_alias_scope_20261016/scratch/clean/scripts/build_archive.py\",\n    \"--out\",\n    \"/Users/alec/Documents/Math/draft_pr_actual_claims_1000_1100_20261012/reviews/case_alias_scope_20261016/scratch/clean/direct_0.zip\"\n  ],\n  \"cwd\": \"/Users/alec/Documents/Math/draft_pr_actual_claims_1000_1100_20261012/reviews/case_alias_scope_20261016/scratch/clean\",\n  \"label\": \"pr1071_normal_direct_control\",\n  \"returncode\": 1,\n  \"stderr\": \"Traceback (most recent call last):\\n  File \\\"/Users/alec/Documents/Math/draft_pr_actual_claims_1000_1100_20261012/reviews/case_alias_scope_20261016/scratch/clean/scripts/build_archive.py\\\", line 9, in <module>\\n    output=fresh_output(a.out)\\n  File \\\"/Users/alec/Documents/Math/draft_pr_actual_claims_1000_1100_20261012/reviews/case_alias_scope_20261016/scratch/clean/scripts/package_paths.py\\\", line 38, in fresh_output\\n    require(not target.is_relative_to(Path(root).resolve()) and not target.resolve().is_relative_to(Path(root).resolve()), 'Output must be outside all frozen package descendants.')\\n    ~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\\n  File \\\"/Users/alec/Documents/Math/draft_pr_actual_claims_1000_1100_20261012/reviews/case_alias_scope_20261016/scratch/clean/scripts/package_paths.py\\\", line 13, in require\\n    raise RuntimeError(message)\\nRuntimeError: Output must be outside all frozen package descendants.\\n\",\n  \"stdout\": \"\"\n}\n",
      "parsed": {
        "argv": [
          "/opt/homebrew/opt/python@3.14/bin/python3.14",
          "-B",
          "/Users/alec/Documents/Math/draft_pr_actual_claims_1000_1100_20261012/reviews/case_alias_scope_20261016/scratch/clean/scripts/build_archive.py",
          "--out",
          "/Users/alec/Documents/Math/draft_pr_actual_claims_1000_1100_20261012/reviews/case_alias_scope_20261016/scratch/clean/direct_0.zip"
        ],
        "cwd": "/Users/alec/Documents/Math/draft_pr_actual_claims_1000_1100_20261012/reviews/case_alias_scope_20261016/scratch/clean",
        "label": "pr1071_normal_direct_control",
        "returncode": 1,
        "stderr": "Traceback (most recent call last):\n  File \"/Users/alec/Documents/Math/draft_pr_actual_claims_1000_1100_20261012/reviews/case_alias_scope_20261016/scratch/clean/scripts/build_archive.py\", line 9, in <module>\n    output=fresh_output(a.out)\n  File \"/Users/alec/Documents/Math/draft_pr_actual_claims_1000_1100_20261012/reviews/case_alias_scope_20261016/scratch/clean/scripts/package_paths.py\", line 38, in fresh_output\n    require(not target.is_relative_to(Path(root).resolve()) and not target.resolve().is_relative_to(Path(root).resolve()), 'Output must be outside all frozen package descendants.')\n    ~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/Users/alec/Documents/Math/draft_pr_actual_claims_1000_1100_20261012/reviews/case_alias_scope_20261016/scratch/clean/scripts/package_paths.py\", line 13, in require\n    raise RuntimeError(message)\nRuntimeError: Output must be outside all frozen package descendants.\n",
        "stdout": ""
      }
    },
    {
      "original_file": "command_010.json",
      "bytes": 981,
      "sha256": "108a6109a5590d6ad01c5c6ca0ae60de43d28a7222a2fc9f4a9639c2f59b2727",
      "exact_utf8_bytes": "{\n  \"argv\": [\n    \"/opt/homebrew/opt/python@3.14/bin/python3.14\",\n    \"-O\",\n    \"-B\",\n    \"/Users/alec/Documents/Math/draft_pr_actual_claims_1000_1100_20261012/reviews/case_alias_scope_20261016/scratch/clean/scripts/build_archive.py\",\n    \"--out\",\n    \"/Users/alec/Documents/Math/draft_pr_actual_claims_1000_1100_20261012/reviews/case_alias_scope_20261016/scratch/CLEAN/case_alias_1.zip\"\n  ],\n  \"cwd\": \"/Users/alec/Documents/Math/draft_pr_actual_claims_1000_1100_20261012/reviews/case_alias_scope_20261016/scratch/clean\",\n  \"label\": \"pr1071_optimized_case_alias\",\n  \"returncode\": 0,\n  \"stderr\": \"\",\n  \"stdout\": \"{\\n  \\\"archive\\\": \\\"/Users/alec/Documents/Math/draft_pr_actual_claims_1000_1100_20261012/reviews/case_alias_scope_20261016/scratch/CLEAN/case_alias_1.zip\\\",\\n  \\\"members\\\": 150,\\n  \\\"compression\\\": \\\"ZIP_STORED\\\",\\n  \\\"fixed_time\\\": \\\"2026-10-14T00:00:00\\\",\\n  \\\"permissions\\\": \\\"regular-file 0644\\\",\\n  \\\"order\\\": \\\"lexicographic explicit manifest allowlist\\\"\\n}\\n\"\n}\n",
      "parsed": {
        "argv": [
          "/opt/homebrew/opt/python@3.14/bin/python3.14",
          "-O",
          "-B",
          "/Users/alec/Documents/Math/draft_pr_actual_claims_1000_1100_20261012/reviews/case_alias_scope_20261016/scratch/clean/scripts/build_archive.py",
          "--out",
          "/Users/alec/Documents/Math/draft_pr_actual_claims_1000_1100_20261012/reviews/case_alias_scope_20261016/scratch/CLEAN/case_alias_1.zip"
        ],
        "cwd": "/Users/alec/Documents/Math/draft_pr_actual_claims_1000_1100_20261012/reviews/case_alias_scope_20261016/scratch/clean",
        "label": "pr1071_optimized_case_alias",
        "returncode": 0,
        "stderr": "",
        "stdout": "{\n  \"archive\": \"/Users/alec/Documents/Math/draft_pr_actual_claims_1000_1100_20261012/reviews/case_alias_scope_20261016/scratch/CLEAN/case_alias_1.zip\",\n  \"members\": 150,\n  \"compression\": \"ZIP_STORED\",\n  \"fixed_time\": \"2026-10-14T00:00:00\",\n  \"permissions\": \"regular-file 0644\",\n  \"order\": \"lexicographic explicit manifest allowlist\"\n}\n"
      }
    },
    {
      "original_file": "command_011.json",
      "bytes": 1681,
      "sha256": "59056cf21fc321ef0c470af85866cb5d2db75978f9d2b4fbdcb2c97571a28fcb",
      "exact_utf8_bytes": "{\n  \"argv\": [\n    \"/opt/homebrew/opt/python@3.14/bin/python3.14\",\n    \"-O\",\n    \"-B\",\n    \"/Users/alec/Documents/Math/draft_pr_actual_claims_1000_1100_20261012/reviews/case_alias_scope_20261016/scratch/clean/scripts/build_archive.py\",\n    \"--out\",\n    \"/Users/alec/Documents/Math/draft_pr_actual_claims_1000_1100_20261012/reviews/case_alias_scope_20261016/scratch/clean/direct_1.zip\"\n  ],\n  \"cwd\": \"/Users/alec/Documents/Math/draft_pr_actual_claims_1000_1100_20261012/reviews/case_alias_scope_20261016/scratch/clean\",\n  \"label\": \"pr1071_optimized_direct_control\",\n  \"returncode\": 1,\n  \"stderr\": \"Traceback (most recent call last):\\n  File \\\"/Users/alec/Documents/Math/draft_pr_actual_claims_1000_1100_20261012/reviews/case_alias_scope_20261016/scratch/clean/scripts/build_archive.py\\\", line 9, in <module>\\n    output=fresh_output(a.out)\\n  File \\\"/Users/alec/Documents/Math/draft_pr_actual_claims_1000_1100_20261012/reviews/case_alias_scope_20261016/scratch/clean/scripts/package_paths.py\\\", line 38, in fresh_output\\n    require(not target.is_relative_to(Path(root).resolve()) and not target.resolve().is_relative_to(Path(root).resolve()), 'Output must be outside all frozen package descendants.')\\n    ~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\\n  File \\\"/Users/alec/Documents/Math/draft_pr_actual_claims_1000_1100_20261012/reviews/case_alias_scope_20261016/scratch/clean/scripts/package_paths.py\\\", line 13, in require\\n    raise RuntimeError(message)\\nRuntimeError: Output must be outside all frozen package descendants.\\n\",\n  \"stdout\": \"\"\n}\n",
      "parsed": {
        "argv": [
          "/opt/homebrew/opt/python@3.14/bin/python3.14",
          "-O",
          "-B",
          "/Users/alec/Documents/Math/draft_pr_actual_claims_1000_1100_20261012/reviews/case_alias_scope_20261016/scratch/clean/scripts/build_archive.py",
          "--out",
          "/Users/alec/Documents/Math/draft_pr_actual_claims_1000_1100_20261012/reviews/case_alias_scope_20261016/scratch/clean/direct_1.zip"
        ],
        "cwd": "/Users/alec/Documents/Math/draft_pr_actual_claims_1000_1100_20261012/reviews/case_alias_scope_20261016/scratch/clean",
        "label": "pr1071_optimized_direct_control",
        "returncode": 1,
        "stderr": "Traceback (most recent call last):\n  File \"/Users/alec/Documents/Math/draft_pr_actual_claims_1000_1100_20261012/reviews/case_alias_scope_20261016/scratch/clean/scripts/build_archive.py\", line 9, in <module>\n    output=fresh_output(a.out)\n  File \"/Users/alec/Documents/Math/draft_pr_actual_claims_1000_1100_20261012/reviews/case_alias_scope_20261016/scratch/clean/scripts/package_paths.py\", line 38, in fresh_output\n    require(not target.is_relative_to(Path(root).resolve()) and not target.resolve().is_relative_to(Path(root).resolve()), 'Output must be outside all frozen package descendants.')\n    ~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/Users/alec/Documents/Math/draft_pr_actual_claims_1000_1100_20261012/reviews/case_alias_scope_20261016/scratch/clean/scripts/package_paths.py\", line 13, in require\n    raise RuntimeError(message)\nRuntimeError: Output must be outside all frozen package descendants.\n",
        "stdout": ""
      }
    },
    {
      "original_file": "command_012.json",
      "bytes": 747,
      "sha256": "517cc4e7759cb91a4a02d9d17c4b82923cae08bc23666f889c77262b23dd0168",
      "exact_utf8_bytes": "{\n  \"argv\": [\n    \"/opt/homebrew/opt/python@3.14/bin/python3.14\",\n    \"-B\",\n    \"/Users/alec/Documents/Math/draft_pr_actual_claims_1000_1100_20261012/reviews/case_alias_scope_20261016/scratch/clean/build_archive.py\",\n    \"--output\",\n    \"/Users/alec/Documents/Math/draft_pr_actual_claims_1000_1100_20261012/reviews/case_alias_scope_20261016/scratch/CLEAN/case_alias_0.zip\"\n  ],\n  \"cwd\": \"/Users/alec/Documents/Math/draft_pr_actual_claims_1000_1100_20261012/reviews/case_alias_scope_20261016/scratch/clean\",\n  \"label\": \"pr1085_normal_case_alias\",\n  \"returncode\": 0,\n  \"stderr\": \"\",\n  \"stdout\": \"{\\n  \\\"archive_bytes\\\": 495659,\\n  \\\"archive_sha256\\\": \\\"77a2b789e16c868e8c73b6c55a726957d63ab9f50441c9b4e20828ddabbe5533\\\",\\n  \\\"passed\\\": true\\n}\\n\"\n}\n",
      "parsed": {
        "argv": [
          "/opt/homebrew/opt/python@3.14/bin/python3.14",
          "-B",
          "/Users/alec/Documents/Math/draft_pr_actual_claims_1000_1100_20261012/reviews/case_alias_scope_20261016/scratch/clean/build_archive.py",
          "--output",
          "/Users/alec/Documents/Math/draft_pr_actual_claims_1000_1100_20261012/reviews/case_alias_scope_20261016/scratch/CLEAN/case_alias_0.zip"
        ],
        "cwd": "/Users/alec/Documents/Math/draft_pr_actual_claims_1000_1100_20261012/reviews/case_alias_scope_20261016/scratch/clean",
        "label": "pr1085_normal_case_alias",
        "returncode": 0,
        "stderr": "",
        "stdout": "{\n  \"archive_bytes\": 495659,\n  \"archive_sha256\": \"77a2b789e16c868e8c73b6c55a726957d63ab9f50441c9b4e20828ddabbe5533\",\n  \"passed\": true\n}\n"
      }
    },
    {
      "original_file": "command_013.json",
      "bytes": 1697,
      "sha256": "cc64632b94557181f13dbda9002f906541a8e33f36582fc8f6db180f70bcd5ec",
      "exact_utf8_bytes": "{\n  \"argv\": [\n    \"/opt/homebrew/opt/python@3.14/bin/python3.14\",\n    \"-B\",\n    \"/Users/alec/Documents/Math/draft_pr_actual_claims_1000_1100_20261012/reviews/case_alias_scope_20261016/scratch/clean/build_archive.py\",\n    \"--output\",\n    \"/Users/alec/Documents/Math/draft_pr_actual_claims_1000_1100_20261012/reviews/case_alias_scope_20261016/scratch/clean/direct_0.zip\"\n  ],\n  \"cwd\": \"/Users/alec/Documents/Math/draft_pr_actual_claims_1000_1100_20261012/reviews/case_alias_scope_20261016/scratch/clean\",\n  \"label\": \"pr1085_normal_direct_control\",\n  \"returncode\": 1,\n  \"stderr\": \"Traceback (most recent call last):\\n  File \\\"/Users/alec/Documents/Math/draft_pr_actual_claims_1000_1100_20261012/reviews/case_alias_scope_20261016/scratch/clean/build_archive.py\\\", line 32, in <module>\\n    main()\\n    ~~~~^^\\n  File \\\"/Users/alec/Documents/Math/draft_pr_actual_claims_1000_1100_20261012/reviews/case_alias_scope_20261016/scratch/clean/build_archive.py\\\", line 26, in main\\n    out = safe_output(args.output)\\n  File \\\"/Users/alec/Documents/Math/draft_pr_actual_claims_1000_1100_20261012/reviews/case_alias_scope_20261016/scratch/clean/kit_common.py\\\", line 72, in safe_output\\n    require(target != ROOT and ROOT not in target.parents,\\n    ~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\\n            \\\"output must be outside canonical kit directory\\\")\\n            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\\n  File \\\"/Users/alec/Documents/Math/draft_pr_actual_claims_1000_1100_20261012/reviews/case_alias_scope_20261016/scratch/clean/kit_common.py\\\", line 11, in require\\n    raise ValueError(message)\\nValueError: output must be outside canonical kit directory\\n\",\n  \"stdout\": \"\"\n}\n",
      "parsed": {
        "argv": [
          "/opt/homebrew/opt/python@3.14/bin/python3.14",
          "-B",
          "/Users/alec/Documents/Math/draft_pr_actual_claims_1000_1100_20261012/reviews/case_alias_scope_20261016/scratch/clean/build_archive.py",
          "--output",
          "/Users/alec/Documents/Math/draft_pr_actual_claims_1000_1100_20261012/reviews/case_alias_scope_20261016/scratch/clean/direct_0.zip"
        ],
        "cwd": "/Users/alec/Documents/Math/draft_pr_actual_claims_1000_1100_20261012/reviews/case_alias_scope_20261016/scratch/clean",
        "label": "pr1085_normal_direct_control",
        "returncode": 1,
        "stderr": "Traceback (most recent call last):\n  File \"/Users/alec/Documents/Math/draft_pr_actual_claims_1000_1100_20261012/reviews/case_alias_scope_20261016/scratch/clean/build_archive.py\", line 32, in <module>\n    main()\n    ~~~~^^\n  File \"/Users/alec/Documents/Math/draft_pr_actual_claims_1000_1100_20261012/reviews/case_alias_scope_20261016/scratch/clean/build_archive.py\", line 26, in main\n    out = safe_output(args.output)\n  File \"/Users/alec/Documents/Math/draft_pr_actual_claims_1000_1100_20261012/reviews/case_alias_scope_20261016/scratch/clean/kit_common.py\", line 72, in safe_output\n    require(target != ROOT and ROOT not in target.parents,\n    ~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n            \"output must be outside canonical kit directory\")\n            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/Users/alec/Documents/Math/draft_pr_actual_claims_1000_1100_20261012/reviews/case_alias_scope_20261016/scratch/clean/kit_common.py\", line 11, in require\n    raise ValueError(message)\nValueError: output must be outside canonical kit directory\n",
        "stdout": ""
      }
    },
    {
      "original_file": "command_014.json",
      "bytes": 760,
      "sha256": "0c27d7b733b00cdbe23d1360ead67e1a149f2c18ffdef7998d70fa1ec8b35fda",
      "exact_utf8_bytes": "{\n  \"argv\": [\n    \"/opt/homebrew/opt/python@3.14/bin/python3.14\",\n    \"-O\",\n    \"-B\",\n    \"/Users/alec/Documents/Math/draft_pr_actual_claims_1000_1100_20261012/reviews/case_alias_scope_20261016/scratch/clean/build_archive.py\",\n    \"--output\",\n    \"/Users/alec/Documents/Math/draft_pr_actual_claims_1000_1100_20261012/reviews/case_alias_scope_20261016/scratch/CLEAN/case_alias_1.zip\"\n  ],\n  \"cwd\": \"/Users/alec/Documents/Math/draft_pr_actual_claims_1000_1100_20261012/reviews/case_alias_scope_20261016/scratch/clean\",\n  \"label\": \"pr1085_optimized_case_alias\",\n  \"returncode\": 0,\n  \"stderr\": \"\",\n  \"stdout\": \"{\\n  \\\"archive_bytes\\\": 495659,\\n  \\\"archive_sha256\\\": \\\"77a2b789e16c868e8c73b6c55a726957d63ab9f50441c9b4e20828ddabbe5533\\\",\\n  \\\"passed\\\": true\\n}\\n\"\n}\n",
      "parsed": {
        "argv": [
          "/opt/homebrew/opt/python@3.14/bin/python3.14",
          "-O",
          "-B",
          "/Users/alec/Documents/Math/draft_pr_actual_claims_1000_1100_20261012/reviews/case_alias_scope_20261016/scratch/clean/build_archive.py",
          "--output",
          "/Users/alec/Documents/Math/draft_pr_actual_claims_1000_1100_20261012/reviews/case_alias_scope_20261016/scratch/CLEAN/case_alias_1.zip"
        ],
        "cwd": "/Users/alec/Documents/Math/draft_pr_actual_claims_1000_1100_20261012/reviews/case_alias_scope_20261016/scratch/clean",
        "label": "pr1085_optimized_case_alias",
        "returncode": 0,
        "stderr": "",
        "stdout": "{\n  \"archive_bytes\": 495659,\n  \"archive_sha256\": \"77a2b789e16c868e8c73b6c55a726957d63ab9f50441c9b4e20828ddabbe5533\",\n  \"passed\": true\n}\n"
      }
    },
    {
      "original_file": "command_015.json",
      "bytes": 1710,
      "sha256": "1b7ed006229f1ab2d3ef671978431fe178e74ffb8b2ce67979a1f39578b13bc5",
      "exact_utf8_bytes": "{\n  \"argv\": [\n    \"/opt/homebrew/opt/python@3.14/bin/python3.14\",\n    \"-O\",\n    \"-B\",\n    \"/Users/alec/Documents/Math/draft_pr_actual_claims_1000_1100_20261012/reviews/case_alias_scope_20261016/scratch/clean/build_archive.py\",\n    \"--output\",\n    \"/Users/alec/Documents/Math/draft_pr_actual_claims_1000_1100_20261012/reviews/case_alias_scope_20261016/scratch/clean/direct_1.zip\"\n  ],\n  \"cwd\": \"/Users/alec/Documents/Math/draft_pr_actual_claims_1000_1100_20261012/reviews/case_alias_scope_20261016/scratch/clean\",\n  \"label\": \"pr1085_optimized_direct_control\",\n  \"returncode\": 1,\n  \"stderr\": \"Traceback (most recent call last):\\n  File \\\"/Users/alec/Documents/Math/draft_pr_actual_claims_1000_1100_20261012/reviews/case_alias_scope_20261016/scratch/clean/build_archive.py\\\", line 32, in <module>\\n    main()\\n    ~~~~^^\\n  File \\\"/Users/alec/Documents/Math/draft_pr_actual_claims_1000_1100_20261012/reviews/case_alias_scope_20261016/scratch/clean/build_archive.py\\\", line 26, in main\\n    out = safe_output(args.output)\\n  File \\\"/Users/alec/Documents/Math/draft_pr_actual_claims_1000_1100_20261012/reviews/case_alias_scope_20261016/scratch/clean/kit_common.py\\\", line 72, in safe_output\\n    require(target != ROOT and ROOT not in target.parents,\\n    ~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\\n            \\\"output must be outside canonical kit directory\\\")\\n            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\\n  File \\\"/Users/alec/Documents/Math/draft_pr_actual_claims_1000_1100_20261012/reviews/case_alias_scope_20261016/scratch/clean/kit_common.py\\\", line 11, in require\\n    raise ValueError(message)\\nValueError: output must be outside canonical kit directory\\n\",\n  \"stdout\": \"\"\n}\n",
      "parsed": {
        "argv": [
          "/opt/homebrew/opt/python@3.14/bin/python3.14",
          "-O",
          "-B",
          "/Users/alec/Documents/Math/draft_pr_actual_claims_1000_1100_20261012/reviews/case_alias_scope_20261016/scratch/clean/build_archive.py",
          "--output",
          "/Users/alec/Documents/Math/draft_pr_actual_claims_1000_1100_20261012/reviews/case_alias_scope_20261016/scratch/clean/direct_1.zip"
        ],
        "cwd": "/Users/alec/Documents/Math/draft_pr_actual_claims_1000_1100_20261012/reviews/case_alias_scope_20261016/scratch/clean",
        "label": "pr1085_optimized_direct_control",
        "returncode": 1,
        "stderr": "Traceback (most recent call last):\n  File \"/Users/alec/Documents/Math/draft_pr_actual_claims_1000_1100_20261012/reviews/case_alias_scope_20261016/scratch/clean/build_archive.py\", line 32, in <module>\n    main()\n    ~~~~^^\n  File \"/Users/alec/Documents/Math/draft_pr_actual_claims_1000_1100_20261012/reviews/case_alias_scope_20261016/scratch/clean/build_archive.py\", line 26, in main\n    out = safe_output(args.output)\n  File \"/Users/alec/Documents/Math/draft_pr_actual_claims_1000_1100_20261012/reviews/case_alias_scope_20261016/scratch/clean/kit_common.py\", line 72, in safe_output\n    require(target != ROOT and ROOT not in target.parents,\n    ~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n            \"output must be outside canonical kit directory\")\n            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/Users/alec/Documents/Math/draft_pr_actual_claims_1000_1100_20261012/reviews/case_alias_scope_20261016/scratch/clean/kit_common.py\", line 11, in require\n    raise ValueError(message)\nValueError: output must be outside canonical kit directory\n",
        "stdout": ""
      }
    }
  ]
}
END_COMMAND_RECEIPT_JSON

All 16 original receipt filenames and exact bytes restored and independently rehashed against the preserved original ledger. The earlier temporary names did not contain genuine final reports/pins/seals. No canonical input changed.

2026-10-16T04:13:13.148551+00:00: Completed bounded scope audit. Final original-receipt and all 2244 canonical-file hashes reverified. Three P3 support-interface findings; no canonical changes or repairs. Report/output pins/terminal seal are now genuine separately authored outputs. Bounded completion estimate: 100%. Parent goal remains incomplete.
