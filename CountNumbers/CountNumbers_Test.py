import asyncio
import time
from playwright.async_api import async_playwright, Page, Browser
import pytest
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class StreamlitTester:
    def __init__(self, streamlit_url: str = "http://localhost:8501"):
        self.streamlit_url = streamlit_url
        self.browser = None
        self.page = None
    
    async def setup_browser(self, headless: bool = False):
        """Setup browser and page"""
        playwright = await async_playwright().start()
        self.browser = await playwright.chromium.launch(
            headless=headless,
            args=['--no-sandbox', '--disable-dev-shm-usage']
        )
        self.page = await self.browser.new_page()
        
        # Set viewport size
        await self.page.set_viewport_size({"width": 1280, "height": 720})
        
        logger.info(f"Browser setup complete. Headless: {headless}")
    
    async def navigate_to_app(self):
        """Navigate to Streamlit application"""
        try:
            await self.page.goto(self.streamlit_url, wait_until="networkidle")
            logger.info(f"Navigated to {self.streamlit_url}")
            
            # Wait for the app to fully load
            await self.page.wait_for_selector("h1", timeout=10000)
            logger.info("Streamlit app loaded successfully")
            
        except Exception as e:
            logger.error(f"Failed to navigate to app: {e}")
            raise
    
    async def wait_for_streamlit_ready(self):
        """Wait for Streamlit to be fully ready"""
        try:
            # Wait for the main title to appear
            await self.page.wait_for_selector("h1:has-text('Number Counter API Client')", timeout=15000)
            
            # Wait for the form to be ready
            await self.page.wait_for_selector("textarea", timeout=10000)
            
            # Wait for the submit button to be ready
            await self.page.wait_for_selector("button:has-text('Count Numbers')", timeout=10000)
            
            logger.info("Streamlit application is ready for testing")
            
        except Exception as e:
            logger.error(f"Streamlit app not ready: {e}")
            raise
    
    async def enter_numbers(self, numbers: str):
        """Enter numbers into the textarea"""
        try:
            # Find the textarea for number input
           # textarea = self.page.locator("textarea").first
            textarea = self.page.locator('xpath=//*[@id="text_area_2"]')
            
            # Clear existing content and enter new numbers
            await textarea.clear()
            await textarea.fill(numbers)
            
            logger.info(f"Entered numbers: {numbers}")
            
            # Wait a moment for the input to be processed
            await self.page.wait_for_timeout(500)
            
        except Exception as e:
            logger.error(f"Failed to enter numbers: {e}")
            raise
    
    async def click_count_numbers_button(self):
        """Click the 'Count Numbers' button"""
        try:
            # Find and click the Count Numbers button
            button = self.page.locator("button:has-text('Count Numbers')")
            await button.click()
            
            logger.info("Clicked 'Count Numbers' button")
            
            # Wait for the processing to complete
            await self.page.wait_for_timeout(2000)
            
        except Exception as e:
            logger.error(f"Failed to click Count Numbers button: {e}")
            raise
    
    async def wait_for_results(self):
        """Wait for results to appear"""
        try:
            # Wait for either success or error message
            await self.page.wait_for_selector(
                ".popup-success, .popup-error", 
                timeout=15000
            )
            
            logger.info("Results appeared")
            
        except Exception as e:
            logger.error(f"Results did not appear: {e}")
            raise
    
    async def capture_results(self):
        """Capture and return the test results"""
        results = {
            "success": False,
            "message": "",
            "metrics": {},
            "error": None
        }
        
        try:
            # Check for success message
            success_popup = self.page.locator(".popup-success")
            if await success_popup.count() > 0:
                results["success"] = True
                results["message"] = await success_popup.text_content()
                logger.info("Success message found")
                
                # Capture metrics if available
                metrics = await self.capture_metrics()
                results["metrics"] = metrics
                
            # Check for error message
            error_popup = self.page.locator(".popup-error")
            if await error_popup.count() > 0:
                results["success"] = False
                results["error"] = await error_popup.text_content()
                logger.info("Error message found")
            
        except Exception as e:
            results["error"] = str(e)
            logger.error(f"Failed to capture results: {e}")
        
        return results
    
    async def capture_metrics(self):
        """Capture the metrics from the results"""
        metrics = {}
        
        try:
            # Wait for metrics to load
            await self.page.wait_for_selector("[data-testid='metric-container']", timeout=5000)
            
            # Capture all metrics
            metric_containers = self.page.locator("[data-testid='metric-container']")
            count = await metric_containers.count()
            
            for i in range(count):
                metric = metric_containers.nth(i)
                label = await metric.locator("[data-testid='metric-container'] > div > div").first.text_content()
                value = await metric.locator("[data-testid='metric-container'] > div > div").nth(1).text_content()
                
                if label and value:
                    metrics[label.strip()] = value.strip()
            
            logger.info(f"Captured metrics: {metrics}")
            
        except Exception as e:
            logger.warning(f"Could not capture metrics: {e}")
        
        return metrics
    
    async def take_screenshot(self, filename: str = "test_screenshot.png"):
        """Take a screenshot of the current page"""
        try:
            await self.page.screenshot(path=filename, full_page=True)
            logger.info(f"Screenshot saved: {filename}")
        except Exception as e:
            logger.error(f"Failed to take screenshot: {e}")
    
    async def cleanup(self):
        """Clean up browser resources"""
        if self.browser:
            await self.browser.close()
            logger.info("Browser closed")

