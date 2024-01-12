# Bulk Mail (v0.7)

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

Please see the USER_GUIDE.md file or the [Bulk Mail website](https://rdswift.github.io/bulkmail/)
for more information.

## Developer Notes

Although functional, this script is far from complete or polished.  It has not been reviewed for
PEP8 compliance, and has not been optimized.  The intent so far has been to make it available
quickly for immediate use, and follow up with additional features, optimization and PEP8 review.

Improvement suggestions and bug reports are greatly appreciated, and can be reported in
the [Issues](https://github.com/rdswift/bulkmail/issues) section of the
[GitHub repository](https://github.com/rdswift/bulkmail).  Thanks.
