# Class porject for CS425

# How to connect to Oracle DB (pip & flask installed before)
(A tutorial link: http://www.golden-orb.ltd.uk/working-with-oracle-from-python-on-a-mac/)
1. Download Oracle instantclient basic, sqlplus and sdk.
2. unzip file
    
    mkdir -p ~/Applications/Oracle
    cd ~/Applications/Oracle
    unzip ~/Downloads/instantclient-basiclite-macos.x64-11.2.0.4.0.zip
    unzip ~/Downloads/instantclient-sqlplus-macos.x64-11.2.0.4.0.zip
    unzip ~/Downloads/instantclient-sdk-macos.x64-11.2.0.4.0.zip

3. Add the following configuration to .bash_profile, and restart the shell.
    
    export ORACLE_HOME=~/Applications/Oracle/instantclient_11_2
    export PATH="${PATH:+$PATH:}$ORACLE_HOME"
    export DYLD_LIBRARY_PATH="${DYLD_LIBRARY_PATH:+$DYLD_LIBRARY_PATH:}$ORACLE_HOME"

4. Create the following file
    
    mkdir -p $ORACLE_HOME/network/admin
    $ORACLE_HOME/network/admin/tnsnames.ora

5. put the following content in tnsnames.ora

    ORCL =
        (DESCRIPTION =
        (ADDRESS = (PROTOCOL = TCP)(HOST = fourier.cs.iit.edu)(PORT = 1521))
        (CONNECT_DATA =
        (SERVER = DEDICATED)
        (SERVICE_NAME = orcl)
        )
    )

6. Set up a link for library file.

    cd $ORACLE_HOME
    ln -s libclntsh.dylib.11.1 libclntsh.dylib
    
7. pip install oc_Oracle
   pip install sqlalchemy

