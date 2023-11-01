def compute_indices_ls89(image):
    '''
    Compute indices for DSWE calculation for Landsat 8 and 9 (OLI sensor)
    ==================
    author: Florian Betz
    email: fbetz.geo@gmail.com
    -------------------------------
    '''

    if not image.get('SENSOR_ID').getInfo() in ['OLI_TIRS']:
        raise ValueError("Working for Landsat 8 and 9 with OLI sensor only!")


    ndvi=image.normalizedDifference(["SR_B5","SR_B4"])

    mndwi=image.normalizedDifference(["SR_B3","SR_B7"])

    mbsrv=image.select("SR_B3").add(image.select("SR_B4"))

    mbsrn=image.select("SR_B5").add(image.select("SR_B6"))

    awesh=image.expression(
    'BLUE+(2.5*GREEN)-(1.5*MBSRN)-0.25*SWIR2',{
    'BLUE':image.select("SR_B2"),
    'GREEN':image.select("SR_B3"),
    'MBSRN':image.select("MBSRN"),
    'SWIR2':image.select("SR_B7")})

    return image.addBands(awesh.rename("AWESH")).addBands(mbsrn.rename("MBSRN")).addBands(mbsrv.rename("MBSRV")).addBands(mndwi.rename("MNDWI")).addBands(ndvi.rename("NDVI"))
