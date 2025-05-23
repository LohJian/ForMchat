PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE likes (
	id INTEGER NOT NULL, 
	user_id INTEGER, 
	target_user_id INTEGER, session_id TEXT, created_at TIMESTAMP, 
	PRIMARY KEY (id), 
	FOREIGN KEY(user_id) REFERENCES user (id), 
	FOREIGN KEY(target_user_id) REFERENCES user (id)
);
INSERT INTO "likes" VALUES(1,1,1,NULL,NULL);
INSERT INTO "likes" VALUES(2,NULL,1,'4f008494e479f161636094751171ef09',NULL);
INSERT INTO "likes" VALUES(3,NULL,1,'a0852f69136641c35837a8cc9cf8f7df',NULL);
INSERT INTO "likes" VALUES(4,NULL,1,'83ca53dc48c1722fe8d52e07c4d0f636',NULL);
INSERT INTO "likes" VALUES(5,123,NULL,NULL,'2025-05-10T14:24:13.057119+08:00');
INSERT INTO "likes" VALUES(6,123,NULL,NULL,'2025-05-10T14:35:37.576556+08:00');
INSERT INTO "likes" VALUES(7,NULL,1,'70811dbdf71ec48c95cfd1af7da7bda5',NULL);
INSERT INTO "likes" VALUES(8,1,1,'7effa4fe75c9e99470dc6c60c9adbb9b','2025-05-10 16:49:51.255652');
INSERT INTO "likes" VALUES(9,1,1,'7effa4fe75c9e99470dc6c60c9adbb9b','2025-05-10 16:50:30.413214');
INSERT INTO "likes" VALUES(10,1,1,'6f7659923aa581f9c378347ff2dc365e','2025-05-10 16:56:10.439879');
INSERT INTO "likes" VALUES(11,1,1,'6f7659923aa581f9c378347ff2dc365e','2025-05-10 16:56:11.413417');
INSERT INTO "likes" VALUES(12,1,1,'6f7659923aa581f9c378347ff2dc365e','2025-05-10 16:56:12.471339');
INSERT INTO "likes" VALUES(13,1,1,'6f7659923aa581f9c378347ff2dc365e','2025-05-10 16:56:13.101217');
INSERT INTO "likes" VALUES(14,1,1,'6f7659923aa581f9c378347ff2dc365e','2025-05-10 16:56:13.504825');
INSERT INTO "likes" VALUES(15,1,1,'6f7659923aa581f9c378347ff2dc365e','2025-05-10 16:56:13.661444');
INSERT INTO "likes" VALUES(16,1,1,'6f7659923aa581f9c378347ff2dc365e','2025-05-10 16:56:13.807072');
INSERT INTO "likes" VALUES(17,1,1,'6f7659923aa581f9c378347ff2dc365e','2025-05-10 16:56:13.965683');
INSERT INTO "likes" VALUES(18,1,1,'6f7659923aa581f9c378347ff2dc365e','2025-05-10 16:57:23.840682');
INSERT INTO "likes" VALUES(19,1,1,'8863580a7768b77a7bd8bd3a69452fec','2025-05-13 19:08:17.176977');
INSERT INTO "likes" VALUES(20,1,1,'d09ac2726c0abb5704d9174c70faa825','2025-05-14 14:24:35.022620');
CREATE TABLE loves (
	id INTEGER NOT NULL, 
	user_id INTEGER, 
	target_user_id INTEGER, session_id TEXT, created_at TIMESTAMP, 
	PRIMARY KEY (id), 
	FOREIGN KEY(user_id) REFERENCES user (id), 
	FOREIGN KEY(target_user_id) REFERENCES user (id)
);
INSERT INTO "loves" VALUES(1,1,1,NULL,NULL);
INSERT INTO "loves" VALUES(2,NULL,1,'4f008494e479f161636094751171ef09',NULL);
INSERT INTO "loves" VALUES(3,NULL,1,'27637e0f5e72c94d2b537613adffcd08',NULL);
INSERT INTO "loves" VALUES(4,NULL,1,'5d70eced8961cade5876380f28ecc9ec',NULL);
INSERT INTO "loves" VALUES(5,NULL,1,'83ca53dc48c1722fe8d52e07c4d0f636',NULL);
INSERT INTO "loves" VALUES(6,456,NULL,NULL,'2025-05-10T14:35:37.576556+08:00');
INSERT INTO "loves" VALUES(7,NULL,1,'610993968f765643b5d521cc24ed9810',NULL);
INSERT INTO "loves" VALUES(8,1,1,'6f7659923aa581f9c378347ff2dc365e','2025-05-10 17:07:15.039548');
INSERT INTO "loves" VALUES(9,1,1,'8863580a7768b77a7bd8bd3a69452fec','2025-05-13 19:06:35.994430');
INSERT INTO "loves" VALUES(10,1,1,'d09ac2726c0abb5704d9174c70faa825','2025-05-14 14:26:01.294591');
CREATE TABLE user (
	id INTEGER NOT NULL, 
	username VARCHAR(100) NOT NULL, 
	email VARCHAR(120) NOT NULL, 
	password VARCHAR(200) NOT NULL, 
	is_verified BOOLEAN, 
	verification_status VARCHAR(100), 
	age INTEGER, 
	race VARCHAR(50), 
	faculty VARCHAR(50), 
	sex VARCHAR(10), 
	bio TEXT, 
	location VARCHAR(100), 
	avatar VARCHAR(200), 
	likes INTEGER, 
	loves INTEGER, 
	PRIMARY KEY (id), 
	UNIQUE (email)
);
INSERT INTO "user" VALUES(1,'yyz','YIP.YU.ZHE@student.mmu.edu.my','scrypt:32768:8:1$C9LxkYpl9syActif$5ec103dd8fc4834e7d3abbe138b20228b29a7e4d2e9fcb3f7f95c7c8e5cfbcbb19cc0bb7bd2d7ddacb5885bf3136d69965a02f6141931c80ba5b92e19ea4f41b',1,'Verified',19,'Chinese','FCI','male','None any','Seremban','default.jpg',0,0);
COMMIT;
