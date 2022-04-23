# suppylib - A WhatsApp bot framework automating WhatsApp Web

suppylib is a small Python library I wrote, to make it possible to automate 
the WhatsApp Web interface using Selenium and Google Chrome.

As cool as this project is remember the following:
* Spam isn't cool
* Facebook, as you may know, does not endorse these kinds of projects
* Therefore, this may break at any given moment and I may not have the time or
energy to fix it
* I am not responsible for you abusing this and/or getting banned
* Zucc please don't sue me bro

## Installation:
```
pip install suppylib
```

## Requirements:
1. Google Chrome
2. The corresponding [ChromeDriver](https://chromedriver.chromium.org/downloads)
   in your `$PATH`
3. Python 3.x
4. The libraries listed in requirements.txt

## Library:
suppylib is made of several sub-modules for the sake of order (or lack thereof)
* `suppylib.messaging`
* `suppylib.navigation`
* `suppylib.logging`
* `suppylib.bot`

My assumption is that only `suppylib.bot` will be used but feel free to use the
underlying sub-modules for whatever devious thing you're planning.

### the SuppyBot class  
The class `suppylib.bot.SuppyBot` allows you to seamlessly and intuitively control
WhatsApp Web.

```
from suppylib import bot
my_suppybot = bot.SuppyBot(<Config File>)


# Wait for suppy bot to login...
# If running headless, make sure you scan the QR code created under `status.jpg`


my_suppybot.check_for_new_messages()

#  Checks visible conversations on the side pane for new messages and returns a dictionary:
#
#      Parameters:
#          None
#
#      Returns:
#          Dictionary:
#              {<Conversation Name>: [<Amount of New Messages>, <Is Group>]}


my_suppybot.move_to_conversation(contact_name)

#  Looks for contact/group in the search pane and opens conversation with them.
#  Partial name recognition is implemented, but not recommended.
#
#  Parameters:
#      contact_name (string): Contact to open a conversation with
#
#  Returns:
#      None


my_suppybot.send_message(message)

#  Sends message in current conversation
#
#   Parameters:
#       message (string): Message to send
#
#   Returns:
#       None


my_suppybot.read_my_messages(conversation, tail)

#  Reads messages sent by us
#
#   Parameters:
#       conversation (string): Conversation to read messages in.
#           If ommited, reads from current conversation.
#
#       tail (int): Number of messages to read from the end.
#           If ommited, all visible messages are retrieved
#
#   Returns:
#       list of tuples:
#           [(<Message 1>,<Time Sent>), (<Message 2>,<Time Sent>)]...


my_suppybot.read_my_messages(conversation, tail, isgroup)

#  Reads new messages sent by others in a conversation
#    Message parsing is different beetwen contacts and groups, and so the isgroup flag is important.
#
#    Parameters:
#        conversation (string): Conversation to read messages in.
#        If ommited, reads from current conversation.
#
#        tail (int): Number of messages to read from the end.
#        If ommited, all visible messages are retrieved
#
#        isgroup (bool): Is the conversation a group or a private chat?
#        Default is False (conversation is a private chat)
#
#    Returns:
#        if isgroup:
#            3-string list [sender, message, time]
#        else:
#            2-string list [message, time]
#    Might standardize later if I decide to implement a logging or data storage mechanism.


my_suppybot.go_home()

# Goes to the conversation defined in "home_group" in the config file
# Recommended to be done after finishing with a conversation


my_suppybot.shutdown()

# Close the bot and Chrome

```



## The configuration file
To configure SuppyBot you need to create a valid JSON config file.

`home_group` - Where Suppy will go to rest after performing operations  
`chrome_arguments` - Arguments to pass the Chrome executable, you can look at
Chrome's official documentation on the matter.

Example config file:
```
{
  "home_group": "SuppyHomeBeepBoop",
  "chrome_arguments": [
    "--profile-directory=Profile 3",
    "--user-data-dir=\/home\/orel\/.config\/google-chrome",
    "--start-maximized",
    "--headless",
    "--user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36"
    ]
}
```

## Things left to do (this is where you may come in...):
* Better TCP protocolization, and actual use of TCP
* Solve some bugs and crashes
* Add support for better configuration options (such as different browsers)
