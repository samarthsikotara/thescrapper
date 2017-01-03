import time
import csv
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
import re
import pdb

import sys
reload(sys)
sys.setdefaultencoding('utf8')



def init_driver():
	driver = webdriver.Chrome()
	driver.wait = WebDriverWait(driver, 100)
	driver.set_page_load_timeout(100)
	return driver


def check_exists_by_xpath(driver,xpath):
	try:
		driver.find_element_by_xpath(xpath)
	except NoSuchElementException:
		return False
	
	return True

def check_exists_by_css_selector(element,selector):
	try:
		select_element = element.find_element_by_css_selector('select.parentchild')
	except NoSuchElementException:
		return False
	return True


def check_class_and_style_is_valid(driver,xpath):
	class_of_element_to_check = driver.find_element_by_xpath(xpath).get_attribute('class')
	style_of_element_to_check = driver.find_element_by_xpath(xpath).get_attribute('style')

	if (style_of_element_to_check == "display: none;"):
		return True

	if (class_of_element_to_check == "" and style_of_element_to_check == ""):
		# print "true"
		return True
	else:
		return False


def scroll_to_bottom(driver,no_of_times):
	count = 1
	while (count < no_of_times):
		driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
		time.sleep(5)
		count = count + 1




def lookup(driver):

	# Opening a file
	f = open('bb-meat-part-2.csv', 'wt')
	writer = csv.writer(f)

	driver.get("http://www.bigbasket.com/cl/meat/?nc=nb")
	try:
		
		# button = driver.wait.until(EC.element_to_be_clickable((By.ID, "skip_explore")))

		# button.click()

		# Scrolling to bottom
		scroll_to_bottom(driver,15)
		
		#Defining variables
		scrolled = False
		div_id = 7
		li_id = 1
		parent_div_id = 0
		real_items = []
		new_page_div_id = 1

		div_xpath = '//*[@id="products-container"]/div/div[' + str(div_id) + ']'
		li_xpath = '//*[@id="products-container"]/div/div[' + str(div_id) + ']/ul/li[' + str(li_id) + ']'
		new_page_div_xpath = '//*[@id="products-container"]/div/div[' + str(div_id) + ']/div[' + str(new_page_div_id) + ']'
		new_page_div_li_xpath = '//*[@id="products-container"]/div/div[' + str(div_id) + ']/div[' + str(new_page_div_id) + ']/ul/li[' + str(li_id) + ']'
		while check_exists_by_xpath(driver,new_page_div_xpath):

			# Looping through rows
			while check_exists_by_xpath(driver,new_page_div_xpath):
				
				while check_exists_by_xpath(driver,new_page_div_li_xpath):
					# Lopping through columns
					if check_class_and_style_is_valid(driver,new_page_div_li_xpath):
						element = driver.find_element_by_xpath(new_page_div_li_xpath)
						content = driver.find_element_by_xpath(new_page_div_li_xpath).get_attribute('name')
						tag_id = driver.find_element_by_xpath(new_page_div_li_xpath).get_attribute('id')
						
						position = content.index('_')
						position = position + 1
						product_id = content[position:]
						real_items.append(product_id)
						
						driver.execute_script("document.getElementById('"+tag_id+"').style.display = 'block';")

						brand = element.find_element_by_css_selector('span.uiv2-brand-title').text
						product_url = element.find_elements_by_css_selector('span.uiv2-title-tool-tip')[1].find_element_by_tag_name('a').get_attribute('href')
							
						title = element.find_elements_by_css_selector('span.uiv2-title-tool-tip')[1].find_element_by_tag_name('a').text
						print title

						try:
							if (element.find_elements_by_css_selector('div.Rate_count_low') == []):
								mrp = "NA"
							else:
								mrp = element.find_elements_by_css_selector('div.Rate_count_low')[0].text
								#mrp = re.sub("[^0-9]", "", mrp)
								mrp = re.findall(r"[-+]?\d*\.\d+|\d+", mrp)[0]

						except ValueError:
							mrp = "NA"

						print mrp

							parent_string = element.find_element_by_css_selector('div.uiv2-field-wrap').text
				  		parent_string = re.sub(r'[^\x00-\x7F]+',' ', parent_string)
							# Taking size out
						try:
							space_position = parent_string.index(' ')
							size = parent_string[:space_position]
							print "Size is"
							print size
							space_position = space_position + 1
							parent_string = parent_string[space_position:]
						except ValueError:
							size = 1

						# Taking sizeunit out
						try:
							space_position = parent_string.index(' ')
							sizeunit = parent_string[:space_position]
							print "Sizeunit is"
							print sizeunit
							space_position = space_position + 1
							parent_string = parent_string[space_position:]
						except ValueError:
							#space_position = parent_string.index('')
							sizeunit = parent_string
							#pdb.set_trace()
							print "Sizeunit is"
							print sizeunit

						# Taking out the itemtype
						try:
							space_position = parent_string.index(' ')
							itemtype = parent_string[:space_position]
							space_position = space_position + 1
							parent_string = parent_string[space_position:]
						except ValueError:
							itemtype = ""
						
						print "Itemtype is"
						print itemtype
						
						# Taking out the quantity
						try:
							open_bracket_position = parent_string.index('(')
							close_bracket_position = parent_string.index(')')
							quantity = parent_string[open_bracket_position + 1:close_bracket_position]
							parent_string = parent_string[close_bracket_position + 1:]
						except ValueError:
							quantity = 1
						
						print "Quantity is"
						print quantity

						try:
							price = element.find_element_by_css_selector('div.uiv2-rate-count-avial').text.encode('utf-8')
							#price = re.sub("[^0-9]", "", price)
							price = re.findall(r"[-+]?\d*\.\d+|\d+", price)[0]
						except ValueError:
							price = ""

						print price

			  			writer.writerow( (product_id, product_url, brand, title, size, sizeunit, itemtype, quantity, price, mrp) )
									
					#Lopping through columns
					li_id = li_id + 1
					if scrolled == True:
						new_page_div_li_xpath = '//*[@id="products-container"]/div/div[' + str(div_id) + ']/div[' + str(new_page_div_id) + ']/ul/li[' + str(li_id) + ']'
						li_xpath = '//*[@id="products-container"]/div/div[' + str(div_id) + ']/ul/li[' + str(li_id) + ']'
					else:
						new_page_div_li_xpath = '//*[@id="products-container"]/div/div[' + str(div_id) + ']/div[' + str(new_page_div_id) + ']/ul/li[' + str(li_id) + ']'
						li_xpath = '//*[@id="products-container"]/div/div[' + str(div_id) + ']/ul/li[' + str(li_id) + ']'

					print "li to be searched"
					print new_page_div_li_xpath

				new_page_div_id = new_page_div_id + 1
				li_id = 1
				if scrolled == True:
					new_page_div_xpath = '//*[@id="products-container"]/div/div[' + str(div_id) + ']/div[' + str(new_page_div_id) + ']/ul/li[' + str(li_id) + ']'
					new_page_div_li_xpath = '//*[@id="products-container"]/div/div[' + str(div_id) + ']/div[' + str(new_page_div_id) + ']/ul/li[' + str(li_id) + ']'
				else:
					new_page_div_xpath = '//*[@id="products-container"]/div/div[' + str(div_id) + ']/div[' + str(new_page_div_id) + ']/ul/li[' + str(li_id) + ']'
					new_page_div_li_xpath = '//*[@id="products-container"]/div/div[' + str(div_id) + ']/div[' + str(new_page_div_id) + ']/ul/li[' + str(li_id) + ']'

				print "New next level div to be searched"
				print new_page_div_li_xpath
				#pdb.set_trace()
			# Turning a row
			div_id = div_id + 1
			li_id = 1
			new_page_div_id = 1
			
			# # Turning first page
			# if (div_id == 6) and (scrolled == False):
			# 	scrolled = True
			# 	parent_div_id = 7
			# 	div_id = 1

			# # Turning subsequent pages
			# if (div_id == 6) and (scrolled == True):
			# 	parent_div_id = parent_div_id + 1
			# 	div_id = 1

      
			if scrolled == True:
				div_xpath = '//*[@id="products-container"]/div/div[' + str(div_id) + ']'
				li_xpath = '//*[@id="products-container"]/div/div[' + str(div_id) + ']/ul/li[' + str(li_id) + ']'
				new_page_div_xpath = '//*[@id="products-container"]/div/div[' + str(div_id) + ']/div[' + str(new_page_div_id) + ']'
				new_page_div_li_xpath = '//*[@id="products-container"]/div/div[' + str(div_id) + ']/div[' + str(new_page_div_id) + ']/ul/li[' + str(li_id) + ']'
			else:
				div_xpath = '//*[@id="products-container"]/div/div[' + str(div_id) + ']'
				li_xpath = '//*[@id="products-container"]/div/div[' + str(div_id) + ']/ul/li[' + str(li_id) + ']'
				new_page_div_xpath = '//*[@id="products-container"]/div/div[' + str(div_id) + ']/div[' + str(new_page_div_id) + ']'
				new_page_div_li_xpath = '//*[@id="products-container"]/div/div[' + str(div_id) + ']/div[' + str(new_page_div_id) + ']/ul/li[' + str(li_id) + ']'

			print "div to be searched"
			print new_page_div_xpath



		print real_items
		f.close()
	
	except TimeoutException:
		print("Timeout")


if __name__ == "__main__":
	driver = init_driver()
	lookup(driver)
	time.sleep(5000)
	driver.quit()