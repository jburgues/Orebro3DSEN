# Orebro3DSEN
Dataset and code of indoor gas dispersion experiments using a 3D grid of metal oxide semiconductor sensors. This software is used in the following article: 
Burgués J, Hernandez V, Lilienthal AJ, Marco S. 3D Gas Distribution with and without Artificial Airflow: An Experimental Study with a Grid of Metal Oxide Semiconductor Gas Sensors. InMultidisciplinary Digital Publishing Institute Proceedings 2018 (Vol. 2, No. 13, p. 911).

# 1. Introduction
Advances in gas distribution mapping and localization algorithms are hindered by the lack of experimental measurements over three-dimensional (3D) volumes. Such measurements are important to characterize gas dispersion patterns produced by different types of gas release and to extract robust estimators of source proximity. In this project, we provide code and data for studying gas dispersion of an evaporating chemical source in an indoor scenario, using a 3D MOX sensor network. The source was placed in several locations of the room, including variations in height, release rate and air flow profiles. The MOX sensors were calibrated in laboratory conditions to provide signals in concentration units. This is the first open access dataset using a 3D MOX sensor network, and it can be the basis to develop, validate, and compare new approaches related to gas sensing in complex environments. For example, we used this data to study the performance of source proximity estimators in 3D.
 
# 2. Experimental setup
A 30 sq-mt office room located at the School of Science and Technology of Örebro University (Sweden) was used as the test environment. The room has a single door and multiple windows on the east wall, however only one window can be opened. A HVAC air duct supplied clean air at floor level at a low velocity, which was then removed at ceiling level. The tables and chairs were re-arranged to provide ample access in the central part of the room. 27 MOX sensors (Several TGS models, Figaro Engineering Inc.) were evenly distributed in a 3 x 3 x 3 grid. Each sensor was mounted on a conditioning board that integrates a voltage divider (load resistor = 68 kΩ) to read out the sensor output. The sensors were divided into four groups of 9, 6, 6 and 6 sensors, respectively, to minimize the amount of wiring. Each group of sensors was powered by an individual power source, and the analog sensor signals were acquired by a custom processing node based on an Arduino Mega microcontroller with a WiFi shield (Arduino AG). The sensor signals, together with temperature and humidity measurements (DHT22, Adafruit Industries) in different locations of the test room, were sent to a central computer via WiFi.  The sampling frequency was limited by the acquisition hardware to 2 Hz. The sensors were individually calibrated in a laboratory, in similar conditions of humidity and temperature than the test room. 

![alt text](https://raw.githubusercontent.com/jburgues/Orebro3DSEN/master/img/room_labelled.png "CAD drawing of test room")
CAD drawing of test room

![alt text](https://raw.githubusercontent.com/jburgues/Orebro3DSEN/master/img/room_real_labelled.png "Photo of test room")
Photo of test room

# 3. Some results
The following results correspond to different experiments. The idea is to show what kind of signals have been recorded during the experiments, and how these signals can be manipulated to produce 3D gas distribution maps. These maps are useful to understand how the gas is dispersed in the environment, if it is easy to locate the gas source from such measurements, etc. In particular, we have found that the bout frequency is a better estimator of source proximity than the mean concentration, as the corresponding map shows a gradient with maximum value at the source. 

![alt text](https://raw.githubusercontent.com/jburgues/Orebro3DSEN/master/img/rawSignal.png "Calibrated sensor signals")
Calibrated sensor signals

![alt text](https://raw.githubusercontent.com/jburgues/Orebro3DSEN/master/img/tempHumi.png "Temperature and humidity")
Temperature and humidity in four locations of the room

![alt text](https://raw.githubusercontent.com/jburgues/Orebro3DSEN/master/img/windrose.png "Wind")
Wind rose in the center of the room (height=1.3 m)

![alt text](https://raw.githubusercontent.com/jburgues/Orebro3DSEN/master/img/meanMap.png "Mean map")
Mean gas distribution at different timestamps

![alt text](https://raw.githubusercontent.com/jburgues/Orebro3DSEN/master/img/boutsfreqMap.png "Bout freq map")
Mean bout frequency map at different timestamps

# 4. Logs
The folder /logs contains 10 csv files, corresponding to a subset of the experiments, which are described in Table 1.
The meaning of the columns of the CSV file is indicated in the header. Basically, there is a timestamp, 27 concentration values (1 per MOX sensor), 4 temperature measurements, 4 humidity measurements, wind speed and wind direction.

![alt text](https://raw.githubusercontent.com/jburgues/Orebro3DSEN/master/img/TableExperiments.PNG "List of experiments")
Table 1. List of experiments

# 5. Code
The file "wsn_lite.py" is the main file of the project. It contains a class "wsn" that provides functions for parsing and plotting the logs. It requires the file "log_wsn.py" to be in the same folder.
The file "wsn_test.py" is an example of how to use the class "wsn". The 3D maps presented in Section 3 were done using MATLAB, due to limitations of matplotlib to perform such visualizations. The plots available in the current code are therefore 2D plots.

# 6. License
The code and logs are licensed under the GNU General Public License v3.0

# 7. Contact
For any inquiries or questions, please write an email to jburgues8@gmail.com

