from Alef_Bot import *
import _thread
from utime import sleep_ms, sleep
from Cards_map import *
from MQTTHandler import MQTTCommandHandler
import Internal_LED


if __name__ == "__main__":
    Internal_LED.ON()
    motor_driver_pins = [6, 7, 27, 26]
    frequency = 1000
    alefbot = AlefBot(motor_driver_pins, frequency, ssid="Orange-Seif", password="t01001007352", repo_url = "https://raw.githubusercontent.com/Seif-El-Dein/tesee/main/", filename= "main.py")
    command = "None"
    alefbot.set_Speed(30)
    server_status = True
    counter = 0
    lock = _thread.allocate_lock()
    try:
        while True:
            alefbot.key = "None"
            alefbot.reset_command()
            if alefbot.command_handler.wifi.isconnected():
                if alefbot.command_handler.Server == False:
                    sleep(20)
                    alefbot.command_handler.reconnect_to_broker()
                    alefbot.command_handler.Server = True
                Internal_LED.ON()
                command = alefbot.waiting_commands()
                if command is None:
                    command = alefbot.reset_command()
            elif not alefbot.command_handler.wifi.isconnected():
                alefbot.command_handler.Server = False
                Internal_LED.ON(delay=0.02)
                Internal_LED.OFF(delay=0.02)
            alefbot.readCard()
            
            if command == "FIRMWARE":
                alefbot.command_handler.download_and_install_update_if_available()
                
            if command == "say about":
                alefbot.play_voiceTrack(language= "Arabic", catagory= "Sentence", track_name="About me")
                sleep(20)
            
            if ',' in command:
                print(command)
                scenario_list = command.split(',')
                print(scenario_list)
                for block in scenario_list:
                    if block == "Forward":
                        alefbot.move_Forward(moving_delay_ms=1000)
                        alefbot.blink_eyes()
                        print(block)

                    elif block == "Backward":
                        alefbot.move_Backward(moving_delay_ms=1000)
                        alefbot.blink_eyes()
                        print(block)
                
                    elif block == "Right":
                        alefbot.look_right()
                        alefbot.turnRight(moving_delay_ms=1000)
                        alefbot.blink_eyes()
                        print(block)
                
                    elif block == "Left":
                        alefbot.look_left()
                        alefbot.turnLeft(moving_delay_ms=1000)
                        alefbot.blink_eyes()
                        print(block)
                    alefbot.Stop(stop_delay_ms=1000)
                 
            if '=' in command:
                equation = command[0:3]
                result = command[4:]
                
                if eval(equation) == int(result):
                    alefbot.play_voiceTrack(language= "English", catagory= "Sentence", track_name="Right Answer")
                    alefbot.trophy()
                else:
                    alefbot.play_voiceTrack(language= "English", catagory= "Sentence", track_name="Try again")
                print(equation)

            if command == "Forward":
                alefbot.move_Forward(moving_delay_ms=200)
                alefbot.blink_eyes()
                print(command)

            elif command == "Backward":
                alefbot.move_Backward(moving_delay_ms=200)
                alefbot.blink_eyes()
                print(command)
                
            elif command == "Right":
                alefbot.look_right()
                alefbot.turnRight(moving_delay_ms=200)
                alefbot.blink_eyes()
                print(command)
                
            elif command == "Left":
                alefbot.look_left()
                alefbot.turnLeft(moving_delay_ms=200)
                alefbot.blink_eyes()
                print(command)
            
            elif alefbot.key == English_words.get("Cat") or command == "CAT":
                alefbot.play_voiceTrack(language= "English", catagory= "Word", track_name="Cat")
                sleep_ms(1000)
                
            elif alefbot.key == Arabic_letters.get("Alef"):
                alefbot.play_voiceTrack(language= "Arabic", catagory= "Letter", track_name="Alef")
                sleep_ms(1000)
            
            else:
                alefbot.Stop()
                
            if alefbot.key == WiFi_reconnect.get("WiFi"):
                alefbot.reconnect_WiFi()
                alefbot.blink_eyes()
                    
            counter +=1
            if counter == 50:
                counter = 0
                lock.acquire()
                thread = _thread.start_new_thread(alefbot.blink_eyes, ())
                lock.release()
                

            
    except KeyboardInterrupt:
        print("Exit test phase")