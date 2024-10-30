# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . .

# Install any needed packages specified in requirements.txt
RUN pip install Flask

# Expose the port your app runs on
EXPOSE 5002

# Run the app.py when the container launches
CMD ["python", "app.py"]
