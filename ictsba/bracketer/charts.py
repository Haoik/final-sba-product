from bracketer import app,db,bcrypt,admin
from flask import render_template,redirect,url_for,session,request


from sqlalchemy import func 
from bracketer.forms import progress, reset,  setcolor 
from bracketer.models import schools , chart2024 , chart2023 , chartinfo 
from math import ceil , log2
import numpy



def createteam(chartyear): 
    #chart generating algorithm , return an array with proper arrangement      
    teams = [[]*4 for i in range(4)]
    rank4 = []
    def moveteam(num , team,  bye):  
        if len(teams[3-num]) != groupamount:
            lastspace = 3-num
        else:
            lastspace = num
        movedto = -999
        i = 0
        addbye = False
        while movedto == -999 and i != 2:# while hvnt moved
            j = 0
            index = -999
            #first check position[j] , then j-2 then 3-j lastly j
            checkteam = [position[num] , num-2]
            while j != len(teams[checkteam[i]]): #while not all teams inside that block is checked 
                if teams[checkteam[i]][j]['sid'] == None: #if a bye is found
                    movedto = checkteam[i]
                    index = j
                    addbye = True 
                j += 1 
            i += 1
        #if confirmed other blocks hv byes , add to that block and add bye in lastspace's bye , else append block to lastspace
        if addbye == True:
            teams[movedto][index] = team
            teams[lastspace].append(bye)
        else:
            teams[lastspace].append(team)
    #get amount = total player that hvnt losed
    amount = db.session.query(chartyear).count()
    if amount == 1: #if theres only one team 
        champion = db.session.query(chartyear.SID,chartyear.TID).all()
        name = db.session.query(schools.NAME).filter(schools.SID == champion[0][0]).all()

        newteam = { 'name':f'{name[0][0]} Team {champion[0][1]}',
                                    'sid': champion[0][0],
                                    'tid': champion[0][1],
                                    'eliminated':  False
                                }
        teams[0].append(newteam)
    else: #if there are more then one team , start arranging the teams
        #variable declarations : byes (amount of byes remaining to add) totalbyes (total amount of byes)  groupamount (each group's number of schools) position (used when adding team two)
        byes = 2**ceil(log2(amount)) - amount
        totalbyes = byes
        amount = amount + byes
        groupamount = amount//4
        position = [1,0,3,2]
        byedict = {'name':'bye' ,'sid':None , 'tid':None, 'eliminated': True}
    #get sid of rank 4 last year and store in rank4
        if chartyear == chart2024:
            top4 = db.session.query(chart2023.SID).order_by(chart2023.WON.desc()).limit(4).all() 
            for i in range(len(top4)):
                if top4[i][0] not in rank4: #only distinct sid is added
                    rank4.append(top4[i][0]) 
        db.session.query(chart2024).filter(chart2024.SID.notin_(rank4)).update({chart2024.SEED:0})   
        db.session.query(chart2024).filter(chart2024.SID.in_(rank4) , chart2024.TID == 2).update({chart2024.SEED:0}) 
        db.session.commit()    
        #first step add seeded team 's team one 
        j = -1
        for i in range(len(rank4)):
            seeded_school = db.session.query(schools.NAME , schools.SID).filter(schools.SID == chartyear.SID , schools.SID == rank4[i]).distinct().all() #0,1,2,3            
            if seeded_school:
                
                    j += 1
 
                    
                    newteam = { 'name':f'{seeded_school[0][0]} Team one seed {j+1} ', 
                                'sid': str(seeded_school[0][1]),
                                'tid': 1,
                                'eliminated': False
                    }                          
                    #update seed 
                    db.session.query(chart2024).filter(chart2024.SID == str(seeded_school[0][1]) , chart2024.TID == 1).update({chart2024.SEED:j+1})  
                    db.session.commit()
                    if len(teams[j])!=groupamount: #if the block have no space choose the next block to have the seed player
                        teams[j].append(newteam)
                    else:
                        teams[j+1].append(newteam)
                    if byes != 0:         
                        db.session.commit()
                        if len(teams[j]) != groupamount: #there are chance bye needs to be add but the block it self hv no space
                            teams[j].append(byedict)
                        elif len(teams[3-j]) != groupamount:
                            teams[3-j].append(byedict) 
                        elif len(teams[position[j]]!= groupamount):
                            teams[position[j]].append(byedict)
                        else:
                            teams[j-2].append(byedict)
                        byes -= 1
        #second step add seeded team 's team two                
        j = -1
        for i in range(len(rank4)):
            seeded_school = db.session.query(schools.NAME , schools.SID).filter(schools.SID == chartyear.SID , schools.SID == rank4[i]).distinct().all() #0,1,2,3
            #first step
            if seeded_school:
                j += 1
                if db.session.query(chartyear).where(chartyear.SID == seeded_school[0][1]).count() == 2:
                    
                        newteam = { 'name':f'{seeded_school[0][0]} Team two',
                                    'sid': str(seeded_school[0][1]),
                                    'tid': 2,
                                    'eliminated':  False
                                }
                        if totalbyes > 4 and byes != 0:
                            newbye = byedict                           
                            db.session.commit()
                            byes -= 1
                        else:
                            newbye = None
                        if len(teams[j-2]) != groupamount: #if the school added if two team , add to the furtherest block which have space:   
                            teams[j-2].append(newteam)
                            if newbye != None and len(teams[j-2]) != groupamount :
                                teams[j-2].append(newbye)
                        elif len(teams[position[j]]) != groupamount:
                            teams[position[j]].append(newteam)
                            if newbye != None and len(teams[j]) != groupamount:
                                teams[position[j]].append(newbye)
                        else:
                            moveteam(j, newteam , byedict)
        # second step (add bye or player until each block is power of two)
        # find the name , sid , tid of the remaining schools 
        remaining_school = db.session.query(chartyear.SID , chartyear.TID ).filter( chartyear.SID.notin_(rank4)).group_by(chartyear.SID, chartyear.TID).order_by(func.count(chartyear.SID).desc()).all()
        print(remaining_school)
        # it will be something like [(name,sid)......] 
        print('139',teams,byes,totalbyes) 
        while byes != 0 or remaining_school:
            
            blocknum = 0
            # go through each block and see if it is even or not , if not : add things
            while blocknum != 4:

                if len(teams[blocknum]) != groupamount or amount == 2: 
    
                
                    if len(teams[blocknum]) %2 != 0 and byes != 0  :
                            print(blocknum)     #the block contains things + odd = need byes
                            print(byes)
                            print("hiiiiiiiiiiiiiiiiiiiiiiiiii")
                            newbye = {'name':'bye' ,'sid':None , 'tid':None, 'eliminated': True}
                            teams[blocknum].append(newbye)
                            byes -= 1                        
                    elif remaining_school: #if there are teams hvnt been added
                            print('remain',remaining_school)
                            print('teams',teams)
                            #if there are schools that hv team two 
                            name = db.session.query(schools.NAME).filter(schools.SID == remaining_school[0][0]).all()[0][0]
                            if db.session.query(chartyear).where(chartyear.SID == remaining_school[0][0] ).count() == 2 and remaining_school[0][1] == 1:
                                    
                                    newteam = { 'name':f'{name} Team one',
                                        'sid': remaining_school[0][0],
                                        'tid': remaining_school[0][1],
                                        'eliminated': False
                                    }
                                    teams[blocknum].append(newteam)
                                    if byes != 0 and len(teams[blocknum])!= groupamount:
                                        teams[blocknum].append(byedict)
                                        byes -= 1
                                    remaining_school.pop(0)
                                    newteam = { 'name':f'{name} Team two',
                                            'sid': remaining_school[0][0],
                                            'tid': remaining_school[0][1],
                                            'eliminated':  False
                                        }
                                    
                                
                                    if len(teams[blocknum-2]) != groupamount: #if the school added if two team , add to the furtherest block which have space:
                                            teams[blocknum-2].append(newteam)
                                            if byes != 0 and len(teams[blocknum-2])!= groupamount:
                                                teams[blocknum-2].append(byedict)
                                                byes -= 1
                                    elif len(teams[position[blocknum]]) != groupamount:
                                            teams[position[blocknum]].append(newteam)
                                            if byes != 0 and len(teams[position[blocknum]])!= groupamount:
                                                teams[position[blocknum]].append(byedict)
                                                byes -= 1
                                    else:
                                        moveteam(blocknum,newteam,byedict)  
                                    remaining_school.pop(0)               
                            
                            else: #if no two team 
                                    
                                    if remaining_school[0][1] == 1: #if is team one
                                        newteam = { 'name':f'{name} Team one',
                                            'sid': remaining_school[0][0],
                                            'tid': remaining_school[0][1],
                                            'eliminated': False
                                            }
                                    else: #if is team two
                                        newteam = { 'name':f'{name} Team two',
                                            'sid': remaining_school[0][0],
                                            'tid': remaining_school[0][1],
                                            'eliminated': False
                                            }
                                    teams[blocknum].append(newteam)
                                    remaining_school.pop(0)

                                    if byes != 0 and len(teams[blocknum])!= groupamount:
                                        teams[blocknum].append(byedict)
                                        byes -= 1

                         #next time will not add the same school
                blocknum += 1
    ## rearrange block four as the second block (block four must be the block with the least seed)
    teams.insert(1,teams.pop(3))
    ##flattening the 2d array using numpy and also remove null values 
    teams = list(numpy.concatenate(teams).flat)
    #change all byed team to won
    for team in range(len(teams)):
        if teams[team]['sid'] == None:
            byedsid = teams[team-1]['sid']
            byedtid = teams[team-1]['tid']
            db.session.query(chartyear).filter(chartyear.SID == byedsid , chartyear.TID == byedtid).update({'WON':chartyear.WON + 1})
    db.session.commit() 
    return teams , amount

