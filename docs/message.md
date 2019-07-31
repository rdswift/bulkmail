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

You can include a [link](https://github.com/rdswift) and it is
available in both HTML and plain text versions of the message.

This should be a new paragraph with *italic*, **bold**, and ***both***.

This should be a list:

- one
- two
- three

Thanks to my friend Nicolás for suggesting I write something like this.

That's all for now.

Bob
```

---
