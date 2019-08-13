import urllib.request
import mysql.connector
import time
import random

mydb = mysql.connector.connect(
    host="ai",
    user="db_user",
    passwd="db_password",
    database="dataiku"
)

mycursor = mydb.cursor()

query = """
SELECT DISTINCT purl, playerName, playerId from NFL_player_url order by purl
"""

mycursor.execute(query)
myresult = mycursor.fetchall()

count = 0
for purl in myresult:
    count = count + 1

csv = open('position_scrape.csv', 'w')

header = 'sort_id,name,player_id,url,pos,draft_round,draft_overall,draft_year,college,agent\n'
csv.write(header)
print(header)

for row in myresult:
    url = row[0]
    name = row[1]
    player_id = row[2]
    url.replace("'", "")  # remove apostrophes from names

    response = urllib.request.urlopen(url)
    html_bytes = response.read()
    html = str(html_bytes, 'utf-8')
    end_span = '</span>'

    pos = 'failed'
    draft_round = -1
    draft_overall = -1
    draft_year = -1
    college = 'failed'

    try:
        college_split_1 = '<strong>College:</strong>'
        college = html.split(college_split_1)[1].split(end_span)[0]

        agent_split_1 = '<span class="player-item"><strong>Agent(s):</strong>'
        agent = html.split(agent_split_1)[1].split(end_span)[0]

        pos_split_1 = '<span class="player-item position">'
        pos = html.split(pos_split_1)[1].split(end_span)[0]

        if '<strong>Undrafted:</strong>' in html:
            draft_round = 0
            draft_overall = 0
            draft_year = html.split('<strong>Undrafted:</strong> ')[1].split(end_span)[0].split(',')[0]
            draft_team = html.split('<strong>Undrafted:</strong> ')[1].split(end_span)[0].split(',')[1]
        else:
            draft_split_1 = '<strong>Drafted:</strong>'
            draft_info = html.split(draft_split_1)[1].split(end_span)[0]
            draft_info.replace('Round ', '')
            draft_round = draft_info.replace('Round ', '').split(' ')[1]
            draft_overall = draft_info.split('#')[1].split('overall')[0]
            draft_year = draft_info.split(', ')[1]

    except:
        print('FAIL ', url)

    line = str(count).strip() + ',"' +  name.strip() + '",' + str(player_id).strip() + ',"' + url.strip() + '","' + pos.strip() + '",' + str(draft_round).strip() + ','  + str(draft_overall).strip() + ',' + str(draft_year).strip() + ',"' + college.strip() + '","' + agent.strip() + '"\n'
    print(line)
    csv.write(line)
    count = count - 1

    sleep_secs = random.randint(0, 3)
    # print('sleeping: ', sleep_secs)
    time.sleep(sleep_secs)

csv.flush()
csv.close()
