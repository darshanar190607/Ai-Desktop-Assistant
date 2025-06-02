import subprocess
import webbrowser
import time
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import json
import os

class WebAutomation:
    def __init__(self):
        self.driver = None
        self.wait = None
        
    def setup_driver(self):
        """Setup Chrome driver with options"""
        try:
            chrome_options = Options()
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-blink-features=AutomationControlled")
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            chrome_options.add_experimental_option('useAutomationExtension', False)
            
            # Use webdriver-manager to automatically download and manage ChromeDriver
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            self.wait = WebDriverWait(self.driver, 10)
            return True
        except Exception as e:
            print(f"Error setting up driver: {e}")
            return False
    
    def close_driver(self):
        """Close the browser driver"""
        if self.driver:
            self.driver.quit()
            self.driver = None
            self.wait = None
    
    def open_whatsapp_desktop(self):
        """Open WhatsApp desktop application"""
        try:
            # Try to open WhatsApp desktop app
            subprocess.Popen(["start", "whatsapp:"], shell=True)
            return True, "WhatsApp desktop app is opening..."
        except Exception as e:
            try:
                # Fallback to WhatsApp Web
                webbrowser.open("https://web.whatsapp.com/")
                return True, "WhatsApp Web is opening in your browser..."
            except Exception as e2:
                return False, f"Failed to open WhatsApp: {str(e2)}"
    
    def open_youtube(self):
        """Open YouTube"""
        try:
            webbrowser.open("https://youtube.com/")
            return True, "YouTube is now open. Enjoy!"
        except Exception as e:
            return False, f"Failed to open YouTube: {str(e)}"
    
    def open_instagram(self):
        """Open Instagram"""
        try:
            webbrowser.open("https://www.instagram.com/")
            return True, "Instagram is now open. Enjoy browsing!"
        except Exception as e:
            return False, f"Failed to open Instagram: {str(e)}"
    
    def fill_google_form(self, form_url, form_data):
        """Fill a Google Form with provided data"""
        try:
            if not self.setup_driver():
                return False, "Failed to setup browser driver"
            
            self.driver.get(form_url)
            time.sleep(3)
            
            filled_fields = 0
            
            # Try to find and fill text inputs
            text_inputs = self.driver.find_elements(By.CSS_SELECTOR, "input[type='text'], input[type='email'], textarea")
            
            for i, input_field in enumerate(text_inputs):
                try:
                    if i < len(form_data):
                        input_field.clear()
                        input_field.send_keys(form_data[i])
                        filled_fields += 1
                        time.sleep(0.5)
                except Exception as e:
                    print(f"Error filling field {i}: {e}")
                    continue
            
            # Try to find and fill specific Google Form elements
            form_elements = self.driver.find_elements(By.CSS_SELECTOR, "[data-params*='textInput'], [role='textbox']")
            
            for i, element in enumerate(form_elements):
                try:
                    if i < len(form_data) and filled_fields < len(form_data):
                        element.clear()
                        element.send_keys(form_data[filled_fields])
                        filled_fields += 1
                        time.sleep(0.5)
                except Exception as e:
                    print(f"Error filling Google Form field {i}: {e}")
                    continue
            
            if filled_fields > 0:
                return True, f"Successfully filled {filled_fields} fields in the Google Form. Please review and submit manually."
            else:
                return False, "No form fields were found or filled. Please check the form URL."
                
        except Exception as e:
            return False, f"Error filling Google Form: {str(e)}"
        finally:
            # Keep browser open for user to review and submit
            pass
    
    def search_and_add_to_cart(self, search_query, max_price=None):
        """Search for products on Google Shopping and add to cart"""
        try:
            if not self.setup_driver():
                return False, "Failed to setup browser driver"
            
            # Search on Google Shopping
            search_url = f"https://www.google.com/search?tbm=shop&q={search_query.replace(' ', '+')}"
            self.driver.get(search_url)
            time.sleep(3)
            
            # Find product links
            product_links = self.driver.find_elements(By.CSS_SELECTOR, "a[href*='/shopping/product']")
            
            if not product_links:
                return False, "No products found for your search query."
            
            # Filter by price if specified
            suitable_products = []
            
            for link in product_links[:10]:  # Check first 10 products
                try:
                    # Try to find price in the product element
                    price_element = link.find_element(By.CSS_SELECTOR, "[data-price], .price, .a-price-whole")
                    price_text = price_element.text
                    
                    # Extract numeric price
                    price_match = re.search(r'[\d,]+', price_text.replace('₹', '').replace('$', '').replace(',', ''))
                    if price_match:
                        price = int(price_match.group())
                        if max_price is None or price <= max_price:
                            suitable_products.append({
                                'link': link,
                                'price': price,
                                'text': link.text[:100]
                            })
                except:
                    # If price not found, add anyway
                    suitable_products.append({
                        'link': link,
                        'price': 0,
                        'text': link.text[:100]
                    })
            
            if not suitable_products:
                return False, f"No products found within the price range of ₹{max_price}" if max_price else "No suitable products found."
            
            # Click on the first suitable product
            best_product = suitable_products[0]
            best_product['link'].click()
            time.sleep(3)
            
            # Try to find and click "Add to Cart" or "Buy Now" button
            cart_buttons = [
                "Add to cart", "Add to Cart", "ADD TO CART",
                "Buy now", "Buy Now", "BUY NOW",
                "Add to bag", "Add to Bag"
            ]
            
            button_found = False
            for button_text in cart_buttons:
                try:
                    button = self.wait.until(
                        EC.element_to_be_clickable((By.XPATH, f"//button[contains(text(), '{button_text}')]"))
                    )
                    button.click()
                    button_found = True
                    break
                except:
                    continue
            
            if button_found:
                return True, f"Product added to cart! Price: ₹{best_product['price']}. Please complete the purchase manually."
            else:
                return True, f"Found product (₹{best_product['price']}) but couldn't add to cart automatically. Please add manually."
                
        except Exception as e:
            return False, f"Error during shopping: {str(e)}"
        finally:
            # Keep browser open for user to complete purchase
            pass

