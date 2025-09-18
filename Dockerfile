# Using local base image
FROM 172.23.12.160:8083/autocm-base-image:1.0.2

# Set working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY . .

# Expose port
EXPOSE 8000

# Run FastAPI app with Uvicorn from Merge_api.py
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]