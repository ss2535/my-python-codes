!pip install selenium 
 
 
from selenium import webdriver 
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC 
 
# تنظیمات Chrome برای Colab 
options = webdriver.ChromeOptions() 
options.add_argument('--headless')  # اجرای مرورگر در پس‌زمینه 
options.add_argument('--no-sandbox') 
options.add_argument('--disable-dev-shm-usage') 
 
# ایجاد یک instance از مرورگر Chrome 
driver = webdriver.Chrome(options=options) 
 
def check_text_similarity(text1, text2): 
    try: 
        # باز کردن سایت 
        driver.get("https://searchnatural.co.uk/text-similarity-checker/") 
 
        # منتظر ماندن برای بارگذاری صفحه 
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "string1"))) 
 
        # پیدا کردن فیلدهای ورودی متن با استفاده از ID 
        input1 = driver.find_element(By.ID, "string1") 
        input2 = driver.find_element(By.ID, "string2") 
 
        # وارد کردن متن‌ها 
        input1.send_keys(text1) 
        input2.send_keys(text2) 
 
        # کلیک روی دکمه Calculate Similarity 
        calculate_button = driver.find_element(By.ID, "calculateBtn") 
        calculate_button.click() 
 
        # منتظر ماندن برای بارگذاری نتیجه 
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "similarity"))) 
 
        # پیدا کردن نتیجه 
        result = driver.find_element(By.ID, "similarity") 
        return result.text.strip() 
    except Exception as e: 
        return f"خطا: {str(e)}" 
 
# دریافت دو رشته از کاربر 
text1 = input("متن اول را وارد کنید: ") 
text2 = input("متن دوم را وارد کنید: ") 
 
# بررسی تشابه و نمایش نتیجه 
similarity_result = check_text_similarity(text1, text2) 
print("نتیجه تشابه متن:", similarity_result) 
 
# بستن مرورگر 
driver.quit()