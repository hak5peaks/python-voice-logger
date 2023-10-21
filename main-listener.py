import speech_recognition as sr
import requests
import time

def auto_detect_and_transcribe(server_url):
    r = sr.Recognizer()

    with sr.Microphone() as source:
        print("Listening for microphone input...")
        try:
            audio = r.listen(source)
            text = r.recognize_google(audio)
            print(f"Detected speech: {text}")

            data = {'text': text}
            response = requests.post(server_url, json=data)
            if response.status_code == 200:
                print("Data sent successfully to the server.")
            else:
                print("Failed to send data to the server.")
        except sr.WaitTimeoutError:
            print("No speech detected within the timeout.")
        except sr.UnknownValueError:
            print("Speech recognition could not understand audio.")

if __name__ == "__main__":
    server_url = "http://0.0.0.0:8000"  # Replace with your actual server URL
    while True:
        auto_detect_and_transcribe(server_url)
