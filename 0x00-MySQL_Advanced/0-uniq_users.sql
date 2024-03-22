-- creates a table users following these requirements:
-- With these attributes:
-- id, integer, never null, auto increment and primary key
-- email, string (255 characters), never null and unique
-- name, string (255 characters)

CREATE TABLE IF NOT EXISTS users (
	id INT AUTO_INCREMENT UNIQUE PRIMARY KEY NOT NULL,
	email VARCHAR(255) NOT NULL,
	name VARCHAR(255));
