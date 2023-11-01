def preprocess(image):
    '''
    Preprocessing Landsat images in Google Earth Engine
    ==================
    author: Florian Betz
    email: fbetz.geo@gmail.com
    -------------------------------
    '''

    # Apply scaling factors to the surface reflectance and thermal bands (thermal just in case...)
    opticalBands = image.select("SR_B.").multiply(0.0000275).add(-0.2)
    thermalBands = image.select('ST_B.*').multiply(0.00341802).add(149.0)

    # Cloud masking with quality band, same for all Landsat generations since collection 2
    qa = image.select("QA_PIXEL")
    clouds = 1 << 5
    cloud_shadows = 1 << 3
    snow = 1 << 4
    mask = qa.bitwiseAnd(clouds).eq(0).And(qa.bitwiseAnd(cloud_shadows).eq(0)).And(qa.bitwiseAnd(snow).eq(0))

    return image.addBands(srcImg=opticalBands, overwrite=True).addBands(srcImg=thermalBands, overwrite=True).updateMask(mask)