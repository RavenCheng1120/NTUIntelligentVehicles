import math
import random
import sys
import copy

# Read the input.dat file. Get the total number of the messages, tau, and lines contains the priority (Pi), the transmission time (Ci), and the period (Ti)
def ImportData(filename):
	n = open(filename).readlines()[:1]
	tau = open(filename).readlines()[1:2]
	n = int(''.join(n).strip())
	tau = float(''.join(tau).strip())
	dataList = [i.strip().split() for i in open(filename).readlines()[2:]] # read data to a 2D list
	dataList = [list(map(float, data)) for data in dataList] # turn type string to float

	return n, tau, dataList

# Find the message's index based on the priority
def PriorityFindMessageLocation(prior, localDataList, n):
	idx = 0
	for x in range(n):
		if localDataList[x][0] == prior:
			idx = x
	return idx


def CalculateResponse(index, n, tau, localDataList):
	Q, B, R = 0, 0, 0
	isViolate = False
	
	# Find the B value (blocking time of the longest lower or same priority message).
	for blockIndex in (lower for lower in [firstColumn[0] for firstColumn in localDataList] if lower >= localDataList[index][0]):
		location = PriorityFindMessageLocation(int(blockIndex), localDataList, n)
		if B < localDataList[location][1]:
			B = localDataList[location][1]

	Q = B
	while True:
		sum = 0
		for blockIndex in (lower for lower in [firstColumn[0] for firstColumn in localDataList] if lower < localDataList[index][0]):
			location = PriorityFindMessageLocation(int(blockIndex), localDataList, n)
			sum += math.ceil((Q + tau) / localDataList[location][2]) * localDataList[location][1]

		if (B+sum)+localDataList[index][1] > localDataList[index][2] and not isViolate:
			# print("Constraint violation")
			isViolate = True
		
		if Q == B+sum:
			# worst-case R
			R = round((B+sum)+localDataList[index][1],2)
			# print(f'{ R }')
			break
		else:
			Q = B+sum

	return float(R), isViolate


# Swap two messages' priority
def SwapPriority(n, localDataList):
	tempDataList = copy.deepcopy(localDataList)
	# Random select two priority to swap
	x, y = random.sample(priorityList, 2)
	tempDataList[x][0], tempDataList[y][0] = tempDataList[y][0], tempDataList[x][0] # Swap two messages' priority
	# print(f'Swap {x} and {y}')
	return tempDataList



if __name__ == '__main__':
	# Read in the data set
	n, tau, dataList = ImportData("input.dat")
	priorityList = [int(dataListPriority[0]) for dataListPriority in dataList]

	# Summation of the worst-case response times of all messages. The objective is to minimize it.
	summation, newSummation = 0, 0
	T = 10000000000
	reduceRate = 0.1
	isResponseViolate = False
	finalOutput = 0

	# Calculate the response time of each message
	for i in range(int(n)):
		idx = PriorityFindMessageLocation(i, dataList, n)
		temp_summation, isResponseViolate = CalculateResponse(idx, n, tau, dataList)
		summation += temp_summation
		if isResponseViolate:
			print("Constraint violation")
			sys.exit()
	finalOutput = summation
	# print(f'Origin sum = {summation}\n')


	### -------- Simulated Annealing --------
	while T > 0:
		newDataList = SwapPriority(n, dataList)
		tempR = 0
		newSummation = 0
		isResponseViolate = False

		# Calculate the response time of each message
		for i in range(int(n)):
			idx = PriorityFindMessageLocation(i, newDataList, n)
			tempR, temp_isViolate = CalculateResponse(idx, n, tau, newDataList)
			if temp_isViolate:
				isResponseViolate = True
			newSummation += tempR

		newSummation = round(newSummation, 2)

		### -------- "down-hill" move --------
		if newSummation <= summation:
			# Violated the constraint, make it harder to go down hill in this direction
			if isResponseViolate:
				# print("Constraint violation")
				T = T * reduceRate
				continue
				# prob = min(math.exp(-(summation-newSummation)*10000/T), 1)
				# if random.random() <= prob:
				# 	print()
				# 	continue

			dataList = copy.deepcopy(newDataList)
			summation = newSummation
			# print(f'downhill: {summation}')

			if isResponseViolate == False and finalOutput > summation:
				finalOutput = summation
			# print()
		### -------- "up-hill" move --------
		else:
			prob = min(math.exp(-(newSummation-summation)/T), 1)
			# print(f'\tSum = {summation} New Sum = {newSummation} / Prob = {prob}')
			
			# Take the chance to go up hill
			if random.random() <= prob:
				dataList = copy.deepcopy(newDataList)
				summation = newSummation
				# print(f'\tuphill: {summation}')
		# print()

		T = T * reduceRate

	for i in range(int(n)):
		print(int(dataList[i][0]))
	print(finalOutput)



