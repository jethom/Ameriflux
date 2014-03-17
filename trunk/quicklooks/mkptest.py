values = range(1,11)
valrange = range(10)
fig,ax = plt.subplots()
rbcm = plt.get_cmap('rainbow')
cNorm = colors.Normalize(vmin=1, vmax=values[-1])
scalarMap = cm.ScalarMappable(norm=cNorm, cmap = rbcm)
for i in values:
    timelist = []
    datalist = []
    colorVal = scalarMap.to_rgba(values[i-1])
    id_indx = np.nonzero(fastarray[3]==i)
    id_indx = id_indx[0]
    id_indx = id_indx.tolist()
    labtext = ('%2d'%i)
    for j in id_indx:
        timelist.append(fasttimelist[j]) 
        datalist.append(fastarray[1][j])
    plt.plot_date(timelist,datalist,color=colorVal,marker='.',label=labtext)
ax.legend(loc='best',fontsize='x-small')
    