async def test_streamlit_app_basic():
    """Basic test for the Streamlit application"""
    tester = StreamlitTester()
    
    try:
        # Setup browser (set headless=False to see the browser)
        await tester.setup_browser(headless=False)
        
        # Navigate to the app
        await tester.navigate_to_app()
        
        # Wait for app to be ready
        await tester.wait_for_streamlit_ready()
        
        # Test with basic numbers
        test_numbers = "1, 2, -3, 0, 5, -1, 0"
        await tester.enter_numbers(test_numbers)
        
        # Click the count numbers button
        await tester.click_count_numbers_button()
        
        # Wait for and capture results
        await tester.wait_for_results()
        results = await tester.capture_results()
        
        # Take screenshot
        await tester.take_screenshot("test_basic_success.png")
        
        # Validate results
        assert results["success"], f"Test failed: {results.get('error', 'Unknown error')}"
        logger.info("✅ Basic test passed successfully!")
        
        return results
        
    except Exception as e:
        logger.error(f"❌ Basic test failed: {e}")
        await tester.take_screenshot("test_basic_failure.png")
        raise
    finally:
        await tester.cleanup()

async def test_streamlit_app_multiple_scenarios():
    """Test multiple scenarios"""
    tester = StreamlitTester()
    test_results = []
    
    test_cases = [
        {"name": "Basic Mixed Numbers", "input": "1, 2, -3, 0, 5, -1, 0", "expected_success": True},
        {"name": "Only Positive Numbers", "input": "1, 2, 3, 4, 5", "expected_success": True},
        {"name": "Only Negative Numbers", "input": "-1, -2, -3, -4, -5", "expected_success": True},
        {"name": "Only Zeros", "input": "0, 0, 0, 0", "expected_success": True},
        {"name": "Decimal Numbers", "input": "3.14, -2.5, 0, 1.5, -0.5", "expected_success": True},
        {"name": "Invalid Input", "input": "a, b, c", "expected_success": False},
        {"name": "Empty Input", "input": "", "expected_success": False},
    ]
    
    try:
        await tester.setup_browser(headless=True)
        await tester.navigate_to_app()
        await tester.wait_for_streamlit_ready()
        
        for i, test_case in enumerate(test_cases):
            logger.info(f"Running test case {i+1}: {test_case['name']}")
            
            try:
                # Enter numbers
                await tester.enter_numbers(test_case["input"])
                
                # Click button
                await tester.click_count_numbers_button()
                
                # Wait for results
                await tester.wait_for_results()
                
                # Capture results
                results = await tester.capture_results()
                
                # Take screenshot
                await tester.take_screenshot(f"test_case_{i+1}_{test_case['name'].replace(' ', '_')}.png")
                
                # Validate results
                test_result = {
                    "test_case": test_case["name"],
                    "input": test_case["input"],
                    "expected_success": test_case["expected_success"],
                    "actual_success": results["success"],
                    "passed": results["success"] == test_case["expected_success"],
                    "message": results.get("message", ""),
                    "error": results.get("error", ""),
                    "metrics": results.get("metrics", {})
                }
                
                test_results.append(test_result)
                
                if test_result["passed"]:
                    logger.info(f"✅ Test case '{test_case['name']}' passed")
                else:
                    logger.error(f"❌ Test case '{test_case['name']}' failed")
                
                # Wait before next test
                await tester.page.wait_for_timeout(1000)
                
            except Exception as e:
                logger.error(f"❌ Test case '{test_case['name']}' failed with exception: {e}")
                test_results.append({
                    "test_case": test_case["name"],
                    "input": test_case["input"],
                    "expected_success": test_case["expected_success"],
                    "actual_success": False,
                    "passed": False,
                    "error": str(e),
                    "exception": True
                })
        
        return test_results
        
    finally:
        await tester.cleanup()

