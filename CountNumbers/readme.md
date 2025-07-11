# Number Counter Flask API

A Flask API that counts positive, negative, and zero numbers in a list.

## Features

- Count positive, negative, and zero numbers from a comma-separated list
- RESTful API with GET method
- Configurable port through config.py
- Error handling and validation
- Health check endpoint
- API documentation endpoint

## Installation

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
python app.py
```

The API will start on `http://localhost:5000` by default.

## Configuration

The port and other settings can be configured in `config.py`:

- **PORT**: Default is 5000 (can be overridden with environment variable)
- **DEBUG**: Default is False (can be overridden with environment variable)

### Environment Variables

- `PORT`: Set the port number (default: 5000)
- `DEBUG`: Set to 'true' to enable debug mode (default: False)

## API Endpoints

### 1. Count Numbers
- **URL**: `/count-numbers`
- **Method**: GET
- **Parameters**: 
  - `numbers`: Comma-separated list of numbers
- **Example**: 
  ```
  GET /count-numbers?numbers=1,2,-3,0,5,-1,0
  ```
- **Response**:
  ```json
  {
    "input_numbers": [1, 2, -3, 0, 5, -1, 0],
    "counts": {
      "positive": 3,
      "negative": 2,
      "zero": 2,
      "total": 7
    },
    "status": "success"
  }
  ```

### 2. Health Check
- **URL**: `/health`
- **Method**: GET
- **Response**:
  ```json
  {
    "status": "healthy",
    "message": "Number counting API is running"
  }
  ```

### 3. API Documentation
- **URL**: `/`
- **Method**: GET
- **Description**: Returns API documentation

## Usage Examples

### Using curl:
```bash
# Count numbers
curl "http://localhost:5000/count-numbers?numbers=1,2,-3,0,5,-1,0"

# Health check
curl "http://localhost:5000/health"

# API documentation
curl "http://localhost:5000/"
```

### Using Python requests:
```python
import requests

# Count numbers
response = requests.get('http://localhost:5000/count-numbers', 
                       params={'numbers': '1,2,-3,0,5,-1,0'})
print(response.json())
```

## Error Handling

The API handles various error cases:

- Missing numbers parameter
- Invalid number format
- Internal server errors

All errors return appropriate HTTP status codes and error messages.

## Running in Different Environments

### Development:
```bash
export DEBUG=true
python app.py
```

### Production:
```bash
export PORT=8080
export DEBUG=false
python app.py
```

### Using environment variables:
```bash
export PORT=3000
export DEBUG=true
python app.py
```