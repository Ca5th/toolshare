INSERT INTO toolshareapp_toolcategory VALUES (1, 'Building');
INSERT INTO toolshareapp_toolcategory VALUES (2, 'Carpentry');
INSERT INTO toolshareapp_toolcategory VALUES (3, 'Plumbing');
INSERT INTO toolshareapp_toolcategory VALUES (4, 'Landscaping');

UPDATE auth_user SET email = 'toolshare.team.d@gmail.com' WHERE id = 1;

INSERT INTO toolshareapp_user VALUES (1, 'toolshare.team.d@gmail.com', 'teamd', 'teamd', 'teamd', '2013-11-21 01:53:49.881287', '000', '000', '000', '00000', '2013-11-21 01:53:49.881287', '000', 1, '000', 1, 'Regular', 'user/Koala_7.jpg');

INSERT INTO django_site VALUES ('2', '127.0.0.1:8000', 'localhost');