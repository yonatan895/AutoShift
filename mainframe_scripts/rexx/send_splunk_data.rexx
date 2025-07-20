/*
 * Gather system information and send to Splunk using FTP.
 * Replace placeholders with actual dataset names and credentials.
 */
trace off

data = SYSVAR('SYSNAME')
address TSO
"ALLOC F(INFILE) DA('USER.DATA(SYSINFO)') SHR REUSE"
"EXECIO * DISKR INFILE (STEM L.)"
"FREE F(INFILE)"
address FTP "OPEN splunk.example.com"
address FTP "USER user password"
address FTP "QUOTE SITE FILETYPE=JES"
address FTP "PUT 'USER.DATA(SYSINFO)'" "HEC_TOKEN=yourtoken"
address FTP "QUIT"
