def dswe(image,wigt=0.124,awgt=0,pswt_1_mndwi=-0.44,pswt1_1_swir1=0.09,pswt_1_nir=0.15,pswt_1_ndvi=0.7,pswt_2_mndwi=-0.5,pswt_2_blue=0.1,pswt_2_swir1=0.3,pswt_2_swir2=0.1,pswt_2_nir=0.25, thrs_hillshade=80):
    '''
    DSWE: Dynamic Surface Water Extraction for Google Earth Engine
    ==================
    author: Florian Betz
    email: fbetz.geo@gmail.com
    -------------------------------

    '''

    # Make hillshade masking => Update for dynamic hillshade threshold

    # Make hillshade band per Landsat scene for masking terrain shadow effects
    # (using NASADEM as standard DEM for Landsat Collection 2 processing, see Franks et al. 2020, https://doi.org/10.3390/rs12233909 for details)
    dem = ee.Image("NASA/NASADEM_HGT/001").clip(image.geometry())
    azimuth = image.get("SUN_AZIMUTH")
    elevation = image.get("SUN_ELEVATION")
    hillshade = ee.Terrain.hillshade(input=dem, azimuth=azimuth, elevation=elevation)
    hillshade_mask = hillshade.gt(thrs_hillshade)

    # Individual tests
    # Test 1
    test1 = image.select("MNDWI").gt(wigt)

    # Test2
    test2 = image.select("MBSRV").gt(image.select("MBSRN")).multiply(10)

    # Test3
    test3 = image.select("AWESH").gt(awgt).multiply(100)

    # Test4 (SR_B5 is the SWIR-1 band in LS457, for LS89 equals SR_B6)
    test4 = image.select("MNDWI").gt(pswt_1_mndwi) \
        .And(image.select("SR_B5").lt(pswt1_1_swir1)) \
        .And(image.select("SR_B4").lt(pswt_1_nir)) \
        .And(image.select("NDVI").lt(pswt_1_ndvi)) \
        .multiply(1000)

    # Test5
    test5 = image.select("MNDWI").gt(pswt_2_mndwi) \
        .And(image.select("SR_B1").lt(pswt_2_blue)) \
        .And(image.select("SR_B5").lt(pswt_2_swir1)) \
        .And(image.select("SR_B7").lt(pswt_2_swir2)) \
        .And(image.select("SR_B4").lt(pswt_2_nir)) \
        .multiply(10000)

    # Putting the tests together to get final digit coding
    test = test1.add(test2).add(test3).add(test4).add(test5)

    # Final recoding by remapping the test-scores to the final output classes
    test_scores = [0, 1, 10, 100, 1000, 1111, 10111, 11011, 11101, 11110, 11111, 111, 1011, 1101, 1110, 10011, 10101,
                   10110, 11001, 11010, 11100, 11000, 11, 101, 110, 1001, 1010, 1100, 10000, 10001, 10010, 10100]
    remap = [0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4]
    recoded = test.remap(test_scores, remap).updateMask(hillshade_mask)

    # Create binary water mask (water=1, non-water=0)
    wm = recoded.eq(1).Or(recoded.eq(2)).Or(recoded.eq(3)).Or(recoded.eq(4))
    wmm=wm.updateMask(hillshade_mask)

    # Return final output as image band
    return image.addBands(recoded.rename("DSWE")).addBands(test.rename("DSWE_SCORE")).addBands(wmm.rename("WATERMASK")).addBands(hillshade_mask.rename("HILLSHADE_MASK"))