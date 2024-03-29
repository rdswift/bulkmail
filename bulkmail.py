#!/usr/bin/env python3
##############################################################################
#                                                                            #
#   Bulk Mail - A bulk mail / mail merge system using Python 3               #
#   Copyright (C) 2019, 2024 Bob Swift (rdswift)                             #
#                                                                            #
#   This program is free software: you can redistribute it and/or modify     #
#   it under the terms of the GNU General Public License as published by     #
#   the Free Software Foundation, either version 3 of the License, or        #
#   (at your option) any later version.                                      #
#                                                                            #
#   This program is distributed in the hope that it will be useful,          #
#   but WITHOUT ANY WARRANTY; without even the implied warranty of           #
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the            #
#   GNU General Public License for more details.                             #
#                                                                            #
#   You should have received a copy of the GNU General Public License        #
#   along with this program.  If not, see <https://www.gnu.org/licenses/>.   #
#                                                                            #
##############################################################################
#                                                                            #
#   This project is hosted at https://github.com/rdswift/bulkmail and        #
#   suggestions for improvement (with or without code), and bug reports      #
#   are appreciated.
#                                                                            #
#   The author can be contacted via email at bswift@rsds.ca or via postal    #
#   mail at:                                                                 #
#                                                                            #
#   Bob Swift                                                                #
#   5708 47 Street                                                           #
#   Stony Plain, Alberta T7Z 1C6                                             #
#   Canada                                                                   #
#                                                                            #
##############################################################################
"""
Python script used to send bulk email as individual messages using
an external smtp account such as Gmail.
"""

SCRIPT_NAME = 'Bulk Mail'
SCRIPT_VERS = '0.07'
SCRIPT_COPYRIGHT = '2024'
SCRIPT_AUTHOR = 'Bob Swift'
SCRIPT_URL = 'https://rdswift.github.io/bulkmail/'


import argparse
import csv
import datetime
import os
import re
import smtplib
import textwrap
import time
from email.message import Message
# from email.mime.message import MIMEMessage
from email.mime.multipart import MIMEMultipart
# from email.mime.text import MIMEText

import commonmark
import html2text

DASH_LINE = '-' * 79

########################################
#   Error messages and return values   #
########################################

ERRORS = {
    100: "No processing command specified.",
    101: "Error accessing the configuration file.",
    102: "Invalid key in the configuration file.",
    103: "Invalid setting in the configuration file.",
    104: "Invalid setting on the command line.",
    105: "Error accessing the address file.",
    106: "Address file does not appear to have a header row.",
    107: "Address list appears to be empty.",
    108: "Error accessing the message file.",
    109: "Missing email address template.",
    110: "No fields in email address template.",
    111: "Unknown field(s) in email address template.",
    112: "Error accessing the message file.",
    113: "Message appears to be blank.",
    114: "Error connecting to the mail server.",
    115: "Error sending one or more messages.",
    116: "Unknown field(s) in email message template.",
    117: "Missing or invalid log file name.",
    118: "Unable to write to the log file.",
}


################################
#   Regular expressions used   #
################################

# Remove header formatting from message plain text template
RE_HEADERS = re.compile(r'^[ \t]*#+[ \t]+', re.M)

# Extract subject from message markdown template
RE_SUBJ_GET = re.compile(r'^[ \t]*#+\s+(.*)[ \t]*[\n\r]')

# Remove subject line from message markdown template
RE_SUBJ_DEL = re.compile(r'^[ \t]*#+\s+.*[ \t]*[\n\r]+')

# Identify fields in email address template and message template
RE_MAIL_ADD = re.compile(r'\{([^\}]*)')

# Check if a message template is blank
RE_BLANK_MSG = re.compile(r'^[\s\t\n\r]*$')

# Identify and reformat markdown links in message plain text template
RE_TEXT_LINKS = re.compile(r'\[([^\]]*)\]\(<([^>]*)>\)')


#######################################################
#   Initialize program settings to program defaults   #
#######################################################

