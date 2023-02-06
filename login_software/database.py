import csv
# name, id, pw, email, birthday, MAC id = order
i = 0
j = 0
users = [[], [], [], [], [], [], []]
with open('data.csv', 'r') as file:
    csv_reader = csv.reader(file)

    next(csv_reader)

    # for i in range(sum(1 for row in csv_reader)):
    #     users[5].append([])
    #     users[6].append([])

    for line in csv_reader:
        if len(line) > 0:
            try:
                users[5].append([])
                users[6].append([])
                print(line)
                users[0].append(line[0])
                users[1].append(line[1])
                users[2].append(line[2])
                users[3].append(line[3])
                users[4].append(line[4])
                for i in range(100):
                    try:
                        if i % 2 == 1:
                            users[5][j].append(line[5].split("'")[i])
                            users[6][j].append(line[6].split("'")[i])

                    except IndexError:
                        pass
            except IndexError:
                pass
            j += 1

# user_name, rank, room_pw = order
star_wars_pre = [[], [], []]
star_wars_se = [[], [], []]
lord_of_the_ring = [[], [], []]
marvel = [[], [], []]