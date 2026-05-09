# Activity 5-2: Using a utility script to modify all tags and create a "new" patient

In this activity, you'll use a utility script to change the DICOM tags in a DICOM study, such that the series will be interpreted as another patient.

## Exercise 1
1. Delete all data you already have in nordicMEDiVA - to have a clean start
2. Copy a full DICOM study (a single patient with several series) into a dedicated folder to be used in this exercise
3. Run the script `modify-to-new-patient.py` in this repository and give the path of the folder you created above as an argument. 
4. Use `dcmsend` to send the folder to nordicMEDiVA
5. Repeat step 3 and 4 to make yourself comfortable with using the script.

> Discuss: check out the script. What tags does it affect?
