# Activity: Practical DICOM - Creating your own DICOM listener!

In this activity, you will create a simple DICOM listener on your own computer, and make simple interactions with it.

The goal of this exercise is that you understand a bit more about what goes on in a DICOM association.

# Setup

1. Open a terminal window (PowerShell on Windows)
2. Change directory into the folder containing this file (it has a pre-set folder structure to help the rest of the exercises)
3. Open another terminal window and repeat do the same change of directory. Keep both terminal windows open.
4. In the first terminal window, run the command `storescp -od output -v -aet TEST 8080`

# Exercise 1
In the second terminal window, run `echoscu -v localhost 8080`

> Discuss: 
> 
> * What does this command mean? 
>   * What does "echoscu" mean?
>   * What does it mean that we put `-v`
>   * What does the `localhost` `8080` arguments mean?
> * Check the output in the terminal in the storescp. It should be similar to the below. Discuss the what happens
>   ```
>   I: Association Received
>   I: Association Acknowledged (Max Send PDV: 16372)
>   I: Received Echo Request (MsgID 1)
>   I: Association Release
>   ```

# Exercise 2
Still using the second terminal window, execute now
```
dcmsend localhost 8080 dicom/IM-0001-0001.dcm
```

> Discuss:
>
> * What does this command mean?

This command will send the dicom file located at `dicom/IM-0001-0001.dcm` to the DICOM Store SCP we created earlier.
You should now see a file appeared in the `output` folder. **Do you?**

## Exercise 2a
In the previous example we sent a single DICOM file to our local DICOM Store SCP.

However, the `dcmsend` command accepts a number or arguments, including sending entire directories/folders.

Explore the `dcmsend` command's documentation and edit the <options> section ONLY to make the following command work. The goal is to be able to send all the files inside the `dicom` directory to our local DICOM SCP.
```
dcmsend <options> localhost 8080 dicom
```
