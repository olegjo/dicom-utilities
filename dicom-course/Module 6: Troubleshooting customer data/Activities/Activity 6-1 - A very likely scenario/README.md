# Activity - A very likely scenario

## Preamble
When we speak with prospective customers, more often than not, the customer will ask for a trial. Often, they would also like to try the software using their own data. Our process for doing this is that the customer provides us with anonymized, or de-identified data, and we upload it to an AWS instance dedicated to trials.

In this exercise, we'll look at an example of what can go wrong in this process, and try to understand what happened, why it went wrong, and how we can fix it.

## Step 1 - Uploading the first patient to nordicMEDiVA
Imagine Jennifer has a customer, let's call them "Customer 1". You received some DICOM data from this customer, and put it in the folder `dicom/Customer_1_data`.

* Upload this data to nordicMEDiVA, and check that you received it. Open the data in the viewer.

## Step 2 - Uploading another patient to nordicMEDiVA
It's now gone a month's time, and Jennifer has another customer, "Customer 2". She provides you with data from this customer, and you put it in the folder `dicom/Customer_2_data`.

* Upload this data to nordicMEDiVA. 

What happened? - Discuss.

## Step 3 - Fixing
Can you come up with a solution on how to fix this? Try it out! The end result should be that you have two separate patients in the viewer, with the correct data associated with each patient.
