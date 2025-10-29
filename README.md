# phangs2caom2
An application to generate CAOM2 Observations for [PHANGS](https://public.nrao.edu/news/2019-alma-phangs/) observations.

# How to run the phangs2caom2 pipeline

This container will find all files ending in '.fits' or '.fits.gz', and will attempt to store them at CADC in the PHANGS archive. This container will also create CAOM2 records for the PHANGS collection based on the metadata from these files.

These instructions assume a linux-type environment, with `bash` syntax.

In a directory (the 'working directory'), on a machine with Docker installed:

1. This is the working directory, so it should be where the .fits/fits.gz files are located.

1. Set up credentials. A CADC account is required (you can request one here: 
http://www.cadc-ccda.hia-iha.nrc-cnrc.gc.ca/en/auth/request.html) In this directory, run the following command:

   ```
   user@dockerhost:<cwd># docker run --rm -ti -v ${PWD}:/usr/src/app --name phangs_run opencadc/phangs2caom2 cadc-get-cert --days-valid 10 --cert-filename ./cadcproxy.pem -u canfarusername
   Password: canfarpassword
   ```

   This will create the the proxy certificate credentials required for the 
   CADC services. These credentials allow the user to read, write, and delete 
   CAOM2 observations, and read and write file header metadata and files.
   
   1. Replace canfarusername and canfarpassword with your CADC username and 
   password values.

   1. The name and location of this file may be changed by modifying the 
   `proxy_file_name` entry in the `config.yml` file. This entry requires a 
   fully-qualified pathname.

1. Get the script that executes the pipeline by doing the following:

   ```
   wget https://raw.github.com/opencadc-metadata-curation/phangs2caom2/master/scripts/phangs_run.sh
   ```

1. Ensure the script is executable:

    ```
    chmod +x phangs_run.sh
    ```

1. To run the application:

    ```
    ./phangs_run.sh
    ```

1. To debug the application from inside the container:

   ```
   user@dockerhost:<cwd># docker run --rm -ti -v <cwd>:/usr/src/app --name phangs_run opencadc/phangs2caom2 /bin/bash
   root@53bef30d8af3:/usr/src/app# phangs_run
   ```

1. For a description of the `config.yml` file, see: https://github.com/opencadc-metadata-curation/collection2caom2/wiki/config.yml

1. For some instructions that might be helpful on using containers, see:
https://github.com/opencadc-metadata-curation/collection2caom2/wiki/Docker-and-Collections

1. For some insight into what's happening, see: https://github.com/opencadc-metadata-curation/collection2caom2