#select which chart to view
def continueteam(previousteam,turn):
    oldchart = previousteam[turn-1]
    newchart = []
    for i in range (len(oldchart)):
        if oldchart[i]['eliminated'] == False:
            newchart.append(oldchart[i])
    return newchart , len(newchart)

@app.route('/chartselect' , methods=['GET', 'POST'])
def chartselect():
     flash = session.pop('flash', None)
     return render_template('chartselect.html' , flash = flash)

@app.route('/chart' , methods=['GET', 'POST'])

def chart():
    session.pop('flash',None)
    if db.session.query(chart2024).first():
        session['nowchart'] = 2024
        form = progress()
        doreset = reset()
        colors = setcolor()
        if 'charts' not in session:
            session['charts'] = []
        if 'losers' not in session:
            session['losers']=[]
        if 'rotated' not in session:
            session['rotated']= False
        if 'color' not in session:
            session['color']= 'black'

        if db.session.query(chartinfo).filter(chartinfo.ID == 2024).count() == 0:  #add chartinfo if a chart hvnt been created
            newchart = chartinfo(ID = 2024, TURN = 0, AMOUNT = 0)
            db.session.add(newchart)
            db.session.commit()

        turn = db.session.query(chartinfo.TURN).filter(chartinfo.ID == 2024).all()[0][0]

        if len(session['charts']) != turn + 1:

            if turn == 0:
                newteam , newamount = createteam(chart2024)
                session['charts'].append(newteam)
                db.session.query(chartinfo).filter(chartinfo.ID == 2024).update({ 'AMOUNT': newamount })
                db.session.commit()
            else:
                newteam , newamount = continueteam(session['charts'],turn)
                session['charts'].append(newteam)
                db.session.query(chartinfo).filter(chartinfo.ID == 2024).update({ 'AMOUNT': newamount })
                db.session.commit()

        if form.validate_on_submit() and form.wontid.data:

            tidwon = int(form.wontid.data.strip())
            sidwon = form.wonsid.data.strip()
            sidlose = form.losesid.data.strip()
            tidlose = int(form.losetid.data.strip())
            if isinstance(sidwon, int):
                sidwon = str(sidwon)
            if isinstance(sidlose, int):
                sidlose = str(sidlose)  
            print(sidwon,tidwon,sidlose,tidlose)
            db.session.query(chart2024).filter(chart2024.SID == sidwon, chart2024.TID == tidwon).update({'WON': chart2024.WON + 1})
            print('hidasfasdfasdfdsafsdaf')
            db.session.commit()
           
            session['losers'].append([sidlose,tidlose])
            session.modified = True
            for team in session['charts'][turn]: # turn eliminated to true 
                    print(team)
                    if team['sid'] == sidlose and team['tid'] == tidlose:
                        team['eliminated'] = True
                        session.modified = True
            return redirect(url_for('chart'))
        elif request.method == 'POST':
            return redirect(url_for('chart') )
            
        if db.session.query(chart2024).filter(chart2024.WON == turn + 1).count() == db.session.query(chartinfo.AMOUNT).filter(chartinfo.ID == 2024).all()[0][0] // 2 and db.session.query(chartinfo.AMOUNT).filter(chartinfo.ID == 2024).all()[0][0] != 1: 
            #if teams with won not equal to turn (e.g. turn 0 hv one win) , that means they won. if all win (winning team equal to amount/2) , new turn can be generated
            for loser in session['losers']:
                db.session.query(chart2024).filter(chart2024.SID == loser[0], chart2024.TID == loser[1]).update({'LOSE': True})
                db.session.commit()
            db.session.query(chartinfo).filter(chartinfo.ID == 2024).update({ 'TURN': chartinfo.TURN + 1 })
            db.session.commit()
            session['losers']=[]
            return redirect(url_for('chart'))
        db.session.commit()
    
        return render_template('chart.html' , teams = session['charts'], form = form , doreset = doreset, createteam = createteam , errors = doreset.errors , colors = colors) #
    else:
        session['flash'] = 'The chart is empty!'
        return redirect(url_for('chartselect'))

