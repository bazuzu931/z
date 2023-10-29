from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from appium.webdriver.common.appiumby import AppiumBy
from appium.webdriver.common.touch_action import TouchAction
from time import sleep as s
from random import choice
from time import sleep
from random import uniform
import builtins, json

from .keycodes import *

from rich.console import Console
cp = Console().print

#----  ---------------------------------------------------------------------------------

# def print(*args, **kwargs):
# 	builtins.print(json.dumps(*args, **kwargs, indent=8))


#----  ---------------------------------------------------------------------------------

def kill_emulator():
	s(2)
	cp(' --- Starting Kill Emulator --- ')
	emulator_name = (subprocess.check_output(["adb devices"], shell=True)).decode('utf-8').split('\t')[0].split('\n')[-1].strip()
	# subprocess.Popen([f"adb -s {emulator_name} emu kill"], shell=True)
	os.system(f"adb -s {emulator_name} emu kill")
	cp(' --- Emulator killed Manually --- ')
	s(3)


def kill_appium(port):
	cp(' --- Starting Kill Appium Server (Wait 20 sec) --- ')
	s(7)
	try:
		# subprocess.Popen(["pkill -9 -f appium"], shell=True)
		os.system("pkill -9 -f appium")
	except NoSuchDriverError as e:
		pp('Нет такого процесса')
	s(2)
	# subprocess.Popen(["kill -9 $(ps aux | grep main.js | grep " + str(port) + "  | grep -v grep | awk '{print $2}')"], shell=True)
	# subprocess.Popen(["kill -9 $(ps aux | grep  python | grep ap_insta_faberlic | awk '{print $2}')"], shell=True)
	os.system("kill -9 $(ps aux | grep main.js | grep " + str(port) + " | grep -v grep | awk '{print $2}')")
	os.system("kill -9 $(ps aux | grep  python | grep ap_insta_faberlic | awk '{print $2}')")


#---- sleep in ms ---------------------------------------------------------------------------------

def su(start, end=0):
	start = start / 1000
	if end == 0:
		sleep(start)
	else:
		end = end / 1000
		sleep(uniform(start, end))

#----  ---------------------------------------------------------------------------------

def rc(min_digit, max_digit=0):
	if max_digit == 0:
		max_digit = min_digit
		min_digit = 0
	return choice(range(min_digit, max_digit))

#----  ---------------------------------------------------------------------------------

def pp(*args, **kwargs):
	cp('[yellow]---------------------------------------------------------------------------------------')
	print(*args, **kwargs)
	cp('[yellow]---------------------------------------------------------------------------------------')

def pe(*args, **kwargs):
	cp('[red]---------------------------------------------------------------------------------------')
	print(*args, **kwargs)
	cp('[red]---------------------------------------------------------------------------------------')

#----  ---------------------------------------------------------------------------------

def true_loop(ifunc):
	def ofunc(*args, **kwargs):
		counter_limit = 2
		counter = 0
		while True:
			try:
				ifunc(*args, **kwargs)
				break
			except Exception as e:
				pp('Error: ', e)
				print(f'Retry again: {ifunc}')
				counter += 1
				if counter >= counter_limit:
					break
				su(2000, 3000)
				continue
	return ofunc


#----  ---------------------------------------------------------------------------------

def tap(driver, element, count):
	actions = TouchAction(driver)
	actions.tap(element, count)
	actions.perform()

#----  ---------------------------------------------------------------------------------

# @true_loop
def print_speed(driver, text, delay=rc(500,1000)):
	try:
		for character in text.lower():
			if character in SYM_LIST:
				char_code = SYM_LIST[character]
			else:
				char_code = SYM_LIST[' ']
			pp(char_code)
			driver.press_keycode(char_code)
			su(delay)
	except Exception as e:
		pp('Error while printing in search field')
		pp(e)

#----  ---------------------------------------------------------------------------------

# @true_loop
def btn_click(driver, elem_xpath):
	btn = WebDriverWait(driver, 30).until(
		EC.presence_of_element_located((AppiumBy.XPATH, elem_xpath))
	)
	btn.click()
	pp(elem_xpath, ' clicked!')


#----  ---------------------------------------------------------------------------------

@true_loop
def get_element(driver, elem_xpath):
	return WebDriverWait(driver, 30).until(
		EC.presence_of_element_located((AppiumBy.XPATH, elem_xpath))
	)

