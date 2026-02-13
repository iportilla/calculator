# Use a slim Python image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the server script
COPY mcp_calculator.py .

# Expose port 8000 for SSE
EXPOSE 8000

# Set the entry point to run as SSE by default for cloud usage
CMD ["python", "mcp_calculator.py", "sse"]
