import matplotlib.pyplot as plt

def read_data(filename):
    data = []
    with open(filename, 'r') as f:
        for line in f.readlines():
            if not line.startswith('#'):
                data.append([int(word) for word in line.split(',')])
    return data

if __name__ == '__main__':
    class_kr = read_data('./5주차 과제/data/class_score_kr.csv')
    class_en = read_data('./5주차 과제/data/class_score_en.csv')

    midterm_kr, final_kr = zip(*class_kr)
    total_kr = [40/125 * midterm + 60/100 * final for (midterm, final) in class_kr]

    midterm_en, final_en = zip(*class_en)
    total_en = [40/125 * midterm + 60/100 * final for (midterm, final) in class_en]

    skypurple = '#9b6ef3'

    plt.figure(figsize=(10, 5))

    plt.subplot(1, 2, 1)
    plt.scatter(midterm_kr, final_kr, color='red', label='Korean', marker='o')
    plt.scatter(midterm_en, final_en, color='blue', label='English', marker='+')
    plt.xlim(0, 125)
    plt.ylim(0, 100)
    plt.grid(True)
    plt.xlabel('Midterm scores')
    plt.ylabel('Final scores')
    plt.title('Midterm vs Final scores')
    plt.legend()

    plt.subplot(1, 2, 2)
    plt.hist(total_kr, bins=range(0, 101, 5), alpha=0.7, label='Korean', color='red')
    plt.hist(total_en, bins=range(0, 101, 5), alpha=0.7, label='English', color=skypurple)
    plt.xlim(0, 100)
    plt.xlabel('Total scores')
    plt.ylabel('The number of students')
    plt.title('Total scores distribution')
    plt.legend()

    plt.tight_layout()
    plt.show()
