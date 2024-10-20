from bmf import Module, Log, LogLevel, InputType, ProcessResult, Packet, Timestamp, scale_av_pts, av_time_base, \
    BmfCallBackType, VideoFrame, AudioFrame
import bmf.hml.hmp as mp
from PIL import Image
import numpy as np
import cv2
import easyocr
import warnings

class PyOCRModule(Module):
    def __init__(self, node, option=None):
        warnings.filterwarnings("ignore", category=UserWarning, message=".*?Your .*? set is empty.*?")
        self.node_ = node
        self.option_ = option
        # Initialize EasyOCR reader
        if torch.cuda.is_available():
            self.reader = easyocr.Reader(['en'], gpu=True, detector='dbnet18')
        else:
            print('warning: GPU is not available, the computation is going to be very slow...')
            self.reader = easyocr.Reader(['en'], detector='dbnet18')
        self.idx = 0
        self.word_dict = {}

    def process(self, task):
        idx = self.idx
        for (input_id, input_packets) in task.get_inputs().items():

            # output queue
            output_packets = task.get_outputs()[input_id]

            while not input_packets.empty():
                pkt = input_packets.get()

                # process EOS
                if pkt.timestamp == Timestamp.EOF:
                    output_packets.put(Packet.generate_eof_packet())
                    task.timestamp = Timestamp.DONE

                # process video frame
                if pkt.timestamp != Timestamp.UNSET and pkt.is_(VideoFrame):
                  vf = pkt.get(VideoFrame)
                  rgb = mp.PixelInfo(mp.kPF_RGB24)
                  np_vf = vf.reformat(rgb).frame().plane(0).numpy()
                  image = Image.fromarray(np_vf.astype('uint8'), 'RGB')

                  frame_ocr_result = self.reader.readtext(np_vf, batch_size=5)
                  for iframe in frame_ocr_result:
                    bbox, text, confidence = iframe
                    if text not in self.word_dict:
                      if str(self.ai_grading(text)["answer"]).upper() == "YES":
                        self.word_dict[text] = []
                        # blur the text region based on the bounding box
                        x1, y1 = bbox[0]
                        x2, y2 = bbox[2]
                        margin = 10  # Set your desired margin here
                        frame_width, frame_height = np_vf.shape[1], np_vf.shape[0]
                        # Consider margins and image boundaries
                        top_left = (max(x1 - margin, 0), max(y1 - margin, 0))
                        bottom_right = (min(x2 + margin, frame_width), min(y2 + margin, frame_height))
                        # Create a mask for the region to be blurred
                        mask = np.zeros(np_vf.shape[:2], dtype=np.uint8)
                        cv2.rectangle(mask, top_left, bottom_right, 255, -1)
                        # Apply the blur to the region using the mask
                        blurred = cv2.GaussianBlur(np_vf, (81, 81), 0)
                        np_vf[mask == 255] = blurred[mask == 255]

                        out_frame_np = np.array(np_vf)
                        rgb = mp.PixelInfo(mp.kPF_RGB24)
                        frame = mp.Frame(mp.from_numpy(out_frame_np), rgb)

                        out_frame = VideoFrame(frame)
                        out_frame.pts = vf.pts
                        out_frame.time_base = vf.time_base

                        pkt = Packet(out_frame)
                        pkt.timestamp = out_frame.pts
                        output_packets.put(pkt)

                    else:
                      self.word_dict[text].append(bbox)
                      # blur the text region based on the bounding box
                      x1, y1 = bbox[0]
                      x2, y2 = bbox[2]
                      margin = 10  # Set your desired margin here
                      frame_width, frame_height = np_vf.shape[1], np_vf.shape[0]
                      # Consider margins and image boundaries
                      top_left = (max(x1 - margin, 0), max(y1 - margin, 0))
                      bottom_right = (min(x2 + margin, frame_width), min(y2 + margin, frame_height))
                      # Create a mask for the region to be blurred
                      mask = np.zeros(np_vf.shape[:2], dtype=np.uint8)
                      cv2.rectangle(mask, top_left, bottom_right, 255, -1)
                      # Apply the blur to the region using the mask
                      blurred = cv2.GaussianBlur(np_vf, (81, 81), 0)
                      np_vf[mask == 255] = blurred[mask == 255]

                      out_frame_np = np.array(np_vf)
                      rgb = mp.PixelInfo(mp.kPF_RGB24)
                      frame = mp.Frame(mp.from_numpy(out_frame_np), rgb)

                      out_frame = VideoFrame(frame)
                      out_frame.pts = vf.pts
                      out_frame.time_base = vf.time_base

                      pkt = Packet(out_frame)
                      pkt.timestamp = out_frame.pts
                      output_packets.put(pkt)


                self.idx += 1
                print("Process frame " + str(self.idx))
                if self.idx == 20:
                  break


        return ProcessResult.OK
