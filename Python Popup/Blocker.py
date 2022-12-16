from pyuac import main_requires_admin
import time
import os
import wmi
from ischedule import schedule, run_loop
from plyer import notification
import Block_Logic as block

f = wmi.WMI()

expression = "taskkill /f /im "

data = {
    "browsers": [],
    "time": [],

}

# https://steamcommunity.com/sharedfiles/filedetails/?id=1031683053


def timer(seconds):
    t = int(seconds) * 60
    while t > 0:
        i = t % 60
        m = t // 60
        timer = '{:02d}:{:02d}'.format(m, i)
        print(timer, end="\r")
        time.sleep(1)
        t = t - 1

def logic(seconds, browser):
    print("\n"+browser + " Only active for " + str(seconds) + " minutes")
    timer(seconds)
    # notification_bar(browser, seconds)
    extend = "n"
    if(extend == "y" or extend == "Y"):
        timer(15)
        os.system(expression + browser + ".exe")
    else:
        os.system(expression + browser + ".exe")
    print("Okie dokie, Bye Bye")
    notification_bar(browser, seconds)


def application_checker(browser, block=False):
    found = []
    for process in f.Win32_Process():
        if process.Name == browser + ".exe":
            print("Voila, Found The App Running\n")
            found = True
            if(block == True):
                block_logic()
            break
        else:
            found = False
    return found


def block_logic(time = 4):
    data["time"].append(time)
    schedule(block, interval=180)
    run_loop(return_after=data["time"][0])

def block():
    found = False
    browser = data["browsers"][0]
    found = application_checker(browser)
    if found == True:
        os.system(expression + browser + ".exe")
        # notification_bar(browser)
    else:
        print("Cheers, Mate! The App is not running\nCongratulations")


    
    
def notification_bar(browser, seconds=0):
    notification.notify(
        title="PAB blocker",
        message=browser + "blocked successfully" + (seconds),
        # displaying time
        timeout=5)



@main_requires_admin
def main():
    browser = input("Which App do you use ? (All Small Letters) \n")
    data["browsers"].append(browser)
    found = False
    found = application_checker(browser)
    if(found == True):
        seconds = input("Now Tell me the time in Minutes, for how long do you want to use the app ?\n")
        hold = input("Do you want to prevent the app from opening after this session again ? (y/n)\n")
        if(hold == "y" or hold == "Y"):
            time = float(input("How Long do you want to prevent the app from opening ? (in Hours)\n")) * 3600
            logic(seconds, browser)
            block_logic(time)
        else:
            print("Okay, I will restrict App")
            logic(seconds, browser)
    else:
        print("App Not Found\n")
    repeat = input("Do you want to block another app ? (y/n)\n")
    if(repeat == "y" or repeat == "Y"):
        main()
    else:
        print("Okay, Bye Bye")


# The window will disappear as soon as the program exits!

if __name__ == "__main__":
    main()


# 1. Run the program as admin   // Done
# 2. Automatically find the id of the process // Done
# 3. Kill the process after the time limit // Done
# 4. Providing multiple application options to user
# 5. Python Window should not be visible
# 6. Run the Block Code in the Background
# 6. Make it a .exe file
# 7. Make it a GUI


# Advanced
# 1. Add Browser Window Limitar as well
