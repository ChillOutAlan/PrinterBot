from slackclient import SlackClient
import scrapemodnot
import mysql.connector as mariadb
import unicodedata
from datetime import datetime
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
color = "xxx"
bw = 'xxx'

mariadb_connection = mariadb.connect(user='x', password='xxx', database='xxx') # config file
cursor = mariadb_connection.cursor()

def slack_message(message, channel):
    access_token = "xxx" #Also Export Token
    sc = SlackClient(access_token)
    sc.api_call('chat.postMessage', channel=channel, text=message, username='Notifier Bot')

# Notify on Replacing the Ink Cartridge for the Color Printer
def catridge_notification():
    cartridge_list = [scrapemodnot.printer_stats(color)['yellow'],scrapemodnot.printer_stats(color)['cyan'],scrapemodnot.printer_stats(color)['black'], scrapemodnot.printer_stats(color)['magenta']]
    cartridge_names = ["`yellow status`", "`cyan status`", "`black status`", "`magenta status`"]
    cartridge_stats = [scrapemodnot.printer_stats(color)['yellowst'],scrapemodnot.printer_stats(color)['cyanst'],scrapemodnot.printer_stats(color)['blackst'], scrapemodnot.printer_stats(color)['magentast']]
    #COLOR PRINTER Catridge Notifier
    # If Cartridge != DB Row don't push
    for a in range(len(cartridge_list)):
        query_statement = "select {} from COLORPRINTER LIMIT 1;".format(cartridge_names[a])
        cursor.execute(query_statement)
        data = cursor.fetchone()
        data = ''.join(data)
        if data != cartridge_list[a]:
            slack_message("{0}".format(cartridge_stats[a]), "bot-tester")
            update_state = "UPDATE COLORPRINTER SET {0} = '{1}';".format(cartridge_names[a], cartridge_list[a])
            cursor.execute(update_state)
            # Time update
            dt = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            time_statement = "UPDATE COLORPRINTER SET `DATE TIME` = '{0}'".format(dt)
            cursor.execute(time_statement)
            mariadb_connection.commit()
            print("Pushed Message and Updated Database")
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
#drum_stats = [scrapemodnot.printer_stats(color)['yellowdrumst'],scrapemodnot.printer_stats(color)['cyandrumst'],scrapemodnot.printer_stats(color)['blackdrumst'], scrapemodnot.printer_stats(color)['magdrumst']]
def drum_notification():
    cartridge_list = [scrapemodnot.printer_stats(color)['yellowdrum'],scrapemodnot.printer_stats(color)['cyandrum'],scrapemodnot.printer_stats(color)['blackdrum'], scrapemodnot.printer_stats(color)['magdrum'], scrapemodnot.printer_stats(color)['wastebox']]
    cartridge_names = ["`yellow drum status`", "`cyan drum status`", "`black drum status`", "`magenta drum status`", "`wastebox status`"]
    cartridge_stats = [scrapemodnot.printer_stats(color)['yellowdrumst'],scrapemodnot.printer_stats(color)['cyandrumst'],scrapemodnot.printer_stats(color)['blackdrumst'], scrapemodnot.printer_stats(color)['magdrumst'], scrapemodnot.printer_stats(color)['wastebox']]
    #COLOR PRINTER Catridge Notifier
    # If Cartridge != DB Row don't push
    for a in range(len(cartridge_list)):
        query_statement = "select {} from COLORPRINTER LIMIT 1;".format(cartridge_names[a])
        cursor.execute(query_statement)
        data = cursor.fetchone()
        data = ''.join(data)
        if data != cartridge_list[a]:
            slack_message("{0}".format(cartridge_stats[a]), "bot-tester")
            update_state = "UPDATE COLORPRINTER SET {0} = '{1}';".format(cartridge_names[a], cartridge_list[a])
            cursor.execute(update_state)
            # Time update
            dt = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            time_statement = "UPDATE COLORPRINTER SET `DATE TIME` = '{0}'".format(dt)
            cursor.execute(time_statement)
            mariadb_connection.commit()
            print("Pushed Message and Updated Database")
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
#'tray1':tray_response,'tray2':tray2_response, 'tray_status':tray1, 'tray2_status':tray2}
def paper_notfication():
    cartridge_list = [scrapemodnot.printer_stats(color)['tray_response'],scrapemodnot.printer_stats(color)['tray2_response']]
    cartridge_names = ["`TRAY STATUS 1`", "`TRAY STATUS 2`"]
    cartridge_stats = [scrapemodnot.printer_stats(color)['tray_status'],scrapemodnot.printer_stats(color)['tray2_status']]
    #COLOR PRINTER Catridge Notifier
    # If Cartridge != DB Row don't push
    for a in range(len(cartridge_list)):
        query_statement = "select {} from COLORPRINTER LIMIT 1;".format(cartridge_names[a])
        cursor.execute(query_statement)
        data = cursor.fetchone()
        data = ''.join(data)
        if data != cartridge_list[a]:
            slack_message("{0}".format(cartridge_stats[a]), "bot-tester")
            update_state = "UPDATE COLORPRINTER SET {0} = '{1}';".format(cartridge_names[a], cartridge_list[a])
            cursor.execute(update_state)
            # Time update
            dt = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            time_statement = "UPDATE COLORPRINTER SET `DATE TIME` = '{0}'".format(dt)
            cursor.execute(time_statement)
            mariadb_connection.commit()
            print("Pushed Message and Updated Database")
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

if __name__ == '__main__':
    catridge_notification()
    drum_notification()
    paper_notfication()
    mariadb_connection.close()