# TODO: enable Cc: and Bcc: addresses
# SETTINGS = {
#     'MAIL_SERV': 'smtp.gmail.com',
#     'MAIL_PORT': 587,
#     'MAIL_SERV_LOGON_ID': '',
#     'MAIL_SERV_LOGON_PW': '',
#     'MAIL_WAIT': 1,
#     'MAIL_FROM_ADDR': '',
#     'MAIL_REPLY_ADDR': '',
#     # 'MAIL_CC_ADDR': [],
#     # 'MAIL_BCC_ADDR': [],
#     'MAIL_ADDRESS_FILE': '',
#     'MAIL_MESSAGE_FILE': '',
#     # 'SEND_CC': False,
#     # 'SEND_BCC': False,
#     'SEND_REPLY': False,
#     'ADDRESS_TEMPLATE': '',
#     'NO_CONFIRM': False,
#     'LOG_FILE': 'bulkmail.log',
#     'LOG_LEVEL': 2,
#     'DISPLAY_LEVEL': 2,
#     'NO_FOOTER': False,
# }


#########################################################
#   Text to display when --warranty option is invoked   #
#########################################################

WARRANTY_TEXT = '''\
THERE IS NO WARRANTY FOR THE PROGRAM, TO THE EXTENT PERMITTED BY
APPLICABLE LAW. EXCEPT WHEN OTHERWISE STATED IN WRITING THE COPYRIGHT
HOLDERS AND/OR OTHER PARTIES PROVIDE THE PROGRAM “AS IS” WITHOUT
WARRANTY OF ANY KIND, EITHER EXPRESSED OR IMPLIED, INCLUDING, BUT NOT
LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A
PARTICULAR PURPOSE. THE ENTIRE RISK AS TO THE QUALITY AND PERFORMANCE OF
THE PROGRAM IS WITH YOU. SHOULD THE PROGRAM PROVE DEFECTIVE, YOU ASSUME
THE COST OF ALL NECESSARY SERVICING, REPAIR OR CORRECTION.

IN NO EVENT UNLESS REQUIRED BY APPLICABLE LAW OR AGREED TO IN WRITING
WILL ANY COPYRIGHT HOLDER, OR ANY OTHER PARTY WHO MODIFIES AND/OR
CONVEYS THE PROGRAM AS PERMITTED ABOVE, BE LIABLE TO YOU FOR DAMAGES,
INCLUDING ANY GENERAL, SPECIAL, INCIDENTAL OR CONSEQUENTIAL DAMAGES
ARISING OUT OF THE USE OR INABILITY TO USE THE PROGRAM (INCLUDING BUT
NOT LIMITED TO LOSS OF DATA OR DATA BEING RENDERED INACCURATE OR LOSSES
SUSTAINED BY YOU OR THIRD PARTIES OR A FAILURE OF THE PROGRAM TO OPERATE
WITH ANY OTHER PROGRAMS), EVEN IF SUCH HOLDER OR OTHER PARTY HAS BEEN
ADVISED OF THE POSSIBILITY OF SUCH DAMAGES.

If the disclaimer of warranty and limitation of liability provided above
cannot be given local legal effect according to their terms, reviewing
courts shall apply local law that most closely approximates an absolute
waiver of all civil liability in connection with the Program, unless a
warranty or assumption of liability accompanies a copy of the Program in
return for a fee.
'''


##################################################
#   Text to display when the script is started   #
##################################################

COPYRIGHT_TEXT = f"""
{SCRIPT_NAME} (v{SCRIPT_VERS})  Copyright (C) {SCRIPT_COPYRIGHT}  {SCRIPT_AUTHOR}
This program comes with ABSOLUTELY NO WARRANTY; for details use option
'--warranty'.  This is free software, and you are welcome to redistribute
it under certain conditions.  Please see the GPLv3 license for details.

"""


###############################################################
#   Text to display when --redistribution option is invoked   #
###############################################################

REDISTRIBUTION_TEXT = '''\
'''


class Settings():
    MAIL_SERV = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_SERV_LOGON_ID = ''
    MAIL_SERV_LOGON_PW = ''
    MAIL_WAIT = 1
    MAIL_FROM_ADDR = ''
    MAIL_REPLY_ADDR = ''
    # MAIL_CC_ADDR = []
    # MAIL_BCC_ADDR = []
    MAIL_ADDRESS_FILE = ''
    MAIL_MESSAGE_FILE = ''
    # SEND_CC = False
    # SEND_BCC = False
    SEND_REPLY = False
    ADDRESS_TEMPLATE = ''
    NO_CONFIRM = False
    LOG_FILE = 'bulkmail.log'
    LOG_LEVEL = 2
    DISPLAY_LEVEL = 2
    NO_FOOTER = False


