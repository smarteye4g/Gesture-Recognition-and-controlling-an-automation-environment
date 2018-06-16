import xlsxwriter
import numpy as np
import xlrd
import sample_plot as convert
import math
from scipy.fftpack import fft, ifft
from scipy import stats

file_location = '/home/ubuntu/Documents/Gesture_Recognition/ACC.csv'
excelfile = convert.convert_csv_to_xlsx(file_location)
workbook = xlrd.open_workbook(excelfile)
sheet = workbook.sheet_by_index(0)
L = sheet.nrows 		#Length of the temporal sequence
N = 9				#Number of segments of identical length
LS = int(math.floor(L/(N+1)))        #Length of each segment
s = 0                           #Segment no
k1 = 0				#Frame No
k2 = 0
kmax = N			#No of Frames
n1 = 0
n2 = 0
axis = 3            #Number of axis
number_of_features = 5

def sum(a, axes, i, initial, final):
    sum = 0
    for j in range(initial,final + 1):
        sum = sum + a[axes,i ,j]
    return sum

time = []
for value in sheet.col_values(0):
        time.append(value)
Time=np.array(time)

ax = []
for value in sheet.col_values(1):
        ax.append(value)
Ax = np.array(ax)

ay = []
for value in sheet.col_values(2):
        ay.append(value)
Ay = np.array(ay)

az = []
for value in sheet.col_values(3):
        az.append(value)
Az = np.array(az)

rxk1 = np.empty([kmax,2*LS],dtype = float)
ryk1 = np.empty([kmax,2*LS],dtype = float)
rzk1 = np.empty([kmax,2*LS],dtype = float)
rxk2 = np.empty([kmax,2*LS],dtype = float)
ryk2 = np.empty([kmax,2*LS],dtype = float)
rzk2 = np.empty([kmax,2*LS],dtype = float)

#Dividing the input signal sequence into segments and frames
for i in range(0,L):
    if ((i!=0) and (i<L) and ((i%LS) is 0)):         #On encountering the index as a multiple of LS (Segment length), then increment the segment counter
        s = s + 1
        if (s%2) is 0:
            k2 = k2 + 1
        elif (s%2) != 0:
            k1 = k1 + 1
    if n2 == 2*LS:
        n2 = 0
    if n1 == 2*LS:
        n1 = 0

    if (s%2) is 0:
        rxk2[k2,n2] = Ax[i]
        ryk2[k2,n2] = Ay[i]
        rzk2[k2,n2] = Az[i]
        if n2<LS:
            n2 = n2 + 1
        if n1 >= LS and n1<= 2*LS:
            rxk1[k1,n1] = Ax[i]
            ryk1[k1,n1] = Ay[i]
            rzk1[k1,n1] = Az[i]           
            n1 = n1 + 1  
    elif (s%2) != 0:
        rxk1[k1,n1] = Ax[i]
        ryk1[k1,n1] = Ay[i]
        rzk1[k1,n1] = Az[i]
        if n1<LS:           
            n1 = n1 + 1
        if n2 >= LS and n2<= 2*LS:
            rxk2[k2,n2] = Ax[i]
            ryk2[k2,n2] = Ay[i]
            rzk2[k2,n2] = Az[i]           
            n2 = n2 + 1

frame = np.empty([axis, kmax, 2*LS],dtype = float)
fo = np.empty([axis, kmax, 2*LS],dtype = float)
fos = np.empty([axis, kmax, 2*LS],dtype = float)

for i in range(0,5):
    k = 2*i
    frame[0, k, :] = rxk2[i, :]
    frame[1, k, :] = ryk2[i, :]
    frame[2, k, :] = rzk2[i, :]

for j in range(1,5):
    l = 2*j-1
    frame[0, l, :] = rxk1[j, :]
    frame[1, l, :] = ryk1[j, :]
    frame[2, l, :] = rzk1[j, :]

#Feature Extraction of each frame in frequency domain
#Finding the fft of the frames (Equation 7)
fo = np.absolute(fft(frame,(2*LS)))

#isolating the real and imaginary parts - for checking the correctness of the fft function
foc = fft(frame,(2*LS))
foreal = np.real(foc)
foimg = np.imag(foc)

#Feature 1: mean of each frame (Equation 8)
u = np.empty([axis, kmax],dtype = float)
for a in range(0,3):
    for i in range(0,kmax):
        u[a, i] = fo[a, i, 0]   #The frame vector needs to be updated

#Feature 2: Energy of each frame (Equation 9)
energy = np.empty([axis, kmax],dtype = float)
energy_num = np.empty([axis, kmax],dtype = float)                #numerator of the energy
energy_den = abs(2*LS-1)                                   #denominator of the energy
np.square(fo,fos)
for a in range(0,3):
    for i in range(0,kmax):
        energy_num[a, i] = sum(fos, a, i, 1,(2*LS-1))
        energy[a, i] = energy_num[a, i]/energy_den

#Probability of each frame (Equation 11)
probability_num = np.empty([axis, kmax,2*LS], dtype = float)
probability_den = np.empty([axis, kmax], dtype = float)
probability = np.empty([axis, kmax,2*LS], dtype = float)
probability_num = fo
for a in range(0,3):
    for i in range(0,kmax):
        probability_den[a, i] = sum(fo, a, i, 1, (2 * LS - 1))
        for j in range(0,(2*LS)):
            probability[a, i, j] = probability_num[a, i, j]/probability_den[a, i]

