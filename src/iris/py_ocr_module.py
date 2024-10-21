from bmf import Module, Log, LogLevel, InputType, ProcessResult, Packet, Timestamp, scale_av_pts, av_time_base, \
    BmfCallBackType, VideoFrame, AudioFrame
import easyocr
import numpy as np
import bmf.hml.hmp as mp
from bmf.lib._bmf import sdk
from bmf.lib._bmf.sdk import ffmpeg
import cv2
import io
import torch
import warnings
from PIL import Image
from bmf.builder.ff_filter import decode
import json
from presidio_image_redactor import ImageRedactorEngine
from PIL import Image


class py_ocr_module(Module):
    def __init__(self, node, option=None):
        print(f'ocr_module init ...')
        warnings.filterwarnings("ignore", category=UserWarning, message=".*?Your .*? set is empty.*?")
        self.node_ = node
        self.option_ = option
        self.idx = 0
        self.word_dict = {}
        self.engine = ImageRedactorEngine()


    def process(self, task):
        for (input_id, input_packets) in task.get_inputs().items():

            # output queue
            output_packets = task.get_outputs()[input_id]

            while not input_packets.empty():
                pkt = input_packets.get()

                # process EOS
                if pkt.timestamp == Timestamp.EOF:
                    Log.log_node(LogLevel.DEBUG, task.get_node(), "Receive EOF")
                    output_packets.put(Packet.generate_eof_packet())
                    task.timestamp = Timestamp.DONE
                    return ProcessResult.OK
                
                video_frame = pkt.get(VideoFrame)
                # use ffmpeg
                frame = ffmpeg.reformat(video_frame, "rgb24").frame().plane(0).numpy()

                output, _ = self.engine.redact(frame, (255, 192, 203))
                # process packet if not empty
                if pkt.timestamp != Timestamp.UNSET and pkt.is_(VideoFrame):

                    vf = pkt.get(VideoFrame)
                    dst_md = sdk.MediaDesc().pixel_format(mp.kPF_RGB24)
                    np_vf = sdk.bmf_convert(vf, sdk.MediaDesc(), dst_md).frame().plane(0).numpy()

                    # numpy to PIL
                    image = Image.fromarray(np_vf.astype('uint8'), 'RGB')

                    redacted_image = self.engine.redact(image, (255, 192, 203)) # Redact with pink

                    output = np.ascontiguousarray(output)
                    rgbformat = mp.PixelInfo(mp.kPF_RGB24)
                    image = mp.Frame(mp.from_numpy(output), rgbformat)

                    output_frame = VideoFrame(image)
                    Log.log_node(LogLevel.DEBUG, self._node, "output video frame")

                    output_frame.pts = video_frame.pts
                    output_frame.time_base = video_frame.time_base
                    output_pkt = Packet(output_frame)
                    output_pkt.timestamp = pkt.timestamp
                    if output_packets is not None:
                        output_packets.put(output_pkt)
        return ProcessResult.OK