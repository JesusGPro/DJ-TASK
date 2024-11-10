chapter_totals= {'1': '0.00', '2': '0.00', '3': '137,056,857.64'}

print(chapter_totals['1'])

key = 3
key_str = str(key)

print(chapter_totals.get(key_str, 'N/A'))