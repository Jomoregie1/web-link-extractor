# Web Link Extractor

A tool that extracts hyperlinks from the given URLs and outputs the results to the terminal.

## Description

This Dockerized application extracts hyperlinks from provided URLs. The program fetches the content of each URL, parses it, and then identifies and outputs all the hyperlinks contained within.

### Test File Included

A test file named `urls.txt` is provided in the `/data/` directory. You can use this file to test the application's functionality.

## Prerequisites

- Docker installed on your machine.

## Quick Start

1. **Pull the Docker Image from Docker Hub:**
   ```bash
   docker pull jomoregie1/web-extractor:v1

2. **Follow the on-screen prompts to provide the path to your file containing URLs.**
   ```bash
   docker run -it --rm jomoregie1/web-extractor:v1
   
3. Follow the on-screen prompts to provide the path to your file containing URLs.


## Running without Docker

If you don't have Docker installed or prefer running the application directly, follow these steps:

### Prerequisites

- Python 3.11 or newer installed on your machine.
- pip (Python package installer) installed.

### Installation & Execution

1. **Clone the GitHub repository to your machine:**
   ```bash
   git clone [https://github.com/Jomoregie1/web-link-extractor.git]
   cd web-link-extractor
2. **(Optional but recommended) Set up a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use: .\venv\Scripts\activate
3. **Install the required Python packages:**
    ```bash
   pip install -r requirements.txt
4. **Run the application:**
    ```bash
   python src/main.py
5. **When prompted, you can input /data/urls.txt to test with the included URLs.**

## Running Tests


### Running Tests 

1. **Navigate to the project directory:**
   ```bash
   cd web-link-extractor
2. **Run the tests using the unittest module:**
   ```bash
   python -m unittest discover tests
This will automatically discover and run all tests within the tests directory.

## Assumptions:

1. **URLs Schema:**
 Only http and https URLs are allowed. Other schemes like ftp or file are discarded.
2. **URL Validity:**
 A URL is considered valid if it has both a scheme and a netloc (domain).
3. **Retries:**
The producer will retry fetching a URL up to 3 times in the event of specific HTTP errors (500, 502, 503, 504).
4. **Timeout:**
There is a 10-second timeout for each URL fetch operation in the producer.
5. **Sentinel Value:**
A sentinel value (None) is used to signal the end of the production process.
6. **Queue Management:**
If the shared queue size exceeds the defined maximum, the oldest entry is removed to make space for a new one.
7. **Error Isolation:**
Both producer and consumer are designed to handle errors gracefully. An error with one URL doesn't stop the processing of others.

## Considerations:
1. **LRU Cache:**
The lru_cache for fetching HTML content has an unlimited size. This ensures that if the same URL appears multiple times, the producer won't fetch it again but may lead to excessive memory usage if the list of unique URLs is very large.
2. **Concurrency:**
The producer fetches URLs concurrently using a ThreadPoolExecutor.
The consumer, however, processes URLs sequentially. This is because parsing HTML content and extracting hyperlinks is typically a fast operation, so the bottleneck is more likely to be the fetching of URLs.
3. **Logging:**
Detailed logs are maintained for both the producer and consumer to monitor the processing status and any errors.
4. **Consumer Output:**
The consumer currently outputs the hyperlinks to the terminal. This can be redirected to a file if needed.
5. **Queue Timeout:**
The consumer waits for 10 seconds before assuming the queue is empty. This timeout can be adjusted based on specific use-cases.
6. **Error Reporting:**
Detailed error messages are logged, but they are not propagated up. This ensures that one bad URL does not halt the entire process.

## Testing:
### 1. Consumer Tests (`test_consumer.py`)

- **test_extract_hyperlinks**: Validates that hyperlinks are correctly extracted from given HTML content.
- **test_extract_hyperlinks_invalid_content**: Checks the behavior when provided with invalid HTML content.
- **test_write_to_terminal**: Ensures that the `write_to_terminal` function correctly invokes the built-in `print` function.
- **test_extract_hyperlinks_parsing_exception**: Asserts that parsing errors during hyperlink extraction are handled gracefully.
- **test_run_method**: Tests the core run method of the consumer, ensuring proper flow of operations.

### 2. Producer Tests (`test_producer.py`)

- **test_sanitize_url_valid_scheme**: Checks if the producer correctly sanitizes URLs with valid schemes.
- **test_sanitize_url_invalid_scheme**: Asserts the correct behavior for URLs with invalid schemes.
- **test_is_valid_url**: Tests various URL formats for validity.
- **test_prepare_urls**: Validates the initialisation process where invalid URLs are filtered out.
- **test_fetch_html_content_success**: Simulates a successful fetch operation for HTML content.
- **test_fetch_html_content_failure** & **test_fetch_html_content_exception**: Assures correct behavior during failed fetch operations.
- **test_run**: Confirms that the producer correctly pushes URLs and HTML content to the shared queue.

### 3. Logging Configuration Tests (`test_setup_logging.py`)

- **test_log_file_creation**: Verifies that the log file gets created and written to.
- **test_setup_logging**: Ensures that the logging setup correctly configures both file and console logging.
