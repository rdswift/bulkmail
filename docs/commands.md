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
- **-f, --footer**: Include a footer in the message indicating the version of the Python Bulk Mail script used.
- **-F, --no-footer**: Do not include a footer in the message indicating the version of the Python Bulk Mail script used.
- **-r, --send-reply**: Include the Reply-To address in all messages sent.
- **-R, --no-reply**: Do not include the Reply-To address.
- **--reply ADDRESS**: Set the Reply-To: address.  (e.g.: `'No Spam <nospam@nospam.com>'`)
- **--server-url SERVER**: The URL of the mail server. (e.g.: `smtp.myserver.com`)
- **--server-port PORT**: The port to use on the mail server. (e.g.: `587`)
- **--subject SUBJECT**: The message subject line to use.  Overrides the subject line extracted from the markdown message template file.
- **--wait SECONDS**: Number of seconds to wait between sending messages.
- **--warranty**: Show the warranty information and exit.

---
