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

---
