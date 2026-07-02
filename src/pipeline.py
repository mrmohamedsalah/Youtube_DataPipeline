import json
import logging
from pathlib import Path

from api_client import APIClient
from transformer import Transformer
from database import DatabaseManager


class Pipeline:
    """
    Orchestrates the entire data pipeline.
    """

    def __init__(self):
        self.api_client = APIClient()
        self.transformer = Transformer()
        self.database = DatabaseManager()

        self.raw_data_path = Path("data/raw")
        self.processed_data_path = Path("data/processed")

        self.raw_data_path.mkdir(parents=True, exist_ok=True)
        self.processed_data_path.mkdir(parents=True, exist_ok=True)

    def run(self, search_query: str):
        """
        Executes the complete pipeline.
        """

        logging.info("========== Pipeline Started ==========")

        # --------------------------------------------------
        # STEP 1: Search videos
        # --------------------------------------------------

        videos = self.api_client.search_videos(
            query=search_query,
            max_results=50
        )

        logging.info(f"Found {len(videos)} videos.")

        raw_dataset = []

        # --------------------------------------------------
        # STEP 2: Collect statistics & comments
        # --------------------------------------------------

        for index, video in enumerate(videos, start=1):

            logging.info(
                f"Processing video {index}/{len(videos)}"
            )

            statistics = self.api_client.get_video_statistics(
                video["video_id"]
            )

            comments = self.api_client.get_video_comments(
                video["video_id"]
            )

            raw_dataset.append(
                {
                    "video": video,
                    "statistics": statistics,
                    "comments": comments
                }
            )

        # --------------------------------------------------
        # STEP 3: Save raw JSON (Landing Zone)
        # --------------------------------------------------

        raw_file = self.raw_data_path / "youtube_raw.json"

        with open(raw_file, "w", encoding="utf-8") as file:
            json.dump(
                raw_dataset,
                file,
                indent=4,
                ensure_ascii=False
            )

        logging.info("Raw JSON saved successfully.")

        # --------------------------------------------------
        # STEP 4: Transform data
        # --------------------------------------------------

        videos_df, comments_df = self.transformer.transform(
            raw_dataset
        )

        # Save processed CSVs

        videos_df.to_csv(
            self.processed_data_path / "videos.csv",
            index=False
        )

        comments_df.to_csv(
            self.processed_data_path / "comments.csv",
            index=False
        )

        logging.info("Transformation completed.")

        # --------------------------------------------------
        # STEP 5: Create Database Tables
        # --------------------------------------------------

        self.database.create_tables()

        # --------------------------------------------------
        # STEP 6: Insert Data
        # --------------------------------------------------

        self.database.insert_videos(videos_df)

        self.database.insert_comments(comments_df)

        logging.info("Database loading completed.")
        
        self.database.close()

        logging.info("========== Pipeline Finished ==========")