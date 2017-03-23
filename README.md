# Aqueduct
CLI Tool for migrating MySQL databases

### Requirements
- Python3
- PIP

### Usage
For help run `Aqueduct -h`
```
Aqueduct {src.ini.example} {target.ini.example}
```

### Build
```
pip install -r requirements.txt
```

### Config files
Create a file called `.my.cnf` in your home directory.
```
touch ~/.my.cnf
```

Give it the correct permissions:
```
chmod 0600 ~/.my.cnf
```

Add your DB credentials with the following format:
```
[client]
user={DB_USERNAME}
password={DB_PASSWORD}
```

### CentOS6 Install
##### Install Python3
```
sudo yum install -y https://centos6.iuscommunity.org/ius-release.rpm
sudo yum install -y python35u python35u-pip
```
