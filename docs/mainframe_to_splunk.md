# Mainframe Data Collection and Splunk Integration

This document outlines a minimal approach to gather information on a z/OS system and forward it to Splunk's HTTP Event Collector (HEC).

## Overview

1. **Collect data using REXX or assembler.**
2. **Trigger via JCL.**
3. **Send the resulting dataset using FTP with the HEC token.**

## Sample REXX Script

The example `mainframe_scripts/rexx/send_splunk_data.rexx` reads a dataset and uploads it to Splunk using FTP.
Replace the dataset name, credentials, and host as needed.

```rexx
/* See: mainframe_scripts/rexx/send_splunk_data.rexx */
```

## Sample JCL

`mainframe_scripts/jcl/SENDSPLU.JCL` demonstrates how to execute the REXX routine.

```jcl
//SENDSPLU JOB (ACCT),'SEND SPLUNK',CLASS=A,MSGCLASS=X,NOTIFY=&SYSUID
//STEP1   EXEC PGM=IRXJCL,PARM='SEND_SPLUNK_DATA'
//SYSEXEC DD DISP=SHR,DSN=USER.REXX.LIB
//SYSTSPRT DD SYSOUT=*
//SYSTSIN  DD *
  %SEND_SPLUNK_DATA
/*
```

## ASM Helper

The assembler file `mainframe_scripts/asm/GETSYSIN.ASM` can be assembled and linked to produce a load module that collects system information.

## Pipeline

The GitHub Actions workflow in `.github/workflows/ci-cd.yml` runs tests and builds Docker images. Adjust the workflow to fit your environment.