@app.route('/chartlastyear' , methods=['GET', 'POST'])

def chartlastyear():
    session.pop('flash',None)
    if db.session.query(chart2023).first():
        session['nowchart'] = 2023
        form = progress()
        doreset = reset()
        colors = setcolor()
        print(session['rotated'])
        if 'charts2023' not in session:
            session['charts2023'] = []
        if 'losers2023' not in session:
            session['losers2023']=[]
        if 'rotated' not in session:
            session['rotated']= False
        if 'color' not in session:
            session['color']= 'black'
        
        if db.session.query(chartinfo).filter(chartinfo.ID == 2023).count() == 0:  #add chartinfo if a chart hvnt been created
            newchart = chartinfo(ID = 2023, TURN = 0, AMOUNT = 0)
            db.session.add(newchart)
            db.session.commit()

        turn = db.session.query(chartinfo.TURN).filter(chartinfo.ID == 2023).all()[0][0]
        print('305',turn)
        if len(session['charts2023']) != turn + 1:
            if turn == 0:
                newteam , newamount = createteam(chart2023)
                print(newteam)
                session['charts2023'].append(newteam)
                db.session.query(chartinfo).filter(chartinfo.ID == 2023).update({ 'AMOUNT': newamount })
                db.session.commit()
            else:
                print(session['charts2023'])
                newteam , newamount = continueteam(session['charts2023'],turn)
                session['charts2023'].append(newteam)
                db.session.query(chartinfo).filter(chartinfo.ID == 2023).update({ 'AMOUNT': newamount })
                db.session.commit()
        if form.validate_on_submit() and form.wontid.data:
            db.session.query(chart2024).update({'LOSE': False}) ## if changed chart2023, chart2024 must be reset
            db.session.query(chart2024).update({'WON':0})
            db.session.commit()
            db.session.query(chartinfo).filter(chartinfo.ID == 2024).delete()
            db.session.commit()
            session.pop('charts', None)
            session.pop('losers', None)
            tidwon = int(form.wontid.data.strip())
            sidwon = form.wonsid.data.strip()
            sidlose = form.losesid.data.strip()
            tidlose = int(form.losetid.data.strip())
            if isinstance(sidwon, int):
                sidwon = str(sidwon)
            if isinstance(sidlose, int):
                sidwon = str(sidlose)  
            db.session.query(chart2023).filter(chart2023.SID == sidwon, chart2023.TID == tidwon).update({'WON': chart2023.WON + 1})
            db.session.commit()
            session['losers2023'].append([sidlose,tidlose])
            session.modified = True
            for team in session['charts2023'][turn]: # turn eliminated to true 
                    print(team['sid'])
                    if team['sid'] == sidlose and team['tid'] == tidlose:
                        team['eliminated'] = True
                        session.modified = True
            return redirect(url_for('chartlastyear'))
        elif request.method == 'POST':
            session['message'] = 'Please choose a winning team!'
            session['redirect'] =  url_for('chartlastyear') 
    else: 
        session['flash'] = 'The chart is empty!'
        return redirect(url_for('chartselect'))

        
    if db.session.query(chart2023).filter(chart2023.WON == turn + 1).count() == db.session.query(chartinfo.AMOUNT).filter(chartinfo.ID == 2023).all()[0][0] // 2 and db.session.query(chartinfo.AMOUNT).filter(chartinfo.ID == 2023).all()[0][0] != 1: 
        #if teams with won not equal to turn (e.g. turn 0 hv one win) , that means they won. if all win (winning team equal to amount/2) , new turn can be generated
        for loser in session['losers2023']:
            db.session.query(chart2023).filter(chart2023.SID == loser[0], chart2023.TID == loser[1]).update({'LOSE': True})
            db.session.commit()
        db.session.query(chartinfo).filter(chartinfo.ID == 2023).update({ 'TURN': chartinfo.TURN + 1 })
        db.session.commit()
        session['losers2023']=[]
        return redirect(url_for('chartlastyear'))
    db.session.commit()
    return render_template('chart.html' , teams = session['charts2023'], form = form , doreset = doreset, createteam = createteam , errors = doreset.errors , colors = colors)










