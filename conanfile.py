from conans import ConanFile, CMake, tools, AutoToolsBuildEnvironment
import os


class SmpegConan(ConanFile):
    name = "smpeg"
    version = "2.0.0"
    license = "<Put the package license here>"
    url = "<Package recipe repository url here, for issues about the package>"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=True"
    generators = "cmake"
    requires = "SDL2/2.0.5_1@hi3c/experimental"

    def source(self):
        tools.download("https://www.libsdl.org/projects/smpeg/release/smpeg2-2.0.0.tar.gz", "smpeg.tar.gz")
        tools.unzip("smpeg.tar.gz")
        os.remove("smpeg.tar.gz")

    def build(self):
        atbe = AutoToolsBuildEnvironment(self)
        atbe.flags.append("-Wno-narrowing")
        atbe.fpic = True
        atbe.configure(configure_dir="smpeg2-2.0.0")
        atbe.make()

    def package(self):
        self.copy("*.h", dst="include", src="smpeg2-2.0.0")
        self.copy("*.lib", dst="lib", keep_path=False)

        if self.options.shared:
            self.copy("*.dll", dst="bin", keep_path=False)
            self.copy("*.so*", dst="lib", keep_path=False)
            self.copy("*.dylib", dst="lib", keep_path=False)
        else:
            self.copy("*.a", dst="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ["smpeg2"]
