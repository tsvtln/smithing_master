# data = [
#     "X 746 / Y 434 / W 74 / H 74",
#     "X 826 / Y 434 / W 74 / H 74",
#     "X 906 / Y 434 / W 74 / H 74",
#     "X 986 / Y 434 / W 74 / H 74",
#     "X 1066 / Y 434 / W 74 / H 74",
#     "X 746 / Y 514 / W 74 / H 74",
#     "X 826 / Y 514 / W 74 / H 74",
#     "X 906 / Y 514 / W 74 / H 74",
#     "X 986 / Y 514 / W 74 / H 74",
#     "X 1066 / Y 514 / W 74 / H 74",
#     "X 746 / Y 594 / W 74 / H 74",
#     "X 826 / Y 594 / W 74 / H 74",
#     "X 906 / Y 594 / W 74 / H 74",
#     "X 986 / Y 594 / W 74 / H 74",
#     "X 1066 / Y 594 / W 74 / H 74",
#     "X 746 / Y 594 / W 74 / H 74",
#     "X 826 / Y 594 / W 74 / H 74",
#     "X 906 / Y 594 / W 74 / H 74",
#     "X 986 / Y 594 / W 74 / H 74",
#     "X 1066 / Y 594 / W 74 / H 74",
#     "X 746 / Y 675 / W 74 / H 74",
#     "X 826 / Y 675 / W 74 / H 74",
#     "X 906 / Y 675 / W 74 / H 74",
#     "X 986 / Y 675 / W 74 / H 74",
#     "X 1066 / Y 675 / W 74 / H 74",
#     "X 746 / Y 755 / W 74 / H 74",
#     "X 826 / Y 755 / W 74 / H 74",
#     "X 906 / Y 755 / W 74 / H 74",
#     "X 986 / Y 755 / W 74 / H 74",
#     "X 1066 / Y 755 / W 74 / H 74",
#     "X 746 / Y 835 / W 74 / H 74",
#     "X 826 / Y 835 / W 74 / H 74",
#     "X 906 / Y 835 / W 74 / H 74",
#     "X 986 / Y 835 / W 74 / H 74",
#     "X 1066 / Y 835 / W 74 / H 74"
# ]
#
# # Convert the strings to tuples
# coordinates_list = []
# for line in data:
#     parts = line.split()
#     x = int(parts[1])
#     y = int(parts[4])
#     w = int(parts[7])
#     h = int(parts[10])
#     coordinates_tuple = (x, y, x + w, y + h)
#     coordinates_list.append(coordinates_tuple)
#
# # Print the resulting list of tuples
# print(coordinates_list)

# filename = "board_icon_01.png"
#
# parts = filename.split("_")[1:]
# new_name = "_".join(parts)[:-4]
#
# print(new_name)
