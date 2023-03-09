import requests
from bs4 import BeautifulSoup as bs
import mysql.connector as mysql

mydb = mysql.connect(
  host="localhost",
  user="root",
  password="******",
  database="samp"
)

mc = mydb.cursor()


url = 'https://gct.ac.in/results'

def getresults(rollno):    
    payload = {'reg_no':rollno}
    resp = requests.post(url,data=payload)
    soup = bs(resp.text,'lxml')

    result_table = soup.find('div',class_='result_tbl')
    tables = result_table.find_all('table',cellpadding= 4)
    title = tables[0].find_all('td')
    reg,name= title[1].text,title[3].text

    sub = []
    res = []
    datas = tables[1].find_all('div',align='center')

    for i in range(len(datas)):
        if i%5 == 0:
            sub.append(datas[i].text)
        elif i%5 == 3:
            res.append(datas[i].text)

    result = {sub[i]:res[i] for i in range(len(sub))}
    result['rno']=reg
    result['name']=name
  
    return result


j = 76
while j<=76:
    try:
        res = getresults('717721111'+(str(j).zfill(2)))

        res1 = {}
        res1['RollNo'] = res['rno']
        res1['Name'] = res['name']

        for i in res.keys():
            if ('30' in i or '3Z' in i or 'VA3' in i) and (res[i]!='--') and (res[i]!='WD'):
                res1[i] = res[i]

        que1 = "insert into sem3c"
        que2 = " (%s" + (",%s"*(len(res1.keys())-1)) + ") "
        que3 = "values"
        att = tuple(res1.keys())
        val = tuple(res1.values())
        que4 = " (" + (", ".join(att)) + ") "
        query = que1+que4+que3+que2        

        print(val)

        mc.execute(query,val)
        mydb.commit()
        j+=1
    
    except:
        print("RNo doesn't exist!")
        j+=1



mc.execute('select * from sem3m')

cred = [3,4,4,3,3,3,0,2,1.5,2]
gpa1 = []
temp = []

for i in mc:
    grade = []
    credits = 0
    for j in range(2,(len(i)-1)):
        if (i[j] is not None) and (i[j]!=0):
            grade.append(int(i[j])*cred[j-2])
            credits += cred[j-2]
    gpa1.append(round((sum(grade)/credits),2))
    temp.append((round((sum(grade)/credits),2),i[0:2]))



que1 = 'update sem3m set gpa = ' 
que3 = ' where RollNo = '

for i in temp:
    que2 = str(i[0])
    que4 = "'"+str(i[1][0])+"'"
    query = que1+que2+que3+que4
    mc.execute(query)
    mydb.commit()
    