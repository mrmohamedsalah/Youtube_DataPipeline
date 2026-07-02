import logging
from typing import Dict, List, Optional
from urllib import response

import requests
from dotenv import load_dotenv
import os


load_dotenv()


class APIClient:
    """
    Handles communication with the YouTube Data API v3.
    """

    BASE_URL = "https://www.googleapis.com/youtube/v3"

    def __init__(self):
        self.api_key = os.getenv("YOUTUBE_API_KEY")

        if not self.api_key:
            raise ValueError("YOUTUBE_API_KEY not found in .env file")

        self.session = requests.Session()

    def _make_request(
        self,
        endpoint: str,
        params: Dict
    ) -> Optional[Dict]:
        """
        Sends a GET request to the YouTube API.

        Returns:
            JSON response if successful.
            None if the request fails.
        """

        url = f"{self.BASE_URL}/{endpoint}"

        params["key"] = self.api_key

        try:
            response = self.session.get(
                url,
                params=params,
                timeout=20
            )

            response.raise_for_status()

            return response.json()

        except requests.exceptions.Timeout:
            logging.error("Request timed out.")

        except requests.exceptions.HTTPError:
            logging.error(response.text)

        except requests.exceptions.RequestException as e:
            logging.error(f"Request failed: {e}")

        return None

    def search_videos(self, query: str, max_results: int = 50) -> List[Dict]:
        """
        Searches YouTube videos and returns up to max_results videos.
        """

        videos = []
        next_page_token = None

        while len(videos) < max_results:

            remaining = min(50, max_results - len(videos))

            params = {
                "part": "snippet",
                "q": query,
                "type": "video",
                "maxResults": remaining
            }

            if next_page_token:
                params["pageToken"] = next_page_token

            response = self._make_request("search", params)

            if response is None:
                break

            for item in response.get("items", []):

                video_id = item.get("id", {}).get("videoId")

                if not video_id:
                    continue

                snippet = item.get("snippet", {})

                videos.append({
                    "video_id": video_id,
                    "title": snippet.get("title"),
                    "channel": snippet.get("channelTitle"),
                    "publish_date": snippet.get("publishedAt")
                })

            next_page_token = response.get("nextPageToken")

            if not next_page_token:
                break

        logging.info(f"Retrieved {len(videos)} videos.")

        return videos
    def get_video_statistics(
        self,
        video_id: str
    ) -> Dict:
        """
        Retrieves statistics for a single video.
        """

        params = {
            "part": "statistics",
            "id": video_id
        }

        response = self._make_request("videos", params)

        if response is None:
            return {}

        items = response.get("items", [])

        if not items:
            return {}

        statistics = items[0].get("statistics", {})

        return {
            "view_count": statistics.get("viewCount"),
            "like_count": statistics.get("likeCount"),
            "comment_count": statistics.get("commentCount")
        }

    def get_video_comments(
        self,
        video_id: str,
        max_results: int = 100
    ) -> List[Dict]:
        """
        Retrieves comments for one video.

        Returns:
            List of comment dictionaries.
        """

        params = {
            "part": "snippet",
            "videoId": video_id,
            "maxResults": max_results,
            "textFormat": "plainText"
        }

        response = self._make_request(
            "commentThreads",
            params
        )

        if response is None:
            return []

        comments = []

        for item in response.get("items", []):

            snippet = (
                item.get("snippet", {})
                .get("topLevelComment", {})
                .get("snippet", {})
            )

            comments.append({
                "author": snippet.get("authorDisplayName"),
                "text": snippet.get("textDisplay"),
                "publish_date": snippet.get("publishedAt")
            })

        logging.info(
            f"Retrieved {len(comments)} comments for {video_id}"
        )

        return comments