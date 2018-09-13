import csv
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
import datetime as dt


def bar_diagram(file_in, file_out):
    """
    Saves the bar diagram of the number of shows in function of the date to file_out with the data of file_in.
    """
    with open(file_in, 'r') as f:
        next(f)
        reader = csv.reader(f)
        n = 0
        dates_x = []
        count_y = []
        pre_month = 0
        i = 0

        for row in reader:
            n += 1
            date = row[1]
            year = int(date[6:10])
            month = int(date[3:5])

            if pre_month == month:
                count_y[i - 1] += 1
            else:
                dates_x.append(date[3:5] + "/" + date[6:10])
                count_y.append(1)
                i += 1
            pre_year, pre_month = year, month

        plt.rcParams["figure.figsize"] = [20, 10]
        plt.bar(dates_x[::-1], count_y[::-1])
        plt.text(17.5, 125, "Total: " + str(n), fontsize=15)
        plt.ylabel("Number of shows")
        plt.savefig(file_out)



def matrix_init():
    """
    Returns a 52*7 matrix filled with 0.
    """
    M = []
    for n in range(52):
        M.append([0, 0, 0, 0, 0, 0, 0])
    return np.array(M)


def dataset_reduction(fname):
    """
    Returns a .csv file with only the data from the past year.
    """
    today = dt.date.today()
    year = today.year
    month = today.month
    day = today.day
    max_d = (year, month, day)
    min_d = (year - 1, month, day)

    with open(fname, 'r') as f, open('C:/Users/Médéric Carriat/Documents/Projets/netflix-data-analysis-master/Data/out.csv','w') as f_out:
        next(f)
        reader = csv.reader(f)
        for row in reader:
            r_date = row[1]
            d = int(r_date[6:10]), int(r_date[3:5]), int(r_date[0:2])
            if min_d <= d <= max_d:
                writer = csv.writer(f_out)
                writer.writerow(row)


def matrix(fname):
    """
    Returns a tuple of a matrix containing the number of episodes per day and another tuple containing the position of the first day.
    """
    A = matrix_init()
    s = 0
    month = 0
    tick_pos = 0
    not_found = True
    shift = dt.date.today().isocalendar()[1]
    dataset_reduction(fname)


    with open("C:/Users/Médéric Carriat/Documents/Projets/netflix-data-analysis-master/Data/out.csv", 'r') as f:
        reader = csv.reader(f)

        # To catch the first line in order to initialize pre_date, pre_day and the counter c
        for row in reader:
            pre_date = row[1]
            pre_day = int(pre_date[0:2])
            last_day = dt.datetime(int(row[1][6:10]), int(row[1][3:5]), int(row[1][0:2]))
            c = 1
            break

        for row in reader:
            if row:  # No idea why half the rows are empty
                date = dt.datetime(int(row[1][6:10]), int(row[1][3:5]), int(row[1][0:2]))
                day = date.day

                if day == 1 and not_found:
                    month = date
                    tick_pos = (date.isocalendar()[1] + (52-shift)) % 52
                    not_found = False

                if pre_day == day:
                    c += 1
                else:
                    j = (pre_date.isocalendar()[1] + (52-shift)) % 52  # The coordinates in the matrix are the week number
                    i = pre_date.weekday()                 # and the weekday
                    A[j][i] = c
                    s += c
                    c = 1
                pre_day = day
                pre_date = date
            else:
                pass
        first_day = date
    B = np.array(A)
    return np.swapaxes(B, 0, 1), month, tick_pos, first_day, last_day, s


def heatmap_save(file_in, file_out):
    """
    Saves the heatmap representing the number of shows watched per day during a year to file_out with the data of file_in.
    """

    data, date, tick_pos, first_day, last_day, s = matrix(file_in)
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    ticks = []
    months = []

    ticks.append(tick_pos)
    months.append(date.strftime("%b"))
    month_num = date.month
    for i in range(1, 12):
        tick_pos = (tick_pos + 4.3) % 52
        ticks.append(tick_pos)
        month_num = (month_num + 1) % 12
        if month_num == 0:
            month_num = 12
        next_month = dt.datetime(2015, month_num, 1).strftime("%b")
        months.append(next_month)

    fig, ax = plt.subplots(figsize=(9, 3.5))
    im = ax.imshow(data)

    ax.set_yticks(np.arange(len(days)))
    ax.set_yticklabels(days)
    plt.tick_params(labelsize=5)

    ax.set_xticklabels(months)
    ax.xaxis.set_major_locator(ticker.FixedLocator(ticks))

    cbar = ax.figure.colorbar(im, ax=ax, orientation='horizontal')
    cbar.ax.set_xlabel("Number of shows per day between " + first_day.strftime("%Y-%m") + " and " + last_day.strftime("%Y-%m"), va="top")
    plt.savefig.dpi: 10
    plt.text(46, -3, "Total: " + str(s), fontsize=8)

    plt.savefig(file_out)
    plt.show()
    print("Saved to: " + file_out)
