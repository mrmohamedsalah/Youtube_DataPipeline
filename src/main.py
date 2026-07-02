import logging
from pathlib import Path

from pipeline import Pipeline
from queries import QueryManager


def setup_logging():
    """
    Configures application logging.
    """

    Path("logs").mkdir(exist_ok=True)

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler("logs/pipeline.log"),
            logging.StreamHandler()
        ]
    )


def main():

    setup_logging()

    search_query = input(
        "Enter a YouTube search keyword: "
    ).strip()

    if not search_query:
        search_query = "Data Engineering"

    # Everything below should NOT be inside the if block
    pipeline = Pipeline()

    pipeline.run(search_query)

    query_manager = QueryManager()

    query_manager.run_queries()

    query_manager.close()

    logging.info("Application completed successfully.")


if __name__ == "__main__":
    main()