from flask import Flask, request, jsonify
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

def count_numbers(numbers):
    """
    Count positive, negative, and zero numbers in a list.
    
    Args:
        numbers (list): List of numbers
        
    Returns:
        dict: Dictionary with counts of positive, negative, and zero numbers
    """
    positive_count = 0
    negative_count = 0
    zero_count = 0
    
    for num in numbers:
        if num > 0:
            positive_count += 1
        elif num < 0:
            negative_count += 1
        else:
            zero_count += 1
    
    return {
        'positive': positive_count,
        'negative': negative_count,
        'zero': zero_count,
        'total': len(numbers)
    }

@app.route('/count-numbers', methods=['GET'])
def count_numbers_api():
    """
    API endpoint to count positive, negative, and zero numbers.
    
    Query Parameters:
        numbers: Comma-separated list of numbers
        
    Example:
        GET /count-numbers?numbers=1,2,-3,0,5,-1,0
        
    Returns:
        JSON response with counts
    """
    try:
        # Get numbers from query parameters
        numbers_param = request.args.get('numbers', '')
        
        if not numbers_param:
            return jsonify({
                'error': 'Missing numbers parameter',
                'message': 'Please provide numbers as comma-separated values in the query parameter'
            }), 400
        
        # Parse numbers from string
        try:
            numbers = [float(num.strip()) for num in numbers_param.split(',')]
        except ValueError:
            return jsonify({
                'error': 'Invalid number format',
                'message': 'Please ensure all values are valid numbers'
            }), 400
        
        # Count the numbers
        result = count_numbers(numbers)
        
        return jsonify({
            'input_numbers': numbers,
            'counts': result,
            'status': 'success'
        })
        
    except Exception as e:
        return jsonify({
            'error': 'Internal server error',
            'message': str(e)
        }), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'message': 'Number counting API is running'
    })

@app.route('/', methods=['GET'])
def home():
    """Home endpoint with API documentation"""
    return jsonify({
        'message': 'Number Counting API',
        'endpoints': {
            'count-numbers': {
                'method': 'GET',
                'description': 'Count positive, negative, and zero numbers',
                'parameters': {
                    'numbers': 'Comma-separated list of numbers'
                },
                'example': '/count-numbers?numbers=1,2,-3,0,5,-1,0'
            },
            'health': {
                'method': 'GET',
                'description': 'Health check endpoint'
            }
        }
    })

if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=app.config['PORT'],
        debug=app.config['DEBUG']
    )