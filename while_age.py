#!/usr/bin/env python
# _*_ coding: utf-8 _*_
"""
作者:qtwaiter
日期:2020年12月22日

"""
age_of_oldboy = 56
count = 0
while count < 3:

    guess_age = int(input('guess age: '))

    if guess_age == age_of_oldboy:
        print('Yes,you got it!')
        break
    elif guess_age > age_of_oldboy:
        print('think smaller...')
    else:
        print('think bigger!')
    count +=1
    if count == 3:
        continue_confirm = input('Do you want to keep guessing..? type any key for continue and n for quit.')
        if continue_confirm != 'n':
            count = 0
else:
    print('You have tried too many times....fuck off')
