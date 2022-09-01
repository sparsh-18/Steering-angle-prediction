
# Self Driving Car - Behavioural Cloning




## Data Extraction

The data for the behavioural cloning is collected using Udacity's Self Driving Car Simulator.

`https://github.com/udacity/self-driving-car-sim`

The following features are set for graphics:

`600 x 800 format`

`Fastest graphics`

In the training mode the car is driven for 3 Laps in the forward directon as well as for 3 laps in the opposite directon.
This is performed so that the model is not biased towards one turn.
The data is taken from 3 cameras `left`, `right` and `center`. It stores `steering`, `throttle`, `reverse` and `speed`. 

