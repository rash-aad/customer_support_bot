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

# Tell Docker that the container listens on port 5002
EXPOSE 5002

# The command to run your application when the container starts
CMD ["gunicorn", "--bind", "0.0.0.0:5005", "app:app"]
