sudo apt-get install ipython python-opencv python-scipy python-numpy python-pygame python-setuptools git
cd ~
git clone https://github.com/sightmachine/SimpleCV.git
cd SimpleCV/
sudo pip install -r requirements.txt
sudo python setup.py install
cd ~/SimpleCV/scripts/install/ubuntu
./opencv-install.sh
./opencv2_4_2_install.sh
./simplecv-install.sh
cd ~
rm -rf SimpleCV
cd ~
git clone https://github.com/akhilcjacob/python-ardrone-squareTracker.git
cd python-ardrone-squareTracker
sudo pip install -r requirements.txt


