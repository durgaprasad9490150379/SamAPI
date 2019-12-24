## Steps to install samba & python3 in centos machine

yum group install "Development Tools"

yum update

yum install gcc openssl-devel bzip2-devel libffi-devel zlib-devel

cd usr/src

yum install wget

wget https://www.python.org/ftp/python/3.7.3/Python-3.7.3.tgz

wget https://www.sqlite.org/2019/sqlite-autoconf-3280000.tar.gz

wget https://download.samba.org/pub/samba/stable/samba-4.10.2.tar.gz

tar -zxvf Python-3.7.3.tgz 

tar -zxvf sqlite-autoconf-3280000.tar.gz

tar -zxvf samba-4.10.2.tar.gz

cd sqlite-autoconf-3280000

./configure

make

make install

cd ../Python-3.7.3

./configure --prefix=/usr/local --enable-shared LDFLAGS="-Wl,-rpath /usr/local/lib"

make

make altinstall

strip /usr/local/lib/libpython3.7m.so.1.0 

wget https://bootstrap.pypa.io/get-pip.py

python3.7 get-pip.py

cd /usr/local/bin/

ln -sf python3.7 python3

cd /usr/src/samba-4.10.2


yum install -y https://centos7.iuscommunity.org/ius-release.rpm

yum install attr bind-utils docbook-style-xsl gcc gdb krb5-workstation \
       libsemanage-python libxslt perl perl-ExtUtils-MakeMaker \
       perl-Parse-Yapp perl-Test-Base pkgconfig policycoreutils-python \
       python2-crypto gnutls-devel libattr-devel keyutils-libs-devel \
       libacl-devel libaio-devel libblkid-devel libxml2-devel openldap-devel \
       pam-devel popt-devel python-devel readline-devel zlib-devel systemd-devel \
       lmdb-devel jansson-devel gpgme-devel pygpgme libarchive-devel
       
       
./configure

make

make install

export PATH=/usr/local/samba/bin/:/usr/local/samba/sbin/:$PATH
