import pandas as pd
import novotar_parser


class Data:
    pd.options.display.max_rows = 200

    def __init__(self):
        self.group_average = []
        self.group_score = []
        self.__ls_of_groups = ['ФІОТ, ІВ-81.xls', 'ФІОТ, ІВ-82.xls', 'ФІОТ, ІВ-83.xls',
                               'ФІОТ, ІО-81.xls', 'ФІОТ, ІО-82.xls', 'ФІОТ, ІО-83.xls']
        self.__data = pd.DataFrame()
        for i in self.__ls_of_groups:
            x = pd.read_excel(i)
            self.__data = pd.concat([self.__data, x], ignore_index=True, sort=False)
        first = pd.Series(self.__data['бал'])
        self.__data = self.__data.drop(['бал'], axis='columns')
        second = pd.Series(self.__data[' бал'])
        self.__data = self.__data.drop([' бал'], axis='columns')
        self.__data['Бал'] = pd.concat([first.dropna(), second.dropna()])

    @classmethod
    def __number_validator(cls, number):
        digits = number.split(',')
        res = int(digits[0])
        return res

    def norm_distribution(self, step=5):
        all_marks = [Data.__number_validator(self.__data.iloc[i]['Бал']) for i in range(self.__data.shape[0])]
        highest_point = max(all_marks) + 6
        norm_distribution_dict = {i: 0 for i in range(0, highest_point)}
        for i in range(self.__data.shape[0]):
            number = Data.__number_validator(self.__data.loc[i]["Бал"])
            norm_distribution_dict[number] += 1
        keys = list(norm_distribution_dict.keys())
        rng = tuple(range(0, highest_point, step))
        for j in range(len(rng) - 1):
            low, high = rng[j], rng[j + 1] - 1
            current_keys = [i for i in keys if low <= i <= high]
            summ = 0
            for i in range(len(current_keys)):
                summ += norm_distribution_dict[current_keys[i]]
            column = '*' * summ
            print("Marks from {0:>02} to {1:>02}: {2}".format(low, high, column))

    def group_score_and_average(self):
        ls_group_score = []
        aver_score_groups = []
        for i in self.__ls_of_groups:
            res = 0
            num_students = 0
            for j in range(len(self.__data)):
                if self.__data.iloc[j]['Група'] == i[:-4]:
                    res += int(self.__data.iloc[j]['Бал'][:-2])
                    num_students += 1
            ls_group_score.append({i[:-4]: res})
            aver_score_groups.append({i[:-4]: "{:.3f}".format(res / num_students)})
        self.group_score = ls_group_score
        self.group_average = aver_score_groups

    def all_rating(self):
        self.__data["Бал"] = self.__data["Бал"].apply(Data.__number_validator)
        self.__data = self.__data.sort_values("Бал")
        print("General rating")
        j = 0
        print("Place  Mark  Name")
        for i in range(self.__data.shape[0]-1, 0, -1):
            j += 1
            name = self.__data.iloc[i]["ДМ"]
            mark = self.__data.iloc[i]["Бал"]
            print("{:<6} {:<5} {}".format(j, mark, name))

    def statistics(self, step_for_normal_distribution=5):
        """
        :param step_for_normal_distribution:
        Range of points for showing normal distribution, optimal choice is  from 5 to 10
        :return:
        Prints sum of group marks, group's GPA and normal distribution of marks
        """
        self.group_score_and_average()
        print("Info:\n" + "-" * 30)
        print("Sum of marks:")
        for i in self.group_score:
            group = list(i.keys())[0]
            mark = list(i.values())[0]
            print("{}: {:>4}".format(group, mark))
        print("-" * 30 + "\n" + "Grade point average")
        for i in self.group_average:
            group = list(i.keys())[0]
            mark = list(i.values())[0]
            print("{} - {}".format(group, mark))
        print("-" * 30 + "\n" + "Normal distribution:")
        self.norm_distribution(step_for_normal_distribution)
        print("-"*30)
        self.all_rating()


def main():
    data = Data()
    data.statistics()


if __name__ == '__main__':
    # novotar_parser.main()
    main()
