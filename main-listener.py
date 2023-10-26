import speech_recognition as sr
import requests
import time
import logging
import os

def save_data_to_file(data, filename):
    with open(filename, 'a') as file:
        file.write(data + '\n')

def auto_detect_and_transcribe(server_url, unsent_data_filename):
    r = sr.Recognizer()

    with sr.Microphone() as source:
        print("Listening for microphone input... Press Ctrl+C to exit.")
        try:
            audio = r.listen(source, timeout=10)  # Set Listening time (10 seconds)
            text = r.recognize_google(audio)
            print(f"Detected speech: {text}")

            data = {'text': text}
            try:
                response = requests.post(server_url, json=data)
                if response.status_code == 200:
                    print("Data sent successfully to the server.")
                else:
                    print("Failed to send data to the server. Saving to file.")
                    save_data_to_file(text, unsent_data_filename)
            except requests.exceptions.ConnectionError:
                print("Connection to the server failed. Saving to file.")
                save_data_to_file(text, unsent_data_filename)
        except sr.WaitTimeoutError:
            print("No speech detected within the timeout.")
        except sr.UnknownValueError:
            print("Speech recognition could not understand audio.")
        except KeyboardInterrupt:
            print("Exiting the script.")
            exit()

def send_unsent_data(server_url, unsent_data_filename):
    try:
        with open(unsent_data_filename, 'r') as file:
            unsent_data = file.readlines()
        
        for data in unsent_data:
            data = data.strip()
            data = {'text': data}
            try:
                response = requests.post(server_url, json=data)
                if response.status_code == 200:
                    print(f"Data '{data}' sent successfully to the server.")
                else:
                    print(f"Failed to send data '{data}' to the server.")
                    return  
            except requests.exceptions.ConnectionError:
                print(f"Connection to the server failed for data '{data}'.")
                return  


        open(unsent_data_filename, 'w').close()
        os.remove(unsent_data_filename)
    except FileNotFoundError:
        print(f"'{unsent_data_filename}' does not exist. No unsent data to send.")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    server_url = "http://0.0.0.0:8000"  # Replace with your actual server URL
    unsent_data_filename = "unsent_data.txt"

    while True:
        auto_detect_and_transcribe(server_url, unsent_data_filename)
        send_unsent_data(server_url, unsent_data_filename)
