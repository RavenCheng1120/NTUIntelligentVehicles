import math

# Read the input.dat file. Get the total number of the messages, tau, and lines contains the priority (Pi), the transmission time (Ci), and the period (Ti)
def importData(filename):
	n = open(filename).readlines()[:1]
	tau = open(filename).readlines()[1:2]
	n = int(''.join(n).strip())
	tau = float(''.join(tau).strip())
	dataList = [i.strip().split() for i in open(filename).readlines()[2:]] # read data to a 2D list
	dataList = [list(map(float, data)) for data in dataList] # turn type string to float

	return n, tau, dataList

def calculateResponse(index):
	Q, B = 0, 0
	
	# Find the B value (blocking time of the longest lower or same priority message).
	for blockIndex in (lower for lower in [firstColumn[0] for firstColumn in dataList] if lower >= dataList[index][0]):
		# print(f'{int(blockIndex)} ', end='')
		if B < dataList[int(blockIndex)][1]:
			B = dataList[int(blockIndex)][1]
	# print(f'{B } ', end='')
	# print()

	Q = B
	while True:
		sum = 0
		for blockIndex in (lower for lower in [firstColumn[0] for firstColumn in dataList] if lower < dataList[index][0]):
			sum += math.ceil((Q + tau) / dataList[int(blockIndex)][2]) * dataList[int(blockIndex)][1]

		if (B+sum)+dataList[index][1] > dataList[index][2]:
			print("Constraint violation")
			break
		elif Q == B+sum:
			R = format((B+sum)+dataList[index][1], '.2f')
			# worst-case R
			print(f'{ R }')
			break
		else:
			Q = B+sum


if __name__ == '__main__':
	n, tau, dataList = importData("input.dat")
	for i in range(int(n)):
		calculateResponse(i)