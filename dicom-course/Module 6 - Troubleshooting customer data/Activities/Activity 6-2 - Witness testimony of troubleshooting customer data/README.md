# Activity 6-2: Witness testimony of an account from January 21st 2026

Dear reader,

On January 21st 2026, I received some data from a customer who wanted to have a demo and try to use their own data.

We tried to upload the data using nordicBrainEx, and the `dcmsend` command, but nothing worked. 

What's more peculiar is that it appeared that most of the data was uploaded successfully to nordicMEDiVA.

Below is an excerpt of the terminal output of the command.

```
> dcmsend +sd -v +r 3.16.165.155 11112 201
[...]

I: Sending C-STORE Request (MsgID 51, MR)
I: Received C-STORE Response (Success)
I: Sending C-STORE Request (MsgID 52, MR)
I: Received C-STORE Response (Success)
I: Sending C-STORE Request (MsgID 53, MR)
I: Received C-STORE Response (Success)
E: No presentation context found for sending C-STORE with SOP Class / Transfer Syntax: 1.3.46.670589.11.0.0.12.2 / Little Endian Explicit
F: cannot send SOP instance: DIMSE No valid Presentation Context ID
I: Aborting Association
```

This error indicates that there is an issue with the Transfer Syntax. However, nordicMEDiVA does support Little Endian Explicit!
Moreover, the UID given in the error message, is not a valid transfer syntax (google it).

Nevertheless, I thought a good first step was to check if all files in the directory had the same transfer syntax.

## Investigation 1 - no results
So I created a python script called `check_transfer_syntax.py`. This script will use the `pydicom` library and go through all the files in the problematic 
folder. Then it will print out the value of the Transfer Syntax UID DICOM tags. These should all be the same"

Here is an excerpt of the execution of that script

```
❯ python3 check_transfer_syntax.py dicom/201
[...]
Transfer syntax was 1.2.840.10008.1.2.1 for file dicom/201/26.dcm
Transfer syntax was 1.2.840.10008.1.2.1 for file dicom/201/32.dcm
Transfer syntax was 1.2.840.10008.1.2.1 for file dicom/201/127.dcm
Transfer syntax was 1.2.840.10008.1.2.1 for file dicom/201/133.dcm
Transfer syntax was 1.2.840.10008.1.2.1 for file dicom/201/132.dcm
Transfer syntax was 1.2.840.10008.1.2.1 for file dicom/201/126.dcm
Transfer syntax was 1.2.840.10008.1.2.1 for file dicom/201/33.dcm
Transfer syntax was 1.2.840.10008.1.2.1 for file dicom/201/27.dcm
All transfer syntaxes were the same
```

So this was a dead-end for me. All transfer syntaxes were the same, and moreover, they all had the value `1.2.840.10008.1.2.1` which stands for `Explicit VR Little Endian` ([check DICOM standard](https://www.dicomlibrary.com/dicom/transfer-syntax/)).

## Investigation 2 - success
When the first investigation failed, I thought I would go in from a different angle.

Since the error message was
```
E: No presentation context found for sending C-STORE with SOP Class / Transfer Syntax: 1.3.46.670589.11.0.0.12.2 / Little Endian Explicit
```
I knew, I was looking for the UID `1.3.46.670589.11.0.0.12.2`. 

So, then I created a new script, `find_mystery_uid.py`.

This script will, again, go through all the files in the given folder. Now, it'll check if any of the file's DICOM headers contains the mysterious UID...

Running the script gives the following excerpt:
```
❯ python3 find_mystery_uid.py dicom/201
[...]
Checking file... dicom/201/201.dcm
Checking file... dicom/201/215.dcm
(0002,0002) UI [1.3.46.670589.11.0.0.12.2]              #  26, 1 MediaStorageSOPClassUID
(0008,0016) UI [1.3.46.670589.11.0.0.12.2]              #  26, 1 SOPClassUID
Checking file... dicom/201/214.dcm
Checking file... dicom/201/200.dcm
[...]
```

Ah! Success. It seems that the file `215.dcm` contains the mysterious UID, and it's been put into the SOPClassUID tag! 

I'll stop here, an encourage a discussion what this means.
