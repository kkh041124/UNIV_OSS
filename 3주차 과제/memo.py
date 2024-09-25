# def calc_weighted_average(data_2d, weight):
#     average = []
#     for ((m_score, f_score)) in (data_2d):
#         average.append(m_score*weight[0]+f_score*weight[1])

data=[]


mean = 0
with open("./data/class_score_en.csv",'r') as file:
    for line in file:
        if line and line[0].startswith("#"):
            continue
        line=line.strip()
        m_score,f_score = map(int,line.split(','))
        data.append((m_score,f_score))
sum=0
for m_score, _ in data:
    sum=(m_score)
    

mean= sum/len(data)
print(min(data))
