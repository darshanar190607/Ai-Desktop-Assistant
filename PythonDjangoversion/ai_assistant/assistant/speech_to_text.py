
import speech_recognition as sr

def speech_to_text():
    r = sr.Recognizer()  

    try:
       
        with sr.Microphone() as source:
            print("Adjusting for ambient noise... Please wait.")
            r.adjust_for_ambient_noise(source, duration=1) 

            print("Listening...")
            audio = r.listen(source)  

            print("Processing...")
            voice_data = r.recognize_google(audio) 

            print("You said:", voice_data)
            return voice_data 

    except sr.UnknownValueError:
        print("Sorry, I could not understand the audio.")
        return ""
    except sr.RequestError as e:
        print(f"Could not request results; {e}")
        return ""
    except Exception as e:
        print(f"An error occurred: {e}")
        return ""

if __name__ == "__main__":
    result = speech_to_text()
    print("Recognized Text:", result)
