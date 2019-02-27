# Bulk Mail (v0.3)

## Overview

This is a script developed in Python 3 to send the same email message to a list of recipients.
The recipient list of email addresses, optionally including other information, is read from a
comma separated values (CSV) file.  Each message is sent individually so that they can be
customized with replaceable parameters if required.

The message is read from a markdown file and is processed using the CommonMark standard.  The
email is sent as a multi-part message with both HTML and plain text versions included.  Both
versions are developed automatically based on the markdown message provided.

The script uses a configuration file to set the various options, with command line options to
override the configuration file as required.  The user is prompted to provide confirmation for
any warnings and before any mail is sent.  There is an option for disabling the confirmations
which allows for unattended batch operation, if desired.  The script provides error checking
and specific error exit codes for each type of error.

In addition to the full mail processing, there is also a `test` mode provided to confirm the
settings and connection to the specified mail server.

There is an optional logging function to capture the information from each session, with various
levels of information logging available.

## Requirements

The script required Python 3, along with a few function libraries.  Required standard libraries
include:

- argparse
- csv
- datetime
- email
- os
- re
- smtplib
- textwrap
- time

Required third-party libraries include:

- commonmark
- html2text

All third-party libraries are available for installation using `pip`.

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

## Command Line

The script is run from the command line as:

    bulkmail.py -h|--help

or

    bulkmail.py -c|--cmd command [options]

where **command** is either `send` or `test`.

The options available include:

- **-a,--confirm**: Request confirmation on actions or warnings.
- **-A, --no-confirm**: Don't request confirmation on actions or warnings.
- **--addr_file FILE**: The file containing a list of destination addresses in CSV format with the first row containing the column names.
- **--config-file FILE**: The file containing the configuration information.  Defaults to bulkmail.cfg in the current directory.
- **--display-level LEVEL**: The amount of information to write to the display.  0=no display (also implies -A) to 3=display everything (debug)
- **--email TEMPLATE**: Set the template to use to build the destination email addresses from the fields in the CSV file. (e.g.: `'{first_name} {last_name} <{email}>'`)
- **--from ADDRESS**: Set the From: address.  (e.g.: `'Joseph Blow <j.blow@address.com>'`)
- **--log-file FILE**: The file to write the session logs.  Defaults to bulkmail.log in the current directory.
- **--log-level LEVEL**: The amount of information to write to the log file.  0=no logging; 1=errors; 2=normal; 3=debug; 4=everything (extreme debug)
- **--message FILE**: The file containing the message (in markdown format) to send. The first line contains the message subject formatted as a Header 1. (e.g.: `# This is the Subject`)
- **-r, --send-reply**: Include the Reply-To address in all messages sent.
- **-R, --no-reply**: Do not include the Reply-To address.
- **--reply ADDRESS**: Set the Reply-To: address.  (e.g.: `'No Spam <nospam@nospam.com>'`)
- **--server-url SERVER**: The URL of the mail server. (e.g.: `smtp.myserver.com`)
- **--server-port PORT**: The port to use on the mail server. (e.g.: `587`)
- **--subject SUBJECT**: The message subject line to use.  Overrides the subject line extracted from the markdown message template file.
- **--wait SECONDS**: Number of seconds to wait between sending messages.
- **--warranty**: Show the warranty information and exit.

## Address File

The list of destination addresses is read from a CSV file, with field (column) names provided on the first line. The
file can contain any number of fields of information, providing that each field has a unique name.  A typical address
file might look like:

    user_id,first_name,last_name,email
    joe,Joseph,Blow,j.blow@somewhere.com
    ready_freddy,Fred,Bloggs,ready_freddy@example.com
    ...

The field names are used to map the information on each line of data to corresponding replacement parameters in the
markdown message template and the ADDRESS_TEMPLATE.  The replacement parameter fields are simply the field name
enclosed in curley braces.  (e.g.: {first_name})  Before sending an email message, all occurrences of the replacement
parameter fields are replaced by the content of the field column corresponding to the parameter name.  Note that this
replacement happens in the To: address template specified in the ADDRESS_TEMPLATE setting as well as both the HTML
and plain text parts of the message.

## Message File

The message file used as the template for each message sent is provided in markdown format following the CommonMark
standard.  This allows the user to develop the formatted message easily using their favorite markdown editor.  The
script will automatically generate the HTML and plain text portions of the messages sent based on the template
provided.

The first line of the template should be the message subject, formatted as a level 1 header.  (e.g.: `# This is the message subject`)

The template should also include any parameter fields that should be replaced with information from the address file.

A sample message file might look like:

```md
# Bulk Mail Test Message

Dear {first_name},

This is a test of the **Bulk Mail** message script.

You can include a [link](https://github.com/rdswift) and it is available in both HTML
and plain text versions of the message.

This should be a new paragraph with *italic*, **bold**, and ***both***.

This should be a list:

- one
- two
- three

That's all for now.
```

## Error Codes

The following error and warning codes are provided by the script:

- 100: No processing command specified.
- 101: Error accessing the configuration file.
- 102: Invalid key in the configuration file.
- 103: Invalid setting in the configuration file.
- 104: Invalid setting on the command line.
- 105: Error accessing the address file.
- 106: Address file does not appear to have a header row.
- 107: Address list appears to be empty.
- 108: Error accessing the message file.
- 109: Missing email address template.
- 110: No fields in email address template.
- 111: Unknown field(s) in email address template.
- 112: Error accessing the message file.
- 113: Message appears to be blank.
- 114: Error connecting to the mail server.
- 115: Error sending one or more messages.
- 116: Unknown field(s) in email message template. (Warning)
- 117: Missing or invalid log file name.
- 118: Unable to write to the log file.

## License

    ##############################################################################
    #                                                                            #
    #   Bulk Mail - A bulk mail / mail merge system using Python 3               #
    #   Copyright (C) 2019 Bob Swift (rdswift)                                   #
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

## Developer Notes

Although functional, this script is far from complete or polished.  It has not been reviewed for
PEP8 compliance, and has not been optimized.  The intent so far has been to make it available
quickly for immediate use, and follow up with additional features, optimization and PEP8 review.

Improvement suggestiona and bug reports are greatly appreciated, and can be reported in
the [Issues](https://github.com/rdswift/bulkmail/issues) section of the
[GitHub repository](https://github.com/rdswift/bulkmail).  Thanks.
