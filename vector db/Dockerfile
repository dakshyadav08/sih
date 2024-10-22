# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Install necessary system dependencies
RUN apt-get update && \
    apt-get install -y libmagic1 libmagic-dev libgl1 libglib2.0-0 && \
    pip install python-magic

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install -r req.txt

# Expose the port Qdrant is running on (if needed for your application)
EXPOSE 6333

# Command to run the Python script
CMD ["python", "injest.py"]
