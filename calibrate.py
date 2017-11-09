import copy
import sys
import time

time_start=time.clock()
maxPos=[-1,-1]
alpha=-sys.maxint-1
beta=sys.maxint
utility=0


#strike out all positions reachable
def strikeOut(board,n,i,j,fruitType,player,fruitsClaimed):

	if i>=0 and i<n and j>=0 and j<n and board[i][j]==fruitType:
		
		board[i][j]='*'
		if player=="max":
			fruitsClaimed=fruitsClaimed+1
		else:
			fruitsClaimed=fruitsClaimed-1

		fruitsClaimed=strikeOut(board,n,i+1,j,fruitType,player,fruitsClaimed)
		fruitsClaimed=strikeOut(board,n,i-1,j,fruitType,player,fruitsClaimed)
		fruitsClaimed=strikeOut(board,n,i,j+1,fruitType,player,fruitsClaimed)
		fruitsClaimed=strikeOut(board,n,i,j-1,fruitType,player,fruitsClaimed)

	return fruitsClaimed


#drop fruits onto gaps
def dropFruits(board,n):
	for j in xrange(n):
		count=0
		i=n-1
		while i>=0:

			while i>=0 and board[i][j]=='*':
				count=count+1
				i=i-1

			if count>0 and i>=0:

				while i>=0 and board[i][j]!='*':
					board[i+count][j]=board[i][j]
					board[i][j]='*'
					i=i-1

				count=count+1

			i=i-1

#checks if board is empty
def terminal_test(board,n):
	for i in xrange(n):
		for j in xrange(n):
			if(board[i][j]!='*'):
				return 0
	return 1


#min value

def min_value(board,n,depth):
	global utility


	if depth==0 or terminal_test(board,n):
		return utility

	v=sys.maxint
	#implement for each action code
	for i in xrange(n): 
		for j in xrange(n):
			if board[i][j]!='*':
				prevBoard=copy.deepcopy(board)
				prevUtil=utility

				fruitsClaimed=strikeOut(board,n,i,j,board[i][j],"min",0)
				
				utility=utility-(fruitsClaimed*fruitsClaimed)

				dropFruits(board,n)

				v=min(v,max_value(board,n,depth-1))
									
				board=copy.deepcopy(prevBoard) #revert back original value
				
				utility=prevUtil
	return v

#max value
def max_value(board,n,depth):
	global utility
	global maxPos

	if depth==0 or terminal_test(board,n):
		return utility
	v=-sys.maxint-1

	
	#implement for each action code
	for i in xrange(n): 
		for j in xrange(n):
			if board[i][j]!='*':
				prevBoard=copy.deepcopy(board)
				prevUtil=utility

				fruitsClaimed= strikeOut(board,n,i,j,board[i][j],"max",0)

				utility=utility+(fruitsClaimed*fruitsClaimed)

				dropFruits(board,n)				
				v=max(v,min_value(board,n,depth-1))
				
				board=copy.deepcopy(prevBoard) #revert back original value
				utility=prevUtil
	return v


#alpha beta caller
def alphabeta(board,n):
	global utility
	global alpha
	global beta
	global maxPos


	curmax=-sys.maxint-1
	for i in xrange(n): 
		for j in xrange(n):
			if board[i][j]!='*':
				utility=0
				alpha=-sys.maxint-i
				beta=sys.maxint
				prevBoard=copy.deepcopy(board)
				fruitsClaimed=strikeOut(board,n,i,j,board[i][j],"max",0)	

				utility=utility+(fruitsClaimed*fruitsClaimed)

				dropFruits(board,n)

				v=min_value(board,n,4)
				if(v>curmax):
					curmax=v
					maxPos=[i,j]
				board=copy.deepcopy(prevBoard)

	return board
				

def main():
	global maxPox
	global time_start
	time_start=time.clock();

	n=2
	board=[[1,2],[3,4]]
	
	board=alphabeta(board,n)

	time_elapsed = (time.clock() - time_start)

	fout=open("calibration.txt","w")

	fout.write(str(time_elapsed/64))
	fout.close()



main()


