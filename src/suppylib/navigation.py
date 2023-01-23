from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException, ElementClickInterceptedException
from . import messaging


def openConversationWith(contact_name):
    """
    Looks for contact/group in the search pane and opens conversation with them
    Partial name recognition is implemented, but not recommended

    Parameters:
        contact_name (string): Contact to open a conversation with

    Returns:
        None
    """
    try:
        convo = next((conversation for conversation in messaging.side_pane.find_elements(by=By.XPATH, value='//div[starts-with(@style, "z-index")]') if conversation.text.split("\n")[0] == contact_name))
        convo.click()
    except (StopIteration, ElementClickInterceptedException):
        search_box = side_pane.find_element(by=By.TAG_NAME, value="label").find_element(by=By.TAG_NAME, value="div")
        search_box.click()
        search_box_to_fill = side_pane.find_element(by=By.TAG_NAME, value="label").find_element(by=By.TAG_NAME, value="div").find_element(by=By.XPATH, value='.//div[@data-tab="3"][@contenteditable="true"]')
        search_box_to_fill.send_keys(contact_name)
        contact_conversation_loaded = EC.presence_of_element_located((By.XPATH,'//span[@title="' + contact_name + '"]'))
        try:
            WebDriverWait(browser, 3).until(contact_conversation_loaded)
        except TimeoutException:
            WebDriverWait(browser, 3).until(EC.presence_of_element_located((By.XPATH,'//span[starts-with(@title,"' + contact_name + '")]')))
        search_box_to_fill.send_keys(Keys.ENTER)
        if contact_name == config_data["home_group"]:
            messaging.sendMessage("Home sweet home :)")
    

def getCurrentConversation():
    """
    Parameters:
        None
    Returns:
        List:
            For groups: ['GroupName', 'Member1,Member2[...membern]']
            For private chats: ['Contact Name/Number','Last seen (If applicable)]
    """
    return browser.find_element_by_id("main").find_element(by=By.TAG_NAME, value="header").text.split("\n")



def goHome():
    """
    Goes to the conversation specified in "home_group".
    Important to not accidentally read messages
    """
    openConversationWith(config_data["home_group"])
