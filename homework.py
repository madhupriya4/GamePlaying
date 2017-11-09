import copy
import sys
import time

maxPos=[-1,-1]
alpha=-sys.maxint-1
beta=sys.maxint
utility=0
time_start=time.clock()


#input parameters
def inputBoard(fin):
	board=[]
	with open("input.txt") as fin:
		n=int(fin.readline())
		p=int(fin.readline())
		time_given=float(fin.readline())
		for line in fin.readlines():
			board.append([x for x in (line) if x!='\n'])
	return n,p,time_given,board


#output function
def printMove(board,n,maxPos):
	
	
	fout=open("output.txt","w")
	i=maxPos[0]
	j=maxPos[1]
	fout.write(chr(j+65))
	fout.write(str(i+1)+'\n')

	strikeOut(board,n,i,j,board[i][j],"max",0)
	dropFruits(board,n)
	for i in xrange(n):
		fout.write(''.join(board[i])+'\n')


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

def min_value(board,n,depth,t):
	global utility
	global alpha
	global beta

	if depth ==0 or terminal_test(board,n):
		return utility

	v=sys.maxint



	for i in xrange(n): 
		for j in xrange(n):

			time_elapsed = (time.clock() - time_start)
			if time_elapsed>t-0.1:
				return v

			if board[i][j]!='*':

				prevBoard=copy.deepcopy(board)
				prevUtil=utility

				fruitsClaimed=strikeOut(board,n,i,j,board[i][j],"min",0)
				
				utility=utility-(fruitsClaimed*fruitsClaimed)

				dropFruits(board,n)

				v=min(v,max_value(board,n,depth-1,t))
				if v<=alpha:
					return v
					
				board=copy.deepcopy(prevBoard) #revert back original value
				
				utility=prevUtil

				beta=min(beta,v)
	return v

#max value
def max_value(board,n,depth,t):
	global utility
	global alpha
	global beta
	global time_start


	if depth==0 or terminal_test(board,n):
		return utility

	v=-sys.maxint-1

		
	for i in xrange(n): 
		for j in xrange(n):

			time_elapsed = (time.clock() - time_start)
			if time_elapsed>t-0.1:
				return v

			if board[i][j]!='*':
				prevBoard=copy.deepcopy(board)
				prevUtil=utility

				fruitsClaimed= strikeOut(board,n,i,j,board[i][j],"max",0)

				utility=utility+(fruitsClaimed*fruitsClaimed)

				dropFruits(board,n)				
				v=max(v,min_value(board,n,depth-1,t))
				
				if v>=beta:
					return v

				board=copy.deepcopy(prevBoard) #revert back original value
				utility=prevUtil

				alpha=max(alpha,v)
	return v

#compute intial sorted list
def initVals(board,n,t):

	q=[]


	for i in xrange(n): 
		for j in xrange(n):
			if board[i][j]!='*':
				utility=0

				prevBoard=copy.deepcopy(board)
				
				fruitsClaimed=strikeOut(board,n,i,j,board[i][j],"max",0)	

				utility=utility+(fruitsClaimed*fruitsClaimed)

				dropFruits(board,n)

				q.append((utility*-1,[i,j]))


				board=copy.deepcopy(prevBoard)

	
	z=sorted(q,key=lambda tup:tup[0])
	result = list(dict(z).items())
	z=sorted(result,key=lambda tup:tup[0])

	return z


#alpha beta caller
def alphabeta(board,n,t):
	global utility
	global alpha
	global beta
	global maxPos
	global time_start


	prevBoard=copy.deepcopy(board)
	z=initVals(board,n,t)
	board=copy.deepcopy(prevBoard)

	utility=0

	time_elapsed = (time.clock() - time_start)
	t=t-time_elapsed

	if n>15:
		t=t-1

	cali=open("calibration.txt")
	numnodes=t/(float(cali.readline()))
	
	depth=compute_depth(numnodes,len(z)*n)

	curmax=-sys.maxint-1
	for ele in z:
		
		i=ele[1][0]
		j=ele[1][1]

		utility=0

		alpha=-sys.maxint-1
		beta=sys.maxint
		prevBoard=copy.deepcopy(board)

		fruitsClaimed=strikeOut(board,n,i,j,board[i][j],"max",0)	

		utility=utility+(fruitsClaimed*fruitsClaimed)

		dropFruits(board,n)

		v=min_value(board,n,depth,t)

		if(v>curmax):
			curmax=v
			maxPos=[i,j]

		board=copy.deepcopy(prevBoard)

	return board



def compute_depth(numnodes,n):
	sum=0
	i=n
	j=0
	for w in xrange(n,0,-1):
		sum=sum+i
		if sum>numnodes:
			break
		j=j+1
		i=i*(w-1)
	return j



#main code
def main():
	global maxPox

	n,p,t,board=inputBoard("input.txt")

	if t>200:
		t=200

	t=t-0.2

	
	board=alphabeta(board,n,t)

	printMove(board,n,maxPos)

main()