#Information of each frame (Equation 10)
logarithm = np.empty([axis, kmax, 2*LS], dtype = float)
information = np.empty([axis, kmax, 2*LS], dtype = float)
for a in range(0,3):
    for i in range(0,kmax):
        for j in range(1, (2 * LS)):
            logarithm[a, i, j] = math.log((1/probability[a, i, j]),10)
            information[a, i, j] = probability[a, i,j] * logarithm[a, i, j]

#Feature 3: Entropy of each frame (Equation 10)
entropy = np.empty([axis, kmax],dtype = float)
for a in range(0,3):
    for i in range(0,kmax):
        entropy[a, i] = sum(information, a, i, 1, (2 * LS - 1))

#Feature Extraction in Time domain
#Part 1: Mean of each element (Equation 13)
mean = np.empty([axis, kmax, 2*LS],dtype = float)
mean_num = np.empty([axis, kmax, 2*LS],dtype = float)
mean_den = np.empty([axis, kmax],dtype = float)
for a in range(0,3):
    for i in range(0, kmax):
        mean_den[a, i] = sum(frame, a, i, 0, (2 * LS - 1))
mean_num = frame
for a in range(0,3):
    for i in range(0,kmax):
        for j in range(0,2*LS):
            mean[a, i, j] = mean_num[a, i, j]/mean_den[a, i]

#Part 2: Standard Deviation
#Deviation and Variance from mean
deviation = np.empty([axis, kmax,2*LS],dtype = float)
deviation_square = np.empty([axis, kmax,2*LS],dtype = float)
variance = np.empty([axis, kmax],dtype = float)
standard_deviation = np.empty([axis, kmax],dtype = float)
for a in range(0,3):
    for i in range(0,kmax):
        for j in range(0,2*LS):
            deviation[a, i, j] = frame[a, i, j] - mean[a, i, j]
np.square(deviation, deviation_square)
for a in range(0,3):
    for i in range(0,kmax):
        variance[a, i] = sum(deviation_square, a, i, 0, (2 * LS - 1))

#Feature 3: Standard Deviation (Equation 12)
np.sqrt(variance,standard_deviation)

#Corelation
corelation = np.empty([axis, kmax],dtype = float)
aa = np.empty(4, dtype = float)
for i in range(0, kmax):
    aa = stats.pearsonr(frame[0, i], frame[1, i])   #X - Y Corelation
    corelation[0, i] = aa[0]
    print('i = ' + str(i) + ' corelation in X-Y = ' + str(corelation[0,i]))
    aa = stats.pearsonr(frame[0, i], frame[2, i])  #X - Z Corelation
    corelation[1, i] = aa[0]
    aa = stats.pearsonr(frame[1, i], frame[2, i])  #Y - Z Corelation
    corelation[2, i] = aa[0]

feature = np.empty([axis, kmax, number_of_features],dtype= float)
for a in range(0,3):
    for i in range(0,kmax):
            feature[a,i,0] = u[a,i]
            feature[a,i,1] = energy[a,i]
            feature[a,i,2] = entropy[a,i]
            feature[a,i,3] = standard_deviation[a,i]
            feature[a,i,4] = corelation[a,i]

workbook = xlsxwriter.Workbook('arrays.xlsx')
worksheet1 = workbook.add_worksheet()
worksheet2 = workbook.add_worksheet()
worksheet3 = workbook.add_worksheet()
'''
worksheet4 = workbook.add_worksheet()
worksheet5 = workbook.add_worksheet()
worksheet6 = workbook.add_worksheet()
worksheet7 = workbook.add_worksheet()
worksheet8 = workbook.add_worksheet()
worksheet9 = workbook.add_worksheet()
'''

row = 0

for col, data in enumerate(frame[0]):
    worksheet1.write_column(row, col, data)

row = 0

for col, data in enumerate(frame[1]):
    worksheet2.write_column(row, col, data)

row = 0

for col, data in enumerate(frame[2]):
    worksheet3.write_column(row, col, data)


'''
row = 0

for col, data in enumerate(frame[1]):
    worksheet2.write_column(row, col, data)

row = 0

for col, data in enumerate(frame[2]):
    worksheet3.write_column(row, col, data)
'''

workbook.close()

#print('i = ' + str(i) + ' k1='+str(k1) + ' n1 =' + str(n1) + ' k2='+str(k2) + ' n2 =' + str(n2) + ' s=' +str(s) +' i%LS=' + str(i%LS) + ' L = ' + str(L) +' s%2=' + str(s%2))
#print('Final data:''k1 =' + str(k1) + ' n1 = ' + str(n1) +' k2 =' + str(k2) + ' n2 = ' + str(n2) +' rxk1[k1,n1] = ' + str(rxk1[k1,n1-1]) + ' rxk2[k2,n2] = ' + str(rxk2[k2,n2-1]) + ' Ax[i] = ' + str(Ax[i]) + ' i = ' + str(i)+ ' s=' +str(s))
