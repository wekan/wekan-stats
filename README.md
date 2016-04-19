# WekanStats

Usage :

	/parser.py --help
	usage: parser.py [-h] [--action {list-stats,label-stats,user-stats}]
    
	Get some stats on Wekan Dashboard
    
	optional arguments:
	  -h, --help            show this help message and exit
	  --action {list-stats,label-stats,user-stats}


To have stats based on Lists :

	./parser.py --action list-stats
	+-------------------------+--------------------+-----------------------+---------------+
	| List name               | NB of live card(s) | NB of archive card(s) | Total card(s) |
	+-------------------------+--------------------+-----------------------+---------------+
	| Backlog                 |                 73 |                     2 |            75 |
	| Backlog for the week    |                 30 |                     0 |            30 |
	| In Progress             |                 18 |                     1 |            19 |
	| Deploy (REL / INFRADAY) |                  5 |                     0 |             5 |
	| Done                    |                  0 |                   139 |           139 |
	| Blocked                 |                 27 |                     1 |            28 |
	+-------------------------+--------------------+-----------------------+---------------+
	| Total : 6 list(s)       |                153 |                   143 |           296 |
	+-------------------------+--------------------+-----------------------+---------------+
	

To have stats based on Labels :

	./parser.py --action label-stats
	+---------------------+--------------------+-----------------------+---------------+
	| Label name          | NB of live card(s) | NB of archive card(s) | Total card(s) |
	+---------------------+--------------------+-----------------------+---------------+
	| COS                 |                  2 |                     2 |             4 |
	| July                |                  0 |                     0 |             0 |
	| August              |                  1 |                     0 |             1 |
	| Puppet              |                 17 |                     7 |            24 |
	| UNIX                |                 86 |                    76 |           162 |
	| ADM                 |                  5 |                     1 |             6 |
	| June                |                  1 |                     0 |             1 |
	| NAS                 |                 20 |                    24 |            44 |
	| MNG                 |                 10 |                     8 |            18 |
	| Infraday            |                  3 |                    10 |            13 |
	| TOT                 |                 10 |                     2 |            12 |
	| May                 |                  1 |                     0 |             1 |
	| SAN                 |                  7 |                    12 |            19 |
	| TO                  |                 87 |                    80 |           167 |
	| April               |                  5 |                     1 |             6 |
	| PAPAPAP             |                  1 |                     0 |             1 |
	| DR                  |                  2 |                     4 |             6 |
	| TOTOTOO             |                 37 |                    27 |            64 |
	| TITIT               |                 23 |                    15 |            38 |
	+---------------------+--------------------+-----------------------+---------------+
	| Total : 19 label(s) |                318 |                   269 |           587 |
	+---------------------+--------------------+-----------------------+---------------+

To have stats based on Users :

	+--------------------------+--------------------+-----------------------+---------------+
	| Username                 | NB of live card(s) | NB of archive card(s) | Total card(s) |
	+--------------------------+--------------------+-----------------------+---------------+
	| jp.tevoila               |                 10 |                     8 |            18 |
	| tototoot                 |                  1 |                     0 |             1 |
	| tototooto.tototoot       |                 12 |                    17 |            29 |
	| toitii.tototooto         |                 24 |                    33 |            57 |
	| yogourt.totot            |                  0 |                     0 |             0 |
	| mathieu.tototo           |                  0 |                     0 |             0 |
	| tototoot                 |                 11 |                    15 |            26 |
	| olivier.lesom            |                 18 |                    13 |            31 |
	| remi.totot               |                  0 |                     0 |             0 |
	| fmonthel                 |                 24 |                    28 |            52 |
	| tottoto                  |                 45 |                    36 |            81 |
	| titit.tototooto          |                  0 |                     0 |             0 |
	+--------------------------+--------------------+-----------------------+---------------+
	| Total : 12 User(s)       |                145 |                   150 |           295 |
	+--------------------------+--------------------+-----------------------+---------------+