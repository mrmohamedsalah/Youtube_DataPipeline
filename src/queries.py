import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()


class QueryManager:
    """
    Executes analytical queries on the PostgreSQL database.
    """

    def __init__(self):

        self.connection = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD")
        )

        self.cursor = self.connection.cursor()

    def run_queries(self):

        output = []

        queries = {

            "Top 10 Videos by Views":

            """
            SELECT
                title,
                channel,
                view_count
            FROM videos
            ORDER BY view_count DESC
            LIMIT 10;
            """,

            "Average Views Per Channel":

            """
            SELECT
                channel,
                ROUND(AVG(view_count),2) AS average_views
            FROM videos
            GROUP BY channel
            ORDER BY average_views DESC;
            """,

            "Videos Published in the Last 30 Days":

            """
            SELECT
                title,
                channel,
                publish_date
            FROM videos
            WHERE publish_date >= CURRENT_DATE - INTERVAL '30 days'
            ORDER BY publish_date DESC;
            """
        }

        for title, sql in queries.items():

            print("=" * 80)
            print(title)
            print("=" * 80)

            output.append("=" * 80)
            output.append(title)
            output.append("=" * 80)

            self.cursor.execute(sql)

            rows = self.cursor.fetchall()

            if not rows:
                print("No records found.\n")
                output.append("No records found.\n")
                continue

            for row in rows:
                print(row)
                output.append(str(row))

            print()

            output.append("\n")

        with open("query_results.txt", "w", encoding="utf-8") as file:

            file.write("\n".join(output))

    def close(self):

        self.cursor.close()
        self.connection.close()