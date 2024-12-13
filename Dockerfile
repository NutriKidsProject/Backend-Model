# Base image Python 3.9 slim
FROM python:3.9-slim

# Copy credential file
COPY nutrikids-key.json /app/nutrikids-key.json

# Set working directory
WORKDIR /app

# Install wget
RUN apt-get update && apt-get install -y wget && rm -rf /var/lib/apt/lists/*

# Copy dependencies list
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy main app
COPY app.py .

# Download model file
RUN wget -nc https://storage.googleapis.com/bucket-nutri/models/model_nutrition_stat.h5 -O /app/model_nutrition_stat.h5 || true

# Download food data
RUN wget -nc https://storage.googleapis.com/bucket-nutri/models/food-data.csv -O /app/food-data.csv || true

# Download label file
RUN wget -nc https://storage.googleapis.com/bucket-nutri/models/labels.json -O /app/labels.json || true

# Expose port
EXPOSE 8080

# Run the app
CMD ["python", "app.py"]
