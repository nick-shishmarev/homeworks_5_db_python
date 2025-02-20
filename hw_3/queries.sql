-- Задание 2
-- Название и продолжительность самого длительного трека.
SELECT name, to_char(duration / 60, '90') || ':' || to_char(duration % 60, '00') AS duration_minutes
FROM songs AS s 
where s.duration = (
	SELECT MAX(s2.duration)
	FROM songs AS s2);

-- Название треков, продолжительность которых не менее 3,5 минут.
SELECT name, to_char(duration / 60, '90') || ':' || to_char(duration % 60, '00') AS duration_minutes
FROM songs AS s
WHERE s.duration >= 3.5 * 60;

-- Названия сборников, вышедших в период с 2018 по 2020 год включительно.
SELECT name, to_char(year, '9999') AS release_year
FROM collections
WHERE year BETWEEN 2018 AND 2020;

-- Исполнители, чьё имя состоит из одного слова.
SELECT name 
FROM musicians
WHERE NOT name LIKE '% %';

-- Название треков, которые содержат слово «мой» или «my».
SELECT name 
FROM Songs
WHERE LOWER(name) ILIKE '% my %'
OR LOWER(name) ILIKE 'my %'
OR LOWER(name) ILIKE '% my'
OR LOWER(name) ILIKE 'my'
OR LOWER(name) ILIKE '% мой %'
OR LOWER(name) ILIKE 'мой %'
OR LOWER(name) ILIKE '% мой'
OR LOWER(name) ILIKE 'мой';

-- Задание 3
-- Количество исполнителей в каждом жанре.
SELECT st.name AS style_name, COUNT(st.name) AS musicians_count
FROM styles AS st
INNER JOIN musician_style AS ms ON ms.style_id = st.style_id
GROUP BY st.name
ORDER BY st.name;

-- Количество треков, вошедших в альбомы 2019–2020 годов.
SELECT COUNT(s.song_id) AS songs_count
FROM albums AS a
INNER JOIN songs AS s ON s.album_id = a.album_id 
WHERE a.year BETWEEN 2019 AND 2020;


-- Средняя продолжительность треков по каждому альбому.
SELECT a.name AS album_name, ROUND(AVG(s.duration),0) AS average_song_duration_seconds
FROM albums AS a
INNER JOIN songs AS s ON s.album_id = a.album_id 
GROUP BY a.name;

-- Все исполнители, которые не выпустили альбомы в 2020 году.
SELECT mus.name 
FROM musicians AS mus WHERE mus.name NOT IN
(SELECT m.name
FROM musicians AS m 
INNER JOIN musician_album AS ma ON m.musician_id = ma.musician_id 
INNER JOIN albums AS a ON a.album_id = ma.album_id
WHERE a.year = 2020);

-- Названия сборников, в которых присутствует конкретный исполнитель (выберите его сами).
SELECT DISTINCT c.name AS collection_name
FROM collections AS c 
INNER JOIN collection_song AS c2 ON c2.collection_id = c.collection_id 
INNER JOIN songs AS s ON c2.song_id = s.song_id 
INNER JOIN albums AS a ON a.album_id = s.album_id 
INNER JOIN musician_album AS ma ON ma.album_id = a.album_id 
INNER JOIN musicians AS m ON m.musician_id = ma.musician_id 
WHERE m.name = 'Paul McCartney';

-- Задание 4(необязательное)

-- Названия альбомов, в которых присутствуют исполнители более чем одного жанра.
SELECT a.name 
FROM albums AS a
INNER JOIN musician_album AS ma ON ma.album_id = a.album_id
INNER JOIN (SELECT musician_id 
			FROM musicians AS mus
			INNER JOIN (SELECT m.name, COUNT(ms.style_id) AS count_style
						FROM musicians AS m 
						INNER JOIN musician_style AS ms ON ms.musician_id = m.musician_id 
						GROUP BY m.name) AS st ON st.name = mus.name
			WHERE st.count_style > 1) AS m2 ON ma.musician_id = m2.musician_id;

-- Наименования треков, которые не входят в сборники.
SELECT name AS song_name
FROM songs
WHERE name NOT IN 
	(SELECT s.name
	FROM songs AS s 
	INNER JOIN collection_song AS c ON c.song_id = s.song_id); 

-- Исполнитель или исполнители, написавшие самый короткий по продолжительности трек, — теоретически таких треков может быть несколько.
SELECT m.name AS musician_name, s.name AS song_name, to_char(s.duration / 60, '90') || ':' || to_char(s.duration % 60, '00') AS duration 
FROM songs AS s
INNER JOIN albums AS a ON a.album_id = s.album_id 
INNER JOIN musician_album AS ma ON ma.album_id = a.album_id 
INNER JOIN musicians AS m ON m.musician_id = ma.musician_id 
WHERE duration = (
	SELECT MIN(s1.duration)
	FROM songs AS s1
	);

-- Названия альбомов, содержащих наименьшее количество треков.
SELECT a1.name AS album_name, a1.song_count 
FROM (SELECT a.name, COUNT(s.song_id) AS song_count
	  FROM albums AS a 
	  INNER JOIN songs AS s ON s.album_id = a.album_id
	  GROUP BY a.name) AS a1
WHERE a1.song_count = (
	SELECT MIN(a3.song_count)
	FROM (SELECT a2.name, COUNT(s2.song_id) AS song_count
	      FROM albums AS a2 
	      INNER JOIN songs AS s2 ON s2.album_id = a2.album_id
	      GROUP BY a2.name) AS a3);