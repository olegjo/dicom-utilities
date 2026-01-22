# Activity - modifying DICOM tags and seeing how they affect how the data is presented

## Exercise 1
In this exercise, we will modify some DICOM tags and see how it affects how the data is displayed.

1. Delete all data you already have in nordicMEDiVA - to have a clean start
2. Copy a full DICOM study (a single patient with several series) into a dedicated folder to be used in this exercise
   1. A suggestion is to use the T1 from NNL25
3. Change the number of rows in the header: `dcmodify -m "(0028,0010)=200" -nb $(ls)`
4. Send it to nordicMEDiVA and open it. What's changed?

Repeat steps 3 and 4, for each of the following. For each change, delete the data from nordicMEDiVA before sending, then send the modified data, and observe the effects.

* `dcmodify -m "(0028,0030)=2\\2" -nb $(ls)`
* `dcmodify -m "(0018,0088)=10" -nb $(ls)`

## Exercise 2
1. upload the series you used in the previous exercise to nordicMEDiVA.
2. Now, change the series instance UID such that it's different than it was.
3. Upload the modified data.
4. Check the viewer. What changed?
