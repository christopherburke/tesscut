# TessCut: Creating cutouts from TESS FFI image stacks

## Tesscut Design 

### Input
- Coordinate center (RA, Dec) in degrees.  
- Image size, in degrees.
  (Will have to deal with images that extend past chip and sector boundaries.)
- Time range, as an optional argument.  
  A user may not want every FFI, so allow for optional time range to be specified, e.g., t_min, t_max.
- User can requuest caluibrated or unclaibrated FFI products. Calibrated is default.

### Output
- Return a Target Pixel File (TPF) FITS file that follows TESS TPF conventions. 
  (Essentially an image cube cutout.)
- Return a separate TPF file for each sector (where a requested cutout is present in more than one sector)
- Open question is what to do when returning a TPF that spans multiple chips/cameras: separate TPF return files, single return file?
- Nice-to-have: Sum all the image cubes into a single stacked image. 
        
        
### Functionality
- Lookup to determine which stack(s) are needed for a given cutout.
  (Will be a database query)
- Will have to handle requested cut out regions that span multiple chips within a single camera.  
- Limit query to single sector, i.e. if cutout region is in multiple sectors, one TPF for each sector.
  (First run a query that returns which sectors of data are available?)
- Have local stand-alone code to generate TPF from on-disk FFI files (e.g., if someone downloads all FFIs, generate TPF files)
- Nice-to-have: Should allow for basic image differencing. 
  There are various algorithms, the most basic is where each frame has some template image subtracted from it.
