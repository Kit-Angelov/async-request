import select
import sys
import os

loop = True

w, rr = os.popen4('ping google.com -c 5') # запускаем процесс
# добавляем в список стандартный ввод
# и поток с чтением результата запущенного процесса
input = [ sys.stdin, rr]

while loop:
    r,w,e = select.select(input, [], []) # функция опроса устройств
    for op in r:
        if op == sys.stdin:
            print(':',op.readline().rstrip())
        else:
            s = op.readline()
            # получать больше нечего, удаляем из списка опрашиваемых
            if not s: input.remove(op)
            else:
                print('>',s.rstrip())