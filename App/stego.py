from App import models
from flask import Flask, render_template, redirect, url_for
import os


stego_text = ''  # dùng để ghép chuỗi lại với nhau
encryp_table = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K',
                'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', ' ', '!', '"', '#', '$', '%',
                '&', '\'', '(', ')', '*', '+', ',', '-', '.', '/', ':', ';', '<', '=', '>', '?', '@', '[', '\\', ']',
                '^', '_', '`', '{', '|', '}', '~']

encryp_table = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K',
                'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', ' ', '!', '"', '#', '$', '%',
                '&', '\'', '(', ')', '*', '+', ',', '-', '.', '/', ':', ';', '<', '=', '>', '?', '@', '[', '\\', ']',
                '^', '_', '`', '{', '|', '}', '~']


def adjust_enter(content):
    content = content.replace("\n ", "\n")
    content = content.replace("\n  ", "\n")
    return content


def ma_hoa_thong_diep(thong_diep=None):
    arr_thong_diep = []
    if thong_diep:
        arr_thong_diep = list(
            thong_diep.upper())  # cắt 1 mảng chữ in hoa thành các kí tự, ví dụ: ['H', 'I', 'E', 'N', 'V', 'Y']
    else:
        'Ban chua nhap thong diep'

    s = ''
    for c in arr_thong_diep:
        if c in encryp_table:
            s += bin(encryp_table.index(c))[2:].zfill(
                8)  # tìm xem ký tự cần giấu nằm ở đâu trong chuỗi, lấy cái số index đó mã hoá nhị phân 8 bit

    return s  # trả về chuỗi gồm mã nhị phân, ví dụ: '00010110101011110000'


def tach_chuoi(text=None, key=None):  # phải kiểm tra khoá >=2 ở 1 chỗ nào đó
    arr_tach_chuoi = list(text)  # cắt văn bản thành các kí tự
    arr_chuoi_con = []
    chuoicon = ''
    dem = 0

    for c in arr_tach_chuoi:
        chuoicon += c  # cộng các ký tự lại với nhau
        if c == " " and chuoicon != "":
            try:
                if chuoicon[-2] == " ":
                    continue
            except:
                pass

        if c == ' ':
            dem = dem + 1

        if dem == key:  # cộng cho tới khi có key khoảng trống
            dem = 0
            arr_chuoi_con.append(chuoicon)  # ta gắn chuỗi đó trở thành 1 phần tử của mảng arr_chuoi_con, ví dụ: ['nguyen thi hien ', 'vy hoc nganh ', 'cong nghe thong ', 'tin']
            chuoicon = ''  # reset chuỗi con trở thành chuỗi rỗng để bắt đầu cộng tiếp

    return arr_chuoi_con  # trả về mảng gần các chuỗi con gồm key khoảng trống


def dieu_kien(cover_text,
              ma, k):  # hàm kiểm tra xem văn bản dùng để giấu thông tin có ủ điều kiện để giấu thông điệp không
    a = len(tach_chuoi(cover_text, k))
    b = len(ma_hoa_thong_diep(ma))
    if a > b:  # phải lớn hơn vì chuỗi cuối cùng k kiểm soát chuỗi cuối có mấy khoảng trống, nếu ít hơn2 th k thể giấu
        return True
    else:
        return False


def nhung(chuoi_nhi_phan=None, chuoi_con=None):  # nhúng các bit nhị phân vào văn bản
    dem = 0
    idx = 0
    for n in chuoi_nhi_phan:  # chạy vòng lặp cho đến khi giấu hết bit nhị phân
        if n == '0':  # nếu là bit 0
            dem2 = 0
            dem3 = 0

            for c in chuoi_con[dem]:

                if c == ' ':
                    dem2 += 1
                if dem2 == 2:  # nếu đến khoảng trống thứ 2 thì thêm khoảng trống
                    chuoi_con[dem] = chuoi_con[dem][:dem3] + ' ' + chuoi_con[dem][dem3:]
                    break  # thêm xong thì dừng luôn không cần chạy tiếp trong chuỗi
                dem3 += 1  # cái này dùng để đếm xem trong chuỗi con mấy kí tự thì đến khoảng trống sau đó cắt ra ghép lại tại đó
            idx += len(chuoi_con[dem])
        else:  # nếu là bit 1
            dem4 = 0

            for c in chuoi_con[dem]:
                if c == ' ':  # bit 1 thì đến khoảng trống đầu tiên thì thêm khoảng trống luôn rồi dừng vòng lặp luôn
                    chuoi_con[dem] = chuoi_con[dem][:dem4] + ' ' + chuoi_con[dem][dem4:]
                    break
                dem4 += 1
            idx += len(chuoi_con[dem])
        dem += 1
        # print(''.join(chuoi_con)) # print tại màn hình console vì khi in lên màn web các khoảng trống bị reset lại thành cách nhau bằng 1 khoảng trống, dùng thư viện jinja2 import Markup để giữ nhưng chưa import được
    s = ''.join(chuoi_con)
    # print(s[:idx]+":")
    s = s[:idx] + "   " + s[idx + 1:]
    return s  # trả về chuỗi con đã được giấu thông điệp


def giai_ma_nhi_phan(text=None, key=None):
    arr_chuoi_con_gm = tach_chuoi(text, key)

    stri = ''

    for t in arr_chuoi_con_gm:
        if not t.__contains__("  "):
            return stri
        dem = 0  # dem cho so cap bit
        dem1 = 0  # dem cho khoang cach

        for c in t:
            if c == ' ':
                dem += 1
                #print("Message:", t[dem1 + 1], t[dem1 + 2])
                #if t[dem1 + 1] == ' ' and t[dem1 + 2] == " ":
                #    return stri
                if t[dem1 + 1] == ' ':
                    stri = stri + '1'
                else:
                    stri = stri + '0'
                break

            dem1 += 1

    return stri


def giai_thong_diep(stri=None):
    s = []
    s1 = ''
    for i in stri:
        s1 += i
        if len(s1) == 8:
            s.append(encryp_table[int(s1, 2)])
            s1 = ''

    return "".join(s)