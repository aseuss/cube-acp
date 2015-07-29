#
# CMakeLists.txt
#
# Copyright 2015 Andreas Seuss
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

cmake_minimum_required (VERSION 2.8)
project (Cube-ACP)

set (NVTEXTURE_TOOL "nvcompress")
set (ASTC_ENCODER "astcenc")

set (OUT_DIR "${CMAKE_SOURCE_DIR}/out")

set (DXT1_SOURCES tex1.png tex2.png tex3.png tex4.png tex5.png)
set (DXT3_SOURCES tex6.png tex7.png tex8.png)
set (DXT5_SOURCES tex9.png tex10.png tex11.png)
set (ASTC_SOURCES ${DXT1_SOURCES})

macro (addDxtTarget target options sources comment)
    set (${target}_FILES)
    foreach (DXT_SOURCE ${${sources}})
        string (REGEX REPLACE "[.][^.]+$" "" DXT_FILE ${DXT_SOURCE})
        set (DXT_FILE "${DXT_FILE}.dds")
        add_custom_command(
            OUTPUT ${DXT_FILE}
            COMMAND ${NVTEXTURE_TOOL} ${options} ${CMAKE_CURRENT_SOURCE_DIR}/${DXT_SOURCE} ${DXT_FILE} > /dev/null
            DEPENDS ${DXT_SOURCE}
        )
        list (APPEND ${target}_FILES ${DXT_FILE})
    endforeach()

    add_custom_target (${target}
        DEPENDS ${${target}_FILES}
        COMMENT ${comment})
endmacro()

macro (addAstcTarget target rate options sources comment)
    set (${target}_FILES)
    foreach (ASTC_SOURCE ${${sources}})
        string (REGEX REPLACE "[.][^.]+$" "" ASTC_FILE ${ASTC_SOURCE})
        set (ASTC_FILE "${ASTC_FILE}_${rate}.astc")
        add_custom_command(
            OUTPUT ${ASTC_FILE}
            COMMAND ${ASTC_ENCODER} -c ${CMAKE_CURRENT_SOURCE_DIR}/${ASTC_SOURCE} ${ASTC_FILE} ${rate} ${${options}}
            DEPENDS ${ASTC_SOURCE}
        )
    list (APPEND ${target}_FILES ${ASTC_FILE})
    endforeach()

    add_custom_target (${target}
        DEPENDS ${${target}_FILES}
        COMMENT ${comment})
endmacro()

addDxtTarget (dxt1 "-bc1" DXT1_SOURCES "convert textures to DXT1/BC1")
addDxtTarget (dxt3 "-bc2" DXT3_SOURCES "convert textures to DXT3/BC2")
addDxtTarget (dxt5 "-bc3" DXT5_SOURCES "convert textures to DXT5/BC3")

set (ASTC_OPTIONS "-srgb" "-medium")
addAstcTarget (astc "5x4" ASTC_OPTIONS ASTC_SOURCES "convert textures to ASTC")

add_custom_target (textures
    DEPENDS dxt1 dxt3 dxt5 astc
    COMMENT "compress textures")


# read texture conversion parameters from json config file
execute_process (COMMAND python "files.py" "astc"
    OUTPUT_VARIABLE target_parameters
    WORKING_DIRECTORY ${CMAKE_SOURCE_DIR})

string (REGEX MATCHALL "[^\n]+" TARGET_PARAM_LIST ${target_parameters})
set (ASTC_NEW_FILES)
foreach (img_file ${TARGET_PARAM_LIST})
    string (REPLACE "," ";" mylist ${img_file})
    list (GET mylist 0 target)
    list (GET mylist 1 src_file)

    get_filename_component (filename ${src_file} NAME_WE)
    get_filename_component (filepath ${src_file} DIRECTORY)

    if (${target} MATCHES "^astc")
        message ("convert to astc")
        list (GET mylist 2 astc_options)
        list (GET mylist 3 astc_rate)

        string (REGEX REPLACE " " ";" astc_options ${astc_options})

        set (astc_file "${filepath}/${filename}_${astc_rate}.astc")
        add_custom_command(
            OUTPUT ${astc_file}
            COMMAND ${CMAKE_COMMAND} -E make_directory "${CMAKE_BINARY_DIR}/${filepath}"
            COMMAND ${ASTC_ENCODER} -c ${CMAKE_CURRENT_SOURCE_DIR}/${src_file} ${astc_file} ${astc_rate} ${astc_options}
            DEPENDS ${src_file}
        )
        list (APPEND ASTC_NEW_FILES ${astc_file})
    elseif (${target} MATCHES "^dxt1")
        message ("convert to dxt1")
        # TODO: add structure here, maybe use macro
    elseif (${target} MATCHES "^dxt3")
        message ("convert to dxt3")
        # TODO: add structure here, maybe use macro
    elseif (${target} MATCHES "^dxt5")
        message ("convert to dxt5")
        # TODO: add structure here, maybe use macro
    endif()

endforeach()

add_custom_target (astc_new
    DEPENDS ${ASTC_NEW_FILES}
    COMMENT "convert new astc")

