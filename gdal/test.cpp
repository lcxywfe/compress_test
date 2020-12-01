#include <gdal_utils.h>
#include <gdal_priv.h>
#include <assert.h>
#include <chrono>
#include <iostream>


namespace{

class Timer {
public:
    Timer() { reset(); }
    void reset() {
        m_started = false;
        m_stopped = false;
    }
    void start() {
        assert(!m_started);
        m_started = true;
        m_start = std::chrono::high_resolution_clock::now();
    }
    void stop() {
        assert(m_started);
        assert(!m_stopped);
        m_stopped = true;
        m_stop = std::chrono::high_resolution_clock::now();
    }
    size_t get_time_in_ms() const {
        assert(m_stopped);
        return std::chrono::duration_cast<std::chrono::milliseconds>(m_stop -
                                                                     m_start)
                .count();
    }

private:
    using time_point = std::chrono::high_resolution_clock::time_point;
    time_point m_start, m_stop;
    bool m_started, m_stopped;
};

}  // anonymous namespace


void gdal_translate(const char* src_path, const char* dst_path);


int main() { 
    GDALAllRegister();
    Timer timer;
    timer.reset();
    timer.start();
    gdal_translate("/home/heyao/repo/compress_test/uint16/7388.ortho.uint16.tif", "out0.tif");
    timer.stop();
    std::cout << "time: " << timer.get_time_in_ms() / 3 << std::endl;
    return 0;
}
