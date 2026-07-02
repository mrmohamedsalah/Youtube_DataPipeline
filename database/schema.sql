DROP TABLE IF EXISTS comments;
DROP TABLE IF EXISTS videos;

CREATE TABLE videos (

    video_id VARCHAR(50) PRIMARY KEY,

    title TEXT NOT NULL,

    channel VARCHAR(255),

    publish_date TIMESTAMP,

    view_count BIGINT,

    like_count BIGINT,

    comment_count BIGINT

);

CREATE TABLE comments (

    comment_id SERIAL PRIMARY KEY,

    video_id VARCHAR(50),

    author VARCHAR(255),

    comment TEXT,

    publish_date TIMESTAMP,

    CONSTRAINT fk_video
        FOREIGN KEY(video_id)
        REFERENCES videos(video_id)
        ON DELETE CASCADE

);