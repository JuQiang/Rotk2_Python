import Data

# game_start_new_ruler_birthday_info, line 37868 call --->
data.buf[0xCB1d] = month # game_start_new_ruler_month_born , line 36568
data.buf[0xCAEA] = day # game_start_new_ruler_day_born, line 36640
data.buf[0XCAA0] = age # game_start_new_ruler_enter_age, line 37665

data.buf[0x2B11] = (month*day) % 0x65 # xiangxing, game_start_new_game_sub_2, line 34206
data.buf[0xCB1E] = sex # game_start_new_ruler_enter_sex, line 37871, 1 means male, 2 means female

# BX=2B02, customized ruler
data.buf[BX+7] = yili #line 34210 ~ 34225, a random number + 0x50
data.buf[BX+8] = rende #line 34210 ~ 34225, a random number + 0x50
data.buf[BX+9] = yewang #line 34210 ~ 34225, a random number + 0x50

data.buf[0xCE95] = follower_age # game_start_new_ruler_add_follower, line 37483
data.buf[0xCE94] = follower_sex # game_start_new_ruler_enter_sex, line 37871, 1 means male, 2 means female

now: 34282