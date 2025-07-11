# Streamlit Number Counter Client

A beautiful Streamlit web application that provides a user-friendly interface for the Number Counter Flask API.

## Features

- 🎨 **Beautiful UI**: Clean, modern interface with popup-style messages
- 📊 **Visual Results**: Interactive metrics and charts displaying count results
- ⚙️ **Configurable**: Easy API URL configuration in sidebar
- 🏥 **Health Check**: Built-in API health monitoring
- 📋 **Input Validation**: Comprehensive input validation with helpful error messages
- 🔍 **Detailed View**: Expandable sections showing raw API responses
- 📱 **Responsive**: Works on desktop and mobile devices

## Installation

1. Install the required dependencies:
```bash
pip install -r requirements_streamlit.txt
```

2. Make sure your Flask API is running:
```bash
python app.py
```

3. Run the Streamlit application:
```bash
streamlit run streamlit_app.py
```

The application will open in your default web browser at `http://localhost:8501`.

## Usage

### Step 1: Configure API URL
- In the sidebar, enter your Flask API URL (default: `http://localhost:5000`)
- Click "Check API Health" to verify connection

### Step 2: Enter Numbers
- Enter comma-separated numbers in the text area
- Examples: `1, 2, -3, 0, 5` or `10, -5, 0, 3.14, -2.5`

### Step 3: Count Numbers
- Click "Count Numbers" button
- View results in the popup message window
- See detailed breakdown with metrics

### Step 4: View Results
- **Metrics Display**: See counts for positive, negative, zero, and total numbers
- **Detailed Breakdown**: Expandable section showing which numbers fall into each category
- **Raw API Response**: View the complete JSON response from the API

## Features Overview

### Main Interface
- **Input Area**: Large text area for entering comma-separated numbers
- **Action Buttons**: Count Numbers and Clear buttons
- **Results Display**: Beautiful metrics cards showing counts
- **Popup Messages**: Success, error, and info messages with distinctive styling

### Sidebar Features
- **API Configuration**: Set custom API URL
- **Health Check**: Test API connectivity
- **Instructions**: Built-in help and examples
- **Status Information**: Current API URL and timestamp

### Error Handling
The application handles various error scenarios:
- Invalid number formats
- API connection issues
- Empty input validation
- Timeout errors
- API response errors

### Popup Message Types
- ✅ **Success**: Green popup for successful operations
- ❌ **Error**: Red popup for errors and validation issues
- ℹ️ **Info**: Blue popup for informational messages

## Example Usage

1. **Basic Numbers**:
   ```
   Input: 1, 2, -3, 0, 5, -1, 0
   Result: 3 positive, 2 negative, 2 zeros
   ```

2. **Decimal Numbers**:
   ```
   Input: 3.14, -2.5, 0, 1.5, -0.5
   Result: 2 positive, 2 negative, 1 zero
   ```

3. **Large Numbers**:
   ```
   Input: 1000, -500, 0, 2500, -1000
   Result: 2 positive, 2 negative, 1 zero
   ```

## Screenshots

The application provides:
- Clean, modern interface
- Interactive metrics display
- Popup-style messages
- Detailed result breakdown
- API health monitoring
- Responsive design

## Troubleshooting

### Common Issues

1. **API Connection Error**:
   - Ensure Flask API is running
   - Check API URL in sidebar
   - Verify port number matches Flask configuration

2. **Invalid Number Format**:
   - Use only numbers separated by commas
   - Decimals are allowed
   - Remove any extra characters

3. **Timeout Error**:
   - Check network connection
   - Ensure API server is responsive

### API Requirements
- Flask API must be running on specified URL
- API should have `/count-numbers` endpoint
- API should return JSON responses

## Development

To extend the application:

1. **Add New Features**: Modify `streamlit_app.py`
2. **Update Styling**: Modify CSS in the markdown section
3. **Add New Endpoints**: Extend API calls in the `call_api` function
4. **Enhance UI**: Add new Streamlit components

## Dependencies

- `streamlit`: Web app framework
- `requests`: HTTP library for API calls
- `json`: JSON parsing (built-in)
- `datetime`: Timestamp functionality (built-in)

## License

This project is open source and available under the MIT License.