[33mcommit 2f87c0dda9863de9264f230d5ca4bd0e58c49d9d[m[33m ([m[1;36mHEAD[m[33m -> [m[1;32mYipPart[m[33m, [m[1;31morigin/YipPart[m[33m)[m
Author: YIP YU ZHE <yipyuzhe1402@gamil.com>
Date:   Tue Apr 15 20:17:33 2025 +0800

    Add .gitignore to ignore venv folder

 instance/users.db  | Bin [31m12288[m -> [32m0[m bytes
 website/.gitignore |   1 [32m+[m
 2 files changed, 1 insertion(+)

[33mcommit 03974be243b1cbf856101d64246cc8644ffa6de6[m
Author: YIP YU ZHE <yipyuzhe1402@gamil.com>
Date:   Mon Apr 14 21:48:14 2025 +0800

    sign up and password hashing done

 instance/users.db                                  |  Bin [31m0[m -> [32m12288[m bytes
 .../site-packages/pip-24.0.dist-info/AUTHORS.txt   |  760 [31m--[m
 .../Lib/site-packages/pip-24.0.dist-info/INSTALLER |    1 [31m-[m
 .../site-packages/pip-24.0.dist-info/LICENSE.txt   |   20 [31m-[m
 venv/Lib/site-packages/pip-24.0.dist-info/METADATA |   88 [31m-[m
 venv/Lib/site-packages/pip-24.0.dist-info/RECORD   | 1024 [31m---[m
 .../Lib/site-packages/pip-24.0.dist-info/REQUESTED |    0
 venv/Lib/site-packages/pip-24.0.dist-info/WHEEL    |    5 [31m-[m
 .../pip-24.0.dist-info/entry_points.txt            |    4 [31m-[m
 .../site-packages/pip-24.0.dist-info/top_level.txt |    1 [31m-[m
 venv/Lib/site-packages/pip/__init__.py             |   13 [31m-[m
 venv/Lib/site-packages/pip/__main__.py             |   24 [31m-[m
 venv/Lib/site-packages/pip/__pip-runner__.py       |   50 [31m-[m
 .../pip/__pycache__/__init__.cpython-312.pyc       |  Bin [31m675[m -> [32m0[m bytes
 .../pip/__pycache__/__main__.cpython-312.pyc       |  Bin [31m831[m -> [32m0[m bytes
 .../pip/__pycache__/__pip-runner__.cpython-312.pyc |  Bin [31m2189[m -> [32m0[m bytes
 venv/Lib/site-packages/pip/_internal/__init__.py   |   18 [31m-[m
 .../_internal/__pycache__/__init__.cpython-312.pyc |  Bin [31m777[m -> [32m0[m bytes
 .../__pycache__/build_env.cpython-312.pyc          |  Bin [31m14281[m -> [32m0[m bytes
 .../_internal/__pycache__/cache.cpython-312.pyc    |  Bin [31m12650[m -> [32m0[m bytes
 .../__pycache__/configuration.cpython-312.pyc      |  Bin [31m17647[m -> [32m0[m bytes
 .../__pycache__/exceptions.cpython-312.pyc         |  Bin [31m33265[m -> [32m0[m bytes
 .../pip/_internal/__pycache__/main.cpython-312.pyc |  Bin [31m660[m -> [32m0[m bytes
 .../__pycache__/pyproject.cpython-312.pyc          |  Bin [31m4955[m -> [32m0[m bytes
 .../self_outdated_check.cpython-312.pyc            |  Bin [31m10542[m -> [32m0[m bytes
 .../__pycache__/wheel_builder.cpython-312.pyc      |  Bin [31m13615[m -> [32m0[m bytes
 venv/Lib/site-packages/pip/_internal/build_env.py  |  311 [31m-[m
 venv/Lib/site-packages/pip/_internal/cache.py      |  290 [31m-[m
 .../site-packages/pip/_internal/cli/__init__.py    |    4 [31m-[m
 .../cli/__pycache__/__init__.cpython-312.pyc       |  Bin [31m268[m -> [32m0[m bytes
 .../cli/__pycache__/autocompletion.cpython-312.pyc |  Bin [31m8455[m -> [32m0[m bytes
 .../cli/__pycache__/base_command.cpython-312.pyc   |  Bin [31m10439[m -> [32m0[m bytes
 .../cli/__pycache__/cmdoptions.cpython-312.pyc     |  Bin [31m30364[m -> [32m0[m bytes
 .../__pycache__/command_context.cpython-312.pyc    |  Bin [31m1765[m -> [32m0[m bytes
 .../_internal/cli/__pycache__/main.cpython-312.pyc |  Bin [31m2288[m -> [32m0[m bytes
 .../cli/__pycache__/main_parser.cpython-312.pyc    |  Bin [31m4895[m -> [32m0[m bytes
 .../cli/__pycache__/parser.cpython-312.pyc         |  Bin [31m14992[m -> [32m0[m bytes
 .../cli/__pycache__/progress_bars.cpython-312.pyc  |  Bin [31m2607[m -> [32m0[m bytes
 .../cli/__pycache__/req_command.cpython-312.pyc    |  Bin [31m18827[m -> [32m0[m bytes
 .../cli/__pycache__/spinners.cpython-312.pyc       |  Bin [31m7824[m -> [32m0[m bytes
 .../cli/__pycache__/status_codes.cpython-312.pyc   |  Bin [31m365[m -> [32m0[m bytes
 .../pip/_internal/cli/autocompletion.py            |  172 [31m-[m
 .../pip/_internal/cli/base_command.py              |  236 [31m-[m
 .../site-packages/pip/_internal/cli/cmdoptions.py  | 1074 [31m---[m
 .../pip/_internal/cli/command_context.py           |   27 [31m-[m
 venv/Lib/site-packages/pip/_internal/cli/main.py   |   79 [31m-[m
 .../site-packages/pip/_internal/cli/main_parser.py |  134 [31m-[m
 venv/Lib/site-packages/pip/_internal/cli/parser.py |  294 [31m-[m
 .../pip/_internal/cli/progress_bars.py             |   68 [31m-[m
 .../site-packages/pip/_internal/cli/req_command.py |  505 [31m--[m
 .../site-packages/pip/_internal/cli/spinners.py    |  159 [31m-[m
 .../pip/_internal/cli/status_codes.py              |    6 [31m-[m
 .../pip/_internal/commands/__init__.py             |  132 [31m-[m
 .../commands/__pycache__/__init__.cpython-312.pyc  |  Bin [31m3992[m -> [32m0[m bytes
 .../commands/__pycache__/cache.cpython-312.pyc     |  Bin [31m9701[m -> [32m0[m bytes
 .../commands/__pycache__/check.cpython-312.pyc     |  Bin [31m2080[m -> [32m0[m bytes
 .../__pycache__/completion.cpython-312.pyc         |  Bin [31m5182[m -> [32m0[m bytes
 .../__pycache__/configuration.cpython-312.pyc      |  Bin [31m13202[m -> [32m0[m bytes
 .../commands/__pycache__/debug.cpython-312.pyc     |  Bin [31m10148[m -> [32m0[m bytes
 .../commands/__pycache__/download.cpython-312.pyc  |  Bin [31m7576[m -> [32m0[m bytes
 .../commands/__pycache__/freeze.cpython-312.pyc    |  Bin [31m4346[m -> [32m0[m bytes
 .../commands/__pycache__/hash.cpython-312.pyc      |  Bin [31m2973[m -> [32m0[m bytes
 .../commands/__pycache__/help.cpython-312.pyc      |  Bin [31m1663[m -> [32m0[m bytes
 .../commands/__pycache__/index.cpython-312.pyc     |  Bin [31m6710[m -> [32m0[m bytes
 .../commands/__pycache__/inspect.cpython-312.pyc   |  Bin [31m3965[m -> [32m0[m bytes
 .../commands/__pycache__/install.cpython-312.pyc   |  Bin [31m28895[m -> [32m0[m bytes
 .../commands/__pycache__/list.cpython-312.pyc      |  Bin [31m15390[m -> [32m0[m bytes
 .../commands/__pycache__/search.cpython-312.pyc    |  Bin [31m7608[m -> [32m0[m bytes
 .../commands/__pycache__/show.cpython-312.pyc      |  Bin [31m9718[m -> [32m0[m bytes
 .../commands/__pycache__/uninstall.cpython-312.pyc |  Bin [31m4716[m -> [32m0[m bytes
 .../commands/__pycache__/wheel.cpython-312.pyc     |  Bin [31m8940[m -> [32m0[m bytes
 .../site-packages/pip/_internal/commands/cache.py  |  225 [31m-[m
 .../site-packages/pip/_internal/commands/check.py  |   54 [31m-[m
 .../pip/_internal/commands/completion.py           |  130 [31m-[m
 .../pip/_internal/commands/configuration.py        |  280 [31m-[m
 .../site-packages/pip/_internal/commands/debug.py  |  201 [31m-[m
 .../pip/_internal/commands/download.py             |  147 [31m-[m
 .../site-packages/pip/_internal/commands/freeze.py |  108 [31m-[m
 .../site-packages/pip/_internal/commands/hash.py   |   59 [31m-[m
 .../site-packages/pip/_internal/commands/help.py   |   41 [31m-[m
 .../site-packages/pip/_internal/commands/index.py  |  139 [31m-[m
 .../pip/_internal/commands/inspect.py              |   92 [31m-[m
 .../pip/_internal/commands/install.py              |  774 [31m--[m
 .../site-packages/pip/_internal/commands/list.py   |  368 [31m-[m
 .../site-packages/pip/_internal/commands/search.py |  174 [31m-[m
 .../site-packages/pip/_internal/commands/show.py   |  189 [31m-[m
 .../pip/_internal/commands/uninstall.py            |  113 [31m-[m
 .../site-packages/pip/_internal/commands/wheel.py  |  183 [31m-[m
 .../site-packages/pip/_internal/configuration.py   |  383 [31m-[m
 .../pip/_internal/distributions/__init__.py        |   21 [31m-[m
 .../__pycache__/__init__.cpython-312.pyc           |  Bin [31m931[m -> [32m0[m bytes
 .../distributions/__pycache__/base.cpython-312.pyc |  Bin [31m2852[m -> [32m0[m bytes
 .../__pycache__/installed.cpython-312.pyc          |  Bin [31m1687[m -> [32m0[m bytes
 .../__pycache__/sdist.cpython-312.pyc              |  Bin [31m8464[m -> [32m0[m bytes
 .../__pycache__/wheel.cpython-312.pyc              |  Bin [31m2233[m -> [32m0