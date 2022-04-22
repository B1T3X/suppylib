from suppylib import logging as suppy_logging
from suppylib import messaging as suppy_messaging
from suppylib import navigation as suppy_navigation

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import json, time, types, base64

class SuppyBot:
    def __init__(self, config_path):
        self._current_conversation = None
        
        with open(config_path, "rb") as json_config_file:
            self._config_data = json.load(json_config_file)

        options = webdriver.ChromeOptions()
        for argument in self._config_data["chrome_arguments"]:
            options.add_argument(argument)
            print(f"Adding option {argument}")

        self._browser = webdriver.Chrome(options=options)
        self._browser.get("https://web.whatsapp.com")
        self.export_screenshot("status.jpg")
        self.wait_for_login()
        self._side_pane = self._browser.find_element(by=By.ID, value="side")
        self.update_submodules()

    def update_submodules(self):
        suppylib_submodules = [module_obj for name, module_obj in globals().items() if isinstance(module_obj, types.ModuleType) and module_obj.__name__.startswith("suppylib.")]
        for module in suppylib_submodules:
            module.side_pane = self._side_pane
            module.browser = self._browser
            module.config_data = self._config_data
 

    def wait_for_login(self):
        """
        Waits for WhatsApp to login
        """
        time.sleep(5)
        whatsapp_loaded = EC.presence_of_element_located((By.XPATH,'//div[text()="End-to-end encrypted"]'))
        while True:
            try:
                WebDriverWait(self._browser, 2).until(whatsapp_loaded)
            except TimeoutException:
                print("WhatsApp hasn't loaded yet")
                time.sleep(7)
            else:
                print("WhatsApp loaded successfully")
                time.sleep(15)
                break
        return

    def export_screenshot(self, filename):
        """
        Kind of obsolete, used for local testing, saves a screenshot of the QR code, handy if running in headless mode
        """
        with open(filename, 'wb') as image:
            image.write(base64.b64decode(self._browser.get_screenshot_as_base64()))
        return

    def send_message(self, message):
        suppy_messaging.sendMessage(message)
    
    def send_message_to(self, contact, message):
        suppy_messaging.sendMessageTo(contact, message)
    
    def check_for_new_messages(self):
        return suppy_messaging.checkForNewMessages()
    
    def move_to_conversation(self, conversation):
        suppy_navigation.openConversationWith(conversation)
        self.set_current_conversation()

    def set_current_conversation(self):
        try:
            self._current_conversation = suppy_navigation.getCurrentConversation()
        except NoSuchElementException:
            self._current_conversation = None
    
    def get_current_conversation(self):
        return self._current_conversation

    def read_new_messages(self, conversation=None, tail=None):
        return suppy_messaging.readNewMessages(conversation=conversation, tail=tail)

    def read_own_messages(self, conversation=None, tail=None, isgroup=False):
        return suppy_messaging.readMyMessages(conversation=conversation, tail=tail, isgroup=isgroup)

    def go_home(self):
        suppy_navigation.goHome()
    
    def shutdown(self):
        self._browser.close()
        print("Goodbye")
