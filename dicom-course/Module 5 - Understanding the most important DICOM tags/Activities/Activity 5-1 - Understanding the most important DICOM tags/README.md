# Activity 5-1: Understanding the most important DICOM tags

## Exercise 1 - SeriesInstanceUID
1. In the DICOM folder related to this activity, there is a single DICOM file.
2. Send this DICOM file to nordicMEDiVA
3. Make sure you can see it in nordicMEDiVA and that you can load it in the viewer.
4. Now, inspect the DICOM header of the DICOM file. What's the SeriesInstanceUID?

On your local machine:
1. Open a terminal and cd into the folder you created above
2. Change the SeriesInstanceUID of the DICOM file using the `dcmodify` tool.
   1. Food for thought: How can you define a new value for the UID?
3. Send the DICOM file, with updated SeriesInstanceUID to nordicMEDiVA.
4. What happened? Can you explain?

## Exercise 2 - Study tags
In this exercise, edit the SeriesInstanceUID to something new and unique (like above), but also change the StudyInstanceUID and StudyDescription.

Observe and try to explain what you see.

## Exercise 3 - Knock yourself out and experiment with other tags
As you should have understood by now, nordicMEDiVA (and indeed other systems) will interpret a DICOM file as part of a new series, as long as the SeriesInstanceUID tag is different.
