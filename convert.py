import os
import urllib
import traceback
import time
import sys
import numpy as np
from rknn.api import RKNN

ONNX_MODEL = 'robotics.onnx'
RKNN_MODEL = 'robotics.rknn'
TARGET_PLATFORM='rk3566'
if __name__ == '__main__':

    rknn = RKNN(verbose=True)

    # pre-process config
    print('--> Config model')
    rknn.config(mean_values=[[0, 0, 0]], std_values=[
                    [255, 255, 255]],target_platform=TARGET_PLATFORM, optimization_level=0,) 
    
    print('Config model done')

    # Load ONNX model
    print('--> Loading model')
    ret = rknn.load_onnx( model=ONNX_MODEL )   #, inputs=['inputs', 'buffer'], input_size_list=[[514],[27724] ], outputs=['out', 'out_buffer'])  
    rknn.build(do_quantization=True)
    if ret != 0:
        print('Load model failed!')
        exit(ret)
    print('Loading model done')

    # Build model
    print('--> Building model')
    ret = rknn.build(do_quantization=False)
    if ret != 0:
        print('Build model failed!')
        exit(ret)
    print('Building model done')

    # Export RKNN model
    print('--> Export rknn model')
    ret = rknn.export_rknn(RKNN_MODEL)
    if ret != 0:
        print('Export rknn model failed!')
        exit(ret)
    print('Export rknn model done')

    rknn.release()