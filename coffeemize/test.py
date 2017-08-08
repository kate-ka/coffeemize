# def index_power(array, n):
#     """
#         Find Nth power of the element with index N.
#     """
#     try:
#         return (pow(array[n], n))
#     except IndexError:
#         return (-1)
#
#
#
#
# if __name__ == '__main__':
#     #These "asserts" using only for self-checking and not necessary for auto-testing
#     assert index_power([1, 2, 3, 4], 2) == 9, "Square"
#     assert index_power([1, 3, 10, 100], 3) == 1000000, "Cube"
#     assert index_power([0, 1], 0) == 1, "Zero power"
#     assert index_power([1, 2], 3) == -1, "IndexError"
#
#
# array = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
# l=[]
# print([array[i] for i in range(0, len(array), 2)])



# def checkio(array):
#     """
#         sums even-indexes elements and multiply at the last
#     """
#     if array:
#         return sum([array[i] for i in range(0, len(array), 2)]) * array[len(array) -1]
#     return 0
#
# #These "asserts" using only for self-checking and not necessary for auto-testing
# if __name__ == '__main__':
#     assert checkio([0, 1, 2, 3, 4, 5]) == 30
#     assert checkio([1, 3, 5]) == 30
#     assert checkio([6]) == 36
#     assert checkio([]) == 0
#
# import re
#
#
# def checkio(words):
#     return re.search('([A-Za-z]+\s[A-Za-z]+\s[A-Za-z]+\s?)', words)
# words = "Hi 9000"
#
# print(checkio(words))

# def checkio(*args):
#     return min(args)
#
# print(checkio(1, 2, 3))

def checkio(str_number, radix):
    characters = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    result = 0
    i = len(str_number)-1
    for item in str_number:
        if characters.index(item) < radix:
            converted = characters.index(item) * radix ** i
            i -= 1
            result += converted
        else:
            return -1
    return result


print(checkio("Z",36))