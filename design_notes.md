# Design Notes

## Q1 — Why did you structure your solution the way you did?

I structured the project using an object-oriented approach to separate the responsibilities of each component. This makes the code easier to understand, maintain, and extend.

* **APIClient** is responsible only for communicating with the YouTube Data API. It performs all HTTP requests and returns Python objects without modifying the data.
* **Pipeline** orchestrates the entire workflow. It coordinates the ingestion, transformation, and loading processes while keeping each step independent.
* **Transformer** handles data cleaning and reshaping. It converts the nested API responses into flat, analysis-ready tables and handles missing values where necessary.
* **DatabaseManager** is responsible for connecting to PostgreSQL, creating the database schema, and loading the transformed data into the appropriate tables.
* **QueryManager** executes analytical SQL queries against the database and saves the results for review.

Separating the application into these components follows the Single Responsibility Principle, making each class easier to test, debug, and modify without affecting the rest of the system.

---

## Q2 — What would break at scale?

The current implementation works well for approximately 50 videos, but several challenges would appear if the pipeline needed to process around 50,000 videos.

### 1. API Rate Limits

The YouTube Data API has quota limits. Fetching tens of thousands of videos and comments would require many API requests, which could quickly exhaust the daily quota.

To address this, I would implement request scheduling, retry logic with exponential backoff, and incremental data collection over multiple executions.

### 2. Sequential API Requests

The current implementation processes one video at a time. While this is simple and easy to understand, it would become slow for large datasets.

To improve performance, I would process requests concurrently using asynchronous programming or a thread pool while respecting the API rate limits.

### 3. Database Loading

Although `execute_batch()` is more efficient than inserting rows individually, loading very large datasets could still become a bottleneck.

For larger workloads, I would use PostgreSQL's bulk loading features such as the `COPY` command, batch processing, or dedicated ETL tools to improve insertion performance.

---

## Q3 — What would you improve with more time?

If I had an additional hour, I would improve the robustness of the pipeline by implementing automatic retry logic for failed API requests.

Currently, failed requests are logged and skipped so the pipeline can continue running. While this prevents the application from crashing, it may result in missing data if a temporary network issue occurs.

I would implement configurable retries with exponential backoff for transient failures such as timeouts or temporary server errors. This would increase the reliability of the ingestion process while still avoiding unnecessary repeated requests.

Additional improvements I would consider include adding unit tests, Docker support, and configuration files for easier deployment.
