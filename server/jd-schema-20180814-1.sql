BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS `users` (
	`uid`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	`username`	TEXT NOT NULL UNIQUE,
	`email`	TEXT NOT NULL,
	`password`	TEXT NOT NULL,
	`signature`	TEXT NOT NULL,
	`language`	TEXT NOT NULL DEFAULT 'C++',
	`register_time`	TEXT NOT NULL DEFAULT '2018-08-14 09:00:00'
);
CREATE TABLE IF NOT EXISTS `submissions` (
	`sid`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	`pid`	TEXT NOT NULL,
	`time`	INTEGER NOT NULL DEFAULT 0,
	`memory`	INTEGER NOT NULL DEFAULT 0,
	`score`	REAL NOT NULL DEFAULT 0,
	`code`	TEXT NOT NULL,
	`code_length`	INTEGER NOT NULL DEFAULT 0,
	`submit_time`	TEXT NOT NULL DEFAULT '2000-01-01 00:00',
	`judge_time`	TEXT NOT NULL DEFAULT 'N/A',
	`player_name`	TEXT NOT NULL,
	`language`	TEXT NOT NULL DEFAULT 'C++',
	`status`	TEXT NOT NULL DEFAULT 'Unknown',
	`status_short`	TEXT NOT NULL DEFAULT '',
	`detail`	TEXT NOT NULL DEFAULT '',
	`saved`	INTEGER NOT NULL DEFAULT 0
);
CREATE TABLE IF NOT EXISTS `problems` (
	`pid`	TEXT NOT NULL UNIQUE,
	`name`	TEXT NOT NULL,
	`description`	TEXT NOT NULL,
	`time_limit`	INTEGER NOT NULL DEFAULT 1000000,
	`memory_limit`	INTEGER NOT NULL DEFAULT 512,
	`statement`	TEXT NOT NULL,
	`statement_html`	TEXT NOT NULL,
	`sample_code`	TEXT NOT NULL,
	`class`	TEXT NOT NULL DEFAULT 'traditional',
	`hidden`	INTEGER NOT NULL DEFAULT 1
);
CREATE TABLE IF NOT EXISTS `jd_meta` (
	`key`	TEXT NOT NULL UNIQUE,
	`value`	TEXT NOT NULL
);
CREATE UNIQUE INDEX IF NOT EXISTS `username` ON `users` (
	`username`
);
CREATE UNIQUE INDEX IF NOT EXISTS `uid` ON `users` (
	`uid`
);
CREATE INDEX IF NOT EXISTS `submissions_score` ON `submissions` (
	`score`
);
CREATE INDEX IF NOT EXISTS `submissions_saved` ON `submissions` (
	`saved`
);
CREATE INDEX IF NOT EXISTS `submissions_player_name` ON `submissions` (
	`player_name`
);
CREATE INDEX IF NOT EXISTS `submissions_pid` ON `submissions` (
	`pid`
);
CREATE UNIQUE INDEX IF NOT EXISTS `sid` ON `submissions` (
	`sid`
);
CREATE INDEX IF NOT EXISTS `problem_hidden` ON `problems` (
	`hidden`
);
CREATE INDEX IF NOT EXISTS `problem_class` ON `problems` (
	`class`
);
CREATE UNIQUE INDEX IF NOT EXISTS `pid` ON `problems` (
	`pid`
);
CREATE UNIQUE INDEX IF NOT EXISTS `jd_meta_key` ON `jd_meta` (
	`key`
);
COMMIT;
