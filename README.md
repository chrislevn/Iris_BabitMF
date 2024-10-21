# Iris BabitMF
Iris is a PII removal package based on BabitMF - a cross-platform video proceessing platform from ByteDance. 
This is an on-going project to achive real-time PII and senstive audio detection and removal. 

![Untitled Diagram drawio (1)](https://github.com/user-attachments/assets/75479028-47e0-475f-b5ab-1e5e1d9b57cb)

## Features:
- Detect and remove PII (credit card, phone number, email, etc) from image.

Example (fake ID)
| Before    | After (hiding sensitive number) |
| -------- | ------- |
|<img width="633" alt="Screenshot 2024-10-21 at 11 36 22 AM" src="https://github.com/user-attachments/assets/cb4d8d38-b3a4-4724-8f80-06c2637e1f71">| <img width="735" alt="Screenshot 2024-10-21 at 11 42 52 AM" src="https://github.com/user-attachments/assets/4a94fc88-c020-44fc-a6aa-b518bf5b9ad0">| 
- [WIP] Remove sensive audio with customizable GenAI prompt.

## Usage
- [WIP] Publish as PyPi package. Once the project is finished, you can install it with
`pip install iris`
- To process a video file
```python
from iris import app

app.process(<LOCAL_INPUT_VIDEO_FILE>, <LOCAL_OUTPUT_FILE>)
```

