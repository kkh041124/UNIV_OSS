import numpy as np
import matplotlib.pyplot as plt
from sklearn import metrics
from sklearn.ensemble import RandomForestClassifier  # Better classifier
from matplotlib.lines import Line2D  # For the custom legend

# 데이터 로드 함수 정의
def load_wdbc_data(filename):
    class WDBCData:
        data = []  # Shape: (569, 30)
        target = []  # Shape: (569, )
        target_names = ['malignant', 'benign']
        feature_names = ['mean radius', 'mean texture', 'mean perimeter', 'mean area', 'mean smoothness',
                         'mean compactness', 'mean concavity', 'mean concave points', 'mean symmetry', 
                         'mean fractal dimension', 'radius error', 'texture error', 'perimeter error', 
                         'area error', 'smoothness error', 'compactness error', 'concavity error', 
                         'concave points error', 'symmetry error', 'fractal dimension error', 'worst radius', 
                         'worst texture', 'worst perimeter', 'worst area', 'worst smoothness', 
                         'worst compactness', 'worst concavity', 'worst concave points', 'worst symmetry', 
                         'worst fractal dimension']
    
    wdbc = WDBCData()
    with open(filename) as f:
        for line in f.readlines():
            items = line.strip().split(',')
            # 'M'은 0으로, 'B'는 1로 설정
            wdbc.target.append(0 if items[1] == 'M' else 1)
            # 30개 속성을 float 형으로 변환하여 저장
            wdbc.data.append([float(x) for x in items[2:]])
    
    wdbc.data = np.array(wdbc.data)
    wdbc.target = np.array(wdbc.target)
    return wdbc

# 데이터 로드
wdbc = load_wdbc_data('C:/Users/kimalogo/Documents/GitHub/UNIV_OSS/8주차 과제/data/wdbc.data')

# 모델 학습 - RandomForestClassifier 사용
model = RandomForestClassifier(random_state=42)  # 랜덤 상태 고정
model.fit(wdbc.data, wdbc.target)

# 모델 테스트
predict = model.predict(wdbc.data)
accuracy = metrics.balanced_accuracy_score(wdbc.target, predict)

# 혼동 행렬 시각화
conf_matrix = metrics.confusion_matrix(wdbc.target, predict)
metrics.ConfusionMatrixDisplay(conf_matrix, display_labels=wdbc.target_names).plot(cmap='viridis')
plt.title("Confusion Matrix")
plt.show()

# 선택된 특징에 대한 산점도 시각화
cmap = np.array([(1, 0, 0), (0, 1, 0)])  # 빨강, 초록 색상
clabel = [Line2D([0], [0], marker='o', lw=0, label=wdbc.target_names[i], color=cmap[i]) for i in range(len(cmap))]
for (x, y) in [(0, 1)]:  # 두 개의 특징 사용
    plt.figure()
    plt.title(f'My Classifier (Accuracy: {accuracy:.3f})')
    plt.scatter(wdbc.data[:, x], wdbc.data[:, y], c=cmap[wdbc.target], edgecolors=cmap[predict])
    plt.xlabel(wdbc.feature_names[x])
    plt.ylabel(wdbc.feature_names[y])
    plt.legend(handles=clabel, framealpha=0.5)
    plt.show()
