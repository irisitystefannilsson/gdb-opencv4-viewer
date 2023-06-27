# filename: cvplot.py
# from: https://github.com/beenfrog/gdb-opencv-viewer
# modified to use opencv4 mats (numpy arrays)
import gdb
import cv2 as cv
import numpy as np


class PlotterCommand(gdb.Command):
    def __init__(self):
        super(PlotterCommand, self).__init__("plot",
                                             gdb.COMMAND_DATA,
                                             gdb.COMPLETE_SYMBOL)

    def invoke(self, arg, from_tty):
        args = gdb.string_to_argv(arg)

        # generally, we type "plot someimage" in the GDB commandline
        # where "someimage" is an instance of cv::Mat
        v = gdb.parse_and_eval(args[0])

        # the value v is a gdb.Value object of C++
        # code's cv::Mat, we need to translate to
        # a python object under cv2
        cols = int(v['cols'])
        rows = int(v['rows'])
        image_size = (cols, rows)

        CV_8U = 0
        CV_8S = 1
        CV_16U = 2
        CV_16S = 3
        CV_32S = 4
        CV_32F = 5
        CV_64F = 6
        CV_USRTYPE1 = 7
        CV_CN_MAX = 512
        CV_CN_SHIFT = 3
        CV_MAT_CN_MASK = (CV_CN_MAX - 1) << CV_CN_SHIFT
        flags = v['flags']
        channel = (((flags) & CV_MAT_CN_MASK) >> CV_CN_SHIFT) + 1
        CV_DEPTH_MAX = (1 << CV_CN_SHIFT)
        CV_MAT_DEPTH_MASK = CV_DEPTH_MAX - 1
        depth = (flags) & CV_MAT_DEPTH_MASK
        IPL_DEPTH_SIGN = 0x80000000
        cv_elem_size = (((4 << 28) | 0x8442211) >> depth*4) & 15
        if (depth == CV_8S or depth == CV_16S or depth == CV_32S):
            mask = IPL_DEPTH_SIGN
        else:
            mask = 0
        ipl_depth = cv_elem_size*8 | mask

        # convert the v['data'] type to "char*" type
        char_type = gdb.lookup_type('char')
        char_pointer_type = char_type.pointer()
        buffer = v['data'].cast(char_pointer_type)

        # read bytes from inferior's memory, because
        # we run the opencv-python module in GDB's own process
        # otherwise, we use memory corss processes
        buf = v['step']['buf']

        # find out if we are plotting a submatrix
        # i.e., a roi
        delta1 = v['data'] - v['datastart']
        ofs_y = int(delta1 / buf[0])
        ofs_x = delta1 - int(buf[0])*ofs_y

        bytes = buf[0] * (rows + ofs_y)  # buf[0] is the step
        inferior = gdb.selected_inferior()
        mem = inferior.read_memory(buffer, bytes)

        # set the img's raw data
        img_char = np.asarray(mem)
        if ofs_x == 0 and ofs_y == 0:
            img_char = img_char.reshape((image_size[1], image_size[0], channel))
        else:  # this a roi submatrix
            roi_data = img_char[0:(rows*cols*channel)]
            roi_offs = 0
            for r in range(ofs_y, ofs_y + rows):
                roi_data[roi_offs:(roi_offs + cols*channel)] = \
                    img_char[(r*int(buf[0]) + ofs_x):(r*int(buf[0]) + ofs_x + cols*channel)]
                roi_offs += cols*channel
            img_char = roi_data.reshape((image_size[1], image_size[0], channel))
        gdb.write('shape: ' + str(img_char.shape) + '\n')
        gdb.write('ipl_depth: ' + str(ipl_depth) + '\n')
        gdb.flush()
        img = np.zeros(img_char.shape, dtype=np.uint8)
        for i in range(0, img.shape[0]):
            for j in range(0, img.shape[1]):
                for k in range(0, img.shape[2]):
                    try:
                        img[i, j, k] = ord(img_char[i, j, k])
                    except:
                        pass
        # create a window, and show the image
        cv.startWindowThread()
        warning_title = 'DO NOT CLOSE ME USING MOUSE PTR!!, IT WILL HANG THE GDB SESSION !!'
        cv.namedWindow(warning_title)
        cv.imshow(warning_title, img)
        # the below statement is necessary, otherwise, the Window
        # will hang
        cv.waitKey(0)
        cv.destroyWindow(warning_title)


PlotterCommand()