# Global instance
web_automation = WebAutomation()

def open_whatsapp():
    """Open WhatsApp desktop application"""
    return web_automation.open_whatsapp_desktop()

def open_youtube():
    """Open YouTube"""
    return web_automation.open_youtube()

def open_instagram():
    """Open Instagram"""
    return web_automation.open_instagram()

def fill_google_form(form_url, form_data):
    """Fill Google Form with provided data"""
    return web_automation.fill_google_form(form_url, form_data)

def google_shopping(search_query, max_price=None):
    """Search and add products to cart on Google Shopping"""
    return web_automation.search_and_add_to_cart(search_query, max_price)

def parse_form_data(user_input):
    """Parse form data from user input"""
    # Extract data in format: "fill form with name John, email john@email.com, phone 1234567890"
    data_pattern = r'fill\s+form\s+with\s+(.+)'
    match = re.search(data_pattern, user_input.lower())
    
    if match:
        data_string = match.group(1)
        # Split by comma and clean up
        data_parts = [part.strip() for part in data_string.split(',')]
        
        # Extract values (remove field names like "name", "email", etc.)
        form_data = []
        for part in data_parts:
            # Try to extract value after field name
            value_match = re.search(r'(?:name|email|phone|address|message|text)\s+(.+)', part)
            if value_match:
                form_data.append(value_match.group(1).strip())
            else:
                # If no field name found, use the whole part as value
                form_data.append(part.strip())
        
        return form_data
    
    return []

def parse_shopping_query(user_input):
    """Parse shopping query and price limit from user input"""
    # Extract search query and price limit
    # Example: "go to google and buy watch under 2000"
    
    # Extract price limit
    price_pattern = r'under\s+(\d+)'
    price_match = re.search(price_pattern, user_input.lower())
    max_price = int(price_match.group(1)) if price_match else None
    
    # Extract search query
    # Remove common phrases to get the product name
    query = user_input.lower()
    query = re.sub(r'go\s+to\s+google\s+and\s+buy\s+', '', query)
    query = re.sub(r'search\s+for\s+', '', query)
    query = re.sub(r'find\s+', '', query)
    query = re.sub(r'under\s+\d+', '', query)
    query = query.strip()
    
    return query, max_price