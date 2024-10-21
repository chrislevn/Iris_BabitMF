import bmf
import requests
import json


def process(local_input_path: str, local_output_path: str):
    """
    Process a video file to detect and remove PII.
    
    Args: 
        local_video_path (str): The path to the video file.
        local_output_path (str): The path to save the output video
        
    """
    graph = bmf.graph()
    video = graph.decode({"input_path": local_input_path})
    output_video = video['video'].module('py_ocr_module')

    bmf.encode(output_video[0], None, {"output_path": local_output_path}).run()

    
if __name__ == "__main__":
    process("src/iris/input/Screen Recording 2024-08-28 at 7.29.39 AM.mov", "output.mp4")
    