@app.route('/reset' , methods=['GET','POST'])
def resetsession():     
    ## chart2024 must be reset either way
    db.session.query(chart2024).update({'LOSE': False})
    db.session.query(chart2024).update({'WON':0})
    db.session.commit()
    db.session.query(chartinfo).filter(chartinfo.ID == 2024).delete()
    db.session.commit()
    session.pop('charts', None)
    session.pop('losers', None)
        
    #if reset is clicked in 2023 , reset 2023
    if session['nowchart'] == 2023:
        db.session.query(chart2023).update({'LOSE': False})
        db.session.query(chart2023).update({'WON':0})
        db.session.commit()
        db.session.query(chartinfo).filter(chartinfo.ID == 2023).delete()
        db.session.commit()
        session.pop('charts2023', None)
        session.pop('losers2023', None)
        return redirect(url_for('chartlastyear'))
    else:
        return redirect(url_for('chart'))
    
    

    



@app.route('/rotate' , methods=['GET','POST'])
def rotategraph():     
    session['rotated'] = not session['rotated']
    if session['nowchart'] == 2024:
        return redirect(url_for('chart'))
    else:
        return redirect(url_for('chartlastyear'))


@app.route('/setcolor' , methods=['GET','POST'])
def colorset():     
    colors = setcolor()
    session['color'] = colors.color.data
    print(session['color'])
    if session['nowchart'] == 2024:
        return redirect(url_for('chart'))
    else:
        return redirect(url_for('chartlastyear'))