async def run_performance_test():
    """Run performance test"""
    tester = StreamlitTester()
    
    try:
        await tester.setup_browser(headless=True)
        
        # Measure page load time
        start_time = time.time()
        await tester.navigate_to_app()
        await tester.wait_for_streamlit_ready()
        load_time = time.time() - start_time
        
        # Measure form interaction time
        start_time = time.time()
        await tester.enter_numbers("1, 2, -3, 0, 5")
        await tester.click_count_numbers_button()
        await tester.wait_for_results()
        interaction_time = time.time() - start_time
        
        performance_results = {
            "page_load_time": load_time,
            "form_interaction_time": interaction_time,
            "total_time": load_time + interaction_time
        }
        
        logger.info(f"Performance Results: {performance_results}")
        return performance_results
        
    finally:
        await tester.cleanup()

async def main():
    """Main test runner"""
    logger.info("🚀 Starting Playwright tests for Streamlit application")
    
    try:
        # Run basic test
        logger.info("📋 Running basic test...")
        basic_results = await test_streamlit_app_basic()
        
        # Run multiple scenarios
      #  logger.info("📋 Running multiple test scenarios...")
      #  scenario_results = await test_streamlit_app_multiple_scenarios()
        
        # Run performance test
        logger.info("📋 Running performance test...")
        performance_results = await run_performance_test()
        
        # Print summary
        logger.info("\n" + "="*50)
        logger.info("📊 TEST SUMMARY")
        logger.info("="*50)
        
        logger.info(f"✅ Basic test: {'PASSED' if basic_results['success'] else 'FAILED'}")
        
        passed_scenarios = sum(1 for result in scenario_results if result["passed"])
        total_scenarios = len(scenario_results)
        logger.info(f"✅ Scenario tests: {passed_scenarios}/{total_scenarios} PASSED")
        
        logger.info(f"⏱️ Performance:")
        logger.info(f"   - Page load time: {performance_results['page_load_time']:.2f}s")
        logger.info(f"   - Form interaction time: {performance_results['form_interaction_time']:.2f}s")
        logger.info(f"   - Total time: {performance_results['total_time']:.2f}s")
        
        # Detailed scenario results
        logger.info("\n📝 Detailed Results:")
        for result in scenario_results:
            status = "✅ PASSED" if result["passed"] else "❌ FAILED"
            logger.info(f"   {status}: {result['test_case']}")
            if result.get("error"):
                logger.info(f"     Error: {result['error']}")
        
        logger.info("\n🎉 All tests completed!")
        
    except Exception as e:
        logger.error(f"❌ Test execution failed: {e}")
        raise

if __name__ == "__main__":
    # Run the tests
    asyncio.run(main())