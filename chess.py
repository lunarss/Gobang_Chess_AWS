from flask import render_template, redirect, url_for, request
from app import webapp
from random import shuffle


current_map=[[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]] ############# Current status 1 represents user（user always black chess） 2 represents AI（ai always white chess）

@webapp.route('/chess',methods=['GET'])
#Start the game
def chess_game():
  current_map=[[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
  [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
  [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
  [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
  [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
  [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
  [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
  [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
  [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
  [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
  [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
  [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
  [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
  [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
  [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]
  current_map_str = ""
  # history_map = ""
  for i in range(15*15):
    current_map_str = current_map_str + "0,"
  print("Game Start")
  return render_template("chess/form.html", current_map_str = current_map_str)
    
    
@webapp.route('/chess/replay',methods=['GET'])
#Replay the game
def replay_game():
  return redirect(url_for("chess_game"))
  
  
  
@webapp.route('/chess/user',methods=['GET'])
def user_step():
  column = request.args.get('column')
  row = request.args.get('row')
  # # chessBox = request.args.get('chessBox')
  print("row="+row+" column="+column)
  print("User Input Confirm")
  
  current_map_str = request.args.get('current_map_str')
  # print(current_map_str)
  
  # current_map = []
  for i in range(15):
    # current_map.append([])
    for j in range(15):
      current_map[i][j] = int(current_map_str.split(",")[15*i+j])
        
  # print(current_map)
  user_step_row = int(row)
  user_step_column = int(column)

  print('current map:')
  for i in range(0,15):
      for j in range(0,15):
          print(str(current_map[i][j])+' ',end='')
      print('')
  if(check_max_number([user_step_row,user_step_column],1)[0]==5):
    print('You win!')
    return redirect(url_for("chess_game"))
  # if(current_map_arr[user_step_row][user_step_column]!=0):
  #   print('r u fking kidding me')

  # current_map[user_step_row][user_step_column]=1
  
  print('AI step:')
  ai_step = generate_ai_step(current_map)
  print(ai_step)

  current_map[ai_step[0]][ai_step[1]]=2
  # print(current_map)

  print('updated map:')
  for i in range(0,15):
      for j in range(0,15):
          print(str(current_map[i][j])+' ',end='')
      print('')
  if(check_max_number([ai_step[0],ai_step[1]],2)[0]==5):
    print('You lose!')
    return redirect(url_for("chess_game"))

    
  list_map = list(current_map_str)
  # list_map[int(x)*30+int(y)*2] = "1"
  list_map[ai_step[0]*30+ai_step[1]*2] = "2"
  current_map_str = "".join(list_map)
  # print(current_map_str)
    	
  return render_template("chess/form.html", current_map_str = current_map_str)
    
    









def boundary_check(check_step): # check if this chess is in the board, return 1 for true, 0 for false
	if(check_step[0]>=0 and check_step[0]<=14 and check_step[1]>=0 and check_step[1]<=14):
		return 1
	else:
		return 0

def check_max_number(current_step, current_player): # return the maximum number of connected chesses from this chess
	step_up_flag=0
	step_down_flag=0
	step_left_flag=0
	step_right_flag=0
	step_up_left_flag=0
	step_down_right_flag=0
	step_up_right_flag=0
	step_down_left_flag=0

	for i in range(1,5):
		if(boundary_check([current_step[0]-i,current_step[1]])==1 and current_map[current_step[0]-i][current_step[1]]==current_player):
			step_up_flag=step_up_flag+1
		else:
			break
	for i in range(1,5):
		if(boundary_check([current_step[0]+i,current_step[1]])==1 and current_map[current_step[0]+i][current_step[1]]==current_player):
			step_down_flag=step_down_flag+1
		else:
			break
	for i in range(1,5):
		if(boundary_check([current_step[0],current_step[1]-i])==1 and current_map[current_step[0]][current_step[1]-i]==current_player):
			step_left_flag=step_left_flag+1
		else:
			break
	for i in range(1,5):
		if(boundary_check([current_step[0],current_step[1]+i])==1 and current_map[current_step[0]][current_step[1]+i]==current_player):
			step_right_flag=step_right_flag+1
		else:
			break
	for i in range(1,5):
		if(boundary_check([current_step[0]-i,current_step[1]-i])==1 and current_map[current_step[0]-i][current_step[1]-i]==current_player):
			step_up_left_flag=step_up_left_flag+1
		else:
			break
	for i in range(1,5):
		if(boundary_check([current_step[0]+i,current_step[1]+i])==1 and current_map[current_step[0]+i][current_step[1]+i]==current_player):
			step_down_right_flag=step_down_right_flag+1
		else:
			break
	for i in range(1,5):
		if(boundary_check([current_step[0]-i,current_step[1]+i])==1 and current_map[current_step[0]-i][current_step[1]+i]==current_player):
			step_up_right_flag=step_up_right_flag+1
		else:
			break
	for i in range(1,5):
		if(boundary_check([current_step[0]+i,current_step[1]-i])==1 and current_map[current_step[0]+i][current_step[1]-i]==current_player):
			step_down_left_flag=step_down_left_flag+1
		else:
			break
	result_list=[step_up_flag+step_down_flag+1,step_left_flag+step_right_flag+1,step_up_left_flag+step_down_right_flag+1,step_up_right_flag+step_down_left_flag+1]
	return max(result_list),result_list.index(max(result_list))

def check_alive(current_check,direction_to_defend,current_player): # check if one direction works for the next round
  alive_direction=[0,0]
  if(direction_to_defend==0):
    for i in range(1,5):
      if(boundary_check([current_check[0]-i,current_check[1]])==0):
        alive_direction[0]=0
        break
      if(current_map[current_check[0]-i][current_check[1]]==0):
        alive_direction[0]=1
        break
      if(current_map[current_check[0]-i][current_check[1]]==3-current_player):
        alive_direction[0]=0
        break
      if(current_map[current_check[0]-i][current_check[1]]==current_player):
        continue
    for i in range(1,5):
      if(boundary_check([current_check[0]+i,current_check[1]])==0):
        alive_direction[1]=0
        break
      if(current_map[current_check[0]+i][current_check[1]]==0):
        alive_direction[1]=1
        break
      if(current_map[current_check[0]+i][current_check[1]]==3-current_player):
        alive_direction[1]=0
        break
      if(current_map[current_check[0]+i][current_check[1]]==current_player):
        continue
  if(direction_to_defend==1):
    for i in range(1,5):
      if(boundary_check([current_check[0],current_check[1]-i])==0):
        alive_direction[0]=0
        break
      if(current_map[current_check[0]][current_check[1]-i]==0):
        alive_direction[0]=1
        break
      if(current_map[current_check[0]][current_check[1]-i]==3-current_player):
        alive_direction[0]=0
        break
      if(current_map[current_check[0]][current_check[1]-i]==current_player):
        continue
    for i in range(1,5):
      if(boundary_check([current_check[0],current_check[1]+i])==0):
        alive_direction[1]=0
        break
      if(current_map[current_check[0]][current_check[1]+i]==0):
        alive_direction[1]=1
        break
      if(current_map[current_check[0]][current_check[1]+i]==3-current_player):
        alive_direction[1]=0
        break
      if(current_map[current_check[0]][current_check[1]+i]==current_player):
        continue
  if(direction_to_defend==2):
    for i in range(1,5):
      if(boundary_check([current_check[0]-i,current_check[1]-i])==0):
        alive_direction[0]=0
        break
      if(current_map[current_check[0]-i][current_check[1]-i]==0):
        alive_direction[0]=1
        break
      if(current_map[current_check[0]-i][current_check[1]-i]==3-current_player):
        alive_direction[0]=0
        break
      if(current_map[current_check[0]-i][current_check[1]-i]==current_player):
        continue
    for i in range(1,5):
      if(boundary_check([current_check[0]+i,current_check[1]+i])==0):
        alive_direction[1]=0
        break
      if(current_map[current_check[0]+i][current_check[1]+i]==0):
        alive_direction[1]=1
        break
      if(current_map[current_check[0]+i][current_check[1]+i]==3-current_player):
        alive_direction[1]=0
        break
      if(current_map[current_check[0]+i][current_check[1]+i]==current_player):
        continue
  if(direction_to_defend==3):
    for i in range(1,5):
      if(boundary_check([current_check[0]-i,current_check[1]+i])==0):
        alive_direction[0]=0
        break
      if(current_map[current_check[0]-i][current_check[1]+i]==0):
        alive_direction[0]=1
        break
      if(current_map[current_check[0]-i][current_check[1]+i]==3-current_player):
        alive_direction[0]=0
        break
      if(current_map[current_check[0]-i][current_check[1]+i]==current_player):
        continue
    for i in range(1,5):
      if(boundary_check([current_check[0]+i,current_check[1]-i])==0):
        alive_direction[1]=0
        break
      if(current_map[current_check[0]+i][current_check[1]-i]==0):
        alive_direction[1]=1
        break
      if(current_map[current_check[0]+i][current_check[1]-i]==3-current_player):
        alive_direction[1]=0
        break
      if(current_map[current_check[0]+i][current_check[1]-i]==current_player):
        continue
  return alive_direction[0]+alive_direction[1]



def best_choice_to_win(current_player): # mostly winning chess
  random_list = [i for i in range(15)]
  shuffle(random_list)
  for row in random_list:
    for column in random_list:

      if(current_map[row][column]==current_player):
        if(check_max_number([row,column],current_player)[0]==4):
          if(check_alive([row,column],check_max_number([row,column],current_player)[1],current_player))>=1:
            return 4,[row,column],check_max_number([row,column],current_player)[1]

  for row in random_list:
    for column in random_list:

      if(current_map[row][column]==current_player):
        if(check_max_number([row,column],current_player)[0]==3):
          if(check_alive([row,column],check_max_number([row,column],current_player)[1],current_player))>=1:
            return 3,[row,column],check_max_number([row,column],current_player)[1]

  for row in random_list:
    for column in random_list:

      if(current_map[row][column]==current_player):
        if(check_max_number([row,column],current_player)[0]==2):
          if(check_alive([row,column],check_max_number([row,column],current_player)[1],current_player))>=1:
            return 2,[row,column],check_max_number([row,column],current_player)[1]

  for row in random_list:
    for column in random_list:

      if(current_map[row][column]==current_player):
        if(check_max_number([row,column],current_player)[0]==1):
          if(check_alive([row,column],check_max_number([row,column],current_player)[1],current_player))>=1:
            return 1,[row,column],check_max_number([row,column],current_player)[1]

def generate_ai_step(current_map): # calculate ai's decision of the next chess coordinate
  #print(best_choice_to_win(1))
  if(best_choice_to_win(1)!=None):
    step_to_defend=best_choice_to_win(1)[1]
    direction_to_defend=best_choice_to_win(1)[2]

#############################444444444444
    if(best_choice_to_win(1)[0]==4):
      #print('defend4')
      #print('user best chance to win')
      #print(best_choice_to_win(1))
      if(direction_to_defend==0):
        for i in range(1,5):
          if(boundary_check([step_to_defend[0]-i,step_to_defend[1]])==1):
            if(current_map[step_to_defend[0]-i][step_to_defend[1]]==0):
              return [step_to_defend[0]-i,step_to_defend[1]]
            if(current_map[step_to_defend[0]-i][step_to_defend[1]]==2):
              break
            if(current_map[step_to_defend[0]-i][step_to_defend[1]]==1):
              continue
        for i in range(1,5):
          if(boundary_check([step_to_defend[0]+i,step_to_defend[1]])==1):
            if(current_map[step_to_defend[0]+i][step_to_defend[1]]==0):
              return [step_to_defend[0]+i,step_to_defend[1]]
            if(current_map[step_to_defend[0]+i][step_to_defend[1]]==2):
              break
            if(current_map[step_to_defend[0]+i][step_to_defend[1]]==1):
              continue

      if(direction_to_defend==1):
        for i in range(1,5):
          if(boundary_check([step_to_defend[0],step_to_defend[1]-i])==1):
            if(current_map[step_to_defend[0]][step_to_defend[1]-i]==0):
              return [step_to_defend[0],step_to_defend[1]-i]
            if(current_map[step_to_defend[0]][step_to_defend[1]-i]==2):
              break
            if(current_map[step_to_defend[0]][step_to_defend[1]-i]==1):
              continue
        for i in range(1,5):
          if(boundary_check([step_to_defend[0],step_to_defend[1]+i])==1):
            if(current_map[step_to_defend[0]][step_to_defend[1]+i]==0):
              return [step_to_defend[0],step_to_defend[1]+i]
            if(current_map[step_to_defend[0]][step_to_defend[1]+i]==2):
              break
            if(current_map[step_to_defend[0]][step_to_defend[1]+i]==1):
              continue
      if(direction_to_defend==2):
        for i in range(1,5):
          if(boundary_check([step_to_defend[0]-i,step_to_defend[1]-i])==1):
            if(current_map[step_to_defend[0]-i][step_to_defend[1]-i]==0):
              return [step_to_defend[0]-i,step_to_defend[1]-i]
            if(current_map[step_to_defend[0]-i][step_to_defend[1]-i]==2):
              break
            if(current_map[step_to_defend[0]-i][step_to_defend[1]-i]==1):
              continue
        for i in range(1,5):
          if(boundary_check([step_to_defend[0]+i,step_to_defend[1]+i])==1):
            if(current_map[step_to_defend[0]+i][step_to_defend[1]+i]==0):
              return [step_to_defend[0]+i,step_to_defend[1]+i]
            if(current_map[step_to_defend[0]+i][step_to_defend[1]+i]==2):
              break
            if(current_map[step_to_defend[0]+i][step_to_defend[1]+i]==1):
              continue
      if(direction_to_defend==3):
        for i in range(1,5):
          if(boundary_check([step_to_defend[0]-i,step_to_defend[1]+i])==1):
            if(current_map[step_to_defend[0]-i][step_to_defend[1]+i]==0):
              return [step_to_defend[0]-i,step_to_defend[1]+i]
            if(current_map[step_to_defend[0]-i][step_to_defend[1]+i]==2):
              break
            if(current_map[step_to_defend[0]-i][step_to_defend[1]+i]==1):
              continue
        for i in range(1,5):
          if(boundary_check([step_to_defend[0]+i,step_to_defend[1]-i])==1):
            if(current_map[step_to_defend[0]+i][step_to_defend[1]-i]==0):
              return [step_to_defend[0]+i,step_to_defend[1]-i]
            if(current_map[step_to_defend[0]+i][step_to_defend[1]-i]==2):
              break
            if(current_map[step_to_defend[0]+i][step_to_defend[1]-i]==1):
              continue
###################################33333333333333333333333
    if(best_choice_to_win(1)[0]==3):
      #print('defend3')
      #print('user best chance to win')
      #print(best_choice_to_win(1))
      if(direction_to_defend==0):
        for i in range(1,4):

          if(boundary_check([step_to_defend[0]-i,step_to_defend[1]])==1):
            if(current_map[step_to_defend[0]-i][step_to_defend[1]]==0):
              return [step_to_defend[0]-i,step_to_defend[1]]
            if(current_map[step_to_defend[0]-i][step_to_defend[1]]==2):
              break
            if(current_map[step_to_defend[0]-i][step_to_defend[1]]==1):
              continue
        for i in range(1,4):
          if(boundary_check([step_to_defend[0]+i,step_to_defend[1]])==1):
            if(current_map[step_to_defend[0]+i][step_to_defend[1]]==0):
              return [step_to_defend[0]+i,step_to_defend[1]]
            if(current_map[step_to_defend[0]+i][step_to_defend[1]]==2):
              break
            if(current_map[step_to_defend[0]+i][step_to_defend[1]]==1):
              continue

      if(direction_to_defend==1):
        for i in range(1,4):
          if(boundary_check([step_to_defend[0],step_to_defend[1]-i])==1):
            if(current_map[step_to_defend[0]][step_to_defend[1]-i]==0):
              return [step_to_defend[0],step_to_defend[1]-i]
            if(current_map[step_to_defend[0]][step_to_defend[1]-i]==2):
              break
            if(current_map[step_to_defend[0]][step_to_defend[1]-i]==1):
              continue
        for i in range(1,4):
          if(boundary_check([step_to_defend[0],step_to_defend[1]+i])==1):
            if(current_map[step_to_defend[0]][step_to_defend[1]+i]==0):
              return [step_to_defend[0],step_to_defend[1]+i]
            if(current_map[step_to_defend[0]][step_to_defend[1]+i]==2):
              break
            if(current_map[step_to_defend[0]][step_to_defend[1]+i]==1):
              continue
      if(direction_to_defend==2):
        for i in range(1,4):
          if(boundary_check([step_to_defend[0]-i,step_to_defend[1]-i])==1):
            if(current_map[step_to_defend[0]-i][step_to_defend[1]-i]==0):
              return [step_to_defend[0]-i,step_to_defend[1]-i]
            if(current_map[step_to_defend[0]-i][step_to_defend[1]-i]==2):
              break
            if(current_map[step_to_defend[0]-i][step_to_defend[1]-i]==1):
              continue
        for i in range(1,4):
          if(boundary_check([step_to_defend[0]+i,step_to_defend[1]+i])==1):
            if(current_map[step_to_defend[0]+i][step_to_defend[1]+i]==0):
              return [step_to_defend[0]+i,step_to_defend[1]+i]
            if(current_map[step_to_defend[0]+i][step_to_defend[1]+i]==2):
              break
            if(current_map[step_to_defend[0]+i][step_to_defend[1]+i]==1):
              continue
      if(direction_to_defend==3):
        for i in range(1,4):
          if(boundary_check([step_to_defend[0]-i,step_to_defend[1]+i])==1):
            if(current_map[step_to_defend[0]-i][step_to_defend[1]+i]==0):
              return [step_to_defend[0]-i,step_to_defend[1]+i]
            if(current_map[step_to_defend[0]-i][step_to_defend[1]+i]==2):
              break
            if(current_map[step_to_defend[0]-i][step_to_defend[1]+i]==1):
              continue
        for i in range(1,4):
          if(boundary_check([step_to_defend[0]+i,step_to_defend[1]-i])==1):
            if(current_map[step_to_defend[0]+i][step_to_defend[1]-i]==0):
              return [step_to_defend[0]+i,step_to_defend[1]-i]
            if(current_map[step_to_defend[0]+i][step_to_defend[1]-i]==2):
              break
            if(current_map[step_to_defend[0]+i][step_to_defend[1]-i]==1):
              continue

#22222222222222222222222222 attack!!!!!!!!!!!
  #print('attack')
  if(best_choice_to_win(2)==None):
    print('ai start to play')
    if(current_map[7][7]==0):
      return [7,7]
    else:
      return [7,8]
        
  step_to_defend=best_choice_to_win(2)[1]
  direction_to_defend=best_choice_to_win(2)[2]
  #print('user best chance to win')
  #print(best_choice_to_win(1))
  #print('ai best chance to win')
  #print(best_choice_to_win(2))
  if(direction_to_defend==0):
    for i in range(1,4):
      if(boundary_check([step_to_defend[0]-i,step_to_defend[1]])==1):
        if(current_map[step_to_defend[0]-i][step_to_defend[1]]==0):
          return [step_to_defend[0]-i,step_to_defend[1]]
        if(current_map[step_to_defend[0]-i][step_to_defend[1]]==1):
          break
        if(current_map[step_to_defend[0]-i][step_to_defend[1]]==2):
          continue
    for i in range(1,4):
      if(boundary_check([step_to_defend[0]+i,step_to_defend[1]])==1):
        if(current_map[step_to_defend[0]+i][step_to_defend[1]]==0):
          return [step_to_defend[0]+i,step_to_defend[1]]
        if(current_map[step_to_defend[0]+i][step_to_defend[1]]==1):
          break
        if(current_map[step_to_defend[0]+i][step_to_defend[1]]==2):
          continue
  if(direction_to_defend==1):
    for i in range(1,4):
      if(boundary_check([step_to_defend[0],step_to_defend[1]-i])==1):
        if(current_map[step_to_defend[0]][step_to_defend[1]-i]==0):
          return [step_to_defend[0],step_to_defend[1]-i]
        if(current_map[step_to_defend[0]][step_to_defend[1]-i]==1):
          break
        if(current_map[step_to_defend[0]][step_to_defend[1]-i]==2):
          continue
    for i in range(1,4):
      if(boundary_check([step_to_defend[0],step_to_defend[1]+i])==1):
        if(current_map[step_to_defend[0]][step_to_defend[1]+i]==0):
          return [step_to_defend[0],step_to_defend[1]+i]
        if(current_map[step_to_defend[0]][step_to_defend[1]+i]==1):
          break
        if(current_map[step_to_defend[0]][step_to_defend[1]+i]==2):
          continue
  if(direction_to_defend==2):
    for i in range(1,4):
      if(boundary_check([step_to_defend[0]-i,step_to_defend[1]-i])==1):
        if(current_map[step_to_defend[0]-i][step_to_defend[1]-i]==0):
          return [step_to_defend[0]-i,step_to_defend[1]-i]
        if(current_map[step_to_defend[0]-i][step_to_defend[1]-i]==1):
          break
        if(current_map[step_to_defend[0]-i][step_to_defend[1]-i]==2):
          continue
    for i in range(1,4):
      if(boundary_check([step_to_defend[0]+i,step_to_defend[1]+i])==1):
        if(current_map[step_to_defend[0]+i][step_to_defend[1]+i]==0):
          return [step_to_defend[0]+i,step_to_defend[1]+i]
        if(current_map[step_to_defend[0]+i][step_to_defend[1]+i]==1):
          break
        if(current_map[step_to_defend[0]+i][step_to_defend[1]+i]==2):
          continue
  if(direction_to_defend==3):
    for i in range(1,4):
      if(boundary_check([step_to_defend[0]-i,step_to_defend[1]+i])==1):
        if(current_map[step_to_defend[0]-i][step_to_defend[1]+i]==0):
          return [step_to_defend[0]-i,step_to_defend[1]+i]
        if(current_map[step_to_defend[0]-i][step_to_defend[1]+i]==1):
          break
        if(current_map[step_to_defend[0]-i][step_to_defend[1]+i]==2):
          continue
    for i in range(1,4):
      if(boundary_check([step_to_defend[0]+i,step_to_defend[1]-i])==1):
        if(current_map[step_to_defend[0]+i][step_to_defend[1]-i]==0):
          return [step_to_defend[0]+i,step_to_defend[1]-i]
        if(current_map[step_to_defend[0]+i][step_to_defend[1]-i]==1):
          break
        if(current_map[step_to_defend[0]+i][step_to_defend[1]-i]==2):
          continue
