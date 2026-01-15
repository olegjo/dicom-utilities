# Purpose

The learners should understand
* The difference between a DICOM file and the DICOM protocol
* DICOM is a standard for transferring medical imaging, but also other data
* Where to find the DICOM standard

# Topics

## The Difference Between a DICOM File and the DICOM Protocol
DICOM is often spoken about as if it were a single thing, but in practice it covers two distinct (but related) aspects:

### DICOM Files
A DICOM file is a standardized file format used to store medical data.
It typically contains:
* **Metadata – DICOM Header** (patient, study, acquisition, geometry, etc.)
* **Pixel data** (for images) or other structured content

A DICOM file:
* Is usually stored on disk
* Can be opened without any network connection
* Uses tags, value representations (VRs), and transfer syntaxes to encode data

You can think of a DICOM file as a **self-describing container** for medical data.

### DICOM Protocol (DICOM Networking)
The DICOM protocol defines how systems communicate over a network.

It specifies:
* How two systems establish a connection (association)
* How they agree on what kind of data they can exchange
* How data is sent, queried, or retrieved

Examples of protocol operations include:
* Verifying connectivity (C-ECHO)
* Sending images (C-STORE)
* Querying studies (C-FIND)
* Retrieving data (C-MOVE, C-GET)

A key point:

> You can use DICOM files without DICOM networking, and DICOM networking always transfers DICOM data objects (not arbitrary files).

## DICOM Is More Than Just Images
DICOM is widely associated with medical images such as MR, CT, X-ray, and ultrasound—but the standard goes far beyond image storage.

DICOM defines how to represent and transfer:
* **Images** (2D, 3D, multi-frame)
* **Structured Reports (SR)** – machine-readable clinical measurements and observations
* **Radiation Dose information**
* **Waveforms** (e.g. ECG)
* **Segmentations and annotations**
* **Presentation states** (how images should be displayed)
* **Encapsulated documents** (e.g. PDFs)

This means:
* Not every DICOM object contains pixel data
* Some DICOM objects exist purely to describe, measure, or reference other data

For us at NNL, the most important DICOM object representations to know about are images (more on this later).

## Where to Find the DICOM Standard (M1)
The official DICOM standard is published by **DICOM Standards Committee (NEMA)** and is freely available online.

### Official Website
The authoritative source is: https://www.dicomstandard.org 

From there you can access:
* The complete standard, organized into multiple parts
* Current and historical versions
* Supplements and corrections (for example the tractography suplement)

You are not expected to read the entire standard end-to-end. In practice:
* Most people consult specific parts as needed
* Vendors and tools often implement subsets relevant to their use case

### Practical Advice
* Treat the standard as a reference, not a tutorial
* Expect real-world DICOM to be valid but inconsistent
* Use the standard to answer precise questions, not to infer behavior

### Alternative references
The DICOM standard document is notoriously hard to read, and in most cases, you will spend a lot of time finding and understanding the informatino than is useful. Instead, use the following references:
* Innolitics DICOM reference – for checking DICOM tags, their meaning, usage and limitations

# Key Takeaways
* A DICOM file is a data container; the DICOM protocol defines network communication.
* DICOM covers images and many other types of medical data.
* The full DICOM standard is publicly available and extensive—knowing where to look is more important than memorizing it.