@app.route('/leaderboard2024')
def lb2024():
    if db.session.query(chart2024).first():
        lb = []
        #get all sid and tid , order by won count
        teams = db.session.query(chart2024.SID,chart2024.TID,chart2024.WON,chart2024.LOSE).order_by(chart2024.WON.desc()).all()
        #put info in lb var to pass into html template 
        for team in teams:
            newteam = {'name': db.session.query(schools.NAME).filter(schools.SID==team[0]).all()[0][0],
            'tid':team[1] ,'won':team[2],'losed':team[3]}
            lb.append(newteam)
        return render_template('leaderboard.html',lb=lb)
    else:
        session['flash'] = 'The leaderboard is empty!'
        return redirect(url_for('chartselect'))

@app.route('/leaderboard2023')
def lb2023():
    if db.session.query(chart2023).first():
        lb = []
        #get all sid and tid , order by won count
        teams = db.session.query(chart2023.SID,chart2023.TID,chart2023.WON,chart2023.LOSE).order_by(chart2023.WON.desc()).all()
        #put info in lb var to pass into html template 
        for team in teams:
            newteam = {'name': db.session.query(schools.NAME).filter(schools.SID==team[0]).all()[0][0],
            'tid':team[1] ,'won':team[2],'losed':team[3]}
            lb.append(newteam)
        return render_template('leaderboard.html',lb=lb)
    else:
        session['flash'] = 'The leaderboard is empty!'
        return redirect(url_for('chartselect'))
