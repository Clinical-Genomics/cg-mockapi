# Use the official Python image as the base image
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Copy the project files into the container
COPY . .

# Install uv
RUN pip install uv

# Sync dependencies using uv
RUN uv sync

# Expose the port FastAPI will run on
EXPOSE 8000

# Create a .env file with the LIMS_HOST value and run the application
CMD ["sh", "-c", "echo LIMS_HOST=${LIMS_HOST} > .env && uv run uvicorn mock_api.src.main:app --reload --host 0.0.0.0 --port 8000"]
