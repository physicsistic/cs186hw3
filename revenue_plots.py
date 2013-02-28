import sys
import matplotlib.pyplot as plt

GSP = [4713.48, 4713.48, 4751.34, 4513.05, 4602.66, 4882.91, 4914.21, 5019.69, 5147.24, 5031.36, 4892.17, 4722.28, 4654.94, 3816.67, 3672.81, 2952.2, 1798.4, 665.75, 0.]
VCG = [4530.65,
4530.65,
4530.65,
4521.44,
4434.72,
4713.08,
4856.08,
5049.74,
5161.99,
5113.63,
4894.78,
4837.23,
4270.31,
4043.36,
3635.67,
2639.76,
2073.83,
668.18,
0.]

r = [0.1 * i for i in range(0, 19)]

revenue_plot = plt.figure()
plt.plot(r, GSP, "-r", label ="GSP Truthful Bidding")
plt.plot(r, VCG, "-b", label ="VCG Balanced Bidding")
plt.xlabel("Reserve prices ($)")
plt.ylabel("Revenue ($)")
plt.title("Plot of Revenue vs Reserve Prices")
plt.legend(loc=3)
plt.show()