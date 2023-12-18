import tkinter as tk
from tkinter import simpledialog, filedialog, messagebox
from functools import partial
from software_opening_and_function_defination import *

def main():
    root = tk.Tk()
    root.title("Combined Chatbot and AWS Services GUI")
    
    # Set the background color of the main window
    root.configure(bg="lightblue")

    # Create a frame for AWS actions
    action_frame = tk.Frame(root, bg="lightblue")
    action_frame.grid(row=0, column=0, padx=20, pady=20)

    # Create a frame for output text
    output_frame = tk.Frame(root)
    output_frame.grid(row=0, column=1, padx=20, pady=20)

    output_text = tk.Text(output_frame, height=10, width=50)
    output_text.grid(row=0, column=0)

   # Create buttons for different AWS actions
    buttons = [
        ("Create EC2 Instance", partial(create_ec2_instance, output_text)),
        ("Create S3 Bucket", partial(create_s3_bucket, output_text)),
        ("List EC2 Instances", partial(list_ec2_instances, output_text)),
        ("List S3 Buckets", partial(list_s3_buckets, output_text)),
        ("Create SNS Topic", partial(create_sns_topic, output_text)),
        ("List SNS Topics", partial(list_sns_topics, output_text)),
        ("Create IAM User", partial(create_iam_user, output_text)),
        ("Create Lambda Function", partial(create_lambda_function, output_text)),
        ("List Lambda Functions", partial(list_lambda_functions, output_text)),
        ("Invoke Lambda Function", partial(invoke_lambda_function, output_text)),
        ("Upload to S3", partial(upload_to_s3, output_text)),
        ("Download from S3", partial(download_from_s3, output_text)),
        ("Exit", partial(exit_app, root)),
    ]

    for i, (text, command) in enumerate(buttons):
        button = tk.Button(action_frame, text=text, command=command)
        button.grid(row=i, column=0, pady=5, padx=5, sticky="ew")

    # Create labels, radio buttons, text boxes, and buttons for the Chatbot GUI
    command_type_label = tk.Label(root, text="Select input type:")
    command_type_label.grid(row=1, column=0, pady=5)

    command_type = tk.StringVar()
    command_type.set("WRITE")
    write_radio = tk.Radiobutton(root, text="Write", variable=command_type, value="WRITE")
    speak_radio = tk.Radiobutton(root, text="Speak", variable=command_type, value="SPEAK")
    write_radio.grid(row=2, column=0, pady=5)
    speak_radio.grid(row=3, column=0, pady=5)

    command_text_label = tk.Label(root, text="Enter command:")
    command_text_label.grid(row=4, column=0, pady=5)

    command_text = tk.Text(root, height=5, width=50)
    command_text.grid(row=5, column=0, pady=5)

    process_button = tk.Button(root, text="Process Command", command=lambda: process_command(output_text, command_type, command_text))
    process_button.grid(row=6, column=0, pady=5)

    root.mainloop()

if __name__ == "__main__":
    main()
