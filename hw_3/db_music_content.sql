INSERT INTO musicians (name)
values 
('Akon'),
('Little Simz (Simbiatu Abisola Abiola Ajikawo)'),
('Paul McCartney'),
('The Rolling Stones'),
('Testing My');

INSERT INTO styles (name)
VALUES
('Rock'),
('Pop'),
('Rythm and Blues'),
('Hip-Hop'),
('Afrobit');


INSERT INTO albums (name, year)
VALUES
('El Negreeto', 2019),
('Akonda', 2020),
('Grey Area', 2019),
('Egypt Station', 2018),
('McCartney III', 2020),
('Blue and Lonesome', 2016),
('Test for My', 2015);

INSERT INTO songs (name, duration, album_id)
VALUES
('Te quiero amar', 226, 1),
('Bailame lento', 242, 1),
('Como no', 193, 1),
('Boom, Boom', 152, 1),
('Dile', 192, 1),
('Innocente', 204, 1),
('Solo Tu', 221, 1),
('Baila conmigo', 231, 1),
('Welcome To Africa', 187, 2),
('Scammers', 130, 2),
('Low Key', 193, 2),
('Bottom', 191, 2),
('Boogie Down', 178, 2),
('Take Your Place', 227, 2),
('Control', 231, 2),
('Kryptonite', 206, 2),
('Pretty Girls', 195, 2),
('Wakonda', 145, 2),
('Offence', 168, 3),
('Boss', 185, 3),
('Selfish', 226, 3),
('Wounds', 279, 3),
('Venom', 154, 3),
('101 FM', 191, 3),
('Pressure', 207, 3),
('Therapy', 195, 3),
('Sherbet Sunset', 295, 3),
('Flowers', 225, 3),
('Opening Station', 42, 4),
('I Dont Know', 267, 4),
('Come On to Me', 251, 4),
('Happy with You', 214, 4),
('Who Cares', 193, 4),
('Fuh You', 203, 4),
('Confidante', 184, 4),
('People Want Peace', 179, 4),
('Hand in Hand', 155, 4),
('Dominoes', 302, 4),
('Back in Brazil', 201, 4),
('Do It Now', 197, 4),
('Caesar Rock', 209, 4),
('Despite Repeated Warnings', 418, 4),
('Station II', 46, 4),
('Hunt You Down/Naked/C-Link', 382, 4),
('Long Tailed Winter Bird', 315, 5),
('Find My Way', 234, 5),
('Pretty Boys', 180, 5),
('Women and Wives', 172, 5),
('Lavatory Lil', 142, 5),
('Deep Deep Feeling', 505, 5),
('Slidin', 203, 5),
('The Kiss of Venus', 186, 5),
('Seize the Day', 200, 5),
('Deep Down', 352, 5),
('Winter Bird / When Winter Comes', 192, 5),
('Just Your Fool', 136, 6),
('Commit a Crime', 218, 6),
('Blue and Lonesome', 187, 6),
('All of Your Love', 286, 6),
('I Gotta Go', 206, 6),
('Everybody Knows About My Good Thing', 270, 6),
('Ride �Em On Down', 168, 6),
('Hate to See You Go', 200, 6),
('Hoo Doo Blues', 156, 6),
('Little Rain', 212, 6),
('Just Like I Treat You', 204, 6),
('I Cant Quit You Baby', 313, 6),
('my own', 130, 7),
('own my', 123, 7),
('my', 124, 7),
('oh my god', 165, 7),
('myself', 127, 7),
('by myself', 165, 7),
('bemy self', 154, 7),
('myself by', 143, 7),
('by myself by', 138, 7),
('beemy', 128, 7),
('premyne', 197, 7);

INSERT INTO musician_style
VALUES
(1, 3),
(1, 5),
(2, 3),
(2, 4),
(3, 1),
(3, 2),
(4, 1),
(5, 1);

INSERT INTO musician_album
VALUES
(1, 1),
(1, 2),
(2, 3),
(3, 4),
(3, 5),
(4, 6),
(5, 7);

INSERT INTO collections (name, year)
VALUES 
('HipHop 2019', '2019'),
('Afrobit 2020', '2020'),
('Rock collection 2018', '2018'),
('McCartney collection 2020', '2020'),
('Rock collection 2016', '2016');

INSERT INTO collection_song
VALUES
(1, 27),
(1, 28),
(1, 21),
(1, 19),
(1, 22),
(1, 20),
(1, 23),
(1, 25),
(2, 3),
(2, 1),
(2, 6),
(2, 7),
(2, 13),
(2, 17),
(2, 16),
(2, 9),
(2, 5),
(2, 4),
(2, 2),
(2, 8),
(3, 30),
(3, 35),
(3, 37),
(3, 43),
(3, 64),
(3, 63),
(3, 60),
(3, 59),
(3, 58),
(3, 61),
(3, 56),
(3, 62),
(3, 66),
(3, 65),
(3, 67),
(4, 51),
(4, 52),
(4, 53),
(4, 48),
(4, 46),
(4, 54),
(4, 49),
(4, 47),
(4, 35),
(4, 36),
(4, 37),
(4, 39),
(5, 58),
(5, 59),
(5, 60),
(5, 64),
(5, 65),
(5, 67);