CREATE TABLE IF NOT EXISTS Musicians (
	musician_id SERIAL PRIMARY KEY,
	name VARCHAR(60) NOT NULL
);

CREATE TABLE IF NOT EXISTS Styles (
	style_id SERIAL PRIMARY KEY,
	name VARCHAR(60) NOT NULL
);

CREATE TABLE IF NOT EXISTS Albums (
	album_id SERIAL PRIMARY KEY,
	name VARCHAR(60) NOT NULL,
	year CHAR(4)  NOT NULL
);

CREATE TABLE IF NOT EXISTS Songs (
	song_id SERIAL PRIMARY KEY,
	name VARCHAR(60) NOT NULL,
	duration DECIMAL(6,2) CHECK (duration > 0),
	album_id INTEGER REFERENCES Albums(album_id)
);

CREATE TABLE IF NOT EXISTS Collections (
	collection_id SERIAL PRIMARY KEY,
	name VARCHAR(60) NOT NULL,
	year CHAR(4)  NOT NULL
);


CREATE TABLE IF NOT EXISTS MusicianStyle (
	musician_id INTEGER REFERENCES Musicians(musician_id),
	style_id INTEGER REFERENCES Styles(style_id),
	CONSTRAINT mst PRIMARY KEY (musician_id, style_id)
);

CREATE TABLE IF NOT EXISTS MusicianAlbum (
	musician_id INTEGER REFERENCES Musicians(musician_id),
	album_id INTEGER REFERENCES Albums(album_id),
	CONSTRAINT ma PRIMARY KEY (musician_id, album_id)
);

CREATE TABLE IF NOT EXISTS CollectionSong (
	collection_id INTEGER REFERENCES Collections(collection_id),
	song_id INTEGER REFERENCES Songs(song_id),
	CONSTRAINT ms PRIMARY KEY (collection_id, song_id)
);

