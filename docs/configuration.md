<div style="text-align: center;">
<a href="index.html">Home</a> |
<a href="requirements.html">Requirements</a> |
<a href="commands.html">Commands</a> |
<a href="configuration.html">Configuration</a> |
<a href="address.html">Addresses</a> |
<a href="message.html">Message</a> |
<a href="errors.html">Errors</a> |
<a href="https://www.gnu.org/licenses/gpl-3.0-standalone.html" target="_license">License</a>
</div>

## Configuration

Script configuration settings are provided using a plain text configuration file.  The script will
use the file `bulkmail.cfg` in the current directory by default, although an alternate configuration
file can be specified on the commend line.

Configuration file settings include:

- **MAIL_SERV**: The url of the mail server to use.  (e.g.: `smtp.gmail.com`)
- **MAIL_PORT**: The port number to connect to on the server.  (e.g.: `587`)
- **MAIL_SERV_LOGON_ID**: The User ID to use when logging into the mail server.  (e.g.: `joe.blow@gmail.com`)
- **MAIL_SERV_LOGON_PW**: The User password to use when logging into the mail server.
- **MAIL_WAIT**: The number of seconds to wait between sending messages.  Recommend a minimum of 1 second.
- **MAIL_FROM_ADDR**: The address to show in the From: header line.  Note that many (most?) mail servers require that this be the same as the logged in account.
- **MAIL_REPLY_ADDR**: The address to show in the Reply-To: header line.  This is optional and only included if the SEND_REPLY setting is set to True.
- **MAIL_ADDRESS_FILE**: The file containing the destination address list information.
- **MAIL_MESSAGE_FILE**: The file containing the message template in CommonMark markdown format.
- **SEND_REPLY**: Determines whether or not to include the specified Reply-To: address with each message.
- **ADDRESS_TEMPLATE**: The template used to format each entry in the CSV file into an address used as the destination address for a message.  (e.g.: `{first_name} {last_name} <{email}>`)
- **NO_CONFIRM**: Determines whether or not to ask for confirmation to continue after a warning or before sending any email messages.
- **NO_FOOTER**: Determines whether or not to include a footer on the message showing the version of the Python Bulk Mail script used.
- **LOG_FILE**: The file to use for logging processing activity.  This file will be created if it doesn't exist, and subsequent process runs will append to the file.
- **LOG_LEVEL**: Specifies the amount of information to include in the log file, as:
  - 0 = no logging
  - 1 = log errors and warnings
  - 2 = log errors, warnings and processing information
  - 3 = log errors, warnings, processing information and debug information
  - 4 = log errors, warnings, processing information and extreme debug information
- **DISPLAY_LEVEL**: Specifies the amount of information to write to the console, as:
  - 0 = no display (also implies no confirmation)
  - 1 = display errors and warnings
  - 2 = display errors, warnings and processing information
  - 3 = display errors, warnings, processing information and debug information

Please see the sample configuration file for more information about these settings.

---
