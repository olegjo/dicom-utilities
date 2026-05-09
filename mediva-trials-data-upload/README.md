# Introduction
This folder is here to support uploading data to trial instances of nordicMEDiVA.

This is by far not the best way to do it, but it's working.

# Pre requisites
You need docker installed on your native system

# Preparation

Get the credentials
1. Create a file calles gitignore__destinations.py
Populate the file with the credentials. Example
```
destinations = {
    "trial3": {
        "MEDIVA_URL": "https://trial3.us.trials.nordicmediva.com",
        "CLIENT_SECRET": "cSiAMDzZZvxGJUzQumLnf9J4OdiUULnX"
    },
```

Create the docker images.

1. Change directory into the current directory (`mediva-trials-data-upload`)
2. Build the docker images:

```
sudo docker build -t tria3-upload .
```

3. Run the docker image
```
docker run --rm -it -v $(pwd):/data tria3-upload
```

# Next steps
Create a docker hub repository and instructions for people to download the dockers from there.
For exaomple, they can download trial3 upload image, and use that to upload images to trial3.

It's not perfect, but it works.
