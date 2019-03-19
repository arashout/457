# 457

## Example Operation
![Example Tracking](out_vids/7.gif)

## Why
For our capstone project our team is building an bottom bracket for the [Veemo](https://www.velometro.com/veemo/) (Enclosed Electric Bike) with integrated angular position detection of the crank arm. To validate our optical encoder built from scratch I built this tool so that we can compare readings from the arduino to the actual motion of the spindle/crank arm.

## How
1. Take video of the spindle spinning with a clear orange marker to track
2. Using OpenCV + Python track the position of this marker
3. Convert x,y motion capture data by [fitting a circle](http://www.math.stonybrook.edu/~scott/Book331/Fitting_circle.html) using Non-Linear Least Squares (NLLS) to convert x,y into angles of the crank arm
4. Cross-reference the data with our arduino reading from the optical encoder
