def read_data(filename):
    # TODO) Read `filename` as a list of integer numbers
    data = []
    with open(filename,'r') as file:
        for line in file:
            if line and line[0].startswith("#"):
                continue
            line=line.strip()
            m_score,f_score = map(int,line.split(','))
            data.append((m_score,f_score))
    return data

def calc_weighted_average(data_2d, weight):
    # TODO) Calculate the weighted averages of each row of `data_2d`
    average = []
    for ((m_score, f_score)) in (data_2d):
        average.append(m_score*weight[0]+f_score*weight[1])
    return average

def analyze_data(data_1d):
    # TODO) Derive summary of the given `data_1d`
    # Note) Please don't use NumPy and other libraries. Do it yourself.
    mean = 0
    var = 0
    median = 0
    total = 0
    len_arr= len(data_1d)
    for item in data_1d:
        total+=item
    mean = total/len_arr

    vsum = 0
    for val in data_1d:
        vsum += (val - mean) ** 2
    var = vsum / len_arr
    sorted_data = sorted(data_1d)
    if len_arr % 2 == 1:
        median = sorted_data[len_arr // 2]
    else:
        mid1 = sorted_data[len_arr // 2 - 1]
        mid2 = sorted_data[len_arr // 2]
        median = (mid1 + mid2) / 2   
    return mean, var, median, min(data_1d), max(data_1d)

if __name__ == '__main__':
    data = read_data('./data/class_score_en.csv')
    if data and len(data[0]) == 2: # Check 'data' is valid
        average = calc_weighted_average(data, [40/125, 60/100])

        # Write the analysis report as a markdown file
        with open('./data/class_score_analysis.md', 'w') as report:
            report.write('### Individual Score\n\n')
            report.write('| Midterm | Final | Average |\n')
            report.write('| ------- | ----- | ----- |\n')
            for ((m_score, f_score), a_score) in zip(data, average):
                report.write(f'| {m_score} | {f_score} | {a_score:.3f} |\n')
            report.write('\n\n\n')

            report.write('### Examination Analysis\n')
            data_columns = {
                'Midterm': [m_score for m_score, _ in data],
                'Final'  : [f_score for _, f_score in data],
                'Average': average }
            for name, column in data_columns.items():
                mean, var, median, min_, max_ = analyze_data(column)
                report.write(f'* {name}\n')
                report.write(f' * Mean: **{mean:.3f}**\n')
                report.write(f' * Variance: {var:.3f}\n')
                report.write(f' * Median: **{median:.3f}**\n')
                report.write(f' * Min/Max: ({min_:.3f}, {max_:.3f})\n')