#----  ---------------------------------------------------------------------------------

@true_loop
def send_text_to_field(driver, elem_xpath, text, selector_type='xpath'):
	if selector_type == 'xpath':
		selector_type = AppiumBy.XPATH
	elif selector_type == 'id':
		selector_type = AppiumBy.ID
	elif selector_type == 'class':
		selector_type = AppiumBy.CLASS_NAME
	else:
		pass
	field = WebDriverWait(driver, 30).until(
		EC.presence_of_element_located((selector_type, elem_xpath))
	)

	field.click()
	pp('field clicked')
	print_speed(driver, text)


#----  ---------------------------------------------------------------------------------

@true_loop
def press_enter(driver):
	# driver.press_keycode(66) # enter
	# driver.press_keycode(84) # search
	driver.execute_script("mobile: performEditorAction", {"action": "Go"}); # click search/enter button on keyboard
	pp('press Enter')

#---- Random Swipe Down  ---------------------------------------------------------------------------------
class Swipe:

	def __init__(self, driver, coord='down', resolution=(320,640)):
		self.driver = driver
		self.coord = coord
		self.resolution = resolution

	@staticmethod
	def get_random_params(resolution, percentage):
		horizontal_moving_percentage = hmv = 5
		vertical_moving_percentage = vmv = int(percentage) # На сколько процентов сдигать вниз

		init_start_x_percentage = isx = 55
		init_start_y_percentage = isy = 75

		init_end_x_percentage = iex = rc((init_start_x_percentage - hmv), (init_start_x_percentage + hmv))
		init_end_y_percentage = iey = init_start_y_percentage - vmv

		width = resolution[0]
		height = resolution[1]
		width_moving_offset_px = int(width * hmv / 100)
		height_moving_offset_px = int(height * vmv / 100)

		start_x1 = int(width * rc((isx - 5), (isx + 5)) / 100)
		start_x2 = start_x1 + rc(30, 60)
		start_x = rc(start_x1, start_x2)

		start_y1 = int(height * rc((isy - 7), (isy + 7)) / 100)
		start_y2 = start_y1 + rc(15, 30)
		start_y = rc(start_y1, start_y2)

		end_x1 = int(width * rc((isx - 5), (isx + 5)) / 100)
		end_x2 = end_x1 + rc(30, 60)
		end_x = rc(end_x1, end_x2)

		end_y1 = int(height * rc((iey - 7), (iey + 7)) / 100)
		end_y2 = end_y1 + rc(15, 30)
		end_y = rc(end_y1, end_y2)

		swipe_duration = rc(100, 1300)

		down_tuple = (start_x, start_y, end_x, end_y, swipe_duration)
		up_tuple = (end_x, end_y, start_x, start_y, swipe_duration)

		return {'down_tuple': down_tuple, 'up_tuple': up_tuple}
		# return {'start_x1': start_x, 'start_y': start_y, 'end_x': end_x, 'end_y': end_y, 'swipe_duration': swipe_duration}

	def moving_template(self, percentage=7):
		coord = self.coord
		pp(f'Random Swipe {coord.upper()} Start ...')
		#swipe(startX, startY, endX, endY, duration)
		# driver.swipe(rc(150, 200), rc(450, 500), rc(150, 200), rc(200, 250), rc(1000, 3000))
		# self.driver.swipe(self.start_x, self.start_y, self.end_x, self.end_y, self.swipe_duration)
		swipe_tuple = self.get_random_params(self.resolution, percentage)[f'{coord}_tuple']
		pp('Swipe params: ', *swipe_tuple)
		self.driver.swipe(*swipe_tuple)
		su(200, 1100)
		pp(f'Random Swipe {coord.upper()} End ...')


# swipe_down = Swipe(driver, 'down').moving_template
# swipe_up = Swipe(driver, 'up').moving_template



#----  ---------------------------------------------------------------------------------
def rate_say_no(driver):
	try:
		say_no_btn = WebDriverWait(driver, 3).until(EC.element_to_be_clickable((AppiumBy.ID, 'com.instagram.android:id/appirater_cancel_button')))
		# say_no_btn = driver.find_element(AppiumBy.ID, 'com.instagram.android:id/appirater_cancel_button')
		tap(driver, say_no_btn, 1)
		pp('press  No Thanks   ')
	except Exception as e:
		pass