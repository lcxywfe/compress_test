#include <gdal_utils.h>
#include <gdal_priv.h>
#include <assert.h>


void gdal_translate(const char* src_path, const char* dst_path) {
    GDALDatasetUniquePtr src(GDALDataset::Open(src_path));
    assert(src != nullptr);

    const char *options_str[] = {"-co", "COMPRESS=ZSTD", "-co", "PREDICTOR=2",
                                 nullptr};
    auto options =
        GDALTranslateOptionsNew(const_cast<char **>(options_str), nullptr);

    GDALTranslate(dst_path, GDALDataset::ToHandle(src.get()), options, nullptr);
    GDALTranslateOptionsFree(options);
}

