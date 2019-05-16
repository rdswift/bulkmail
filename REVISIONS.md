# Bulk Mail Revision History

## Version 0.04 (2019-05-16)

- Fixed bug that was preventing --cmd processing.
- Add message encoding to allow unicode characters in the message body.

## Version 0.03 (2019-02-27)

- Project moved to GitHub.
- License changed from GPLv2 to GPLv3.
- Added --warranty option as suggested by GPLv3 license.
- Added copyright notice at script interactive startup as suggested by GPLv3 license.
- Added revision history in the form of a REVISIONS.md file.

## Version 0.02 (2019-02-26)

- Major rewrite and initial code cleanup.  Considerable cleanup and optimization work remains.
- Use markdown format message file and automatically develop the HTML and plain text versions sent as a multi-part message.
- Use CSV address file for destination addresses list.
- Use plain text configuration file for initial settings.
- Add command line options to override the initial settings.
- Add replaceable parameters processing to allow personalizing the messages sent.
- Add options for logging processing sessions, including various levels of information logged.
- Add options for various levels of processing information displayed in the terminal.
- Add user confirmation to proceed after warnings, and before sending any email messages.  This can be disabled with a command line option to allow unattended batch operation.
- Add error handling and error return codes.
- Added documentation in the form of a README.md file.

## Version 0.01 (2019-02-18)

- Initial release for private testing and use.
