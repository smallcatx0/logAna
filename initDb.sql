 
DROP TABLE IF EXISTS "main"."log_info";
CREATE TABLE "log_info" (
    "id"  INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "time"  INTEGER,
    "ip"  TEXT(16),
    "method"  TEXT(8),
    "url"  TEXT,
    "source"  TEXT
);


DROP TABLE IF EXISTS "main"."log_items";
CREATE TABLE "log_items" (
    "id"  INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "pid"  INTEGER NOT NULL,
    "level"  TEXT(8),
    "type"  TEXT(8),
    "dt"  REAL(13,4),
    "con"  TEXT,
    "source"  TEXT
);
