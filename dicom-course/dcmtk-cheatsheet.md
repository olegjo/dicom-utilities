# DCMTK Cheat Sheet

## 1. Inspecting a DICOM file's header

### Print out the full DICOM header to the terminal
```
dcmdump image.dcm
```

### Print out a specific DICOM tag
Works on both Windows and Mac/Linux
```
dcmdump +P "PatientName" image.dcm
```

Works on Mac/Linux only
```
dcmdump image.dcm | grep PatientName # Only Linux/Mac
```

## 2. Sending DICOM data
### Send a single file

*Use the `-v` argument for verbose output.*
```
dcmsend -v 192.168.134.22 11112 image.dcm
```

### Send all DICOM files in a folder
*The folder must contain **only** DICOM files. Delete all other files.*
```
dcmsend -v +sd +r 192.168.134.22 11112 path/to/folder
```
* `-v` means verbose output
* `+sd` means "scan directories". Needed when sending the entire directory
* `+r` means "recursive". Will tell `dcmsend` to look through all sub folders, and send DICOM files there too.

### Deleting MacOS files in all sub-directories
Often, MacOS will create hidden files that cause errors with `dcmsend`. Here's how to delete them.

*Works on MacOS/Linux.*
```
find . -type f -name '.DS_Store' -delete
```

## 3. Echoing
```
echoscu -v 192.168.134.22 11112
```
With more arguments

```
echoscu -v -aet MYSELF -aec REMOTE 192.168.134.22 11112
```
* `-v` means verbose output
* `-aet` means the the AE title we're giving outselves
* `-aec` is the AE Title of the remote DICOM node

## 4. Specific to nordicMEDiVA

|   |   |
|---|---|
| Default port when nordicMEDiVA is deployed on-prem or SaaS using VPN (legacy)  | 11112  |
| Default inbound DICOM port for the nordicDicomGateway  | 4242  |

