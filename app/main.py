from env import *
from appium.options.android import UiAutomator2Options


# print('start MAIN')
# s(12)
# print('continue MAIN')

desired_caps = {
	"platformName": "Android",
	"appium:automationName": "UIAutomator2",
	"appium:deviceName": "android33",
	"appium:packageName": "com.chrome.android",
	"appium:appActivity": "com.chrome.mainactivity.MainActivity",
	"noReset": "true"
}

capabilities_options = UiAutomator2Options().load_capabilities(desired_caps)

APPIUM_HOST = '127.0.0.1'
APPIUM_PORT = 4723

driver = webdriver.Remote(f"{APPIUM_HOST}:{APPIUM_PORT}", options=capabilities_options)

swipe_down = Swipe(driver, 'down').moving_template
swipe_up = Swipe(driver, 'up').moving_template

pp(driver.contexts)
driver.switch_to.context('NATIVE_APP')
pp('Window size: ')
driver.get_window_size()

print('Fuck Yourself')

s(100)


#---- Open App ---------------------------------------------------------------------------------

# while True:
# 	try:
# 		btn_click(driver, '//android.widget.TextView[@content-desc="Instagram"]')
# 		break
# 	except Exception as e:
# 		try:
# 			find_element(AppiumBy.ID, 'Instagram').click()
# 			break
# 		except Exception as e:
# 			try:
# 				driver.start_activity('com.instagram.android', 'com.instagram.mainactivity.MainActivity')
# 				break
# 			except Exception as e:
# 				pp('Cannot run Instagram')
# 				s(5)
# 				continue