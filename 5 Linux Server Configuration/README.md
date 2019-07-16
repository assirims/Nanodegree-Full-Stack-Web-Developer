# Linux Server Configuration

### Project Description

This is the third project in the Udacity Full-Stack Nanodegree. The project takes a baseline installation of a Linux Distribution and prepare it to host web applications, including installing updates and securing it from a number of attack vectors.

- IP Address: 54.93.190.254

- Accessible SSH port: 2200

- SSH Connection: ssh -i ~/.ssh/[keyFile] grader@54.93.190.254 -p 2200

This summary will hopefully walk you through all the steps you need to secure your server, install dependinces and get your web application up and running in no time!

# Walkthrough Steps

### 1. The Baseline Installation of a Linux Distribution, Securing it, and Creating Users

## Step 1: Get an Amazon LightSail Server

[Follow the link to start up your own LightSail Server](https://aws.amazon.com/)

1. Sign up to the Amazon Service
2. Once logged in, under **Build a solution tab**, click **Build using virtual servers with LightSail**
3. Create your instance:

    a. Leave the Instance Location as the default (unless you want to change it! Go ahead!)

    b. Select **Linux/Unix** under the **Pick your instance image**

    c. Click **OS Only** and select **Ubuntu 16.04 LTS**

    d. Select the lowest tier of the payment plans. If you complete the project within a month and shut it down, the price is zero anyway!

    e. Give your instance a hostname. Can be anything you want.

    f. Wait for it to start up. Once it says running, you're in business!

## Step 2: Configure LightSail Firewall

Before anything, make sure you configure your server firewall to allow the non-default port number.

1. Click on your instance name
2. Click on **Networking**
3. Under **Firewall**, click **Add Another**
4. Keep everything as default and simply enter the port number **2200**
5. Click Save

Now you are ready to start configuring your instance!

## Step 3: Update, Secure!

1. In the same line as **Networking**, click on **Connect**
2. Click the shiny orange button **Connect using SSH**

You are now inside your instance using the LightSail terminal!

3. Run the following commands:

    ```
    sudo apt-get update
    sudo apt-get upgrade
    sudo apt-get autoremove
    ```

This will ensure your instance is updated to the latest version of its packages.

4. Run the following command:

    `sudo nano /etc/ssh/sshd_config`

Around line 5-6, change **PORT 22** to **PORT 2200**

Save the file: `CTRL + X Y Enter`

Now its time to configure the Uncomplicated Firewall (UFW)** to only allow incoming connections for SSH (port 2200), HTTP (port 80), and NTP (port 123).

5. Back in the terminal, run the following commands:

    ```
    sudo ufw status                     # check the status of the firewall
    sudo ufw default deny incoming      # deny imcoming connections
    sudo ufw default allow outgoing     # allow outgoing connections
    sudo ufw allow 2200\tcp             # allow listening on port 2200
    sudo ufw allow www                  # allow HTTP connections on port 80
    sudo ufw allow ntp                  # allow NTP connections on port 123
    sudo ufw show added                 # double check if all your changes are the ones you want
    sudo ufw enable                     # enable the firewall
    sudo ufw status                     # it should give an Active status now
    ```

> *Warning:* When changing the SSH port, make sure that the firewall is open for port 2200 first, so that you don't lock yourself out of the server. We already did this step in the very beginning so its all good! When you change the SSH port, the Lightsail instance will no longer be accessible through the web app 'Connect using SSH' button. The button assumes the default port is being used. There are instructions on the same page for connecting from your terminal to the instance. Connect using those instructions and then follow the rest of the steps.


Once done with those configurations, it is now time to create the `grader` user and give them root permission!


## Step 4: Create user Grader; Sudo! Sudo! Sudo!
1. Run the following command to create the user:

    `sudo adduser grader   #password: udacity`

2. To give the grader user permission to sudo, run the following command:

    `sudo nano /etc/sudoers.d/grader`

3. Inside the now open file, add the following text:

      **"grader  ALL=(ALL:ALL) ALL"**

4. Save and Exit the file: `CTRL + X Y Enter`

That's it! Now your grader user has sudo permissions! It is now time to allow the grader to access our server!

## Step 5: Permission Granted!
1. On your local machine, inside a terminal (Recommended for Windows: Git Bash), run the following command:

    `ssh-keygen`

2. Enter the path you want to save the key-pairs in:

    `/c/Users/yourDesktopName/.ssh/yourFileName`

3. Once the key is created, run the following command:

    `cat ~/.ssh/yourFileName.pub`

4. Copy the whole line that is displayed.

5. Back on your LightSail terminal, run the following commands:

    ```
    sudo mkdir /home/grader/.ssh
    sudo touch /home/grader/.ssh/authorized_keys
    sudo nano /home/grader/.ssh/authorized_keys
    ```

    Within the opened file, paste the line you just copied inside and Save: `CTRL + X, Y, Enter`

    Continue running commands to change file permissions for the `grader` user

    ```
    sudo chown grader:grader /home/grader/.ssh
    sudo chmod 700 /home/grader/.ssh
    sudo chmod 644 /home/grader/.ssh/authorized_keys
    ```

Alright! `grader` user is setup. Now, we just need one last thing before we start deploying our application!

## Step 5: RootLogin: Permission Denied!
1. Run the following command:

    `sudo nano /etc/ssh/sshd_config`

2. Navigate the file until you find the following:

    **PermitRootLogin** - Change to **no**

    **PasswordAuthentication** - Change to **no**

## Step 6: Restart the SSH Service
1. Run the following command:

    `sudo service ssh restart`


And, we are done with the first Part of the Configuration! We will start deploying our application in the next part.

> *Note:* By now, you might have lost access to your LightSail terminal. Don't worry! Since you configured the grader user with the key-pair you generated, you can easily log into the server using your own terminal. Simply run `ssh -i ~/.ssh/yourFile name grader@PUBLIC IP ADDRESS -p 2200` in your terminal. If you are prompted to continue the connection, type 'yes'. And voila, you are logged in!


### 2. Flask Application Deployment

Let's get into deploying our application for real now!

## Step 1: Configure Timezone
1. Make sure the timezone is UTC by running the following command:

    `date`

2. Incase it is not UTC, run the following command:

    `sudo timedatectl set-timezone UTC`

## Step 2: Apache time!
We will now configure the Apache to serve Python mod_wsgi applications.

1. Run the following commands:

    ```
    sudo apt-get install apache2                    # install the apache2 package
    sudo apt-get install libapache2-mod-wsgi-py3    # install the mod_wsgi package for Python3
    sudo a2enmod wsgi                               # enable mod_wsgi
    sudo service apache2 restart                    # restart the service
    ```

> *Note:* If you have built your application with Python2, use the following command instead `sudo apt-get install libapache2-mod-wsgi`


## Step 3: PostgreSQL Time!
We will now configure the PostgreSQL package

1. Run the following commands:

    ```     
    sudo apt-get install libpq-dev python-dev               # for python development
    sudo apt-get install postgresql postgresql-contrib      # install the postgresql package
    sudo nano /etc/postgresql/9.5/main/pg_hba.conf          # check the configuration file for remote connections
    ```

    > *Note:* To ensure that remote connections to PostgreSQL are not allowed, check that the configuration file so that it only allows connections from the local host addresses **127.0.0.1** for IPv4 and **::1** for IPv6.

2. Inside the database, run the following:

    ```
    sudo -u postgres psql                                   # Change into user `postgres` & access the psql
    CREATE USER catalog WITH PASSWORD 'catalog';            # Create user
    ALTER USER catalog CREATEDB;                            # Alter the user
    CREATE DATABASE catalog WITH OWNER catalog;             # Create the database
    ```

## Step 4: Git Time!
1. Install git (if not already installed). Run the following command:

    `sudo apt-get install git`

## Step 5: Deployment Time!
1. Clone the git repositroy for your Item Catalog Project & place it the appropriate directory:

    ```
    cd /var/www
    sudo mkdir catalog
    sudo chown -R grader:grader catalog
    cd catalog
    sudo git clone https://github.com/a-g-hantash/item-catalog-project.git catalog
    ```

2. Change your files (database_setup.py, database_init.py, app.py) for the application to work

    a. Change all `create_engine` lines to:

    `create_engine('postgresql://catalog:yourPassword@localhost/catalog')`

    b. Give the absolute path for the `client_secrets.json` file:

    `/var/www/catalog/catalog/client_secrets.json`

    c. Import additional modules into your `app.py` file:


        import os
        import logging
        import psycopg2


    In the same file, in the main method, add:

        app.run()

    And remove:


         app.debug = True
         app.run(host='0.0.0.0', port=8080)


    d. Import additional modules into your `database_setup.py` file:

        import os
        import sys
        import psycopg2


    e. Import additional modules into your `databse_init.py` file:

        import psycopg2

3. Create your _.wsgi_ file. Run the following commands:

    ```
    cd /var/www/catalog  
    sudo touch /var/www/catalog/catalog.wsgi
    sudo nano /var/www/catalog/catalog.wsgi
    ```

   a. Inside the file, write the following:

    ```
    import sys
    import logging

    logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
    sys.path.insert(0, "/var/www/catalog/")
    sys.path.append('/var/www/catalog/catalog/')
    sys.path.append('/usr/local/bin/python3.5/site-packages')


    from catalog import app as application
    application.secret_key = 'super_secret_key
    ```

    b. Save the file: `CTRL + X, Y, Enter`

4. Configure a New VirtualHost. Run the following commands:

    `sudo nano /etc/apache2/sites-available/catalog.conf`

    a. Inside the file, write the following:

    ```
    WSGIApplicationGroup %{GLOBAL}
    WSGIRestrictEmbedded On

    <VirtualHost *:80>
        ServerName 54.93.190.254
        ServerAlias ec2-54-93-190-254.eu-central-1.compute.amazonaws.com
        ServerAdmin grader@54.93.190.254
        WSGIDaemonProcess catalog
        WSGIProcessGroup catalog
        WSGIScriptAlias / /var/www/catalog/catalog.wsgi

        <Directory /var/www/catalog/catalog/>
            Order allow,deny
            Allow from all
        </Directory>

        Alias /static /var/www/catalog/catalog/static

        <Directory /var/www/catalog/catalog/static/>
            Order allow,deny
            Allow from all
        </Directory>

        ErrorLog ${APACHE_LOG_DIR}/error.log
        LogLevel warn
        CustomLog ${APACHE_LOG_DIR}/access.log combined
    </VirtualHost>
    ```

     b. Save the file: `CTRL + X, Y, Enter`

5. Install all the dependencies

    ```
    sudo apt-get install python3-flask
    sudo apt-get install python3-sqlalchemy
    sudo apt-get install python3-psycopg2
    sudo apt-get install python3-oauth2client
    sudo apt-get install python3-httplib2
    ```

6. Rename app.py. Run the following command:

    `mv app.py __init__.py`

7. Enable the catalog virtual host and disable the default site. Run the following commands:

    ```
    sudo a2ensite catalog.conf
    sudo service apache2 restart
    sudo a2dissite 000-default.conf
    sudo service apache2 restart
    ```
8. Enable the virtual site. Run the following command:

    ```
    sudo a2ensite catalog
    sudo service apache2 restart
    ```


**And all done! If you visit your application URL or your IP address, you should see your site live!**


## References

**Udacity Forums**

**GitHub**
**Special Thanks to *
https://github.com/a-g-hantash/linux-server-configuration
https://github.com/iliketomatoes/linux_server_configuration
https://github.com/rrjoson/udacity-linux-server-configuration
https://github.com/twhetzel/ud299-nd-linux-server-configuration
https://github.com/stueken/FSND-P5_Linux-Server-Configuration
https://github.com/kongling893/Linux-Server-Configuration-UDACITY
https://github.com/louiscollinsjr/udacity-linux-server-configuration


* for a very helpful README**
