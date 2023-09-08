# Use an official Python 3.11 image as the base image
FROM python:3.11

# Set environment variables
ENV PYTHONUNBUFFERED 1

# Set working directory
WORKDIR /src

# Copy the source code, tests directory, and requirements from your local machine to the container
COPY src/ /src/
COPY tests/ /tests/
COPY requirements.txt /src/
COPY data/ /data/

# Install the required Python packages
RUN pip install --no-cache-dir -r /src/requirements.txt

# Run your web link extractor script
CMD [ "python", "/src/main.py" ]