# ASL Vowel Identifier

 This project identifies the position of your left hand and tells you what letter you are signing. 

![Screenshot 2024-07-29 151645](https://github.com/user-attachments/assets/73581012-b43e-417c-a480-d1e9cc0aedb7)

## The Algorithm

The algorithm using ResNet-18 to compare the position of your hand to the dataset of asl vowels and determines which vowel you are signing.  

## Running this project
Requirements:
- jetson-inference 
- jetson-utils


1. Connect a webcam to the Nano.
2. Use the line python3 aslvowels.py <input> <output>
3. Move your head out of the frame and start signing.

[View a video explanation here](https://drive.google.com/file/d/1Nr9DLwQKojnBzSUAuSaDRL9Lil1p8nny/view?usp=sharing)
