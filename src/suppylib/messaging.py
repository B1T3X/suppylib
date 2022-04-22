from .navigation import *
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import re
from . import navigation, logging


#from suppy import *

def checkForNewMessages():
    """
    Checks visible conversations on the side pane for new messages and returns a dictionary:

    Parameters:
        None

    Returns:
        Dictionary:
            {<Conversation Name>: [<Amount of New Messages>, <Is Group>]}
    """
    last_conversation_containers = side_pane.find_elements_by_xpath('.//div[starts-with(@style, "z-index")]')
    last_conversations = [conversation.text.split("\n") for conversation in last_conversation_containers]
    conversations_with_new_messages = dict()
    for conversation in last_conversations:
        if 3 < len(conversation) < 7 and re.match("^[1-9]$",conversation[-1]):
            if conversation[3] == ": ":
                is_group = True
            else:
                is_group = False
            conversations_with_new_messages[conversation[0]] = [int(conversation[-1]), is_group]
    return conversations_with_new_messages

def readMyMessages(conversation=None, tail=None):
    """
    Reads messages sent by us
    
    Parameters:
        conversation (string): Conversation to read messages in.
            If ommited, reads from current conversation.

        tail (int): Number of messages to read from the end.
            If ommited, all visible messages are retrieved

    Returns:
        list of tuples:
            [(<Message 1>,<Time Sent>), (<Message 2>,<Time Sent>)]...
    """
    messages_to_return = list()
    if conversation != None:
        openConversationWith(conversation)
    main_pane = browser.find_element_by_id("main")
    my_messages = [message_block for message_block in main_pane.find_elements_by_xpath('.//div[contains(@class,"message-out")]')]
    if tail:
        my_messages = my_messages[len(my_messages)-tail:]
    for message in my_messages:
        message_textual_fields = message.text.split("\n")
        if re.match('^[0-9]{2}:[0-9]{2}$', message_textual_fields[0]):
            print("Message at {} is unreadable".format(message_textual_fields[0]))
        else:
            print("Message at {} is {}".format(message_textual_fields[-1], message_textual_fields[0]))
        message_to_append = (lambda lst: (','.join(lst[:-1]), lst[-1]))(message_textual_fields)
        messages_to_return.append(message_to_append)
    return messages_to_return


def readNewMessages(conversation=None, tail=None, isgroup=False):
    """
    Reads new messages sent by others in a conversation
    Message parsing is different beetwen contacts and groups, and so the isgroup flag is important.

    Parameters:
        conversation (string): Conversation to read messages in.
        If ommited, reads from current conversation.

        tail (int): Number of messages to read from the end.
        If ommited, all visible messages are retrieved

        isgroup (bool): Is the conversation a group or a private chat?
        Default is False (conversation is a private chat)

    Returns:
        if isgroup:
            3-string list [sender, message, time]
        else:
            2-string list [message, time]
    Might standardize later if I decide to implement a logging or data storage mechanism.
    """
    messages_to_return = list()
    if conversation != None:
        openConversationWith(conversation)
    main_pane = browser.find_element_by_id("main")
    new_messages = [message_block for message_block in main_pane.find_elements_by_xpath('.//div[contains(@class,"message-in")]')]
    if tail:
        new_messages = new_messages[len(new_messages)-tail:]
    for message in new_messages:
        message_textual_fields = message.text.split("\n")
        if re.match('^[0-9]{2}:[0-9]{2}$', message_textual_fields[0]):
            print("Message at {} is unreadable".format(message_textual_fields[0]))
        # else:
        #     print("Message at {} is {}".format(message_textual_fields[-1], message_textual_fields[0]))
        if isgroup:
            # Check if user who isn't saved as a contact has a nickname, if so, choose it as the name
            if re.match(r"^\+[0-9]+\s\(?[0-9]+\)?(\s|\-)?[0-9]+(\s|\-)?[0-9]+", message_textual_fields[0]):
                try:
                    message.find_element_by_xpath('.//span[text()="' + message_textual_fields[1] + '" and @dir="auto"]')
                    # This line is used to get the nickname from an unsaved contact's phone number, but that's probably a bad idea
                    #message_textual_fields.remove(message_textual_fields[0])
                    # I changed it to choose the number instead of the nickname
                    message_textual_fields.remove(message_textual_fields[1])
                except NoSuchElementException:
                    pass
            try:
                message.find_element_by_xpath('.//div[contains(@class, " color-")]')
                message_to_append = (lambda lst: (lst[0], ','.join(lst[1:-1]), lst[-1]))(message_textual_fields)
            except NoSuchElementException:
                try:
                    message_to_append = (lambda lst1, lst2: (lst1[-1][0], ','.join(lst2[:-1]), lst2[-1]))(messages_to_return, message_textual_fields)
                except IndexError:
                    message_to_append = (lambda name, lst2: (name, ','.join(lst2[:-1]), lst2[-1]))(main_pane.find_elements_by_xpath('.//div[contains(@class," color-")]')[-1].text, message_textual_fields)
        else:
            message_to_append = (lambda lst: (','.join(lst[:-1]), lst[-1]))(message_textual_fields)
        messages_to_return.append(message_to_append)
    logging.logMessagesReceived(getCurrentConversation()[0], messages_to_return, isgroup=isgroup)
    return messages_to_return


def sendMessage(message):
    """
    Sends message in current conversation

    Parameters:
        message (string): Message to send

    Returns:
        None
    """
    if message is None:
        pass
    else:
        try:
            browser.find_element_by_xpath('//div[contains(@class, " color-")]')
        except NoSuchElementException:
            isgroup = False
        else:
            isgroup = True
        message_field = browser.find_element_by_xpath('.//div[@spellcheck="true"]')
        if isinstance(message, list):
            ActionChains(browser).click(message_field).perform()
            for line in message:
                ActionChains(browser).send_keys(line).key_down(Keys.SHIFT).send_keys(Keys.ENTER).key_up(Keys.SHIFT).perform()
        elif isinstance(message, str):
            message_field.send_keys(message)
        try:
            WebDriverWait(browser, 3).until(EC.presence_of_element_located((By.XPATH,'//span[@data-icon="send"]')))
            send_button = browser.find_element(by=By.XPATH, value='//span[@data-icon="send"]')
            browser.execute_script("arguments[0].click();", send_button)
        except (NoSuchElementException, TimeoutException):
            time.sleep(.500)
            send_button = browser.find_element(by=By.XPATH, value='.//span[@data-icon="send"]')
            browser.execute_script("arguments[0].click();", send_button)
        except UnboundLocalError:
            pass
        finally:
            logging.logMessageSent(getCurrentConversation()[0], message, isgroup=isgroup)
            print("Message sent!")

def sendMessageTo(contact, message):
    """
    Navigates to specified contact and sends message
    """
    openConversationWith(contact)
    sendMessage(message)
