CREATE TABLE IF NOT EXISTS musicians (
	PRIMARY KEY (musician_id),
	musician_id SERIAL  ,
	name VARCHAR(60) NOT NULL
);

CREATE TABLE IF NOT EXISTS styles (
	PRIMARY KEY (style_id),
	style_id SERIAL,
	name VARCHAR(60) NOT NULL
);

CREATE TABLE IF NOT EXISTS albums (
	PRIMARY KEY (album_id),
	album_id SERIAL,
	name VARCHAR(60) NOT NULL,
	year NUMERIC(4)  CHECK (year BETWEEN 1920 AND EXTRACT(YEAR FROM NOW()))
);

CREATE TABLE IF NOT EXISTS songs (
	PRIMARY KEY (song_id),
	song_id SERIAL,
	name VARCHAR(60) NOT NULL,
	duration INTEGER CHECK (duration > 20),
	album_id INTEGER NOT NULL, 
	FOREIGN KEY (album_id) REFERENCES albums(album_id)
);

CREATE TABLE IF NOT EXISTS collections (
	PRIMARY KEY (collection_id),
	collection_id SERIAL,
	name VARCHAR(60) NOT NULL,
	year NUMERIC(4) CHECK (year BETWEEN 1920 AND EXTRACT(YEAR FROM NOW()))
);

CREATE TABLE IF NOT EXISTS musician_style (
	PRIMARY KEY (musician_id, style_id),
	musician_id INTEGER,
	style_id INTEGER,
--	CONSTRAINT mst PRIMARY KEY (musician_id, style_id),
	FOREIGN KEY (musician_id) REFERENCES musicians(musician_id),
	FOREIGN KEY (style_id) REFERENCES styles(style_id) 
);

CREATE TABLE IF NOT EXISTS musician_album (
	PRIMARY KEY (musician_id, album_id),
	musician_id INTEGER,
	album_id INTEGER,
--	CONSTRAINT ma PRIMARY KEY (musician_id, album_id),
	FOREIGN KEY (musician_id) REFERENCES musicians(musician_id),
	FOREIGN KEY (album_id) REFERENCES albums(album_id) 
);

CREATE TABLE IF NOT EXISTS collection_song (
	PRIMARY KEY (collection_id, song_id),
	collection_id INTEGER,
	song_id INTEGER,
--	CONSTRAINT ms PRIMARY KEY (collection_id, song_id),
	FOREIGN KEY (collection_id) REFERENCES Collections(collection_id),
	FOREIGN KEY (song_id) REFERENCES Songs(song_id) 
);