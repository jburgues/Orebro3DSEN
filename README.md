# Orebro3DSEN
Dataset and code of indoor gas dispersion experiments using a 3D grid of metal oxide semiconductor sensors.

# 1. Introduction
Advances in gas distribution mapping and localization algorithms are hindered by the lack of experimental measurements over three-dimensional (3D) volumes. Such measurements are important to characterize gas dispersion patterns produced by different types of gas release and to extract robust estimators of source proximity. In this project, we provide code and data for studying gas dispersion of an evaporating chemical source in an indoor scenario, using a 3D MOX sensor network. The source was placed in several locations of the room, including variations in height, release rate and air flow profiles. This is the first open access dataset using a 3D MOX sensor network, and it can be the basis to develop, validate, and compare new approaches related to gas sensing in complex environments. For example, we used this data to study the performance of source proximity estimators in 3D.
</p>
 
# 2. Experimental setup
A 30 sq-mt office room located at the School of Science and Technology of Örebro University (Sweden) was used as the test environment. The room has a single door and multiple windows on the east wall, however only one window can be opened. A HVAC air duct supplied clean air at floor level at a low velocity, which was then removed at ceiling level. The tables and chairs were re-arranged to provide ample access in the central part of the room.

![alt text](https://raw.githubusercontent.com/jburgues/Orebro3DSEN/master/img/room_labelled.png "CAD drawing of test room")
CAD drawing of test room

![alt text](https://raw.githubusercontent.com/jburgues/Orebro3DSEN/master/img/room_real_labelled.png "Photo of test room")
Photo of test room

# 3. Some results

![alt text]("https://raw.githubusercontent.com/jburgues/Orebro3DSEN/master/img/raSignal.png" "Calibrated sensor signals")
Calibrated sensor signals

![alt text]("https://raw.githubusercontent.com/jburgues/Orebro3DSEN/master/img/tempHumi.png" "Temperature and humidity")
Temperature and humidity in four locations of the room

![alt text](https://raw.githubusercontent.com/jburgues/Orebro3DSEN/master/img/windrose.png "Wind")
Wind rose in the center of the room (height=1.3 m)

![alt text](https://raw.githubusercontent.com/jburgues/Orebro3DSEN/master/img/meanMap.png "Mean map")
Mean gas distribution at different timestamps

![alt text](https://raw.githubusercontent.com/jburgues/Orebro3DSEN/master/img/boutsfreqMap.png "Bout freq map")
Mean bout frequency map at different timestamps
