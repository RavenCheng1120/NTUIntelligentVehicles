import hw1

if __name__ == '__main__':
	n, tau, dataList = hw1.importData("input.dat")
	for i in range(int(n)):
		hw1.calculateResponse(i, n, tau, dataList)