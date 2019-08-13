JACK
RUSH
RUSH+
JACK+
MIKE
MIKE+
WLB
WLB+
RILB
LB
ILB



import urllib.request
import urllib.error
import time

def parse_nfl_html(html):
    html_header = 'Player</FONT></TH><TH>GP</TH><TH>GS</TH><TH><A HREF="/football/pro/rosters.nsf/Annual/' + str(
        year) + '-' + team + '-st">Start Pos</TH><TH>Exp</TH><TH>DOB</TH><TH>Ht</TH><TH>Wt</TH><TH>College</TH>'

    split = '">#</A></TH><TH></TH><TH><FONT COLOR=RED>'
    contains_html_header = html.find(split)
    if (contains_html_header < 0):
        return None
    players_html_table = html.split(split)[1].split('</table>')[0]

    if (players_html_table.find(html_header) < 0):
        return None

    # players_csv = players_html_table.replace(html_header, csv_header)
    players_csv = players_html_table.replace(html_header, '')
    players_csv = players_csv.replace('</TR><TR ALIGN=CENTER>', '\n')
    players_csv = players_csv.replace('</TR></TABLE></td></tr>', '')
    players_csv = players_csv.replace('\n<TD>', '\n' + str(year) + ',' + team + ',')
    players_csv = players_csv.replace('</TD><TD ALIGN=RIGHT></TD><TD ALIGN=LEFT><A HREF="/football/pro/players.nsf/ID/',
                                      ',')
    players_csv = players_csv.replace('</TD><TD>', ',')
    players_csv = players_csv.replace('</TD><TD ALIGN=CENTER>', ',')
    players_csv = players_csv.replace('</TD><TD ALIGN=LEFT>', ',')
    players_csv = players_csv.replace('</A>', '')
    players_csv = players_csv.replace('</TD>', '')
    players_csv = players_csv.replace('">', ',')
    players_csv = players_csv.replace('"', ' inches')

    return players_csv


teams = ['arz', 'atl', 'bal', 'buf', 'car', 'chi', 'cin', 'cle', 'dal', 'den', 'det', 'gb', 'hou', 'ind', 'jac', 'kc',
         'sd', 'lac', 'lam', 'mia', 'min', 'ne', 'no', 'nyg', 'nyj', 'oak', 'phi', 'pit', 'stl', 'sf', 'sea', 'tb',
         'ten', 'was']
years = list(range(2015, 2019, 1))

roster_file = open('/Users/Bhill/git/nfl/rosters.csv', 'w')
csv_header = 'yyyy,team,pos,jersey_num,player_id,player,gp,gs,start_pos,nfl_exp,dob,ht,wt,college'
roster_file.write(csv_header)
for year in years:
    year_counter = 0
    for team in teams:
        print('try: ' + str(year) + '-' + team)
        url = 'http://www.jt-sw.com/football/pro/rosters.nsf/Annual/' + str(year) + '-' + str(team)
        try:
            response = urllib.request.urlopen(url)
            html = response.read().decode("utf-8")
            print(url)
            csv = parse_nfl_html(html)
        except urllib.error.HTTPError:
            print('improper team: ' + str(year) + '-' + team)
            continue
        year_counter = year_counter + 1
        print(str(year_counter) + '--' + str(year))
        # print(csv)
        roster_file.flush()
        roster_file.write(csv)
        roster_file.flush()
        time.sleep(3)
        roster_file.flush()

roster_file.flush()
roster_file.close()
