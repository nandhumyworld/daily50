import streamlit as st
import requests
import json
from datetime import datetime

# Configure the page
st.set_page_config(
    page_title="Number Counter API Client",
    page_icon="🔢",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for popup-style messages
st.markdown("""
<style>
    .popup-success {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .popup-error {
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        color: #721c24;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .popup-info {
        background-color: #d1ecf1;
        border: 1px solid #bee5eb;
        color: #0c5460;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .results-container {
        background-color: #f8f9fa;
        padding: 1.5rem;
        border-radius: 0.5rem;
        border-left: 4px solid #007bff;
        margin: 1rem 0;
    }
    
    .metric-card {
        background-color: white;
        padding: 1rem;
        border-radius: 0.5rem;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        text-align: center;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

def validate_numbers(numbers_str):
    """Validate the input string and return list of numbers"""
    if not numbers_str.strip():
        return None, "Please enter some numbers"
    
    try:
        # Remove extra spaces and split by comma
        numbers = [float(num.strip()) for num in numbers_str.split(',') if num.strip()]
        if not numbers:
            return None, "No valid numbers found"
        return numbers, None
    except ValueError:
        return None, "Invalid number format. Please use only numbers separated by commas."

def call_api(numbers_str, api_url):
    """Call the Flask API and return the response"""
    try:
        response = requests.get(
            f"{api_url}/count-numbers",
            params={'numbers': numbers_str},
            timeout=10
        )
        
        if response.status_code == 200:
            return response.json(), None
        else:
            error_data = response.json() if response.headers.get('content-type') == 'application/json' else {}
            return None, f"API Error ({response.status_code}): {error_data.get('message', 'Unknown error')}"
            
    except requests.exceptions.ConnectionError:
        return None, "Connection Error: Cannot connect to the API. Make sure the Flask server is running."
    except requests.exceptions.Timeout:
        return None, "Timeout Error: The API request timed out."
    except requests.exceptions.RequestException as e:
        return None, f"Request Error: {str(e)}"
    except json.JSONDecodeError:
        return None, "Invalid JSON response from API"

def show_popup_message(message, message_type="info"):
    """Display a popup-style message"""
    css_class = f"popup-{message_type}"
    st.markdown(f'<div class="{css_class}">{message}</div>', unsafe_allow_html=True)

def display_results(data):
    """Display the API results in a formatted way"""
    if not data:
        return
    
    st.markdown("## 📊 Results")
    
    # Extract data
    input_numbers = data.get('input_numbers', [])
    counts = data.get('counts', {})
    
    # Display input numbers
    st.markdown("### Input Numbers:")
    st.write(f"**{', '.join(map(str, input_numbers))}**")
    
    # Display counts in columns
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="🟢 Positive Numbers",
            value=counts.get('positive', 0)
        )
    
    with col2:
        st.metric(
            label="🔴 Negative Numbers",
            value=counts.get('negative', 0)
        )
    
    with col3:
        st.metric(
            label="⚫ Zero Numbers",
            value=counts.get('zero', 0)
        )
    
    with col4:
        st.metric(
            label="📈 Total Numbers",
            value=counts.get('total', 0)
        )
    
    # Show detailed breakdown
    with st.expander("📋 Detailed Breakdown"):
        positive_nums = [num for num in input_numbers if num > 0]
        negative_nums = [num for num in input_numbers if num < 0]
        zero_nums = [num for num in input_numbers if num == 0]
        
        if positive_nums:
            st.write(f"**Positive numbers:** {', '.join(map(str, positive_nums))}")
        if negative_nums:
            st.write(f"**Negative numbers:** {', '.join(map(str, negative_nums))}")
        if zero_nums:
            st.write(f"**Zero numbers:** {', '.join(map(str, zero_nums))}")

def main():
    # Header
    st.title("🔢 Number Counter API Client")
    st.markdown("Enter comma-separated numbers to count positive, negative, and zero values using the Flask API.")
    
    # Sidebar for configuration
    with st.sidebar:
        st.header("⚙️ Configuration")
        api_url = st.text_input(
            "API URL",
            value="http://localhost:5000",
            help="Enter the Flask API URL"
        )
        
        # API Health Check
        if st.button("🏥 Check API Health"):
            try:
                response = requests.get(f"{api_url}/health", timeout=5)
                if response.status_code == 200:
                    st.success("✅ API is healthy!")
                else:
                    st.error("❌ API is not responding properly")
            except:
                st.error("❌ Cannot connect to API")
        
        st.markdown("---")
        st.markdown("### 📖 Instructions")
        st.markdown("""
        1. Enter numbers separated by commas
        2. Click 'Count Numbers' button
        3. View results in popup window
        
        **Examples:**
        - `1, 2, -3, 0, 5`
        - `10, -5, 0, 3.14, -2.5`
        - `100, -200, 0, 0, 50`
        """)
    
    # Main content area
    st.markdown("## 📝 Input Numbers")
    
    # Input form
    with st.form("number_form"):
        numbers_input = st.text_area(
            "Enter numbers (comma-separated):",
            placeholder="Example: 1, 2, -3, 0, 5, -1, 0",
            height=100,
            help="Enter numbers separated by commas. Decimals are allowed."
        )
        
        col1, col2, col3 = st.columns([1, 1, 4])
        
        with col1:
            submit_button = st.form_submit_button("🚀 Count Numbers", use_container_width=True)
        
        with col2:
            clear_button = st.form_submit_button("🗑️ Clear", use_container_width=True)
    
    # Handle form submission
    if submit_button and numbers_input:
        # Validate input
        numbers_list, validation_error = validate_numbers(numbers_input)
        
        if validation_error:
            show_popup_message(f"❌ {validation_error}", "error")
        else:
            # Show processing message
            with st.spinner("Processing your request..."):
                # Call API
                api_response, api_error = call_api(numbers_input, api_url)
                
                if api_error:
                    show_popup_message(f"❌ {api_error}", "error")
                else:
                    # Success popup
                    show_popup_message("✅ Numbers counted successfully!", "success")
                    
                    # Display results
                    display_results(api_response)
                    
                    # Show raw JSON response in expandable section
                    with st.expander("🔍 Raw API Response"):
                        st.json(api_response)
    
    elif submit_button:
        show_popup_message("❌ Please enter some numbers first!", "error")
    
    elif clear_button:
        st.rerun()
    
    # Footer
    st.markdown("---")
    st.markdown("### 🔗 API Endpoints")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📋 View API Documentation"):
            try:
                response = requests.get(f"{api_url}/")
                if response.status_code == 200:
                    st.json(response.json())
                else:
                    st.error("Cannot fetch API documentation")
            except:
                st.error("Cannot connect to API")
    
    with col2:
        st.markdown(f"**API Base URL:** `{api_url}`")
        st.markdown(f"**Last Updated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    main()