import xlrd
import matplotlib.pyplot as plt

book = xlrd.open_workbook("pt_data.csv")
sheet = book.sheets()[0]
nrows = sheet.nrows
pt1_x = sheet.col_values(0)
pt1_y = sheet.col_values(1)
del pt1_x[0]
del pt1_y[0]
plt.figure()
plt.scatter(pt1_x, pt1_y)
plt.show()