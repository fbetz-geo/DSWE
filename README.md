## Getting Dynamic Surface Water Extent for Landsat Collection 2 in Google Earth Engine
This is an implementation of the dynamic surface water extraction algorithm for Landsat
collection 2 basing upon the algorithm of Jones (2019). This work is inspired by 
by [Ben DeVries](https://github.com/bendv/eedswe/) who presented GEE code for 
the early version of DSWE and Landsat collection 1. The python code here is a new
implementation of the updated USGS DSWE algorithm and Landsat collection 2 
surface reflection.


### Use the python code
You will need an account and authentication for Google Earth Engine 
to get started. Once you have a working earth engine account, you can install
the python package from github:

```bash
git clone https://github.com/fbetz-geo/cloudDSWE
cd cloudDSWE
pip install .
```
### Detailed algorithm description by USGS

[Landsat Collection 2 (C2) Level 3 (L3) Dynamic Surface Water Extent (DSWE) Algorithm Description Document (ADD) ](https://d9-wret.s3.us-west-2.amazonaws.com/assets/palladium/production/s3fs-public/media/files/LSDS-2084_LandsatC2_L3_DSWE_ADD-v1.pdf)

### References

- Jones, J.W. (2015). Efficient wetland surface water detection and monitoring via
Landsat: Comparison with in situ data from the Everglades Depth Estimation Network.
Remote Sensing, 7(9), 12503-12538. http://dx.doi.org/10.3390/rs70912503
- Jones, J.W. (2019). Improved Automated Detection of Subpixel-Scale Inundation—
Revised Dynamic Surface Water Extent (DSWE) Partial Surface Water Tests. Remote
Sens. 11, 374. https://doi.org/10.3390/rs11040374
- Otsu, N. (1979). A threshold selection method from gray-level histograms. IEEE
transactions on systems, man, and cybernetics, 9(1), 62-66.