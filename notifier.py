#!/usr/bin/python3
from slackclient import SlackClient
import scrapemodnot
import mysql.connector as mariadb
import unicodedata
from datetime import datetime
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import os
import re

with open("/home/ubuntu/Documents/PrinterBot/config.txt", "r") as f: # change the directory based on where the file exist
    content = f.readlines()
content = [x.strip() for x in content]

#Add configuration File
color = content[0]
bw = content[1]

mariadb_connection = mariadb.connect(user=content[2], password=content[3], database=content[4]) # config file or Export Token Value
cursor = mariadb_connection.cursor()

def slack_message(message, channel):
    sc = SlackClient(os.environ.get('SLACK_BOT_TOKEN')) #Token Exported into the OS or Environment
    sc.api_call('chat.postMessage', channel=channel, text=message, username='Notifier Bot')

# Notify on Replacing the Ink Cartridge for the Color Printer
def catridge_notification():
    cartridge_list = [scrapemodnot.printer_stats(color)['yellow'],scrapemodnot.printer_stats(color)['cyan'],scrapemodnot.printer_stats(color)['black'], scrapemodnot.printer_stats(color)['magenta']]
    cartridge_names = ["`yellow status`", "`cyan status`", "`black status`", "`magenta status`"]
    cartridge = ["yellow", "cyan", "black", "magenta"]
    cartridge_stats = [scrapemodnot.printer_stats(color)['yellowst'],scrapemodnot.printer_stats(color)['cyanst'],scrapemodnot.printer_stats(color)['blackst'], scrapemodnot.printer_stats(color)['magentast']]
    #COLOR PRINTER Catridge Notifier
    # If Cartridge != DB Row don't push
    for a in range(len(cartridge_list)):
        query_statement = "select {} from COLORPRINTER LIMIT 1;".format(cartridge_names[a])
        cursor.execute(query_statement)
        data = cursor.fetchone()
        data = ''.join(data)
        cartridge_ratio = fuzz.ratio(data, cartridge_list[a]) # Ratio higher than 90% is safe to push message and update database
        if cartridge_ratio < 90 and cartridge_stats[a] != 'OK': #do not push message
            slack_message("{0}".format("{0} cartridge needs to be replaced".format(cartridge[a])), "bot-tester")
            update_state = "UPDATE COLORPRINTER SET {0} = '{1}';".format(cartridge_names[a], cartridge_list[a])
            cursor.execute(update_state)
            # Time update
            dt = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            time_statement = "UPDATE COLORPRINTER SET `DATE TIME` = '{0}'".format(dt)
            cursor.execute(time_statement)
            mariadb_connection.commit()
            print("Pushed Message and Updated Database (Cartridges)")
        else:
            #Push Notification if x > 1 hour and no changes
            query1_statement = "select `DATE TIME` from COLORPRINTER LIMIT 1;"
            cursor.execute(query1_statement)
            newtime = cursor.fetchone()
            olddata = "".join(str(v) for v in newtime)
            date_old = datetime.strptime(olddata,"%Y-%m-%d %H:%M:%S")
            date_new = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            date_new = datetime.strptime(date_new, "%Y-%m-%d %H:%M:%S")
            time = date_new - date_old
            if time.total_seconds() > 18000 and cartridge_list[a] != "OK": # 18000 seconds = 5 hours
                slack_message("{0}".format(cartridge_stats[a]), "bot-tester")
                dt1 = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                time_statement1 = "UPDATE COLORPRINTER SET `DATE TIME` = '{0}'".format(dt1)
                cursor.execute(time_statement1)
                mariadb_connection.commit()
                print("Updated Time in Database!")
    return None

