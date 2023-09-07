# Use an official Python 3.11 image as the base image
FROM python:3.11

# Set the working directory in the container to /
WORKDIR /

# Copy the source code from your local machine to the container
COPY src/ /src/

# Copy the tests directory from your local machine to the container
COPY tests/ /tests/

# Copy the requirements.txt file from your local machine to the container
COPY requirements.txt /

# Install the required Python packages
RUN pip install --no-cache-dir -r /requirements.txt

# Run your web link extractor script
CMD [ "python", "/src/main.py" ]
