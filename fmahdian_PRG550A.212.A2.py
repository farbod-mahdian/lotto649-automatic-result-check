#!/home/pi/software/bin/python3
import cgitb
import cgi
import re
import urllib.request
import datetime
print("Content-type: text/html\n\n")


cgitb.enable()


def getWinNums():
    webPage = urllib.request.urlopen("http://www.lottolore.com/lotto649.html")
    webPageText = webPage.read()

    # The line below is required to decode a bytes object into standard unicode
    # str before it can be split( )
    webPageText = webPageText.decode("UTF-8")

    lines = webPageText.split("\n")

    # line counter
    counter = 0
    # regex for the date
    pat = r'>[A-Z][a-z]*, [A-Z][a-z]* \d{1,2}, \d{4}'
    for line in lines:
        counter += 1
        isFound = re.search(pat, line)
        if isFound:
            date_ = isFound.group()[1:]
            break

    winNums = []
    # regex for the winning numbers
    pat1 = r'>\d+<'
    counter += 1
    for i in range(counter, counter + 6):
        isFound = re.search(pat1, lines[i])
        if isFound:
            winNums.append(isFound.group()[1:-1])
    return (winNums, date_)

# Showing GIF numbers


def showGif(list_):
    for num in list_:
        for i in num:
            print('<img src="../images/' + i + '.gif" />', end="")
        print("&nbsp;")

# Sort the lists


def listSort(list_):
    for i in range(len(list_)):
        for j in range(i+1, len(list_)):
            if int(list_[i]) > int(list_[j]):
                tmp = list_[i]
                list_[i] = list_[j]
                list_[j] = tmp
    return list_

# Checking for similar selected numbers


def checkUniq(list_):
    for i in range(len(list_)-1):
        for j in range(i+1, len(list_)):
            if list_[i] == list_[j]:
                return False
    return True


form = cgi.FieldStorage()

color = form.getvalue('bgcolor')
nums = [form.getvalue('userNum1'), form.getvalue('userNum2'), form.getvalue(
    'userNum3'), form.getvalue('userNum4'), form.getvalue('userNum5'), form.getvalue('userNum6')]

print("<html>\n")
print("<head>\n")
print("<title>Number Checking Result</title>\n")
print("</head>\n")
print("<body bgcolor='%s'>\n" % color)

if checkUniq(nums):
    (winNums, recordDate) = getWinNums()
    winNums = listSort(winNums)
    nums = listSort(nums)
    similars = []

    for num in nums:
        for win in winNums:
            if num == win:
                similars.append(num)
                break

    if len(similars) >= 3:
        print("<p>Winning Numbers for " + recordDate + "<br />")
        showGif(winNums)
        print("</p>")
        print("<p>User Selected Numbers:<br />")
        showGif(nums)
        print("</p>")
        print("<p>Numbers Matched: %d <br />" % len(similars))
        showGif(similars)
        print("</p>")
    else:
        print("<p>Sorry, NOT a WINNING TICKET... Please Play Again!</p>")

else:
    print("<p>Sorry, numbers selected must be UNIQUE!</p>")

print("</body>\n")
print("</html>\n")
