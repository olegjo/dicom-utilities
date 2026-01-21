# Recovering data provided by a customer

## Introduction
DICOM is hard, and you know it. Very often, when we get data from customers it comes in a format that's very hard to work with, and in a format that nordicMEDiVA doesn't understand, even though the scanner allows the format.

In this activity, you will try to recover the data such that it is possible to process in nordicMEDiVA by changing certain tags within the dataset.

This is a very advanced case. **I** have not been able to recover all cases yet, despite trying many things.

## Data
The data provided in this activity was provided by a real customer for a trial. The patient name, patient birth date, Series instance UID, Study Instance UID and SOP Instance UID tags have been changed, but otherwise the folder structure and contents have been kept identical to how we received it from the customer.

## Task
Take the data attached to this activity. Investigate it, and make necessary modification to the header information such that all DICOM series are recognized by nrdicMEDiVA to the extent that you can process them in an appropriate pipeline and/or open in the viw

## Expected results
If completed successfully, you should, after recovering this data, have the following series in the viewer:
* OH-Test-1:
  * T1 MPRAGE AX
  * 3D T2 FLAIR SAG
  * ep2d_bold_moco
  * Diffusion Tensor Imaging DTI 30 Directions
  * Resting State - TR2500 - p2 (600 measurements)
  * Diffusion Tensor imaging DTI 30 Directions
* OH-Test-2:
  * T1 MRPAGE Ax
  * 3D T2 FLAIR SAG
  * ep2d_bold_moco_1
  * AX T2 TSE - 64
  * Diffusion Tensor Imaging DTI 30 Directions
* OH-Test-3:
  * T1 MPRAGE AX
  * ep2d_bold_moco
  * ep2d_bold_moco_1555
  * 3D T2 FLAIR SAG
  * Resting_state_TR2500_p2_600measurements
  * DTI_30_dir
