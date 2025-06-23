FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
# Make sure the models directory exists
RUN mkdir -p models

# Generate data and train models during build
RUN python data/simulated_profiles.py
RUN python models/model_training.py

# Expose the port
EXPOSE 8000

# Run the FastAPI app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]