#!/usr/bin/python3
import jetson_inference
import jetson_utils

import argparse
import sys
from jetson_inference import imageNet
from jetson_utils import videoSource, videoOutput, cudaFont, Log

# parse the command line
parser = argparse.ArgumentParser(description="Classify a live camera stream using an image recognition DNN.", 
                                 formatter_class=argparse.RawTextHelpFormatter, 
                                 epilog=imageNet.Usage() + videoSource.Usage() + videoOutput.Usage() + Log.Usage())
parser.add_argument("input", type=str, default="", nargs='?', help="URI of the input stream")
parser.add_argument("output", type=str, default="", nargs='?', help="URI of the output stream")
parser.add_argument("--network", type=str, default="models/resnet18.onnx", help="path to the model to use")
parser.add_argument("--labels", type=str, default="models/labels.txt", help="path to the labels file")
parser.add_argument("--input_blob", type=str, default="input_0", help="name of the input blob")
parser.add_argument("--output_blob", type=str, default="output_0", help="name of the output blob")
opt = parser.parse_args()

# Load the custom network
net = imageNet(model=opt.network, labels=opt.labels, input_blob=opt.input_blob, output_blob=opt.output_blob)

input = videoSource(opt.input, argv=sys.argv)
output = videoOutput(opt.output, argv=sys.argv)
font = cudaFont()

# process frames until EOS or the user exits
while True:
    # capture the next image
    img = input.Capture()

    if img is None:  # timeout
        continue  

    classID, confidence = net.Classify(img)

    # draw predicted class labels
    classLabel = net.GetClassLabel(classID)
    confidence *= 100.0

    print(f"imagenet:  {confidence:05.2f}% class #{classID} ({classLabel})")

    font.OverlayText(img, text=f"{confidence:05.2f}% {classLabel}", 
                        x=5, y=5 + 1 * (font.GetSize() + 5),
                        color=font.White, background=font.Gray40)

    # render the image
    output.Render(img)

    # update the title bar
    output.SetStatus("{:s} | Network {:.0f} FPS".format(net.GetNetworkName(), net.GetNetworkFPS()))

    # print out performance info
    net.PrintProfilerTimes()

    # exit on input/output EOS
    if not input.IsStreaming() or not output.IsStreaming():
        break
