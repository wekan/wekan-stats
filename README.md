# WekanStats

Usage :

	./get-stats.py --help
	usage: get-stats.py [-h] [--action {list-stats,label-stats,user-stats}]
    
	Get some stats on Wekan Dashboard
    
	optional arguments:
	  -h, --help            show this help message and exit
	  --action {list-stats,label-stats,user-stats}


To have stats based on Lists :

	./get-stats.py  --board msc-unix-sto --action list-stats
    INFO:WekanStats.WsMotor:Creating an instance of WsMotor
    INFO:WekanStats.WsMotor:Will export below JSON Wekan URL for board msc-unix-sto to a class dic : http://mon-url
    INFO:WekanStats.WsMotor:Will order for a board msc-unix-sto class dic branch labels
    INFO:WekanStats.WsMotor:Will order for a board msc-unix-sto class dic branch users
    +-------------------------+--------------------+--------------------+------------------------+---------------+
    | List name               | Event(s) generated | NB of live card(s) | NB of archived card(s) | Total card(s) |
    +-------------------------+--------------------+--------------------+------------------------+---------------+
    | Backlog                 |                163 |                 73 |                      2 |            75 |
    | Backlog for the week    |                196 |                 30 |                      0 |            30 |
    | In Progress             |                163 |                 18 |                      1 |            19 |
    | Deploy (REL / INFRADAY) |                 33 |                  5 |                      0 |             5 |
    | Done                    |                306 |                  0 |                    139 |           139 |
    | Blocked                 |                 77 |                 27 |                      1 |            28 |
    +-------------------------+--------------------+--------------------+------------------------+---------------+
    | Total : 6 list(s)       |                938 |                153 |                    143 |           296 |
    +-------------------------+--------------------+--------------------+------------------------+---------------+


To have stats based on Labels :

	./get-stats.py  --board msc-unix-sto --action label-stats
	INFO:WekanStats.WsMotor:Creating an instance of WsMotor
	INFO:WekanStats.WsMotor:Will export below JSON Wekan URL for board msc-unix-sto to a class dic : http://mon-url
	INFO:WekanStats.WsMotor:Will order for a board msc-unix-sto class dic branch labels
	INFO:WekanStats.WsMotor:Will order for a board msc-unix-sto class dic branch users
	+---------------------+--------------------+------------------------+---------------+
	| Label name          | NB of live card(s) | NB of archived card(s) | Total card(s) |
	+---------------------+--------------------+------------------------+---------------+
	| TG                  |                 87 |                     80 |           167 |
	| UNIX                |                 86 |                     76 |           162 |
	| NewHome             |                 37 |                     27 |            64 |
	| BURGER              |                 23 |                     15 |            38 |
	| NOS                 |                 20 |                     24 |            44 |
	| Puppet              |                 17 |                      7 |            24 |
	| MNG                 |                 10 |                      8 |            18 |
	| RTT                 |                 10 |                      2 |            12 |
	| SON                 |                  7 |                     12 |            19 |
	| April               |                  5 |                      1 |             6 |
	| ADM                 |                  5 |                      1 |             6 |
	| Infraday            |                  3 |                     10 |            13 |
	| CAS                 |                  2 |                      2 |             4 |
	| DR                  |                  2 |                      4 |             6 |
	| June                |                  1 |                      0 |             1 |
	| August              |                  1 |                      0 |             1 |
	| Tonton              |                  1 |                      0 |             1 |
	| May                 |                  1 |                      0 |             1 |
	| July                |                  0 |                      0 |             0 |
	+---------------------+--------------------+------------------------+---------------+
	| Total : 19 label(s) |                318 |                    269 |           587 |
	+---------------------+--------------------+------------------------+---------------+

To have stats based on Users :

	./get-stats.py  --board msc-unix-sto --action user-stats
    INFO:WekanStats.WsMotor:Creating an instance of WsMotor
    INFO:WekanStats.WsMotor:Will export below JSON Wekan URL for board msc-unix-sto to a class dic : http://mon-url
    INFO:WekanStats.WsMotor:Will order for a board msc-unix-sto class dic branch labels
    INFO:WekanStats.WsMotor:Will order for a board msc-unix-sto class dic branch users
    +--------------------------+--------------------+--------------------+------------------------+---------------+
    | Username                 | Event(s) generated | NB of live card(s) | NB of archived card(s) | Total card(s) |
    +--------------------------+--------------------+--------------------+------------------------+---------------+
    | nholooo                  |                333 |                 45 |                     36 |            81 |
    | konan.dujardin           |                240 |                 24 |                     33 |            57 |
    | fmonthel                 |                453 |                 24 |                     28 |            52 |
    | olivier.sommelier        |                125 |                 18 |                     13 |            31 |
    | yannick.aimelekart       |                138 |                 12 |                     17 |            29 |
    | basile.tho               |                106 |                 11 |                     15 |            26 |
    | carlos.legrec            |                 81 |                 10 |                      8 |            18 |
    | leon.vo                  |                  0 |                  1 |                      0 |             1 |
    +--------------------------+--------------------+--------------------+------------------------+---------------+
    | Total : 8 User(s)        |               1476 |                145 |                    150 |           295 |
    +--------------------------+--------------------+--------------------+------------------------+---------------+

To have stats based on Events :

	./get-stats.py  --board msc-unix-sto --action event-stats
	INFO:WekanStats.WsMotor:Creating an instance of WsMotor
	INFO:WekanStats.WsMotor:Will export below JSON Wekan URL for board msc-unix-sto to a class dic : http://mon-url
	INFO:WekanStats.WsMotor:Will order for a board msc-unix-sto class dic branch labels
	INFO:WekanStats.WsMotor:Will order for a board msc-unix-sto class dic branch users
	+---------------------+----------------+
	| Event name          | NB of event(s) |
	+---------------------+----------------+
	| createCard          |            296 |
	| archivedList        |              1 |
	| addBoardMember      |             11 |
	| moveCard            |            475 |
	| addComment          |            197 |
	| unjoinMember        |             17 |
	| archivedCard        |            160 |
	| joinMember          |            312 |
	| createList          |              6 |
	| createBoard         |              1 |
	+---------------------+----------------+
	| Total : 10 Event(s) |           1476 |
	+---------------------+----------------+