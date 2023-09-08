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
   cd [web-link-extractor]
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
   cd [web-link-extractor]
2. **Run the tests using the unittest module:**
   ```bash
   python -m unittest discover tests
This will automatically discover and run all tests within the tests directory.

