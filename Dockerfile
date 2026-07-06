FROM python:3.11

WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project
COPY . .

# Ensure Python can find the foundational_api package and the example scripts
ENV PYTHONPATH="/app"

# Run the tests
CMD ["python", "-m", "unittest", "discover", "-s", "tests"]