# Give status on Drum if there are issues
def drum_notification():
    cartridge_list = [scrapemodnot.printer_stats(color)['yellowdrum'],scrapemodnot.printer_stats(color)['cyandrum'],scrapemodnot.printer_stats(color)['blackdrum'], scrapemodnot.printer_stats(color)['magdrum'], scrapemodnot.printer_stats(color)['waste']]
    cartridge_names = ["`yellow drum status`", "`cyan drum status`", "`black drum status`", "`magenta drum status`", "`wastebox status`"]
    cartridge = ["yellow", "cyan", "black", "magenta", "waste box"]
    cartridge_stats = [scrapemodnot.printer_stats(color)['yellowdrumst'],scrapemodnot.printer_stats(color)['cyandrumst'],scrapemodnot.printer_stats(color)['blackdrumst'], scrapemodnot.printer_stats(color)['magdrumst'], scrapemodnot.printer_stats(color)['waste']]
    #COLOR PRINTER Catridge Notifier
    # If Cartridge != DB Row don't push
    for a in range(len(cartridge_list)):
        query_statement = "select {} from COLORPRINTER LIMIT 1;".format(cartridge_names[a])
        cursor.execute(query_statement)
        data = cursor.fetchone()
        data = ''.join(data)
        cartridge_ratio = fuzz.ratio(data, cartridge_list[a]) # Case Sensitive 50% match unless partial ratio
        if cartridge_ratio < 90 and cartridge_stats[a] != 'OK':
            slack_message("{0}".format("{0} drum needs to be replaced".format(cartridge[a])), "bot-tester")
            update_state = "UPDATE COLORPRINTER SET {0} = '{1}';".format(cartridge_names[a], cartridge_list[a])
            cursor.execute(update_state)
            # Time update
            dt = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            time_statement = "UPDATE COLORPRINTER SET `DATE TIME` = '{0}'".format(dt)
            cursor.execute(time_statement)
            mariadb_connection.commit()
            print("Pushed Message and Updated Database (Drums Status)")
        else:
            #Push Notification if x > 1 hour and no changes
            query1_statement = "select `DATE TIME` from COLORPRINTER LIMIT 1;"
            cursor.execute(query1_statement)
            newtime = cursor.fetchone()
            olddata = "".join(str(v) for v in newtime)
            date_old = datetime.strptime(olddata,"%Y-%m-%d %H:%M:%S")
            date_new = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            date_new = datetime.strptime(date_new, "%Y-%m-%d %H:%M:%S")
            time = date_new - date_old
            if time.total_seconds() > 18000 and cartridge_list[a] != "OK": # 18000 seconds = 5 hours
                slack_message("{0}".format(cartridge_stats[a]), "bot-tester")
                dt1 = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                time_statement1 = "UPDATE COLORPRINTER SET `DATE TIME` = '{0}'".format(dt1)
                cursor.execute(time_statement1)
                mariadb_connection.commit()
                print("Updated Time in Database!")
    return None

# Tray Status for Color PRINTER
def paper_notfication():
    cartridge_list = [scrapemodnot.printer_stats(color)['tray1'],scrapemodnot.printer_stats(color)['tray2']]
    cartridge_names = ["`TRAY STATUS 1`", "`TRAY STATUS 2`"]
    cartridge_stats = [scrapemodnot.printer_stats(color)['tray_status'],scrapemodnot.printer_stats(color)['tray2_status']]
    #COLOR PRINTER Catridge Notifier
    # If Cartridge != DB Row don't push
    for a in range(len(cartridge_list)):
        query_statement = "select {} from COLORPRINTER LIMIT 1;".format(cartridge_names[a])
        cursor.execute(query_statement)
        data = cursor.fetchone()
        data = ''.join(data)
        cartridge_ratio = fuzz.ratio(data, cartridge_list[a]) # Case Sensitive 50% match unless partial ratio
        if cartridge_ratio < 90 and cartridge_stats != 'OK':
            slack_message("{0}".format('For the Color Printer Add Paper to Tray {0}'.format(a+1)), "bot-tester")
            update_state = "UPDATE COLORPRINTER SET {0} = '{1}';".format(cartridge_names[a], cartridge_list[a])
            cursor.execute(update_state)
            # Time update
            dt = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            time_statement = "UPDATE COLORPRINTER SET `DATE TIME` = '{0}'".format(dt)
            cursor.execute(time_statement)
            mariadb_connection.commit()
            print("Pushed Message and Updated Database (Paper Status)")
        else:
            #Push Notification if x > 1 hour and no changes
            query1_statement = "select `DATE TIME` from COLORPRINTER LIMIT 1;"
            cursor.execute(query1_statement)
            newtime = cursor.fetchone()
            olddata = "".join(str(v) for v in newtime)
            date_old = datetime.strptime(olddata,"%Y-%m-%d %H:%M:%S")
            date_new = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            date_new = datetime.strptime(date_new, "%Y-%m-%d %H:%M:%S")
            time = date_new - date_old
            new_ratio = fuzz.partial_ratio(cartridge_list[a], "Add")
            if time.total_seconds() > 18000 and new_ratio == 100: # 18000 seconds = 5 hours
                slack_message("{0}".format('Please add Paper to Tray {0}'.format(a+1), "bot-tester"))
                dt1 = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                time_statement1 = "UPDATE COLORPRINTER SET `DATE TIME` = '{0}'".format(dt1)
                cursor.execute(time_statement1)
                mariadb_connection.commit()
                print("Updated Time in Database!")
    return None

