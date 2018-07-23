
import uuid

from osgeo import gdal

from _a_pooled_emissary_raster import *

class SequentialGDALFileRaster(APooledEmissaryRaster):

    def __init__(self, ds, path, driver, open_options, mode):
        back_ds = ds._back

        # uuid = uuid.uuid4()
        # with back_ds.acquire(uuid, lambda: BackSequentialGDALFileRaster._open_file(path, driver, open_options, mode)) as gdal_ds:
        #     path = gdal_ds.GetDescription()
        #     driver = gdal_ds.GetDriver().ShortName
        #     fp_stored = Footprint(
        #         gt=gdal_ds.GetGeoTransform(),
        #         rsize=(gdal_ds.RasterXSize, gdal_ds.RasterYSize),
        #     )
        #     band_schema = Raster._band_schema_of_gdal_ds(gdal_ds)
        #     dtype = conv.dtype_of_gdt_downcast(gdal_ds.GetRasterBand(1).DataType)
        #     wkt_stored = gdal_ds.GetProjection()

        back = BackSequentialGDALFileRaster(
            back_ds,
            ...
        )

        super(SequentialGDALFileRaster, self).__init__(ds=ds, back=back)

class BackSequentialGDALFileRaster(ABackPooledEmissaryRaster):

    def __init__(self, back_ds, ...,
                 # gdal_ds,
                 # path, driver, open_options, mode
    ):

        super(..., self).__init__(
            back_ds=back_ds,
            wkt_stored=wkt_stored,
            band_schema=band_schema,
            dtype=dtype,
            fp_stored=fp_stored,
            mode=mode,
            driver=driver,
            open_options=open_options,
            path=path,
            uuid=uuid,
        )

    def get_data(self): pass
    def set_data(self): pass

    def fill(self, value, bands):
        with self.back_ds.acquire_driver_object(self, self.uuid, self._allocator) as gdal_ds:
            for gdalband in [self._gdalband_of_index(gdal_ds, i) for i in bands]:
                gdalband.Fill(value)

    def delete(self):
        super(BackSequentialGDALFileRaster, self).delete()

        dr = gdal.GetDriverByName(self.driver)
        err = dr.Delete(self.path)
        if err:
            raise RuntimeError('Could not delete `{}` (gdal error: `{}`)'.format(
                self.path, str(gdal.GetLastErrorMsg()).strip('\n')
            ))

    def _allocator(self):
        return TODO._open_file(self.path, self.driver, self.open_options, self.mode))

    @staticmethod
    def _gdalband_of_index(gdal_ds, index):
        """Convert a band index to a gdal band"""
        if isinstance(index, int):
            return gdal_ds.GetRasterBand(index)
        else:
            return gdal_ds.GetRasterBand(int(index.imag)).GetMaskBand()

    @staticmethod
    def _open_file(path, driver, options, mode):
        """Open a raster datasource"""
        options = [str(arg) for arg in options]
        gdal_ds = gdal.OpenEx(
            path,
            conv.of_of_mode(mode) | conv.of_of_str('raster'),
            [driver],
            options,
        )
        if gdal_ds is None:
            raise ValueError('Could not open `{}` with `{}` (gdal error: `{}`)'.format(
                path, driver, str(gdal.GetLastErrorMsg()).strip('\n')
            ))
        return gdal_ds