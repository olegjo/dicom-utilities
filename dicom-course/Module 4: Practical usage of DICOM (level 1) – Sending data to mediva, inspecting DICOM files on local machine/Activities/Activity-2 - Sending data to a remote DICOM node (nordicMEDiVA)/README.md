# Activity - Sending data to remote DICOM node

In this activity, we will send some data to an instance of nordicMEDiVA. In doing so, we will try to find out some concepts about the DICOM header and how nordicMEDiVA interprets, and uses the tags to sort data.

## Exercises
Before you do these exercises, identify the IP, port and AE title of a nordicMEDiVA you have access to.

<!--
The purpose of this exersise is to upload a single file from a single-frame series, and a single file from a multi-slice, and a sincle file from a mosaic series. The lerner should discuss and understand the differences.
-->
1. Check out the DICOM files attached to this activity. You should see 3 different folder, each with a single DICOM file. One Enhanced MR, one "normal" MR DICOM and one using the mosaic format.
2. Open the DICOM header of each of these files. How can you identify their format based on the information in the header?

We will now send each of the three DICOM objects to nordicMEDiVA. But before we do that, can you anticipate how they will be presented in the 3D viewer?

### Send the data to nordicMEDiVA
1. Use the `dcmsend` command line tool and send to nordicMEDiVA:
   1. the EnhancedMRImageStorage object
   2. the MRImageStorage object
   3. the MRImageStorage-mosaic object
2. Open the patient named "DICOM-COURSE-ACTIVITY-4.2" in the nordicMEDiVA viewer.

> Discuss:
> * what are the differences between these three images?
> * How are their DICOM representation different? 
> * What are the benefits and drawbacks of each representation?
> * What's special about the mosaic data?


