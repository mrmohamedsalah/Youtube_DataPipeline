import logging
from typing import List, Dict

import pandas as pd


class Transformer:
    """
    Cleans and transforms raw YouTube API data
    into analysis-ready tables.
    """

    def transform(self, raw_data: List[Dict]):
        """
        Transforms nested JSON into two flat DataFrames:
        1. Videos
        2. Comments
        """

        videos = []
        comments = []

        for item in raw_data:

            video = item.get("video", {})
            statistics = item.get("statistics", {})
            video_comments = item.get("comments", [])

            # -----------------------------
            # Video Record
            # -----------------------------

            videos.append({

                "video_id": video.get("video_id"),

                "title": video.get("title"),

                "channel": video.get("channel"),

                "publish_date": video.get("publish_date"),

                "view_count": int(
                    statistics.get("view_count", 0) or 0
                ),

                "like_count": int(
                    statistics.get("like_count", 0) or 0
                ),

                "comment_count": int(
                    statistics.get("comment_count", 0) or 0
                )

            })

            # -----------------------------
            # Comment Records
            # -----------------------------

            for comment in video_comments:

                comments.append({

                    "video_id": video.get("video_id"),

                    "author": comment.get("author"),

                    "comment": comment.get("text"),

                    "publish_date": comment.get("publish_date")

                })

        videos_df = pd.DataFrame(videos)

        comments_df = pd.DataFrame(comments)

        logging.info(
            f"Videos transformed: {len(videos_df)}"
        )

        logging.info(
            f"Comments transformed: {len(comments_df)}"
        )

        return videos_df, comments_df