# Tray Status and ink status for black and white printer
def bw_notfication(): #threshold is 0% for ink and missing for paper
    cartridge_list = [scrapemodnot.blackandwhite(bw)['i1'],scrapemodnot.blackandwhite(bw)['i2']]
    cartridge_names = ["`TRAY 1 STATUS`", "`TRAY 2 STATUS`"]
    #COLOR PRINTER Catridge Notifier
    # If Cartridge != DB Row don't push
    bwlevel = scrapemodnot.blackandwhite(bw)['black']
    percentage_ink = int(re.search(r'\d+', bwlevel).group())
    query1_statement = "select `DATE TIME` from BWPRINTER LIMIT 1;"
    cursor.execute(query1_statement)
    newtime = cursor.fetchone()
    olddata = "".join(str(v) for v in newtime)
    date_old = datetime.strptime(olddata,"%Y-%m-%d %H:%M:%S")
    date_new = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    date_new = datetime.strptime(date_new, "%Y-%m-%d %H:%M:%S")
    time = date_new - date_old
    query_update = "UPDATE BWPRINTER SET `INK LEVEL` = {}".format(percentage_ink)
    cursor.execute(query_update)
    if percentage_ink < 0 and time.total_seconds() > 18000:
        slack_message("Replace the Cartridge", "bot-tester")
        update_state = "UPDATE BWPRINTER SET {0} = '{1}';".format(cartridge_names[a], cartridge_list[a])
        cursor.execute(update_state)
        # Time update
        dt = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        time_statement = "UPDATE BWPRINTER SET `DATE TIME` = '{0}'".format(dt)
        cursor.execute(time_statement)
        mariadb_connection.commit()
    for a in range(len(cartridge_list)):
        query_statement = "select {} from BWPRINTER LIMIT 1;".format(cartridge_names[a])
        cursor.execute(query_statement)
        data = cursor.fetchone()
        data = ''.join(data)
        cartridge_ratio = fuzz.ratio(data, cartridge_list[a]) # Case Sensitive 50% match unless partial ratio
        if cartridge_ratio < 90 and cartridge_list != 'OK':
            slack_message("{0}".format('For Black and White Printer Add Paper to Tray {0}'.format(a+1)), "bot-tester")
            update_state = "UPDATE BWPRINTER SET {0} = '{1}';".format(cartridge_names[a], cartridge_list[a])
            cursor.execute(update_state)
            # Time update
            dt = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            time_statement = "UPDATE BWPRINTER SET `DATE TIME` = '{0}'".format(dt)
            cursor.execute(time_statement)
            mariadb_connection.commit()
            print("Pushed Message and Updated Database (Paper Status)")
        else:
            #Push Notification if x > 1 hour and no changes
            query1_statement = "select `DATE TIME TRAY` from BWPRINTER LIMIT 1;"
            cursor.execute(query1_statement)
            newtime = cursor.fetchone()
            olddata = "".join(str(v) for v in newtime)
            date_old = datetime.strptime(olddata,"%Y-%m-%d %H:%M:%S")
            date_new = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            date_new = datetime.strptime(date_new, "%Y-%m-%d %H:%M:%S")
            time = date_new - date_old
            new_ratio = fuzz.partial_ratio(cartridge_list[a], "Missing")
            if time.total_seconds() > 18000 and new_ratio == 100: # 18000 seconds = 5 hours
                slack_message("{0}".format('Please add Paper to Tray {0}'.format(a+1), "bot-tester"))
                dt1 = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                time_statement1 = "UPDATE BWPRINTER SET `DATE TIME TRAY` = '{0}'".format(dt1)
                cursor.execute(time_statement1)
                mariadb_connection.commit()
                print("Updated Time in Database!")
    return None

if __name__ == '__main__':
    catridge_notification()
    drum_notification()
    paper_notfication()
    bw_notfication()
    mariadb_connection.close()
    file.close(f)
