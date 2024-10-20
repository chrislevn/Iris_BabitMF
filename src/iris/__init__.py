import bmf
from video_process import PyOCRModule
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

    # output_video = video['video'].module('PyOCRModule')
    # bmf.encode(output_video[0], None, {"output_path": local_output_path}).run()
    
    # original_value = '''
    # {
    #     "name": "John Doe",
    #     "email": "john@doe.com",
    #     "address": "123 Front Street, San Francisco, CA",
    #     "phone": "+1 (415) 123-4567"
    # }
    # '''

    # detected_pii = piiscan.scan(original_value)

    # print(detected_pii)
    

    
if __name__ == "__main__":
    process("src/iris/input/Screen Recording 2024-08-28 at 7.29.39 AM.mov", "output.mp4")
    