class Writer():

    INITIALIZING = True

    @classmethod
    def Log(cls, level, text):
        """Write an entry to the log file if the entry level is less than or equal to the log level.

        Arguments:
            level {int} -- the minimum log level to write the entry
            text {str} -- the entry to add to the log
        """
        if cls.INITIALIZING or level > Settings.LOG_LEVEL:
            return
        try:
            lines = text.split("\n")
            with open(Settings.LOG_FILE, 'a', encoding='UTF-8') as f:
                for line in lines:
                    f.write(f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  {line}".strip() + "\n")
        except Exception:
            errorNumber = 118
            cls.Console(1, f"\n{ERRORS[errorNumber]} Filename: '{Settings.LOG_FILE}'\n")
            quit(errorNumber)

    @staticmethod
    def Console(level, text):
        """Write an entry to the console.

        Arguments:
            level {int} -- the minimum display level to write the entry
            text {str} -- the entry to write to the console
        """
        if level > Settings.DISPLAY_LEVEL or Settings.DISPLAY_LEVEL < 1:
            return
        print(text)

    @classmethod
    def ConsoleAndLog(cls, level, text):
        """Write an entry to both the console and the log file.

        Arguments:
            level {int} -- the minimum display / log level to write the entry
            text {str} -- the entry to write
        """
        cls.Console(level, text)
        cls.Log(level, text)


#########################################
#   Error handling (display and exit)   #
#########################################

def errorAndExit(errNumber, errorText="", extraText=""):
    """Print and log error message and exit with specified error number.

    Arguments:
        errNumber {int} -- Error number / exit code

    Keyword Arguments:
        errorText {str} -- Error message to use in place of default message for the specified error number (default: "")
        extraText {str} -- Additional text to append to the error message (default: "")
    """
    if not errorText:
        if errNumber in ERRORS:
            errorText = ERRORS[errNumber]
        else:
            errorText = "Unknown error."
    if extraText:
        errorText += ' ' + extraText
    Writer.ConsoleAndLog(1, errorText)
    quit(errNumber)


# def writeLog(level, text):
#     """Write an entry to the log file if the entry level is less than or equal to the log level.

#     Arguments:
#         level {int} -- the minimum log level to write the entry
#         text {str} -- the entry to add to the log
#     """
#     if (level > SETTINGS['LOG_LEVEL']) or INITIALIZING:
#         return
#     try:
#         lines = text.split("\n")
#         with open(SETTINGS['LOG_FILE'], 'a', encoding='UTF-8') as f:
#             for line in lines:
#                 f.write(f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  {line}".strip() + "\n")
#     except Exception:
#         errorNumber = 118
#         writeConsole(1, f"\n{ERRORS[errorNumber]} Filename: '{SETTINGS['LOG_FILE']}'\n")
#         quit(errorNumber)


#################################
#   Write line to the console   #
#################################

# def writeConsole(level, text):
#     """Write an entry to the console.

#     Arguments:
#         level {int} -- the minimum display level to write the entry
#         text {str} -- the entry to write to the console
#     """
#     if (level > SETTINGS['DISPLAY_LEVEL']):
#         return
#     if (SETTINGS['DISPLAY_LEVEL'] > 0):
#         print(text)


##################################################
#   Write to both the console and the log file   #
##################################################

# def writeConsoleAndLog(level, text):
#     """Write an entry to both the console and the log file.

#     Arguments:
#         level {int} -- the minimum display / log level to write the entry
#         text {str} -- the entry to write
#     """
#     writeConsole(level, text)
#     writeLog(level, text)


##################################
#   Check and save the setting   #
##################################

def saveSetting(key, value, from_config_file=False):
    """Save an entry to the settings dictionary.

    Arguments:
        setting_list {dict} -- the dictionary containing the program settings
        key {str} -- the key to update in the settings dictionary
        value {obj} -- the value to store for the specified key

    Keyword Arguments:
        from_config_file {bool} -- flag to indicate whether the update is from the configuration file (default: False)
    """
    key = key.strip().upper()
    value = f"{value}".strip()
    if hasattr(Settings, key):
        setting_type = type(getattr(Settings, key))
        if setting_type == bool:
            # setting_list[key] = (value.strip().upper() == 'TRUE')
            setattr(Settings, key, (value.strip().upper() == 'TRUE'))
        elif setting_type == int:
            value = value.split()[0]
            try:
                iValue = int(value)
                if (key == 'MAIL_WAIT' and iValue < 0) or \
                        (key == 'LOG_LEVEL' and (iValue < 1 or iValue > 4)) or \
                        (key == 'DISPLAY_LEVEL' and (iValue < 1 or iValue > 3)) or \
                        (key == 'MAIL_PORT' and (iValue < 1 or iValue > 65535)):
                    raise ValueError
                # setting_list[key] = iValue
                setattr(Settings, key, iValue)
            except ValueError:
                errorAndExit(103 if from_config_file else 104, extraText=f"Setting: {key} = '{value}'")
        elif value and setting_type == list:
            setting_list = getattr(Settings, key)
            setting_list.append(value)
            setattr(Settings, key, setting_list)
        else:
            # setting_list[key] = value
            setattr(Settings, key, value)
    else:
        if from_config_file:
            errorAndExit(102, extraText=f"Setting: '{key}'")


#########################
#   Confirm an action   #
#########################

def confirmAction(action_message):
    """Ask the user to confirm the specified action or condition.

    Arguments:
        SETTINGS {dict} -- the dictionary containing the program settings
        action_message {str} -- the action or condition to comfirm
    """
    if Settings.NO_CONFIRM or Settings.DISPLAY_LEVEL < 1:
        return True
    resp = input(f"\n{action_message}  Continue?  (y/N) ")
    resp = (resp and resp[:1].upper() == 'Y')
    if not resp:
        Writer.ConsoleAndLog(2, "\nCancelled by the user.\n")
        quit(0)
    return True


#############################
#   Send an email message   #
#############################

def sendMessage(msg_to, subject, msg_text, msg_html, count, count_err, count_max):
    """Assemble the message and send it using the server, port and credentials specified in the settings.

    Arguments:
        SETTINGS {dict} -- the dictionary containing the program settings
        msg_to {str} -- the email address of the recipient
        subject {str} -- the subject of the message
        msg_text {str} -- the body of the message in plain text format
        msg_html {str} -- the body of the message in html format
        count {int} -- the processed message counter
        count_err {int} -- the number of messages that were not sent successfully
        count_max {int} -- the total number of messages to be sent
    """
    if not Settings.NO_FOOTER:
        msg_text += f"\n---\nSent using the Python {SCRIPT_NAME} (v{SCRIPT_VERS}) script.  {SCRIPT_URL}"
        msg_html += f"\n<p><hr>\n<span style='font-size: 80%;'>Sent using the Python {SCRIPT_NAME} (v{SCRIPT_VERS}) script.  <a href=\"{SCRIPT_URL}\" target=\"_blank\">{SCRIPT_URL}</a></span></p>"
    message = MIMEMultipart('alternative')
    message['From'] = Settings.MAIL_FROM_ADDR
    if Settings.SEND_REPLY and Settings.MAIL_REPLY_ADDR:
        message['Reply-to'] = Settings.MAIL_REPLY_ADDR
    message['To'] = msg_to
    # message['Cc'] = 'Receiver2 Name <receiver2@server>'    # Assume you don't want to Cc: or Bcc: a mass mailing
    # message['Bcc'] = 'Receiver3 Name <receiver3@server>'   # Assume you don't want to Cc: or Bcc: a mass mailing
    message['Subject'] = subject
    message['X-Mailer'] = f'Python/{SCRIPT_NAME} (v{SCRIPT_VERS})'

    # Record the types of both parts - text/plain and text/html.
    part1 = Message()
    part1.set_type('text/plain')
    part1.set_charset('UTF-8')
    part1.replace_header('Content-Transfer-Encoding', '8-bit')
    part1.set_payload(msg_text)
    part2 = Message()
    part2.set_type('text/html')
    part2.set_charset('UTF-8')
    part2.replace_header('Content-Transfer-Encoding', '8-bit')
    part2.set_payload(msg_html)

    # Attach parts into message container.
    # According to RFC 2046, the last part of a multipart message, in this case
    # the HTML message, is best and preferred.
    message.attach(part1)
    message.attach(part2)
    msg_full = message.as_string()

    Writer.ConsoleAndLog(4, f"\n{DASH_LINE}\nMessage Content:\n\n{msg_full}\n")

    # Here is the section that actually processes and sends the mail
    count += 1
    if count < 2:
        Writer.ConsoleAndLog(2, f"\nSending mail to {count_max} recipients:")
    print_text = f"{count:>5}.  {msg_to}{' ' * 61}  "[:61] + ' '
    if Settings.DISPLAY_LEVEL > 1:
        print(print_text, end="", flush=True)
    try:
        server = smtplib.SMTP(f"{Settings.MAIL_SERV}:{Settings.MAIL_PORT}")
        server.starttls()
        server.login(Settings.MAIL_SERV_LOGON_ID, Settings.MAIL_SERV_LOGON_PW)
        return_value = server.sendmail(Settings.MAIL_FROM_ADDR, [msg_to,], msg_full.replace('\r\n', '\n').replace('\n', '\r\n').encode('UTF-8'))
    except Exception as ex:
        if (Settings.DISPLAY_LEVEL > 1):
            print("Failure")
        errorAndExit(114, extraText=f"\nException: {ex}")
    if return_value:
        count_err += 1
    server.quit()
    if Settings.DISPLAY_LEVEL > 1:
        print("Failure" if return_value else "Success")
    Writer.Log(2, print_text + ("Failure" if return_value else "Success"))
    if count < count_max:
        time.sleep(Settings.MAIL_WAIT)
    return (count, count_err)


##############################################################################

def parse_address_file(addr_file):
    """Read the addresses CSV file.

    Args:
        addr_file (str): Name of CSV file to read

    Returns:
        tuple: address list list, address fields list
    """
    addr_list = []
    addr_fields = []
    with open(addr_file, newline='', encoding="UTF-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            addr_list.append(row,)
        addr_fields = reader.fieldnames

    return addr_list, addr_fields


##############################################################################

def parse_command_line():
    """Parse the command line arguments.
    """

    # TODO: enable sending to Cc: and Bcc: addresses
    arg_parser = argparse.ArgumentParser(
        description=f"{SCRIPT_NAME} (v{SCRIPT_VERS})\nSends the same email message individually to multiple recipients.",
        usage="'bulkmail.py --help'  or  'bulkmail.py -c command [options]'",
    )
    arg_parser.add_argument(
        "-c",
        "--cmd",
        help="The processing command 'send' or 'test'.",
        metavar='CMD',
        choices=['send', 'test'],
    )
    group0 = arg_parser.add_mutually_exclusive_group()
    group0.add_argument(
        "-a",
        "--confirm",
        help="Request confirmation on actions or warnings.",
        action='store_true',
    )
    group0.add_argument(
        "-A",
        "--no-confirm",
        help="Don't request confirmation on actions or warnings.",
        action='store_true',
    )
    arg_parser.add_argument(
        "--addr-file",
        help="The file containing a list of destination addresses in CSV format with the first row containing the column names.",
        metavar='FILE',
        dest='MAIL_ADDRESS_FILE',
    )
    # group1 = arg_parser.add_mutually_exclusive_group()
    # group1.add_argument("-b", "--send-bcc", help="Include the Bcc: address(es).", action='store_true')
    # group1.add_argument("-B", "--no-bcc", help="Do not include the Bcc: address(es).", action='store_true')
    # arg_parser.add_argument("--bcc", help="Set the Bcc: address(es).  Multiple addresses are separated by spaces.", metavar='ADD', nargs='+')
    # group2 = arg_parser.add_mutually_exclusive_group()
    # group2.add_argument("-c", "--send-cc", help="Include the Cc: address(es).", action='store_true')
    # group2.add_argument("-C", "--no-cc", help="Do not include the Cc: address(es)", action='store_true')
    # arg_parser.add_argument("--cc", help="Set the Cc: address(es).  Multiple addresses are separated by spaces", metavar='ADD', nargs='+')
    arg_parser.add_argument(
        "--config-file",
        help="The file containing the configuration information.  Defaults to bulkmail.cfg in the current directory.",
        metavar='FILE',
    )
    arg_parser.add_argument(
        "--display-level",
        help="The amount of information to write to the display.  0=no display (also implies -A) to 3=display everything (debug)",
        metavar='NUM',
        choices=['0', '1', '2', '3',],
        dest='DISPLAY_LEVEL',
    )
    arg_parser.add_argument(
        "--email",
        help="Set the template to use to build the destination email addresses from the fields in the CSV file. (e.g.: {first_name} {last_name} <{email}>)",
        metavar='TEMPLATE',
        dest='ADDRESS_TEMPLATE',
    )
    arg_parser.add_argument(
        "--from",
        help="Set the From: address.",
        metavar='ADDR',
        dest='MAIL_FROM_ADDR',
    )
    arg_parser.add_argument(
        "--log-file",
        help="The file to write the session logs.  Defaults to bulkmail.log in the current directory.",
        metavar='FILE',
        dest='LOG_FILE',
    )
    arg_parser.add_argument(
        "--log-level",
        help="The amount of information to write to the log file.  0=no logging to 4=log everything (extreme debug)",
        metavar='NUM',
        choices=['0', '1', '2', '3', '4'],
        dest='LOG_LEVEL',
    )
    arg_parser.add_argument(
        "--message",
        help=(
                "The file containing the message (in markdown format) to send.  "
                "The first line contains the message subject formatted as a Header 1. (e.g.: # This is the Subject)"
            ),
        metavar='FILE',
        dest='MAIL_MESSAGE_FILE',
    )
    group3 = arg_parser.add_mutually_exclusive_group()
    group3.add_argument(
        "-f",
        "--footer",
        help="Include a footer on the message showing the program used.",
        action='store_true',
    )
    group3.add_argument(
        "-F",
        "--no-footer",
        help="Don't include a footer on the message showing the program used.",
        action='store_true',
    )
    group4 = arg_parser.add_mutually_exclusive_group()
    group4.add_argument(
        "-r",
        "--send-reply",
        help="Include the Reply-To address.",
        action='store_true',
    )
    group4.add_argument(
        "-R",
        "--no-reply",
        help="Do not include the Reply-To address.",
        action='store_true',
    )
    arg_parser.add_argument(
        "--reply",
        help="Set the Reply-To: address.",
        metavar='ADDR',
        dest='MAIL_REPLY_ADDR',
    )
    arg_parser.add_argument(
        "--server-url",
        help="The URL of the mail server. (e.g.: smtp.myserver.com)",
        metavar='URL',
        dest='MAIL_SERV',
    )
    arg_parser.add_argument(
        "--server-port",
        help="The port to use on the mail server. (e.g.: 587)",
        type=int,
        metavar='PORT',
        dest='MAIL_PORT',
    )
    arg_parser.add_argument(
        "--subject",
        help="The message subject line.",
    )
    arg_parser.add_argument(
        "--wait",
        help="Number of seconds to wait between sending messages.",
        type=int,
        metavar='SECONDS',
        dest='MAIL_WAIT',
    )
    group5 = arg_parser.add_mutually_exclusive_group()
    group5.add_argument(
        "--warranty",
        help="Show the warranty information and exit.",
        action='store_true',
    )
    # group5.add_argument(
    #     "--redistribution",
    #     help="Show the conditions for redistribution and exit.",
    #     action='store_true',
    # )

    args = arg_parser.parse_args()
    return args


##############################################################################

def main():
    """Main processing.
    """

    Writer.INITIALIZING = True

    args = parse_command_line()

    if args.warranty:
        print(COPYRIGHT_TEXT)
        print(WARRANTY_TEXT)
        quit(0)

    # if args.redistribution:
    #     print(REDISTRIBUTION_TEXT)
    #     quit(0)

    if not args.cmd:
        Settings.LOG_LEVEL = 0
        errorAndExit(100)

    if args.config_file:
        config_file = args.config_file
    else:
        config_file = ""
    if not config_file:
        config_file = 'bulkmail.cfg'

    if not os.path.isfile(config_file):
        errorAndExit(101, extraText=f"File: {config_file}")


    #############################################################
    #   Read updated default settings from configuration file   #
    #############################################################

    with open(config_file, 'rt', encoding='UTF-8', newline=None) as f:
        for line in f:
            line = line.strip()
            if (line) and (line[:1] != '#'):
                key, value = line.split('=', 2)
                saveSetting(key, value, True)


    ###################################################
    #   Update settings from command line arguments   #
    ###################################################

    for arg in vars(args):
        if getattr(args, arg) is not None:
            saveSetting(arg, getattr(args, arg), False)

    if args.send_reply:
        Settings.SEND_REPLY = True

    if args.no_reply:
        Settings.SEND_REPLY = False

    if args.confirm:
        Settings.NO_CONFIRM = False

    if args.no_confirm:
        Settings.NO_CONFIRM = True

    if args.footer:
        Settings.NO_FOOTER = False

    if args.no_footer:
        Settings.NO_FOOTER = True


    #################################
    #   Validate logging settings   #
    #################################

    if Settings.LOG_LEVEL > 0 and not (Settings.LOG_FILE and os.path.isfile(Settings.LOG_FILE)):
        errorAndExit(117, extraText=f"Filename: \"{Settings.LOG_FILE}\"")


    ##################################################
    #   Initialization complete - begin processing   #
    ##################################################

    Writer.INITIALIZING = False

    Writer.Console(1, COPYRIGHT_TEXT)

    Writer.ConsoleAndLog(1, f"\n{'=' * 79}\n\nBegin Bulk Mail processing session.\n")
    print_text = textwrap.fill(f"{args}", 78)
    Writer.ConsoleAndLog(3, f"\nCommand Line Args:\n\n{print_text}\n")

    print_text = ''
    for key, value in Settings.__dict__.items():
        if not key[0] == '_':
            print_text += f"  Key: {key:<24}Value: '{value}'\n"
    Writer.ConsoleAndLog(3, f"\nSettings:\n\n{print_text}\n{DASH_LINE}\n")


    ###############################################
    #   Read the address list from the CSV file   #
    ###############################################

    addr_file = Settings.MAIL_ADDRESS_FILE
    if not (addr_file and os.path.isfile(addr_file)):
        errorAndExit(105, extraText=f"File: {addr_file}")

    addr_list, addr_fields = parse_address_file(addr_file)

    Writer.ConsoleAndLog(3, f"\nAddress CSV Fields: {addr_fields}\n\n{DASH_LINE}\n")

    if not addr_list:
        errorAndExit(107)


    ###########################################################################
    #   Verify that the address template fields are in the address CSV file   #
    ###########################################################################

    if not Settings.ADDRESS_TEMPLATE:
        errorAndExit(109)

    template_fields = re.findall(RE_MAIL_ADD, Settings.ADDRESS_TEMPLATE)

    if not template_fields:
        errorAndExit(110)

    for addr_field in template_fields:
        if not (addr_field in addr_fields):
            errorAndExit(111, extraText=f"Field: '{addr_field}'")

    Writer.ConsoleAndLog(3, f"\nAddress Template Fields: {template_fields}\n\n{DASH_LINE}\n")


    ####################################################
    #   Read the mail message from the markdown file   #
    ####################################################

    msg_file = Settings.MAIL_MESSAGE_FILE
    if not (msg_file and os.path.isfile(msg_file)):
        errorAndExit(112, extraText=f"File: {msg_file}")

    with open(msg_file, newline=None, encoding="UTF-8") as msgfile:
        text = msgfile.read()


    #######################################################
    #   Extract the subject line from the markdown file   #
    #######################################################

    subject = ''
    matches = RE_SUBJ_GET.match(text)
    if matches:
        subject = RE_HEADERS.sub('', matches.group(0).strip())

    if subject:
        text = RE_SUBJ_DEL.sub('', text)
    else:
        subject = 'No subject'

    if args.subject:
        subject = args.subject

    Writer.ConsoleAndLog(3, f"\nMessage Subject:  {subject}\n\n{DASH_LINE}\n")


    #############################################
    #   Verify remaining message is not empty   #
    #############################################

    if RE_BLANK_MSG.search(text):
        errorAndExit(113)

    Writer.ConsoleAndLog(3, f"\nMarkdown Message:\n\n{text}\n\n{DASH_LINE}\n")


    ##############################################################################
    #   Extract list of replaceable parameter fields from the message template   #
    ##############################################################################

    msg_fields = re.findall(RE_MAIL_ADD, text)
    if msg_fields:
        for msg_field in msg_fields:
            if not (msg_field in addr_fields):
                warning_text = f"{ERRORS[116]}  Field: '{msg_field}'"
                Writer.Log(1, warning_text)
                confirmAction(warning_text)


    ####################################################################
    #   Parse the markdown message template to produce HTML template   #
    ####################################################################

    parser = commonmark.Parser()
    ast = parser.parse(text)

    renderer = commonmark.HtmlRenderer()
    html = renderer.render(ast)

    # inspecting the abstract syntax tree
    # json = commonmark.dumpJSON(ast)
    # commonmark.dumpAST(ast) # pretty print generated AST structure

    # html += "\n<hr>\n<sub>Sent using {0} (v{1}).</sub>\n".format(SCRIPT_NAME, SCRIPT_VERS,)

    Writer.ConsoleAndLog(3, f"\nHTML Message Template:\n\n{html}\n\n{DASH_LINE}\n")


    ######################################################################
    #   Parse the HTML message template to produce plain text template   #
    ######################################################################

    text_maker = html2text.HTML2Text()
    text_maker.ignore_links = False
    text_maker.bypass_tables = False
    text_maker.ignore_emphasis = True
    text_maker.skip_internal_links = True
    text_maker.mark_code = False
    text_maker.protect_links = True
    text_maker.body_width = 78
    text = text_maker.handle(html)
    text = RE_HEADERS.sub('', text)

    matches = RE_TEXT_LINKS.search(text)
    while matches:
        (link_text, link_url) = matches.groups()
        text = text.replace(f"[{link_text}]", link_text)
        text = text.replace(f"(<{link_url}>)", f" <{link_url}>")
        matches = RE_TEXT_LINKS.search(text)

    text = text.replace('<\\', '<')

    Writer.ConsoleAndLog(3, f"\nPlain Text Message Template:\n\n{text}\n\n{DASH_LINE}\n")


    #########################################################################
    #   At this point we have final plain text and HTML message templates   #
    #########################################################################

    ####################################
    #   Begin the message processing   #
    ####################################

    Writer.ConsoleAndLog(3, f"\nProcessing Command: {args.cmd}\n\n{DASH_LINE}\n")

    count = 0
    count_err = 0
    if args.cmd == 'send':
        # Sends the email message to the list of recipients from the CSV file
        count_max = len(addr_list)
        if confirmAction(f"You are about to send {count_max} message{'' if count_max == 1 else 's'}."):
            for address_line in addr_list:
                # Process each address in the list
                Writer.ConsoleAndLog(3, f"\nAddress Line from CSV: {address_line}\n")
                msg_text = text
                msg_html = html
                msg_to = Settings.ADDRESS_TEMPLATE
                Writer.ConsoleAndLog(3, "Address and Message Body Replacements:\n")
                for search_field in addr_fields:
                    # Fill in replaceable parameters in the message body for both HTML and plain text
                    old_text = '{' + search_field + '}'
                    new_text = address_line[search_field]
                    msg_text = msg_text.replace(old_text, new_text)
                    msg_html = msg_html.replace(old_text, new_text)
                    # Fill in replaceable parameters in the address template to create the To: address
                    msg_to = msg_to.replace(old_text, new_text)
                    junk = f'"{old_text}"'
                    Writer.ConsoleAndLog(3, f"  Search: {junk:<30}   Replace: \"{new_text}\"")
                Writer.ConsoleAndLog(3, "")
                # Send the email message to the specified address
                (count, count_err) = sendMessage(msg_to, subject, msg_text, msg_html, count, count_err, count_max)
    else:
        # Sends the email template message to the MAIL_FROM_ADDR
        count_max = 1
        if confirmAction("You are about to send 1 message."):
            msg_to = Settings.MAIL_FROM_ADDR
            # Send the email message to the specified address
            (count, count_err) = sendMessage(msg_to, subject, text, html, count, count_err, count_max)


    #############################################################
    #   Processing complete - quit with appropriate exit code   #
    #############################################################

    Writer.ConsoleAndLog(1, f"\nMail processing complete.  Sent {count_max - count_err} of {count_max} message{'' if count_max == 1 else 's'}, with {count_err} failure{'' if count_err == 1 else 's'}.\n\n")

    if count_err > 0:
        errorAndExit(115)

    quit(0)


##############################################################################

if __name__ == '__main__':
    main()

#################################
#   End of bulkmail.py script   #
#################################
