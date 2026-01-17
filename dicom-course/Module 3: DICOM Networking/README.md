# Purpose
In this module, the learner should
* Understand the DICOM network protocol (excluding DICOM Web, which will be covered in another module)
* Know about the negotiation mechanism to a basic level
* Know about DICOM Store SCP vs DICOM Store SCU, DICOM Q/R, and DICOM Echo
* Understand and be able to use the DICOM Send and DICOM Echo protocols

# Topics
You've now, hopefully, gained an understanding in what the DICOM file is and how it is constructed.

In this section, we will talk about the other part of DICOM, namely networking. DICOM is not only a standardized format for conveying medical data, but it also describes the network protocol for how this data shall be transmitted.

The traditional way of transmitting data is called the `DICOM Message Service Element` or DIMSE. This is still the most common protocol and it's what's used when transferring DICOM data between MR scanner, PACS and other DICOM nodes on the hospital network.

Even though the DICOM DIMSE protocol allows encryption of the network traffic, encryption is very seldom used in practice. Largely due to healthcare institutions using dated systems, and even newer health IT systems not supporting DICOM DIMSE encryption.

However, the DICOM standard has in later years adopted more modern protocols such as HTTP. When DICOM is transferred over HTTP, the protocol is called DICOM Web. The DICOM Web protocol can easily be encrypted using over HTTPS.

## DICOM Network Basics
To send a DICOM file from A to B, both systems A and B must implement the DICOM protocol, and be connected to the same network.

When the systems A and B are DICOM compatible, they are called **Application Entities**. Each Application Entity is assigned an **Application Entity Title**, a alphanumerical value of max 16 characters, which must be unique on the local network.

Since both A and B are connected to the network, they have also been assigned an **IP address**. If they accept incoming DICOM traffic, they will also be exposing, or have open, a **network port**. The most common ports for DICOM traffic are 104 and 11112.

To summarize: to allow for incoming DICOM traffic, a DICOM node must
* Be connected to a network and have an IP Address
* Have an Application Entity (AE) Title
* Have a port open for incoming DICOM traffic.

## Types of application entities
Above, we talked about application entities (AEs), and that they are DICOM nodes that exist on a network.

However, consider the situation where you have one AE "A" that can only send DICOM data (and not receive), and another "B" that can only receive (and not send). This could be a primitive version of a scanner <> PACS relationship.

It is clear that we need terminology to distinguish these use cases.

This is handled in DICOM, by defining "Service Class User" and "Service Class Provider".

This will be described in more detail below.

## DICOM Network commands
A DICOM node can execute a number of network "commands", or DIMSE services, accepted by the DICOM standard. These include:

* C-STORE: used for STORING DICOM images at another network location. I.e., sending DICOM data from A to B.
* C-ECHO: used for checking the status of another DICOM network node. Similar to "ping".
* C-FIND: used to query another DICOM node for what DICOM data it has.
* C-MOVE: used to move DICOM data from one DICOM node to another. This is different from C-STORE in that C-MOVE will assume that the data is deleted from the originating location.
* C-GET: used to GET DICOM data from another location. Usually followed by a C-FIND.

## Examples on DICOM network configurations
### Example 1
![](./diagrams/SimpleDicomDiagram1.drawio.svg)

In the example above, the MR Scanner sends DICOM data to PACS. In this situation the action that is performed is C-STORE because the DICOM data is sent from the scanner to PACS.

In this situation, the scanner acts as a C-STORE **Service Class User (SCU)** because it **uses** the storage capability of the PACS.

Likewise, the PACS act as a C-STORE **Service Class Provider (SCP)** because it **provides** the storage capability.

## The DICOM negotiation process
Before any DICOM data can be exchanged, two systems must agree on how they will communicate. This agreement happens during the association negotiation phase.

When a DICOM client initiates a connection, it sends an Association Request to the remote system. This request includes:
* The calling AE Title (who is connecting)
* The called AE Title (who it wants to talk to)
* A list of presentation contexts
* A presentation context defines:
* A SOP Class (what kind of data or service is requested)
* One or more Transfer Syntaxes (how the data is encoded)

The receiving system reviews the request and responds by:
* Accepting or rejecting the association
* Accepting or rejecting each presentation context
* Selecting exactly one transfer syntax per accepted context

Only accepted presentation contexts can be used during the association. If a requested SOP Class or transfer syntax is not accepted, any attempt to use it will fail—even though the network connection itself may be established.

## Using DCMTK
DCMTK (DICOM ToolKit) is a very useful tool to work with DICOM, including networking. 

It can be downloaded from the internet [here](https://dicom.offis.de/en/dcmtk/dcmtk-tools/).

Once installed, you'll have several command line tools available from a terminal window.

The most useful are:

### Echoscu
```
echoscu -v -aec AE_TITLE peer port
```

for example

```
echoscu -v -aec MEDIVA 192.168.134.22 11112
```

### dcmsend
For example
```
dcmsend +sd -v +r  192.168.134.22 11112 .
```
