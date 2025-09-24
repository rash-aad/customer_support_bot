# Use an official lightweight Python image as a parent image
FROM python:3.11-slim

# Set the working directory in the container to /app
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt .

# Install the dependencies. This uses the CPU-only version of PyTorch to save space.
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application's code from your host to your container at /app
COPY . .


# The command to run your application when the container starts
# Expose the port Render will provide
EXPOSE 10000

# The command to run your application when the container starts
# This uses the PORT variable provided by Render's environment
CMD ["gunicorn", "--bind", "0.0.0.0:5002", "app:app"]
