import os
import logging

import psycopg2
from psycopg2.extras import execute_batch

from dotenv import load_dotenv

load_dotenv()


class DatabaseManager:
    """
    Handles PostgreSQL connection,
    table creation,
    and data insertion.
    """

    def __init__(self):
        try:
            self.connection = psycopg2.connect(
                host=os.getenv("DB_HOST"),
                port=os.getenv("DB_PORT"),
                dbname=os.getenv("DB_NAME"),
                user=os.getenv("DB_USER"),
                password=os.getenv("DB_PASSWORD")
            )
            self.cursor = self.connection.cursor()
        except Exception as e:
            logging.exception(f"Database connection failed: {e}")
            raise

    def create_tables(self):
        """
        Creates database tables.
        """

        with open("database/schema.sql", "r") as file:

            sql = file.read()

        self.cursor.execute(sql)

        self.connection.commit()

        logging.info("Tables created successfully.")

    def insert_videos(self, videos_df):
        """
        Inserts videos into PostgreSQL.
        """

        sql = """
        INSERT INTO videos
        (
            video_id,
            title,
            channel,
            publish_date,
            view_count,
            like_count,
            comment_count
        )

        VALUES
        (
            %s,%s,%s,%s,%s,%s,%s
        )

        ON CONFLICT(video_id)

        DO NOTHING;
        """

        data = list(

            videos_df.itertuples(

                index=False,

                name=None

            )

        )

        execute_batch(

            self.cursor,

            sql,

            data

        )

        self.connection.commit()

        logging.info(

            f"{len(data)} videos inserted."

        )

    def insert_comments(self, comments_df):
        """
        Inserts comments into PostgreSQL.
        """

        sql = """
        INSERT INTO comments
        (
            video_id,
            author,
            comment,
            publish_date
        )

        VALUES
        (
            %s,%s,%s,%s
        );
        """

        data = list(

            comments_df.itertuples(

                index=False,

                name=None

            )

        )

        execute_batch(

            self.cursor,

            sql,

            data

        )

        self.connection.commit()

        logging.info(

            f"{len(data)} comments inserted."

        )

    def close(self):

        self.cursor.close()

        self.connection.close()

        logging.info("Database connection closed.")