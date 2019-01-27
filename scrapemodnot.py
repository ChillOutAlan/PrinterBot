import requests
import lxml.html as lh

#Color Printer
def printer_stats(address):

    #Create a handle, page, to handle the contents of the website
    #Status page URL

    page = requests.get(address)

    #Store the contents of the website under doc
    doc = lh.fromstring(page.content)

    #Parse data that are stored between <tr>..</tr> of HTML
    tr_elements = doc.xpath('//tr')

    #print([len(T) for T in tr_elements[:12]])

    #Create empty list
    col=[]
    i=0
    #For each row, store each first element (header) and an empty list
    for t in tr_elements[0]:
        i+=1
        name=t.text_content()
        #print('%d:"%s"'%(i,name))
        col.append((name))
    #print(col[0])
    str1 = ''.join(col).encode('utf-8').strip() # adding encoding or will have unicode error .encode('utf-8').strip()
    str1 = str1.replace('\r', '') # removes \r from string
    str2 = str1.replace('\n', '') # removes \n from string

    #find the string positions of each of the cartridge levels
    cyanpos = str2.find('Cyan Toner Cartridge Level')
    magentapos = str2.find('Magenta Toner Cartridge Level')
    yellowpos = str2.find('Yellow Toner Cartridge Level')
    blackpos = str2.find('Black Toner Cartridge Level')

    #cartridge level
    cyanst = str2[cyanpos:magentapos]
    magentast = str2[magentapos:yellowpos]
    yellowst = str2[yellowpos:blackpos]
    blackst = str2[blackpos:355] #335 Position

    if "OK" in cyanst:
        cyan = "OK"
    else:
        cyan = "Low"
    if "OK" in magentast:
        magenta = "OK"
    else:
        magenta = "Low"
    if "OK" in yellowst:
        yellow = "OK"
    else:
        yellow = "Low"
    if "OK" in blackst:
        black = "OK"
    else:
        black = "Low"


    #cartridge drum positions
    cyandrumpos = str2.find('Cyan Drum Cartridge')
    magdrumpos = str2.find('Magenta Drum Cartridge')
    yellowdrumpos = str2.find('Yellow Drum Cartridge')
    blackdrumpos = str2.find('Black Drum Cartridge')
    wastedrumpos = str2. find('Waste Toner Box')

    #The Cartridge Drum Levels
    cyandrumst = str2[cyandrumpos:magdrumpos]
    magdrumst = str2[magdrumpos:yellowdrumpos]
    yellowdrumst = str2[yellowdrumpos:blackdrumpos]
    blackdrumst = str2[blackdrumpos:wastedrumpos]
    wasteboxst = str2[wastedrumpos:585] #End when the paper status shows up

    if "OK" in cyandrumst:
        cyandrum = "OK"
    else:
        cyandrum = "Low"
    if "OK" in magdrumst:
        magentadrum = "OK"
    else:
        magentadrum = "Low"
    if "OK" in yellowdrumst:
        yellowdrum = "OK"
    else:
        yellowdrum = "Low"
    if "OK" in blackdrumst:
        blackdrum = "OK"
    else:
        blackdrum = "Low"
    if "OK" in wasteboxst:
        wastebox = "OK"
    else:
        wastebox = "Low"

    #find the string positions of the Paper Capacity
    tray1pos = str2.find('Tray 1')
    tray2pos = str2.find('Tray 2')

    #Paper Level (If string contains ok return paper level is good and if string contains low paper return fill paper)
    tray1 = str2[tray1pos:tray2pos] #
    tray2 = str2[tray2pos:680]
    if "Low" in tray1:
        tray_response = "Low"
    elif "Add" in tray1:
        tray_response = "Add"
    elif "OK" in tray1:
       tray_response = "OK"
    if "Add" in tray2:
        tray2_response = "Add"
    elif "Low" in tray2:
        tray2_response = "Low"
    elif "OK" in tray2:
        tray2_response = "OK"
    return {'yellow': yellow, 'cyan': cyan, 'magenta': magenta, 'black': black, 'yellowdrum': yellowdrum, 'cyandrum': cyandrum, 'magdrum': magentadrum, 'blackdrum': blackdrum,
    'waste':wastebox, 'yellowst': yellowst, 'cyanst': cyan, 'magentast': magentast, 'blackst': blackst,
    'yellowdrumst': yellowdrumst, 'cyandrumst': cyandrumst, 'magdrumst': magdrumst, 'blackdrumst': blackdrumst,
    'wastest':wasteboxst, 'tray1':tray_response,'tray2':tray2_response, 'tray_status':tray1, 'tray2_status':tray2}

#Black and White Printer
def blackandwhite(bw):
    #Create a handle, page, to handle the contents of the website
    page = requests.get(bw)

    #Store the contents of the website under doc
    doc = lh.fromstring(page.content)

    #Parse data that are stored between <tr>..</tr> of HTML
    tr_elements = doc.xpath('//tr')

    #Create empty list
    col=[]
    i=0
    #For each row, store each first element (header) and an empty list
    for t in tr_elements:
        i+=1
        name=t.text_content()
        #print('%d:"%s"'%(i,name))
        col.append((name))

    str1 = ''.join(col)
    str1 = str1.replace('\r', '') # removes \r from string
    str2 = str1.replace('\n', '') # removes \n from string

    #Cartrdige Percentage
    blackpos = str2.find('Black Cartridge')
    perpos = str2.find('%')
    black = str2[blackpos: perpos+1]

    #Paper Levels
    tray1pos = str2.find('Tray 1')
    tray1 = str2[tray1pos:680]
    tray2pos = str2.find('Tray 2')
    tray2 = str2[tray2pos:720]

    #print(tray2)
    if 'OK' in tray1:
        icetray1 = 'OK'
    elif 'Missing' in tray1:
        icetray1 = 'Missing'
    elif 'Low Paper' in tray1:
        icetray1 = 'Low'
    if 'OK' in tray2:
        icetray2 = 'OK'
    elif 'Missing' in tray2:
        icetray2 = 'Missing'
    elif 'Low Paper' in tray2:
        icetray2 = 'Low'
    return {'bl':black, 'i1':icetray1, 'i2':icetray2}
